# game loop
while True:
    max = 0
    index = None
    for i in xrange(8):
        mountain_h = int(raw_input())  # represents the height of one mountain.
        if mountain_h > max:
            max = mountain_h
            index = i

    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."

    # The index of the mountain to fire on.
    print index
