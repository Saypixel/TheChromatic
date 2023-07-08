import pygame
from button import Button

from const import CONST
from player import Player
from font import Font

FPS = 30

screen = pygame.display.set_mode(CONST.WINDOW_SIZE)
clock = pygame.time.Clock()

is_running = True  # 게임이 실행되고 있는가?
game_started = True  # 게임이 시작되어 플레이어와 상호작용이 가능한가?
game_paused = False  # 게임이 일시중지되었는가?

player = Player('assets/images/Emilia.png', (100, 100), (200, 200))  # 주인공


def main():
    pygame.init()
    pygame.display.set_caption('The Chromatic')
    pygame.key.set_repeat(5, 40)  # 키 중복 허용

    update_menu()


def update_menu():
    global is_running

    while is_running:
        clock.tick(FPS)
        screen.fill(CONST.COL_MAIN_BACKGROUND_DARK)

        menu_mouse_pos = pygame.mouse.get_pos()
        menu_title = Font.get(Font.TITLE1, 50).render("The Chromatic", True, CONST.COL_WHITE)
        rect_menu = menu_title.get_rect(center=(320, 100))
        button_menu_play = Button(image=pygame.image.load("assets/images/menu_play_rect.png"), pos=(320, 250),
                                  text_input="시작", font=Font.get(Font.TITLE1, 75), base_color="#d7fcd4",
                                  hovering_color="White")

        screen.blit(menu_title, rect_menu)

        for button in [button_menu_play]:
            button.change_color(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():  # 이벤트 확인
            match event.type:
                case pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 시
                    if button_menu_play.check_for_input(menu_mouse_pos):
                        update_ingame()

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
