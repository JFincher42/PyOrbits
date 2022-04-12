"""
Player object for Pyorbits game
"""

import arcade
import pymunk
import pathlib
import math
import pyorbits.rock

from enum import Enum


# Constants
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
SCREEN_TITLE = "PyOrbits!"

# How wide should lines be, based on distance. Smaller is bigger
DRAW_STRENGTH = 20

# Gravitational constant
G = 20

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


class GameView(arcade.View):
    """The main game view"""

    def __init__(self):
        super().__init__()

        self.level = 1

        # Get the background image
        self.background_image = arcade.load_texture(
            ASSETS_PATH / "backgrounds" / "BlueStars.png"
        )
        self.background_color = arcade.color.DARK_MIDNIGHT_BLUE

        # Gravity (0,0) is basically no external gravity acting on anything
        # Damping of 1.0 means no friction, 0.0 is max friction
        gravity = (0, 0)
        damping = 1.0
        self.draw_strength = 1

        # Create the physics engine
        self.physics_engine = arcade.PymunkPhysicsEngine(
            damping=damping, gravity=gravity
        )

        # Define the launcher sprite
        self.launcher = arcade.Sprite(SPRITE_PATH / "launcher_lite.png")
        self.launcher.right = 800
        self.launcher.center_y = 450

        # Define the player sprite
        self.player = arcade.Sprite(SPRITE_PATH / "ball.png")
        self.player.center_x = self.launcher.right + 25
        self.player.center_y = self.launcher.center_y
        self.player.state = PlayerStates.WAITING
        self.player.on_screen = True

        # Define a pointing arrow sprite

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

        self.physics_engine.add_sprite(
            self.launcher,
            body_type=arcade.PymunkPhysicsEngine.KINEMATIC,
            collision_type="none",
        )

    def load_textures(self, path, delay):
        return [
            arcade.AnimationKeyframe(i, delay, arcade.load_texture(file))
            for i, file in enumerate(sorted(path.glob("*.png")))
        ]

    def setup(self):

        # Setup the current level
        self.planets = arcade.SpriteList()

        planet1 = arcade.AnimatedTimeBasedSprite(
            SPRITE_PATH / "planet1/001.png", image_height=48, image_width=48
        )
        planet1.frames = self.load_textures(SPRITE_PATH / "planet1", 100)
        planet1.center_x = 200
        planet1.center_y = 200
        planet1.mass = 95000.0
        self.planets.append(planet1)

        planet2 = arcade.AnimatedTimeBasedSprite(
            SPRITE_PATH / "planet2/001.png", image_height=48, image_width=48
        )
        planet2.frames = self.load_textures(SPRITE_PATH / "planet2", 90)
        planet2.center_x = 500
        planet2.center_y = 400
        planet2.mass = 80000.0
        self.planets.append(planet2)

        planet3 = arcade.AnimatedTimeBasedSprite(
            SPRITE_PATH / "planet1/001.png", image_height=48, image_width=48
        )
        planet3.frames = self.load_textures(SPRITE_PATH / "planet1", 110)
        planet3.center_x = 800
        planet3.center_y = 200
        planet3.mass = 80000.0
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

        # Draw the background image
        arcade.set_background_color(self.background_color)
        arcade.draw_lrwh_rectangle_textured(
            0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_image
        )

        # If we're dragging, we can draw a line between the launcher and the player
        if self.player.state in [PlayerStates.DRAGGING, PlayerStates.WAITING]:
            arcade.draw_line(
                self.launcher.center_x,
                self.launcher.center_y,
                self.player.center_x,
                self.player.center_y,
                color=arcade.color.CANARY_YELLOW,
                line_width=self.draw_strength,
            )

        # Is the player even on screen? If not, we draw an arrow pointing to them
        # if not self.player.on_screen:

        self.player.draw()
        self.player.draw_hit_box(color=arcade.color.WHITE)

        # Draw the launcher, even if it's faded
        self.launcher.draw()

        for planet in self.planets:
            planet.draw()
            planet.draw_hit_box(color=arcade.color.WHITE)

    def on_update(self, delta_time):
        """Movement and game logic"""

        for planet in self.planets:
            planet.update_animation()
            planet.update()

        # Chillin', chillin', mindin' my business...
        if self.player.state == PlayerStates.WAITING:
            # Before the level starts
            # Calculate the angle between the launcher and the player
            x_diff = self.launcher.center_x - self.player.center_x
            y_diff = self.launcher.center_y - self.player.center_y
            angle = math.atan2(y_diff, x_diff)
            # And do the initial launcher rotation
            self.physics_engine.get_physics_object(self.launcher).body.angle = angle

        # Draggin' the line (draggin' the line)
        elif self.player.state == PlayerStates.DRAGGING:
            # Second verse, same as the first
            x_diff = self.launcher.center_x - self.player.center_x
            y_diff = self.launcher.center_y - self.player.center_y
            angle = math.atan2(y_diff, x_diff)
            self.physics_engine.get_physics_object(self.launcher).body.angle = angle

            # Used to draw the line between the player and the launcher
            x_diff = self.launcher.center_x - self.player.center_x
            y_diff = self.launcher.center_y - self.player.center_y
            self.draw_strength = pymunk.Vec2d(x_diff, y_diff).length / DRAW_STRENGTH

        # Drop it like it's hpt
        elif self.player.state == PlayerStates.DROPPED:
            # Calculate impulse
            x_diff = self.launcher.center_x - self.player.center_x
            y_diff = self.launcher.center_y - self.player.center_y
            new_impulse = pymunk.Vec2d(x_diff * 250, y_diff * 250)

            self.physics_engine.apply_impulse(self.player, new_impulse)
            self.physics_engine.set_friction(self.player, 0)
            self.player.state = PlayerStates.FLYING

            # How much time left to fade the launcher
            self.launcher_fade_time = 2.0

            # Make the launcher invisible to collisions
            self.physics_engine.remove_sprite(self.launcher)

        elif self.player.state == PlayerStates.FLYING:
            # First, set the fade out for the launcher
            self.launcher_fade_time = max(self.launcher_fade_time - delta_time, 0.0)
            self.launcher.alpha = (self.launcher_fade_time / 2.0) * 255

            # Figure out gravity
            self.physics_engine.apply_force(self.player, self.calculate_gravity())

            # See if the player is on-screen or not
            self.player.on_screen = (
                self.player.top < 0
                or self.player.bottom > SCREEN_HEIGHT
                or self.player.left < 0
                or self.player.right > SCREEN_WIDTH
            )

        elif self.player.state == PlayerStates.CRASHED:
            # TODO: Add crash animation here
            pass

        elif self.player.state == PlayerStates.FINISH:
            # TODO: Add level end animation here
            pass

        self.physics_engine.step()

    def calculate_gravity(self):
        player_pos = self.physics_engine.get_physics_object(self.player).body.position
        player_mass = self.physics_engine.get_physics_object(self.player).body.mass
        grav = pymunk.Vec2d(0, 0)

        for planet in self.planets:
            planet_pos = self.physics_engine.get_physics_object(planet).body.position
            planet_mass = planet.mass
            grav_force = (
                G * (planet_mass * player_mass) / player_pos.get_dist_sqrd(planet_pos)
            )
            grav += grav_force * (planet_pos - player_pos).normalized()
        return grav


if __name__ == "__main__":
    window = arcade.Window(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE)
    game_view = GameView()
    game_view.setup()
    window.show_view(game_view)
    arcade.run()
