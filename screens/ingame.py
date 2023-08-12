import pygame

from characters.player import Player
from components.config import CONFIG, CONST, debug
from components.events import process
from components.events.text import TextEvent
from components.text import Text
from components.text.text_collection import TextCollection

player = Player('assets/images/chr_player.png', (80, 80), (200, 200), True)  # 주인공
emilia = Player('assets/images/chr_emilia.png', (80, 80), (500, 200))  # 에밀리아

def update_ingame():
    global player, dialog

    def process_ingame(event: pygame.event.Event):
        """인게임 이벤트 처리용 (process() child 함수)"""
        global player

        match event.type:
            case pygame.KEYDOWN:
                if CONFIG.is_interactive():  # 플레이어와 상호작용 가능할 때
                    match event.key:
                        case pygame.K_a | pygame.K_LEFT:  # 왼쪽으로 이동
                            player.move(-1)
                        case pygame.K_d | pygame.K_RIGHT:  # 오른쪽으로 이동
                            player.move(1)

            case pygame.KEYUP:
                if CONFIG.is_interactive():
                    match event.key:
                        case pygame.K_SPACE:
                            if emilia.is_bound():
                                pygame.time.set_timer(CONST.PYGAME_EVENT_DIALOG, 1, 1)  # 텍스트 테스트용
                                TextEvent.process_next_event()

            case CONST.PYGAME_EVENT_DIALOG:  # 텍스트 애니메이션 이벤트
                if CONFIG.is_interactive():
                    TextEvent.process_animation_event()

            case CONST.PYGAME_EVENT_DIALOG_NEXT_INDEX:
                TextEvent.process_animation_next_event()


    TextEvent.dialog = TextCollection([Text('*안녕!*'), Text('나는 에밀리아야.')], (320, 180))

    while CONFIG.is_running:
        CONFIG.clock.tick(CONFIG.FPS)  # 프레임 조절
        CONFIG.surface.fill(CONST.COL_WHITE)

        process(process_ingame)

        CONFIG.surface.blit(player.image, player.get_pos())
        
        CONFIG.update_screen()