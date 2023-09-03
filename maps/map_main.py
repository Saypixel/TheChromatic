from maps import Map

from characters.player import Player
from characters.enemy import Enemy
from characters.texture import Texture

from components.config import debug

from components.events.grace_period import GracePeriod
from components.events.text import TextEvent

from components.text import Text
from components.text.text_collection import TextCollection

from components.sprites.sprite import Sprite
from components.sprites.sprite_handler import SpriteHandler
from components.sprites.sprite_collection import SpriteCollection

from components.sfx_collection import SFX

from components.inventory import Inventory

class MapMain(Map):
    def __init__(self, player: Player, sign):
        super(Map, self).__init__()

        self.player = player

        # NPC
        self.sign = sign

        self.emilia = Player("assets/images/chr_emilia.png", (400, 360), 0.4)  # 에밀리아
        self.emilia.dialog = TextCollection(
            [
                Text("*안녕!*"),
                Text("나는 조작법을 설명해줄 에밀리아야!"),
                Text("*J키*는 #기본공격#이구, *E키*로 아이템 사용할 수 있어!"),
                Text("아이템을 바꾸고 싶다면 *Shift키*를 누르면 될거야."),
                Text("문은 잠겨져 있으니 열쇠를 찾아서 *E키*를 누르면 돼!"),
                Text("잠긴 블록도 문과 같은 방법으로 열 수 있어!"),
                Text("그럼 즐거운 여행되길 바래 ㅎㅎ")
            ],
            self.sign.width
        )
        
        self.NPCs = [self.emilia]

        # 적
        self.enemies = []

        # 장애물
        self.obstacles = []
        
        # 배경
        self.background = Texture("assets/images/background_main.png", (0, 0), 1, repeat_x=2, fit=True)
        self.floor = Texture("assets/images/grass.png", (0, 470), 0.5, repeat_x=2)

        # 아이템
        self.heal = Texture("assets/images/item_heal.png", (800, 420), 0.4, name="heal")
        self.key = Texture("assets/images/item_key.png", (850, 430), 0.4, name="key")

        self.items = [self.heal, self.key]

        # 벽 & 문
        self.ground1_left = Texture("assets/images/ground_end_l.png", (1500, 335))
        self.ground1_right = Texture("assets/images/ground_end_r.png", (1700, 335))
        self.tile1_left = Texture("assets/images/tile_end_l.png", (1500, 195))
        self.tile2_right = Texture("assets/images/tile_end_r.png", (1700, 195))
        self.door = Texture("assets/images/object_door_closed.png", (1580, 335), 0.4)
        self.door_closed = True
        self.door_locked = True

        self.others_front = [self.ground1_left, self.ground1_right, self.tile1_left, self.tile2_right]
        self.others_back = [self.door]

    def process_item_pickup_event(self):
        """아이템 줍기 관련 이벤트를 처리합니다."""
        positions = {  # 인벤토리에 렌더링될 각 아이템의 위치
            "heal": (15, 12),
            "key": (20, 22)
        }

        for item in self.items:
            if item.is_bound(10, 50):  # 플레이어가 아이템을 주울 경우 아이템 삭제
                index = self.items.index(item)  # 현재 아이템의 아이템 배열 index 가져오기
                self.items.pop(index)  # 현재 아이템을 아이템 배열에서 삭제

                position = positions[item.name]  # 인벤토리에 렌더링될 현재 아이템 위치 가져오기
                item.set_pos(position[0], position[1])  # 상대좌표

                # 인벤토리에 아이템 추가
                Inventory.items[item.name] = item
                Inventory.keys.append(item.name)
                Inventory.keys_index = len(Inventory.keys) - 1

                SFX.ITEM_PICKUP.play()  # 아이템 줍는 효과음 재생

    def process_item_use_event(self, item: Texture):
        """
        아이템 사용 관련 이벤트를 처리합니다.
        :param item: 현재 쓸 아이템의 텍스쳐
        """
        match item.name:
            case "heal":
                self.player.healed = True

            case "key":
                self.door_locked = False

    def process_door_event(self):
        """문 관련 이벤트를 처리합니다."""
        from maps.map_manager import MapManager

        if self.door.is_bound(10, 50) and not self.door_locked:  # 문의 범위 안에 있고 잠겨있지 않은 경우
            MapManager.apply("training")  # 훈련장 맵으로 이동
            SFX.MAP.play()  # 맵 이동 효과음 재생

    def render(self, frame_count: int):
        """
        맵을 렌더링합니다.
        :param frame_count: 1초 당 누적되는 프레임 렌더링하는 개수 (범위: 0~10)
        """
        self.process_door_event()
        super().render(frame_count)