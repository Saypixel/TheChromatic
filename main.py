import pygame
from pygame import mixer

from const import CONST
from button import Button
from player import Player
from font import Font
from sfx_collection import SFX

FPS = 30

screen = pygame.display.set_mode(CONST.WINDOW_SIZE)
clock = pygame.time.Clock()

is_running = True  # 게임이 실행되고 있는가?
game_started = True  # 게임이 시작되어 플레이어와 상호작용이 가능한가?
game_paused = False  # 게임이 일시중지되었는가?

player = Player('assets/images/chr_base.png', (100, 100), (200, 200))  # 주인공


def main():
    pygame.init()
    mixer.init()
    SFX.init()

    pygame.display.set_caption('The Chromatic')
    pygame.key.set_repeat(5, 40)  # 키 중복 허용

    update_intro()


def update_intro():
    cooldown = 3000  # ms
    last = pygame.time.get_ticks()
    colon_count = 0

    mixer.Sound.play(SFX.INTRO)

    global is_running

    while is_running:
        clock.tick(FPS)
        screen.fill(CONST.COL_MAIN_BACKGROUND)

        now = pygame.time.get_ticks()

        #region 인트로 : 동적 Saypixel ....
        # if now - last >= cooldown:
        #     if colon_count == 4:
        #         update_menu()
        #         return
        #
        #     last = now
        #     text = 'Saypixel' + '.' * colon_count
        #
        #     colon_count += 1
        #     menu_title = Font.get(Font.TITLE3, 40).render(text, True, CONST.COL_WHITE)
        #     rect_menu = menu_title.get_rect(center=(320, 180))
        #
        #     screen.blit(menu_title, rect_menu)
        #     pygame.display.update()
        #endregion
        #region 인트로 : 정적
        menu_title = Font.get(Font.TITLE3, 40).render('Saypixel', True, CONST.COL_WHITE)
        rect_menu = menu_title.get_rect(center=(320, 180))

        screen.blit(menu_title, rect_menu)
        pygame.display.update()

        if now - last >= cooldown:
            update_menu()
            return

        #endregion

        for event in pygame.event.get():  # 이벤트 확인
            match event.type:
                case pygame.QUIT:  # 게임 종료 이벤트 발생 시
                    is_running = False


def update_menu():
    global is_running

    mixer.music.load('assets/audio/bg_main_theme_demo2.ogg')
    mixer.music.set_volume(0.7)
    mixer.music.play()

    while is_running:
        clock.tick(FPS)
        screen.fill(CONST.COL_MAIN_BACKGROUND_BLUE)

        menu_mouse_pos = pygame.mouse.get_pos()
        menu_title = pygame.image.load('assets/images/menu_title.png')
        menu_title = pygame.transform.scale(menu_title, (302, 120))
        # menu_title = Font.get(Font.TITLE1, 80).render('The Chromatic', True, CONST.COL_WHITE)
        rect_menu = menu_title.get_rect(center=(320, 100))

        button_menu_play = Button(image=pygame.image.load('assets/images/menu_play_rect.png'), pos=(320, 250),
                                  text_input='시작', font=Font.get(Font.TITLE1, 75), base_color='#ffffff',
                                  hovering_color='White')

        screen.blit(menu_title, rect_menu)

        for button in [button_menu_play]:
            button.change_color(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():  # 이벤트 확인
            match event.type:
                case pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 시
                    if button_menu_play.check_for_input(menu_mouse_pos):
                        mixer.music.stop()
                        update_ingame()
                        return

                case pygame.QUIT:  # 게임 종료 이벤트 발생 시
                    is_running = False

        pygame.display.update()


def update_ingame():
    global is_running, player

    while is_running:
        clock.tick(FPS)  # 프레임 조절
        screen.fill(CONST.COL_WHITE)

        for event in pygame.event.get():  # 이벤트 확인
            match event.type:
                case pygame.KEYDOWN:
                    if game_started and not game_paused:  # 플레이어와 상호작용 가능할 때
                        match event.key:
                            case pygame.K_a | pygame.K_LEFT:  # 왼쪽으로 이동
                                player.move(-1)
                            case pygame.K_d | pygame.K_RIGHT:  # 오른쪽으로 이동
                                player.move(1)

                case pygame.QUIT:  # 게임 종료 이벤트 발생 시
                    is_running = False

        screen.blit(player.image, player.get_pos())
        pygame.display.update()


if __name__ == '__main__':
    main()
    pygame.quit()
