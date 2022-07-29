import pygame as pg
from typing import Any
from code.constants import DEFAULT_FRICTION,\
                           DEFAULT_GRAVITY_ACCELERATION,\
                           DEFAULT_SPRITE_COLOR,\
                           DEFAULT_SPRITE_SIZE


class MySprite(pg.sprite.Sprite):
    def __init__(self,
                 pos: tuple[float],
                 speed: tuple[float],
                 image_file: str = None,
                 **kwargs: Any) -> None:
        super().__init__()

        # fetch user-defined arguments
        size = kwargs.get("size", DEFAULT_SPRITE_SIZE)
        color = kwargs.get("color", DEFAULT_SPRITE_COLOR)
        self._friction = pg.Vector2(kwargs.get("friction", DEFAULT_FRICTION))
        self._gravity_acceleretion =\
            pg.Vector2(kwargs.get("gravity", DEFAULT_GRAVITY_ACCELERATION))
        self._gravity = self._gravity_acceleretion.copy()

        self._pos = pg.Vector2(pos)
        self._speed = pg.Vector2(speed)
        self._image = self._load_image(image_file, size, color)
        self._rect = self._image.get_rect()

    @property
    def image(self) -> pg.Surface:
        return self._image

    @property
    def rect(self) -> pg.Rect:
        return self._rect

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
        self._speed.update(speed)

    @property
    def friction(self) -> pg.Vector2:
        return self._friction

    @friction.setter
    def friction(self, friction: tuple[float]) -> None:
        self._friction.update(friction)

    @property
    def gravity(self) -> pg.Vector2:
        return self._gravity

    @gravity.setter
    def gravity(self, gravity: tuple[float]) -> None:
        self._gravity.update(gravity)

    @property
    def gravity_acceleretion(self) -> pg.Vector2:
        return self._gravity_acceleretion

    @gravity_acceleretion.setter
    def gravity_acceleretion(self, gravity_acceleretion: tuple[float]) -> None:
        self._gravity_acceleretion.update(gravity_acceleretion)

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
        except (TypeError, pg.error):
            print(f"Error: Unable to load image file: {image_file}")
            image = pg.Surface(size)
            image.fill(color)
        return image.convert_alpha()
