import pygame
from pygame import mixer
from components.config import CONFIG, CONST, Fonts
from components.events import process
from components.font import Font
from components.sfx_collection import SFX
from screens.menu import update_menu


def update():
    cooldown = 3000  # ms
    last = pygame.time.get_ticks()

    mixer.Sound.play(SFX.INTRO)

    while CONFIG.is_running:
        CONFIG.clock.tick(CONFIG.FPS)
        CONFIG.surface.fill(CONST.COL_MAIN_BACKGROUND)

        now = pygame.time.get_ticks()

        # region 인트로 : 동적 Saypixel ....
        # if now - last >= cooldown:
        #     if colon_count == 4:
        #         update_menu()
        #         return
        #
        #     last = now
        #     text = 'Saypixel' + '.' * colon_count
        #
        #     colon_count += 1
        #     menu_title = Font.get(Font.TITLE3, 40).render(text, True, CONST.COL_WHITE)
        #     rect_menu = menu_title.get_rect(center=(320, 180))
        #
        #     screen.blit(menu_title, rect_menu)
        #     pygame.display.update()
        # endregion
        # region 인트로 : 정적
        menu_title = Font(Fonts.TITLE3, 40).render('Saypixel', CONST.COL_WHITE)
        rect_menu = menu_title.get_rect(center=(320, 180))

        CONFIG.surface.blit(menu_title, rect_menu)
        CONFIG.update_screen()

        if now - last >= cooldown:
            update_menu()
            return

        # endregion

        process()