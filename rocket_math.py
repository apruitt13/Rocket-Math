import sys
from time import sleep
import pygame
import random

from settings import Settings
from ship import Ship
from bullet import Bullet
from answers import Numbers
from correct_answer import Answer
from equation import Equation

class NumberInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Rocket Math")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.numbers = pygame.sprite.Group()
        self.answer = None

        self.first_int = None
        self.second_int = None
        self.problem_answer = None
        self.sign = "+"
        self.problem = (str(self.first_int) + self.sign + str(self.second_int))

        self._create_fleet()

        self.show_equation = Equation(self, self.problem)

        # Set the background color.
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self.bullets.update()
            self._update_bullets()
            self._update_numbers()
            self._update_screen()

    def _check_events(self):
        """Respond to key presses and mouse events."""
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.quit:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

            self._check_bullet_number_collisions()

    def _check_bullet_number_collisions(self):
        """Respond to bullet-number collisions."""
        # Remove any bullets and numbers that have collided.
        # Check for any bullets that have hit numbers.
        # If so, get rid of the bullet and the number.
        collisions = pygame.sprite.groupcollide(self.bullets, self.numbers, True, True)

        # If the answer is hit it is recognized.
        if self.answer not in self.numbers:
            self.bullets.empty()
            self.numbers.empty()
            self._create_fleet()
            self.show_equation
            print("hit")

        #if not self.numbers:
            # Destroy existing bullets and create new fleet.
            #self.bullets.empty()
            #self._create_fleet()


    def _update_numbers(self):
        """Check if the fleet is at an edge, then update the positions of all numbers in the fleet."""
        self._check_fleet_edges()
        self.numbers.update()

        # Look for number-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.numbers):
            self._ship_hit()

    def _ship_hit(self):
        """Respond to the ship being hit by an number."""
        # Decrement ships_left.
        #self.stats.ships_left -= 1

        # Get rid of any remaining numbers and bullets.
        self.numbers.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Pause.
        sleep(0.5)

    def _check_fleet_edges(self):
        """Respond appropriately if any numbers have reached an edge."""
        for number in self.numbers.sprites():
            if number.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for number in self.numbers.sprites():
            number.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fleet(self):
        """Create the fleet of numbers."""
        # Make a number.
        number = Numbers(self, self.problem_answer)
        number_width, number_height = number.rect.size
        available_space_x = self.settings.screen_width - (2 * number_width)
        number_numbers_x = available_space_x // (2 * number_width)

        # Determine the number of rows of numbers that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * number_height) - ship_height)
        number_rows = available_space_y // (2 * number_height)

        # create the full fleet of numbers. One row
        for row_number in range(1):
            index = random.randint(0, number_numbers_x - 1)
            self._create_answer(index, row_number)
            # Create the first row of numbers.
            for number_number in range(number_numbers_x):
                # Inserting the correct answer in a random spot.
                if number_number != index:
                    self._create_number(number_number, row_number)


    def _create_answer(self, number_number, row_number):
        """Create n number and place it in the row."""
        self.first_int = random.randint(1, 4)
        self.second_int = random.randint(1, 4)
        self.problem = (str(self.first_int) + self.sign + str(self.second_int))
        self.show_equation = Equation(self, self.problem)
        self.problem_answer = self.first_int + self.second_int
        self.answer = Answer(self, str(self.problem_answer))
        number_width, number_height = self.answer.rect.size
        self.answer.x = number_width + 2 * number_width * number_number
        self.answer.rect.x = self.answer.x
        self.answer.rect.y = self.answer.rect.height + 2 * self.answer.rect.height * row_number
        self.numbers.add(self.answer)

    def _create_number(self, number_number, row_number):
        """Create n number and place it in the row."""
        number = Numbers(self, self.problem_answer)
        number_width, number_height = number.rect.size
        number.x = number_width + 2 * number_width * number_number
        number.rect.x = number.x
        number.rect.y = number.rect.height + 2 * number.rect.height * row_number
        self.numbers.add(number)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.numbers.draw(self.screen)

        self.show_equation.draw_equation()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ni = NumberInvasion()
    ni.run_game()


