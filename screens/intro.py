import pygame
from pygame import mixer
from components.config import CONFIG, CONST, Fonts, debug
from components.events import process
from components.font import Font
from components.sfx_collection import SFX
from screens.menu import update_menu


def update():
    cooldown = 1000  # ms
    last = pygame.time.get_ticks()

    text = "Saypixel"
    colon_count = 1

    SFX.INTRO.play()

    while CONFIG.is_running:
        CONFIG.clock.tick(CONFIG.FPS)
        CONFIG.surface.fill(CONST.COL_MAIN_BACKGROUND)

        for event in pygame.event.get():
            match event.type:
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_BACKQUOTE:
                            update_menu()
                            reload()

                        case pygame.K_ESCAPE:
                            CONFIG.is_running = False

        now = pygame.time.get_ticks()

        # region 인트로 : 동적 Saypixel ....
        if now - last >= cooldown:
            if colon_count == 4:
                update_menu()
                return

            last = now
            text = "Saypixel" + "." * colon_count

            colon_count += 1
        # endregion
        # region 인트로 : 정적
        menu_title = Font(Fonts.TITLE3, 40).render(text, CONST.COL_WHITE)
        rect_menu = menu_title.get_rect(center=(320, 180))

        CONFIG.surface.blit(menu_title, rect_menu)
        CONFIG.update_screen()

        if now - last >= cooldown:
            update_menu()
            reload()
            return

        # endregion

        process()


def reload():
    import screens.menu

    if screens.menu.reload:
        screens.menu.reload = False

        pygame.mixer.music.stop()

        pygame.mixer.pause()
        pygame.mixer.unpause()

        update()
        reload()
