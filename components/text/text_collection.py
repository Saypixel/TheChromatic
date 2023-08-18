from typing import Optional
from components.text import Text
from components.config import debug


class TextCollection:
    textList: list[Text]

    index = 0
    current: Text = None
    next: Text = None

    position = (0, 0)
    """절대좌표값"""

    def __init__(
        self,
        texts: list[Text],
        sign_width: int,
        pos: Optional[tuple[int, int]] = (320, 180),
    ):
        self.textList = []
        self.position = pos

        pt = 15
        text_width = 0.0
        modified_text = ""

        for text in texts:
            for mutual in text.texts:
                match mutual.prefix:
                    case "#":
                        pt += 2
                    case "/":
                        pt -= 3

                for i in range(0, len(mutual.text)):
                    px = pt / 3.0 * 4.0
                    text_width += px

                    if text_width > sign_width:
                        modified_text += "<"
                        text_width = 0

                        if mutual.text[i] != " ":  # 공백이 아닌 경우
                            modified_text += mutual.text[i]
                            text_width += px
                    else:
                        modified_text += mutual.text[i]

                mutual.text = modified_text
                modified_text = ""

            text_width = 0
            text.positon = pos
            self.textList.append(text)

        if len(self.textList) >= 1:
            self.current = self.textList[0]
        if len(self.textList) >= 2:
            self.next = self.textList[1]

    def jump_to_next(self) -> bool:
        if len(self.textList) <= self.index + 1:
            self.index = 0

            if len(self.textList) >= 1:
                self.current = self.textList[0]
            if len(self.textList) >= 2:
                self.next = self.textList[1]

            return False

        self.index += 1
        self.current = self.next
        self.next = (
            self.textList[self.index + 1]
            if self.index + 2 <= len(self.textList)
            else None
        )

        return True

    def reset_text_index(self):
        """각 텍스트의 인덱스 (애니메이션)을 초기화합니다."""
        for text in self.textList:
            text.jump_to_first_index()

    def set_position(self, pos: tuple):
        self.position = pos

        for text in self.textList:
            text.position = pos
