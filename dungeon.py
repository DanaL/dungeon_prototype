import math
import random

def print_dungeon(dungeon):
	for row in dungeon:
		r = "".join(row)
		print(r)

def pick_room():
	rn = random.random()
	height = 0
	width = 0
	room = []

	if rn < 0.75:
		# rectangle
		height = random.randint(5, 8)
		width = random.randint(5, 25)
		room.append(list('*' * (width + 2)))
		for r in range(0, height):
			row = '*' + ('.' * width) + '*'
			room.append(list(row))
		room.append(list('*' * (width + 2)))

		height += 2
		width += 2
	else:
		# circle
		radius = random.choice([3, 4, 5, 6])
		for row in range(0, radius * 2 + 3):
			room.append(list('*' * (radius * 2 + 3)))

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

	#print("radius:", radius, rc, cc)
	#print_dungeon(room)
	return (room, height, width)

def carve_room(dungoen, row, col, room):
	curr_row = row
	for row in room:
		for curr_col in range(0, len(row)):
			dungeon[curr_row][col + curr_col] = row[curr_col]
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
			if dungeon[r][c] == '.':
				return False

	return True

def place_room(dungeon, rooms, parent, room):
	sides = ["n", "s", "e", "w"]
	random.shuffle(sides)

	while True:
		side = sides.pop()
		if side == "n":
			# Try to place new room to the north of parent. So we know what its lower co-ord will be, 
			# Pick a column roughly toward the center of parent's north wall
			end_row = parent[1]
			start_col = random.randint(parent[2] + 1, parent[4] - 5)
			start_row = end_row - room[1] + 1
			end_col = start_col + room[2]
			fits = room_fits(dungeon, room, start_row, end_row, start_col, end_col)
			if fits:
				rooms.append((room[0], start_row, start_col, end_row, end_col))
				carve_room(dungeon, start_row, start_col, room[0])
				return True
		elif side == "s":
			start_row = parent[3] - 1
			start_col = random.randint(parent[2] + 1, parent[4] - 5)
			end_row = start_row + room[1] 
			end_col = start_col + room[2]
			fits = room_fits(dungeon, room, start_row, end_row, start_col, end_col)
			if fits:
				rooms.append((room[0], start_row, start_col, end_row, end_col))
				carve_room(dungeon, start_row, start_col, room[0])
				return True
		elif side == "w":
			end_col = parent[2]
			start_row = random.randint(parent[1] + 1, parent[3] - 5)
			start_col = end_col - room[2] + 1
			end_row = start_row + room[1] 
			fits = room_fits(dungeon, room, start_row, end_row, start_col, end_col)
			if fits:
				rooms.append((room[0], start_row, start_col, end_row, end_col))
				carve_room(dungeon, start_row, start_col, room[0])
				return True
		elif side == "e":
			start_col = parent[4] - 1
			start_row = random.randint(parent[1] + 1, parent[3] - 5)
			end_col = start_col + room[2] 
			end_row = start_row + room[1] 
			fits = room_fits(dungeon, room, start_row, end_row, start_col, end_col)
			if fits:
				rooms.append((room[0], start_row, start_col, end_row, end_col))
				carve_room(dungeon, start_row, start_col, room[0])
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

def carve_dungeon(dungeon, height, width):
	rooms = [] # in real code should be a hashset
	
	# for the first room, pick a spot roughly near the centre
	center_row = height // 2
	center_col = width // 2
	row = center_row + random.randint(-10, 10)
	col = center_col + random.randint(-10, 10)
	row = 20
	col = 70
	room = pick_room()
	rooms.append((room[0], row, col, row + room[1], col + room[2]))
	carve_room(dungeon, row, col, room[0])

	while True:
		room = pick_room()
		success = find_spot_for_room(dungeon, rooms, room)

		if not success:
			# if we couldn't place a room, that's probably enough rooms
			break
		#break
	return dungeon

dungeon = []

for j in range(0, 50):
	row = '#' * 150
	dungeon.append(list(row))

dungeon = carve_dungeon(dungeon, 50, 150)
print_dungeon(dungeon)
