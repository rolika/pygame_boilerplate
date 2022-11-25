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
        super().__init__()
        self._background_color = \
            MySprite((0, 0), (0, 0), size=size, color=background_color, nomask=True)
        self.add(self._background_color)
        if background_image:
            self._background_image = \
                MySprite((0, 0), (0, 0), image_file=background_image, nomask=True)
            self.add(self._background_image)
        self._level_image = \
            MySprite((0, 0), (0, 0), image_file=level_image)
        self.add(self._level_image)
