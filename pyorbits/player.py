"""
Player object for Pyorbits game
"""

import arcade
import pymunk
import pathlib

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "PyOrbits!"

# Paths to things
ASSETS_PATH = pathlib.Path(__file__).resolve().parent.parent / "assets"
SPRITE_PATH = ASSETS_PATH / "sprites"



# Classes
class Rock(arcade.Sprite):
    """Encapsulates a Rock object for PyOrbits.
    Used for both the player object and planets it orbits.

    Assumes Pymunk physics in use
    """

    def __init__(
        self, path_to_sprite: str, physics_body: pymunk.Body, angular_velocity: int = 0
    ) -> None:
        """Initialize the Rock

        Args:
            path_to_sprite (str): Where is our sprite image
            physics_body (pymunk.Body): The pymunk physics body represented by this sprite
            angular_velocity (int): How fast to spin the sprite (rad/min)
        """

        super.__init__(
            path_to_sprite,
            center_x=physics_body.body.position.x,
            center_y=physics_body.body.position.y,
        )
        self.physics_body = physics_body
        self.angular_velocity = angular_velocity
        self.width = self.physics_body.radius * 2
        self.height = self.physics_body.radius * 2


class GameView(arcade.View):
    """The main game view"""

    def __init__(self):
        super().__init__()

        self.level = 1

        # Gravity (0,0) is basically no external gravity acting on anything
        # Damping of 1.0 means no friction, 0.0 is max friction
        gravity = (0,0)
        damping = 1.0

        # Create the physics engine
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping,gravity=gravity)

        # Define the player sprite
        self.player = arcade.Sprite(SPRITE_PATH / "tundra.png", scale=0.2)
        self.player.center_x = 600
        self.player.center_y = 600

        # Initial force
        self.initial_force = (-100,-200)

        # Add the player.
        # For the player, we set the damping to a lower value, which increases
        # the damping rate. This prevents the character from traveling too far
        # after the player lets off the movement keys.
        # Setting the moment to PymunkPhysicsEngine.MOMENT_INF prevents it from
        # rotating.
        # Friction normally goes between 0 (no friction) and 1.0 (high friction)
        # Friction is between two objects in contact. It is important to remember
        # in top-down games that friction moving along the 'floor' is controlled
        # by damping.
        self.physics_engine.add_sprite(self.player,
                                       friction=0,
                                       mass=10,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=2000,
                                       max_vertical_velocity=2000,
                                       radius=20.0)

    def setup(self):

        # Setup the current level
        self.planets = arcade.SpriteList()

        planet1 = arcade.Sprite(SPRITE_PATH / "rock.png")
        planet1.center_x = 400
        planet1.center_y = 400
        self.planets.append(planet1)

        self.physics_engine.add_sprite_list(self.planets,
                                            mass=100000,
                                            friction=0,
                                            body_type=arcade.PymunkPhysicsEngine.STATIC
                                            )

    def on_draw(self):
        arcade.start_render()
        self.player.draw()
        self.planets.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """
        if self.initial_force:
            self.physics_engine.apply_impulse(self.player, self.initial_force)
            self.physics_engine.set_friction(self.player, 0)
            self.initial_force = None
        self.physics_engine.step()


if __name__ == "__main__":
    window = arcade.Window(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE)
    game_view = GameView()
    game_view.setup()
    window.show_view(game_view)
    arcade.run()
