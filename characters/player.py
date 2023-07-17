from characters import Character

from components.config import CONST


class Player(Character):
    def move(self, velocity: float):
        # 윈도우 내부에 위치해 있는 경우
        if (velocity > 0 and self.pos_x <= 0) or (velocity < 0 and self.pos_x >= CONST.SCREEN_SIZE[0]) or (0 <= self.pos_x <= CONST.SCREEN_SIZE[0]):
            self.pos_x += 10 * velocity
