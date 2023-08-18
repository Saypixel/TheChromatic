import pygame.mixer as mixer


class SFX(object):
    INTRO: mixer.Sound
    UNMUTED: mixer.Sound
    ATTACKED: mixer.Sound

    sounds: list[mixer.Sound]

    muted = False
    volume: float = 1.0

    @classmethod
    def init(cls):
        cls.INTRO = mixer.Sound("assets/audio/sfx_intro.ogg")
        cls.UNMUTED = mixer.Sound("assets/audio/sfx_unmuted.ogg")
        cls.ATTACKED = mixer.Sound("assets/audio/sfx_attacked.ogg")

        cls.sounds = [cls.INTRO, cls.UNMUTED, cls.ATTACKED]

    @classmethod
    def control_mute(cls):
        cls.muted = not cls.muted
        cls.volume = 0.0 if cls.muted else 1.0

        cls.set_volume(cls.volume)

    @classmethod
    def set_volume(cls, volume: float):
        volume_rounded = round(volume, 1)  # 소수점 계산 문제 방지

        if volume_rounded == 0.0:
            cls.muted = True
        else:
            cls.muted = False

        cls.volume = volume

        mixer.music.set_volume(volume)

        for sound in cls.sounds:
            sound.set_volume(volume)
