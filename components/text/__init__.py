import pygame
from typing import Optional, List
from ..config import Fonts
from .mutual_text import MutualText
from ..font import Font
from ..config import debug

__all__ = ["Text", "MutualText", "TextCollection"]


class Text:
    raw: str = ""
    """날 것의 텍스트. 접두어 포함"""

    pure: str = ""
    """순수 텍스트. 접두어 미포함"""

    has_prefix: bool = False
    """접두어가 포함되어있는가?"""

    texts: List[MutualText]
    """텍스트 리스트 (상호작용 배열)"""

    index: int = 0
    """텍스트 리스트 index (상호작용 배열)"""

    delay: int = 30
    """기본 지연 시간 (ms)"""

    position: tuple[int, int] = (0, 0)
    """텍스트 절대좌표값 (TextCollection에서 상속)"""

    """
    https://gist.github.com/ihoneymon/652be052a0727ad59601 : 일부 문법은 깃허브 마크다운 문법을 참조하였습니다.

    * : 굵게
    # : 크게
    / : 작게
    ^ : 흔들리게 (미지원)
    < : New Line
    """

    def __init__(self, text: str, delay: Optional[int] = 30):
        """
        Text 클래스를 생성합니다.
        :param text: 텍스트
        """
        self.texts = []

        self.raw = text
        self.pure = text  # 일단 저장. 어차피 replace() 함수를 통해 접두어를 제거하기 때문.
        self.delay = delay

        for prefix in ["*", "#", "/", "^"]:
            if prefix in self.pure:
                self.has_prefix = True
                self.pure = self.pure.replace(prefix, "")

        is_started = False
        mutual_text_ = ""
        prefix = ""

        for ch in self.raw:
            match ch:
                case "*" | "#" | "/" | "^":
                    is_started = not is_started

                    if mutual_text_:  # mutual text가 비어있지 않은 경우
                        mutual = MutualText(mutual_text_, prefix, delay)
                        mutual_text_ = ""
                        self.texts.append(mutual)

                    prefix = ch if is_started else ""

                case _:
                    mutual_text_ += ch

        if mutual_text_:  # mutual text가 비어있지 않은 경우
            mutual = MutualText(mutual_text_, "", delay)
            self.texts.append(mutual)

    def write(
        self,
        mutual: MutualText,
        index: int,
        text_position: tuple[int, int],
        char_position: tuple[int, int],
        surface: pygame.Surface,
    ) -> tuple[int, int]:
        """
        특정 문자를 렌더링 (출력)합니다.
        :param mutual: 상호작용 테스트
        :param index: 상호작용 테스트의 index
        :param text_position: 화면 위치
        :param char_position: 문자 위치 (렌더링할 위치)
        :param surface: 화면
        :return: 갱신해야할 문자 위치
        """
        ch_x = char_position[0]
        ch_y = char_position[1]

        font = Fonts.DIALOG
        pt = 15
        px = 0

        match mutual.prefix:
            case "*":
                font = Fonts.TITLE3
            case "#":
                font = Fonts.TITLE2
                pt += 2
            case "/":
                font = Fonts.TITLE2
                pt -= 3

        px = pt / 3.0 * 4.0
        chs = mutual.text[index]

        if chs == "<":
            ch_x = text_position[0]
            ch_y += px
        else:
            ch = Font(font, pt).render(chs, (0, 0, 0))
            surface.blit(ch, (ch_x, ch_y))

            ch_x += px

        return (ch_x, ch_y)

    def write_until_next(
        self, position: tuple[int, int], surface: pygame.Surface
    ) -> int:
        """
        진행 중인 텍스트를 렌더링 (출력)합니다.
        :param position: 화면 위치
        :param surface: 화면
        :return: 텍스트 애니메이션 지연 시간
        """
        ch_x = position[0]
        ch_y = position[1]
        mutual = MutualText("", "", 0)

        for i in range(0, self.index + 1):
            mutual = self.texts[i]

            for j in range(0, mutual.index + 1):
                new_ch_pos = self.write(mutual, j, position, (ch_x, ch_y), surface)
                ch_x = new_ch_pos[0]
                ch_y = new_ch_pos[1]

        last_mutual = self.texts[len(self.texts) - 1]

        # 애니메이션이 완료된 텍스트가 렌더링이 다 된 경우
        if (
            self.index == len(self.texts) - 1
            and last_mutual.index == len(last_mutual.text) - 1
        ):
            return -1

        return mutual.delay

    def jump_to_next_index(self, reset=True) -> bool:
        mutual = self.texts[self.index]

        mutual.index += 1

        if mutual.index == len(mutual.text):
            mutual.index = 0
            self.index += 1

        if self.index == len(self.texts):
            if reset:
                self.index = 0
            else:
                self.index = len(self.texts) - 1
                mutual.index = len(mutual.text) - 1

            return False

        return True

    def jump_to_first_index(self):
        self.index = 0

        for mutual in self.texts:
            mutual.index = 0

    def jump_to_last_index(self):
        self.index = len(self.texts) - 1

        for mutual in self.texts:
            mutual.index = len(mutual.text) - 1

    def print_index(self):
        """(디버깅용) index 출력"""
        debug("(" + str(self.index) + ", " + str(self.texts[self.index].index) + ")")
