import sys
import pygame
from setting import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    '''管理游戏资源和行为的类'''
    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()
        self.clock = pygame.time.Clock() # 创建时钟
        self.settings = Settings() # 关于屏幕的一些设置
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')
        self.ship = Ship(self) # 飞船实例，self是给ai_game的参数
        self.bullets = pygame.sprite.Group()#存储创建子弹的编组
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        '''开始游戏的主循环'''
        while True:
            self._check_event()  
            self.ship.update() 
            self.bullets.update()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(60) 
              
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
        elif event.key == pygame.K_ESCAPE:
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
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        '''更新屏幕图像,并切换到新屏幕'''         
        self.screen.fill(self.settings.bg_color)   
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()            
        self.ship.blitme()   
        self.aliens.draw(self.screen)         
        pygame.display.flip()

    def _update_bullets(self):
        '''更新子弹的位置并删除已消失的子弹'''
        #更新子弹的位置
        self.bullets.update()
        #删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
           
    def _create_fleet(self):
        '''创建一个外形舰队'''
        #创建一个外星人，再不断添加，直到没有空间添加外星人为止
        #外星人的间距为外星人的宽度和外星人的高度
        alien = Alien(self)
        alien_width, alien_hight = alien.rect.size
        current_x, current_y = alien_width, alien_hight
        while current_y < (self.settings.screen_height - 3*alien_hight):
            while current_x < (self.settings.screen_width - 2*alien_width):
                self._creat_alien(current_x,current_y)
                current_x += 2*alien_width
            #添加一行外星人后，重置x并递进y
            current_x = alien_width
            current_y += 2*alien_hight

    def _creat_alien(self,x_position,y_position):
        '''创建一个外星人并将其加入外星舰队'''
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

if __name__ == '__main__':
    '''创建游戏实例并运行游戏'''
    ai = AlienInvasion()
    ai.run_game()
