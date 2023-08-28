from maps import Map

from characters.player import Player
from characters.enemy import Enemy
from characters.texture import Texture

from components.events.grace_period import GracePeriod
from components.events.text import TextEvent

from components.text import Text
from components.text.text_collection import TextCollection

from components.sprites.sprite import Sprite
from components.sprites.sprite_handler import SpriteHandler
from components.sprites.sprite_collection import SpriteCollection

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
                Text("나는 에밀리아야."),
                Text("*J키*는 #기본공격#이야!"),
                Text("그럼 즐거운 여행되길 바래!")
            ],
            self.sign.width
        )
        
        self.NPCs = [self.emilia]

        # 적
        self.enemy = Enemy("assets/images/chr_raon.png", (1000, 387), 0.4)
        self.enemies = [self.enemy]

        for enemy in self.enemies:
            enemy.grace_period = GracePeriod(1500)
            enemy.hp = 2

        # 장애물
        self.spike = Player.get_from_sprite(SpriteCollection({
            "default": SpriteHandler(
                Sprite(
                    "assets/images/object_spike_default.png", 17, 1, size=(155, 100)
                )
            )
        },
        "default",
        position=(800, 435),
        scale=0.4))

        self.spike2 = Player.get_from_sprite(SpriteCollection({
            "default": SpriteHandler(
                Sprite(
                    "assets/images/object_spike_default.png", 17, 1, size=(155, 100)
                )
            )
        },
        "default",
        position=(850, 435),
        scale=0.4))

        self.obstacles = [self.spike, self.spike2] 
        
        # 배경
        self.background = Texture("assets/images/background_main.png", (0, 0), 1, repeat_x=2, fit=True)
        self.floor = Texture("assets/images/grass.png", (0, 470), 0.5, repeat_x=2)