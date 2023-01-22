import pygame as pg
from typing import Any
from code.constants import DEFAULT_FRICTION,\
                           DEFAULT_GRAVITY_ACCELERATION,\
                           DEFAULT_COLOR,\
                           DEFAULT_SIZE,\
                           DEFAULT_POS,\
                           DEFAULT_SPEED


class RSprite(pg.sprite.Sprite):
    def __init__(self, **kwargs: Any) -> None:
        """Custom sprite class that handles everything a sprite needs.
        known keyword arguments:
            pos:        tuple[int, int]
                        position of the sprite on the screen
            speed:      tuple[float, float]
                        speed and direction of sprite
            img:        str
                        image of sprite (replaced with the default rectangle if
                        error occurs)
            size:       tuple[int, int]
                        size of sprite (if no image is provided)
            color:      Any datatype pygame recognizes
                        color of sprite (if no image is provided)
            friction:   tuple[float, float]
                        friction (slowdown) of sprite, 0 is no slowdown at all
            gravity:    tuple[float, float]
                        magnitude and direction of gravity, 0 is no gravity
            nomask:     bool
                        clear the mask to 0 bits
            alpha:      int[0...255]
                        set alpha value to image (255 is full opaque)
        """
        super().__init__()

        # fetch useful keyword arguments
        size = kwargs.get("size", DEFAULT_SIZE)
        color = kwargs.get("color", DEFAULT_COLOR)
        self._friction = pg.Vector2(kwargs.get("friction", DEFAULT_FRICTION))
        self._gravity =\
            pg.Vector2(kwargs.get("gravity", DEFAULT_GRAVITY_ACCELERATION))
        nomask = kwargs.get("nomask", False)
        alpha = kwargs.get("alpha", 255)

        self._pos = pg.Vector2(kwargs.get("pos", DEFAULT_POS))
        self._speed = pg.Vector2(kwargs.get("speed", DEFAULT_SPEED))
        img = kwargs.get("img", "")
        self._image = self._load_image(img, size, color)
        self._rect = self._image.get_rect()
        self._mask = pg.mask.from_surface(self.image)
        if nomask:
            self._mask.clear()
        self._image.set_alpha(alpha)

    @property
    def image(self) -> pg.Surface:
        return self._image

    @property
    def rect(self) -> pg.Rect:
        return self._rect

    @property
    def mask(self) -> pg.mask.Mask:
        return self._mask

    @property
    def pos(self) -> pg.Vector2:
        return self._pos

    @pos.setter
    def pos(self, pos: tuple[float]) -> None:
        self._pos.update(pos)

    @property
    def speed(self) -> pg.Vector2:
        return self._speed

    @speed.setter
    def speed(self, speed: tuple[float]) -> None:
        # reset gravity if speed is set
        self._speed.update(speed)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self._speed = self._speed.elementwise() * self._friction
        self._speed += self._gravity
        self._pos += self._speed

    def _load_image(self,
                    image_file: str,
                    size: tuple[int],
                    color: Any) -> pg.Surface:
        try:
            image = pg.image.load(image_file)
        except (FileNotFoundError, TypeError, pg.error):
            print(f"Error: Unable to load image file: {image_file}")
            image = pg.Surface(size)
            image.fill(color)
        return image.convert_alpha()
