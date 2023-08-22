from .config import CONFIG, debug
from characters.player import Player


class World:
    GRAVITY = -32  # 중력 상수

    @classmethod
    def process_gravity(cls, objs: list[Player], floor_y: int):
        """
        중력 처리
        :param objs: 중력을 처리할 오브젝트 배열
        :param floor_y: 바닥 Y 좌표
        """
        for obj in objs:
            fps = max(CONFIG.clock.get_fps(), 1)  # fps를 가져오고 반올림

            GRAVITY_PER_FRAME = World.GRAVITY / fps  # 1프레임당 오브젝트가 받을 중력 계산
            velocity_y = obj.velocity_y + GRAVITY_PER_FRAME  # 현재 오브젝트를 감속시켜 현재 속도 계산
            obj_floor_y = obj.get_pos()[1] + obj.height  # 현재 오브젝트의 바닥 Y 좌표

            if obj_floor_y - velocity_y >= floor_y:  # 현재 오브젝트가 이동될 좌표가 바닥 좌표보다 낮은 경우 (범위를 벗어난 경우)
                obj.y = floor_y - obj.height  # 더 이상 내려가지 않게 바닥 좌표에 위치
                obj.velocity_y = 0  # 속도 초기화

                obj.is_air = False  # 바닥에 착지
            else:
                obj.move_y(velocity_y)  # 중력만큼 받은 속도를 계산하여 움직임
                obj.is_air = True  # 아직 공중에 떠 있는 상태