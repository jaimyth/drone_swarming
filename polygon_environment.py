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


while run:
    t = pg.time.get_ticks()
    env.clear_environment()
    env.global_centroid = env.calculate_global_centroid()
    for i, ag in enumerate(env.agents):
        ag.final_v(cohese=cohese, avoid=True, align=align, follow=False, go_point=go_point, go_line=False,
                   go_shape=go_line, distribute=distribute, center=center, n_petal = n_petal, n_polygon=n_polygon)
        ag.update_velocity()
        ag.update_position()

        #ag.draw_history(env.screen)
    centroid = env.global_centroid# - env.agents[0].position()
    pg.draw.circle(env.screen, (0, 0, 255), centroid.astype(int),
                   5, 0)

    env.update_agents()
    env.draw_agents()
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
            #if event.key == pg.K_p:
             #   go_point = not go_point
              #  print(f'Go point {go_point}')
            if event.key == pg.K_l:
                go_line = not go_line
                print(f'Go line {go_line}')
            if event.key == pg.K_a:
                align = not align
                print(f'Align {align}')
            if event.key == pg.K_d:
                distribute = not distribute
                print(f'Distribute {distribute}')
            if event.key == pg.K_m:
                center = not center
                print(f'Center {center}')
            if event.key == pg.K_f:
                if n_petal == 0:
                    n_petal = n_petal_old
                    print(f'Flower True {n_petal}')
                else:
                    n_petal_old = n_petal
                    n_petal = 0
                    print(f'Flower False')
            if event.key == pg.K_p:
                if n_polygon == 0:
                    n_polygon = n_polygon_old
                    print(f'Polygon True {n_polygon}')
                else:
                    n_petal_old = n_petal
                    n_petal = 0
                    print(f'Polygon False')
            if event.key == pg.K_UP:
                n_petal += 1
            if event.key == pg.K_DOWN:
                n_petal -= 1
    env.update_environment()