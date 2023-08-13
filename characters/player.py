from characters import Character

from components.config import CONST, CONFIG
from components.text.text_collection import TextCollection
from components.events.text import TextEvent

class Player(Character):
    def move(self, velocity: float):
        # 윈도우 내부에 위치해 있는 경우
        if (velocity > 0 and self.x <= 0) or (velocity < 0 and self.x >= CONST.SCREEN_SIZE[0]) or (0 <= self.x <= CONST.SCREEN_SIZE[0]):
            self.x += 10 * velocity

            if self.is_playable:
                CONFIG.player_x = self.x
                CONFIG.player_y = self.y