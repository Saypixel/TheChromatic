import pygame
import numpy as np

import time

from components.config import CONFIG, debug

class NoiseEvent:
    """노이즈 생성 및 관리 클래스"""

    level = 1.0
    """노이즈 강도 (1 ~ 3)"""

    width = 960
    """노이즈 이미지 너비 (기본값: 960)"""

    height = 540
    """노이즈 이미지 높이 (기본값: 540)"""

    @classmethod
    def make_noise(cls) -> pygame.Surface:
        """
        노이즈 이미지를 생성합니다.
        :return: 노이즈 이미지
        """

        noise = pygame.Surface((cls.width, cls.height), pygame.SRCALPHA, 32)
        #noise2 = np.random.normal(0, 0.3, (cls.width, cls.height, 3))

        x = np.zeros(cls.width * cls.height * 3)
        x = x.reshape((cls.width, cls.height, 3)) # flat view

        for ii in range(cls.width):
            x[ii] += CONFIG.random.randint(0, 50)

        pygame.surfarray.blit_array(noise, x)
        return noise.convert()
    
    @classmethod
    def multiply(cls, noise: pygame.Surface, background: pygame.Surface) -> pygame.Surface:
        """
        노이즈 이미지와 배경 이미지를 곱합성합니다.
        :noise: 노이즈 이미지
        :background: 기존 배경 이미지
        :return: 곱합성된 새로운 이미지
        """

        surface = background.copy().convert()
        surface.blit(noise, (0, 0), None, pygame.BLEND_RGBA_SUB)
        return surface