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

        self.mysprite = MySprite((400, 300), (0, 0))

        self.group = pg.sprite.Group()
        self.group.add(self.mysprite)

    def test_blank_sprite(self):
        """Click the sprite to signal the successful completion of the test."""
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return True
                if event.type == pg.MOUSEBUTTONUP and self.mysprite.rect.collidepoint(event.pos):
                    return True

            self.screen.fill(pg.Color("green"))

            # test logic here
            self.mysprite.rect.center = self.mysprite.pos
            self.group.draw(self.screen)

            self.group.update()

            pg.display.flip()
            self.clock.tick(60)

    def test_bounce_sprite(self):
        """Click the sprite to signal the successful completion of the test."""
        self.mysprite.speed = (1, 3)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                if event.type == pg.MOUSEBUTTONUP and self.mysprite.rect.collidepoint(event.pos):
                    return True

            self.screen.fill(pg.Color("green"))

            # test logic here
            if not self.screen_rect.contains(self.mysprite.rect):
                if self.screen_rect.left > self.mysprite.rect.left:
                    self.mysprite.speed.reflect_ip((1, 0))
                if self.screen_rect.right < self.mysprite.rect.right:
                    self.mysprite.speed.reflect_ip((-1, 0))
                if self.screen_rect.top > self.mysprite.rect.top:
                    self.mysprite.speed.reflect_ip((0, 1))
                if self.screen_rect.bottom < self.mysprite.rect.bottom:
                    self.mysprite.speed.reflect_ip((0, -1))

            self.group.update()
            self.mysprite.rect.center = self.mysprite.pos
            self.group.draw(self.screen)

            pg.display.flip()
            self.clock.tick(60)

    def tearDown(self) -> None:
        pg.quit()
