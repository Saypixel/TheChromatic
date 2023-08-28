import pygame
from typing import Optional, List
from ..config import Fonts
from .mutual_text import MutualText
from ..font import Font
from ..config import CONST, debug

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
    
    delay: int = 30
    """기본 지연 시간 (ms)"""
    
    """
    https://gist.github.com/ihoneymon/652be052a0727ad59601 : 일부 문법은 깃허브 마크다운 문법을 참조하였습니다.

    * : 굵게
    # : 크게
    / : 작게
    < : 줄바꿈 (New Line)
    """

    FONT = Fonts.TITLE2
    PT = 18

    SYNTAX: dict[str, tuple[Font, int]] = {
        "*": (Fonts.TITLE3, PT),
        "#": (Fonts.TITLE2, PT + 4),
        "/": (Fonts.DIALOG, PT - 4)
    }

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
            if prefix in self.pure:  # 텍스트에 접두어가 있는 경우
                self.has_prefix = True
                self.pure = self.pure.replace(prefix, "")  # 순수 텍스트는 접두어가 없으므로 접두어만 삭제

        is_started = False  # 접두어가 있는가?
        mutual_text_ = ""  # 각 접두어별 텍스트
        prefix = ""  # 접두어

        for ch in self.raw:
            match ch:
                case "*" | "#" | "/" | "^":  # 접두어
                    is_started = not is_started  # 접두어가 없었으면 시작, 있었으면 끝

                    if mutual_text_:  # mutual text가 비어있지 않은 경우
                        mutual = MutualText(mutual_text_, prefix, delay)  # 상호작용 텍스트 생성
                        mutual_text_ = ""
                        self.texts.append(mutual)  # texts 배열에 MutualText 추가

                    prefix = ch if is_started else ""  # 접두어 저장

                case _:  # 접두어가 아닌 순수 텍스트인 경우
                    mutual_text_ += ch

        # 접두어가 없는 일반 텍스트가 있는 경우
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
        :param index: 상호작용 텍스트의 index
        :param text_position: 화면 위치
        :param char_position: 문자 위치 (렌더링할 위치)
        :param surface: 화면
        :return: 갱신해야할 문자 위치
        """
        ch_x = char_position[0]
        ch_y = char_position[1]

        font = Text.FONT
        pt = Text.PT
        px = 0

        if mutual.prefix in Text.SYNTAX:  # 접두어별 맞는 폰트 지정
            syntax = Text.SYNTAX[mutual.prefix]
            font = syntax[0]
            pt = syntax[1]

        px = pt / 3.0 * 4.0  # pt를 픽셀로 변환
        chs = mutual.text[index]  # 문자

        if chs == "<":  # 줄바꿈 접두어
            ch_x = text_position[0]  # x 좌표를 처음 좌표로 이동
            ch_y += px  # y 좌표를 일정 이동

            # x 좌표와 y 좌표를 각각 이동시켜 마치 줄바꿈이 된 것처럼 행동
        else: 
            ch = Font(font, pt).render(chs, CONST.COL_BLACK)  # 검정색인 텍스트 생성
            surface.blit(ch, (ch_x, ch_y))  # 화면에 렌더링

            ch_x += px  # x 좌표를 일정 이동

        return (ch_x, ch_y)  # 갱신해야할 문자 위치를 반환