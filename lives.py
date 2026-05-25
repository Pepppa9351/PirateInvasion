import pygame


class Lives:

    def __init__(self, pi_game):
        self.screen = pi_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = pi_game.settings

        self.image = pygame.image.load("textures/heart.png")
        self.rect = self.image.get_rect()

        self.life_count = 3

        self.rect.x = self.settings.screen_width - 40
        self.rect.y = self.settings.screen_height - 40

    def draw_lives(self):
        for heart in range(0, self.life_count):

            match heart:
                case 0:
                    self.rect.x = self.settings.screen_width - 40

                case 1:
                    self.rect.x = self.settings.screen_width - 80

                case 2:
                    self.rect.x = self.settings.screen_width - 120

            self.screen.blit(self.image, self.rect)
