import sys
import pygame
from pygame.locals import QUIT
import numpy

size = 40
screen_width = 1080
screen_height = 720
sub_width = screen_width - 2*size
sub_height = screen_height - 3*size
line_color = (100,255,255)

def draw_background(game):
    game.fill((0,0,0))
    for i in range (0,sub_width, size):
        pygame.draw.line(game, line_color, (i, 0), (i, sub_height))
    for j in range (0,sub_height, size):
        pygame.draw.line(game, line_color, (0, j), (sub_width, j))
    pygame.draw.line(game, line_color, (sub_width-1, 0), (sub_width-1, sub_height))
    pygame.draw.line(game, line_color, (0,  sub_height-1), (sub_width, sub_height-1))

def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    game = pygame.Surface((sub_width, sub_height))
    pygame.display.set_caption('Snake')
    screen.fill((0,0,0))
    draw_background(game)
    screen.blit(game, (size,size*2))
    main_clock = pygame.time.Clock()
    while True:
        # 迭代整個事件迴圈，若有符合事件則對應處理
        for event in pygame.event.get():
            # 當使用者結束視窗，程式也結束
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.update()
            main_clock.tick(60)

if __name__ == '__main__':
    main()


