import pygame

from characters import Character

from components.config import CONST, CONFIG, debug
from components.text.text_collection import TextCollection
from components.events.text import TextEvent
from components.sprite import Sprite

class Player(Character):
    def move(self, velocity: float):
        # 윈도우 내부에 위치해 있는 경우
        if (velocity > 0 and self.x <= 0) or (velocity < 0 and self.x >= CONST.SCREEN_SIZE[0]) or (0 <= self.x <= CONST.SCREEN_SIZE[0]):
            self.velocity = velocity

            self.x += 10 * velocity

            if self.is_playable:
                CONFIG.player_x = self.x
                CONFIG.player_y = self.y

    
    @classmethod
    def get_from_sprite(cls, sprite: Sprite, is_playable = False) -> 'Player':
        """
        캐릭터 클래스 생성

        :param sprite: 캐릭터 스프라이트
        """
        chr = Player('', (0, 0))
        chr.sprite = sprite
        chr.sprite_group = pygame.sprite.Group(sprite)

        chr.x = sprite.position[0]
        chr.y = sprite.position[1]
        chr.width = sprite.size[0]
        chr.height = sprite.size[1]

        if is_playable:
            CONFIG.player_width = chr.width
            CONFIG.player_height = chr.height

        chr.is_playable = is_playable

        return chr