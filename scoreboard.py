import pygame


class Scoreboard:

    def __init__(self, pi_game):
        self.screen = pi_game.screen
        self.settings = pi_game.settings
        self.screen_rect = pi_game.screen.get_rect()
        self.score = 0

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.score_string = str(self.score)
        self.score_image = self.font.render(self.score_string, True, self.text_color)
        self.score_rect = self.score_image.get_rect()

        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_scoreboard(self):
        self.screen.blit(self.score_image, self.score_rect)
