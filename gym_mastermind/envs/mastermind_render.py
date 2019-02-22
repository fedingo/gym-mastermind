import pygame
import time
import numpy as np

import os
import sys
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50)

gray =  (150, 150, 150)
white = (255, 255, 255)
black = (  0,   0,   0)
red =   (255,   0,   0)
yellow= (255, 255,   0)

color_codebook = {
	0 : (  0,   0, 255),
	1 : (  0, 255,   0),
	2 : (255, 255,   0),
	3 : (  0, 255, 255),
	4 : (255,   0, 255),
	5 : (255, 128,   0),
	6 : (165,  42,  42),
	7 : (232, 232, 232),	
}


screen = None
ROW = 50
BORDER = 5
BALL_RADIUS = 18
TINY_RADIUS = 8
MARGIN = 5
LINE = 1


def __draw_code(list, h):
	for i, val in enumerate(list):
		color = color_codebook[val]
		pos = [MARGIN + ROW//2 + i*ROW, MARGIN + ROW//2 + h*ROW]
		
		pygame.draw.circle(screen, color, pos, BALL_RADIUS)

def __draw_result(list, k, h):
	for i, el in enumerate(list):
		pos = [MARGIN + k*ROW + ROW//4, MARGIN + LINE + ROW//4 + h*ROW]
		
		#Shift to draw in a square
		if i > 1:
			pos[1] += ROW//2
		if i % 2 == 1:
			pos[0] += ROW//2

		color = None; reduce = 0
		if el == 2:
			color = red
		elif el == 1:
			color = white
		else:
			color = black
			reduce = -2

		pygame.draw.circle(screen, color, pos, TINY_RADIUS + reduce)

def render_mastermind(game_object):

	array = game_object.internal_state
	k, h = game_object.size, game_object.max_guesses

	global screen 
	if screen is None:
		pygame.init()
		screen = pygame.display.set_mode((2*MARGIN+(k+1)*ROW, 2*MARGIN+(h+1)*ROW))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.display.quit()
			pygame.quit()
			sys.exit(0)

	screen.fill(black)

    # first we draw the background
	# 1 more for the target visualization
	for y in range(0,h+1):
		        # Draw the background with the grid pattern
		pygame.draw.rect(screen, black, pygame.Rect(MARGIN, MARGIN + y*ROW, (k+1)*ROW, ROW))

		if y != h:
			#Guess Row
			pygame.draw.rect(screen, gray , pygame.Rect(MARGIN + LINE,MARGIN + y*ROW + LINE,
		                                            k*ROW - 2*LINE, ROW - 2*LINE))
			#Result Block
			pygame.draw.rect(screen, gray , pygame.Rect(MARGIN + k*ROW, MARGIN + y*ROW + LINE,
		                                        	   ROW - 2*LINE, ROW - 2*LINE))

		else:
			pygame.draw.rect(screen, yellow , pygame.Rect(MARGIN + LINE,MARGIN + y*ROW + LINE,
		                                            k*ROW - 2*LINE, ROW - 2*LINE))

			pygame.draw.rect(screen, gray , pygame.Rect(MARGIN + 3*LINE,MARGIN + y*ROW + 3*LINE,
		                                            k*ROW - 6*LINE, ROW - 6*LINE))

	
	for index, (code_try, result) in enumerate(array):
		__draw_code(code_try,    index)
		__draw_result(result, k, index)


	__draw_code(game_object.target, h)

	pygame.display.update()


if __name__ == "__main__":
	from mastermind_class import *
	game = mastermind()
	render_mastermind(game)
	print("Target: %s" % game.target)
	time.sleep(1)
	
	for i in range(20):
		guess = np.random.randint(game.symbols, size=game.size)
		done, _ = game.step(guess)
		print("%d) %s" % (i,guess))
		render_mastermind(game)
		time.sleep(1)

		if done:
			game.reset()
