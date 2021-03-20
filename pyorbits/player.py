"""
Player object for Pyorbits game
"""

import arcade
import pymunk

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "PyOrbits!"


# Classes
class Rocks(arcade.Sprite):
    """Encapsulates a Rock object for PyOrbits.
    Used for both the player object and planets it orbits.

    Assumes Pymunk physics in use
    """

    def __init__(self, path_to_sprite:str, physics_body: pymunk.Body, angular_velocity: int = 0) -> None:
        """Initialize the Rock

        Args:
            path_to_sprite (str): Where is our sprite image
            physics_body (pymunk.Body): The pymunk physics body represented by this sprite
            angular_velocity (int): How fast to spin the sprite (rad/min)
        """

        super.__init__(path_to_sprite, center_x=physics_body.body.position.x, center_y=physics_body.body.position.y)
        self.physics_body = physics_body
        self.angular_velocity = angular_velocity
        self.width = self.physics_body.radius * 2
        self.height = self.physics_body.radius * 2

class GameView(arcade.View):
    """The main game view
    """

    def __init__(self):
        super.__init__()

        # Setup a 

if __name__ == "__main__":
    window = arcade.Window(
        width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE
    )
    game_view = GameView()
    # game_view.setup()
    window.show_view(game_view)
    arcade.run()
