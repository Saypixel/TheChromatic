from enum import Enum
from random import Random

import pygame
import pygame.constants

class CONST:
    SCREEN_SIZE = [960, 540]
    """화면 (카메라) 크기 (960x540)"""

    SURFACE_SIZE = [1920, 1080]
    """세계 크기 (1920x1080)"""

    COL_WHITE = (255, 255, 255)
    COL_BLACK = (0, 0, 0)
    COL_MAIN_BACKGROUND = (55, 222, 172)
    COL_MAIN_BACKGROUND_DARK = (108, 172, 130)
    COL_MAIN_BACKGROUND_BLUE = (96, 189, 214)

    PYGAME_EVENT_DIALOG = pygame.USEREVENT + 1


class Fonts(Enum):
    TITLE1 = "assets/fonts/title1.ttf"
    """제목 1 (둥근모꼴)"""
    TITLE2 = "assets/fonts/title2.ttf"
    """제목 2 (갈무리11)"""
    TITLE3 = "assets/fonts/title3.ttf"
    """제목 3 (갈무리11 볼드)"""
    DIALOG = "assets/fonts/dialog.ttf"
    """대화창 (도스샘물)"""
    ILLUST = "assets/fonts/illust.ttf"
    """설명창 (도스고딕)"""
    OPTION = "assets/fonts/option.ttf"
    """설정창 (갈무리14)"""


class CONFIG:
    FPS = 30

    window_size = [1440, 810]  # CONST.SCREEN_SIZE * 1.5
    window_scale = 1.5

    resolutions = [
        [480, 270],
        [960, 540],
        [1440, 810],
        [1920, 1080],
        [2560, 1440],
        [3840, 2160]
    ]
    """적용할 수 있는 해상도 배열"""

    surface = pygame.Surface(CONST.SURFACE_SIZE)
    """크기가 [960, 540]으로 고정된 화면
    월드 좌표는 [1920, 1080]에 한정됨
    surface에 렌더링하고 업스케일링 후 screen으로 화면 표시"""

    screen = pygame.display.set_mode(window_size)
    """업스케일링된 실제로 플레이어에게 보여주는 화면"""

    clock = pygame.time.Clock()

    is_fullscreen = False
    """전체화면인가?"""

    is_debug = False
    """디버깅 모드가 켜져 있는가?"""

    is_running = True
    """게임이 실행되고 있는가?"""

    game_dead = False
    """플레이어가 죽었는가?"""

    game_fps = False
    """FPS를 표시하는가? (디버깅용)"""

    player_x = 200
    player_y = 225
    player_width = 0
    player_height = 0
    """플레이어 값 (동기화됨)"""

    camera_x = 0
    camera_y = 0
    """카메라 좌표 (동기화됨)"""

    random: Random = Random(100)
    """랜덤"""

    def update_screen():
        """
        화면 업스케일링이 적용되고 카메라가 움직이는 디스플레이 업데이트 기능
        """
        cropped_screen = pygame.Surface(CONST.SCREEN_SIZE)
        cropped_screen.blit(CONFIG.surface, (0, 0), CONFIG.get_camera_bound())

        transformed_screen = pygame.transform.scale(
            cropped_screen, CONFIG.window_size
        )  # 업스케일링
        CONFIG.screen.blit(transformed_screen, (0, 0))  # 화면 표시

        pygame.display.update()  # 디스플레이 업데이트

        # 카메라 좌표 업데이트
        x_to_start = max(0, CONFIG.player_x - (CONST.SCREEN_SIZE[0] // 2))  # 카메라가 움직일 시작 범위 (X좌표)
        x_to_end = CONST.SURFACE_SIZE[0] - CONST.SCREEN_SIZE[0]  # 카메라가 최대 좌표로 이동하여 가만히 있게 될 시작 범위 (X좌표)

        CONFIG.camera_x = min(x_to_start, x_to_end)  # 카메라가 움직일 범위를 벗어나면 x_to_end에서 멈춤
        CONFIG.camera_y = 0  # Y 좌표는 고정

        #  CONFIG.camera_y = min(0, CONFIG.player_y - (CONST.SCREEN_SIZE[1] / 2)) # 음수 좌표는 구현하기 어려워짐

    def get_mouse_pos() -> tuple[int, int]:
        """
        업스케일링과 월드 좌표가 적용된 마우스 좌표 가져오기
        :return: 업스케일링과 월드 좌표가 적용된 마우스 좌표
        """
        mouse_pos = pygame.mouse.get_pos()

        # 업스케일링
        upscaled = (
            mouse_pos[0] // CONFIG.window_scale,
            mouse_pos[1] // CONFIG.window_scale
        )

        # 월드 좌표 구현에 따른 오프셋 적용
        cameraed = (
            upscaled[0] + CONFIG.camera_x,
            upscaled[1] + CONFIG.camera_y
        )
        return cameraed
    
    def get_camera_bound() -> tuple[int, int, int, int]:
        """
        현재 카메라가 위치해있는 좌표와 크기 (Rect)를 가져옵니다.
        :return: 좌표와 크기 (Rect)
        """
        return (CONFIG.camera_x, CONFIG.camera_y, CONST.SCREEN_SIZE[0], CONST.SCREEN_SIZE[1])

    def is_interactive() -> bool:
        """플레이어와 상호작용 가능한가?"""
        return not CONFIG.game_dead

    def is_movable() -> bool:
        """플레이어가 움직일 수 있는가?"""
        from components.events.text import TextEvent
        from components.events.time import TimeEvent

        return (
            CONFIG.is_interactive() and TextEvent.dialog_closed and not CONFIG.game_dead and not TimeEvent.is_rewind
        )

    def resolution_to_str(size: tuple) -> str:
        """해상도 크기를 문자열로 변환합니다. ex) (1920, 1080) => '1920x1080'"""
        return str(size[0]) + "x" + str(size[1])
    
    def reset():
        """CONFIG 클래스 변수를 초기화합니다."""
        CONFIG.game_dead = False
        CONFIG.camera_x = 0
        CONFIG.camera_y = 0

def debug(debug: str):
    """
    디버깅용 출력 함수
    """
    if CONFIG.is_debug:
        from icecream import ic

        ic(debug)
