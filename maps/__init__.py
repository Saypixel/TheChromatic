from components.config import CONFIG
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

    def render(self, frame_count: int):
        """
        맵을 렌더링합니다.
        :param frame_count: 1초 당 누적되는 프레임 렌더링하는 개수 (범위: 0~10)
        """
        self.background.set_pos(CONFIG.camera_x, self.background.y) 
        #self.background.set_pos(CONFIG.camera_x // 1.1, self.background.y)  # 조금씩 움직이게 하고 싶어요

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

        # 장애물
        for obstacle in self.obstacles:
            obstacle.render()

        # NPC
        for NPC in self.NPCs:
            NPC.render()

        # 적
        for enemy in self.enemies:
            enemy.render()

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
        """적 관련 이벤트를 처리합니다. (적 방향, 사망, 따라가기, 공격)"""
        for enemy in self.enemies:
            enemy.apply_movement_flipped(enemy.image)  # 움직임을 따라 적 방향 적용

            if enemy.hp <= 0:
                if not enemy.fade_out():  # 적 사망 후 완전 투명해졌을 때
                    index = self.enemies.index(enemy)
                    self.enemies.pop(index)  # 적 제거
            
            if not enemy.grace_period.is_grace_period():  # 스턴 시간이 끝난 경우
                enemy.follow_player(self.obstacles)  # 적이 플레이어를 따라가기
                self.player.check_if_attacked(enemy.is_bound(40, 100) and enemy.hp > 0 and not enemy.grace_period.is_grace_period())  # 플레이어 공격 받았는지 확인

    def process_grace_period_animation(self):
        """무적 시간 애니메이션을 처리합니다."""
        for player in self.enemies + [self.player]:  # 적 + 플레이어
            if player.grace_period is not None:
                image = player.get_surface_or_sprite()

                if player.grace_period.is_grace_period():  # 무적시간인 경우
                    player.grace_period.make_it_ui(image)
                    player.grace_period.lasted = True

                elif player.grace_period.lasted:
                    image.set_alpha(255)  # 무적 시간이 아니므로 복귀
                    player.grace_period.lasted = False

    def __str__(self):
        return f"<Map Player={self.player}>"