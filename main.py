import sys
import pygame
from pygame.locals import QUIT
import numpy
import random

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

class fruits:
    def __init__(self):
        self.loc = get_random_position()

    def get_loc(self): return self.loc

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


def get_random_position():
    print("in random")
    random_x = random.randint(0, sub_width-size) // size * size
    random_y = random.randint(0, sub_height-size) // size * size
    return (random_x,random_y)

def init_background(screen, game):
    screen.fill(black)
    draw_background(game)
    screen.blit(game, (size, size * 2))

def draw_background(game):
    game.fill((0,0,0))
    for i in range (0,sub_width, size):
        pygame.draw.line(game, line_color, (i, 0), (i, sub_height))
    for j in range (0,sub_height, size):
        pygame.draw.line(game, line_color, (0, j), (sub_width, j))
    pygame.draw.line(game, line_color, (sub_width-1, 0), (sub_width-1, sub_height))
    pygame.draw.line(game, line_color, (0,  sub_height-1), (sub_width, sub_height-1))

def draw_snake(game, snakes):
    head = snakes.get_head()
    past = snakes.get_past()
    for i in past:
        pygame.draw.rect(game, white, [int(i[0] + 1), int(i[1] + 1), size - 1, size - 1], 0)
    pygame.draw.rect(game, red, [int(head[0] + 1), int(head[1] + 1), size - 1, size - 1], 0)

def draw_fruit(game, fruit,):
    loc = fruit.get_loc()
    pygame.draw.rect(game, blue, [int(loc[0]+1), int(loc[1]+1), size-1, size-1], 0)

def update(screen, game, snakes, frame_count):
    draw_snake(game, snakes)
    point = snakes.get_font().render('Points : {}'.format(snakes.get_point()), True, white)
    total_second = snakes.get_font().render('Time : {:>3}'.format(frame_count//fps), True, white)
    if frame_count % snakes.get_speed() == 0:
        snakes.update()
    screen.blit(total_second, (800, 20))
    screen.blit(point, (size, 20))
    screen.blit(game, (size, size * 2))

def check_overlap(snakes, fruit):
    snake_loc = snakes.get_head()
    fruit_loc = fruit.get_loc()
    if snake_loc[0] == fruit_loc[0] and snake_loc[1] == fruit_loc[1]:
        snakes.add_point()
        snakes.add_spped()
        snakes.add_len([fruit_loc[0], fruit_loc[1]])
        return True
    return  False

def main():
    pygame.init()
    frame_count = 0
    screen = pygame.display.set_mode((screen_width, screen_height))
    game = pygame.Surface((sub_width, sub_height))
    pygame.display.set_caption('Snake')
    my_font = pygame.font.SysFont(None, 50)
    snakes = Snake(my_font, sub_width/2-size/2, sub_height/2-size/2)
    init_background(screen, game)
    main_clock = pygame.time.Clock()
    fruit = fruits()
    while True:
        main_clock.tick(fps)
        for event in pygame.event.get():
            # 當使用者結束視窗，程式也結束
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    snakes.set_dir(2)
                if event.key == pygame.K_a:
                    snakes.set_dir(-1)
                if event.key == pygame.K_s:
                    snakes.set_dir(-2)
                if event.key == pygame.K_d:
                    snakes.set_dir(1)
        if snakes.game_over():
            print("game over")
            game_over = snakes.get_font().render("GAME OVER", True, (255,0,0))
            screen.blit(game_over, (screen_width//2-3*size, 20))
        else:
            init_background(screen, game)
            if check_overlap(snakes, fruit):
                del fruit
                fruit = fruits()

            draw_fruit(game, fruit)
            update(screen, game, snakes, frame_count)
        frame_count += 1
        pygame.display.update()

if __name__ == '__main__':
    main()


