import pygame
from components.config import debug


class Sprite(pygame.sprite.Sprite):
    """단일 애니메이션 (스프라이트)를 구현하기 위한 클래스"""

    images: list[pygame.Surface]
    """단일 이미지가 분할된 각 프레임 배열"""

    length: int
    """images 배열 길이"""

    rect: pygame.Rect
    """현재 이미지의 위치와 크기 (Rect)"""

    position: tuple
    """스프라이트가 위치할 절대좌표"""

    size: tuple
    """스프라이트 크기"""

    flipped = False
    """스프라이트 이미지가 반전되어있는가?"""

    alpha = 255
    """스프라이트 투명도"""

    def __init__(
        self,
        path: str,
        columns: int,
        rows: int,
        size: tuple,
        start=(0, 0),
        position=(0, 0),
        scale: float = 1.0,
    ):
        """
        Sprite 클래스를 생성합니다.
        :param path: 이미지의 경로
        :param columns: 스프라이트를 분할할 가로줄
        :param rows: 스프라이트를 분할할 세로줄
        :param size: 스프라이트가 분할된 각 프레임의 크기
        :param start: 분할이 시작될 처음 위치
        :param position: 스프라이트가 위치할 절대좌표
        :param scale: 스프라이트의 상대크기
        """
        super(Sprite, self).__init__()  # 상속된 클래스 초기화

        # 이미지를 불러온 후 스프라이트 분할
        image = pygame.image.load(path)
        images = self.strip_from_sheet(image, start, size, columns, rows)

        # 스케일링
        scale_x = size[0] * scale
        scale_y = size[1] * scale

        # 변수 초기화
        self.position = position
        self.size = (scale_x, scale_y)
        self.images = [pygame.transform.scale(image, self.size) for image in images]  # 크기에 맞게 스케일링
        self.length = len(self.images)
        self.rect = (position, self.size)

        # 캐릭터의 첫번째 이미지
        self.index = 0
        self.image = self.images[self.index]  # 애니메이션의 현재 이미지

    def update(self, added_index = 1, init = False):
        """
        캐릭터의 이미지가 계속 반복해서 나타나도록 하여 애니메이션의 느낌을 주도록 합니다.
        :param: added_index: 스프라이트를 업데이트할 때 어느만큼 업데이트할건지 지정하는 변수, 값에 따라 일부 프레임이 스킵될 수 있음
        :init: index를 초기화할건지의 여부입니다.
        """
        if init:
            self.index = 0

        self.index += added_index  # index 업데이트

        if self.index >= len(self.images):  # index가 범위를 벗어난 경우
            self.index = 0  # index 초기화

        self.image = self.images[self.index]  # 스프라이트 업데이트

    def flip(self):
        """스프라이트를 좌우반전시킵니다."""
        self.images = [pygame.transform.flip(image, True, False) for image in self.images]  # 각 프레임 좌우반전
        self.image = self.images[self.index]  # 좌우반전된 프레임으로 현재 프레임 업데이트하여 동기화

        self.flipped = not self.flipped  # 변수 설정

    def set_pos(self, position: tuple):
        """
        스프라이트의 좌표를 설정합니다.
        :param position: 위치할 절대좌표
        """
        self.position = position
        self.rect = (position, self.size)

    def get_alpha(self) -> int:
        """
        스프라이트의 투명도를 가져옵니다.
        :return: 투명도 값
        """
        return self.alpha

    def set_alpha(self, alpha: int):
        """
        스프라이트의 투명도를 설정합니다.
        :param alpha: 투명도 값 (범위: 0 ~ 255)
        """
        self.alpha = alpha  # 값 설정
        
        for image in self.images:
            image.set_alpha(alpha)  # 각 프레임마다 투명도 설정

    def set_scale(self, scale: float):
        """
        스프라이트의 상대크기를 설정합니다.
        :param scale: 상대크기 (범위 : 0 이상, 기본: 1.0)
        """

        # 스케일링하여 크기 설정
        scale_x = self.size[0] * scale
        scale_y = self.size[1] * scale

        self.size = (scale_x, scale_y)
        self.images = [pygame.transform.scale(image, self.size) for image in self.images]  # 크기에 맞게 스케일링
        self.length = len(self.images)
        self.rect = (self.position, self.size)

        # 캐릭터의 현재 이미지 (동기화)
        self.image = self.images[self.index]  # 애니메이션의 현재 이미지

    def strip_from_sheet(
        self,
        sheet: pygame.Surface,
        start: tuple,
        size: tuple,
        columns: int,
        rows: int = 1,
    ) -> list[pygame.Surface]:
        """
        주어진 시작 위치에서 각 프레임 분할합니다.
        :param sheet: 분할할 이미지
        :param start: 시작할 오프셋 위치
        :param size: 분할할 각 이미지 크기
        :param columns: 가로줄
        :param rows: 세로줄
        :return: 분할된 이미지
        """
        frames = []

        for y in range(rows):  # 세로줄
            for x in range(columns):  # 가로줄
                location = (start[0] + size[0] * x, start[1] + size[1] * y)
                frame = sheet.subsurface(pygame.Rect(location, size))  # 지정된 위치와 크기만큼 이미지 분할
                frames.append(frame)

        return frames
