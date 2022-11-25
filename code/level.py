import pygame as pg
from code.mysprite import MySprite


DEFAULT_SIZE = (320, 240)
DEFAULT_BACKGROUND_COLOR = "black"


class Level(pg.sprite.Group):
    def __init__(self, *sprites:MySprite) -> None:
        super().__init__(sprites)
