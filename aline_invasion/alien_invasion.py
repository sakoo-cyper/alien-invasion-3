import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvansion:
     """overall class to manage game assests and behavior"""

     def __init__(self):
         """intialize the game and create game resourses."""
         pygame.init()
         self.settings = Settings()
         # self.screen = pygame.display.set_mode((0,0) , pygame.FULLSCREEN)
         self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_hight))
         # self.settings.screen_width = self.screen.get_rect().width
         # self.settings.screen_hight = self.screen.get_rect().height
         pygame.display.set_caption ("Alien Invansion")
         self.stats = GameStats(self)
         self.sb = Scoreboard(self)
         self.ship = Ship(self)
         self.bullets = pygame.sprite.Group()
         self.aliens = pygame.sprite.Group()
         self._create_fleet()
         self.play_button = Button(self , "Play")
 
         # set the background color.
         # self.bg_color = (230 , 230 , 230)


     def run_game(self) :
         """start the main loop for the game."""
         while True:
             
          self._check_events()
          self._update_screen()
          
          if self.stats.game_active :
               # watch for keyboard and mouse events.
               self.ship.update()
               self._update_bullets()
               self._update_aliens()
 
     def _check_alien_bottom(self):

          screen_rect = self.screen.get_rect()
          for alien in self.aliens.sprites():
               if alien.rect.bottom >= screen_rect.bottom:
                    self._ship_hit()
                    break

             
     def _ship_hit(self):
          """respond to the ship being hit by an alien."""

          if self.stats.ships_left > 0 :
               #decrement ships_left
               self.stats.ships_left -=1
               self.sb.prep_ships()

               #get rit of any remaining aliens and bullets.
               self.aliens.empty()
               self.bullets.empty()

               #create new fleet abd center the ship.
               self._create_fleet()
               self.ship.center_ship()

               #pause.
               sleep(0.5)   
          else :
               self.stats.game_active = False 
               pygame.mouse.set_visible(True)
            
 
     def _check_events(self):
          """respond to keypress and mouse events"""
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   sys.exit()

               elif event.type == pygame.KEYDOWN:
                  self._check_keydown_events(event)
                  

               elif event.type == pygame.KEYUP:
                 self._check_keyup_events(event)

               elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                    # firing bullet using the mouse button
                    # if not self._check_play_button(mouse_pos) and event.button == 1:
                    #      self._fire_bullet()

          #make the ship control with the mouse .
          # self.ship.rect.midtop = pygame.mouse.get_pos()
               
               
                    

     def _check_play_button(self , mouse_pos):

          if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
               self.stats.game_active = True
               pygame.mouse.set_visible(False)

               self.aliens.empty()
               self.bullets.empty()

               self._create_fleet()
               self.ship.center_ship()

               self.stats.reset_stats()
               self.sb.prep_score()
               self.sb.prep_ships()
               self.sb.prep_level()

               self.settings.intialize_dynamic_settings()

              

 
     def _check_keydown_events(self , event):
          """respond to keypress events"""
          if event.key == pygame.K_RIGHT:
                 self.ship.moveing_right = True
          elif event.key == pygame.K_LEFT:
                 self.ship.moveing_left = True
          elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
               sys.exit()
          elif event.key == pygame.K_SPACE:
               self._fire_bullet()
          elif event.key == 13:
               self.stats.game_active = True
               pygame.mouse.set_visible(False)
               self.aliens.empty()
               self.bullets.empty()

               self._create_fleet()
               self.ship.center_ship()

               self.stats.reset_stats()
               self.sb.prep_score()
               self.sb.prep_ships()

               self.settings.intialize_dynamic_settings()
 
 
     def _check_keyup_events(self,event):
          """respond to key releases"""
          if event.key == pygame.K_RIGHT:
                     self.ship.moveing_right = False
          elif event.key == pygame.K_LEFT:
              self.ship.moveing_left = False 
 
     
     def _fire_bullet(self):
          """create a new buller and add it to the bullets group."""
          new_bullet = Bullet(self)
          self.bullets.add(new_bullet)
 
 
     def _update_bullets(self):
          self.bullets.update()
          # get rid of bullets that have disappeared.
          for bullet in self.bullets.copy():
             if bullet.rect.bottom <= 0 :
                 self.bullets.remove(bullet)
          
                #  for alien_r in self.aliens.sprites():
                #       for alien in alien_r:
                #            if bullet.rect.bottom <= alien.rect.bottom:
                #                 self.bullets.remove(bullet)
                #                 alien_r.remove(alien)
          self._ceck_bullet_alien_collisions()
 
         
               
 
     def _ceck_bullet_alien_collisions(self):
          collisions = pygame.sprite.groupcollide(self.bullets , self.aliens , True , True)
          if collisions:
               for aliens in collisions.values():
                    self.stats.score += self.settings.alien_points * len(aliens)
               self.sb.prep_score()
               self.sb.check_high_score()
          if not self.aliens:
             self.bullets.empty()
             self._create_fleet()
             self.settings.increase_speed()
             self.stats.level +=1
             self.sb.prep_level()
 
 
     def _create_fleet(self):
          
          alien = Alien(self)
          alien_width , alien_height = alien.rect.size
          available_space_x = self.settings.screen_width - (alien_width * 2)
          number_aliens_x = available_space_x // (alien_width * 2)
 
          ship_height = self.ship.rect.height
          available_space_y = self.settings.screen_hight - (alien_height * 3) - ship_height
          number_rows = available_space_y // (2 * alien_height)
 
          for row_number in range(number_rows):
             for alien_number in range(number_aliens_x):
                   self._create_alien(alien_number , row_number)
 
 
     def _create_alien(self , alien_number , row_number):
          
          alien = Alien(self)
          alien_width , alien_height = alien.rect.size
          alien.x = alien_width + 2 * alien_width * alien_number
          alien.rect.x = alien.x
 
          alien.rect.y = alien_height*2 + 2 * alien_height * row_number
 
          self.aliens.add(alien)
 
 
     def _update_aliens(self):
          self._check_fleet_edges()
          self.aliens.update()

          if pygame.sprite.spritecollideany(self.ship , self.aliens):
               self._ship_hit()

          self._check_alien_bottom()
 
     def _check_fleet_edges(self):
           for alien in self.aliens.sprites():
                if alien.check_edges():
                     self._change_fleet_direction()
                     break
 
 
     def _change_fleet_direction(self):
          for alien in self.aliens.sprites():
               alien.rect.y += self.settings.fleet_drop_speed
          self.settings.fleet_direction *= -1         
 
 
     def _update_screen(self):
             """Update image on the screen and flip to the new screen."""
             #redraw the screen during each pass through the loop.
             self.screen.fill(self.settings.bg_color)
             self.sb.show_score()

 
             for bullet in self.bullets.sprites():
                  bullet.draw_bullet()
 
             # function from the ship class to draw the ship in its location.
             self.ship.blitme()
             # drawing the alien fleet on the screen
             self.aliens.draw(self.screen)
             # make the most recently drawn screen visible.
             if not self.stats.game_active :
                  self.play_button.draw_button()
             pygame.display.flip()



if __name__ == '__main__':
    # make a game instance and run the game. 
    ai = AlienInvansion()
    ai.run_game()