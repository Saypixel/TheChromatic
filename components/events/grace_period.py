from datetime import datetime
import pygame

from components.config import CONFIG, debug
from components.sprites.sprite import Sprite

class GracePeriod:
    """무적 시간"""
    period: int
    """무적시간 (ms)"""

    last_graced: datetime = datetime(2023, 1, 1, 12, 0, 0)
    """마지막으로 활성화된 무적 시간"""

    lasted = False
    '''전 프레임에서는 무적시간이였는가?'''

    def __init__(self, period = 3000):
        """
        무적 시간 클래스를 생성합니다.
        :param period: 무적이 활성화 되어있을 시간
        """
        self.period = period

    def is_grace_period(self) -> bool:
        """
        무적 시간인가?
        """
        delta = datetime.now() - self.last_graced  # 현재 시간과 마지막으로 활성화된 무적 시간의 차이
        is_grace_period = delta.total_seconds() * 1000.0 < self.period  # 차이가 무적이 활성화 되어있을 시간보다 작으면 무적 시간에 해당함

        return is_grace_period

    def update(self):
        """
        무적 시간을 현재 시간으로 업데이트
        """
        self.last_graced = datetime.now()

    def make_it_ui(self, image: Sprite | pygame.Surface):
        """
        무적 시간인 것을 UI로 보여줍니다. (투명도값 임의 설정)
        :param image: UI로 보여줄 단일 이미지 / 단일 스프라이트 (다중 스프라이트도 지원하지만 다중 스프라이트 클래스 내에서 단일 스프라이트들로 변환 후 각각 처리됨)
        """
        
        alpha = CONFIG.random.randint(50, 200)  # 50 ~ 200 범위 내에서 투명도를 임의값으로 설정
        image.set_alpha(alpha)