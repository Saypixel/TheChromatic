from components.config import CONFIG, debug
from components.world import World

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

    items: list[Texture]
    """아이템 배열"""

    others_front: list[Texture]
    """가장 처음에 렌더링할 기타 객체 배열"""

    others_back: list[Texture]
    """나중에 렌더링할 기타 객체 배열"""

    obstacle_error_x = 0
    obstacle_error_y = 0
    """가시 오차 범위 (동적 히트박스)"""

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
            items: list[Texture] = [],
            others_front: list[Texture] = [],
            others_back: list[Texture] = [],
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
        :param others_front: 가장 처음으로 렌더링할 기타 객체 배열
        :param others_back: 나중에 렌더링할 기타 객체 배열
        :param background: 배경
        :param floor: 바닥
        """
        self.player = player
        self.NPCs = NPCs
        self.enemies = enemies
        self.obstacles = obstacles
        self.others_front = others_front
        self.others_back = others_back
        self.items = items
        self.sign = sign
        self.background = background
        self.floor = floor

    def render(self, frame_count: int):
        """
        맵을 렌더링합니다.
        :param frame_count: 1초 당 누적되는 프레임 렌더링하는 개수 (범위: 0~10)
        """
        self.background.set_pos(CONFIG.camera_x, self.background.y)

        CONFIG.surface.blit(self.background.image.convert(), self.background.get_pos())
        CONFIG.surface.blit(self.floor.image, self.floor.get_pos())

        World.process_gravity(self.enemies + [self.player], self.floor.y)  # 중력 구현

        self.process_obstacle_bound()  # 장애물
        self.process_enemy_event()  # 적
        self.process_grace_period_animation()  # 무적 시간

        if frame_count % 5 == 0:  # 5 프레임마다 갱신
            # 장애물 애니메이션
            for obstacle in self.obstacles:
                if obstacle.is_sprite():
                    obstacle.sprites.get_sprite_handler().sprite.update()

        # 기타 객체
        for other in self.others_front:
            other.render()

        # 장애물
        for obstacle in self.obstacles:
            obstacle.render()

        # NPC
        for NPC in self.NPCs:
            NPC.render()

        # 기타 객체
        for other in self.others_back:
            other.render()

        # 적
        for enemy in self.enemies:
            enemy.render()

        # 아이템
        self.process_item_pickup_event()

        for item in self.items:
            item.render()

        # 플레이어
        self.player.render()

    def process_obstacle_bound(self):
        """장애물 충돌 감지를 처리합니다."""
        for obstacle in self.obstacles:
                if self.player.is_air:  # 플레이어가 점프 한 경우 가시에 잘 안닿도록 오차 범위 설정
                    self.obstacle_error_x = max(self.obstacle_error_x - 1, -5)
                    self.obstacle_error_y = max(self.obstacle_error_y - 1, 20)
                else:  # 걷고 있는 경우 가시에 잘 닿도록 오차 범위 설정
                    self.obstacle_error_x = min(self.obstacle_error_x + 1, 10)
                    self.obstacle_error_y = min(self.obstacle_error_y + 1, 26)

                is_bound = obstacle.is_bound(self.obstacle_error_x, self.obstacle_error_y)  # 보정값만큼 충돌 감지
                self.player.check_if_attacked(is_bound)  # 조건에 충족된 충돌 감지가 되면 플레이어가 공격받았다고 처리

    def process_enemy_event(self):
        """적 관련 이벤트를 처리합니다. (적 방향, 사망)"""
        for enemy in self.enemies:
            image = enemy.get_surface_or_sprite()
            enemy.apply_movement_flipped(image)  # 움직임을 따라 적 방향 적용

            if enemy.hp <= 0:
                if not enemy.fade_out():  # 적 사망 후 완전 투명해졌을 때
                    index = self.enemies.index(enemy)
                    self.enemies.pop(index)  # 적 제거

    def process_grace_period_animation(self):
        """무적 시간 애니메이션을 처리합니다."""
        for player in self.enemies + [self.player]:  # 적 + 플레이어
            if player.grace_period is not None:  # 무적 시간 변수가 할당되어 있는 경우
                image = player.get_surface_or_sprite()  # 단일 이미지 / 다중 스프라이트 반환

                if player.grace_period.is_grace_period():  # 무적시간인 경우
                    player.grace_period.make_it_ui(image)  # 무적 시간인 것을 플레이어에게 UI로 보여줌
                    player.grace_period.lasted = True  # 무적 시간 프레임 업데이트 변수 갱신

                elif player.grace_period.lasted:  # 이전 프레임에서는 무적 시간이였고, 지금은 아닌 경우
                    image.set_alpha(255)  # 무적 시간이 아니므로 UI 복귀
                    player.grace_period.lasted = False  # 무적 시간 프레임 업데이트 변수 갱신

    def process_item_pickup_event(self):
        """아이템 줍기 관련 이벤트를 처리합니다."""
        pass

    def process_item_use_event(self, item: Texture):
        """
        아이템 사용 관련 이벤트를 처리합니다.
        :param item: 현재 쓸 아이템의 텍스쳐 
        """
        pass

    def __str__(self):
        return f"<Map Player={self.player}>"