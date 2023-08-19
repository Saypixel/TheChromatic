import pygame

from components.button import Button
from components.config import CONFIG, debug
from components.events import process, update_screen_resolution
from components.sfx_collection import SFX

from screens.settings import update_settings

surface_recovered: pygame.Surface
need_to_exit = False


def update_pause_menu():
    def process_menu(event: pygame.event.Event):
        """인게임 이벤트 처리용 (process() child 함수)"""

        global need_to_exit

        match event.type:
            case pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 시
                if button_play.check_for_input(menu_mouse_pos):  # 돌아가기
                    need_to_exit = True
                    return

                if button_settings.check_for_input(menu_mouse_pos):  # 설정
                    update_settings()
                    return

                if button_fullscreen.check_for_input(menu_mouse_pos):  # 전체화면
                    CONFIG.is_fullscreen = not CONFIG.is_fullscreen

                    path = (
                        "assets/images/button_window.png"
                        if CONFIG.is_fullscreen
                        else "assets/images/button_fullscreen.png"
                    )
                    image = pygame.image.load(path)

                    button_fullscreen.change_image(image)
                    update_screen_resolution()
                    return

                if button_unmute.check_for_input(menu_mouse_pos):  # 음소거
                    path = (
                        "assets/images/button_unmute.png"
                        if SFX.muted
                        else "assets/images/button_mute.png"
                    )
                    image = pygame.image.load(path)
                    image = pygame.transform.scale_by(image, 0.2)

                    SFX.control_mute()
                    button_unmute.change_image(image)

                    if not SFX.muted:
                        SFX.UNMUTED.play()

                    return

                if button_exit.check_for_input(menu_mouse_pos):  # 나가기
                    from .ingame import Ingame

                    need_to_exit = True
                    Ingame.default.need_to_exit = True
                    return

            case pygame.KEYUP:
                match event.key:
                    case pygame.K_ESCAPE:
                        need_to_exit = True

    global need_to_exit
    surface_recovered = CONFIG.surface.copy()

    background = pygame.image.load("assets/images/status3.png")
    background = pygame.transform.scale_by(background, 0.2)
    background = pygame.transform.rotate(background, 90)
    background_rect = background.get_rect(center=(320 + CONFIG.camera_x, 180 + CONFIG.camera_y))

    button_play_image = pygame.image.load("assets/images/button_play.png")
    button_play_image = pygame.transform.scale_by(button_play_image, 0.2)
    button_play = Button(image=button_play_image, pos=(290, 140))

    button_settings_image = pygame.image.load("assets/images/button_settings.png")
    button_settings_image = pygame.transform.scale_by(button_settings_image, 0.2)
    button_settings = Button(image=button_settings_image, pos=(350, 140))

    button_fullscreen_image = pygame.image.load("assets/images/button_fullscreen.png")
    button_fullscreen = Button(image=button_fullscreen_image, pos=(260, 200))

    button_unmute_image = pygame.image.load("assets/images/button_unmute.png")
    button_unmute_image = pygame.transform.scale_by(button_unmute_image, 0.2)
    button_unmute = Button(image=button_unmute_image, pos=(320, 200))

    button_exit_image = pygame.image.load("assets/images/button_exit.png")
    button_exit = Button(image=button_exit_image, pos=(380, 200))

    while CONFIG.is_running and not need_to_exit:
        CONFIG.clock.tick(CONFIG.FPS)

        menu_mouse_pos = CONFIG.get_mouse_pos()

        # 전체화면 동기화
        path = (
            "assets/images/button_window.png"
            if CONFIG.is_fullscreen
            else "assets/images/button_fullscreen.png"
        )
        image = pygame.image.load(path)

        button_fullscreen.change_image(image)

        # 음소거 동기화
        path = (
            "assets/images/button_mute.png"
            if SFX.muted
            else "assets/images/button_unmute.png"
        )
        image = pygame.image.load(path)
        image = pygame.transform.scale_by(image, 0.2)

        button_unmute.change_image(image)

        CONFIG.surface.blit(background, background_rect)

        for button in [
            button_play,
            button_settings,
            button_fullscreen,
            button_unmute,
            button_exit,
        ]:
            button.change_color(menu_mouse_pos)
            button.update(CONFIG.surface)

        CONFIG.update_screen()

        process(process_menu)

    CONFIG.surface = surface_recovered
    need_to_exit = False
