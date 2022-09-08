import pygame
import random
from pygame.sprite import Sprite


class Answer(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game, answer):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Create a number as an image
        number_font = pygame.font.SysFont(None, 72)
        background = (0, 0, 0)
        color = (245, 245, 245)
        self.image = number_font.render(answer, color, background)
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien to the right or the left."""
        self.x += (self.settings.numbers_speed *
                        self.settings.fleet_direction)
        self.rect.x = self.x


