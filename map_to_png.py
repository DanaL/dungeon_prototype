from PIL import Image

def terrain_to_rgb(t):
	if t == '^':
		return (112, 128, 144)
	elif t == '~':
		return (0, 0, 221)
	elif t == '`':
		return (0, 80, 0)
	elif t == '#':
		return (34, 139, 34)
	elif t == '.':
		return (153, 0, 0)

def to_png(grid, size):
	img = Image.new('RGB', (size * 2, size * 2))
	pixels = []

	for row in grid:
		row = row.strip()
		for sq in row:
			pixels.append(terrain_to_rgb(sq))
			pixels.append(terrain_to_rgb(sq))
		for sq in row:
			pixels.append(terrain_to_rgb(sq))
			pixels.append(terrain_to_rgb(sq))

	img.putdata(pixels)
	img.show()

f = open("wilderness.txt", "r")

grid = []
for line in f.readlines():
	grid.append(line)

to_png(grid, 257)
	
