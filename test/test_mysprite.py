from code.mysprite import MySprite
import pygame as pg
import unittest


SPEED = 0.3
FRICTION = (0.95, 0.95)


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
        sprite1 = MySprite((100, 100), (2, 6))
        sprite2 = MySprite((400, 300), (-4, -4), size=(10, 10), color="black")
        sprite3 = MySprite((600, 300), (2, 4), size=(32, 32), color="red")
        sprite4 = MySprite((700, 500), (-4, -6), size=(64, 64), color="blue")
        group = pg.sprite.Group()
        group.add(sprite1, sprite2, sprite3, sprite4)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

            self.screen.fill(pg.Color("green"))

            # test logic here
            for sprite in group:
                subgroup = group.copy()
                subgroup.remove(sprite)
                for other in subgroup:
                    if sprite.rect.colliderect(other.rect):
                        # substract vectors to get reflection plane
                        sprite.speed.reflect_ip(sprite.speed - other.speed)
                if not self.screen_rect.contains(sprite.rect):
                    if self.screen_rect.left > sprite.rect.left:
                        sprite.speed.reflect_ip((1, 0))
                    if self.screen_rect.right < sprite.rect.right:
                        sprite.speed.reflect_ip((-1, 0))
                    if self.screen_rect.top > sprite.rect.top:
                        sprite.speed.reflect_ip((0, 1))
                    if self.screen_rect.bottom < sprite.rect.bottom:
                        sprite.speed.reflect_ip((0, -1))

            group.update()
            for sprite in group:
                sprite.rect.center = sprite.pos
            group.draw(self.screen)

            pg.display.flip()
            self.clock.tick(60)

    def test_stay_on_screen_keyboard(self):
        sprite = MySprite((400, 300), (0, 0), size=(16, 32), color="black")
        group = pg.sprite.GroupSingle()
        group.add(sprite)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

            self.screen.fill(pg.Color("green"))

            # test logic here
            # order of procedures is important

            # handle key input
            keys = pg.key.get_pressed()
            if keys[pg.K_KP4]:
                sprite.speed = (-3, 0)
            elif keys[pg.K_KP6]:
                sprite.speed = (3, 0)
            elif keys[pg.K_KP8]:
                sprite.speed = (0, -3)
            elif keys[pg.K_KP2]:
                sprite.speed = (0, 3)
            elif keys[pg.K_KP7]:
                sprite.speed = (-3, -3)
            elif keys[pg.K_KP9]:
                sprite.speed = (3, -3)
            elif keys[pg.K_KP1]:
                sprite.speed = (-3, 3)
            elif keys[pg.K_KP3]:
                sprite.speed = (3, 3)
            else:
                sprite.speed = (0, 0)

            # update the sprite
            group.update()
            sprite.rect.center = sprite.pos

            # keep sprite on screen
            if not self.screen_rect.contains(sprite.rect):
                if self.screen_rect.left >= sprite.rect.left:
                    sprite.rect.left = self.screen_rect.left
                if self.screen_rect.right <= sprite.rect.right:
                    sprite.rect.right = self.screen_rect.right
                if self.screen_rect.top >= sprite.rect.top:
                    sprite.rect.top = self.screen_rect.top
                if self.screen_rect.bottom <= sprite.rect.bottom:
                    sprite.rect.bottom = self.screen_rect.bottom
                # update position to the restricted position
                sprite.pos = sprite.rect.center

            # finally draw the sprite
            group.draw(self.screen)

            pg.display.flip()
            self.clock.tick(60)

    def test_accelerate_sprite(self):
        sprite = MySprite((400, 300), (0, 0), size=(16, 32), color="black")
        group = pg.sprite.GroupSingle()
        group.add(sprite)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

            self.screen.fill(pg.Color("green"))

            # test logic here: Space Taxi :-D
            # order of procedures is important

            # handle key input
            keys = pg.key.get_pressed()
            if keys[pg.K_KP4]:
                sprite.speed += (-SPEED, 0)
            elif keys[pg.K_KP6]:
                sprite.speed += (SPEED, 0)
            elif keys[pg.K_KP8]:
                sprite.speed += (0, -SPEED)
            elif keys[pg.K_KP2]:
                sprite.speed += (0, SPEED)
            elif keys[pg.K_KP7]:
                sprite.speed += (-SPEED, -SPEED)
            elif keys[pg.K_KP9]:
                sprite.speed += (SPEED, -SPEED)
            elif keys[pg.K_KP1]:
                sprite.speed += (-SPEED, SPEED)
            elif keys[pg.K_KP3]:
                sprite.speed += (SPEED, SPEED)

            # update the sprite
            group.update()
            sprite.rect.center = sprite.pos

            # keep sprite on screen
            if not self.screen_rect.contains(sprite.rect):
                if self.screen_rect.left >= sprite.rect.left:
                    sprite.rect.left = self.screen_rect.left
                    sprite.speed.x = 0
                if self.screen_rect.right <= sprite.rect.right:
                    sprite.rect.right = self.screen_rect.right
                    sprite.speed.x = 0
                if self.screen_rect.top >= sprite.rect.top:
                    sprite.rect.top = self.screen_rect.top
                    sprite.speed.y = 0
                if self.screen_rect.bottom <= sprite.rect.bottom:
                    sprite.rect.bottom = self.screen_rect.bottom
                    sprite.speed.y = 0
                # update position to the restricted position
                sprite.pos = sprite.rect.center

            # finally draw the sprite
            group.draw(self.screen)

            pg.display.flip()
            self.clock.tick(60)

    def test_friction(self):
        sprite = MySprite((400, 300), (0, 0), size=(16, 32), color="black", friction=FRICTION)
        group = pg.sprite.GroupSingle()
        group.add(sprite)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

            self.screen.fill(pg.Color("green"))

            # test logic here
            # order of procedures is important

            # handle key input
            keys = pg.key.get_pressed()
            if keys[pg.K_KP4]:
                sprite.speed += (-SPEED, 0)
            elif keys[pg.K_KP6]:
                sprite.speed += (SPEED, 0)
            elif keys[pg.K_KP8]:
                sprite.speed += (0, -SPEED)
            elif keys[pg.K_KP2]:
                sprite.speed += (0, SPEED)
            elif keys[pg.K_KP7]:
                sprite.speed += (-SPEED, -SPEED)
            elif keys[pg.K_KP9]:
                sprite.speed += (SPEED, -SPEED)
            elif keys[pg.K_KP1]:
                sprite.speed += (-SPEED, SPEED)
            elif keys[pg.K_KP3]:
                sprite.speed += (SPEED, SPEED)

            # update the sprite
            group.update()
            sprite.rect.center = sprite.pos

            # keep sprite on screen
            if not self.screen_rect.contains(sprite.rect):
                if self.screen_rect.left >= sprite.rect.left:
                    sprite.rect.left = self.screen_rect.left
                    sprite.speed.x = 0
                if self.screen_rect.right <= sprite.rect.right:
                    sprite.rect.right = self.screen_rect.right
                    sprite.speed.x = 0
                if self.screen_rect.top >= sprite.rect.top:
                    sprite.rect.top = self.screen_rect.top
                    sprite.speed.y = 0
                if self.screen_rect.bottom <= sprite.rect.bottom:
                    sprite.rect.bottom = self.screen_rect.bottom
                    sprite.speed.y = 0
                # update position to the restricted position
                sprite.pos = sprite.rect.center

            # finally draw the sprite
            group.draw(self.screen)

            pg.display.flip()
            self.clock.tick(60)

    def test_gravity(self):
        sprite = MySprite((400, 300), (0, 0), size=(16, 32), color="black", gravity=(0.0, .005))
        group = pg.sprite.GroupSingle()
        group.add(sprite)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

            self.screen.fill(pg.Color("green"))

            # test logic here
            # order of procedures is important

            # handle key input
            keys = pg.key.get_pressed()
            if keys[pg.K_KP4]:
                sprite.speed += (-SPEED, 0)
            elif keys[pg.K_KP6]:
                sprite.speed += (SPEED, 0)
            elif keys[pg.K_KP8]:
                sprite.speed += (0, -SPEED)
            elif keys[pg.K_KP2]:
                sprite.speed += (0, SPEED)
            elif keys[pg.K_KP7]:
                sprite.speed += (-SPEED, -SPEED)
            elif keys[pg.K_KP9]:
                sprite.speed += (SPEED, -SPEED)
            elif keys[pg.K_KP1]:
                sprite.speed += (-SPEED, SPEED)
            elif keys[pg.K_KP3]:
                sprite.speed += (SPEED, SPEED)

            # update the sprite
            group.update()
            sprite.rect.center = sprite.pos

            # keep sprite on screen
            if not self.screen_rect.contains(sprite.rect):
                if self.screen_rect.left >= sprite.rect.left:
                    sprite.rect.left = self.screen_rect.left
                    sprite.speed.x = 0
                if self.screen_rect.right <= sprite.rect.right:
                    sprite.rect.right = self.screen_rect.right
                    sprite.speed.x = 0
                if self.screen_rect.top >= sprite.rect.top:
                    sprite.rect.top = self.screen_rect.top
                    sprite.speed.y = 0
                if self.screen_rect.bottom <= sprite.rect.bottom:
                    sprite.rect.bottom = self.screen_rect.bottom
                    sprite.speed.y = 0
                # update position to the restricted position
                sprite.pos = sprite.rect.center

            # finally draw the sprite
            group.draw(self.screen)

            pg.display.flip()
            self.clock.tick(60)

    def test_gravity_with_friction(self):
        sprite = MySprite((400, 300), (0, 0), size=(16, 32), color="black", gravity=(0.0, .005), friction=(0.9, 1.0))
        group = pg.sprite.GroupSingle()
        group.add(sprite)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

            self.screen.fill(pg.Color("green"))

            # test logic here
            # order of procedures is important

            # handle key input
            keys = pg.key.get_pressed()
            if keys[pg.K_KP4]:
                sprite.speed += (-SPEED, 0)
            elif keys[pg.K_KP6]:
                sprite.speed += (SPEED, 0)
            elif keys[pg.K_KP8]:
                sprite.speed += (0, -SPEED)
            elif keys[pg.K_KP2]:
                sprite.speed += (0, SPEED)
            elif keys[pg.K_KP7]:
                sprite.speed += (-SPEED, -SPEED)
            elif keys[pg.K_KP9]:
                sprite.speed += (SPEED, -SPEED)
            elif keys[pg.K_KP1]:
                sprite.speed += (-SPEED, SPEED)
            elif keys[pg.K_KP3]:
                sprite.speed += (SPEED, SPEED)

            # update the sprite
            group.update()
            sprite.rect.center = sprite.pos

            # keep sprite on screen
            if not self.screen_rect.contains(sprite.rect):
                if self.screen_rect.left >= sprite.rect.left:
                    sprite.rect.left = self.screen_rect.left
                    sprite.speed.x = 0
                if self.screen_rect.right <= sprite.rect.right:
                    sprite.rect.right = self.screen_rect.right
                    sprite.speed.x = 0
                if self.screen_rect.top >= sprite.rect.top:
                    sprite.rect.top = self.screen_rect.top
                    sprite.speed.y = 0
                if self.screen_rect.bottom <= sprite.rect.bottom:
                    sprite.rect.bottom = self.screen_rect.bottom
                    sprite.speed.y = 0
                # update position to the restricted position
                sprite.pos = sprite.rect.center

            # finally draw the sprite
            group.draw(self.screen)

            pg.display.flip()
            self.clock.tick(60)


    def tearDown(self) -> None:
        pg.quit()
