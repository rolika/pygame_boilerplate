from constants import SCREEN_SIZE, SCREEN_TITLE, FPS
import pygame as pg
import sys
from state import State



def main(size: tuple[int],
         fps: int,
         bgr: pg.Color,
         title: str,
         state: State) -> None:

    pg.init()
    screen = pg.display.set_mode(size)
    pg.display.set_caption(title)
    clock = pg.time.Clock()

    while state != State.QUIT:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                state = State.QUIT
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                        state = State.QUIT

        screen.fill(bgr)

        if state == State.TITLE:
            pass
        elif state == State.INSTRUCTIONS:
            pass
        elif state == State.PLAY:
            pass
        elif state == State.PAUSED:
            pass
        elif state == State.GAME_OVER:
            pass

        pg.display.flip()
        clock.tick(fps)

    pg.quit()
    sys.exit()


if __name__ == '__main__':
    main(size=SCREEN_SIZE,
         fps=FPS,
         bgr=pg.Color('green'),
         title=SCREEN_TITLE,
         state=State.TITLE)
