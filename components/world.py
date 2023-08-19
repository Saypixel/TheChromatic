from .config import CONFIG, debug
from characters.player import Player


class World:
    GRAVITY = -32

    def __init__():
        pass

    @classmethod
    def process_gravity(cls, objs: list[Player], floor_y: int):
        """중력 처리"""
        for obj in objs:
            fps = max(CONFIG.clock.get_fps(), 1)

            GRAVITY_PER_FRAME = World.GRAVITY / fps
            velocity_y = obj.velocity_y + GRAVITY_PER_FRAME

            if obj.get_pos()[1] + obj.height - velocity_y >= floor_y:
                obj.y = floor_y - obj.height
                obj.velocity_y = 0

                obj.is_air = False
            else:
                obj.move_y(velocity_y)
                obj.is_air = True