import math
import random

DUNGEON_WIDTH = 125
DUNGEON_HEIGHT = 40

def print_dungeon(dungeon):
	for row in dungeon:
		r = "".join(row)
		print(r)

def pick_room():
	rn = random.random()
	height = 0
	width = 0
	room = []

	if rn < 0.80:
		# rectangle
		height = random.randint(5, 8)
		width = random.randint(5, 25)
		room.append(list('#' * (width + 2)))
		for r in range(0, height):
			row = '#' + ('.' * width) + '#'
			room.append(list(row))
		room.append(list('#' * (width + 2)))

		height += 2
		width += 2
	else:
		# circle
		radius = random.choice([3, 4, 5, 6])
		for row in range(0, radius * 2 + 3):
			room.append(list('#' * (radius * 2 + 3)))

		height = radius * 2 + 3
		width = radius * 2 + 3
		x = radius
		y = 0
		error = 0
		sqrx_inc = 2 * radius - 1
		sqry_inc = 1
		rc = radius + 1
		cc = radius + 1

		while y <= x:
			room[rc + y][cc + x] = '.'
			room[rc + y][cc - x] = '.'
			room[rc - y][cc + x] = '.'
			room[rc - y][cc - x] = '.'
			room[rc + x][cc + y] = '.'
			room[rc + x][cc - y] = '.'
			room[rc - x][cc + y] = '.'
			room[rc - x][cc - y] = '.'

			y += 1
			error += sqry_inc
			sqry_inc += 2
			if error > x:
				x -= 1
				error -= sqrx_inc
				sqrx_inc -= 2

		for r in range(1, height - 1):
			for c in range(1, width - 1):
				if math.sqrt(abs(r - rc) ** 2 + abs(c - cc) ** 2) <= radius:
					room[r][c] = '.'

	return (room, height, width)

def carve_room(dungeon, row, col, room):
	curr_row = row
	for line in room:
		for curr_col in range(0, len(line)):
			dungeon[curr_row][col + curr_col] = line[curr_col]
		curr_row += 1

def room_fits(dungeon, room, start_row, end_row, start_col, end_col):
	# is it in bounds
	if start_row <= 0:
		return False
	elif end_row >= len(dungeon):
		return False
	elif start_col <= 0:
		return False
	elif end_col > len(dungeon[0]):
		return False

	for r in range(start_row, end_row):
		for c in range(start_col, end_col):
			if dungeon[r][c] != '#':
				return False

	return True

def add_doorway(dungeon, horizontal, loc, lo, hi):
	if horizontal:
		# find the places where a door could go
		options = []
		for col in range(lo, hi):
			if dungeon[loc - 1][col] == "." and dungeon[loc + 1][col] == ".":
				options.append(col)

		if len(options) > 0:
			c = random.choice(options)
			dungeon[loc][c] = "+" if random.random() < 0.80 else "."
		else:
			# if there are no options of 1-thickness walls, make a short hallway between
			# the two rooms.
			col = (lo + hi) // 2	
			row = loc
			while dungeon[row][col] != ".":
				dungeon[row][col] = "."
				row -= 1
			row = loc + 1
			while dungeon[row][col] != ".":
				dungeon[row][col] = "."
				row += 1
	else:
		options = []
		for row in range(lo, hi):
			if dungeon[row][loc - 1] == "." and dungeon[row][loc + 1] == ".":
				options.append(row)
			
		if len(options) > 0:
			r = random.choice(options)
			dungeon[r][loc] = "+" if random.random() < 0.80 else "."
		else:
			row = (lo + hi) // 2	
			col = loc
			while dungeon[row][col] != ".":
				dungeon[row][col] = "."
				col -= 1
			col = loc + 1
			while dungeon[row][col] != ".":
				dungeon[row][col] = "."
				col += 1

