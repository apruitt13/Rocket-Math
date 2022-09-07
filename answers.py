import pygame
import random
from pygame.sprite import Sprite


class Numbers(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.all_numbers = []
        for nums in range(10):
            number = random.choice([1, 2, 3, 4, 5])
            self.all_numbers.append(str(number))

        # Create a number as an image
        number_font = pygame.font.SysFont(None, 46)
        background = (0, 0, 0)
        color = (245, 245, 245)
        self.image = number_font.render(self.all_numbers[1], color, background)
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


