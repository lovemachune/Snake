import pygame
from Snake import *

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