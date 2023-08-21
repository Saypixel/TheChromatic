import pygame
from components.config import CONFIG, CONST, Fonts, debug
from components.events import process
from components.font import Font
from components.sfx_collection import SFX
from screens.menu import update_menu


def update():
    cooldown = 1000  # ms
    last = pygame.time.get_ticks()

    text = "Saypixel"
    colon_count = 1

    SFX.INTRO.play()

    from characters.player import Player
    from components.sprites.sprite import Sprite
    from components.sprites.sprite_collection import SpriteCollection
    from components.sprites.sprite_handler import SpriteHandler

    player = Player.get_from_sprite(
            SpriteCollection(
                {
                    "walk": SpriteHandler(
                        Sprite(
                            "assets/images/chr_player_walk.png", 6, 1, size=(345, 270)
                        ))
                },
                "walk",
                position=(-250, 255),
                scale=0.4,
            )
        )
    player_icon = Player.get_from_sprite(
        SpriteCollection(
                {
                    "walk": SpriteHandler(
                        Sprite(
                            "assets/images/icon_walk.png", 2, 1, size=(80, 80)
                        ))
                },
                "walk",
                position=(-250, 320),
                scale=0.4,
            )
    )
    is_player = False
    is_player_icon = not is_player
    
    count = 0

    while CONFIG.is_running:
        CONFIG.clock.tick(CONFIG.FPS)
        CONFIG.surface.fill(CONST.COL_MAIN_BACKGROUND)

        for event in pygame.event.get():
            match event.type:
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_BACKQUOTE:
                            update_menu()
                            reload()

                        case pygame.K_ESCAPE:
                            CONFIG.is_running = False

        now = pygame.time.get_ticks()

        # region 인트로 : 동적 Saypixel ....
        if now - last >= cooldown:
            if colon_count == 4:
                update_menu()
                reload()
                return

            last = now
            text = "Saypixel" + "." * colon_count

            colon_count += 1
        # endregion

        count += 1

        if count == 3:
            count = 0
            if is_player:
                player.sprites.get_sprite_handler().sprite.update()

            if is_player_icon:
                player_icon.sprites.get_sprite_handler().sprite.update()

        if player.x <= CONST.SCREEN_SIZE[0]:
            if is_player:
                player.move_x(0.8)
                player.render()
                
            if is_player_icon:
                player_icon.move_x(0.8)
                player_icon.render()

        title = Font(Fonts.TITLE3, 40).render(text, CONST.COL_WHITE)
        title_rect = title.get_rect(center=(320, 180))

        # region 아이콘
        # icon = pygame.image.load("assets/images/icon.png")
        # icon = pygame.transform.scale_by(icon, 0.4)

        # CONFIG.surface.blit(icon, (title_rect[0] - 3, title_rect[1] - 30))
        # endregion

        CONFIG.surface.blit(title, title_rect)

        CONFIG.update_screen()

        process()


def reload():
    import screens.menu

    if screens.menu.reload:
        screens.menu.reload = False

        pygame.mixer.music.stop()

        pygame.mixer.pause()
        pygame.mixer.unpause()

        update()
        reload()
