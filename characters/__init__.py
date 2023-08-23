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
    """단일 이미지"""

    image_path: str
    """단일 이미지 경로"""

    image_flipped: bool = False
    """단일 이미지가 좌우반전 되어있는가?"""

    sprites: SpriteCollection = None
    """다중 스프라이트"""

    """
    캐릭터 클래스는 단일 이미지 / 다중 스프라이트 중 하나를 지원하여 어느 것을 사용할지 선택할 수 있습니다.
    1. 단일 이미지 => 기본 생성자 __init__()
    2. 다중 스프라이트 => Player.get_from_sprite()
    """

    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    """좌표 및 크기"""

    is_playable: bool = False
    """플레이어인가?"""

    hp = 5
    """플레이어의 체력"""

    attack = False
    """플레이어가 공격을 했는가?"""

    attacked = False
    """플레이어가 공격을 받았는가?"""

    healed = False
    """플레이어가 체력 회복을 했는가?"""

    velocity_x = 0.0
    """플레이어의 속도 (X)"""

    velocity_y = 0.0
    """플레이어의 속도 (Y)"""

    is_air = False
    """플레이어가 공중에 떠 있는가?"""

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
        repeat_x=1,
        repeat_y=1,
        is_playable=False,
    ):
        """
        캐릭터 클래스 생성
        :param path: 캐릭터 이미지 경로
        :param position: 캐릭터가 위치한 절대좌표
        :param scale: 캐릭터 상대크기
        :param flipped: 이미지가 처음부터 좌우반전 되어 있었는가?
        :param fit: 화면 크기에 맞춰 스케일링 할 것인가?
        :param repeat_x: 이미지가 가로로 반복될 횟수
        :param repeat_y: 이미지가 세로로 반복될 횟수
        :param is_playable: 플레이어인가?
        """
        if path == "":  # 다중 스프라이트로 초기화하기 위해 단일 이미지를 선택하지 않은 경우
            self.image_path = ""
            return  # 빈 클래스로 반환

        # 단일 이미지로 설정
        self.image_path = path
        self.image = pygame.image.load(path)
        self.image_flipped = flipped

        if fit:  # 화면 크기에 맞춰 스케일링
            self.image = pygame.transform.scale(self.image, CONST.SCREEN_SIZE)
        else:  # 상대크기에 맞춰 스케일링
            scale_x = float(self.image.get_width()) * scale
            scale_y = float(self.image.get_height()) * scale

            self.image = pygame.transform.scale(self.image, (scale_x, scale_y))

        if repeat_x > 1 or repeat_y > 1:  # 이미지가 반복되는 경우
            width_per_image = self.image.get_width()  # 이미지당 너비
            height_per_image = self.image.get_height()  # 이미지당 높이
            image_repeated = pygame.Surface((width_per_image * repeat_x, height_per_image * repeat_y), pygame.SRCALPHA, 32)  # 배경이 투명한 이미지 생성
            
            for y in range(0, repeat_y):
                for x in range(0, repeat_x):
                    image_repeated.blit(self.image, (x * width_per_image, y * height_per_image))  # 이미지 렌더링 반복

            self.image = image_repeated  # 반복된 이미지로 저장

        # 좌표 & 크기 변수 초기화
        self.x = position[0]
        self.y = position[1]
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        if is_playable:  # 플레이어인 경우 플레이어 관련 변수 업데이트
            CONFIG.player_width = self.width
            CONFIG.player_height = self.height

        self.is_playable = is_playable

    def get_pos(self) -> tuple:
        """
        캐릭터의 현재 좌표를 가져옵니다.
        :return: 현재 좌표
        """
        return (self.x, self.y)

    def set_pos(self, x: int, y: int):
        """
        캐릭터의 현재 좌표를 설정합니다.
        :param x: 설정할 X 좌표
        :param y: 설정할 Y 좌표
        """
        self.x = x
        self.y = y

        if self.is_playable:  # 플레이어인 경우 플레이어 관련 변수 업데이트
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

    def is_bound(self, error_x = 0, error_y = 0, obj_x = -1, obj_y = -1, obj_width = -1, obj_height = -1, hitbox = False) -> bool:
        """
        충돌 감지
        :param error_x: 오차 범위 (X 좌표)
        :param error_y: 오차 범위 (Y 좌표)
        :param obj_x: 플레이어 대신 비교할 X 좌표 (기본: -1)
        :param obj_y: 플레이어 대신 비교할 Y 좌표 (기본: -1)
        :param obj_width: 플레이어 대신 비교할 Width (기본: -1)
        :param obj_height: 플레이어 대신 비교할 Height (기본: -1)
        :param hitbox: 히트박스 여부 (디버깅)
        :return: 충돌 감지 여부
        """
        # 비교할 좌표 기준을 오브젝트의 중심으로 설정
        compared_x = CONFIG.player_x + CONFIG.player_width / 2 if obj_x == -1 else obj_x + obj_width / 2  # 비교할 X 좌표 (obj_x가 -1인 경우 플레이어로 설정)
        compared_y = CONFIG.player_y + CONFIG.player_height / 2 if obj_y == -1 else obj_y + obj_height / 2  # 비교할 Y 좌표 (obj_y가 -1인 경우 플레이어로 설정)

        # 비교할 오브젝트의 좌표가 현재 오브젝트의 좌표 범위 안에 있는 경우
        # 오차 보정을 해야하는 경우 보정값 추가
        is_x = self.x - error_x <= compared_x <= self.x + self.width + error_x
        is_y = self.y - error_y <= compared_y <= self.y + self.height + error_y

        if hitbox:  # 히트박스를 그려야 하는 경우
            x = self.x - error_x
            y = self.y - error_y
            width = self.width + error_x * 2
            height = self.height + error_y * 2
            pygame.draw.rect(CONFIG.surface, (0, 200, 0), (x, y, width, height), 3)  # 두께가 3이고 초록색으로 히트박스 범위를 그림

        return is_x and is_y
    
    def generate_hitbox(self):
        """히트박스를 생성합니다. (디버깅)"""
        pygame.draw.rect(CONFIG.surface, (0, 200, 0), (self.x + self.width / 2, self.y + self.height / 2, 3, 3), 3)

    def is_camera_bound(self, error: float = 1.00) -> bool:
        """
        해당 오브젝트가 카메라 안에 들어와있는지 확인합니다.
        :param error: 오차 보정값
        :return: 오브젝트가 카메라 안에 들어왔는지 여부
        """

        camera = CONFIG.get_camera_bound()  # 카메라 범위 가져오기
        camera_x = camera[0]
        camera_y = camera[1]
        camera_width = camera[2]
        camera_height = camera[3]

        # 양쪽 범위를 끝까지 벗어나지 않았을 때도 렌더링 해야하므로 보정값 추가, 오차 보정값이 있는 경우 오차 보정
        is_x = camera_x <= self.x + self.width <= (camera_x + camera_width + self.width) / error
        is_y = camera_y <= self.y + self.height <= (camera_y + camera_height + self.height) / error

        return is_x and is_y

    def render(self, other_surface: pygame.Surface = None, optimization = True):
        """
        오브젝트를 렌더링합니다.
        :param other_surface: 사용자 지정 렌더링할 화면 (기본: CONFIG.surface)
        :param optimization: 렌더링 최적화 여부
        """

        if optimization and not self.is_camera_bound():  # 최적화 중 카메라 범위에 벗어나있는 경우
            return  # 렌더링할 필요 없으므로 종료

        if other_surface is None:
            other_surface = CONFIG.surface

        if not self.is_sprite():  # 정적 이미지인 경우
            other_surface.blit(self.image, self.get_pos())

        else:  # 스프라이트인 경우
            self.sprites.set_pos(self.get_pos())
            self.sprites.get_sprite_handler().group.draw(other_surface)

        if self.sign is not None:  # 말풍선을 렌더링 해야하는 경우
            other_surface.blit(self.sign.image, self.sign.get_pos())

    def speech(self, sign):
        """
        캐릭터가 대화를 할 수 있도록 합니다.
        :param sign: 말풍선
        """
        if self.sign is None:  # 말풍선이 초기화되어 있는 경우 
            self.sign = sign  # 말풍선 설정

        # 말풍선 좌표 설정
        x = self.x - self.sign.width + 10
        y = self.y - self.sign.height + 5

        sign.set_pos(x, y)
        TextEvent.dialog.set_position((10, 10))  # 말풍선 속 텍스트 상대 좌표 설정

    def unspeech(self):
        """
        캐릭터가 대화가 끝났을 때 관련 변수를 재설정합니다.
        """
        if self.sign is None:  # 이미 말풍선이 초기화된 경우 반환
            return

        self.sign = None  # 말풍선 초기화

    def refresh(self):
        """단일 이미지를 새로고침합니다."""
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))  # 상대크기에 맞춰 스케일링

    def flip_image(self):
        """단일 이미지를 좌우 반전시킵니다."""
        self.image = pygame.transform.flip(self.image, True, False)
        self.image_flipped = not self.image_flipped  # 좌우 반전 변수 업데이트

    def check_if_attacked(self, attacked: bool):
        """
        공격받았는지 확인 후, 공격받았을 때 조건이 충족된 경우 공격받았다고 설정됩니다.
        :param attacked: 공격받았는지 여부 (보통 함수로부터 반환됨)
        """

        """
        공격받았을 때 조건
        1. 공격을 받았는가?
        2. 무적 시간에 위배되지 않았는가?
        3. 플레이어가 상호작용하고 움직일 수 있었는가?
        """

        if (not self.attacked
            and not self.grace_period.is_grace_period()  # 무적 시간 계산
            and CONFIG.is_movable()):  # 플레이어가 움직일 수 있는 경우

            self.attacked = attacked  # 공격받았다고 설정

    def fade_out(self, delta: int = 30) -> bool:
        """
        캐릭터를 점차 흐리게 만들어 투명도를 0으로 만듭니다.
        :param delta: 한 프레임당 투명도 감소량 (기본: 30)
        :return: 더 이상 흐리게 만들 수 있는지의 여부
        """

        surface = self.get_surface_or_sprite()  # 단일 이미지 / 다중 스프라이트 가져오기
        alpha = surface.get_alpha()  # 투명도값 가져오기
        alpha_next = max(0, alpha - delta)  # delta 값만큼 감소된 투명도값 가져오기

        surface.set_alpha(alpha_next)  # delta 값만큼 감소된 투명도 값 설정

        return alpha_next > 0  # 더 이상 흐리게 만들 수 있는가?

    def get_surface_or_sprite(self) -> SpriteCollection | pygame.Surface: 
        """단일 이미지인 경우 pygame.Surface를 반환하고, 다중 스프라이트인 경우 SpriteCollection을 반환합니다."""
        image: Sprite | pygame.Surface

        if self.is_sprite():
            image = self.sprites
        else:
            image = self.image

        return image
    
    def is_sprite(self) -> bool:
        """스프라이트인지 여부를 반환합니다. (그렇지 않은 경우 단일 이미지)"""
        return self.sprites is not None and self.image_path == ""