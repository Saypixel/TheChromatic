import pygame

from characters import Character

from components.config import CONST, CONFIG, debug

from components.sprites.sprite_collection import SpriteCollection
from components.sprites.sprite_handler import SpriteHandler
from components.sprites.sprite import Sprite


class Player(Character):
    def move_x(self, velocity: float):
        """
        플레이어의 X 좌표를 이동시킵니다.
        :param velocity: 속도
        """
        
        if round(velocity, 3) != 0.0:  # 부동소수점 계산 문제를 해결하기 위해 소수점 반올림
            if (
                (velocity > 0 and self.x <= 0)
                or (velocity < 0 and self.x + self.width >= CONST.SURFACE_SIZE[0])
                or (self.x >= 0 and self.x + self.width <= CONST.SURFACE_SIZE[0])
            ):  # 세계 내부에 위치해 있는 경우 / 범위를 벗어났을 때 다시 범위 안으로 들어가려고 할 경우
                multiplied = 1 if not self.is_air else 0.7  # 공중에 떠 있으면 패널티 부여

                self.velocity_x = velocity  # 현재 속도 저장
                self.x += 10 * velocity * multiplied  # 속도와 일정 보정값만큼 위치 변화

        if self.is_playable:  # 만약 플레이어 (주인공)이라면 플레이어 좌표 따로 저장
            CONFIG.player_x = self.x

    def move_y(self, velocity: float):
        """
        플레이어의 Y 좌표를 이동시킵니다.
        :param velocity: 속도
        """

        if round(velocity, 3) != 0.0:  # 부동소수점 계산 문제를 해결하기 위해 소수점 반올림
            self.velocity_y = velocity  # 현재 속도 저장
            self.y -= velocity  # 속도만큼 위치 변화

        if self.is_playable:  # 만약 플레이어 (주인공)이라면 플레이어 좌표 따로 저장
            CONFIG.player_y = self.y

    def apply_movement_flipped(self, image: SpriteCollection | SpriteHandler | Sprite | pygame.Surface):
        """객체 움직임 적용 (다중 스프라이트, 단일 스프라이트, 단일 이미지 지원)"""
        sprite: Sprite = None
        surface: pygame.Surface = None

        if isinstance(image, SpriteCollection):
            sprite = image.get_sprite_handler().sprite
        elif isinstance(image, SpriteHandler):
            sprite = image.sprite
        elif isinstance(image, Sprite):
            sprite = image
        elif isinstance(image, pygame.Surface):
            surface = image

        if sprite is not None:
            if (self.velocity_x > 0 and sprite.flipped) or (
                self.velocity_x < 0 and not sprite.flipped
            ):  # 방향이 반대인 경우
                sprite.flip()  # 스프라이트 좌우 반전
        elif surface is not None:
            if (self.velocity_x > 0 and self.image_flipped) or (
                self.velocity_x < 0 and not self.image_flipped
            ):  # 방향이 반대인 경우
                self.flip_image()  # 단일 이미지 좌우 반전

    @classmethod
    def get_from_sprite(cls, sprites: SpriteCollection, is_playable = False) -> "Player":
        """
        다중 스프라이트를 사용하는 캐릭터 클래스를 생성합니다.

        :param sprites: 캐릭터 다중 스프라이트
        :param is_playable: 플레이어인가?
        """

        # 변수 초기화
        chr = Player("", (0, 0))  # 기본 생성자는 다중 스프라이트를 지원하지 않으므로 빈 변수로 초기화 후 다중 스프라이트 추가
        chr.sprites = sprites

        chr.x = sprites.position[0]
        chr.y = sprites.position[1]
        chr.width = sprites.size[0]
        chr.height = sprites.size[1]

        if is_playable:  # 플레이어면 플레이어 관련 변수 업데이트
            CONFIG.player_x = chr.x
            CONFIG.player_y = chr.y
            CONFIG.player_width = chr.width
            CONFIG.player_height = chr.height

        chr.is_playable = is_playable

        return chr