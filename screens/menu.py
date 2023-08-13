import pygame
from pygame import mixer

from components.button import Button
from components.config import CONFIG, CONST, Fonts
from components.events import process
from components.font import Font
from screens.ingame import update_ingame


def update_menu():
    def process_menu(event: pygame.event.Event):
        """인게임 이벤트 처리용 (process() child 함수)"""
        match event.type:
            case pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 시
                if button_menu_play.check_for_input(menu_mouse_pos):
                    mixer.music.stop()
                    update_ingame()
                    return

    mixer.music.load('assets/audio/bg_daily.ogg')
    mixer.music.set_volume(0.7)
    mixer.music.play(-1)

    while CONFIG.is_running:
        CONFIG.clock.tick(CONFIG.FPS)
        CONFIG.surface.fill(CONST.COL_MAIN_BACKGROUND_BLUE)

        menu_mouse_pos = CONFIG.get_mouse_pos()
        menu_title = pygame.image.load('assets/images/menu_title.png')
        menu_title = pygame.transform.scale(menu_title, (242, 96))
        # menu_title = Font(Fonts.TITLE1, 80).render('The Chromatic', True, CONST.COL_WHITE)
        rect_menu = menu_title.get_rect(center=(320, 100))
        button_menu_play_image = pygame.image.load('assets/images/menu_play_rect.png')
        button_menu_play_image = pygame.transform.scale(button_menu_play_image, (200, 50))
        button_menu_play = Button(image=button_menu_play_image, pos=(320, 250),
                                  text_input='시작', font=Font(Fonts.TITLE1, 40).to_pygame(), base_color='#ffffff',
                                  hovering_color='White')

        for button in [button_menu_play]:
            button.change_color(menu_mouse_pos)
            button.update(CONFIG.surface)

        CONFIG.surface.blit(menu_title, rect_menu)
        CONFIG.update_screen()

        process(process_menu)