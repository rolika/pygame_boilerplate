"""Test facilities with a Space Taxi-like game."""


from code.mysprite import MySprite
from code.level import Level
import pygame as pg
import unittest
import typing


SPEED = 0.05
FRICTION = (0.99, 0.99)
GRAVITY = (0, 0.00005)


class Taxi(MySprite):
    def __init__(self, pos: tuple[int, int], speed: tuple[float, float], image_file: str = None, **kwargs: typing.Any) -> None:
        super().__init__(pos, speed, image_file, **kwargs)
        # although the taxi has only 3 lives (hulls), an original hull damage
        # seems to occur, so if i want 3 hulls, i have to start with a 4
        # perhaps it's because one sprite is inside another
        self._hull = 4
        self._passenger = pg.sprite.GroupSingle()

    def collide(self):
        self.speed.rotate_ip(180)
        self._hull -= 1

    def is_wrecked(self) -> bool:
        return self._hull < 1

    def get_input(self, keys):
        if keys[pg.K_KP4]:
            self.speed += (-SPEED, 0)
        elif keys[pg.K_KP6]:
            self.speed += (SPEED, 0)
        elif keys[pg.K_KP8]:
            self.speed += (0, -SPEED)
        elif keys[pg.K_KP2]:
            self.speed += (0, SPEED)
        elif keys[pg.K_KP7]:
            self.speed += (-SPEED, -SPEED)
        elif keys[pg.K_KP9]:
            self.speed += (SPEED, -SPEED)
        elif keys[pg.K_KP1]:
            self.speed += (-SPEED, SPEED)
        elif keys[pg.K_KP3]:
            self.speed += (SPEED, SPEED)

    def update(self, *args, **kwargs):
        super().update()
        self.rect.center = self.pos

    @property
    def passenger(self) -> MySprite:
        return self._passenger.sprite

    def pickup(self, survivor:MySprite) -> None:
        self._passenger.add(survivor)

    def deliver(self) -> MySprite:
        survivor = self._passenger.sprite
        self._passenger.empty()
        return survivor


class Survivors(pg.sprite.Group):
    def __init__(self, *sprites: typing.Union[MySprite, typing.Sequence[MySprite]]) -> None:
        super().__init__(*sprites)

    def all_safe(self) -> bool:
        return not bool(self)

    def update(self, *args, **kwargs):
        for survivor in self:
            survivor.rect.topleft = survivor.pos


class Rescued(pg.sprite.Group):
    def __init__(self, *sprites: typing.Union[MySprite, typing.Sequence[MySprite]]) -> None:
        super().__init__(*sprites)

    def update(self, *args, **kwargs):
        for i, survivor in enumerate(self):
            survivor.rect.topleft = (240 + i * 8, 8)


class Level1(Level):
    def __init__(self, level_image, bgr_image) -> None:
        super().__init__(level_image, background_image=bgr_image)


class TestTaxi(unittest.TestCase):
    """Close the window to end the tests."""

    def setUp(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((320, 240), flags=pg.SCALED)
        self.screen_rect = self.screen.get_rect()
        pg.display.set_caption("Space Rescue")
        self.clock = pg.time.Clock()

    def test_taxi_game(self):
        # setup level
        scene = Level1("test/taxi_scene.png", "test/taxi_bgr_img.png")
        rescue_area = pg.Rect(288, 192, 32, 32)

        # setup player
        taxi = Taxi((300, 200), (0, 0), size=(16, 8), color="orange", gravity=GRAVITY, friction=FRICTION)
        player = pg.sprite.GroupSingle(taxi)

        # setup survivors
        survivors = pg.sprite.Group()
        survivor1 = MySprite((50, 214), (0, 0), size=(4, 8), color="blue")
        survivor2 = MySprite((130, 84), (0, 0), size=(4, 8), color="red")
        survivor3 = MySprite((280, 170), (0, 0), size=(4, 8), color="purple")
        survivors = Survivors(survivor1, survivor2, survivor3)
        rescued = Rescued()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

            self.screen.fill("black")
            scene.draw(self.screen)

            # handle key input
            taxi.get_input(pg.key.get_pressed())

            # cave walls damages the taxi
            if pg.sprite.spritecollideany(taxi, scene, collided=pg.sprite.collide_mask):
                taxi.collide()
                if taxi.is_wrecked():
                    return

            player.update()

            # if the taxi meets a survivor and it's vacant, pick him up
            survivor = pg.sprite.spritecollide(taxi, survivors, False)
            if not taxi.passenger:
                survivors.remove(survivor)
                taxi.pickup(survivor)

            # check if the taxi is in the rescue area, and if it's occupied,
            # deliver the survivor
            if rescue_area.contains(taxi.rect):
                survivor = taxi.deliver()
                if survivor:
                    rescued.add(survivor)
                    # end game if all survivors rescued
                    # check here in the if statement!
                    if survivors.all_safe():
                        return

            survivors.update()
            survivors.draw(self.screen)

            rescued.update()
            rescued.draw(self.screen)

            player.draw(self.screen)

            pg.display.flip()
            self.clock.tick(60)


    def tearDown(self) -> None:
        pg.quit()