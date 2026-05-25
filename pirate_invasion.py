import sys
import pygame
from settings import Settings
from player import Player
from bullet import Bullet
from pirate import Pirate
from porch import Porch
from scoreboard import Scoreboard
from lives import Lives
from pause import Pause
from button import Button
from loss_message import LossMessage


class PirateInvasion:

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.last_pirate_spawn = 0
        self.pause = False
        self.game_active = False
        self.game_loss = False

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.screen_rect = self.screen.get_rect()

        pygame.display.set_caption("Pirate Invasion")

        self.background_texture = pygame.image.load("textures/water_tile.png")
        self.background_texture = pygame.transform.scale(self.background_texture,
                                                         (self.settings.screen_width, self.settings.screen_height))

        self.player = Player(self)
        self.bullets = pygame.sprite.Group()
        self.pirates = pygame.sprite.Group()
        self.porch = Porch(self)
        self.scoreboard = Scoreboard(self)
        self.lives = Lives(self)

        self.play_button = Button(self, "Play")
        self.quit_button = Button(self, "Quit", -70)
        self.game_return = Pause(self, "Return to the game", 70)
        self.game_restart = Pause(self, "Restart")
        self.menu_return = Pause(self, "Return to the menu", -70)
        self.game_quit = Pause(self, "Quit", -140)
        self.loss_message = LossMessage(self, "Game Over!", 70)

    # Check for events in the game
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_buttons(mouse_position)

    # Checks which key we pressed
    def _check_keydown_events(self, event):
        if event.key == pygame.K_w:
            self.player.moving_up = True
        elif event.key == pygame.K_s:
            self.player.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            if self.game_active:
                if not self.pause:
                    self.pause = True
                else:
                    self.pause = False

    # Checks which key we let go off
    def _check_keyup_events(self, event):
        if event.key == pygame.K_w:
            self.player.moving_up = False
        elif event.key == pygame.K_s:
            self.player.moving_down = False

    # Check for button collisions with mouse click
    def _check_buttons(self, mouse_position):
        if not self.game_active:
            if self.play_button.rect.collidepoint(mouse_position):
                self.game_active = True
            elif self.quit_button.rect.collidepoint(mouse_position):
                sys.exit()
        elif self.pause:
            if self.game_return.rect.collidepoint(mouse_position):
                self.pause = False
            elif self.game_restart.rect.collidepoint(mouse_position):
                self._restart_game()
            elif self.menu_return.rect.collidepoint(mouse_position):
                self._restart_game()
                self.game_active = False
            elif self.game_quit.rect.collidepoint(mouse_position):
                sys.exit()
        elif self.game_loss:
            if self.game_restart.rect.collidepoint(mouse_position):
                self._restart_game()
                self.game_loss = False
            elif self.menu_return.rect.collidepoint(mouse_position):
                self._restart_game()
                self.game_active = False
                self.game_loss = False

    # Create a new bullet and add it to the group of bullets
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    # Update the position of the bullets and delete the ones that are off the screen
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen_rect.right:
                self.bullets.remove(bullet)

    def _update_scoreboard(self):
        if pygame.sprite.groupcollide(self.bullets, self.pirates, True, True):
            self.scoreboard.score += 100
            self.settings.pirate_speed *= self.settings.pirate_speed_up

        score_string = str(self.scoreboard.score)
        self.scoreboard.score_image = self.scoreboard.font.render(score_string, True, self.scoreboard.text_color)
        self.scoreboard.score_rect = self.scoreboard.score_image.get_rect()
        self.scoreboard.score_rect.right = self.screen_rect.right - 20
        self.scoreboard.score_rect.top = 20
        self.scoreboard.show_scoreboard()

    # Draw the current amount of lives
    def _update_lives(self):
        if pygame.sprite.spritecollide(self.porch, self.pirates, True):
            self.lives.life_count -= 1
            self.lives.draw_lives()

        if self.lives.life_count <= 0:
            self._loss_screen()
            self.game_loss = True

    # Add each new pirate to the fleet
    def _spawn_pirate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pirate_spawn > self.settings.pirate_cooldown:
            pirate = Pirate(self)
            self.pirates.add(pirate)
            self.last_pirate_spawn = current_time

    # Draw every button in the pause menu
    def _pause_menu(self):
        self.game_return.draw_button()
        self.game_quit.draw_button()
        self.game_restart.draw_button()
        self.menu_return.draw_button()

    # Restart the game
    def _restart_game(self):
        self.pause = False
        self.scoreboard.score = 0
        self.lives.life_count = 3
        self.bullets.empty()
        self.pirates.empty()
        self.player.rect.midleft = self.screen_rect.midleft

    # Draw the loss screen
    def _loss_screen(self):
        self.loss_message.draw_button()
        self.game_restart.draw_button()
        self.menu_return.draw_button()

    # Update everything on the screen to the latest state
    def _update_screen(self):
        if not self.game_active:
            self.screen.blit(self.background_texture, (0, 0))
            self.play_button.draw_button()
            self.quit_button.draw_button()
        elif self.pause:
            self._pause_menu()
        elif self.game_loss:
            self._loss_screen()
        else:
            self.screen.blit(self.background_texture, (0, 0))
            self.porch.draw_porch()
            self.player.draw_player()
            self.pirates.draw(self.screen)
            self.bullets.draw(self.screen)
            self._update_scoreboard()
            self.lives.draw_lives()

        pygame.display.flip()

    # The mainloop of the game
    def run_game(self):
        while True:
            self._check_events()
            if self.game_active and not self.pause and not self.game_loss:
                self.player.update_player()
                self._update_bullets()
                self._update_lives()
                self.pirates.update()
                self._spawn_pirate()
            self._update_screen()
            self.clock.tick(60)


if __name__ == '__main__':
    pi = PirateInvasion()
    pi.run_game()
