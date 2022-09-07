import pygame.font

class Equation:

    def __init__(self, rm_game, msg):
        """Initializes the equation attributes."""
        self.screen = rm_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.equation_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the equation's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The printed equation only needs to be set onces.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered imnage and center text on the background."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.equation_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_equation(self):
        """ Draw the equation"""
        self.screen.fill(self.equation_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

