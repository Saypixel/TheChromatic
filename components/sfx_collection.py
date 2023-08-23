import pygame.mixer as mixer


class SFX(object):
    INTRO: mixer.Sound
    UNMUTED: mixer.Sound
    ATTACKED: mixer.Sound

    sounds: list[mixer.Sound]
    """효과음 배열, 음량 조절하는 데 사용"""

    muted = False
    """음소거 되어있는가?"""

    volume: float = 1.0
    """음량 (기본: 1.0, 범위: 0.0 ~ 1.0)"""

    @classmethod
    def init(cls):
        """SFX 클래스를 초기화합니다."""
        cls.INTRO = mixer.Sound("assets/audio/sfx_intro.ogg")
        cls.UNMUTED = mixer.Sound("assets/audio/sfx_unmuted.ogg")

        cls.ATTACK = mixer.Sound("assets/audio/sfx_attack.ogg")
        cls.ATTACKED = mixer.Sound("assets/audio/sfx_attacked.ogg")
        cls.DEAD = mixer.Sound("assets/audio/sfx_dead.ogg")

        cls.ENEMY_ATTACKED = mixer.Sound("assets/audio/sfx_enemy_attacked.ogg")

        cls.sounds = [cls.INTRO, cls.UNMUTED,
                      cls.ATTACK, cls.ATTACKED, cls.DEAD,
                      cls.ENEMY_ATTACKED]

    @classmethod
    def control_mute(cls):
        """음소거 되어있으면 해제하고, 되어있지 않으면 음소거합니다."""
        cls.muted = not cls.muted
        cls.volume = 0.0 if cls.muted else 1.0  # 음소거면 음량을 0으로 조절

        cls.set_volume(cls.volume)  # 음량 저장

    @classmethod
    def set_volume(cls, volume: float):
        """
        음량을 설정합니다.
        :param volume: 음량 (범위: 0.0 ~ 1.0)
        """
        volume_rounded = round(volume, 1)  # 소수점 계산 문제 방지

        if volume_rounded == 0.0:  # 음소거
            cls.muted = True
        else:
            cls.muted = False  # 음소거 해제

        cls.volume = volume  # 음량 설정

        mixer.music.set_volume(volume)  # 음악 음량 설정

        for sound in cls.sounds:
            sound.set_volume(volume)  # 효과음 음량 설정
