import pygame

from player import Player
from const import CONST

FPS = 30
WHITE = (255, 255, 255)

screen = pygame.display.set_mode(CONST.WINDOW_SIZE)
clock = pygame.time.Clock()

is_running = True  # 게임이 실행되고 있는가?
game_started = True  # 게임이 시작되어 플레이어와 상호작용이 가능한가?
game_paused = False  # 게임이 일시중지되었는가?

player = Player('resources/images/Emilia.png', (100, 100), (200, 200))  # 주인공


def main():
    pygame.init()
    pygame.display.set_caption('The Chromatic')
    pygame.key.set_repeat(5, 40)  # 키 중복 허용

    update()


def update():
    global is_running, player

    while is_running:
        clock.tick(FPS)  # 프레임 조절
        screen.fill(WHITE)

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
