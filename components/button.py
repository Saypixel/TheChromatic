import pygame
from components.config import CONFIG

class Button:
    image: pygame.Surface
    """버튼 이미지"""

    x_pos: int
    y_pos: int
    """버튼 좌표"""

    font: pygame.font.Font
    """버튼 텍스트 폰트"""

    base_color: str
    """버튼 텍스트 기본 색상"""

    hovering_color: str
    """버튼에 마우스 포인터가 올라갔을 때 텍스트 색상"""

    text_input: str
    """버튼 텍스트 (문자열)"""

    text: pygame.Surface = None
    """렌더링된 버튼 텍스트"""

    def __init__(
        self,
        image: pygame.Surface,
        pos: tuple,
        base_color: str = "",
        hovering_color: str = "",
        text_input="",
        text_offset=(0, 0),
        font: pygame.font.Font = None,
        camera_calibrated = True
    ):
        """
        버튼 클래스를 생성합니다.
        :param image: 버튼 이미지
        :param pos: 버튼이 위치할 절대좌표
        :param base_color: 버튼 텍스트의 기본 색상 ex) #ff00ff
        :param hovering_color: 버튼에 마우스 포인터가 올라갔을 때의 텍스트 색상 ex) #00ffff
        :param text_input: 버튼 텍스트 (문자열)
        :param text_offset: 버튼 텍스트의 위치 오프셋
        :param font: 버튼 텍스트의 폰트
        :param camera_calibrated: 해당 버튼 좌표에 카메라 좌표가 보정될건지 여부
        """
        self.image = image
        self.x_pos = pos[0] + CONFIG.camera_x if camera_calibrated else 0  # 카메라 보정 여부 (X 좌표)
        self.y_pos = pos[1] + CONFIG.camera_y if camera_calibrated else 0  # 카메라 보정 여부 (Y 좌표)
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input

        if self.font is not None:  # 폰트가 지정되어있는 경우 안티 에일리어싱 없이 폰트 렌더링 (픽셀 게임이므로 안티 에일리어싱 X)
            self.text = self.font.render(self.text_input, False, self.base_color)

        if self.image is None:  # 이미지가 지정되어 있지 않은 경우 텍스트가 이미지로 지정됨
            self.image = self.text

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))  # 이미지 좌표 & 크기 (Rect) 설정

        if self.text is not None:  # 텍스트가 지정되어 있는 경우 텍스트 좌표 & 크기 (Rect) 설정
            self.text_rect = self.text.get_rect(
                center=(self.x_pos + text_offset[0], self.y_pos + text_offset[1])  # 오프셋만큼 좌표 이동
            )

    def update(self, screen: pygame.Surface):
        """
        버튼을 화면에 렌더링합니다.
        :param screen: 렌더링할 화면
        """
        if self.image is not None:  # 이미지가 지정되어 있는 경우 이미지 렌더링
            screen.blit(self.image, self.rect)
        if self.text is not None:  # 텍스트가 지정되어 있는 경우 텍스트 렌더링
            screen.blit(self.text, self.text_rect)

    def check_for_input(self, position: tuple) -> bool:
        """
        버튼이 클릭됐는지 확인합니다.
        :param position: 마우스 커서 좌표
        :return: 버튼이 클릭됐는지의 여부
        """
        # 마우스 커서 좌표가 버튼 Rect 범위에 해당하는지 확인
        is_x = position[0] in range(self.rect.left, self.rect.right)
        is_y = position[1] in range(self.rect.top, self.rect.bottom)

        return is_x and is_y

    def change_color(self, position: tuple):
        """
        버튼에 마우스 포인터가 올라가면 색상을 바꿉니다.
        :param position: 마우스 커서 좌표
        """
        # 마우스 커서 좌표가 버튼 Rect 범위에 해당하는지 확인
        is_x = position[0] in range(self.rect.left, self.rect.right)
        is_y = position[1] in range(self.rect.top, self.rect.bottom)

        color = self.hovering_color if is_x and is_y else self.base_color  # 버튼에 마우스 포인터가 올라가면 색상 변경

        if self.text is not None:
            self.text = self.font.render(self.text_input, False, color)  # 해상 색상으로 안티 에일리어싱 없이 폰트 렌더링 (픽셀 게임이므로 안티 에일리어싱 X)

    def change_image(self, image: pygame.Surface):
        """
        버튼 이미지를 변경합니다.
        :param image: 변경할 버튼 이미지
        """
        self.image = image
        self.rect = image.get_rect(center=(self.x_pos, self.y_pos))  # 이미지 좌표 & 크기 (Rect) 설정
