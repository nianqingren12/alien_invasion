import sys
from time import sleep
import pygame
from setting import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button

class AlienInvasion:
    '''管理游戏资源和行为的类'''
    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()
        self.clock = pygame.time.Clock() # 创建时钟
        self.settings = Settings() # 关于屏幕的一些设置
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')
        #创建一个用于存储游戏统计信息的实例,并创建记分牌
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self) # 飞船实例，self是给ai_game的参数
        self.bullets = pygame.sprite.Group()#存储创建子弹的编组
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        #让游戏一开始处于非活动状态
        self.game_active = False
        #创建play按钮
        self.play_button = Button(self,'Play')

    def run_game(self):
        '''开始游戏的主循环'''
        while True:
            self._check_event()  
            if self.game_active:
                self.ship.update()           
                self._update_bullets()
                self._update_aliens()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self,mouse_pos):
        '''在玩家点击play按钮时开始新游戏'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #还原游戏设置
            self.settings.initialize_dynamic_settings()
            #重置游戏统计信息
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            #清空外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            #创建一群新的外星人，并让飞船居中底端
            self._create_fleet()
            self.ship.center_ship()
            #隐藏光标
            pygame.mouse.set_visible(False)

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
        #显示得分
        self.sb.show_score()
        #如果游戏处于非活动状态，就绘制play按钮
        if not self.game_active:
            self.play_button.draw_button()     
        pygame.display.flip()

    def _update_bullets(self):
        '''更新子弹的位置并删除已消失的子弹'''
        #更新子弹的位置
        self.bullets.update()
        #删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        '''响应子弹和外星人的碰撞'''
        #删除发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            #删除现有的子弹并新建一群外星人
            self.bullets.empty()
            self._create_fleet()   
            self.settings.increase_speed() #提高游戏难度
            #提高等级
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        '''创建一个外形舰队'''
        #创建一个外星人，再不断添加，直到没有空间添加外星人为止
        #外星人的间距为外星人的宽度和外星人的高度
        alien = Alien(self)
        alien_width, alien_hight = alien.rect.size
        current_x, current_y = alien_width, alien_hight
        while current_y < (self.settings.screen_height - 3*alien_hight):
            while current_x < (self.settings.screen_width - 2*alien_width):
                self._create_alien(current_x,current_y)
                current_x += 2*alien_width
            #添加一行外星人后，重置x并递进y
            current_x = alien_width
            current_y += 2*alien_hight

    def _create_alien(self,x_position,y_position):
        '''创建一个外星人并将其加入外星舰队'''
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        '''检查是否有外星人位于屏幕边缘，更新外星人舰队中所有外星人的位置'''
        self.aliens.update()
        self._check_fleet_edges()
        #检查外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        #检查是否有外星人到达屏幕底端
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        '''有外星人到达边缘时采取相应的措施'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''将整群外星人下移，并改变它们的方向'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        '''响应飞船被外星人碰撞'''
        if self.stats.ships_left > 0: #飞船生命数
            # 将ship_left减1,并更新记分牌
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # 清空外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            # 创建一群新的外星人，并将飞船放到屏幕底端中央
            self._create_fleet()
            self.ship.center_ship()
            # 暂停
            sleep(0.5)
        else:
            self.game_active = False #游戏结束
            pygame.mouse.set_visible(True)#显示光标

    def _check_aliens_bottom(self):
        '''检查是否有外星人到达了屏幕底端'''
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #像飞船被撞倒一样处理
                self._ship_hit()
                break

if __name__ == '__main__':
    '''创建游戏实例并运行游戏'''
    ai = AlienInvasion()
    ai.run_game()
