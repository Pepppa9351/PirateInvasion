import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, pi_game):
        super().__init__()

        self.screen = pi_game.screen
        self.settings = pi_game.settings
        self.screen_rect = pi_game.screen.get_rect()

        self.image = pygame.image.load("textures/cannonMobile.png")
        self.image = pygame.transform.scale(self.image, (self.settings.player_width, self.settings.player_height))

        self.rect = self.image.get_rect()

        self.rect.midleft = self.screen_rect.midleft

        self.y = float(self.rect.y)

        self.moving_up = False
        self.moving_down = False

    # Update player's position every frame if we are holding down a key
    def update_player(self):
        if self.moving_up and self.rect.top >= 0:
            self.rect.y -= self.settings.player_speed

        elif self.moving_down and self.rect.bottom <= self.screen_rect.bottom:
            self.rect.y += self.settings.player_speed

        self.y = float(self.rect.y)

    # Blit the player on the screen at its current location
    def draw_player(self):
        self.screen.blit(self.image, self.rect)
