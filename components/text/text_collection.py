from components.text import Text

class TextCollection:
    Texts: list[Text]

    index = 0
    current: Text = None
    next: Text = None

    def __init__(self, texts: list[Text]):
        self.Texts = []

        for text in texts:
            self.Texts.append(text)

        if len(self.Texts) >= 1:
            self.current = self.Texts[0]
        if len(self.Texts) >= 2:
            self.next = self.Texts[1]

    def jump_to_next(self) -> bool:
        if len(self.Texts) <= self.index + 1:
            self.index = 0

            if len(self.Texts) >= 1:
                self.current = self.Texts[0]
            if len(self.Texts) >= 2:
                self.next = self.Texts[1]

            return False

        self.index += 1
        self.current = self.next
        self.next = self.Texts[self.index + 1] if len(self.Texts) > self.index + 2 else None

        return True

    def reset_text_index(self):
        '''각 텍스트의 인덱스 (애니메이션)을 초기화합니다.'''
        for text in self.Texts:
            text.jump_to_first_index()
