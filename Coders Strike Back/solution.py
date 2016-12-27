import sys
from math import sqrt, ceil


def calc_distance(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return sqrt(pow(dx, 2) + pow(dy, 2))


def cross_circle(a, b, radius):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    r = sqrt(pow(dx, 2) + pow(dy, 2))

    ccos = dx / r
    ssin = dy / r

    return int(ceil(b[0] - ccos * radius)), int(ceil(b[1] - ssin * radius))


def get_thrust(distance):
    if distance > 100:
        return 100
    else:
        return int(round(distance))

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
    if next_checkpoint_dist > 700:
        next_x, next_y = cross_circle((x, y), (next_checkpoint_x, next_checkpoint_y), 700)
    else:
        next_x, next_y = cross_circle((x, y), (next_checkpoint_x, next_checkpoint_y), 600)
    print >> sys.stderr, (next_checkpoint_x, next_checkpoint_y), (next_x, next_y)

    boost_used = False
    thrust = get_thrust(calc_distance((x, y), (next_x, next_y)))
    if abs(next_checkpoint_angle) > 90:
        thrust = 0
    elif boost_used and next_checkpoint_dist > 5000:
        thrust = "BOOST"
        boost_used = True

    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"
    print str(next_x) + " " + str(next_y) + " " + str(thrust)