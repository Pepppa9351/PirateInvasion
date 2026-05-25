import pygame


class Porch(pygame.sprite.Sprite):

    def __init__(self, pi_game):
        super().__init__()

        self.screen = pi_game.screen
        self.settings = pi_game.settings
        self.screen_rect = pi_game.screen.get_rect()

        self.image = pygame.image.load("textures/hullSmall (1).png")
        self.image = pygame.transform.scale(self.image, (self.settings.porch_width, self.settings.porch_height))

        self.rect = self.image.get_rect()

        self.rect.x = -900
        self.rect.y = -600

    # Blit the porch on the screen at its set location
    def draw_porch(self):
        self.screen.blit(self.image, self.rect)
