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

        noise_image = pygame.Surface((cls.width, cls.height), pygame.SRCALPHA, 32)  # 노이즈를 저장하기 위한 이미지 새로 생성

        noise_np = np.zeros(cls.width * cls.height * 3)  # 배열의 길이가 width * height * 3인 배열 생성
        noise_np = noise_np.reshape((cls.width, cls.height, 3)) # 1차원 배열에서 3차원 배열로 재할당

        for i in range(0, cls.width):
            noise_np[i] += CONFIG.random.randint(0, 50 * cls.level)  # 노이즈 이미지를 생성하기 위함, 이 때 x좌표만 적용하는 이유는 렉 걸리지 않기 위해서

        pygame.surfarray.blit_array(noise_image, noise_np)  # numpy 배열을 pygame.Surface로 변환

        return noise_image.convert()
    
    @classmethod
    def blend(cls, noise: pygame.Surface, background: pygame.Surface) -> pygame.Surface:
        """
        노이즈 이미지와 배경 이미지를 합성합니다.
        :noise: 노이즈 이미지
        :background: 기존 배경 이미지
        :return: 합성된 새로운 이미지
        """

        surface = background.copy().convert()  # 기존 배경 이미지 복사
        surface.blit(noise, (0, 0), None, pygame.BLEND_RGBA_SUB)  # SUBTRACT 모드로 이미지 합성
        return surface