import pygame


class Font:
    TITLE1 = 'assets/fonts/title1.ttf'
    '''제목 1 (둥근모꼴)'''
    TITLE2 = 'assets/fonts/title2.ttf'
    '''제목 2 (갈무리11)'''
    TITLE3 = 'assets/fonts/title3.ttf'
    '''제목 3 (갈무리11 볼드)'''
    DIALOG = 'assets/fonts/dialog.ttf'
    '''대화창 (도스샘물)'''
    ILLUST = 'assets/fonts/illust.ttf'
    '''설명창 (도스고딕)'''
    OPTION = 'assets/fonts/option.ttf'
    '''설정창 (갈무리14)'''

    def get(font_path: str, size: int) -> pygame.font.Font:
        return pygame.font.Font(font_path, size)

    def get_dialog(size: int) -> pygame.font.Font:
        return Font.get(Font.DIALOG, size)