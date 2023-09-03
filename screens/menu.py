import pygame
from pygame import mixer

from components.button import Button
from components.config import CONFIG, CONST, Fonts, debug
from components.events import process
from components.font import Font
from components.sfx_collection import SFX

from screens.ingame import Ingame
from screens.settings import update_settings

reload = False
"""재시작을 해야하는 경우"""

music_playing = True
"""음악이 재생 중인지의 여부"""

def update_menu():
    """메인 메뉴 화면을 표시합니다."""

    def process_menu(event: pygame.event.Event):
        """인게임 이벤트 처리용 (process() child 함수)"""

        global reload, music_playing
        nonlocal need_to_exit

        ctrl = pygame.key.get_mods() & pygame.K_LCTRL  # ctrl 키 누르는 여부

        match event.type:
            case pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 시
                if button_play.check_for_input(mouse_pos):  # 시작
                    music_playing = False  
                    mixer.music.stop()  # 음악 정지

                    # 인게임 기본 변수 초기화 후 인게임으로 화면 업데이트
                    Ingame.default = Ingame()
                    Ingame.default.update_ingame()
                    return

                if button_settings.check_for_input(mouse_pos):  # 설정
                    update_settings()  # 설정창 표시
                    return

                if button_exit.check_for_input(mouse_pos):  # 종료
                    CONFIG.is_running = False
                    return

            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:  # 종료 (ESC 키)
                        CONFIG.is_running = False

                    case pygame.K_r:  # 재시작
                        if ctrl:  # Ctrl 키가 눌러진 경우
                            reload = True
                            need_to_exit = True

    def play_music():
        """음악을 재생합니다."""
        mixer.music.load("assets/audio/bg_daily.ogg")
        mixer.music.set_volume(SFX.volume)
        mixer.music.play(-1)

    global music_playing
    
    need_to_exit = False  # 메인 메뉴를 나가야 하는지 여부

    background = pygame.image.load("assets/images/background_menu.png")  # 배경 불러오기
    background = pygame.transform.scale(background, CONST.SCREEN_SIZE)  # 화면 크기만큼 이미지 스케일링

    # 제목
    title = pygame.image.load("assets/images/menu_title.png")
    title = pygame.transform.scale_by(title, 0.6)  # 이미지 스케일링

    # 버튼: 시작
    button_play_image = pygame.image.load("assets/images/menu_play_rect.png")
    button_play_image = pygame.transform.scale(button_play_image, (300, 80))  # 이미지 스케일링
    button_play = Button(
        image=button_play_image,
        pos=(478, 380),
        text_input="시작",
        font=Font(Fonts.TITLE2, 60).to_pygame(),
        base_color="#ffffff",
        hovering_color="White",
    )

    # 버튼: 설정
    button_settings_image = pygame.image.load(
        "assets/images/button_settings.png"
    )
    button_settings_image = pygame.transform.scale_by(button_settings_image, 0.4)  # 이미지 스케일링
    button_settings = Button(image=button_settings_image, pos=(588, 480))

    # 버튼: 종료
    button_exit_image = pygame.image.load("assets/images/menu_play_rect.png")
    button_exit_image = pygame.transform.scale(button_exit_image, (200, 80))  # 이미지 스케일링
    button_exit = Button(
        image=button_exit_image,
        pos=(428, 480),
        text_input="종료",
        font=Font(Fonts.TITLE2, 50).to_pygame(),
        base_color="#ffffff",
        hovering_color="White",
    )

    play_music()  # 음악 재생

    while CONFIG.is_running and not need_to_exit:
        CONFIG.clock.tick(CONFIG.FPS)

        mouse_pos = CONFIG.get_mouse_pos()  # 업스케일링 및 카메라 좌표가 보정된 마우스 좌표 가져오기
        
        if not music_playing:  # 음악이 재생되고 있지 않은 경우 (메인 메뉴로 나가서 메인 메뉴로 돌아온 경우)
            music_playing = True
            play_music()  # 음악 재생

        CONFIG.surface.blit(background, (0, 0))  # 배경 렌더링
        CONFIG.surface.blit(title, title.get_rect(center=(480, 140)))  # 제목 렌더링

        for button in [button_play, button_settings, button_exit]:
            button.change_color(mouse_pos)  # Hovering 시 (마우스 커서가 버튼에 올려졌을 때) 색상 변경
            button.update(CONFIG.surface)  # 버튼 렌더링

        CONFIG.update_screen()  # 화면 업스케일링

        process(process_menu)  # 키보드 및 마우스 입력 이벤트 처리
