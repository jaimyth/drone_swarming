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
x_pos = 200
y_pos = np.linspace(200,800, n)



for i in range(n):
    #ag = Agent_Flock(environment=env, x = random.randint(150, 250), y = random.randint(150, 250), id=get_id())
    ag = Agent_Flock(environment=env, x = y_pos[i]+5*i, y = y_pos[i], id=get_id())
    env.add_agent(ag)

run =  True
cohese = False
go_point = False
go_line = False
align = False
distribute = False
center = False

n_polygon = 4
square_points = create_polygon_points(n_polygon, 130, (400, 400))
square = Shape(env, square_points)
env.shape = square

pp = Ppoint(env, 475, 475)
env.ppoints = [pp]

kt = 0
polygon_update = False

while run:
    t = pg.time.get_ticks()
    kt += 1

    if polygon_update:
        points = create_polygon_points(n_polygon, 130, (400, 400))
        shape = Shape(env, points)
        env.shape = shape
        polygon_update=False

    env.clear_environment()

    for i, ag in enumerate(env.agents):
        ag.final_v(cohese=cohese, avoid=True, align=align, follow=False, go_point=go_point, go_line=False, go_shape=go_line, distribute=distribute, center=center)
        ag.update_velocity()
        ag.update_position()

        #ag.draw_history(env.screen)
    centroid = env.agents[0].centroid_neighbors(env.agents[0].sense_neighbors(15)[0])
    pg.draw.circle(env.screen, (0, 0, 255), centroid.astype(int),
                   5, 0)
    env.shape.draw_shape()

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
            if event.key == pg.K_p:
                go_point = not go_point
                print(f'Go point {go_point}')
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
            if event.key == pg.K_UP:
                n_polygon += 1
                polygon_update = True
            if event.key == pg.K_DOWN:
                n_polygon -= 1
                polygon_update = True
    env.update_environment()