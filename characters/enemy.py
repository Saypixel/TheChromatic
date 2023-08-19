import pygame
from threading import Timer

from characters.player import Player
from characters.texture import Texture

from components.config import CONFIG, CONST, debug
from components.sprites.sprite import Sprite

class Enemy(Player):
    is_attacking = False
    '''적이 플레이어를 공격하고 있는가?'''

    def follow_player(self, obstacles: list[Texture]):
        """적이 플레이어를 따라가도록 합니다."""
        if self.hp == 0:
            return  # 사망
        
        if CONFIG.camera_x <= self.x <= (CONFIG.camera_x + CONST.SCREEN_SIZE[0] / 1.05):  # 플레이어 화면 범위에 있는 경우
            velocity_x = 0.7

            if self.x > CONFIG.player_x:
                velocity_x *= -1

            if self.x != CONFIG.player_x and abs(velocity_x * 10) <= abs(CONFIG.player_x - self.x):
                self.move_x(velocity_x)

            for obstacle in obstacles:  # 장애물을 피해 다님
                if obstacle.is_bound(5, 40, self.x, self.y, self.width, self.height):  # 주변에 장애물이 있다면
                    self.move_y(13)  # 점프