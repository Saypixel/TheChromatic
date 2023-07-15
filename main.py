import pygame
from pygame import mixer

from const import CONST
from button import Button
from player import Player
from font import Font
from sfx_collection import SFX
from text import Text

FPS = 30

window_size = [1920, 1080]  # CONST.WINDOW_SIZE * 3
window_scale = 3

is_fullscreen = False

surface = pygame.Surface(CONST.SCREEN_SIZE)
'''크기가 [640, 360]으로 고정된 화면
surface에 렌더링하고 업스케일링 후 screen으로 화면 표시'''

screen = pygame.display.set_mode(window_size)
'''업스케일링된 실제로 플레이어에게 보여주는 화면'''

clock = pygame.time.Clock()

is_running = True
'''게임이 실행되고 있는가?'''

game_started = True
'''게임이 시작되어 플레이어와 상호작용이 가능한가?'''

game_paused = False
'''게임이 일시중지되었는가?'''

dialog_delayed = False
'''대화창의 텍스트 출력이 지연되었는가? (REFRESH 이슈 대응)'''

dialog_paused = False
'''대화창의 텍스트 출력이 완성되었는가?'''

dialog_current: Text
'''현재 대화 텍스트'''

dialog_next: Text
'''다음 대화 텍스트'''

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
        surface.fill(CONST.COL_MAIN_BACKGROUND)

        now = pygame.time.get_ticks()

        # region 인트로 : 동적 Saypixel ....
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
        # endregion
        # region 인트로 : 정적
        menu_title = Font.render(Font.TITLE3, 40, 'Saypixel', CONST.COL_WHITE)
        rect_menu = menu_title.get_rect(center=(320, 180))

        surface.blit(menu_title, rect_menu)
        update_screen()

        if now - last >= cooldown:
            update_menu()
            return

        # endregion

        process_event()


def update_menu():
    def process_event_menu(event: pygame.event.Event):
        """인게임 이벤트 처리용 (process_event() child 함수)"""
        match event.type:
            case pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 시
                if button_menu_play.check_for_input(menu_mouse_pos):
                    mixer.music.stop()
                    update_ingame()
                    return

    global is_running

    mixer.music.load('assets/audio/bg_main_theme_demo2.ogg')
    mixer.music.set_volume(0.7)
    mixer.music.play()

    while is_running:
        clock.tick(FPS)
        surface.fill(CONST.COL_MAIN_BACKGROUND_BLUE)

        menu_mouse_pos = get_mouse_pos()
        menu_title = pygame.image.load('assets/images/menu_title.png')
        menu_title = pygame.transform.scale(menu_title, (242, 96))
        # menu_title = Font.get(Font.TITLE1, 80).render('The Chromatic', True, CONST.COL_WHITE)
        rect_menu = menu_title.get_rect(center=(320, 100))

        button_menu_play_image = pygame.image.load('assets/images/menu_play_rect.png')
        button_menu_play_image = pygame.transform.scale(button_menu_play_image, (200, 50))
        button_menu_play = Button(image=button_menu_play_image, pos=(320, 250),
                                  text_input='시작', font=Font.get(Font.TITLE1, 40), base_color='#ffffff',
                                  hovering_color='White')

        for button in [button_menu_play]:
            button.change_color(menu_mouse_pos)
            button.update(surface)

        surface.blit(menu_title, rect_menu)
        update_screen()

        process_event(process_event_menu)


