import sys

# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in
                                                                                               raw_input().split()]
    opponent_x, opponent_y = [int(i) for i in raw_input().split()]

    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."
    # print >> sys.stderr, next_checkpoint_dist

    boost_used = False
    thrust = 100
    if abs(next_checkpoint_angle) > 90:
        thrust = 0
    elif boost_used and next_checkpoint_dist > 10000:
        thrust = "BOOST"
        boost_used = True

    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"
    print str(next_checkpoint_x) + " " + str(next_checkpoint_y) + " " + str(thrust)