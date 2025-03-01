import sys
import pygame
from setting import Settings
from ship import Ship

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

    def run_game(self):
        '''开始游戏的主循环'''
        while True:
            self._check_event()  
            self.ship.update() # 更新飞船的位置
            self._update_screen()
            self.clock.tick(60) # 设置帧率  

    def _check_event(self):
        '''响应按键和鼠标'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:                                   
                    self.ship.moving_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
    def _update_screen(self):
        '''更新屏幕图像,并切换到新屏幕'''         
        self.screen.fill(self.settings.bg_color)   
        self.ship.blitme()            
        pygame.display.flip()
           
         

if __name__ == '__main__':
        #创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
