import pygame

from components.config import CONFIG, CONST
from components.text import Text
from components.config import debug
from components.text.text_collection import TextCollection

class TextEvent(object):
# 인게임 내에서 처리될 공통 텍스트 이벤트

    dialog_delayed = False
    '''대화창의 텍스트 출력이 지연되었는가? (REFRESH 이슈 대응)'''

    dialog_paused = False
    '''대화창의 텍스트 출력이 완성되었는가?'''

    dialog_closed = False
    '''대화창 텍스트가 닫혀있는가?'''

    dialog: TextCollection
    '''대화창 (Text 배열)'''

    @classmethod
    def process_next_event(cls):
        # 다음 대화창 이벤트 구현

        if cls.dialog_closed:
            cls.dialog_closed = False
            return

        if cls.dialog_paused:  # 대화창의 텍스트 출력이 완성되었을 때
            if cls.dialog.index == 0:  # 대화창이 처음으로 출력될 때
                debug('대화창 열림')

            if cls.dialog.jump_to_next():
                debug('대화창 넘김')

            else:  # 대화창의 텍스트가 더이상 없을 때
                cls.dialog_closed = True
                debug('대화창 닫힘')

                cls.dialog.reset_text_index()

            cls.dialog_delayed = False
            cls.dialog_paused = False

        else:
            cls.dialog.current.jump_to_last_index()
            cls.dialog_delayed = True  # 텍스트 미리 모두 출력
            cls.dialog_paused = True

    @classmethod
    def process_animation_event(cls):
        # 애니메이션 이벤트 구현
        if cls.dialog_delayed or cls.dialog_paused:  # 대화창이 지연되었거나 완성된 경우
            cls.dialog.current.write_until_next(cls.dialog.position, CONFIG.surface)  # 완성된 텍스트를 화면에 출력
        else:
            delay = cls.dialog.current.write_until_next(cls.dialog.position, CONFIG.surface)  # 진행 중인 텍스트를 화면에 출력

            if delay > 0:
                cls.dialog_delayed = True  # delay 만큼 지연
                pygame.time.set_timer(CONST.PYGAME_EVENT_DIALOG_NEXT_INDEX, delay, 1)  # delay ms 후 다음 텍스트 진행
            else:
                cls.dialog_paused = True

    @classmethod
    def process_animation_next_event(cls):
        # 애니메이션 다음 글자 이벤트 구현
        if cls.dialog.current.jump_to_next_index(False):  # 다음 텍스트 진행
                    cls.dialog_delayed = False