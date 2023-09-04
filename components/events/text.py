import pygame
from threading import Timer

from components.config import CONFIG

from components.text.text_collection import TextCollection

from characters.player import Player

class TextEvent(object):
    """인게임 내에서 처리될 공통 텍스트 이벤트"""

    dialog_delayed = True
    """대화창의 텍스트 출력이 지연되어야 하는가? (REFRESH 이슈 & 텍스트 미리 출력 대응)"""

    dialog_paused = True
    """대화창의 텍스트 출력이 완성되었는가?"""

    dialog_closed = True
    """대화창 텍스트가 닫혀있는가?"""

    dialog: TextCollection = None
    """대화창 (Text 배열)"""

    NPC: Player = None
    """대화하는 NPC"""

    @classmethod
    def process_next_event(cls):
        # 다음 대화창 이벤트 구현

        if cls.dialog_paused:  # 대화창의 텍스트 출력이 완성되었을 때
            if cls.dialog.index == 0 and cls.dialog_closed:  # 대화창이 처음으로 출력될 때
                cls.dialog_closed = False  # 대화창 열림
                cls.dialog_paused = False  # 텍스트 출력 미완성

            else:
                if cls.dialog.jump_to_next():  # 대화창을 넘길 때
                    cls.dialog_paused = False  # 텍스트 출력 미완성

                else:  # 대화창의 텍스트가 더이상 없을 때
                    cls.dialog = None  # 대화창 초기화
                    cls.dialog_closed = True  # 대화창 닫힘
                    cls.dialog_paused = True  # 텍스트 출력 완성
                    
                cls.dialog_delayed = True  # 텍스트 출력 지연

        else:
            cls.dialog_delayed = False  # 텍스트 미리 모두 출력
            cls.dialog_paused = True  # 텍스트 출력 완성

    @classmethod
    def process_animation_event(cls, surface: pygame.Surface = None):
        """
        한번에 애니메이션 이벤트 구현 (V2)
        :param surface: 렌더링할 화면 (기본: CONFIG.surface)
        """
        
        mutual_index = 0  # MutualText 클래스 index
        mutual_text_index = 0  # MutualText 클래스의 텍스트 index
        ch_x = cls.dialog.position[0]  # 대화창 시작 X좌표
        ch_y = cls.dialog.position[1]  # 대화창 시작 Y좌표

        def write_each():
            """각 문자 렌더링 (출력)"""
            nonlocal mutual_index, mutual_text_index, ch_x, ch_y

            if cls.dialog is None:  # 대화를 너무 빨리 넘긴 경우
                return  # 출력할 대화가 없으므로 종료

            if mutual_index + 1 > len(cls.dialog.current.texts):  # MutualText 배열의 범위를 벗어난 경우
                cls.dialog_paused = True  # 텍스트 출력 완성
                cls.dialog_delayed = True  # 텍스트 지연

                return  # 함수를 재귀할 때 무한 루프를 돌면 안되므로 반환

            mutual = cls.dialog.current.texts[mutual_index]  # MutualText 클래스 가져오기
            new_ch_pos = cls.dialog.current.write(
                mutual, mutual_text_index, cls.dialog.position, (ch_x, ch_y), surface
            )  # 텍스트 렌더링 후 좌표 갱신

            if new_ch_pos is None:  # 대화를 너무 빨리 넘긴 경우
                return  # 출력할 대화가 없으므로 종료

            ch_x = new_ch_pos[0]
            ch_y = new_ch_pos[1]

            mutual_text_index += 1

            if mutual_text_index + 1 > len(mutual.text):  # MutualText 클래스의 문자열 범위를 벗어난 경우
                mutual_index += 1  # 새로운 MutualText 클래스 가져오기 위해 index를 1씩 추가
                mutual_text_index = 0  # 새로운 MutualText 클래스를 가져오므로 index 초기화

            if mutual.delay > 0 and cls.dialog_delayed:  # 지연 시간이 있는 경우
                delay_per_second = mutual.delay / 1000.0  # 이 때 threading.Timer 클래스의 시간 변수는 단위가 초이므로 단위를 ms에서 초로 변환
                Timer(delay_per_second, write_each).start()  # threading.Timer 클래스로 특정 시간 후 비동기적으로 함수 재귀
            else:
                write_each()  # 특정 시간 없이 함수 재귀

        if surface is None: # 사용자 지정한 화면이 없다면
            surface = CONFIG.surface # 렌더링할 화면을 기본 지정한 화면으로 지정

        if not cls.dialog_paused:  # 텍스트 출력이 미완성인 경우
            write_each()  # 텍스트를 처음부터 출력

    @classmethod
    def reset(cls):
        """TextEvent 클래스의 변수를 초기화합니다."""
        TextEvent.dialog_closed = True
        TextEvent.dialog_delayed = True
        TextEvent.dialog_paused = True
        TextEvent.NPC = None
        TextEvent.dialog = None
        