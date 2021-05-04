"""
Rock object for Pyorbits game
"""

import arcade

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