import pygame

from components.button import Button
from components.config import CONFIG, CONST, Fonts, debug
from components.events import process, update_screen_resolution
from components.font import Font
from components.sfx_collection import SFX

surface_recovered: pygame.Surface
"""백업된 화면 (인게임 화면에서 덮어씌우는걸 방지)"""

need_to_exit = False
"""설정창을 닫아야 하는 경우"""

def update_settings():
    """설정창을 화면에 표시합니다."""

    def apply():
        """설정을 게임에 적용합니다. (확인 버튼 누를 시 적용됨)"""

        # 화면
        CONFIG.window_size = resolution
        CONFIG.window_scale = resolution[0] / CONST.SCREEN_SIZE[0]
        CONFIG.is_fullscreen = is_fullscreen
        CONFIG.game_fps = fps

        update_screen_resolution()  # 화면 해상도 업데이트

        # 소리
        SFX.set_volume(volume)

    def process_menu(event: pygame.event.Event):
        """인게임 이벤트 처리용 (process() child 함수)"""

        global need_to_exit
        nonlocal resolution, resolutions_index, is_fullscreen, fps, volume

        match event.type:
            case pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 시
                if button_resolution_prev.check_for_input(mouse_pos):  # 화면/이전
                    if resolutions_index > 0:
                        resolutions_index -= 1
                        resolution = CONFIG.resolutions[resolutions_index]

                if button_resolution_next.check_for_input(mouse_pos):  # 화면/다음
                    if resolutions_index < len(CONFIG.resolutions) - 1:
                        resolutions_index += 1
                        resolution = CONFIG.resolutions[resolutions_index]

                if button_resolution_full.check_for_input(mouse_pos):  # 전체화면
                    is_fullscreen = not is_fullscreen

                    path = (
                        "assets/images/button_checked.png"
                        if is_fullscreen
                        else "assets/images/button_unchecked.png"
                    )
                    image = pygame.image.load(path)
                    image = pygame.transform.scale_by(image, 0.4)  # 이미지 스케일링

                    button_resolution_full.change_image(image)  # 이미지 변경

                if button_fps.check_for_input(mouse_pos):  # FPS 표시
                    fps = not fps

                    path = (
                        "assets/images/button_checked.png"
                        if fps
                        else "assets/images/button_unchecked.png"
                    )
                    image = pygame.image.load(path)
                    image = pygame.transform.scale_by(image, 0.4)  # 이미지 스케일링

                    button_fps.change_image(image)  # 이미지 변경

                if button_audio_prev.check_for_input(mouse_pos):  # 소리/이전
                    if round(volume, 1) > 0.0:  # 소수점 계산 문제 방지
                        volume -= 0.1

                if button_audio_next.check_for_input(mouse_pos):  # 소리/다음
                    if round(volume, 1) < 1.0:  # 소수점 계산 문제 방지
                        volume += 0.1

                if button_cancel.check_for_input(mouse_pos):  # 취소
                    need_to_exit = True
                    return

                if button_ok.check_for_input(mouse_pos):  # 확인
                    apply()  # 설정을 게임에 적용
                    need_to_exit = True
                    return

            case pygame.KEYUP:
                match event.key:
                    case pygame.K_ESCAPE:  # ESC 키는 취소와 같은 역할
                        need_to_exit = True

                    case pygame.K_RETURN:  # Enter 키는 확인 (적용)과 같은 역할
                        apply()
                        need_to_exit = True

    global need_to_exit
    surface_recovered = CONFIG.surface.copy()  # 렌더링한 화면 복사 후 백업

    resolution = CONFIG.window_size  # 현재 해상도
    is_fullscreen = CONFIG.is_fullscreen  # 현재 전체화면 여부
    fps = CONFIG.game_fps  # 현재 FPS 표시 여부

    volume = SFX.volume  # 현재 음량
    resolutions_index = CONFIG.resolutions.index(CONFIG.window_size)  # 현재 해상도를 resolutions 중에서 찾고 index 반환

    # 설정창 배경
    background = pygame.image.load("assets/images/status3.png")
    background = pygame.transform.scale_by(background, 0.45)
    background = pygame.transform.scale(background, (background.get_width(), 500))  # 설정 UI에 맞게 스케일링
    background_rect = background.get_rect(center=(480 + CONFIG.camera_x, 270 + CONFIG.camera_y))  # 카메라 좌표 보정

    # 텍스트: 화면
    surface_resolution_2 = Font(Fonts.TITLE2, 36).render("화면", CONST.COL_WHITE)

    # 화면 / 해상도: 이전
    button_resolution_prev_image = pygame.image.load("assets/images/arrow_left.png")
    button_resolution_prev_image = pygame.transform.scale_by(
        button_resolution_prev_image, 0.3
    )
    button_resolution_prev = Button(image=button_resolution_prev_image, pos=(340, 110))

    # 화면 / 해상도: 다음
    button_resolution_next_image = pygame.image.load("assets/images/arrow_right.png")
    button_resolution_next_image = pygame.transform.scale_by(
        button_resolution_next_image, 0.3
    )
    button_resolution_next = Button(image=button_resolution_next_image, pos=(616, 110))

    # 화면 / 전체화면
    button_resolution_full_path = (
        "assets/images/button_checked.png"
        if is_fullscreen
        else "assets/images/button_unchecked.png"
    )
    button_resolution_full_image = pygame.image.load(button_resolution_full_path)
    button_resolution_full_image = pygame.transform.scale_by(
        button_resolution_full_image, 0.4
    )
    button_resolution_full = Button(
        image=button_resolution_full_image,
        pos=(350, 170),
        text_offset=(100, 0),
        text_input="전체화면",
        font=Font(Fonts.ILLUST, 32).to_pygame(),
        base_color="#ffffff",
        hovering_color="White",
    )

    # 화면 / FPS 표시
    button_fps_path = (
        "assets/images/button_checked.png"
        if fps
        else "assets/images/button_unchecked.png"
    )
    button_fps_image = pygame.image.load(button_fps_path)
    button_fps_image = pygame.transform.scale_by(button_fps_image, 0.4)
    button_fps = Button(
        image=button_fps_image,
        pos=(350, 225),
        text_offset=(100, 0),
        text_input="FPS 표시",
        font=Font(Fonts.ILLUST, 32).to_pygame(),
        base_color="#ffffff",
        hovering_color="White",
    )

    # 텍스트: 소리
    surface_audio = Font(Fonts.TITLE2, 36).render("소리", CONST.COL_WHITE)

    # 소리 / 음량: 이전
    button_audio_prev_image = pygame.image.load("assets/images/arrow_left.png")
    button_audio_prev_image = pygame.transform.scale_by(button_audio_prev_image, 0.3)
    button_audio_prev = Button(image=button_audio_prev_image, pos=(340, 340))

    # 소리 / 음량: 다음
    button_audio_next_image = pygame.image.load("assets/images/arrow_right.png")
    button_audio_next_image = pygame.transform.scale_by(button_audio_next_image, 0.3)
    button_audio_next = Button(image=button_audio_next_image, pos=(616, 340))

    # 버튼: 취소
    button_cancel_image = pygame.image.load("assets/images/menu_play_rect.png")
    button_cancel_image = pygame.transform.scale(button_cancel_image, (100, 50))
    button_cancel = Button(
        image=button_cancel_image,
        pos=(485, 460),
        text_input="취소",
        font=Font(Fonts.OPTION, 50).to_pygame(),
        base_color="#ffffff",
        hovering_color="White",
    )

    # 버튼: 확인
    button_ok_image = pygame.image.load("assets/images/menu_play_rect.png")
    button_ok_image = pygame.transform.scale(button_ok_image, (100, 50))
    button_ok = Button(
        image=button_ok_image,
        pos=(600, 460),
        text_input="확인",
        font=Font(Fonts.OPTION, 50).to_pygame(),
        base_color="#ffffff",
        hovering_color="White",
    )

    while CONFIG.is_running and not need_to_exit:
        CONFIG.clock.tick(CONFIG.FPS)

        mouse_pos = CONFIG.get_mouse_pos()  # 업스케일링 및 카메라 좌표가 보정된 마우스 커서 좌표 가져오기

        surface_resolution = Font(Fonts.ILLUST, 36).render(  # 해상도 텍스트 폰트 렌더링
            CONFIG.resolution_to_str(resolution), CONST.COL_WHITE
        )
        surface_audio_text = Font(Fonts.ILLUST, 36).render(  # 음량 텍스트 폰트 렌더링 (백분율로 표시)
            str(int(round(volume, 1) * 100)) + "%", CONST.COL_WHITE
        )

        # 렌더링 (카메라 좌표 보정)
        CONFIG.surface.blit(background, background_rect)
        CONFIG.surface.blit(
            surface_resolution, surface_resolution.get_rect(center=(480 + CONFIG.camera_x, 110 + CONFIG.camera_y))
        )
        CONFIG.surface.blit(
            surface_resolution_2, surface_resolution_2.get_rect(center=(340 + CONFIG.camera_x, 60 + CONFIG.camera_y))
        )
        CONFIG.surface.blit(surface_audio, surface_audio.get_rect(center=(340 + CONFIG.camera_x, 290 + CONFIG.camera_y)))
        CONFIG.surface.blit(
            surface_audio_text, surface_audio_text.get_rect(center=(480 + CONFIG.camera_x, 340 + CONFIG.camera_y))
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
            button.change_color(mouse_pos)  # Hovering 시 (마우스 커서가 버튼에 올려졌을 때) 색상 변경
            button.update(CONFIG.surface)  # 버튼 렌더링

        CONFIG.update_screen()  # 화면 업스케일링

        process(process_menu)  # 키보드 키 및 마우스 입력 이벤트 처리

    # 렌더링하는 화면 복구
    CONFIG.surface = surface_recovered
    need_to_exit = False
