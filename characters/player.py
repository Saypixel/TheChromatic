import pygame

from characters import Character

from components.config import CONST, CONFIG, debug
from components.text.text_collection import TextCollection
from components.events.text import TextEvent

from components.sprites.sprite_collection import SpriteCollection
from components.sprites.sprite_handler import SpriteHandler
from components.sprites.sprite import Sprite

class Player(Character):
    def move(self, velocity_x: float, velocity_y: float = 0):
        # 윈도우 내부에 위치해 있는 경우
        if (velocity_x > 0 and self.x <= 0) or (velocity_x < 0 and self.x + self.width >= CONST.SCREEN_SIZE[0]) or (0 <= self.x <= CONST.SCREEN_SIZE[0]):
            self.velocity_x = velocity_x

            self.x += 10 * velocity_x

            if self.is_playable:
                CONFIG.player_x = self.x
                CONFIG.player_y = self.y

        self.velocity_y = velocity_y
        self.y -= velocity_y
    
    @classmethod
    def get_from_sprite(cls, sprites: SpriteCollection, is_playable = False) -> 'Player':
        """
        캐릭터 클래스 생성

        :param sprite: 캐릭터 스프라이트
        """
        chr = Player('', (0, 0))
        chr.sprites = sprites

        chr.x = sprites.position[0]
        chr.y = sprites.position[1]
        chr.width = sprites.size[0]
        chr.height = sprites.size[1]

        if is_playable:
            CONFIG.player_width = chr.width
            CONFIG.player_height = chr.height

        chr.is_playable = is_playable

        return chr