import pygame
from .sprite import Sprite

class SpriteHandler:
    """스프라이트를 쉽게 쓰고 관리할 수 있는 클래스"""
    sprite: Sprite
    group: pygame.sprite.Group

    def __init__(self, sprite: Sprite):
        self.sprite = sprite
        self.group = pygame.sprite.Group(sprite)