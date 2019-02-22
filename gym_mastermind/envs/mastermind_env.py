
import gym
from gym.utils import seeding
from gym import spaces

import numpy as np
from gym_mastermind.envs.mastermind_class import *
from gym_mastermind.envs.mastermind_render import *

## DEFAULT VALUES
SYMBOLS_COUNT = 8
SIZE = 4
MAX_GUESS = 12

class MastermindEnv(gym.Env):


    def __init__(self):
        
        self.game = mastermind(SYMBOLS_COUNT, SIZE, MAX_GUESS)

        self.symbols     = SYMBOLS_COUNT
        self.size        = SIZE
        self.max_guesses = MAX_GUESS

        self.seed()
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        #Assertion to check Action is valid
        assert self.action_space.contains(action)
        
        done, solved = self.game.step(action)
        state = self.game.get_state()
        # Reward Function that gives 1 only if we guess the combination correctly 
        reward = 0
        if solved:
            reward = 1
        # In the additional info we give the number of tries that has been done
        add_info = {"guess_count": self.game.guess_count}

        return state, reward, done, add_info 

    def reset(self):

        # Used to change values if the user wants to modify the game parameters
        self.game.symbols = self.symbols
        self.game.size = self.size
        self.game.max_guesses = self.max_guesses

        self.game.reset()

        self.obs_shape = [self.game.size*2]
        self.action_space = spaces.MultiDiscrete([self.game.symbols]*self.game.size)

        # The observation space is actually composed of a vector of twice the length of the guesses
        # The first half contains the guess that we have just made
        # The second half is the result of the query (containing 2,1,0) that indicates how many are correct
        self.observation_space = spaces.Box(low=0, high=self.game.symbols, shape=self.obs_shape, dtype=np.int)

    def render(self, mode='human', close=False):

        render_mastermind(self.game)
        if close:
            pygame.quit()


if __name__ == "__main__":
    import time

    env = MastermindEnv()
    env.game.symbols = 2
    _ = env.reset()

    print(env.action_space)

    for _ in range(0,100):
        _, reward, done, _ = env.step(env.action_space.sample())
        env.render()

        if done:
            env.reset()

        time.sleep(0.1)