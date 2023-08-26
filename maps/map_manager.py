from characters.player import Player

from maps import Map
from maps.map_main import MapMain

class MapManager:
    """플레이어가 다니는 맵을 관리합니다."""

    maps: dict[str, Map] = {}

    current: Map = None
    """현재 맵"""

    @classmethod
    def apply(cls, map: str):
        """
        맵을 적용합니다.
        :param map: 적용할 맵
        """
        
        cls.current = cls.maps[map]