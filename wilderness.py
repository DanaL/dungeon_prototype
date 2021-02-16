from copy import deepcopy
import math
import random

WATER = 0
DIRT = 1
GRASS = 2
TREE = 3
MOUNTAIN = 4

def print_terrain(grid, file=""):
	if file != "":
		lines = []
		for row in grid:
			lines.append("".join(row) + '\n')
		f = open(file, "w")
		f.writelines(lines)
	else:
		for row in grid:
			print("".join(row))

def count_neighbouring_terrain(grid, r, c, tile):
	count = 0
	for dr in (-1, 0, 1):
		for dc in (-1, 0, 1):
			if dr == 0 and dc == 0: continue
			if grid[r + dr][c + dc] == tile:
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
					trees = count_neighbouring_terrain(grid, r, c, '#')
					if trees >= 6 and trees <=8: next_gen[r][c] = '#'
				elif grid[r][c] == '#':
					trees = count_neighbouring_terrain(grid, r, c, '#')
					if trees < 4: next_gen[r][c] = '`'
		grid = next_gen

	return grid

def in_bounds(grid, r, c):
	if r <= 0 or r >= len(grid) - 1:
		return False
	if c <= 0 or c >= len(grid) - 1:
		return False
	return True

def bresenham(r0, c0, r1, c1):
	pts = []
	error = 0
	delta_c = c1 - c0

	if delta_c < 0:
		delta_c = -delta_c
		step_c = -1
	else:
		step_c = 1

	delta_r = r1 - r0
	if delta_r < 0:
		delta_r = -delta_r
		step_r = -1
	else:
		step_r = 1

	if delta_r <= delta_c:
		criterion = delta_c // 2
		while c0 != c1 + step_c:
			pts.append((r0, c0))
			c0 += step_c
			error += delta_r
			if error > criterion:
				error -= delta_c
				r0 += step_r
	else:
		criterion = delta_r // 2
		while r0 != r1 + step_r:
			pts.append((r0, c0))
			r0 += step_r
			error += delta_c
			if error > criterion:
				error -= delta_r
				c0 += step_c

	return pts

def next_point(r, c, d, angle):
	next_r = int(r + (d * math.sin(angle)))
	next_c = int(c + (d * math.cos(angle)))

	return (next_r, next_c)

def river_start_bottom_left(SIZE):
	x = SIZE // 3

	while True:
		r = random.randint(SIZE - x, SIZE - 2)
		c = random.randint(2, x)

		mountains = count_neighbouring_terrain(grid, r, c, '^')
		if mountains > 3:
			loc = (r, c)
			break
			
	angle = 6 #5.5
	
	return (r, c, angle)

def river_start_bottom_right(SIZE):
	x = SIZE // 3

	while True:
		r = random.randint(SIZE - x, SIZE - 2)
		c = random.randint(SIZE - x - 2, SIZE - 2)

		mountains = count_neighbouring_terrain(grid, r, c, '^')
		if mountains > 3:
			loc = (r, c)
			break
			
	angle = 3.5 #5.5
	
	return (r, c, angle)

def river_start_centre(SIZE):
	x = SIZE // 3

	while True:
		r = random.randint(SIZE - x, SIZE - 2)
		c = random.randint(x, x + x)

		mountains = count_neighbouring_terrain(grid, r, c, '^')
		if mountains > 3:
			loc = (r, c)
			break

	angle = 5

	return (r, c, angle)

def draw_river(grid, row, col, angle):
	start = (row, col)

	pts =[]
	while True:
		d = random.randint(2, 4)
		n = next_point(row, col, d, angle)
		if not in_bounds(grid, n[0], n[1]):
			break

		next_segment = bresenham(row, col, n[0], n[1])

		river_crossing = False
		for pt in next_segment:
			if grid[pt[0]][pt[1]] == '~':
				river_crossing = True
				break
			else:
				pts.append(pt)

		if grid[n[0]][n[1]] == '~' or river_crossing:
			break

		row, col = n
		
		angle_delta = random.uniform(-0.25, 0.25)
		angle += angle_delta

		# keep the river from turning back and flowing uphill into the mountains
		if angle > 6.5: angle = 6.0
		if angle < 2.75: angle = 3.0
				
	# smooth river
	# bresenham draws lines that can look like:
	#      ~
	#    ~~
	#   ~@
	# I don't want those points where the player could walk
	# say NW and avoid stepping on the river
	extra_pts = []
	for x in range(len(pts) - 1):
		a = pts[x]
		b = pts[x + 1]
		if a[0] != b[0] and a[1] != b[1]:
			extra_pts.append((a[0] - 1, a[1]))

	for pt in pts:
		grid[pt[0]][pt[1]] = '~'
	grid[start[0]][start[1]] = '~'

	for pt in extra_pts:
		grid[pt[0]][pt[1]] = '~'

def add_rivers(grid, SIZE):
	# I want to draw at least 1 and up to 3 rivers
	starts = (river_start_bottom_left, river_start_bottom_right, river_start_centre)
	opts = [0, 1, 2]
	random.shuffle(opts)

	start_r, start_c, angle = starts[opts.pop()](SIZE)
	draw_river(grid, start_r, start_c, angle)

	start_r, start_c, angle = starts[opts.pop()](SIZE)
	if random.random() < 0.5:
		draw_river(grid, start_r, start_c, angle)

	start_r, start_c, angle = starts[opts.pop()](SIZE)
	if random.random() < 0.5:
		draw_river(grid, start_r, start_c, angle)

def fill_in_borders(grid, SIZE):
	for col in range(SIZE):
		for row in range(random.randint(5, 10)):
			grid[row][col] = '~'

	for col in range(SIZE):
		grid[SIZE - 1][col] = '^'

	x = random.randint(SIZE // 3, (SIZE // 3) * 2)
	for r in range(x):
		grid[r][0] = '~'
	for r in range(x, SIZE):
		grid[r][0] = '^'
	x = random.randint(SIZE // 3, (SIZE // 3) * 2)
	for r in range(x):
		grid[r][SIZE - 1] = '~'
	for r in range(x, SIZE):
		grid[r][SIZE - 1] = '^'

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

SIZE = 257
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
add_rivers(grid, SIZE)
fill_in_borders(grid, SIZE)

print_terrain(grid, "wilderness.txt")

