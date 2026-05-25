import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, pi_game):
        super().__init__()

        self.screen = pi_game.screen
        self.settings = pi_game.settings

        self.image = pygame.image.load("textures/cannonBall.png")
        self.image = pygame.transform.scale(self.image, (self.settings.bullet_width, self.settings.bullet_height))
        self.rect = self.image.get_rect()
        self.rect.midleft = pi_game.player.rect.midright

        self.x = float(self.rect.x)

    # Move and update the bullet's position
    def update(self):
        self.x += self.settings.bullet_speed
        self.rect.x = int(self.x)
