width = int(raw_input())  # the number of cells on the X axis
height = int(raw_input())  # the number of cells on the Y axis
lines = []
empty = (-1, -1)
for y in xrange(height):
    line = raw_input()  # width characters, each either 0 or .
    lines.append(line)

columns = zip(*lines)
columns = map(lambda c: "".join(c), columns)

for y in xrange(height):
    for x in xrange(width):
        if lines[y][x] == "0":
            right_x = lines[y].find("0", x + 1)
            right = (right_x, y if right_x > -1 else -1)
            bottom_y = columns[x].find("0", y + 1)
            bottom = (x if bottom_y > -1 else -1, bottom_y)
            print "{} {} {} {} {} {}".format(x, y, right[0], right[1], bottom[0], bottom[1])
