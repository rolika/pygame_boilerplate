from code.mysprite import MySprite
import pygame as pg
import unittest


class TestMySprite(unittest.TestCase):

    def setUp(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        self.screen_rect = self.screen.get_rect()
        pg.display.set_caption("Sprite Test")
        self.clock = pg.time.Clock()

    def test_blank_sprite(self):
        """Close the window to end the test."""
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
        """Close the window to end the test."""
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

    def tearDown(self) -> None:
        pg.quit()
