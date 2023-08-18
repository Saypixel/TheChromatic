from datetime import datetime

from components.config import debug


class GracePeriod:
    """무적 시간"""

    period = 3000  # 무적시간: 3000ms

    last_graced: datetime = datetime(2023, 1, 1, 12, 0, 0)

    @classmethod
    def is_grace_period(cls) -> bool:
        """
        무적 시간인가?
        """
        delta = datetime.now() - cls.last_graced
        return delta.total_seconds() * 1000.0 < cls.period

    @classmethod
    def update(cls):
        """
        무적 시간을 현재 시간으로 업데이트
        """
        cls.last_graced = datetime.now()
