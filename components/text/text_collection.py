from typing import Optional
from components.text import Text
from components.config import debug


class TextCollection:
    textList: list[Text]
    """Text 배열"""

    index = 0
    """Text 배열의 index"""

    current: Text = None
    """현재 Text"""

    next: Text = None
    """다음 Text"""

    position = (0, 0)
    """텍스트가 표시될 절대좌표"""

    def __init__(
        self,
        texts: list[Text],
        sign_width: int,
        pos: Optional[tuple[int, int]] = (320, 180),
    ):
        """
        Text 배열을 TextCollection로 초기화합니다.
        :param texts: Text 배열
        :param sign_width: 말풍선 너비 (줄바꿈할 때 쓰임)
        :param pos: 텍스트를 표시할 절대좌표
        """
        self.textList = []
        self.position = pos

        pt = Text.PT  # 폰트 단위
        text_width = 0.0  # 현재 텍스트 너비
        modified_text = ""  # 줄바꿈이 들어간 텍스트

        for text in texts:  # Text
            for mutual in text.texts:  # Mutual Text
                if mutual.prefix in Text.SYNTAX:  # 접두어별 맞는 폰트 지정
                    syntax = Text.SYNTAX[mutual.prefix]
                    pt = syntax[1]

                px = pt / 3.0 * 4.0  # pt를 픽셀로 변환

                for ch in mutual.text:  # Mutual Text의 문자
                    text_width += px

                    if text_width > sign_width:  # 말풍선 너비보다 텍스트 너비가 더 큰 경우 (범위를 벗어난 경우)
                        modified_text += "<"  # 텍스트에 줄바꿈 추가
                        text_width = 0  # 줄바꿈 했으니 텍스트 너비 초기화

                        if ch != " ":  # 공백이 아닌 경우
                            modified_text += ch  # 텍스트에 문자 추가
                            text_width += px
                    else:
                        modified_text += ch  # 텍스트에 문자 추가

                mutual.text = modified_text  # 기존 텍스트를 줄바꿈이 들어간 텍스트로 변경
                modified_text = ""  # 줄바꿈이 들어간 텍스트 초기화

            text_width = 0  # 텍스트 너비 초기화 (새로운 Text 등장)
            self.textList.append(text)  # TextCollection에 Text 추가

        if len(self.textList) >= 1:  # 텍스트 배열 크기가 1 이상인 경우
            self.current = self.textList[0]  # 현재 텍스트 지정
        if len(self.textList) >= 2:  # 텍스트 배열 크기가 2 이상인 경우
            self.next = self.textList[1]  # 다음 텍스트 지정

    def jump_to_next(self) -> bool:
        """
        다음 대화로 이동 (텍스트를 넘김)
        """

        if len(self.textList) <= self.index + 1:  # 모든 텍스트를 다 본 경우
            self.index = 0  # index 초기화

            # 현재 출력할 텍스트와 다음 출력할 텍스트 지정
            if len(self.textList) >= 1:
                self.current = self.textList[0]
            if len(self.textList) >= 2:
                self.next = self.textList[1]

            return False  # 다음 대화로 이동할 수 없으므로 False 반환

        self.index += 1

        # 다음 출력할 텍스트를 현재 출력할 텍스트로 지정
        # 다음 출력할 텍스트 지정
        self.current = self.next
        self.next = (
            self.textList[self.index + 1]
            if self.index + 2 <= len(self.textList)
            else None
        )

        return True  # 다음 대화로 이동할 수 있으므로 True 반환

    def set_position(self, pos: tuple):
        """텍스트가 표시될 좌표 설정"""
        self.position = pos