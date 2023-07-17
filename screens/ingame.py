import pygame

from characters.player import Player
from components.config import CONFIG, CONST, debug
from components.events import process
from components.text import Text

dialog_delayed = False
'''대화창의 텍스트 출력이 지연되었는가? (REFRESH 이슈 대응)'''

dialog_paused = False
'''대화창의 텍스트 출력이 완성되었는가?'''

dialog_current: Text
'''현재 대화 텍스트'''

dialog_next: Text
'''다음 대화 텍스트'''

player = Player('assets/images/chr_base.png', (100, 100), (200, 200))  # 주인공

def update_ingame():
    global player, dialog_current, dialog_next

    def process_ingame(event: pygame.event.Event):
        """인게임 이벤트 처리용 (process() child 함수)"""
        global player, dialog_current, dialog_next, dialog_paused, dialog_delayed

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
                            if dialog_paused:  # 대화창의 텍스트 출력이 완성되었을 때
                                if dialog_current is None:  # 대화창의 텍스트가 더이상 없을 때
                                    debug('대화창 닫힘')
                                else:
                                    debug('대화창 넘김')
                                    dialog_current = dialog_next
                                    dialog_delayed = False
                                    dialog_paused = False

                            else:
                                dialog_current.jump_to_last_index()
                                dialog_delayed = True  # 텍스트 미리 모두 출력
                                dialog_paused = True

            case CONST.PYGAME_EVENT_DIALOG:  # 텍스트 애니메이션 이벤트
                if CONFIG.is_interactive():
                    if dialog_delayed or dialog_paused:  # 대화창이 지연되었거나 완성된 경우
                        dialog_current.write_until_next((320, 180), CONFIG.surface)  # 완성된 텍스트를 화면에 출력
                    else:
                        delay = dialog_current.write_until_next((320, 180), CONFIG.surface)  # 진행 중인 텍스트를 화면에 출력

                        if delay > 0:
                            dialog_delayed = True  # delay 만큼 지연
                            pygame.time.set_timer(CONST.PYGAME_EVENT_DIALOG_NEXT_INDEX, delay, 1)  # delay ms 후 다음 텍스트 진행
                        else:
                            dialog_paused = True

            case CONST.PYGAME_EVENT_DIALOG_NEXT_INDEX:
                if dialog_current.jump_to_next_index(False):  # 다음 텍스트 진행
                    dialog_delayed = False

    dialog_current = Text('*안녕!*')
    dialog_next = Text('나는 에밀리아야.')

    while CONFIG.is_running:
        CONFIG.clock.tick(CONFIG.FPS)  # 프레임 조절
        CONFIG.surface.fill(CONST.COL_WHITE)

        process(process_ingame)

        CONFIG.surface.blit(player.image, player.get_pos())
        pygame.time.set_timer(CONST.PYGAME_EVENT_DIALOG, 1, 1)  # 텍스트 테스트용
        CONFIG.update_screen()