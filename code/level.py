import pygame as pg
from code.rsprite import RSprite


DEFAULT_SIZE = (320, 240)
DEFAULT_BACKGROUND_COLOR = "black"


class Level(pg.sprite.Group):
    def __init__(self, *sprites:RSprite) -> None:
        super().__init__(sprites)
