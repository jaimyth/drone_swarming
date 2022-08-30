import pygame as pg
import numpy as np
from environment import Environment
import constants

### File to visualise the shape rule ###

#Note, keyboard inputs are different from final simulation tool version



width, height = (1200, 700)
bg_color = (255, 200, 180)
env = Environment(width=width, height=height, bg_color=bg_color)
env.update_environment()
run =  True
theta = np.deg2rad(np.linspace(0, 360, 2000))

k = 1
n = 4
m = 0
scale = 100

spacing = 22
msg_y_positions = np.arange(10, 1000, spacing)
msg_x_positions = np.ones(len(msg_y_positions))*10
msg_positions = np.array([msg_x_positions, msg_y_positions]).T

while run:
    t = pg.time.get_ticks()
    env.clear_environment()
    r = scale*np.cos((2*np.arcsin(k)+np.pi*m)/(2*n)) / (np.cos( (2*np.arcsin(k*np.cos(n*theta))+np.pi*m) /(2*n)))

    x = r * np.cos(theta) + width/2
    y = r * np.sin(theta) + height/2
    points = np.array([x, y]).T
    pg.draw.polygon(env.screen, [0,0,0], points, 2)
    msg_scale = f'Scale [DOWN_ARROW] [UP_ARROW] : {scale}'
    msg_n = f'n [LEFT_ARROW] [RIGHT_ARROW] : {n}'
    msg_m = f'm [,] [.] : {m}'
    msg_k = f"k [;] ['] : {k}"
    messages = [msg_scale, msg_n, msg_m, msg_k]

    for i in range(len(messages)):
        env.render_text(messages[i], position=msg_positions[i])


    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                scale += 5
            if event.key == pg.K_DOWN:
                scale -= 5
            if event.key == pg.K_RIGHT:
                n += 1
            if event.key == pg.K_LEFT:
                n -= 1
                n = max(1,n)
            if event.key == pg.K_COMMA:
                m -= 1
            if event.key == pg.K_PERIOD:
                m += 1
            if event.key == pg.K_SEMICOLON:
                k -= 0.05
                k = max(k, 0)
            if event.key == pg.K_QUOTE:
                k += 0.05
                k = min(k,1)
    pg.time.delay(int(constants.dt*1000))
    env.update_environment()