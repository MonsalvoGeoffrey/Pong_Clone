import pygame
pygame.init()
import time

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Pong Clone")
clock = pygame.time.Clock()



class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


##### FONTS #####
FPS_FONT = pygame.font.Font(None,50)




##### Paddles #####

player = dotdict()
player.x = 0
player.y = 0

enemy = dotdict()
enemy.x = 0
enemy.y = 0


##### Ball #####

ball = dotdict()
ball.x = 0
ball.y = 0


def display_fps():
    screen.blit(FPS_FONT.render(f"{int(clock.get_fps())} FPS", True, "white"), (16, 16))






def clear(color):
    screen.fill(color)

def update(dt):
    pass

def draw():
    clear("blue")
    display_fps()




def mouse_motion(pos, rel, buttons):
    pass


def mouse_up(pos, button):
    pass


def mouse_down(pos, button):
    pass


def key_pressed(key, unicode):
    pass


def key_released(key, unicode):
    pass



last_time = time.time()


def get_dt():
    global last_time
    t = time.time()
    dt = t - last_time
    last_time = time.time()
    return dt

while True:
    # dt = clock.get_time()#/1000
    dt = get_dt()
    # print(dt)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEMOTION:
            mouse_motion(event.pos, event.rel, event.buttons)
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_up(event.pos, event.button)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down(event.pos, event.button)
        if event.type == pygame.KEYDOWN:
            key_pressed(event.key, event.unicode)
        if event.type == pygame.KEYUP:
            key_released(event.key, event.unicode)

    update(dt)
    draw()

    pygame.display.update()
    clock.tick()