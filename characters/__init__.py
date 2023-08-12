import pygame
from abc import ABC

class Character(ABC):
    image: pygame.Surface | pygame.SurfaceType
    pos_x: int
    pos_y: int
    
    is_playable: bool

    def __init__(self, path: str, scale: tuple, position: tuple, is_playable = False):
        """
        캐릭터 클래스 생성

        :param path: 캐릭터 이미지 경로
        :param scale: 캐릭터 크기 ex) (100, 100)
        :param position: 캐릭터가 위치한 절대좌표
        """
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, scale)

        self.pos_x = position[0]
        self.pos_y = position[1]

        self.is_playable = is_playable

    def get_pos(self) -> tuple:
        return (self.pos_x, self.pos_y)
    
    def move(self, velocity: float):
        """
        캐릭터 움직임

        :param velocity: 속도 (주로 1, -1 이용)
        """
        pass