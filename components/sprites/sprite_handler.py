import pygame
from .sprite import Sprite


class SpriteHandler:
    """스프라이트를 쉽게 쓰고 관리할 수 있는 클래스"""

    sprite: Sprite
    """현재 스프라이트"""

    group: pygame.sprite.Group
    """현재 스프라이트를 관리하고 렌더링할 때 쓰이는 클래스"""

    def __init__(self, sprite: Sprite):
        """
        SpriteHandler 클래스를 생성합니다.
        :param sprite: 관리할 스프라이트
        """
        self.sprite = sprite
        self.group = pygame.sprite.Group(sprite)
