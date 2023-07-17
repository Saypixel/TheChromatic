import pygame
from components.config import Fonts


class Font:
    def __init__(self, font: Fonts, size: int):
        self.font: Fonts = font
        self.size: int = size

    def to_pygame(self) -> pygame.font.Font:
        return pygame.font.Font(self.font.value, self.size)

    def get_dialog(self) -> pygame.font.Font:
        return pygame.font.Font(self.font.DIALOG.value, self.size)

    def render(self, text: str,
               color: tuple[int, int, int]) -> pygame.Surface | pygame.SurfaceType:
        return pygame.font.Font(self.font.value, self.size).render(text, False, color)
