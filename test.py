import pygame as pg
import sys

#初始化
clock = pg.time.Clock()
pg.init()
ship_moving_right = False
screen = pg.display.set_mode((800,500))
screen_rect = screen.get_rect()

class Ship:
    def __init__(self):
        self.image = pg.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = screen_rect.midbottom

    def update(self):
        if ship_moving_right:
            self.rect.x += 5

ship = Ship()
            
while True:
    
    pg.display.set_caption('ship_game')
    screen.fill((230,230,230))
    ship.update()
    screen.blit(ship.image,ship.rect)
    pg.display.flip()
    clock.tick(60)

    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:         
            if event.key == pg.K_RIGHT:
               ship_moving_right = True                       
            if event.key == pg.K_LEFT:
                ship.rect.x -= 5
            if event.key == pg.K_UP:
                ship.rect.y -=5
            if event.key == pg.K_DOWN:
                ship.rect.y +=5
        elif event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                ship_moving_right = False
            
    
    


