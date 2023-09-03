from components.events.time import TimeEvent
from maps import Map

class MapManager:
    """플레이어가 다니는 맵을 관리합니다."""

    maps: dict[str, Map] = {}
    """맵 배열"""

    current: Map = None
    """현재 맵"""

    @classmethod
    def apply(cls, map: str):
        """
        맵을 적용합니다.
        :param map: 적용할 맵 이름
        """
        cls.current = cls.maps[map]  # 맵 이름으로 맵을 찾아 현재 맵으로 적용

        cls.current.player.set_pos(200, 320)  # 플레이어 좌표값 초기화
        TimeEvent.reset()  # 시간 관리 변수 초기화