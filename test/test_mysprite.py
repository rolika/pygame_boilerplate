from code.mysprite import MySprite
import pygame as pg
import unittest


class TestMySprite(unittest.TestCase):
    """Close the window to end the tests."""

    def setUp(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        self.screen_rect = self.screen.get_rect()
        pg.display.set_caption("Sprite Test")
        self.clock = pg.time.Clock()

    def test_blank_sprite(self):
        mysprite = MySprite((400, 300), (0, 0))
        group = pg.sprite.Group()
        group.add(mysprite)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

            self.screen.fill(pg.Color("green"))

            # test logic here
            mysprite.rect.center = mysprite.pos

            group.draw(self.screen)
            group.update()

            pg.display.flip()
            self.clock.tick(60)

    def test_bounce_sprite(self):
        mysprite = MySprite((400, 300), (1, 3))
        group = pg.sprite.Group()
        group.add(mysprite)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

            self.screen.fill(pg.Color("green"))

            # test logic here
            if not self.screen_rect.contains(mysprite.rect):
                if self.screen_rect.left > mysprite.rect.left:
                    mysprite.speed.reflect_ip((1, 0))
                if self.screen_rect.right < mysprite.rect.right:
                    mysprite.speed.reflect_ip((-1, 0))
                if self.screen_rect.top > mysprite.rect.top:
                    mysprite.speed.reflect_ip((0, 1))
                if self.screen_rect.bottom < mysprite.rect.bottom:
                    mysprite.speed.reflect_ip((0, -1))

            group.update()
            mysprite.rect.center = mysprite.pos
            group.draw(self.screen)

            pg.display.flip()
            self.clock.tick(60)

    def test_multiple_bounce_sprite(self):
        sprite1 = MySprite((100, 100), (1, 3))
        sprite2 = MySprite((400, 300), (-2, -2), size=(10, 10), color="black")
        sprite3 = MySprite((600, 300), (1, 2), size=(32, 32), color="red")
        sprite4 = MySprite((700, 500), (-2, -3), size=(64, 64), color="blue")
        group = pg.sprite.Group()
        group.add(sprite1, sprite2, sprite3, sprite4)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

            self.screen.fill(pg.Color("green"))

            # test logic here
            for sprite in group:
                if not self.screen_rect.contains(sprite.rect):
                    if self.screen_rect.left > sprite.rect.left:
                        sprite.speed.reflect_ip((1, 0))
                    if self.screen_rect.right < sprite.rect.right:
                        sprite.speed.reflect_ip((-1, 0))
                    if self.screen_rect.top > sprite.rect.top:
                        sprite.speed.reflect_ip((0, 1))
                    if self.screen_rect.bottom < sprite.rect.bottom:
                        sprite.speed.reflect_ip((0, -1))
                subgroup = group.copy()
                subgroup.remove(sprite)
                for other in subgroup:
                    if sprite.rect.colliderect(other.rect):
                        sprite.speed.reflect_ip(other.speed)

            group.update()
            for sprite in group:
                sprite.rect.center = sprite.pos
            group.draw(self.screen)

            pg.display.flip()
            self.clock.tick(60)


    def tearDown(self) -> None:
        pg.quit()
