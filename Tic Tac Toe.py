import pygame
import sys
import random
import time

class Input:
	def __init__(self):
		self.exit = False
		self.mouse_pressed = False

	def get_input(self):
		self.exit = False
		self.mouse_pressed = False
		self.space = False

		for event in pygame.event.get():

			if pygame.mouse.get_pressed()[0]:  # Left
				self.mouse_pressed = True

			if event.type == pygame.QUIT:
				self.exit = True

class Color:
	WHITE = (255,255,255)
	BLACK = (0,0,0)
	RED = (254,32,32)
	GREEN = (0,255,0)
	BLUE = (0,50,255)

def draw_circle(x, y, WIDTH, HEIGHT, screen, LINE_SIZE_OF_PLAYERS):
	pygame.draw.circle(screen, Color.BLUE, (x, y), 60)
	pygame.draw.circle(screen, Color.WHITE, (x, y), 60 - LINE_SIZE_OF_PLAYERS)

def draw_cross(x, y, WIDTH, HEIGHT, screen, LINE_SIZE_OF_PLAYERS):
	c = 0.7

	start_pos = (int(x - int(c * (WIDTH / 6))), int(y - int(c * (HEIGHT / 6))))
	end_pos = (int(x + int(c * (WIDTH / 6))), int(y + int(c * (HEIGHT / 6))))
	pygame.draw.line(screen, Color.RED, start_pos, end_pos, LINE_SIZE_OF_PLAYERS)

	start_pos = (int(x + int(c * (WIDTH / 6))), int(y - int(c * (HEIGHT / 6))))
	end_pos = (int(x - int(c * (WIDTH / 6))), int(y + int(c * (HEIGHT / 6))))
	pygame.draw.line(screen, Color.RED, start_pos, end_pos, LINE_SIZE_OF_PLAYERS)

def draw(screen, WIDTH, HEIGHT, LINE_SIZE_OF_GRID, grid, LINE_SIZE_OF_PLAYERS):
	screen.fill(Color.WHITE)

	x = WIDTH // 3 - LINE_SIZE_OF_GRID // 2
	y = HEIGHT // 3 - LINE_SIZE_OF_GRID // 2

	pygame.draw.rect(screen, Color.BLACK, (x, 0, LINE_SIZE_OF_GRID, HEIGHT))
	pygame.draw.rect(screen, Color.BLACK, (2*x, 0, LINE_SIZE_OF_GRID, HEIGHT))
	pygame.draw.rect(screen, Color.BLACK, (0, y, WIDTH, LINE_SIZE_OF_GRID))
	pygame.draw.rect(screen, Color.BLACK, (0, 2*y, WIDTH, LINE_SIZE_OF_GRID))

	for j in range(3):
		for i in range(3):
			x = (WIDTH / 6) + (WIDTH * i / 3)
			y = (HEIGHT / 6) + (HEIGHT * j / 3)

			if grid[j][i] == "X":
				draw_cross(x, y, WIDTH, HEIGHT, screen, LINE_SIZE_OF_PLAYERS)
			elif grid[j][i] == "O":
				draw_circle(x, y, WIDTH, HEIGHT, screen, LINE_SIZE_OF_PLAYERS)

	pygame.display.update()

def get_tile_clicked(WIDTH, HEIGHT):
	x, y = pygame.mouse.get_pos()
	x //= WIDTH / 3
	y //= HEIGHT / 3
	return (int(x), int(y))

def O_win(grid):
	for row in grid:
		if row.count("O") == 3:
			return True

	for i in range(3):
		col = [grid[j][i] for j in range(3)]
		if col.count("O") == 3:
			return True

	diagonal1 = [grid[i][i] for i in range(3)]
	diagonal2 = [grid[i][-1-i] for i in range(3)]
	if diagonal1.count("O") == 3 or diagonal2.count("O") == 3:
		return True

	return False

def X_win(grid):
	for row in grid:
		if row.count("X") == 3:
			return True

	for i in range(3):
		col = [grid[j][i] for j in range(3)]
		if col.count("X") == 3:
			return True
			
	diagonal1 = [grid[i][i] for i in range(3)]
	diagonal2 = [grid[i][-1-i] for i in range(3)]
	if diagonal1.count("X") == 3 or diagonal2.count("X") == 3:
		return True

	return False

def grid_full(grid):
	for j in range(3):
		for i in range(3):
			if grid[j][i] == None:
				return False
	return True

def main():
	pygame.init()

	WIDTH = 600
	HEIGHT = WIDTH

	LINE_SIZE_OF_GRID = 6  # This shoud be an even number

	CIRCLE_SIZE = 30
	CROSS_SIZE = 30
	LINE_SIZE_OF_PLAYERS = 10

	grid = [
	[None, None, None],
	[None, None, None],
	[None, None, None]
	]

	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Tic Tac Toe")

	game_input = Input()

	x_turn = True

	while not game_input.exit:
		game_input.get_input()
		draw(screen, WIDTH, HEIGHT, LINE_SIZE_OF_GRID, grid, LINE_SIZE_OF_PLAYERS)

		if game_input.mouse_pressed:
			x, y = get_tile_clicked(WIDTH, HEIGHT)

			if grid[y][x] == None:
				if x_turn:
					grid[y][x] = "X"
				else:
					grid[y][x] = "O"
				x_turn = not x_turn

		if O_win(grid) or X_win(grid):
			draw(screen, WIDTH, HEIGHT, LINE_SIZE_OF_GRID, grid, LINE_SIZE_OF_PLAYERS)
			time.sleep(0.3)

			if O_win(grid):
				text = "O won"
				color = Color.BLUE
			elif X_win(grid):
				text = "X won"
				color = Color.RED

			font = pygame.font.SysFont("monospace", 70)
			screen.fill(Color.WHITE)
			label = font.render(text, 1, color)
			screen.blit(label, (WIDTH//2 - 110, HEIGHT//2 - 45))
			pygame.display.update()

			while not (game_input.exit or game_input.mouse_pressed):
				game_input.get_input()

				if game_input.mouse_pressed:
					grid = [
					[None, None, None],
					[None, None, None],
					[None, None, None]
					]

		if grid_full(grid):
			draw(screen, WIDTH, HEIGHT, LINE_SIZE_OF_GRID, grid, LINE_SIZE_OF_PLAYERS)
			time.sleep(0.3)

			font = pygame.font.SysFont("monospace", 70)
			screen.fill(Color.WHITE)
			label = font.render("DRAW", 1, Color.BLACK)
			screen.blit(label, (WIDTH//2 - 100, HEIGHT//2 - 45))
			pygame.display.update()

			while not (game_input.exit or game_input.mouse_pressed):
				game_input.get_input()

				if game_input.mouse_pressed:
					grid = [
					[None, None, None],
					[None, None, None],
					[None, None, None]
					]


if __name__ == "__main__":
	main()