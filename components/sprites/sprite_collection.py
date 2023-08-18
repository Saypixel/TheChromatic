from .sprite_handler import SpriteHandler


class SpriteCollection:
    """다중 스프라이트 지원"""

    sprites: dict[str, SpriteHandler]

    status: str
    """현재 상태 (sprites key)"""

    position: tuple
    """위치"""

    size: tuple
    """크기"""

    alpha = 255
    """투명도"""

    def __init__(
        self,
        sprites: dict[str, SpriteHandler],
        status: str,
        position: tuple,
        size: tuple = (0, 0),
        scale: float = 1.0,
    ):
        self.sprites = sprites
        self.status = status
        self.position = position

        self.set_pos(position)

        if scale != 1.0:
            self.set_scale(scale)

        if size[0] == 0 and size[1] == 0:  # default
            self.size = list(sprites.values())[0].sprite.size
        else:
            scaled_x = size[0] * scale
            scaled_y = size[1] * scale

            self.size = (scaled_x, scaled_y)

    def set_pos(self, position: tuple):
        for key in self.sprites:
            self.sprites[key].sprite.set_pos(position)

    def set_scale(self, scale: float):
        for key in self.sprites:
            self.sprites[key].sprite.set_scale(scale)

    def get_sprite_handler(self) -> SpriteHandler:
        return self.sprites[self.status]
    
    def get_alpha(self) -> int:
        return self.alpha

    def set_alpha(self, value: int):
        """
        전체 스프라이트의 알파값 수정
        :param value: 0~255
        """
        self.alpha = value

        for key in self.sprites:
            self.sprites[key].sprite.set_alpha(value)