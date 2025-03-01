import pygame as pg
import sys

while True:
    pg.display.set_mode((200,100))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit