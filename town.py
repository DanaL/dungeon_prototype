from copy import deepcopy
import random

def write_map_file(grid, file):
	lines = []
	for row in grid:
		lines.append("".join(row) + '\n')
	f = open(file, "w")
	f.writelines(lines)

def print_building(sqs):
	for line in sqs:
		print("".join(line))

def rotate(building):
	rotated = deepcopy(building)

	for r in range(len(building)):
		for c in range(len(building)):
			nr = -(c - 4) + 4
			nc = r

			if building[r][c] == '|':
				rotated[nr][nc] = '-'
			elif building[r][c] == '-':
				rotated[nr][nc] = '|'
			else:	
				rotated[nr][nc] = building[r][c]	 

	return rotated

def draw_building(grid, r, c, loc, building):
	start_r = r + 12 * loc[0]
	start_c = c + 12 * loc[1]

	# lots are 12x12 and building templates are 9x9 so we can stagger them on the lot 
	# a bit
	stagger_r = random.randint(0, 2)
	stagger_c = random.randint(0, 2)

	for row in range(9):
		for col in range(9):
			grid[start_r + stagger_r + row][start_c + stagger_c + col] = building[row][col]

def lot_has_water(grid, start_r, start_c, lot_r, lot_c):
	for r in range(12):
		for c in range(12):
			if grid[start_r + (lot_r * 12) + r][start_c + (lot_c * 12) + c] == '~':
				return True
	return False

# town will be laid out as 5x3 lots, each 12x12 squares
def place_town(grid, size, buildings):
	# pick start co-ordinates that are in the centre-ish part of the map
	start_r = random.randint(size // 4, size // 2)
	start_c = random.randint(size // 4, size // 2 +  60)

	start_r = 100
	start_c = 50

	# Step one, get rid of most of the trees in town and replace with grass.
	# (in rogue village I'll probably replace grass and trees with mostly dirt)
	for r in range(start_r, start_r + 36):
		for c in range(start_c, start_c + 60):
			if grid[r][c] == 'T' and random.random() < 0.85:
				grid[r][c] = '`'

	available_lots = set([])
	for r in range(3):
		for c in range(5):
			# Avoid lots with water in the them to avoid plunking a house
			# over a river. I could do something fancier like actually checking
			# if placing a house will overlap with water so that if there is just
			# a corner or edge that's water it's still good. Maybe in Real CodeTM.
			# Also should reject a town placement where there aren't enough lots 
			# for all the buildings I want to add because of water hazards.
			if not lot_has_water(grid, start_r, start_c, r, c):
				available_lots.add((r, c))

	# The town will have only one shrine
	loc = random.choice(tuple(available_lots))
	available_lots.remove(loc)
	draw_building(grid, start_r, start_c, loc, buildings["shrine"])

	for  _ in range(6):
		loc = random.choice(tuple(available_lots))
		available_lots.remove(loc)
		if random.random() < 0.5:
			draw_building(grid, start_r, start_c, loc, buildings["cottage 1"])
		else:
			draw_building(grid, start_r, start_c, loc, buildings["cottage 2"])
	
# load buildings
f = open("buildings.txt", "r")
lines = [line.strip() for line in f.readlines()]

buildings = { }
for b in range(len(lines) // 10):
	name = lines[b * 10]
	sqs = []
	for r in range(b * 10 + 1, b * 10 + 10):
		sqs.append([c for c in lines[r]])
	buildings[name] = sqs

# load the test wilderness map
grid = []
f = open("wilderness.txt", "r")
for line in f.readlines():
	grid.append([c for c in line.strip()])
size = len(grid)

place_town(grid, size, buildings)

write_map_file(grid, "wilderness2.txt")

