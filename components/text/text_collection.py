from typing import Optional
from components.text import Text

class TextCollection:
    textList: list[Text]
    
    index = 0
    current: Text = None
    next: Text = None
    
    position = (0, 0)
    '''절대좌표값'''

    def __init__(self, texts: list[Text], pos: Optional[tuple[int, int]] = (320, 180)):
        self.textList = []
        self.position = pos

        for text in texts:
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
        self.next = self.textList[self.index + 1] if len(self.textList) > self.index + 2 else None

        return True

    def reset_text_index(self):
        '''각 텍스트의 인덱스 (애니메이션)을 초기화합니다.'''
        for text in self.textList:
            text.jump_to_first_index()
