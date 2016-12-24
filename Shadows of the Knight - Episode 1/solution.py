class Field(object):
    def __init__(self, width, height, x, y):
        self.y = y
        self.x = x
        self.min_x = 0
        self.min_y = 0
        self.max_x = width - 1
        self.max_y = height - 1
        self._move_map = {
            'U': self.up,
            'UR': self.up_right,
            'UL': self.up_left,
            'D': self.down,
            'DR': self.down_right,
            'DL': self.down_left,
            'L': self.left,
            'R': self.right
        }
        self.prev_ver = None
        self.prev_hor = None

    def up(self):
        self.max_y = self.y
        self.y -= int(round((self.y - self.min_y) / 2.0))

    def down(self):
        self.min_y = self.y
        self.y += int(round((self.max_y - self.y) / 2.0))

    def left(self):
        self.max_x = self.x
        self.x -= int(round((self.x - self.min_x) / 2.0))

    def right(self):
        self.min_x = self.x
        self.x += int(round((self.max_x - self.x) / 2.0))

    def up_right(self):
        self.up()
        self.right()

    def up_left(self):
        self.up()
        self.left()

    def down_right(self):
        self.down()
        self.right()

    def down_left(self):
        self.down()
        self.left()

    def move(self, dir):
        self._move_map[dir]()

# w: width of the building.
# h: height of the building.
w, h = [int(i) for i in raw_input().split()]
n = int(raw_input())  # maximum number of turns before game over.
x0, y0 = [int(i) for i in raw_input().split()]

field = Field(w, h, x0, y0)
# game loop
while True:
    bomb_dir = raw_input()  # the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)
    field.move(bomb_dir)
    print field.x, field.y