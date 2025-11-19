import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    """class to manage the ship."""

    def __init__(self , ai_game):
        """intialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()


        # load the ship image and get its rect.
        self.image = pygame.image.load('images/rocket-306209_1280.png')
        self.rect = self.image.get_rect()

        # start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -=1
        self.x = float(self.rect.x)
    

        # movement flag
        self.moveing_right = False
        self.moveing_left = False

    def update(self):
        if self.moveing_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moveing_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x


    def blitme(self):
        """draw the ship at its current location."""
        self.screen.blit(self.image , self.rect)
        

    def center_ship(self):

        # start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -=1
        self.x = float(self.rect.x)