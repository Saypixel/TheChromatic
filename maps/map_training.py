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

class MapTraining(Map):
    def __init__(self, player: Player, sign):
        super(Map, self).__init__()

        self.player = player

        # NPC
        self.sign = sign

        self.emilia = Player("assets/images/chr_emilia.png", (400, 193), 0.4)  # 에밀리아
        self.emilia.dialog = TextCollection(
            [
                Text("#이 쪽으로 잘 왔구나!#"),
                Text("여기는 훈련장이야."),
                Text("쭉 가면 적이 출몰할거야!"),
                Text("적은 *J키*로 공격할 수 있으니 참고하라구!")
            ],
            self.sign.width
        )

        self.NPCs = [self.emilia]

        self.obstacles = []
        self.enemies = []

        # 배경
        self.background = Texture("assets/images/background.png", (0, 0), 1, repeat_x=2, fit=True)
        self.floor = Texture("assets/images/ground_temp.png", (0, 0), repeat_x=2, fit=True)