import pygame as pg
from typing import Any
from code.constants import DEFAULT_SPRITE_COLOR, DEFAULT_SPRITE_SIZE


class MySprite(pg.sprite.Sprite):
    def __init__(self, pos: pg.Vector2, speed: pg.Vector2, image_file: str = None) -> None:
        super().__init__()
        self._pos = pos
        self._speed = speed
        self._image = self._load_image(image_file)
        self._image.convert_alpha()
        self._rect = self._image.get_rect()
    
    @property
    def image(self) -> pg.Surface:
        return self._image
    
    @property
    def rect(self) -> pg.Rect:
        return self._rect
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        self._pos += self._speed
        self._rect.center = self._pos
    
    def _load_image(self, image_file: str) -> pg.Surface:
        try:
            image = pg.image.load(image_file)
        except (TypeError, pg.error):
            print(f"Error: Unable to load image file: {image_file}")
            image = pg.Surface(DEFAULT_SPRITE_SIZE)
            image.fill(DEFAULT_SPRITE_COLOR)
        return image
