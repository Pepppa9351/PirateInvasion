import pygame
from button import Button


class LossMessage(Button):

    def __init__(self, pi_game, message, how_low=0):
        super().__init__(pi_game, message, how_low=0)

        self.width = 350
        self.height = 50
        self.button_color = (101, 67, 33)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.y = self.rect.y - how_low

        self._prepare_message(message)
