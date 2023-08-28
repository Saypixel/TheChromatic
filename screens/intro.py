import pygame
from components.config import CONFIG, CONST, Fonts, debug
from components.events import process
from components.font import Font
from components.sfx_collection import SFX
from screens.menu import update_menu


def update():
    """인트로 화면으로 이동합니다."""
    cooldown = 1000  # 인트로 업데이트 간격 (단위: ms)
    last = pygame.time.get_ticks()  # 현재 시간 가져오기

    text = "Saypixel"  # 로고
    colon_count = 1  # 로고 애니메이션

    SFX.INTRO.play()  # 인트로 효과음 재생

    from characters.player import Player
    from components.sprites.sprite import Sprite
    from components.sprites.sprite_collection import SpriteCollection
    from components.sprites.sprite_handler import SpriteHandler

    # SpriteCollection, SpriteHandler, Sprite를 이용하여 다중 스프라이트를 사용하는 플레이어 가져오기
    player_icon = Player.get_from_sprite(
        SpriteCollection(
                {
                    "walk": SpriteHandler(
                        Sprite(
                            "assets/images/icon_walk.png", 2, 1, size=(80, 80)
                        ))
                },
                "walk",
                position=(-250, 480),
                scale=0.4,
            )
    )
    count = 0  # 매 프레임마다 업데이트 되는걸 방지, 그러면 애니메이션이 너무 빨라질 수 있음

    while CONFIG.is_running:
        CONFIG.clock.tick(CONFIG.FPS)
        CONFIG.surface.fill(CONST.COL_MAIN_BACKGROUND)  # 정해놓은 백그라운드 색상으로 칠

        for event in pygame.event.get():
            match event.type:
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_BACKQUOTE:  # ` 키를 누를 시 인트로 스킵
                            update_menu()
                            reload()

                        case pygame.K_ESCAPE:  # ESC 키를 누를 시 게임 종료
                            CONFIG.is_running = False

        now = pygame.time.get_ticks()  # 현재 시간 가져오기

        # region 인트로 : 동적 Saypixel ....
        if now - last >= cooldown:  # 인트로 업데이트 간격보다 시간이 지난 경우
            if colon_count == 4:  # 애니메이션이 끝난 경우 메인 메뉴로 이동함
                update_menu()
                reload()
                return

            last = now  # 업데이트한 시간 갱신

            # 로고 애니메이션
            text = "Saypixel" + "." * colon_count
            colon_count += 1
        # endregion

        count += 1

        if count == 3:  # 매 3프레임 마다 호출
            count = 0
            player_icon.sprites.get_sprite_handler().sprite.update()  # 스프라이트 애니메이션 업데이트

        player_icon.move_x(1.2)  # 1.2의 속도만큼 X 좌표로 이동
        player_icon.render()  # 렌더링

        title = Font(Fonts.TITLE3, 60).render(text, CONST.COL_WHITE)  # 로고 폰트 렌더링
        title_rect = title.get_rect(center=(480, 270))  # 로고의 좌표 & 크기 (Rect) 가져오기

        CONFIG.surface.blit(title, title_rect)  # 로고를 화면에 렌더링
        CONFIG.update_screen()  # 업스케일링

        process()  # 공통 이벤트 처리


def reload():
    """Ctrl + R을 누르면 게임을 새로고침합니다. 이 때 게임이 재시작됩니다."""
    import screens.menu

    if screens.menu.reload:  # Ctrl + R이 눌려서 게임을 새로고침 해야하는 경우
        screens.menu.reload = False  # 새로고침 변수 업데이트

        # 음악 및 효과음 중지
        pygame.mixer.music.stop()

        pygame.mixer.pause()
        pygame.mixer.unpause()

        update()  # 인트로 화면으로 이동
        reload()  # 새로고침 시 update_menu()는 종료되기 때문에 update() 함수도 같이 종료됨.
                  # 이 때 관련 변수를 이용하여 새로고침을 해야하는지 알 수 있음.
