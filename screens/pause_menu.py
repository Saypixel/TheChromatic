import pygame

from components.button import Button
from components.config import CONFIG, debug
from components.events import process, update_screen_resolution
from components.sfx_collection import SFX

from screens.settings import update_settings

surface_recovered: pygame.Surface
"""백업된 화면 (인게임 화면에서 덮어씌우는걸 방지)"""

need_to_exit = False
"""설정창을 닫아야 하는 경우"""

def update_pause_menu():
    """ESC 화면을 표시합니다."""

    def process_menu(event: pygame.event.Event):
        """인게임 이벤트 처리용 (process() child 함수)"""

        global need_to_exit

        match event.type:
            case pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 시
                if button_play.check_for_input(mouse_pos):  # 돌아가기
                    need_to_exit = True  # ESC 화면 나가기
                    return

                if button_settings.check_for_input(mouse_pos):  # 설정
                    update_settings()  # 설정창 표시
                    return

                if button_fullscreen.check_for_input(mouse_pos):  # 전체화면
                    CONFIG.is_fullscreen = not CONFIG.is_fullscreen

                    path = (
                        "assets/images/button_window.png"
                        if CONFIG.is_fullscreen
                        else "assets/images/button_fullscreen.png"
                    )
                    image = pygame.image.load(path)

                    button_fullscreen.change_image(image)  # 이미지 변경
                    update_screen_resolution()  # 전체화면으로 화면 업데이트
                    return

                if button_unmute.check_for_input(mouse_pos):  # 음소거
                    path = (
                        "assets/images/button_unmute.png"
                        if SFX.muted
                        else "assets/images/button_mute.png"
                    )
                    image = pygame.image.load(path)
                    image = pygame.transform.scale_by(image, 0.2)  # 이미지 스케일링

                    SFX.control_mute()  # 음소거 조절
                    button_unmute.change_image(image)  # 이미지 변경

                    if not SFX.muted:
                        SFX.UNMUTED.play()  # 음소거 해제 효과음 재생

                    return

                if button_exit.check_for_input(mouse_pos):  # 나가기
                    from .ingame import Ingame

                    need_to_exit = True
                    Ingame.default.need_to_exit = True  # 인게임도 나가서 메인 메뉴로 이동
                    return

            case pygame.KEYUP:
                match event.key:
                    case pygame.K_ESCAPE:  # ESC 키를 누른 경우 ESC 화면 나가기
                        need_to_exit = True

    global need_to_exit
    surface_recovered = CONFIG.surface.copy()  # 렌더링한 화면 복사 후 백업

    # ESC 화면 배경
    background = pygame.image.load("assets/images/status3.png")
    background = pygame.transform.scale_by(background, 0.2)  # 이미지 스케일링
    background = pygame.transform.rotate(background, 90)  # 이미지를 시계방향으로 90도만큼 회전
    background_rect = background.get_rect(center=(320 + CONFIG.camera_x, 180 + CONFIG.camera_y))  # 카메라 좌표 보정

    # 버튼: 돌아가기
    button_play_image = pygame.image.load("assets/images/button_play.png")
    button_play_image = pygame.transform.scale_by(button_play_image, 0.2)  # 이미지 스케일링
    button_play = Button(image=button_play_image, pos=(290, 140))

    # 버튼: 설정
    button_settings_image = pygame.image.load("assets/images/button_settings.png")
    button_settings_image = pygame.transform.scale_by(button_settings_image, 0.2)  # 이미지 스케일링
    button_settings = Button(image=button_settings_image, pos=(350, 140))

    # 버튼: 전체화면 / 창모드
    button_fullscreen_image = pygame.image.load("assets/images/button_fullscreen.png")
    button_fullscreen = Button(image=button_fullscreen_image, pos=(260, 200))

    # 버튼: 음소거 / 음소거 해제
    button_unmute_image = pygame.image.load("assets/images/button_unmute.png")
    button_unmute_image = pygame.transform.scale_by(button_unmute_image, 0.2)  # 이미지 스케일링
    button_unmute = Button(image=button_unmute_image, pos=(320, 200))

    # 버튼: 메뉴화면으로 나가기
    button_exit_image = pygame.image.load("assets/images/button_exit.png")
    button_exit = Button(image=button_exit_image, pos=(380, 200))

    while CONFIG.is_running and not need_to_exit:
        CONFIG.clock.tick(CONFIG.FPS)

        mouse_pos = CONFIG.get_mouse_pos()  # 업스케일링 및 카메라 좌표가 보정된 마우스 좌표 가져오기

        # 전체화면 값 동기화
        path = (
            "assets/images/button_window.png"
            if CONFIG.is_fullscreen
            else "assets/images/button_fullscreen.png"
        )
        image = pygame.image.load(path)

        button_fullscreen.change_image(image)  # 맞는 값에 맞춰 이미지 변경

        # 음소거 값 동기화
        path = (
            "assets/images/button_mute.png"
            if SFX.muted
            else "assets/images/button_unmute.png"
        )
        image = pygame.image.load(path)
        image = pygame.transform.scale_by(image, 0.2)  # 이미지 스케일링

        button_unmute.change_image(image)  # 맞는 값에 맞춰 이미지 변경

        CONFIG.surface.blit(background, background_rect)  # ESC 화면 배경 렌더링

        for button in [
            button_play,
            button_settings,
            button_fullscreen,
            button_unmute,
            button_exit,
        ]:
            button.change_color(mouse_pos)  # Hovering 시 (마우스 커서가 버튼에 올려졌을 때) 색상 변경
            button.update(CONFIG.surface)  # 버튼 렌더링

        CONFIG.update_screen()  # 화면 업스케일링

        process(process_menu)  # 키보드 및 마우스 입력 이벤트 처리

    # 렌더링하는 화면 복구
    CONFIG.surface = surface_recovered
    need_to_exit = False
