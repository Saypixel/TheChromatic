from .sprite_handler import SpriteHandler


class SpriteCollection:
    """다중 스프라이트 지원"""

    sprites: dict[str, SpriteHandler]
    """각 스프라이트를 관리하고 및 저장할 다중 스프라이트"""

    status: str
    """현재 렌더링할 스프라이트 기본 상태 (sprites key)"""

    position: tuple
    """각 스프라이트가 위치할 절대좌표"""

    size: tuple
    """각 스프라이트의 크기"""

    alpha = 255
    """전체 스프라이트의 투명도"""

    def __init__(
        self,
        sprites: dict[str, SpriteHandler],
        status: str,
        position: tuple,
        size: tuple = (0, 0),
        scale: float = 1.0,
    ):
        """
        SpriteCollection 클래스를 생성합니다.
        :param sprites: 각 스프라이트가 들어있는 다중 스프라이트
        :param status: 현재 렌더링할 스프라이트 사전 Key
        :param position: 스프라이트가 위치할 절대좌표
        :param size: 스프라이트의 크기 (너비, 높이), 명시되지 않은 경우 기본 스프라이트의 크기로 설정
        :param scale: 스프라이트의 상대크기
        """

        # 변수 초기화
        self.sprites = sprites
        self.status = status
        self.position = position

        self.set_pos(position)  # 각 스프라이트가 위치할 좌표 지정

        if scale != 1.0:
            self.set_scale(scale)  # 스케일링

        if size[0] == 0 and size[1] == 0:  # 프로그래머가 크기를 명시하지 않았으므로 기본 스프라이트 크기로 설정
            self.size = self.get_sprite_handler().sprite.size
        else:
            scaled_x = size[0] * scale
            scaled_y = size[1] * scale

            self.size = (scaled_x, scaled_y)  # 크기 지정

    def set_pos(self, position: tuple):
        """
        각 스프라이트의 좌표를 지정합니다.
        :param position: 위치할 절대좌표
        """
        for key in self.sprites:
            self.sprites[key].sprite.set_pos(position)  # 각 스프라이트 좌표 지정

    def set_scale(self, scale: float):
        """
        각 스프라이트의 상대크기를 지정합니다.
        :param scale: 상대크기 (범위: 0 이상, 기본: 1.0)
        """
        for key in self.sprites:
            self.sprites[key].sprite.set_scale(scale)  # 각 스프라이트 상대크기 지정

    def get_sprite_handler(self) -> SpriteHandler:
        """
        현재 렌더링할 스프라이트를 가져옵니다.
        :return: 현재 렌더링할 스프라이트, status 변수에 따라 가져올 스프라이트가 달라짐
        """
        return self.sprites[self.status]
    
    def get_alpha(self) -> int:
        """
        전체 스프라이트의 투명도를 가져옵니다.
        :return: 스프라이트의 투명도
        """
        return self.alpha

    def set_alpha(self, value: int):
        """
        전체 스프라이트의 투명도를 설정합니다.
        :param value: 투명도값 (범위: 0 ~ 255)
        """
        self.alpha = value

        for key in self.sprites:
            self.sprites[key].sprite.set_alpha(value)  # 각 스프라이트 투명도 설정