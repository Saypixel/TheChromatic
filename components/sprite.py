import pygame
from components.config import debug

class Sprite(pygame.sprite.Sprite):
    images: list[pygame.Surface]
    rect: pygame.Rect
    position: tuple
    size: tuple

    flipped = False

    def __init__(self, path: str, columns: int, rows: int, position: tuple, size: tuple, start = (0, 0), scale: float = 1.0):

        super(Sprite, self).__init__()

        image = pygame.image.load(path)
        images = self.strip_from_sheet(image, start, size, columns, rows)

        # 스케일링
        scale_x = size[0] * scale
        scale_y = size[1] * scale

        self.position = position
        self.size = (scale_x, scale_y)
        self.images = [pygame.transform.scale(image, self.size) for image in images]
        self.rect = (position, self.size)

        # 캐릭터의 첫번째 이미지 
        self.index = 0
        self.image = self.images[self.index]  # 'image' is the current image of the animation.


    def update(self, start = 0):
        # update를 통해 캐릭터의 이미지가 계속 반복해서 나타나도록 한다. 
        self.index += 1

        if self.index >= len(self.images):
            self.index = start

        self.image = self.images[self.index]


    def add_image(self, path: str):
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, self.size)

        self.images.append(image)


    def flip(self):
        self.images = [pygame.transform.flip(image, True, False) for image in self.images]
        self.image = self.images[self.index]

        self.flipped = not self.flipped


    def strip_from_sheet(self, sheet: pygame.Surface, start: tuple, size: tuple, columns: int, rows: int = 1) -> list[pygame.Surface]:
        """
        주어진 시작 위치에서 각 프레임 분할
        """
        frames = []

        for j in range(rows):
            for i in range(columns):
                location = (start[0] + size[0] * i, start[1] + size[1] * j)
                frames.append(sheet.subsurface(pygame.Rect(location, size)))
                
        return frames