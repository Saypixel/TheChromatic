import pygame
from ..config import CONFIG

def update_screen_resolution():
    """
    화면 해상도 업데이트
    """
    if CONFIG.is_fullscreen:
        CONFIG.screen = pygame.display.set_mode(CONFIG.window_size, pygame.FULLSCREEN)
    else:
        CONFIG.screen = pygame.display.set_mode(CONFIG.window_size)


def process(f=None):
    """
    공통 이벤트 확인 및 처리
    :param f: 이벤트를 처리할 함수
    """

    for event in pygame.event.get():  # 이벤트 확인
        match event.type:
            case pygame.QUIT:  # 게임 종료 이벤트 발생 시
                CONFIG.is_running = False

            case pygame.KEYDOWN: # 키를 눌렸을 때
                match event.key:
                    case pygame.KMOD_ALT | pygame.K_F4:  # ALT + F4
                        CONFIG.s_running = False

                    case pygame.K_ESCAPE: # ESC
                        CONFIG.is_running = False # TODO: 종료 화면 띄우기
                        
                    case _:
                        if f is not None:
                            f(event)

            case pygame.KEYUP:
                match event.key:
                    case pygame.K_F11:  # 전체화면 이벤트 처리
                        CONFIG.is_fullscreen = not CONFIG.is_fullscreen
                        update_screen_resolution()

                    case _:
                        if f is not None:
                            f(event)

            case _:
                if f is not None:
                    f(event)
