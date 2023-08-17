import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # "pygame 2.5.0 (SDL 2.28.0, Python 3.10.6)" 메세지 지움
import pygame
from screens import intro
from pygame import mixer
from components.sfx_collection import SFX
from components.config import CONFIG


def main():
    pygame.init()
    mixer.init()
    SFX.init()

    pygame.display.set_caption('The Chromatic: A hero\'s long journey')
    #pygame.key.set_repeat(5, 40)  # 키 중복 허용

    intro.update() # 인트로 시작

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='The Chromatic: A hero\'s long journey')
    parser.add_argument('-d', '--debug', help='디버깅 메세지가 출력됩니다.',  action='store_true')
    args = parser.parse_args()
        
    if args.debug:
        CONFIG.is_debug = True
        from icecream import ic
        from datetime import datetime
        ic.configureOutput(prefix=f'{datetime.now()}|>') # 디버깅용 debug("테스트하면 됨")
    
    main()
    pygame.quit()
