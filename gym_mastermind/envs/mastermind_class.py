import numpy as np
from collections import Counter


# Class that incapsulate the game logic 

class mastermind():



	def __init__(self, symbols_count, size, max_guess):

		self.symbols = symbols_count
		self.size = size
		self.max_guesses = max_guess
		self.reset()

	def reset(self):

		self.target = np.random.randint(self.symbols, size=[self.size])
		self.guess_count = 0
		self.internal_state = []
		self.is_finished = False
		self.found_combination = False

    # Suppose that action is a valid action (same length of target and same amount of possible symbols)
    #
    # The match is returned as a set of 4 values with the following meaning:
    #	- 2 means that a number is an exact match
    #	- 1 means that a number is correct but in the wrong place
    #	- 0 means that a number is wrong
	def __match(self, action):

		exact_match = (self.target == action)

		if exact_match.all():
			return np.array([2]*self.size) # Exact result

		not_matches = [not x for x in exact_match]
		action_left = action[not_matches]
		target_left = list(self.target[not_matches]) # It's easier to remove elements from a list

		red_count = np.sum(exact_match) #Count the exact matches by summing the True values (True == 1)

		# We count how many of the non-exact matches have the same values (right number but wrong position)
		white_count = 0
		for value in action_left:
			if value in target_left:
				target_left.remove(value) # we remove to not count multiple times if there are repetitions
				white_count += 1

		mistakes = self.size - red_count - white_count

		return np.array([2]*red_count + [1]*white_count + [0]*mistakes)

	## Function that allows to perform an action in the game
	# Returns a tuple of booleans where the first is True if the game is Finished
	# and the second is True if we have guessed the right combination
	def step(self, action):

		if self.is_finished:
			raise Exception("Cannot try any more, the game is over!")

		if not type(action) == type(np.array([])):
			action = np.array(action) 

		self.guess_count += 1
		match_result = self.__match(action)
		self.internal_state += [(action, match_result)]


		if (match_result == 2).all():
			self.is_finished = True
			self.found_combination = True
		if (self.guess_count >= self.max_guesses):
			self.is_finished = True

		return self.is_finished, self.found_combination

	def get_state(self):

		if len(self.internal_state) == 0:
			return None

		return np.concatenate(self.internal_state[-1])

# TESTING
if __name__ == "__main__":

	obj = mastermind()

		