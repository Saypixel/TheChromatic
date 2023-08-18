from datetime import datetime
import pygame

from components.config import CONFIG, debug
from components.sprites.sprite import Sprite

class GracePeriod:
    """무적 시간"""
    period: int # 무적시간 (ms)

    last_graced: datetime = datetime(2023, 1, 1, 12, 0, 0)

    lasted = False
    '''전 프레임에서는 무적시간이였는가?'''

    def __init__(self, period = 3000):
        self.period = period

    def is_grace_period(self) -> bool:
        """
        무적 시간인가?
        """
        delta = datetime.now() - self.last_graced
        return delta.total_seconds() * 1000.0 < self.period

    def update(self):
        """
        무적 시간을 현재 시간으로 업데이트
        """
        self.last_graced = datetime.now()

    def make_it_ui(self, image: Sprite | pygame.Surface):
        """무적 시간인 것을 UI로 보여줍니다. (Alpha값 임의 설정)"""
        
        alpha = CONFIG.random.randint(50, 200)
        image.set_alpha(alpha)