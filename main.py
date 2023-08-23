import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # "pygame 2.5.0 (SDL 2.28.0, Python 3.10.6)" 메시지 지움
os.environ['SDL_VIDEO_CENTERED'] = '1'  # 게임 실행 시 모니터 중심에서 실행됨

import pygame
from pygame import mixer

from screens import intro
from components.sfx_collection import SFX
from components.config import CONFIG
from components.events import update_screen_resolution

def main():
    # 초기화
    pygame.init()
    mixer.init()
    SFX.init()

    # 게임 아이콘을 불러온 후 32x32 크기로 스케일링
    icon = pygame.image.load('assets/images/icon.png')
    icon = pygame.transform.scale(icon, (32, 32))

    pygame.display.set_icon(icon)  # 게임 아이콘 설정
    pygame.display.set_caption("The Chromatic: A hero's long journey")  # 게임 제목 설정

    intro.update()  # 인트로 시작


if __name__ == "__main__":
    import argparse
    import sys

    # 인수 설정
    parser = argparse.ArgumentParser(description="The Chromatic: A hero's long journey", add_help=False)
    parser.add_argument('-h', '--help', help='도움 메시지가 출력됩니다.', action="store_true")
    parser.add_argument("-d", "--debug", help="디버깅 메시지가 출력됩니다.", action="store_true")
    parser.add_argument("-f", "--fps", help="FPS를 표시합니다.", action="store_true")
    parser.add_argument("-fs", "--fullscreen", help="전체화면으로 시작됩니다.", action="store_true")
    parser.add_argument("-fhd", "--fullhd", help="FHD (1920x1080) 해상도로 시작됩니다.", action="store_true")
    parser.add_argument("-qhd", "--quadhd", help="QHD (2560x1440) 해상도로 시작됩니다.", action="store_true")
    args = parser.parse_args()

    if args.debug:  # 디버깅 메시지 출력
        CONFIG.is_debug = True
        from icecream import ic
        from datetime import datetime

        ic.configureOutput(prefix=f"{datetime.now()}|>")  # 디버깅용 debug("테스트하면 됨")

    if args.fps:  # FPS 표시
        CONFIG.game_fps = True

    if args.fullscreen:  # 전체화면
        CONFIG.is_fullscreen = True

    if args.fullhd:  # FHD (1920x1080)
        CONFIG.window_size = (1920, 1080)
        CONFIG.window_scale = 3

        update_screen_resolution()  # 화면 해상도 업데이트
            
    elif args.quadhd:  # QHD (2560x1440)
        CONFIG.window_size = (2560, 1440)
        CONFIG.window_scale = 4

        update_screen_resolution()  # 화면 해상도 업데이트

    if hasattr(args, 'help') and args.help:  # 도움 메시지 출력
        parser.print_help(sys.stderr)  # 출력 후 종료
    else:  # 도움 메시지 출력을 하지 않은 경우 게임 실행
        main()
        pygame.quit()