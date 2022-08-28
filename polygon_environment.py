import pygame as pg
import random
import numpy as np
from agent_flock import Agent_Flock
from environment import Environment
import constants
from agent_id import *
width, height = (1200, 700)
bg_color = (255, 200, 180)

env = Environment(width=width, height=height, bg_color=bg_color)
env.update_environment()


random.seed(2)

n = 30

n_grid = np.ceil(np.sqrt(n))
x_pos = np.linspace(300, 600, n_grid)
y_pos = np.linspace(300,600, n_grid)
xx, yy = np.meshgrid(x_pos, y_pos)


for i in range(n):
    ag = Agent_Flock(environment=env, x = xx.flatten()[i], y =yy.flatten()[i], id=get_id())
    env.add_agent(ag)

run =  True
cohese = False
go_point = False
go_line = False
align = False
distribute = False
center = False
flower = False
shape = False
draw = False
n_polygon = 0
n_polygon_old = 7
n_petal = 0
n_petal_old = 3

scale = 100
n_shape = 4
m_shape = 0
k_shape = 1
shape_factors = (scale, n_shape, m_shape, k_shape)

n_msg = 6
spacing = 22
msg_y_positions = np.arange(10, 1000, spacing)
msg_x_positions = np.ones(len(msg_y_positions))*10
msg_positions = np.array([msg_x_positions, msg_y_positions]).T
thetas = np.deg2rad(np.linspace(0, 360, 100))

while run:
    t = pg.time.get_ticks()
    env.clear_environment()
    msg_cohese = f'[C]ohese : {cohese}'
    msg_align = f'[A]lign : {align}'
    msg_distribute = f'[S]hape : {shape}'
    msg_flower = f'[F]lower : {n_petal}'
    msg_polygon = f'[P]olygon : {n_polygon}'
    msg_middle = f'[M]iddle : {center}'

    messages = [msg_cohese, msg_align, msg_distribute, msg_flower, msg_polygon, msg_middle]
    env.global_centroid = env.calculate_global_centroid()
    for i, ag in enumerate(env.agents):
        ag.final_v(shape_factors, cohese=cohese, avoid=True, align=align, follow=False, center=center, flower=flower, shape_nmk=shape)
        ag.update_velocity()
        ag.update_position()
        ag.gradient()
        #ag.draw_history(env.screen)
    centroid = env.global_centroid# - env.agents[0].position()
    pg.draw.circle(env.screen, (0, 0, 255), centroid.astype(int),
                   5, 0)
    if draw and (shape or flower):
        if shape:
            r = scale * np.cos((2 * np.arcsin(k_shape) + np.pi * m_shape) / (2 * n_shape)) / (
                np.cos((2 * np.arcsin(k_shape * np.cos(n_shape * thetas)) + np.pi * m_shape) / (2 * n_shape)))
        if flower:
            r = abs(scale * np.cos(n_petal/2 * thetas))

        x = r * np.cos(thetas) + centroid[0]
        y = r * np.sin(thetas) + centroid[1]
        points = np.array([x, y]).T
        pg.draw.polygon(env.screen, [0, 0, 0], points, 2)
        msg_scale = f'Scale [DOWN_ARROW] [UP_ARROW] : {scale}'
        msg_n = f'n [LEFT_ARROW] [RIGHT_ARROW] : {n_shape}'
        msg_m = f'm [,] [.] : {m_shape}'
        msg_k = f"k [;] ['] : {k_shape}"
        messages = [msg_scale, msg_n, msg_m, msg_k]
        for i in range(len(messages)):
            env.render_text(messages[i], position=msg_positions[i])


    env.update_agents()
    env.draw_agents()
    for i in range(len(messages)):
        env.render_text(messages[i], position=msg_positions[i])
    if distribute or n_polygon or n_petal:
        env.render_text(f'Scale = {scale}', msg_positions[len(messages) + 1])

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        keys = pg.key.get_pressed()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                draw = not draw
                print(f'Draw {draw}')
            if event.key == pg.K_r:
                for i in env.agents:
                    i.reset_position()
            if event.key == pg.K_h:
                for ag in env.agents:
                    ag.reset_history()
            if event.key == pg.K_c:
                cohese = not cohese
                print(f'Cohese {cohese}')
            if event.key == pg.K_a:
                align = not align
                print(f'Align {align}')
            if event.key == pg.K_m:
                center = not center
                print(f'Center {center}')

            if event.key == pg.K_f:
                scale = 175
                flower = not flower
                if flower and shape:
                    shape = False
                if n_petal == 0:
                    n_petal = n_petal_old
                    print(f'Flower True {n_petal}')
                else:
                    n_petal_old = n_petal
                    n_petal = 0
                    print(f'Flower False')
            if flower:
                scale = scale +5 *(keys[pg.K_UP] - keys[pg.K_DOWN])
                scale = max(5, scale)
                n_petal = n_petal + (keys[pg.K_RIGHT] - keys[pg.K_LEFT])
                n_petal = max(1,n_petal)
                shape_factors = (scale, n_petal, m_shape, k_shape)
            if event.key == pg.K_s:
                shape = not shape
                if shape and flower:
                    flower = False

            if shape:
                scale = scale +5 *(keys[pg.K_UP] - keys[pg.K_DOWN])
                scale = max(5, scale)
                n_shape = n_shape + 0.5*(keys[pg.K_RIGHT] - keys[pg.K_LEFT])
                n_shape = max(1,n_shape)
                m_shape = m_shape + 1*(keys[pg.K_COMMA] - keys[pg.K_PERIOD])
                k_shape = np.round(k_shape + 0.05*(keys[pg.K_QUOTE]-keys[pg.K_SEMICOLON]),1)
                k_shape = max(k_shape, 0)
                k_shape = min(k_shape,1)
                shape_factors = (scale, n_shape, m_shape, k_shape)


    pg.time.delay(int(constants.dt*2000))
    env.update_environment()