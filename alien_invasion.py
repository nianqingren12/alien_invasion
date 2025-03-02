import sys
import pygame
from setting import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    '''管理游戏资源和行为的类'''
    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()
        self.clock = pygame.time.Clock() # 创建时钟
        self.settings = Settings() # 关于屏幕的一些设置
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')
        self.ship = Ship(self) # 飞船实例
        self.bullets = pygame.sprite.Group()#存储创建子弹的编组

    def run_game(self):
        '''开始游戏的主循环'''
        while True:
            self._check_event()  
            self.ship.update() # 更新飞船的位置
            self.bullets.update()#更新子弹位置
            self._update_screen()
            self.clock.tick(60) # 设置帧率  

    def _check_event(self):
        '''响应按键和鼠标'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)                                  
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)

    def _check_keydown_event(self,event):
        '''相应按下'''
        if event.key == pygame.K_RIGHT:                                   
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_event(self,event):
        '''响应释放'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        '''创建一颗子弹并将其加入编组'''
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_screen(self):
        '''更新屏幕图像,并切换到新屏幕'''         
        self.screen.fill(self.settings.bg_color)   
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()            
        self.ship.blitme()            
        pygame.display.flip()
           
if __name__ == '__main__':
    '''创建游戏实例并运行游戏'''
    ai = AlienInvasion()
    ai.run_game()
