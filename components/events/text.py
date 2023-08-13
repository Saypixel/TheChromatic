import pygame
from threading import Timer

from components.config import CONFIG, CONST, debug
from components.text import Text
from components.text.text_collection import TextCollection
from components.text.mutual_text import MutualText

class TextEvent(object):
# 인게임 내에서 처리될 공통 텍스트 이벤트

    dialog_delayed = False
    '''대화창의 텍스트 출력이 지연되었는가? (REFRESH 이슈 대응)'''

    dialog_paused = True
    '''대화창의 텍스트 출력이 완성되었는가?'''

    dialog_closed = True
    '''대화창 텍스트가 닫혀있는가?'''

    dialog: TextCollection
    '''대화창 (Text 배열)'''

    @classmethod
    def process_next_event(cls):
        # 다음 대화창 이벤트 구현

        if cls.dialog_paused:  # 대화창의 텍스트 출력이 완성되었을 때
            if cls.dialog.index == 0 and cls.dialog_closed:  # 대화창이 처음으로 출력될 때
                cls.dialog_closed = False  # 대화창 열림
                cls.dialog_paused = False

            else:
                if cls.dialog.jump_to_next():  # 대화창을 넘길 때
                    cls.dialog_paused = False

                else:  # 대화창의 텍스트가 더이상 없을 때
                    cls.dialog_closed = True  # 대화창 닫힘

                    cls.dialog.reset_text_index()
                    cls.dialog_paused = True
                cls.dialog_delayed = False
            

        else:
            cls.dialog.current.jump_to_last_index()
            cls.dialog_delayed = True  # 텍스트 미리 모두 출력
            cls.dialog_paused = True

    # @classmethod
    # def process_animation_event(cls, surface: pygame.Surface = None):
    #     # 애니메이션 이벤트 구현
    #     if surface is None:
    #          surface = CONFIG.surface
        
    #     if cls.dialog_delayed or cls.dialog_paused:  # 대화창이 지연되었거나 완성된 경우
    #         cls.dialog.current.write_until_next(cls.dialog.position, surface)  # 완성된 텍스트를 화면에 출력
    #     else:
    #         delay = cls.dialog.current.write_until_next(cls.dialog.position, surface)  # 진행 중인 텍스트를 화면에 출력

    #         if delay > 0:
    #             cls.dialog_delayed = True  # delay 만큼 지연
    #             pygame.time.set_timer(CONST.PYGAME_EVENT_DIALOG_NEXT_INDEX, delay, 1)  # delay ms 후 다음 텍스트 진행
    #         else:
    #             cls.dialog_paused = True

    @classmethod
    def process_animation_event(cls, surface: pygame.Surface = None):
        # 한번에 애니메이션 이벤트 구현 (V2)
        i = 0
        j = 0
        ch_x = cls.dialog.position[0]
        ch_y = cls.dialog.position[1]

        def write_each():
            nonlocal i, j, ch_x, ch_y

            if i + 1 > len(cls.dialog.current.texts):
                cls.dialog_paused = True
                return

            mutual = cls.dialog.current.texts[i]
            new_ch_pos = cls.dialog.current.write(mutual, j, cls.dialog.position, (ch_x, ch_y), surface)
            ch_x = new_ch_pos[0]
            ch_y = new_ch_pos[1]

            j += 1

            if j + 1 > len(mutual.text):
                i += 1
                j = 0

            if mutual.delay > 0:
                Timer(mutual.delay / 1000.0, write_each).start()

        if surface is None:
            surface = CONFIG.surface

        if not cls.dialog_paused:
            write_each()

    @classmethod
    def process_animation_next_event(cls):
        # 애니메이션 다음 글자 이벤트 구현
        if cls.dialog.current.jump_to_next_index(False):  # 다음 텍스트 진행
                    cls.dialog_delayed = False