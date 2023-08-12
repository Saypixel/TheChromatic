from characters import Character

from components.config import CONST, CONFIG
from components.text.text_collection import TextCollection
from components.events.text import TextEvent

class Player(Character):
    def move(self, velocity: float):
        # 윈도우 내부에 위치해 있는 경우
        if (velocity > 0 and self.pos_x <= 0) or (velocity < 0 and self.pos_x >= CONST.SCREEN_SIZE[0]) or (0 <= self.pos_x <= CONST.SCREEN_SIZE[0]):
            self.pos_x += 10 * velocity

            if self.is_playable:
                CONFIG.player_pos_x = self.pos_x
                CONFIG.player_pos_y = self.pos_y

    def is_bound(self) -> bool:
        return CONFIG.player_pos_x >= self.pos_x