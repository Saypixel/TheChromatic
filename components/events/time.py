from collections import deque

from characters.player import Player

from components.config import CONFIG, debug

class TimeEvent:
    """시간 변동 관리국 | Time Variance Authority"""
    
    MAX_LENGTH = CONFIG.FPS * 5  # 5초

    positions: deque[list[tuple[Player, int, int]]] = deque()
    """플레이어 & 적 위치 배열 => Double Ended Queue를 사용"""

    is_rewind = False
    """시간을 되감을건지 여부"""

    @classmethod
    def rewind(cls) -> list[tuple[Player, int, int]]:
        return cls.positions.pop() if len(cls.positions) > 0 else None

    @classmethod
    def update(cls, characters: list[Player]):
        """
        플레이어의 위치를 업데이트합니다.
        :param positions: 현재 플레이어와 적의 위치
        """
        positions: list[tuple[Player, int, int]] = [(character, character.x, character.y) for character in characters]
        cls.positions.append(positions)

        if len(cls.positions) > TimeEvent.MAX_LENGTH:  # 범위를 초과한 경우 첫 요소 삭제
            cls.positions.popleft()
            
    @classmethod
    def reset(cls):
        cls.positions.clear()
        pass

    @classmethod
    def debug(cls):
        pass
