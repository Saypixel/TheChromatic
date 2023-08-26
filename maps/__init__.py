from characters.player import Player
from characters.enemy import Enemy
from characters.texture import Texture

class Map:
    player: Player
    """플레이어"""

    NPCs: list[Player]
    """NPC 배열"""

    enemies: list[Enemy]
    """적 배열"""

    obstacles: list[Player]
    """장애물 배열"""

    sign = None
    """말풍선"""

    background: Texture
    """배경"""

    floor: Texture
    """바닥"""

    def __init__(
            self,
            player: Player = None,
            NPCs: list[Player] = [],
            enemies: list[Enemy] = [],
            obstacles: list[Player] = [],
            sign = None,
            background: Texture = None,
            floor: Texture = None
            ):
        """
        맵 클래스를 생성합니다.
        :param player: 현재 플레이어
        :param npcs: NPC 배열
        :param enemies: 적 배열
        :param obstacles: 장애물 배열
        :param background: 배경
        :param floor: 바닥
        """
        self.player = player
        self.NPCs = NPCs
        self.enemies = enemies
        self.obstacles = obstacles
        self.sign = sign
        self.background = background
        self.floor = floor

    def render(self):
        """맵을 렌더링합니다."""
        pass

    def __str__(self):
        return f"<Map Player={self.player}>"