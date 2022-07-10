import pygame as pg
import numpy as np
from agent import Agent
import constants
width, height = (800, 600)
bg_color = (255, 200, 180)

pg.init()
screen = pg.display.set_mode((width, height))
screen.fill(bg_color)


ag1 = Agent()
ag1.x, ag1.y = 100, 200
ag1.vx = 10

ag1.draw(screen)

pg.display.flip()
run =  True
coords = [(ag1.x,ag1.y)]
while run:


    pg.time.delay(int(constants.dt*1000))
    t = pg.time.get_ticks()
    screen.fill(bg_color)
    vy = 100*np.sin(t/1000)
    ag1.vy = vy
    ag1.update()
    coords.append((ag1.x, ag1.y))
    pg.draw.lines(screen, (0,0,0), False, coords)
    ag1.draw(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    pg.display.flip()