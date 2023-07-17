import pygame
from screens import intro
from icecream import ic
from pygame import mixer
from components.sfx_collection import SFX

from datetime import datetime
ic.configureOutput(prefix=f'{datetime.now()}|>') # 디버깅용 debug("테스트하면 됨")

def main():
    pygame.init()
    mixer.init()
    SFX.init()

    pygame.display.set_caption('The Chromatic')
    pygame.key.set_repeat(5, 40)  # 키 중복 허용

    intro.update() # 인트로 시작

if __name__ == '__main__':
    main()
    pygame.quit()
