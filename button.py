import pygame.font


class Button:

    def __init__(self, pi_game, message, how_low=0):
        self.screen = pi_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = pi_game.settings

        self.width, self.height = 200, 50
        self.button_color = (139, 69, 19)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.y = self.rect.y - how_low

        self._prepare_message(message)

    # Turn the message into an image
    def _prepare_message(self, message):
        self.message_image = self.font.render(message, True, self.text_color, self.button_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    # Draw the button on the screen
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)
