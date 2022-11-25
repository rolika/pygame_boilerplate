import pygame as pg
import typing
from code.mysprite import MySprite


DEFAULT_SIZE = (320, 240)
DEFAULT_BACKGROUND_COLOR = "black"


class Level(pg.sprite.Group):
    def __init__(self,
                 level_image,
                 background_image=None,
                 size=DEFAULT_SIZE,
                 background_color=DEFAULT_BACKGROUND_COLOR) -> None:
        self._background_color = \
            MySprite((0, 0), (0, 0), size=size, color=background_color, nomask=True)
        self._level_image = \
            MySprite((0, 0), (0, 0), image_file=level_image)
        super().__init__(self._background_color, self._level_image)
        if background_image:
            self._background_image = \
                MySprite((0, 0), (0, 0), image_file=background_image, nomask=True)
            self.add(self._background_image)
