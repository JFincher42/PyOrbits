"""
Player object for Pyorbits game
"""

import arcade
import pymunk
import pathlib
from enum import Enum

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "PyOrbits!"

# Gravitational constant
G = 10

# Paths to things
ASSETS_PATH = pathlib.Path(__file__).resolve().parent.parent / "assets"
SPRITE_PATH = ASSETS_PATH / "sprites"

# Player states
class PlayerStates(Enum):
    WAITING = 1
    DRAGGING = 2
    DROPPED = 3
    FLYING = 4
    CRASHED = 5
    FINISH = 6


# Classes
class Rock(arcade.Sprite):
    """Encapsulates a Rock object for PyOrbits.
    Used for both the player object and planets it orbits.

    Assumes Pymunk physics in use
    """

    def __init__(
        self, path_to_sprite: str, position: tuple, mass: float, scale: float = 1.0
    ) -> None:
        """Initialize the Rock

        Args:
            path_to_sprite (str): Where is our sprite image
            position (tuple): Where to place the rock
            mass (float): How big is the rock
            scale (float): scaling factor
        """

        super.__init__(
            path_to_sprite, center_x=position[0], center_y=position[1], scale=scale
        )

        self.mass = mass


class GameView(arcade.View):
    """The main game view"""

    def __init__(self):
        super().__init__()

        self.level = 1

        # Gravity (0,0) is basically no external gravity acting on anything
        # Damping of 1.0 means no friction, 0.0 is max friction
        gravity = (0, 0)
        damping = 1.0

        # Create the physics engine
        self.physics_engine = arcade.PymunkPhysicsEngine(
            damping=damping, gravity=gravity
        )

        # Define the player sprite
        self.player = arcade.Sprite(SPRITE_PATH / "ball.png")
        self.player.center_x = 600
        self.player.center_y = 600
        self.player.state = PlayerStates.WAITING

        # Initial force
        self.initial_impulse = pymunk.Vec2d(-20000, 6000)

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
        self.physics_engine.add_sprite(
            self.player,
            friction=0,
            mass=200,
            moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
            collision_type="player",
            #    max_horizontal_velocity=2000,
            #    max_vertical_velocity=2000,
            radius=20.0,
        )

    def setup(self):

        # Setup the current level
        self.planets = arcade.SpriteList()

        planet1 = arcade.Sprite(SPRITE_PATH / "planet.png")
        planet1.center_x = 200
        planet1.center_y = 200
        planet1.mass = 35000.0
        self.planets.append(planet1)

        planet2 = arcade.Sprite(SPRITE_PATH / "planet.png")
        planet2.center_x = 200
        planet2.center_y = 600
        planet2.mass = 50000.0
        self.planets.append(planet2)

        planet3 = arcade.Sprite(SPRITE_PATH / "planet.png")
        planet3.center_x = 600
        planet3.center_y = 200
        planet3.mass = 75000.0
        self.planets.append(planet3)

        self.physics_engine.add_sprite_list(
            self.planets, friction=0.0, body_type=arcade.PymunkPhysicsEngine.STATIC
        )

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.player.state == PlayerStates.WAITING and arcade.is_point_in_polygon(
            x, y, self.player.get_adjusted_hit_box()
        ):
            # player_obj = self.physics_engine.get_physics_object(self.player)
            # player_obj.body_type = arcade.PymunkPhysicsEngine.KINEMATIC
            self.player.state = PlayerStates.DRAGGING

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if self.player.state == PlayerStates.DRAGGING:
            # self.player.set_position(x, y)
            self.physics_engine.set_position(self.player, (x, y))

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if self.player.state == PlayerStates.DRAGGING:
            # player_obj = self.physics_engine.get_physics_object(self.player)
            # player_obj.body_type = arcade.PymunkPhysicsEngine.DYNAMIC
            self.player.state = PlayerStates.DROPPED

    def on_draw(self):
        arcade.start_render()
        self.player.draw()
        self.player.draw_hit_box(color=arcade.color.WHITE)

        for planet in self.planets:
            planet.draw()
            planet.draw_hit_box(color=arcade.color.WHITE)

    def on_update(self, delta_time):
        """ Movement and game logic """

        if self.player.state == PlayerStates.WAITING:
            # Before the level starts
            pass

        elif self.player.state == PlayerStates.DRAGGING:
            pass

        elif self.player.state == PlayerStates.DROPPED:
            self.physics_engine.apply_impulse(self.player, self.initial_impulse)
            self.physics_engine.set_friction(self.player, 0)
            self.player.state = PlayerStates.FLYING

        elif self.player.state == PlayerStates.FLYING:
            # Figure out gravity
            player_pos = self.physics_engine.get_physics_object(
                self.player
            ).body.position
            player_mass = self.physics_engine.get_physics_object(self.player).body.mass

            grav = pymunk.Vec2d(0, 0)

            for planet in self.planets:
                planet_pos = self.physics_engine.get_physics_object(
                    planet
                ).body.position
                planet_mass = planet.mass
                grav_force = (
                    G
                    * (planet_mass * player_mass)
                    / player_pos.get_dist_sqrd(planet_pos)
                )
                grav += grav_force * (planet_pos - player_pos).normalized()

            self.physics_engine.apply_force(self.player, grav)

        elif self.player.state == PlayerStates.CRASHED:
            # TODO: Add crash animation here
            pass

        elif self.player.state == PlayerStates.FINISH:
            # TODO: Add level end animation here
            pass

        self.physics_engine.step()


if __name__ == "__main__":
    window = arcade.Window(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE)
    game_view = GameView()
    game_view.setup()
    window.show_view(game_view)
    arcade.run()
