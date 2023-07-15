import pygame.mixer as mixer


class SFX(object):
    INTRO: mixer.Sound

    @classmethod
    def init(cls):
        cls.INTRO = mixer.Sound('assets/audio/sfx_intro.ogg')