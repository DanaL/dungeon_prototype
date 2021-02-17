from copy import deepcopy

def print_building(sqs):
	for line in sqs:
		print("".join(line))

def rotate(building):
	rotated = deepcopy(building)

	for r in range(len(building)):
		for c in range(len(building)):
			nr = -(c - 4) + 4
			nc = r
			rotated[nr][nc] = building[r][c]	 

	return rotated

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

print_building(buildings["cottage 2"])
r1 = rotate(buildings["cottage 2"])
print("")
print_building(r1)
r2 = rotate(r1)
print("")
print_building(r2)

