from .sprite_handler import SpriteHandler

class SpriteCollection:
    """다중 스프라이트 지원"""
    sprites: dict[str, SpriteHandler]

    status: str
    '''현재 상태 (sprites key)'''

    position: tuple
    '''위치'''

    size: tuple
    '''크기'''

    def __init__(self, sprites: dict[str, SpriteHandler], status: str, position: tuple, size: tuple):
        self.sprites = sprites
        self.status = status
        self.position = position

        self.set_pos(position)
        self.size = size

    def set_pos(self, position: tuple):
        for key in self.sprites:
            self.sprites[key].sprite.set_pos(position)

    def get_sprite_handler(self) -> SpriteHandler:
        return self.sprites[self.status]
    
    def set_alpha(self, value: int):
        """
        전체 스프라이트의 알파값 수정
        :param value: 0~255
        """

        for key in self.sprites:
            self.sprites[key].sprite.set_alpha(value)