def place_room(dungeon, rooms, parent, room):
	sides = ["n", "s", "e", "w"]
	random.shuffle(sides)

	while True:
		side = sides.pop()
		if side == "n":
			# Try to place new room to the north of parent. So we know what its lower co-ord will be, 
			# Pick a column roughly toward the center of parent's north wall
			end_row = parent[1] + 1
			start_col = random.randint(parent[2] + 1, parent[4] - 5)
			start_row = end_row - room[1] 
			end_col = start_col + room[2]
			fits = room_fits(dungeon, room, start_row, end_row, start_col, end_col)
			if fits:
				rooms.append((room[0], start_row, start_col, end_row, end_col, "N"))
				carve_room(dungeon, start_row, start_col, room[0])

				lo = parent[2] + 1 if parent[2] + 1 > start_col else start_col
				hi = parent[4] - 1 if parent[4] - 1 < end_col else end_col
				add_doorway(dungeon, True, end_row - 1, lo, hi)

				return True
		elif side == "s":
			start_row = parent[3] - 1
			start_col = random.randint(parent[2] + 1, parent[4] - 5)
			end_row = start_row + room[1] 
			end_col = start_col + room[2]
			fits = room_fits(dungeon, room, start_row, end_row, start_col, end_col)
			if fits:
				rooms.append((room[0], start_row, start_col, end_row, end_col, "S"))
				carve_room(dungeon, start_row, start_col, room[0])

				lo = parent[2] + 1 if parent[2] + 1 > start_col else start_col
				hi = parent[4] - 1 if parent[4] - 1 < end_col else end_col
				add_doorway(dungeon, True, start_row, lo, hi)

				return True
		elif side == "w":
			end_col = parent[2] + 1
			start_row = random.randint(parent[1] + 1, parent[3] - 5)
			start_col = end_col - room[2] 
			end_row = start_row + room[1] 
			fits = room_fits(dungeon, room, start_row, end_row, start_col, end_col)
			if fits:
				rooms.append((room[0], start_row, start_col, end_row, end_col, "W"))
				carve_room(dungeon, start_row, start_col, room[0])

				lo = parent[1] + 1 if parent[1] + 1 > start_row else start_row
				hi = parent[3] - 1 if parent[3] - 1 < end_row else end_row
				add_doorway(dungeon, False, end_col - 1, lo, hi)
				
				return True
		elif side == "e":
			start_col = parent[4] - 1
			start_row = random.randint(parent[1] + 1, parent[3] - 5)
			end_col = start_col + room[2] 
			end_row = start_row + room[1] 
			fits = room_fits(dungeon, room, start_row, end_row, start_col, end_col)
			if fits:
				rooms.append((room[0], start_row, start_col, end_row, end_col, "E"))
				carve_room(dungeon, start_row, start_col, room[0])

				lo = parent[1] + 1 if parent[1] + 1 > start_row else start_row
				hi = parent[3] - 1 if parent[3] - 1 < end_row else end_row
				add_doorway(dungeon, False, start_col, lo, hi)
				
				return True	
		if len(sides) == 0:
			break

	return False

def find_spot_for_room(dungeon, rooms, room):
	# we want to try every room in the dungeon to look for a place to 
	# put our new room
	tries = [x for x in range(len(rooms))]
	random.shuffle(tries)

	while len(tries) > 0:
		i = tries.pop()
		parent = rooms[i]
		if place_room(dungeon, rooms, parent, room):
			return True
	return False

# The first pass of sticking rooms beside each other and connecting them
# via a doorway results in a map that has only a single path through it.
# It's acyclic and it's more interesting to explore a dungeon with some loops.
# So look for places we can add doors between rooms that aren't connected.
# This are probably good candidates for secret doors!

# Dumb, duplicated code but hey...prototype
def add_extra_doors(dungeon, rooms):
	# It may not hurt to shuffle the rooms, but they get added to the room
	# list in a somewhat random fashion already.
	extra_door_count = 0
	for room in rooms:
		# check north wall
		already_connected = False
		options = []
		row = room[1]
		for col in range(room[2] + 1, room[4] - 1):
			if dungeon[row][col] != "#": 
				already_connected = True
				break
			if dungeon[row - 1][col] == "." and dungeon[row + 1][col] == ".":
				options.append(col)
		if not already_connected and len(options) > 0:
			col = random.choice(options)
			dungeon[row][col] = "+"
			extra_door_count += 1
			#print("Extra door added (north)!")
			continue
		# check south wall
		already_connected = False
		options = []
		row = room[3] - 1
		for col in range(room[2] + 1, room[4] - 1):
			if dungeon[row][col] != "#": 
				already_connected = True
				break
			if dungeon[row - 1][col] == "." and dungeon[row + 1][col] == ".":
				options.append(col)
		if not already_connected and len(options) > 0:
			col = random.choice(options)
			dungeon[row][col] = "+"
			extra_door_count += 1
			#print("Extra door added (south)!")
			continue
		# check west wall
		already_connected = False
		options = []
		col = room[2] 
		for row in range(room[1] + 1, room[3] - 1):
			if dungeon[row][col] != "#": 
				already_connected = True
				break
			if dungeon[row][col -1] == "." and dungeon[row][col + 1] == ".":
				options.append(row)
		if not already_connected and len(options) > 0:
			row = random.choice(options)
			dungeon[row][col] = "+"
			extra_door_count += 1
			#print("Extra door added (west)!")
			continue
		# check east wall
		already_connected = False
		options = []
		col = room[4] - 1
		if col == DUNGEON_WIDTH - 1: continue
		for row in range(room[1] + 1, room[3] - 1):
			if dungeon[row][col] != "#": 
				already_connected = True
				break
			if dungeon[row][col -1] == "." and dungeon[row][col + 1] == ".":
				options.append(row)
		if not already_connected and len(options) > 0:
			row = random.choice(options)
			dungeon[row][col] = "+"
			extra_door_count += 1
			#print("Extra door added (east)!")
			continue

