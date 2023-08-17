import pygame

from characters import Character

from components.config import CONST, CONFIG, debug
from components.text.text_collection import TextCollection
from components.events.text import TextEvent

from components.sprites.sprite_collection import SpriteCollection
from components.sprites.sprite_handler import SpriteHandler
from components.sprites.sprite import Sprite

class Player(Character):
    def move_x(self, velocity: float):
        # 윈도우 내부에 위치해 있는 경우
        if round(velocity, 3) != 0.0:
            if (velocity > 0 and self.x <= 0) or (velocity < 0 and self.x + self.width >= CONST.SCREEN_SIZE[0]) or (0 <= self.x <= CONST.SCREEN_SIZE[0]):
                multiplied = 1 if not self.is_air else 0.7  # 공중에 떠 있으면 패널티 부여

                self.velocity_x = velocity
                self.x += 10 * velocity * multiplied

        if self.is_playable:
            CONFIG.player_x = self.x

    def move_y(self, velocity: float):
        if round(velocity, 3) != 0.0:
            self.velocity_y = velocity
            self.y -= velocity

        if self.is_playable:
            CONFIG.player_y = self.y
    
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