from collections import deque
from characters.player import Player
from components.config import CONFIG, debug

class CharacterValue:
    """시간 관리를 위한 캐릭터 값 관리 클래스"""

    character: Player
    """캐릭터"""

    x: int
    """X 좌표"""

    y: int
    """Y 좌표"""

    def __init__(self, character: Player, x: int, y: int):
        """
        캐릭터 값 관리 클래스를 생성합니다.
        :param character: 보존할 캐릭터 클래스
        :param x: 보존할 캐릭터의 X 좌표
        :param y: 보존할 캐릭터의 Y 좌표
        """
        self.character = character
        self.x = x
        self.y = y

class TimeEvent:
    """시간 변동 관리국 | Time Variance Authority"""
    
    MAX_LENGTH = CONFIG.FPS * 5
    """캐릭터 값을 저장할 배열 최대 길이 (기본값: 5초)"""

    positions: deque[list[CharacterValue]] = deque()
    """플레이어 & 적 위치 배열 => Double Ended Queue를 사용"""

    is_rewind = False
    """시간을 되감을건지 여부"""

    @classmethod
    def rewind(cls) -> list[CharacterValue]:
        """
        저장된 캐릭터 값을 불러옵니다.
        :return: 저장된 캐릭터들의 값
        """
        return cls.positions.pop() if len(cls.positions) > 0 else None  # 캐릭터 값이 저장되어 있는 경우 deque를 pop하고 그렇지 않은 경우 None 반환

    @classmethod
    def update(cls, characters: list[Player]):
        """
        플레이어의 위치를 업데이트합니다.
        :param characters: 현재 캐릭터 모음
        """
        positions: list[CharacterValue] = [CharacterValue(character, character.x, character.y) for character in characters]  # 캐릭터 값 각각 저장
        cls.positions.append(positions)  # 캐릭터 값을 deque에 push

        if len(cls.positions) > TimeEvent.MAX_LENGTH:  # 범위를 초과한 경우 첫 요소 삭제
            cls.positions.popleft()
            
    @classmethod
    def reset(cls):
        """저장된 캐릭터 값을 모두 삭제합니다."""
        cls.positions.clear()
        