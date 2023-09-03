from characters.texture import Texture

class Inventory:
    """인벤토리에 들어있는 아이템 관리"""

    image = Texture("assets/images/inventory.png", (0, 30), 0.8)
    """렌더링할 인벤토리 텍스쳐"""

    keys: list[str] = []
    """현재 가지고 있는 아이템 이름 배열"""
    
    keys_index = -1
    """현재 들고 있는 아이템"""

    items: dict[str, Texture] = {}
    """인벤토리에 들어있는 아이템들의 텍스쳐"""

    @classmethod
    def pop_item(cls) -> Texture:
        """
        현재 들고 있는 아이템을 배열에서 삭제하고 가져옵니다.
        :return: 현재 들고 있는 아이템
        """
        if cls.keys_index >= 0:  # 현재 들고 있는 아이템이 있는 경우
            status = cls.keys[cls.keys_index]  # 현재 들고 있는 아이템 이름
            item = cls.items[status]  # 현재 들고 있는 아이템
            index_prev = cls.keys_index  # 삭제하기 전 현재 들고 있는 아이템 배열의 index

            # 현재 들고 있는 아이템을 배열에서 삭제하고 변수 갱신
            cls.keys_index -= 1 if len(cls.keys) == 1 or cls.keys_index + 1 == len(cls.keys) else 0
            cls.keys.pop(index_prev)
            cls.items.pop(status)

            return item
        
        return None
        
    @classmethod
    def shift_item(cls) -> bool:
        """
        들 아이템을 변경합니다.
        :return: 들 아이템을 변경할 수 있는지의 여부
        """
        available = len(cls.keys) >= 2  # 아이템이 인벤토리에 들어있고 2가지 이상인 경우

        if available:
            cls.keys_index += 1  # 현재 들고 있는 아이템 갱신

            # 배열 길이 범위를 벗어난 경우
            if cls.keys_index >= len(cls.keys):
                cls.keys_index = 0  # index 초기화

        return available

    @classmethod
    def render_item(cls):
        """현재 들고 있는 아이템을 인벤토리에 렌더링합니다."""
        if cls.keys_index >= 0:  # 가지고 있는 아이템이 존재하는 경우
            status = cls.keys[cls.keys_index]  # 현재 들고 있는 아이템 이름
            cls.items[status].render(cls.image.image, False)  # 상대좌표로 인한 최적화 중지

    @classmethod
    def reset(cls):
        """Inventory 클래스 변수를 초기화합니다."""
        cls.keys = []
        cls.keys_index = -1
        cls.items = {}