from random import Random

import pygame

from characters.player import Player
from characters.enemy import Enemy
from characters.texture import Texture

from components.button import Button
from components.config import CONFIG, CONST, debug
from components.events import process
from components.sfx_collection import SFX
from components.world import World

from components.font import Font, Fonts
from components.text import Text
from components.text.text_collection import TextCollection

from components.events.text import TextEvent
from components.events.grace_period import GracePeriod

from components.sprites.sprite_collection import SpriteCollection
from components.sprites.sprite_handler import SpriteHandler
from components.sprites.sprite import Sprite

from screens.pause_menu import update_pause_menu


class Ingame:
    default: "Ingame"

    def __init__(self):
        self.need_to_exit = False
        self.reload = False

        self.dead_background = None
        self.dead_text = None
        self.button_retry = None
        self.button_menu = None
        self.mouse_pos = CONFIG.get_mouse_pos()

        # 주인공
        self.player = Player.get_from_sprite(
            SpriteCollection(
                {
                    "stay": SpriteHandler(
                        Sprite(
                            "assets/images/chr_player_stay.png", 4, 1, size=(160, 270)
                        )
                    )
                },
                "stay",
                position=(200, 225),
                scale=0.4,
            ),
            True,
        )
        self.player.grace_period = GracePeriod()

        # FX
        self.fx = SpriteCollection({
            "attack": SpriteHandler(
                Sprite(
                    "assets/images/fx_attack.png", 9, 1, size=(150, 150)
                )
            )
        },
        "attack",
        position=(200, 225),
        scale=0.6)

        # 장애물
        self.spike = Texture("assets/images/object_spike.png", (300, 315), 0.2)
        self.obstacles = [self.spike]

        # 적
        self.enemy = Enemy("assets/images/chr_raon.png", (500, 250), 0.4)
        self.enemies = [self.enemy]

        for enemy in self.enemies:
            enemy.grace_period = GracePeriod(1000)
            enemy.hp = 2

        # NPC
        self.emilia = Player("assets/images/chr_emilia.png", (400, 220), 0.4)  # 에밀리아
        self.NPCs = [self.emilia]

        # 기타 아이템
        self.sign = Texture("assets/images/sign_big.png", (300, 100), 0.3)
        self.hp = SpriteHandler(
            Sprite("assets/images/hp_bar.png", 31, 1, size=(500, 165), scale=0.4)
        )

        # 배경
        self.background = Texture("assets/images/background.png", (0, 0), 1, fit=True)
        self.ground = Texture("assets/images/ground.png", (0, 0), 1, fit=True)

    def update_ingame(self):
        def process_ingame_movement():
            """키 동시 입력 처리를 위한 움직임 이벤트 처리"""
            keys = pygame.key.get_pressed()  # 키 동시 입력 처리

            if CONFIG.is_movable():  # 플레이어가 움직일 수 있을 때 (상호작용 포함)
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # 왼쪽으로 이동
                    self.player.move_x(-1)
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # 오른쪽으로 이동
                    self.player.move_x(1)

        def process_ingame(event: pygame.event.Event):
            """인게임 이벤트 처리용 (process() child 함수)"""

            match event.type:
                case pygame.KEYDOWN:
                    if CONFIG.is_interactive():
                        match event.key:
                            case pygame.K_SPACE | pygame.K_w | pygame.K_UP:
                                if self.emilia.is_bound(100, 100):
                                    TextEvent.process_next_event()

                                    if not TextEvent.dialog_delayed:
                                        self.sign.refresh()

                                    if not TextEvent.dialog_closed:
                                        pygame.time.set_timer(
                                            CONST.PYGAME_EVENT_DIALOG, 1, 1
                                        )
                                else:
                                    if not self.player.is_air:  # 다중 점프 금지
                                        self.player.move_y(13)  # 점프

                            case pygame.K_j:  # 기본 공격
                                self.player.attack = True
                                SFX.ATTACK.play()

                                for enemy in self.enemies:
                                    if enemy.is_bound(80, 100) and not enemy.grace_period.is_grace_period():
                                        enemy.hp -= 1
                                        enemy.grace_period.update()
                                        SFX.ENEMY_ATTACKED.play()

                case pygame.KEYUP:
                    pass
                    if CONFIG.is_interactive():
                        match event.key:
                            case pygame.K_ESCAPE:
                                update_pause_menu()

                case CONST.PYGAME_EVENT_DIALOG:  # 텍스트 애니메이션 이벤트
                    if CONFIG.is_interactive():
                        TextEvent.process_animation_event(self.sign.image)

                case CONST.PYGAME_EVENT_DIALOG_NEXT_INDEX:
                    TextEvent.process_animation_next_event()

                case pygame.MOUSEBUTTONDOWN:
                    if CONFIG.game_dead:  # 사망 시
                        if self.button_retry.check_for_input(self.mouse_pos):  # 재도전
                            self.reload = True
                            self.need_to_exit = True

                        if self.button_menu.check_for_input(self.mouse_pos):  # 메뉴화면으로 나가기
                            self.need_to_exit = True

        TextEvent.dialog = TextCollection(
            [Text("*안녕!*"), Text("나는 에밀리아야."), Text("*J키*는 #기본공격#이야!"), Text("그럼 즐거운 여행되길 바래!")],
            self.sign.width,
        )

        count = 0

        hp_count = 0  # 애니메이션

        while CONFIG.is_running and not self.need_to_exit:
            CONFIG.clock.tick(CONFIG.FPS)  # 프레임 조절

            count += 1
            self.mouse_pos = CONFIG.get_mouse_pos()

            CONFIG.surface.blit(self.background.image.convert(), (0, 0))
            CONFIG.surface.blit(self.ground.image, (0, 0))

            # region 플레이어 움직임
            sprite_player = self.player.sprites.get_sprite_handler().sprite
            self.player.apply_movement_flipped(sprite_player)
            # endregion
            # region FX
            fx_sprite = self.fx.get_sprite_handler().sprite
            fx_x = self.player.x + (10 if not fx_sprite.flipped else -40)
            
            self.fx.set_pos((fx_x, self.player.y))
            self.player.apply_movement_flipped(fx_sprite)  # 플레이어 움직임에 따라서 FX 움직임 동기화
            # endregion
            # region 장애물, 적, 중력
            self.player.check_if_attacked(self.spike.is_bound(40, 100))
 
            for enemy in self.enemies:
                enemy.apply_movement_flipped(enemy.image)

                if enemy.hp <= 0:
                    enemy_surface = self.enemy.get_surface_or_sprite()
                    enemy_alpha = enemy_surface.get_alpha()
                    reduced = 20
                    enemy_next_alpha = max(0, enemy_alpha - reduced)

                    enemy_surface.set_alpha(enemy_next_alpha)

                    if enemy_next_alpha == 0:  # 적 사망
                        index = self.enemies.index(enemy)
                        self.enemies.pop(index)
                
                enemy.follow_player(self.obstacles)
                self.player.check_if_attacked(enemy.is_bound(40, 100) and enemy.hp > 0)

            World.process_gravity(self.enemies + [self.player], 333)  # 중력 구현
            # endregion
            # region 체력 + 피공격
            self.hp.group.draw(CONFIG.surface)

            if self.player.attacked:  # 공격을 받은 경우
                if hp_count == 24:
                    CONFIG.game_dead = True

                hp_count += 6
                self.player.hp -= 1
                self.player.move_y(5)

                self.player.grace_period.update()
                SFX.ATTACKED.play()

                self.player.attacked = False

            # 무적 시간
            for player in self.enemies + [self.player]:
                if player.grace_period is not None:
                    image = player.get_surface_or_sprite()

                    if player.grace_period.is_grace_period():  # 무적시간인 경우
                        player.grace_period.make_it_ui(image)
                        player.grace_period.lasted = True

                    elif player.grace_period.lasted:
                        image.set_alpha(255)  # 무적 시간이 아니므로 복귀
                        player.grace_period.lasted = False

            if count % 5 == 0:
                if self.hp.sprite.index < hp_count:  # hp 애니메이션 동기화
                    self.hp.group.update()
            # endregion
            # region 대화
            if not TextEvent.dialog_closed:
                self.emilia.speech(self.sign)
            else:
                self.emilia.unspeech()
            # endregion

            if count == 10:
                count = 0

                sprite_player.update()

            process(process_ingame)
            process_ingame_movement()

            # 장애물
            self.spike.render()

            # NPC
            self.emilia.render()

            # 적
            for enemy in self.enemies:
                enemy.render()

            # 플레이어
            self.player.render()

            # region 공격
            if self.player.attack:  # 공격을 한 경우
                if self.fx.status != "attack":
                    self.fx.status = "attack"
                handler = self.fx.get_sprite_handler()

                if handler.sprite.index != handler.sprite.length - 1:
                    handler.group.draw(CONFIG.surface)
                else:
                    self.player.attack = False
                handler.sprite.update()
            # endregion
            # region 사망 이벤트
            if CONFIG.game_dead:  # 최적화
                if self.dead_background is None:
                    self.dead_background = pygame.image.load(
                        "assets/images/status3.png"
                    )
                    self.dead_background = pygame.transform.rotate(
                        self.dead_background, 90
                    )
                    self.dead_background = pygame.transform.scale_by(
                        self.dead_background, 0.25
                    )
                    self.dead_background = pygame.transform.scale(
                        self.dead_background,
                        (
                            self.dead_background.get_width() + 20,
                            self.dead_background.get_height() - 20,
                        ),
                    )

                if self.dead_text is None:
                    self.dead_text = Font(Fonts.TITLE2, 40).render(
                        "죽었다이", (255, 255, 255)
                    )

                if self.button_retry is None:
                    button_retry_image = pygame.image.load(
                        "assets/images/menu_play_rect.png"
                    )
                    button_retry_image = pygame.transform.scale(
                        button_retry_image, (150, 50)
                    )

                    self.button_retry = Button(
                        image=button_retry_image,
                        pos=(320, 220),
                        text_input="재도전",
                        font=Font(Fonts.TITLE2, 30).to_pygame(),
                        base_color="#ffffff",
                        hovering_color="White",
                    )

                if self.button_menu is None:
                    button_menu_image = pygame.image.load(
                        "assets/images/menu_play_rect.png"
                    )
                    button_menu_image = pygame.transform.scale(
                        button_retry_image, (210, 50)
                    )

                    self.button_menu = Button(
                        image=button_menu_image,
                        pos=(320, 280),
                        text_input="메뉴 화면으로",
                        font=Font(Fonts.TITLE2, 30).to_pygame(),
                        base_color="#ffffff",
                        hovering_color="White",
                    )

                CONFIG.surface.blit(self.dead_background, (180, 120))
                CONFIG.surface.blit(
                    self.dead_text, self.dead_text.get_rect(center=(320, 160))
                )

                for button in [self.button_retry, self.button_menu]:
                    button.change_color(self.mouse_pos)
                    button.update(CONFIG.surface)

                # 흐려지며 사라지다 (Fade Out)
                sprite = self.player.sprites.get_sprite_handler().sprite
                reduced = 10
                alpha_next = max(0, sprite.alpha - reduced)

                sprite.set_alpha(alpha_next)
            # endregion
            # region FPS 표시
            if CONFIG.game_fps:
                fps = round(CONFIG.clock.get_fps(), 1)
                fps_text = Font(Fonts.TITLE3, 20).render(str(fps), (255, 255, 255))

                CONFIG.surface.blit(fps_text, (585, 10))
            # endregion

            CONFIG.update_screen()

        # 초기화
        TextEvent.dialog_closed = True
        TextEvent.dialog_delayed = False
        TextEvent.dialog_paused = True

        self.player.set_pos(200, 225)

        CONFIG.game_dead = False

        if self.reload:
            Ingame.default = Ingame()
            Ingame.default.update_ingame()

        pygame.mixer.music.stop()

        pygame.mixer.pause()
        pygame.mixer.unpause()
