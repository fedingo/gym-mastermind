import time
import gym
import gym_mastermind

env = gym.make('Mastermind-v0')

env.symbols = 4
_ = env.reset()

for _ in range(12):
	state, _, done, _ = env.step(env.action_space.sample())
	env.render()
	time.sleep(0.1)

	if done:
		_ = env.reset()