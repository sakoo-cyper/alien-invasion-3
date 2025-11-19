# import pygame
class Settings:
    """A Class to store all settings for Alien Invasion."""

    def __init__(self):
        """intialize the game`s settings"""

        # screen settings.
        self.screen_width = 1000
        self.screen_hight = 600
        self.bg_color = ('black')
        # self.bg_image = pygame.image.load("")

        # ship settings
        self.ship_limit = 3

        # bullet settings
        self.bullet_width = 6
        self.bullet_height = 15
        self.bullet_color = (60,60,60)

        self.speedup_scale = 1.1
        self.points_scale = 10

        self.intialize_dynamic_settings()

        
        

    def intialize_dynamic_settings(self):
        self.ship_speed = 2
        self.bullet_speed = 5
        #alien settings
        self.alien_speed = 2
        self.fleet_drop_speed = 2
        #fleet direction of 1 represents right; -1 represent left
        self.fleet_direction = 1
        self.alien_points = 50


    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale
        self.alien_points += self.points_scale



