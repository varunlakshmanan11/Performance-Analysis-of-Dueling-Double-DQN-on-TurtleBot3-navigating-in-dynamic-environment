# Importing necessary libraries
import numpy as  np
import torch
import torch.nn.functional as F
import torch.nn as nn
from ..q_learning_parameters.settings import DQN_ACTION_SIZE, TARGET_UPDATE_FREQUENCY

from .policy_agent import OffPolicyAgent, Network

# Linear Velocity and Angular Velocity
LINEAR = 0
ANGULAR = 1

POSSIBLE_ACTIONS = [[0.3, -1.0], [0.3, -0.5], [1.0, 0.0], [0.3, 0.5], [0.3, 1.0]]

# Reference for network structure: https://arxiv.org/pdf/1511.06581

# DuelingDQN architecture
class DuelingDQN(Network):
    def __init__(self, network_name, s_size, actor_size, h_size):
        super(DuelingDQN, self).__init__(network_name)
        
        # Defining the layers
        self.input1 = nn.Linear(s_size, h_size)
        self.input2 = nn.Linear(h_size, h_size)
        self.input3 = nn.Linear(h_size, h_size)
        self.input4 = nn.Linear(h_size, h_size)
        self.state_value = nn.Linear(h_size, 1)
        self.action_advantage = nn.Linear(h_size, len(POSSIBLE_ACTIONS))
        
        # Defining the activation function
        self.elu = nn.ELU(alpha = 1.0)
        
        # Initializing the weights
        self.apply(super().init_weights)
    
    # Forward pass
    def forward(self, states, visualize=False):
        
        # Forward pass through the layers
        f1 = self.elu(self.input1(states))
        f2 = self.elu(self.input2(f1))
        f3 = self.elu(self.input3(f2))
        f4 = self.elu(self.input4(f3))
        state_value = self.state_value(f4)
        action_advantages = self.action_advantage(f4)

        # Calculating the Q-value 
        q_value = state_value + (action_advantages - action_advantages.mean())

        # Visualizing the layers  
        if visualize and self.visual:
            action_selected = torch.from_numpy(np.asarray(POSSIBLE_ACTIONS[q_value.argmax().tolist()], np.float32))
            self.visual.update_layers(states, action_selected, [f1, f2], [self.input1.bias, self.input2.bias])
        
        # Returning the Q-value
        return q_value

# DuelingDQN agent
class DUELING_DQN(OffPolicyAgent):
    def __init__(self, device, sim_speed):
        super().__init__(device, sim_speed)
        
        # Defining the parameters
        self.actor_size = DQN_ACTION_SIZE
        self.possible_actions = POSSIBLE_ACTIONS
        self.target_update_frequency = TARGET_UPDATE_FREQUENCY
        
        # Defining the network
        self.actor = self.create_network(DuelingDQN, 'actor')
        self.actor_target = self.create_network(DuelingDQN, 'target_actor')
        self.optimizer = self.create_optimizer(self.actor)
        
        # Initializing the network
        self.hard_update(self.actor_target, self.actor)
    
    # Function to get the action
    def get_action(self, state, is_training, step=0, visualize=False):
        if is_training and np.random.random() < self.epsilon:
            return self.get_action_random()
        state = torch.from_numpy(np.asarray(state, np.float32)).to(self.device)
        Q_values = self.actor(state, visualize).detach().cpu()
        action = Q_values.argmax().tolist()
        return action
    
    # Getting the random action
    def get_action_random(self):
        return np.random.randint(0, self.actor_size)
    
    # Training the agent
    def train(self, state, action, reward, state_next, done):
        # Converting the state, action, reward, and state_next to tensors
        action = action.long().unsqueeze(1)
        # Calculating the Q by double DQN method
        with torch.no_grad():
            # Getting the next state actions from the policy network
            next_state_actions = self.actor(state_next).max(1,keepdim = True)[1]
        # Using the target actor to calculate the Q-values from the next state actions from the policy network
        Q_next = self.actor_target(state_next).gather(1, next_state_actions)
        # Calculating the Q-target
        Q_target = reward + (self.discount_factor * Q_next * (1 - done))
        # Getting the Q
        Q = self.actor(state).gather(1, action.long())
        # Calculating the loss
        loss = F.mse_loss(Q, Q_target)
        # Backpropagation and optimization
        self.optimizer.zero_grad()
        loss.backward()
        # Clipping the gradients
        nn.utils.clip_grad_norm_(self.actor.parameters(), max_norm=1.0, norm_type=1)
        self.optimizer.step()

        # Updating all target networks
        if self.iteration % self.target_update_frequency == 0:
            self.hard_update(self.actor_target, self.actor)
        return 0, loss.mean().detach().cpu()