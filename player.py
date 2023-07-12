import pygame

from const import CONST


class Player:
    image: pygame.Surface | pygame.SurfaceType
    pos_x: int
    pos_y: int

    def __init__(self, path: str, scale: tuple, position: tuple):
        '''
        캐릭터 클래스 생성

        :param path: 캐릭터 이미지 경로
        :param scale: 캐릭터 크기 ex) (100, 100)
        :param position: 캐릭터가 위치한 절대좌표
        '''
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, scale)

        self.pos_x = position[0]
        self.pos_y = position[1]

    def get_pos(self) -> tuple:
        return (self.pos_x, self.pos_y)

    def move(self, velocity: float):
        '''
        캐릭터 움직임

        :param velocity: 속도 (주로 1, -1 이용)
        '''
        # 윈도우 내부에 위치해 있는 경우
        if (velocity > 0 and self.pos_x <= 0) or (velocity < 0 and self.pos_x >= CONST.SCREEN_SIZE[0]) or (0 <= self.pos_x <= CONST.SCREEN_SIZE[0]):
            self.pos_x += 10 * velocity
