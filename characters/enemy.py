import pygame
from threading import Timer

from characters.player import Player
from characters.texture import Texture

from components.config import CONFIG, debug
from components.sprites.sprite import Sprite

class Enemy(Player):
    is_attacking = False
    '''적이 플레이어를 공격하고 있는가?'''

    def follow_player(self, obstacles: list[Texture]):
        """적이 플레이어를 따라가도록 합니다."""
        if self.hp == 0:
            return  # 사망

        velocity_x = 0.7

        if self.x > CONFIG.player_x:
            velocity_x *= -1

        if self.x != CONFIG.player_x and abs(velocity_x * 10) <= abs(CONFIG.player_x - self.x):
            self.move_x(velocity_x)

        for obstacle in obstacles:  # 장애물을 피해 다님
            if self.is_bound(50, 70, obstacle.x, obstacle.y):  # 주변에 장애물이 있다면
                self.move_y(14)  # 점프