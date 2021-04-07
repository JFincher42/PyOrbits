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

# Gravitational constant
G = 10

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
        self.initial_impulse = pymunk.Vec2d(-20000,6000)

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
                                       mass=200,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                    #    max_horizontal_velocity=2000,
                                    #    max_vertical_velocity=2000,
                                       radius=20.0)

    def setup(self):

        # Setup the current level
        self.planets = arcade.SpriteList()

        planet1 = arcade.Sprite(SPRITE_PATH / "rock.png", scale=0.5)
        planet1.center_x = 200
        planet1.center_y = 200
        planet1.mass = 35000.0
        self.planets.append(planet1)

        planet2 = arcade.Sprite(SPRITE_PATH / "rock.png", scale=0.5)
        planet2.center_x = 200
        planet2.center_y = 600
        planet2.mass = 50000.0
        self.planets.append(planet2)

        planet3 = arcade.Sprite(SPRITE_PATH / "rock.png", scale=0.5)
        planet3.center_x = 600
        planet3.center_y = 200
        planet3.mass = 75000.0
        self.planets.append(planet3)

        self.physics_engine.add_sprite_list(self.planets,
                                            friction=0.0,
                                            body_type=arcade.PymunkPhysicsEngine.STATIC
                                            )

    def on_draw(self):
        arcade.start_render()
        self.player.draw()
        self.player.draw_hit_box(color=arcade.color.WHITE)

        for planet in self.planets:
            planet.draw()
            planet.draw_hit_box(color=arcade.color.WHITE)

    def on_update(self, delta_time):
        """ Movement and game logic """
        if self.initial_impulse:
            print(f"Impulse: {self.initial_impulse}")
            self.physics_engine.apply_impulse(self.player, self.initial_impulse)
            self.physics_engine.set_friction(self.player, 0)
            self.initial_impulse = None

        # Figure out gravity 
        player_pos = self.physics_engine.get_physics_object(self.player).body.position
        player_mass = self.physics_engine.get_physics_object(self.player).body.mass

        # print(f"Player pos: ({player_pos.x}, {player_pos.y}), Player mass: {player_mass}")
        
        grav = pymunk.Vec2d(0,0)
        # print(f"Gravity: ({grav.x}, {grav.y})")

        for planet in self.planets:
            planet_pos = self.physics_engine.get_physics_object(planet).body.position
            # planet_mass = self.physics_engine.get_physics_object(planet).body.mass
            planet_mass = planet.mass
            # print(f"  Planet pos: ({planet_pos.x}, {planet_pos.y}), Planet mass: {planet_mass}")
            # print(f"  Distance: {player_pos.get_dist_sqrd(planet_pos)}")
            grav_force = G * (planet_mass * player_mass) / player_pos.get_dist_sqrd(planet_pos)
            # print(f"  Grav Force: {grav_force}")
            grav += grav_force * (planet_pos - player_pos).normalized()

        # print(f"Gravity: ({grav.x}, {grav.y})")
        self.physics_engine.apply_force(self.player, grav)
        # input()
        self.physics_engine.step()


if __name__ == "__main__":
    window = arcade.Window(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE)
    game_view = GameView()
    game_view.setup()
    window.show_view(game_view)
    arcade.run()
