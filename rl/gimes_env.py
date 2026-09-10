import gymnasium as gym
from gymnasium import spaces
import numpy as np

action_space = spaces.Discrete(4)

state_space = spaces.Box(
    low=0,
    high=100,
    shape=(10,),
    dtype=float
)

class GIMES_Environment(gym.Env):

    def __init__(self):

        super().__init__()

        self.action_space = action_space
        self.observation_space = state_space

    def reset(self, seed=None, options=None):
    
            super().reset(seed=seed)
    
            self.state = np.zeros(10, dtype=float)
    
            return self.state, {}

    def step(self, action):

        reward = 0.0

        if action == 0:
            reward = 1.0
        else:
            reward = -1.0

        terminated = False
        truncated = False

        return self.state, reward, terminated, truncated, {}

env = GIMES_Environment()

print("Action space:", env.action_space)
print("Observation space:", env.observation_space)

state, info = env.reset()

print("Initial state:", state)
print("State shape:", state.shape)

next_state, reward, terminated, truncated, info = env.step(1)

print("Next state:", next_state)
print("Reward:", reward)
print("Terminated:", terminated)
print("Truncated:", truncated)
print("Info:", info)