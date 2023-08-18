import pygame

from components.button import Button
from components.config import CONFIG, CONST, Fonts, debug
from components.events import process, update_screen_resolution
from components.font import Font
from components.sfx_collection import SFX

surface_recovered: pygame.Surface
need_to_exit = False


def update_settings():
    def apply():
        CONFIG.window_size = resolution
        CONFIG.window_scale = resolution[0] / CONST.SCREEN_SIZE[0]
        CONFIG.is_fullscreen = is_fullscreen
        CONFIG.game_fps = fps

        SFX.set_volume(volume)

        update_screen_resolution()

    def process_menu(event: pygame.event.Event):
        """인게임 이벤트 처리용 (process() child 함수)"""

        global need_to_exit
        nonlocal resolution, resolutions_index, is_fullscreen, fps, volume

        match event.type:
            case pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 시
                if button_resolution_prev.check_for_input(menu_mouse_pos):  # 화면/이전
                    if resolutions_index > 0:
                        resolutions_index -= 1
                        resolution = resolutions[resolutions_index]

                if button_resolution_next.check_for_input(menu_mouse_pos):  # 화면/다음
                    if resolutions_index < len(resolutions) - 1:
                        resolutions_index += 1
                        resolution = resolutions[resolutions_index]

                if button_resolution_full.check_for_input(menu_mouse_pos):  # 전체화면
                    is_fullscreen = not is_fullscreen

                    path = (
                        "assets/images/button_checked.png"
                        if is_fullscreen
                        else "assets/images/button_unchecked.png"
                    )
                    image = pygame.image.load(path)
                    image = pygame.transform.scale_by(image, 0.2)

                    button_resolution_full.change_image(image)

                if button_fps.check_for_input(menu_mouse_pos):  # FPS 표시
                    fps = not fps

                    path = (
                        "assets/images/button_checked.png"
                        if fps
                        else "assets/images/button_unchecked.png"
                    )
                    image = pygame.image.load(path)
                    image = pygame.transform.scale_by(image, 0.2)

                    button_fps.change_image(image)

                if button_audio_prev.check_for_input(menu_mouse_pos):  # 소리/이전
                    if round(volume, 1) > 0.0:  # 소수점 계산 문제 방지
                        volume -= 0.1

                if button_audio_next.check_for_input(menu_mouse_pos):  # 소리/다음
                    if round(volume, 1) < 1.0:  # 소수점 계산 문제 방지
                        volume += 0.1

                if button_cancel.check_for_input(menu_mouse_pos):  # 취소
                    need_to_exit = True
                    return

                if button_ok.check_for_input(menu_mouse_pos):  # 확인
                    apply()
                    need_to_exit = True
                    return

            case pygame.KEYUP:
                match event.key:
                    case pygame.K_ESCAPE:
                        need_to_exit = True

                    case pygame.K_RETURN:
                        apply()
                        need_to_exit = True

    global need_to_exit
    surface_recovered = CONFIG.surface.copy()

    resolution: tuple[int, int] = tuple(CONFIG.window_size)
    is_fullscreen = CONFIG.is_fullscreen
    fps = CONFIG.game_fps

    volume = SFX.volume

    resolutions: list[tuple[int, int]] = [
        (640, 360),
        (1280, 720),
        (1920, 1080),
        (2560, 1440),
        (3840, 2160),
    ]
    resolutions_index = resolutions.index(tuple(CONFIG.window_size))

    background = pygame.image.load("assets/images/status3.png")
    background = pygame.transform.scale_by(background, 0.25)
    background = pygame.transform.scale(background, (background.get_width(), 300))
    background_rect = background.get_rect(center=(320 + CONFIG.camera_x, 180 + CONFIG.camera_y))

    surface_resolution_2 = Font(Fonts.TITLE2, 18).render("화면", (255, 255, 255))

    button_resolution_prev_image = pygame.image.load("assets/images/arrow_left.png")
    button_resolution_prev_image = pygame.transform.scale_by(
        button_resolution_prev_image, 0.2
    )
    button_resolution_prev = Button(image=button_resolution_prev_image, pos=(250, 90))

    button_resolution_next_image = pygame.image.load("assets/images/arrow_right.png")
    button_resolution_next_image = pygame.transform.scale_by(
        button_resolution_next_image, 0.2
    )
    button_resolution_next = Button(image=button_resolution_next_image, pos=(380, 90))

    button_resolution_full_path = (
        "assets/images/button_checked.png"
        if is_fullscreen
        else "assets/images/button_unchecked.png"
    )
    button_resolution_full_image = pygame.image.load(button_resolution_full_path)
    button_resolution_full_image = pygame.transform.scale_by(
        button_resolution_full_image, 0.2
    )
    button_resolution_full = Button(
        image=button_resolution_full_image,
        pos=(250, 125),
        text_offset=(50, 0),
        text_input="전체화면",
        font=Font(Fonts.ILLUST, 16).to_pygame(),
        base_color="#ffffff",
        hovering_color="White",
    )

    button_fps_path = (
        "assets/images/button_checked.png"
        if fps
        else "assets/images/button_unchecked.png"
    )
    button_fps_image = pygame.image.load(button_fps_path)
    button_fps_image = pygame.transform.scale_by(button_fps_image, 0.2)
    button_fps = Button(
        image=button_fps_image,
        pos=(250, 150),
        text_offset=(50, 0),
        text_input="FPS 표시",
        font=Font(Fonts.ILLUST, 16).to_pygame(),
        base_color="#ffffff",
        hovering_color="White",
    )

    surface_audio = Font(Fonts.TITLE2, 18).render("소리", (255, 255, 255))

    button_audio_prev_image = pygame.image.load("assets/images/arrow_left.png")
    button_audio_prev_image = pygame.transform.scale_by(button_audio_prev_image, 0.2)
    button_audio_prev = Button(image=button_audio_prev_image, pos=(250, 220))

    button_audio_next_image = pygame.image.load("assets/images/arrow_right.png")
    button_audio_next_image = pygame.transform.scale_by(button_audio_next_image, 0.2)
    button_audio_next = Button(image=button_audio_next_image, pos=(380, 220))

    button_cancel_image = pygame.image.load("assets/images/menu_play_rect.png")
    button_cancel_image = pygame.transform.scale(button_cancel_image, (40, 20))
    button_cancel = Button(
        image=button_cancel_image,
        pos=(350, 305),
        text_input="취소",
        font=Font(Fonts.OPTION, 20).to_pygame(),
        base_color="#ffffff",
        hovering_color="White",
    )

    button_ok_image = pygame.image.load("assets/images/menu_play_rect.png")
    button_ok_image = pygame.transform.scale(button_ok_image, (40, 20))
    button_ok = Button(
        image=button_ok_image,
        pos=(395, 305),
        text_input="확인",
        font=Font(Fonts.OPTION, 20).to_pygame(),
        base_color="#ffffff",
        hovering_color="White",
    )

    while CONFIG.is_running and not need_to_exit:
        CONFIG.clock.tick(CONFIG.FPS)

        menu_mouse_pos = CONFIG.get_mouse_pos()

        surface_resolution = Font(Fonts.ILLUST, 18).render(
            CONFIG.resolution_to_str(resolution), (255, 255, 255)
        )
        surface_audio_text = Font(Fonts.ILLUST, 18).render(
            str(round(volume, 1)), (255, 255, 255)
        )

        CONFIG.surface.blit(background, background_rect)
        CONFIG.surface.blit(
            surface_resolution, surface_resolution.get_rect(center=(315 + CONFIG.camera_x, 90 + CONFIG.camera_y))
        )
        CONFIG.surface.blit(
            surface_resolution_2, surface_resolution_2.get_rect(center=(245 + CONFIG.camera_x, 50 + CONFIG.camera_y))
        )
        CONFIG.surface.blit(surface_audio, surface_audio.get_rect(center=(244 + CONFIG.camera_x, 185 + CONFIG.camera_y)))
        CONFIG.surface.blit(
            surface_audio_text, surface_audio_text.get_rect(center=(315 + CONFIG.camera_x, 220 + CONFIG.camera_y))
        )

        for button in [
            button_resolution_prev,
            button_resolution_next,
            button_resolution_full,
            button_fps,
            button_audio_prev,
            button_audio_next,
            button_cancel,
            button_ok,
        ]:
            button.change_color(menu_mouse_pos)
            button.update(CONFIG.surface)

        CONFIG.update_screen()

        process(process_menu)

    CONFIG.surface = surface_recovered
    need_to_exit = False
