import pygame
from abc import ABC
from components.text.text_collection import TextCollection
from components.events.text import TextEvent
from components.config import CONFIG, CONST, debug

class Character(ABC):
    image: pygame.Surface | pygame.SurfaceType
    image_path: str
    
    x: int
    y: int
    width: int
    height: int
    
    is_playable: bool

    sign = None

    def __init__(self, path: str, position: tuple, scale: float = 1.0, fit = False, is_playable = False):
        """
        캐릭터 클래스 생성

        :param path: 캐릭터 이미지 경로
        :param scale: 캐릭터 크기
        :param position: 캐릭터가 위치한 절대좌표
        """
        self.image_path = path
        self.image = pygame.image.load(path)

        if fit:
            self.image = pygame.transform.scale(self.image, CONST.SCREEN_SIZE)
        else:
            scale_x = float(self.image.get_width()) * scale
            scale_y = float(self.image.get_height()) * scale

            self.image = pygame.transform.scale(self.image, (scale_x, scale_y))

        self.x = position[0]
        self.y = position[1]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        if is_playable:
            CONFIG.player_width = self.width
            CONFIG.player_height = self.height

        self.is_playable = is_playable

    def get_pos(self) -> tuple:
        return (self.x, self.y)
    
    def set_pos(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def move(self, velocity: float):
        """
        캐릭터 움직임

        :param velocity: 속도 (주로 1, -1 이용)
        """
        pass

    def is_bound(self, error = 0) -> bool:
        return CONFIG.player_x >= self.x - error and CONFIG.player_x <= self.x + error

    def render(self, other_surface: pygame.Surface = None):
        if other_surface is None:
            other_surface = CONFIG.surface

        other_surface.blit(self.image, self.get_pos())

        if self.sign is not None:
            other_surface.blit(self.sign.image, self.sign.get_pos())

    def speech(self, sign):
        if self.sign is None:
            self.sign = sign

        x = self.x - self.sign.width + 10
        y = self.y - self.sign.height + 5

        sign.set_pos(x, y)
        TextEvent.dialog.set_position((10, 10))

    def unspeech(self):
        if self.sign is None:
            return
        
        self.sign = None

    def refresh(self):
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))