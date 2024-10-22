#!/usr/bin/env python3

from abc import ABC, abstractmethod
import torch
import torch.nn.functional as torchf

from ..q_learning_environment.reward import REWARD_FUNCTION
from ..q_learning_parameters.settings import ENABLE_BACKWARD, ENABLE_STACKING, DQN_ACTION_SIZE, HIDDEN_SIZE, BATCH_SIZE, BUFFER_SIZE, DISCOUNT_FACTOR, \
                                 LEARNING_RATE, TAU, STEP_TIME, EPSILON_DECAY, EPSILON_MINIMUM, STACK_DEPTH, FRAME_SKIP
from ..q_learning_environment.environment import NUM_SCAN_SAMPLES


class OffPolicyAgent(ABC):
    def __init__(self, device, simulation_speed):

        self.device = device
        self.simulation_speed   = simulation_speed
        self.state_size         = NUM_SCAN_SAMPLES + 4
        self.action_size        = DQN_ACTION_SIZE
        self.hidden_size        = HIDDEN_SIZE
        self.input_size         = self.state_size * STACK_DEPTH if ENABLE_STACKING else self.state_size
        self.batch_size         = BATCH_SIZE
        self.buffer_size        = BUFFER_SIZE
        self.discount_factor    = DISCOUNT_FACTOR
        self.learning_rate      = LEARNING_RATE
        self.tau                = TAU
        self.step_time          = STEP_TIME
        self.loss_function      = torchf.smooth_l1_loss
        self.epsilon            = 1.0
        self.epsilon_decay      = EPSILON_DECAY
        self.epsilon_minimum    = EPSILON_MINIMUM
        self.reward_function    = REWARD_FUNCTION
        self.backward_enabled   = ENABLE_BACKWARD
        self.stacking_enabled   = ENABLE_STACKING
        self.stack_depth        = STACK_DEPTH
        self.frame_skip         = FRAME_SKIP
        self.networks = []
        self.iteration = 0

    @abstractmethod
    def train():
        pass

    @abstractmethod
    def get_action():
        pass

    @abstractmethod
    def get_action_random():
        pass

    def _train(self, replaybuffer):
        batch = replaybuffer.sample(self.batch_size)
        tensors = [torch.from_numpy(sample).to(self.device) for sample in batch]
        result = self.train(*tensors)
        self.iteration += 1
        if self.epsilon and self.epsilon > self.epsilon_minimum:
            self.epsilon *= self.epsilon_decay
        return result

    def create_network(self, type, name):
        network = type(name, self.input_size, self.action_size, self.hidden_size).to(self.device)
        self.networks.append(network)
        return network

    def create_optimizer(self, network):
        return torch.optim.AdamW(network.parameters(), self.learning_rate)

    def hard_update(self, target, source):
        for target_param, param in zip(target.parameters(), source.parameters()):
            target_param.data.copy_(param.data)

    def soft_update(self, target, source, tau):
        for target_param, param in zip(target.parameters(), source.parameters()):
            target_param.data.copy_(target_param.data * (1.0 - tau) + param.data * tau)

    def get_model_configuration(self):
        configuration = ""
        for attribute, value in self.__dict__.items():
            if attribute not in ['actor', 'actor_target', 'critic', 'critic_target']:
                configuration += f"{attribute} = {value}\n"
        return configuration

    def get_model_parameters(self):
        parameters = [self.batch_size, self.buffer_size, self.state_size, self.action_size, self.hidden_size,
                            self.discount_factor, self.learning_rate, self.tau, self.step_time, REWARD_FUNCTION,
                            ENABLE_BACKWARD, ENABLE_STACKING, self.stack_depth, self.frame_skip]
        return ', '.join(map(str, parameters))

    def attach_visual(self, visual):
        self.actor.visual = visual

class Network(torch.nn.Module, ABC):
    def __init__(self, name, visual=None):
        super(Network, self).__init__()
        self.name = name
        self.visual = visual
        self.iteration = 0

    @abstractmethod
    def forward():
        pass

    def init_weights(n, m):
        if isinstance(m, torch.nn.Linear):
            torch.nn.init.xavier_uniform_(m.weight)
            m.bias.data.fill_(0.01)