def update_ingame():
    global is_running, player, dialog_current, dialog_next

    def process_event_ingame(event: pygame.event.Event):
        """인게임 이벤트 처리용 (process_event() child 함수)"""
        global player, dialog_current, dialog_next, dialog_paused, dialog_delayed

        match event.type:
            case pygame.KEYDOWN:
                if is_interactive():  # 플레이어와 상호작용 가능할 때
                    match event.key:
                        case pygame.K_a | pygame.K_LEFT:  # 왼쪽으로 이동
                            player.move(-1)
                        case pygame.K_d | pygame.K_RIGHT:  # 오른쪽으로 이동
                            player.move(1)

            case pygame.KEYUP:
                if is_interactive():
                    match event.key:
                        case pygame.K_SPACE:
                            if dialog_paused:  # 대화창의 텍스트 출력이 완성되었을 때
                                if dialog_current is None:  # 대화창의 텍스트가 더이상 없을 때
                                    print('대화창 닫힘')
                                else:
                                    print('대화창 넘김')
                                    dialog_current = dialog_next
                                    dialog_delayed = False
                                    dialog_paused = False

                            else:
                                dialog_current.jump_to_last_index()
                                dialog_delayed = True  # 텍스트 미리 모두 출력
                                dialog_paused = True

            case CONST.PYGAME_EVENT_DIALOG:  # 텍스트 애니메이션 이벤트
                if is_interactive():
                    if dialog_delayed or dialog_paused:  # 대화창이 지연되었거나 완성된 경우
                        dialog_current.write_until_next((320, 180), surface)  # 완성된 텍스트를 화면에 출력
                    else:
                        delay = dialog_current.write_until_next((320, 180), surface)  # 진행 중인 텍스트를 화면에 출력

                        if delay > 0:
                            dialog_delayed = True  # delay 만큼 지연
                            pygame.time.set_timer(CONST.PYGAME_EVENT_DIALOG_NEXT_INDEX, delay, 1)  # delay ms 후 다음 텍스트 진행
                        else:
                            dialog_paused = True

            case CONST.PYGAME_EVENT_DIALOG_NEXT_INDEX:
                if dialog_current.jump_to_next_index(False):  # 다음 텍스트 진행
                    dialog_delayed = False

    dialog_current = Text('*안녕!*')
    dialog_next = Text('나는 에밀리아야.')

    while is_running:
        clock.tick(FPS)  # 프레임 조절
        surface.fill(CONST.COL_WHITE)

        process_event(process_event_ingame)

        surface.blit(player.image, player.get_pos())
        pygame.time.set_timer(CONST.PYGAME_EVENT_DIALOG, 1, 1)  # 텍스트 테스트용
        update_screen()


def update_screen():
    """
    화면 업스케일링이 적용된 디스플레이 업데이트 기능
    """
    transformed_screen = pygame.transform.scale(surface, window_size)  # 업스케일링
    screen.blit(transformed_screen, (0, 0))  # 화면 표시

    pygame.display.update()  # 디스플레이 업데이트


def update_screen_resolution():
    """
    화면 해상도 업데이트
    """
    if is_fullscreen:
        screen = pygame.display.set_mode(window_size, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(window_size)


def process_event(f=None):
    """
    공통 이벤트 확인 및 처리
    :param f: 이벤트를 처리할 함수
    """
    global is_running, is_fullscreen

    for event in pygame.event.get():  # 이벤트 확인
        match event.type:
            case pygame.QUIT:  # 게임 종료 이벤트 발생 시
                is_running = False

            case pygame.KEYDOWN:
                match event.key:
                    case pygame.KMOD_ALT | pygame.K_F4:  # ALT + F4
                        is_running = False

                    case _:
                        if f is not None:
                            f(event)

            case pygame.KEYUP:
                match event.key:
                    case pygame.K_F11:  # 전체화면 이벤트 처리
                        is_fullscreen = not is_fullscreen
                        update_screen_resolution()

                    case _:
                        if f is not None:
                            f(event)

            case _:
                if f is not None:
                    f(event)


def get_mouse_pos():
    """
    화면 업스케일링이 적용된 마우스 위치 가져오기
    :return:
    """
    mouse_pos = pygame.mouse.get_pos()

    if window_scale == 1:
        return mouse_pos

    transformed_mouse_pos = (mouse_pos[0] // window_scale, mouse_pos[1] // window_scale)
    return transformed_mouse_pos


def is_interactive():
    """플레이어와 상호작용 가능한가?"""
    return game_started and not game_paused


if __name__ == '__main__':
    main()
    pygame.quit()