def in_bounds(row, col):
	return row > 1 and col > 1 and row < DUNGEON_HEIGHT - 1 and col < DUNGEON_WIDTH - 1

def draw_corridor_north(dungeon, row, col):
	pts = [row]
	while True:	
		row -= 1
		if not in_bounds(row, col):
			return False
		if dungeon[row][col - 1] != "#" or dungeon[row][col + 1] != "#":
			return False
		pts.append(row)
		if dungeon[row - 1][col] == ".":
			break;

	for r in pts:
		dungeon[r][col] = "."

	return True

def draw_corridor_south(dungeon, row, col):
	pts = [row]
	while True:	
		row += 1
		if not in_bounds(row, col):
			return False
		if dungeon[row][col - 1] != "#" or dungeon[row][col + 1] != "#":
			return False
		pts.append(row)
		if dungeon[row + 1][col] == ".":
			break;

	for r in pts:
		dungeon[r][col] = "."

	return True

def draw_corridor_west(dungeon, row, col):
	pts = [col]
	while True:	
		col -= 1
		if not in_bounds(row, col):
			return False
		if dungeon[row - 1][col] != "#" or dungeon[row + 1][col] != "#":
			return False
		pts.append(col)
		if dungeon[row][col - 1] == ".":
			break;

	for c in pts:
		dungeon[row][c] = "."

	return True

def draw_corridor_east(dungeon, row, col):
	pts = [col]
	while True:	
		col += 1
		if not in_bounds(row, col):
			return False
		if dungeon[row - 1][col] != "#" or dungeon[row + 1][col] != "#":
			return False
		pts.append(col)
		if dungeon[row][col + 1] == ".":
			break;

	for c in pts:
		dungeon[row][c] = "."

	return True

# Again, we'll look for walls with no egress already
def try_to_add_corridor(dungeon, rooms):
	for room in rooms:
		# check north wall
		row = room[1]
		options = []
		already_connected = False
		for col in range(room[2] + 1, room[4] - 1):
			if dungeon[row + 1][col] != '.':
				continue
			if dungeon[row][col] != '#': 
				already_connected = True
				break
			options.append(col)
		if not already_connected and len(options) > 0:
			col = random.choice(options)
			success = draw_corridor_north(dungeon, row, col)
			if success:
				return
		# check west wall
		col = room[2]
		options = []
		already_connected = False
		for row in range(room[1] + 1, room[3] - 1):
			if dungeon[row][col + 1] != '.':
				continue
			if dungeon[row][col] != '#': 
				already_connected = True
				break
			options.append(row)
		if not already_connected and len(options) > 0:
			row = random.choice(options)
			success = draw_corridor_west(dungeon, row, col)
			if success:
				return
		# check east wall
		col = room[4] - 1
		options = []
		already_connected = False
		for row in range(room[1] + 1, room[3] - 1):
			if dungeon[row][col - 1] != '.':
				continue
			if dungeon[row][col] != '#': 
				already_connected = True
				break
			options.append(row)
		if not already_connected and len(options) > 0:
			row = random.choice(options)
			success = draw_corridor_east(dungeon, row, col)
			if success:
				return
		#check south wall
		row = room[3] - 1
		options = []
		already_connected = False
		for col in range(room[2] + 1, room[4] - 1):
			# checking the square to the south avoids corners of round rooms
			if dungeon[row - 1][col] != ".":
				continue
			if dungeon[row][col] != '#': 
				already_connected = True
				break
			options.append(col)
		if not already_connected and len(options) > 0:
			col = random.choice(options)
			success = draw_corridor_south(dungeon, row, col)
			if success:
				return

# Check to see if the entire dungeon level is reachable
def floodfill_check(dungeon):
	start = None
	open_sqs = 0
	for row in range(len(dungeon)):
		for col in range(len(dungeon[row])):
			if dungeon[row][col] != "#":
				if start == None: start = (row, col)
				open_sqs += 1

	visited = set([])
	queue = [start]
	while len(queue) > 0:
		sq = queue.pop()
		visited.add(sq)
		for r in (-1, 0, 1):
			for c in (-1, 0, 1):
				next = (sq[0] + r, sq[1] + c)
				if not next in visited and dungeon[next[0]][next[1]] != '#':
					queue.append(next)

	return open_sqs == len(visited)

def print_room(dungeon, room):
	for r in range(room[1], room[3]):
		s = ""
		for c in range(room[2], room[4]):
			s += dungeon[r][c]
		print(s)

