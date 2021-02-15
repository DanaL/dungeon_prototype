from copy import deepcopy
import random

WATER = 0
DIRT = 1
GRASS = 2
TREE = 3
MOUNTAIN = 4

def print_terrain(grid):
	for row in grid:
		print("".join(row))

def count_neighbouring_trees(grid, r, c):
	count = 0
	for dr in (-1, 0, 1):
		for dc in (-1, 0, 1):
			if dr == 0 and dc == 0: continue
			if grid[r + dr][c + dc] == '#':
				count += 1
	return count

# We'll do this with a cellular automata rule starting with
# a mix of trees and grass
def lay_down_trees(grid, SIZE):
	for r in range(SIZE):
		for c in range(SIZE):
			if grid[r][c] == '`' and random.random() < 0.5:
				grid[r][c] = '#'

	# Two generations seems to generate pretty good clumps of trees
	for _ in range(2):
		next_gen = deepcopy(grid)
		for r in range(1, SIZE - 1):
			for c in range(1, SIZE - 1):
				if grid[r][c] == '`':
					trees = count_neighbouring_trees(grid, r, c)
					if trees >= 6 and trees <=8: next_gen[r][c] = '#'
				elif grid[r][c] == '#':
					trees = count_neighbouring_trees(grid, r, c)
					if trees < 4: next_gen[r][c] = '`'
		grid = next_gen

	return grid
					
def translate_to_terrain(grid):
	new_grid = []
	for row in grid:
		translated = []
		for sq in row:
			if sq < 1.5:
				t = '~'
			elif sq < 6.0:
				t = '`'
			else:
				t = '^'
			translated.append(t)
		new_grid.append(translated)

	return new_grid

# Average each point with its neighbours to smooth things out
def smooth_map(grid, size):
	size
	for r in range(0, size):
		for c in range(0, size):
			avg = grid[r][c] 
			count = 1
			if r - 1 >= 0: 
				if c - 1 >= 0: 
					avg += grid[r - 1][c - 1]	
					count += 1
				avg += grid[r - 1][c]
				count += 1
				if c + 1 < size:
					avg += grid[r - 1][c + 1]
					count += 1
			if c - 1 >= 0:
				avg += grid[r][c - 1]
				count += 1
			if c + 1 < size:
				avg == grid[r][c + 1]
				count += 1
			if r + 1 < size: 
				if c - 1 >= 0: 
					avg += grid[r + 1][c - 1]	
					count += 1
				avg += grid[r + 1][c]
				count += 1
				if c + 1 < size:
					avg += grid[r + 1][c + 1]
					count += 1
			grid[r][c] = avg / count
	
# Fuzz in the range -0.25 to 0.25
def fuzz():
	return random.uniform(-0.50, 0.50)

def diamond_step(grid, r, c, width):
	avg = grid[r][c]
	avg += grid[r][c + width - 1]
	avg += grid[r + width - 1][c]
	avg += grid[r + width - 1][c + width - 1]
	avg /= 4

	grid[r + width // 2][c + width // 2] = avg + fuzz()

def calc_diamond_avg(grid, r, c, width):
	count = 0
	avg = 0.0

	if c - width >= 0:
		avg += grid[r][c - width]
		count += 1
	if c + width < len(grid):
		avg += grid[r][c + width]	
		count += 1
	if r - width >= 0:
		try:
			avg += grid[r - width][c]
			count += 1
		except IndexError:
			print("what?")
			print("   ", r, c, width)
	if r + width < len(grid):
		avg += grid[r + width][c]
		count += 1

	grid[r][c] = avg / count + fuzz()
	
def square_step(grid, r, c, width):
	half_width = width // 2

	calc_diamond_avg(grid, r - half_width, c, half_width)
	calc_diamond_avg(grid, r + half_width, c, half_width)
	calc_diamond_avg(grid, r, c - half_width, half_width)
	calc_diamond_avg(grid, r, c + half_width, half_width)

def midpoint_displacement(grid, r, c, width):
	diamond_step(grid, r, c, width)
	half_width = width // 2
	square_step(grid, r + half_width, c + half_width, width)

	if half_width == 1:
		return

	midpoint_displacement(grid, r, c, half_width + 1)
	midpoint_displacement(grid, r, c + half_width, half_width + 1)
	midpoint_displacement(grid, r + half_width, c, half_width + 1)
	midpoint_displacement(grid, r + half_width, c + half_width, half_width + 1)

SIZE = 129
grid = []

for _ in range(SIZE):
	grid.append([0.0] * SIZE)

grid[0][0] = random.uniform(-1.0, 1.0)
grid[0][SIZE - 1] = random.uniform(1.0, 2.5)
grid[SIZE - 1][0] = random.uniform(10.0, 12.0)
grid[SIZE - 1][SIZE - 1] = random.uniform(9.0, 11.0)

midpoint_displacement(grid, 0, 0, SIZE)
smooth_map(grid, SIZE)
grid = translate_to_terrain(grid)
grid = lay_down_trees(grid, SIZE)

print_terrain(grid)

