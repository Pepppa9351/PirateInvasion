import pygame
import random


class Pirate(pygame.sprite.Sprite):

    def __init__(self, pi_game):
        super().__init__()

        self.screen = pi_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = pi_game.settings

        self.image = pygame.image.load("textures/ship (2).png")
        self.image = pygame.transform.rotate(self.image, 270)
        self.rect = self.image.get_rect()

        self.rect.x = self.screen_rect.right
        self.rect.y = random.randint(0, self.screen_rect.height - 100)

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    # Move and update the pirate's position
    def update(self):
        self.x -= self.settings.pirate_speed
        self.rect.x = int(self.x)
