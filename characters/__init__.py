import pygame
from abc import ABC

from components.text.text_collection import TextCollection
from components.events.text import TextEvent
from components.config import CONFIG, CONST, debug
from components.sprite import Sprite

class Character(ABC):
    image: pygame.Surface | pygame.SurfaceType
    image_path: str

    sprite: Sprite
    sprite_group: pygame.sprite.Group
    
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0

    velocity = 0.0
    
    is_playable: bool = False

    sign = None

    def __init__(self, path: str, position: tuple, scale: float = 1.0, fit = False, is_playable = False):
        """
        캐릭터 클래스 생성

        :param path: 캐릭터 이미지 경로
        :param scale: 캐릭터 크기
        :param position: 캐릭터가 위치한 절대좌표
        """
        if path == '':
            self.image_path = ''
            return

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

        if self.image_path != '':  # 정적 이미지인 경우
            other_surface.blit(self.image, self.get_pos())
        else:  # 스프라이트인 경우
            #debug(str(self.get_pos()[0]) + ', ' + str(self.get_pos()[1]))
            self.sprite.position = self.get_pos()
            self.sprite.rect = (self.sprite.position[0], self.sprite.position[1], self.sprite.size[0], self.sprite.size[1])

            self.sprite_group.draw(other_surface)

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