import pygame

from ..config import Fonts
from .mutual_text import MutualText
from ..font import Font

__all__ = ['Text', 'MutualText']

class Text:
    DEFAULT_DELAY = 30
    '''기본 지연 시간 (ms)'''

    raw = ''
    '''날 것의 텍스트. 접두어 포함'''

    pure = ''
    '''순수 텍스트. 접두어 미포함'''

    has_prefix = False
    '''접두어가 포함되어있는가?'''

    texts: list[MutualText]
    '''텍스트 리스트 (상호작용 배열)'''

    index = 0
    '''텍스트 리스트 index (상호작용 배열)'''

    '''
    https://gist.github.com/ihoneymon/652be052a0727ad59601 : 일부 문법은 깃허브 마크다운 문법을 참조하였습니다.

    * : 굵게
    # : 크게
    / : 얇게 (미지원)
    ^ : 흔들리게 (미지원)
    < : 느리게
    '''

    def __init__(self, text: str):
        """
        Text 클래스를 생성합니다.
        :param text: 텍스트
        """
        self.texts = []

        self.raw = text
        self.pure = text  # 일단 저장. 어차피 replace() 함수를 통해 접두어를 제거하기 때문.

        for prefix in ['*', '#', '/', '^', '<']:
            if prefix in self.pure:
                self.has_prefix = True
                self.pure = self.pure.replace(prefix, '')

        is_started = False
        mutual_text_ = ''
        prefix = ''
        delay = self.DEFAULT_DELAY

        for ch in self.raw:
            match ch:
                case '*' | '#' | '/' | '^' | '<':
                    is_started = not is_started

                    if mutual_text_:  # mutual text가 비어있지 않은 경우
                        mutual = MutualText(mutual_text_, prefix, delay)
                        mutual_text_ = ''
                        delay = self.DEFAULT_DELAY
                        self.texts.append(mutual)

                    prefix = ch if is_started else ''

                    if ch == '<':
                        prefix = ''
                        delay = self.DEFAULT_DELAY - 10

                case _:
                    mutual_text_ += ch

        if mutual_text_:  # mutual text가 비어있지 않은 경우
            mutual = MutualText(mutual_text_, '', delay)
            self.texts.append(mutual)

    def write_until_next(self, position: tuple[int, int], surface: pygame.Surface) -> int:
        """
        진행 중인 텍스트를 렌더링 (출력)합니다.
        :param position: 화면 위치
        :param surface: 화면
        :return: 텍스트 애니메이션 지연 시간
        """
        ch_x = position[0]
        ch_y = position[1]
        mutual = MutualText('', '', 0)

        for i in range(0, self.index + 1):
            mutual = self.texts[i]

            for j in range(0, mutual.index + 1):
                font = Fonts.DIALOG
                pt = 20
                px = 26.66

                match mutual.prefix:
                    case '*':
                        font = Fonts.TITLE3
                    case '#':
                        pt += 10
                    case '/':
                        pt -= 10

                px = pt / 3.0 * 4.0

                ch = Font(font, pt).render(mutual.text[j], (0, 0, 0))
                surface.blit(ch, (ch_x, ch_y))

                ch_x += px

        last_mutual = self.texts[len(self.texts) - 1]

        # 애니메이션이 완료된 텍스트가 렌더링이 다 된 경우
        if self.index == len(self.texts) - 1 and last_mutual.index == len(last_mutual.text) - 1:
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
        '''(디버깅용) index 출력'''
        print(self.index, self.texts[self.index].index)