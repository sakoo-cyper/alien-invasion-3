import pygame.font
from ship import Ship
from pygame.sprite import Group

class Scoreboard:

    def __init__(self , ai_game):

        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None , 48)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_level(self):

        level = self.stats.level
        level_str = str(level)
        self.level_image = self.font.render(level_str , True, self.text_color, self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right -20
        self.level_rect.top = self.score_rect.bottom

    def prep_score(self):

        rounded_score = round(self.stats.score , -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str , True , self.text_color , self.settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def prep_high_score(self):

        rounded_high_score = round(self.stats.high_score , -1)
        high_score_str = "{:,}".format(rounded_high_score)
        self.high_score_image = self.font.render(high_score_str , True , self.text_color , self.settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20


    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()


    def show_score(self):
        self.screen.blit(self.score_image , self.score_rect)
        self.screen.blit(self.level_image , self.level_rect)
        self.screen.blit(self.high_score_image , self.high_score_rect)
        self.ships.draw(self.screen)
        

    def prep_ships(self):
        self.ships = Group()
        for ship in range(self.stats.ships_left):
            self.ship_limit_view = Ship(self.ai_game)
            self.ship_limit_view.rect.top = 5
            self.ship_limit_view.rect.centerx = self.ship_limit_view.rect.width + (self.ship_limit_view.rect.width * ship)
            self.ships.add(self.ship_limit_view)
