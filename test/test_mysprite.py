from code.mysprite import MySprite
import pygame as pg
import unittest


class TestMySprite(unittest.TestCase):

    def setUp(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        pg.display.set_caption("Sprite Test")
        self.clock = pg.time.Clock()

        self.mysprite = MySprite(pg.Vector2(400, 300), pg.Vector2(0, 0))
        self.mysprite.rect.center = (400, 300)

        self.group = pg.sprite.Group()
        self.group.add(self.mysprite)

    def test_mysprite(self):

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                if event.type == pg.MOUSEBUTTONUP and self.mysprite.rect.collidepoint(event.pos):
                    return True

            self.screen.fill(pg.Color("green"))
            self.group.draw(self.screen)
            self.group.update()

            pg.display.flip()
            self.clock.tick(60)

    def tearDown(self) -> None:
        pg.quit()
