import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # "pygame 2.5.0 (SDL 2.28.0, Python 3.10.6)" 메세지 지움
os.environ['SDL_VIDEO_CENTERED'] = '1'

import pygame
from pygame import mixer

from screens import intro
from components.sfx_collection import SFX
from components.config import CONFIG
from components.events import update_screen_resolution

def main():
    pygame.init()
    mixer.init()
    SFX.init()

    icon = pygame.image.load('assets/images/icon.png')
    icon = pygame.transform.scale(icon, (32, 32))

    pygame.display.set_icon(icon)
    pygame.display.set_caption("The Chromatic: A hero's long journey")
    # pygame.key.set_repeat(5, 40)  # 키 중복 허용

    intro.update()  # 인트로 시작


if __name__ == "__main__":
    help = False
    
    try:
        import argparse
        import sys

        parser = argparse.ArgumentParser(description="The Chromatic: A hero's long journey", add_help=False)
        parser.add_argument('-h', '--help', help='도움 메시지가 출력됩니다.', action="store_true")
        parser.add_argument("-d", "--debug", help="디버깅 메시지가 출력됩니다.", action="store_true")
        parser.add_argument("-f", "--fps", help="FPS를 표시합니다.", action="store_true")
        parser.add_argument("-fs", "--fullscreen", help="전체화면으로 시작됩니다.", action="store_true")
        parser.add_argument("-fhd", "--fullhd", help="FHD (1920x1080) 해상도로 시작됩니다.", action="store_true")
        parser.add_argument("-qhd", "--quadhd", help="QHD (2560x1440) 해상도로 시작됩니다.", action="store_true")
        args = parser.parse_args()

        if args.debug:
            CONFIG.is_debug = True
            from icecream import ic
            from datetime import datetime

            ic.configureOutput(prefix=f"{datetime.now()}|>")  # 디버깅용 debug("테스트하면 됨")

        if args.fps:
            CONFIG.game_fps = True

        if args.fullscreen:
            CONFIG.is_fullscreen = True

        if args.fullhd:
            CONFIG.window_size = (1920, 1080)
            CONFIG.window_scale = 3

            update_screen_resolution()
            
        elif args.quadhd:
            CONFIG.window_size = (2560, 1440)
            CONFIG.window_scale = 4

            update_screen_resolution()

        if hasattr(args, 'help') and args.help:
            help = True
            parser.print_help(sys.stderr)

    except SystemExit:
        pass

    if not help:
        main()
        pygame.quit()