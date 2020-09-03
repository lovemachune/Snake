white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
red = (255,0,0)
size = 40
screen_width = 1080
screen_height = 720
sub_width = screen_width - 2*size
sub_height = screen_height - 3*size
line_color = (100,255,255)
fps = 10

class Snake:
    def __init__(self, font, x, y):
        self.font = font
        self.x = x
        self.y = y
        self.dir = 1
        self.point = 0
        self.speed = 3
        self.past = []

    def set_point(self, point): self.point = point

    def set_dir(self, dir):
        if dir != -self.dir:
            self.dir = dir

    def add_spped(self):
        self.speed -= 1
        if self.speed <1:
            self.speed = 1

    def add_point(self, val=1): self.point += val

    def add_len(self, loc): self.past.append(loc)

    def get_speed(self): return self.speed

    def get_past(self): return self.past

    def get_head(self): return [self.x, self.y]

    def get_font(self): return self.font

    def get_point(self): return self.point

    def game_over(self):
        if self.x >= sub_width or self.x < 0 or self.y >= sub_height or self.y < 0:
            return True
        if len(self.past) != 1:
            for i in self.past[3:]:
                if i[0] == self.x and i[1] == self.y:
                    return True
        return False

    def update_head(self):
        if self.dir == 1:#d
            self.x += size
        if self.dir == -1:#a
            self.x -= size
        if self.dir == 2:#w
            self.y -= size
        if self.dir == -2:#s
            self.y += size

    def update(self):
        if self.past != []:
            self.past.insert(0, [self.x, self.y])
            self.past.pop()
        self.update_head()