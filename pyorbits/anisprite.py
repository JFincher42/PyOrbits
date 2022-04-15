"""
Animated Sprites for Pyorbits game
"""

import arcade


class AniSprite(arcade.Sprite):
    """Animated sprite class for PyOrbits.
    Used for both the Player object, the planets it orbits,
    and other animated duties.

    Assumes Pymunk physics in use
    """

    def __init__(
        self,
        path_to_sprites: str,
        center: tuple = (0.0, 0.0),
        mass: float = 0.0,
        scale: float = 1.0,
        delay: float = 60,
    ) -> None:
        """Animated sprite class for Orbits game.

        Args:
            path_to_sprites (str): Where are the frames for the sprite located?
            center (tuple, optional): Center position. Defaults to (0.0, 0.0).
            mass (float, optional): Mass of object for gravity calc. Defaults to 0.0.
            scale (float, optional): Scaling factor. Defaults to 1.0.
            delay (float, optional): How long to show each frame. Defaults to 1/60.
        """

        # Initialize the Sprite class first
        super().__init__()

        # Get the images that make up the frames of the animation
        # Use Arcade animated key frames to track the frame delays
        # Assumes all the images are in one folder, with a .png extension
        self.frames = [
            arcade.AnimationKeyframe(i, delay, arcade.load_texture(file))
            for i, file in enumerate(sorted(path_to_sprites.glob("*.png")))
        ]
        # Set the texture counter, and the initial texture to show
        self.cur_frame_index = 0
        self.texture = self.frames[self.cur_frame_index].texture

        # Set the position of the sprite
        self.center_x = center[0]
        self.center_y = center[1]

        # Set the scaling factor
        self.scale = scale

        # Set the mass
        self.mass = mass

        # Should gravity move this sprite? Set to False for stationary planets
        self.move_with_gravity = True

        # Should we repeat the animation?
        self.repeat_animation = True

        # Set the internal time counter to 0.0 for animation purposes
        self._time_counter = 0.0

    def update_animation(self, delta: float = 1 / 60):
        """Update the animation for this sprite

        Args:
            delta (float, optional): How much time has passed for this frame. Defaults to 1/60.
        """

        # Increment the time counter
        self._time_counter += delta

        while self._time_counter > self.frames[self.cur_frame_index].duration / 1000.0:
            self._time_counter -= self.frames[self.cur_frame_index].duration / 1000.0

            # Get the next animation in the sequence
            self.cur_frame_index += 1

            # Are we past the end of the frame list?
            if self.cur_frame_index >= len(self.frames):
                if self.repeat_animation:
                    self.cur_frame_index = 0
                else:
                    self.cur_frame_index -= 1

            self.texture = self.frames[self.cur_frame_index].texture
