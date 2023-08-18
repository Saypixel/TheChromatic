import pygame
from abc import ABC

from components.config import CONFIG, CONST, debug

from components.text.text_collection import TextCollection
from components.events.text import TextEvent
from components.events.grace_period import GracePeriod

from components.sprites.sprite_collection import SpriteCollection
from components.sprites.sprite_handler import SpriteHandler
from components.sprites.sprite import Sprite

class Character(ABC):
    image: pygame.Surface | pygame.SurfaceType
    image_path: str
    image_flipped: bool = False

    sprites: SpriteCollection

    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0

    is_playable: bool = False
    """플레이어인가?"""

    hp = 5
    """플레이어의 체력"""

    attacked = False
    """플레이어가 공격을 받았는가?"""

    velocity_x = 0.0
    """플레이어의 속도 (X)"""

    velocity_y = 0.0
    """플레이어의 속도 (Y)"""

    """플레이어가 공중에 떠 있는가?"""
    is_air = False

    sign = None
    """말풍선"""

    grace_period: GracePeriod
    """무적 시간"""

    def __init__(
        self,
        path: str,
        position: tuple,
        scale: float = 1.0,
        flipped=False,
        fit=False,
        is_playable=False,
    ):
        """
        캐릭터 클래스 생성

        :param path: 캐릭터 이미지 경로
        :param scale: 캐릭터 크기
        :param position: 캐릭터가 위치한 절대좌표
        """
        if path == "":
            self.image_path = ""
            return

        self.image_path = path
        self.image = pygame.image.load(path)
        self.image_flipped = flipped

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

        if self.is_playable:
            CONFIG.player_x = x
            CONFIG.player_y = y

    def move_x(self, velocity: float):
        """
        캐릭터 움직임 (X 좌표)

        :param velocity: 속도 (주로 1, -1 이용)
        """
        pass

    def move_y(self, velocity: float):
        """
        캐릭터 움직임 (Y 좌표)

        :param velocity: 속도 (주로 1, -1 이용)
        """
        pass

    def is_bound(self, error_x = 0, error_y = 0, obj_x = -1, obj_y = -1) -> bool:
        """
        충돌 감지
        :param error_x: 오차 범위 (X 좌표)
        :param error_y: 오차 범위 (Y 좌표)
        :param obj_x: 플레이어 대신 비교할 X 좌표 (기본: -1)
        :param obj_y: 플레이어 대신 비교할 Y 좌표 (기본: -1)
        """
        compared_x = CONFIG.player_x if obj_x == -1 else obj_x
        compared_y = CONFIG.player_y if obj_y == -1 else obj_y

        is_x = (
            compared_x >= self.x - error_x and compared_x <= self.x + error_x
        )
        is_y = (
            compared_y >= self.y - error_y and compared_y <= self.y + error_y
        )

        return is_x and is_y

    def render(self, other_surface: pygame.Surface = None):
        if other_surface is None:
            other_surface = CONFIG.surface

        if self.image_path != "":  # 정적 이미지인 경우
            other_surface.blit(self.image, self.get_pos())
        else:  # 스프라이트인 경우
            self.sprites.set_pos(self.get_pos())
            self.sprites.get_sprite_handler().group.draw(other_surface)

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

    def flip_image(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.image_flipped = not self.image_flipped

    def check_if_attacked(self, attacked: bool):
        if (not self.attacked
            and not self.grace_period.is_grace_period()
            and CONFIG.is_movable()):

            self.attacked = attacked

    def get_surface_or_sprite(self) -> Sprite | pygame.Surface:
        """단일 이미지인 경우 pygame.Surface를 반환하고, 단일/다중 스프라이트인 경우 Sprite를 반환합니다."""
        image: Sprite | pygame.Surface

        if self.image_path != '':
            image = self.image
        elif self.sprites is not None:
            image = self.sprites.get_sprite_handler().sprite

        return image