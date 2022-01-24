import pygame
pygame.init()
import time
from math import cos, sin, pi, radians, degrees
import random

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
SCORE_FONT = pygame.font.Font(None, 150)

START_SCREEN = SCORE_FONT.render("START", True, "white")
START_SCREEN_CENTER = ((800 - SCORE_FONT.size("START")[0] )/ 2, (600 - SCORE_FONT.size("START")[1])/2 )
WIN_SCREEN = SCORE_FONT.render("You won !", True, "white")
WIN_SCREEN_CENTER = ((800 - SCORE_FONT.size("You won !")[0] )/ 2, (600 - SCORE_FONT.size("You won !")[1])/2 )
LOST_SCREEN = SCORE_FONT.render("You lost !", True, "white")
LOST_SCREEN_CENTER = ((800 - SCORE_FONT.size("You lost !")[0] )/ 2, (600 - SCORE_FONT.size("You lost !")[1])/2 )



##### Paddles #####


PADDLE = dotdict()
PADDLE.WIDTH = 30
PADDLE.HEIGHT = 100

PADDLE.SURFACE = pygame.Surface((PADDLE.WIDTH, PADDLE.HEIGHT))
PADDLE.SURFACE.fill("white")


player = dotdict()
player.x = 50
player.y = (screen.get_height() - PADDLE.HEIGHT) / 2
player.score = 0

enemy = dotdict()
enemy.x = screen.get_width()-50-PADDLE.WIDTH
enemy.y = (screen.get_height() - PADDLE.HEIGHT) / 2
enemy.score = 0




##### Ball #####

ball = dotdict()
ball.x = (screen.get_width() - 25) /2
ball.y = (screen.get_height() - 25) / 2
ball.dir = 0
ball.speed = 800
ball.acceleration = 50
ball.cap_speed = 1600
ball.surface = pygame.Surface((25,25), pygame.SRCALPHA)
pygame.draw.circle(ball.surface, "white", (12,12), 12.5)




##### AI STATE #####

ai = dotdict()
ai.target = 0
ai.spread = 0.05
ai.spread_increment = 0.01
ai.speed = 400





game_state = "start"



def set_ai_target():
    ai.target = ball.y + ((sin(radians(ball.dir))*((enemy.x - ball.x)/cos(radians(ball.dir)))))+12-PADDLE.HEIGHT/2
    ai.target += random.random() * screen.get_height() * ai.spread
    if ai.target < 0:
        ai.target = 0
    if ai.target > screen.get_height()-PADDLE.HEIGHT:
        ai.target = screen.get_height()-PADDLE.HEIGHT
    ai.spread += ai.spread_increment

def start_game():
    global game_state
    if player.score >= 5 or enemy.score >= 5:
        game_state = "end"
        return
    player.x = 50
    player.y = (screen.get_height() - PADDLE.HEIGHT) / 2
    enemy.x = screen.get_width() - 50 - PADDLE.WIDTH
    enemy.y = (screen.get_height() - PADDLE.HEIGHT) / 2
    ball.x = (screen.get_width() - 25) / 2
    ball.y = (screen.get_height() - 25) / 2
    #ball.dir = random.random()*360
    ball.dir = random.random()*70-35
    if player.score > enemy.score:
        ball.dir += 180
    elif player.score < enemy.score:
        pass
    else:
        if random.random() < 0.5:
            ball.dir += 180
    ball.speed = 200
    ai.spread = 0.05
    set_ai_target()


def hard_start_game():
    global game_state
    game_state = "game"
    player.score = 0
    enemy.score = 0
    start_game()



def display_fps():
    screen.blit(FPS_FONT.render(f"{int(clock.get_fps())} FPS", True, "white"), (16, 16))

def display_ball(ball):
    screen.blit(ball.surface, (ball.x, ball.y))


def display_paddle(paddle):
    screen.blit(PADDLE.SURFACE, (paddle.x, paddle.y))

def display_scores():
    screen.blit(SCORE_FONT.render(f"{player.score}", True, "white"), (200, 30))
    screen.blit(SCORE_FONT.render(f"{enemy.score}", True, "white"), (600, 30))

def clear(color):
    screen.fill(color)


def normalize_trigonometry(value):
    return value%360

def going_left(value):
    return (90 < normalize_trigonometry(value) < 270)

def going_right(value):
    return not going_left(value)

def update(dt):
    global game_state
    if not game_state == "game":
        return

    player.y = pygame.mouse.get_pos()[1] - PADDLE.HEIGHT / 2
    if enemy.y < ai.target:
        enemy.y += ai.speed * dt
        if enemy.y > ai.target:
            enemy.y = ai.target
    elif  enemy.y > ai.target:
        enemy.y -= ai.speed * dt
        if enemy.y < ai.target:
            enemy.y = ai.target

    ball.speed += ball.acceleration * dt
    if ball.speed > ball.cap_speed:
        ball.speed = ball.cap_speed
    ball.x += ball.speed * cos(radians(ball.dir)) * dt
    ball.y += ball.speed * sin(radians(ball.dir)) * dt

    if ball.y < 0:
        ball.y = 0
        ball.dir = -ball.dir
        set_ai_target()
    elif ball.y > screen.get_height():
        ball.y = screen.get_height()
        ball.dir = -ball.dir
        set_ai_target()


    if ball.x < player.x + PADDLE.WIDTH and going_left(ball.dir):
        if player.y - 25 < ball.y < player.y + PADDLE.HEIGHT:
            #ball.x = player.x+PADDLE.HEIGHT
            ball.dir = -ball.dir+180
            set_ai_target()

    if ball.x + 25 > enemy.x and going_right(ball.dir):
        if enemy.y - 25 < ball.y < enemy.y+PADDLE.HEIGHT:
            #ball.x = enemy.x
            ball.dir = -ball.dir + 180
            set_ai_target()

    if ball.x < 0:
        enemy.score += 1
        start_game()
    elif ball.x > screen.get_width():
        player.score += 1
        start_game()



def draw():
    global game_state
    clear("black")
    display_fps()

    if not game_state == "game":
        if game_state == "start":
            screen.blit(START_SCREEN,  START_SCREEN_CENTER)
        else:
            if player.score >= 5:
                screen.blit(WIN_SCREEN, WIN_SCREEN_CENTER)
            else:
                screen.blit(LOST_SCREEN, LOST_SCREEN_CENTER)
        return

    pygame.draw.line(screen, "gray", (400,0), (400,600))
    display_paddle(player)
    display_paddle(enemy)
    display_ball(ball)
    display_scores()

    #pygame.draw.circle(screen, 'red', (enemy.x, ai.target), 5)
    #for i in range(0, 800):
        #pygame.draw.circle(screen, 'red', (i, ball.y + ((sin(radians(ball.dir)) * ((i - ball.x) / cos(radians(ball.dir)))))), 5)
        #ball.y + ((sin(ball.dir) * (1 / cos(ball.dir))) * (i - ball.x))




def mouse_motion(pos, rel, buttons):
    pass


def mouse_up(pos, button):
    pass


def mouse_down(pos, button):
    global game_state
    if game_state == "start" or game_state == "end":
        if button == pygame.BUTTON_LEFT:
            hard_start_game()


def key_pressed(key, unicode):
    pass


def key_released(key, unicode):
    global game_state
    if game_state == "start" or game_state == "end" or unicode == "r":
        hard_start_game()


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