# vaults are rooms that have only one entrance. They might be useful for placing
# dungeon features
def find_vaults(dungeon, rooms):
	for room in rooms:
		egresses = 0
		for col in range(room[2], room[4]):
			if dungeon[room[1]][col] != '#':
				egresses += 1
		for col in range(room[2], room[4]):
			if dungeon[room[3] - 1][col] != '#':
				egresses += 1
		for row in range(room[1] + 1, room[3] - 1):
			if dungeon[row][room[2]] != '#':
				egresses += 1
			if dungeon[row][room[4] - 1] != '#':
				egresses += 1
		if egresses == 1:
			print("Vault found: (", room[5], ")")
			print(room[1], room[2], room[3], room[4], room[5])
			print_room(dungeon, room)

def rnd_set_elt(s):
	return random.choice(tuple(s))

def place_stairs(levels):
	open_sqs = []
	for level in levels:
		curr_open = set([])
		for r in range(len(level)):
			for c in range(len(level[0])):
				if level[r][c] == '.': 
					curr_open.add((r, c))
		open_sqs.append(curr_open)

	# For the up stairs on the first level, we don't have to match them with anything
	exit = rnd_set_elt(open_sqs[0])
	levels[0][exit[0]][exit[1]] = '<'
	open_sqs[0].remove(exit)

	# For the other stairs, I want the stairs to match up so that the levels of the 
	# dungeon are aligned. 
	for n in range(len(levels) - 1):
		options = open_sqs[n].intersection(open_sqs[n + 1])
		loc = rnd_set_elt(options)
		# I wonder what the odds that maps would be generated where there is no
		# corresponding free squares between two adjacent levels??
		# Is this worth accounting for?
		levels[n][loc[0]][loc[1]] = '>'
		levels[n + 1][loc[0]][loc[1]] = '<'
		open_sqs[n].remove(loc)
		open_sqs[n + 1].remove(loc)

def carve_dungeon(dungeon, height, width, check_for_vaults):
	rooms = [] # in real code should be a hashset
	
	# for the first room, pick a spot roughly near the centre
	center_row = height // 2
	center_col = width // 2
	row = center_row + random.randint(-10, 10)
	col = center_col + random.randint(-10, 10)
	row = 20
	col = 70
	room = pick_room()
	rooms.append((room[0], row, col, row + room[1], col + room[2], "Start"))
	carve_room(dungeon, row, col, room[0])

	while True:
		room = pick_room()
		success = find_spot_for_room(dungeon, rooms, room)

		if not success:
			# if we couldn't place a room, that's probably enough rooms
			#print("failed:", room[1], room[2])
			#print_dungeon(room[0])
			#for room in rooms:
			#	print("room:", room[1], room[2], room[3], room[4], room[5])
			break
	add_extra_doors(dungeon, rooms)
	for _ in range(3):
		try_to_add_corridor(dungeon, rooms)

	if check_for_vaults:
		find_vaults(dungeon, rooms)

	return dungeon

acceptable = 0

def test():
	dungeon = []
	rooms = []
	
	f = open("test_map.txt", "r")
	lines = f.readlines()
	for line in lines:
		if line.startswith("room"): 
			room = line[6:].strip().split(' ')
			rooms.append(([], int(room[0]), int(room[1]), int(room[2]), int(room[3]), room[4]))
		elif line[0] == "#":
			dungeon.append([c for c in line.strip()])

	room = [ "######################",
			 "#....................#",
			 "#....................#",
			 "#....................#",
			 "#....................#",
			 "#....................#",
			 "#....................#",
			 "#....................#",
			 "######################"]

	#print(find_spot_for_room(dungeon, rooms, (room, 9, 22)))
	print(place_room(dungeon, rooms, rooms[13], (room, 9, 22)))
	print_dungeon(dungeon)
	
#test()

levels = []
while acceptable < 5:
	dungeon = []

	for j in range(0, DUNGEON_HEIGHT):
		row = '#' * DUNGEON_WIDTH
		dungeon.append(list(row))

	dungeon = carve_dungeon(dungeon, DUNGEON_HEIGHT, DUNGEON_WIDTH, False)

	wall_count = 0
	for row in dungeon:
		for sq in row:
			if sq == "#": wall_count += 1
	open_count = (DUNGEON_HEIGHT * DUNGEON_WIDTH) - wall_count

	# When testing, I generated 10,000 dungeon levels and only came up
	# with 2 that weren't full connected. I could connect them by adding 
	# corridors but I think it's easier and faster to reject them and create
	# a new level.
	if not floodfill_check(dungeon):
		print("** Dungeon was not completely connected!!")
		print_dungeon(dungeon)
		continue

	# I think in a real game I'd probably wnat to reject a map with less than 37 or 38% open space.
	# The just don't use up enough of the available space
	ratio = open_count / (40 * 125)
	if ratio > 0.35:
		levels.append(dungeon)
		acceptable += 1

place_stairs(levels)

for level in levels:
	print_dungeon(level)
	print("")
