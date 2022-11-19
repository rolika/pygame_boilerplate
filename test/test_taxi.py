"""Test facilities with a Space Taxi-like game."""


from code.mysprite import MySprite
import pygame as pg
import unittest


SPEED = 0.05
FRICTION = (0.95, 0.95)
GRAVITY = (0, 0.00005)


class TestTaxi(unittest.TestCase):
    """Close the window to end the tests."""

    def setUp(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((320, 240), flags=pg.SCALED)
        self.screen_rect = self.screen.get_rect()
        pg.display.set_caption("Space Taxi")
        self.clock = pg.time.Clock()

    def test_taxi_game(self):
        level = MySprite((0, 0), (0, 0), "test/taxi_scene.png")
        scene = pg.sprite.GroupSingle(level)

        taxi = MySprite((300, 200), (0, 0), size=(16, 8), color="orange", gravity=GRAVITY, friction=FRICTION)
        player = pg.sprite.GroupSingle(taxi)
        hull = 4
        # although the taxi has only 3 lives (hulls), an original hull damage
        # seems to occur, so the if i want 3 hulls, i have to start with a 4
        # perhaps it's because one sprite is inside another

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

            self.screen.fill("black")
            scene.draw(self.screen)

            # handle key input
            keys = pg.key.get_pressed()
            if keys[pg.K_KP4]:
                taxi.speed += (-SPEED, 0)
            elif keys[pg.K_KP6]:
                taxi.speed += (SPEED, 0)
            elif keys[pg.K_KP8]:
                taxi.speed += (0, -SPEED)
            elif keys[pg.K_KP2]:
                taxi.speed += (0, SPEED)
            elif keys[pg.K_KP7]:
                taxi.speed += (-SPEED, -SPEED)
            elif keys[pg.K_KP9]:
                taxi.speed += (SPEED, -SPEED)
            elif keys[pg.K_KP1]:
                taxi.speed += (-SPEED, SPEED)
            elif keys[pg.K_KP3]:
                taxi.speed += (SPEED, SPEED)

            # cave walls damages the taxi
            if pg.sprite.spritecollideany(taxi, scene, collided=pg.sprite.collide_mask):
                taxi.speed.rotate_ip(180)
                hull -= 1
            
            if hull < 1:
                return

            player.update()
            taxi.rect.center = taxi.pos

            player.draw(self.screen)

            pg.display.flip()
            self.clock.tick(60)


    def tearDown(self) -> None:
        pg.quit()