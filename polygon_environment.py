import pygame as pg
import random
import numpy as np
from agent import Agent
from ppoint import Ppoint
from straight_line import S_line
from shape import Shape, create_polygon_points
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
spiral = False
polygon = False

n_polygon = 0
n_polygon_old = 7
n_petal = 0
n_petal_old = 3

pp = Ppoint(env, 475, 475)
env.ppoints = [pp]

scale=1
n_msg = 6
spacing = 22
msg_y_positions = np.arange(10, 1000, spacing)
msg_x_positions = np.ones(len(msg_y_positions))*10
msg_positions = np.array([msg_x_positions, msg_y_positions]).T


while run:
    t = pg.time.get_ticks()
    env.clear_environment()
    msg_cohese = f'[C]ohese : {cohese}'
    msg_align = f'[A]lign : {align}'
    msg_distribute = f'[D]istribute : {distribute}'
    msg_flower = f'[F]lower : {n_petal}'
    msg_polygon = f'[P]olygon : {n_polygon}'
    msg_middle = f'[M]iddle : {center}'

    messages = [msg_cohese, msg_align, msg_distribute, msg_flower, msg_polygon, msg_middle]
    env.global_centroid = env.calculate_global_centroid()
    for i, ag in enumerate(env.agents):
        ag.final_v(scale, cohese=cohese, avoid=True, align=align, follow=False, distribute=distribute, center=center, n_petal = n_petal, n_polygon=n_polygon)
        ag.update_velocity()
        ag.update_position()

        #ag.draw_history(env.screen)
    centroid = env.global_centroid# - env.agents[0].position()
    pg.draw.circle(env.screen, (0, 0, 255), centroid.astype(int),
                   5, 0)

    env.update_agents()
    env.draw_agents()
    for i in range(len(messages)):
        env.render_text(messages[i], position=msg_positions[i])
    if distribute or n_polygon or n_petal:
        env.render_text(f'Scale = {scale}', msg_positions[len(messages) + 1])
    pg.time.delay(int(constants.dt*1000))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
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

            if event.key == pg.K_d:
                scale = 1.2
                distribute = not distribute
                print(f'Distribute {distribute}')
            if distribute:
                if event.key == pg.K_RIGHT:
                    scale = scale + 0.1
                if event.key == pg.K_LEFT:
                    scale = scale - 0.1
                    scale = max(0.1, scale)

            if event.key == pg.K_f:
                scale = 175
                if n_petal == 0:
                    n_petal = n_petal_old
                    print(f'Flower True {n_petal}')
                    n_polygon_old = n_petal
                    n_polygon = 0
                    print(f'Polygon False')
                else:
                    n_petal_old = n_petal
                    n_petal = 0
                    print(f'Flower False')
            if n_petal:
                if event.key == pg.K_RIGHT:
                    scale = scale + 5
                if event.key == pg.K_LEFT:
                    scale = scale - 5
                    scale = max(1, scale)

            if event.key == pg.K_p:
                if n_polygon == 0:
                    n_polygon = n_polygon_old
                    print(f'Polygon True {n_polygon}')
                    n_petal_old = n_petal
                    n_petal = 0
                    print(f'Flower False')
                else:
                    n_petal_old = n_petal
                    n_petal = 0
                    print(f'Polygon False')
            if n_polygon:
                if event.key == pg.K_RIGHT:
                    scale = scale + 1
                if event.key == pg.K_LEFT:
                    scale = scale - 1
                    scale = max(1, scale)


            if n_petal > 0:
                if event.key == pg.K_UP:
                    n_petal += 1
                if event.key == pg.K_DOWN:
                    n_petal -= 1
                    n_petal = max(n_petal, 3)
            elif n_polygon > 0:
                if event.key == pg.K_UP:
                    n_polygon += 1
                if event.key == pg.K_DOWN:
                    n_polygon -= 1
                    n_polygon = max(n_polygon, 3)


    env.update_environment()