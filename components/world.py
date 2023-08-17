from .config import CONFIG, debug
from characters.player import Player

class World:
    GRAVITY = -9.8

    def __init__():
        pass

    @classmethod
    def process_gravity(cls, obj: Player, floor_y: int):
        """중력 처리"""
        fps = max(CONFIG.clock.get_fps(), 1)

        GRAVITY_PER_FRAME = World.GRAVITY / fps
        velocity_y = obj.velocity_y + GRAVITY_PER_FRAME

        debug("player_y: " + str(obj.get_pos()[1] + obj.height))
        debug("floor_y: " + str(floor_y))

        if obj.get_pos()[1] + obj.height >= floor_y:
            obj.y = floor_y - obj.height
            obj.velocity_y = 0  # 이 코드가 없으면 속도가 보존되는 슈퍼 점프 완성
        else:
            obj.move(0, velocity_y)