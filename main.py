import sys
from pygame.locals import QUIT
from draw import *
import random
import socket
import threading

alive = True
HOST = '127.0.0.1'
PORT = 8888
read = ''

class fruits:
    def __init__(self):
        self.loc = get_random_position()

    def get_loc(self): return self.loc

def get_random_position():
    random_x = random.randint(0, sub_width-size) // size * size
    random_y = random.randint(0, sub_height-size) // size * size
    return (random_x,random_y)


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
    return False

def mysocket():
    global read, alive
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(10)
    conn, _ = server.accept()
    while alive:
        read = conn.recv(1024).decode('ascii')
        if not read:
            break
        read = read.replace('\n', '')
    conn.close()

def check_client(snakes):
    global read
    if read == 'w':
        snakes.set_dir(2)
    if read == 'a':
        snakes.set_dir(-1)
    if read == 's':
        snakes.set_dir(-2)
    if read == 'd':
        snakes.set_dir(1)

def main(thread):
    global read, alive
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
    game_flag = True
    while alive:
        if not thread.is_alive():
            thread = threading.Thread(target=mysocket)
            thread.start()
        main_clock.tick(fps)
        for event in pygame.event.get():
            # 當使用者結束視窗，程式也結束
            if event.type == QUIT:
                alive = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    snakes.set_dir(2)
                    read = 'w'
                if event.key == pygame.K_a:
                    snakes.set_dir(-1)
                    read = 'a'
                if event.key == pygame.K_s:
                    snakes.set_dir(-2)
                    read = 's'
                if event.key == pygame.K_d:
                    snakes.set_dir(1)
                    read = 'd'
                if event.key == pygame.K_r and not game_flag:
                    main(thread)
        if not game_flag and read == 'r':
            main(thread)
        check_client(snakes)
        if snakes.game_over():
            game_over = snakes.get_font().render("GAME OVER", True, red)
            restart = snakes.get_font().render("Press R to restart", True, red)
            screen.blit(game_over, (screen_width//2-3*size, 10))
            screen.blit(restart, (screen_width // 2 - 4*size, 40))
            game_flag = False
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
    thread = threading.Thread(target=mysocket)
    thread.start()
    main(thread)



