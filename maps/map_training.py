from maps import Map

from characters.player import Player
from characters.enemy import Enemy
from characters.texture import Texture

from components.events.grace_period import GracePeriod
from components.events.text import TextEvent
from components.events.time import TimeEvent

from components.text import Text
from components.text.text_collection import TextCollection

from components.sprites.sprite import Sprite
from components.sprites.sprite_handler import SpriteHandler
from components.sprites.sprite_collection import SpriteCollection

from components.sfx_collection import SFX

class MapTraining(Map):
    def __init__(self, player: Player, sign):
        super(Map, self).__init__()

        self.player = player

        # NPC
        self.sign = sign

        self.raon = Player("assets/images/chr_raon.png", (400, 400), 0.4, True)  # 라온
        self.raon.dialog = TextCollection(
            [
                Text("아까 언니가 소개시켜준 사람이지?"),
                Text("여기는 훈련장이야."),
                Text("쭉 가면 #적#이 출몰할거야!"),
                Text("적은 *J키*로 공격할 수 있으니 참고하라구!"),
                Text("아 맞다.. 시간 관리 능력도 있는거 알지?"),
                Text("*R키*를 누르면 궁지에 몰렸을 때 도움될거야!")
            ],
            self.sign.width
        )

        self.NPCs = [self.raon]

        # 장애물
        self.spike = Player.get_from_sprite(SpriteCollection({
            "default": SpriteHandler(
                Sprite(
                    "assets/images/object_spike_default.png", 17, 1, size=(155, 100)
                )
            )
        },
        "default",
        position=(800, 447),
        scale=0.4))

        self.spike2 = Player.get_from_sprite(SpriteCollection({
            "default": SpriteHandler(
                Sprite(
                    "assets/images/object_spike_default.png", 17, 1, size=(155, 100)
                )
            )
        },
        "default",
        position=(850, 447),
        scale=0.4))

        self.obstacles = [self.spike, self.spike2]
        
        # 적
        self.robot = Enemy.get_from_sprite(Player.get_from_sprite(SpriteCollection({
            "walk": SpriteHandler(
                Sprite(
                    "assets/images/chr_robot_walk.png", 3, 1, size=(505, 190)
                )
            ),
            "attack": SpriteHandler(
                Sprite(
                    "assets/images/chr_robot_attack.png", 16, 1, size=(505, 190)
                )
            )
        },
        "walk",
        position=(1400, 435),
        scale=0.4,
        )))
        self.robot.name = "robot"

        self.mimic = Enemy.get_from_sprite(Player.get_from_sprite(SpriteCollection({
            "walk": SpriteHandler(
                Sprite(
                    "assets/images/chr_mimic_walk.png", 7, 1, size=(185, 180)
                )
            )
        },
        "walk",
        position=(1000, 435),
        scale=0.4,
        )))
        self.mimic.name = "mimic"

        self.enemies = [self.robot, self.mimic]

        for enemy in self.enemies:
            enemy.grace_period = GracePeriod(1500)
            enemy.hp = 2

        self.items = []
        self.others_front = []
        self.others_back = []

        # 배경
        self.background = Texture("assets/images/background_training.png", (0, 0), 1, repeat_x=2, fit=True)
        self.floor = Texture("assets/images/ground_temp.png", (0, 482), 0.6, repeat_x=2)

    def process_enemy_event(self):
        """적 관련 이벤트를 처리합니다. (적 방향, 사망, 공격, 따라가기)"""
        super().process_enemy_event()

        # 일정 거리에서 공격하는 경우
        for enemy in [self.robot]:
            if not enemy.grace_period.is_grace_period():  # 스턴 시간이 끝난 경우
                if not enemy.is_bound(40, 50):  # 일정 거리 안에 없는 경우
                    enemy.sprites.status_next = "walk"
                    
                    if enemy.sprites.status == "walk":
                        enemy.follow_player(self.obstacles)  # 적이 플레이어를 따라가기
                else:
                    enemy.sprites.status_next = "attack"


        # 플레이어를 쫓아가서 공격하는 경우
        for enemy in [self.mimic]:
            if not enemy.grace_period.is_grace_period():  # 스턴 시간이 끝난 경우
                enemy.follow_player(self.obstacles)  # 적이 플레이어를 따라가기
                self.player.check_if_attacked(enemy.is_bound(40, 100) and enemy.hp > 0 and not enemy.grace_period.is_grace_period())  # 플레이어 공격 받았는지 확인

    def process_item_pickup_event(self):
        """아이템 줍기 관련 이벤트를 처리합니다."""
        positions = {
            "heal": (15, 12),
            "key": (20, 22)
        }

        for item in self.items:
            if item.is_bound(10, 50):  # 플레이어가 아이템을 주울 경우 아이템 삭제
                from screens.ingame import Ingame
                
                index = self.items.index(item)
                self.items.pop(index)

                position = positions[item.name]
                item.set_pos(position[0], position[1])  # 상대좌표

                Ingame.default.inventories[item.name] = item
                Ingame.default.inventory_keys.append(item.name)
                Ingame.default.inventory_keys_index = len(Ingame.default.inventory_keys) - 1

                SFX.ITEM_PICKUP.play()

    def process_item_use_event(self, item: Texture):
        """
        아이템 사용 관련 이벤트를 처리합니다.
        :param item: 현재 쓸 아이템의 텍스쳐 
        """
        match item.name:
            case "heal":
                self.player.healed = True

            case "key":
                pass

    def process_door_event(self):
        """문 관련 이벤트를 처리합니다."""
        pass

    def render(self, frame_count: int):
        """
        맵을 렌더링합니다.
        :param frame_count: 1초 당 누적되는 프레임 렌더링하는 개수 (범위: 0~10)
        """
        if frame_count % 5 == 0:  # 5프레임마다 적 스프라이트 갱신
            if self.robot in self.enemies:
                self.robot.sprites.get_sprite_handler().sprite.update()

                # 로봇 공격하는 애니메이션일 때 공격하기
                if self.robot.sprites.status == "attack":
                    if self.robot.sprites.get_sprite_handler().sprite.index == 7:
                        additional_attacked = self.robot.hp > 0 and not self.robot.grace_period.is_grace_period() and not TimeEvent.is_rewind
                        attacked = self.robot.is_bound(40, 100) and additional_attacked
                        
                        self.player.check_if_attacked(attacked)

                        if additional_attacked:
                            SFX.ATTACK_LAZER.play()

                # 스프라이트가 바뀌어야 할 상황인 경우
                if self.robot.sprites.get_sprite_handler().sprite.index == 0 and self.robot.sprites.status != self.robot.sprites.status_next:
                    self.robot.sprites.status = self.robot.sprites.status_next  # 바뀌어야 할 스프라이트로 변경

            if self.mimic in self.enemies:
                self.mimic.sprites.get_sprite_handler().sprite.update()

        self.process_door_event()

        super().render(frame_count)