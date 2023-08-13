import pygame.constants
from enum import Enum

class CONST:
    SCREEN_SIZE = [640, 360]

    COL_WHITE = (255, 255, 255)
    COL_BLACK = (0, 0, 0)
    COL_MAIN_BACKGROUND = (55, 222, 172)
    COL_MAIN_BACKGROUND_DARK = (108, 172, 130)
    COL_MAIN_BACKGROUND_BLUE = (96, 189, 214)

    PYGAME_EVENT_DIALOG = pygame.USEREVENT + 1
    PYGAME_EVENT_DIALOG_NEXT_INDEX = pygame.USEREVENT + 2

class Fonts(Enum):
    TITLE1 = 'assets/fonts/title1.ttf'
    '''제목 1 (둥근모꼴)'''
    TITLE2 = 'assets/fonts/title2.ttf'
    '''제목 2 (갈무리11)'''
    TITLE3 = 'assets/fonts/title3.ttf'
    '''제목 3 (갈무리11 볼드)'''
    DIALOG = 'assets/fonts/dialog.ttf'
    '''대화창 (도스샘물)'''
    ILLUST = 'assets/fonts/illust.ttf'
    '''설명창 (도스고딕)'''
    OPTION = 'assets/fonts/option.ttf'
    '''설정창 (갈무리14)'''

class CONFIG:
    FPS = 30

    # window_size = [1920, 1080]  # CONST.WINDOW_SIZE * 3
    # window_scale = 3

    window_size = [1280, 720]  # CONST.WINDOW_SIZE * 2
    window_scale = 2

    surface = pygame.Surface(CONST.SCREEN_SIZE)
    '''크기가 [640, 360]으로 고정된 화면
    surface에 렌더링하고 업스케일링 후 screen으로 화면 표시'''


    screen = pygame.display.set_mode(window_size)
    '''업스케일링된 실제로 플레이어에게 보여주는 화면'''

    clock = pygame.time.Clock()

    is_fullscreen = False

    is_running = True
    '''게임이 실행되고 있는가?'''

    game_started = True
    '''게임이 시작되어 플레이어와 상호작용이 가능한가?'''

    game_paused = False
    '''게임이 일시중지되었는가?'''

    player_x = 0
    player_y = 0
    player_width = 0
    player_height = 0
    '''플레이어 값 (동기화됨)'''

    def update_screen():
        """
        화면 업스케일링이 적용된 디스플레이 업데이트 기능
        """
        transformed_screen = pygame.transform.scale(CONFIG.surface, CONFIG.window_size)  # 업스케일링
        CONFIG.screen.blit(transformed_screen, (0, 0))  # 화면 표시

        pygame.display.update()  # 디스플레이 업데이트


    def get_mouse_pos() -> tuple[int, int]:
        """
        화면 업스케일링이 적용된 마우스 위치 가져오기
        :return: tuple[int, int]
        """
        mouse_pos = pygame.mouse.get_pos()

        if CONFIG.window_scale == 1:
            return mouse_pos

        transformed_mouse_pos = (mouse_pos[0] // CONFIG.window_scale, mouse_pos[1] // CONFIG.window_scale)
        return transformed_mouse_pos


    def is_interactive() -> bool:
        """플레이어와 상호작용 가능한가?"""
        return CONFIG.game_started and not CONFIG.game_paused
    
    
    def is_movable() -> bool:
        """플레이어가 움직일 수 있는가?"""
        from components.events.text import TextEvent
        return CONFIG.is_interactive() and TextEvent.dialog_closed

def debug(debug: str):
    """
    디버깅용 출력 함수
    """
    from icecream import ic
    ic(debug)