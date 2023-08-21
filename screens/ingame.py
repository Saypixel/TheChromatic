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
                            "assets/images/chr_player_stay.png", 4, 1, size=(170, 270)
                        )),
                    "walk": SpriteHandler(
                        Sprite(
                            "assets/images/chr_player_walk.png", 6, 1, size=(345, 270)
                        ))
                },
                "stay",
                position=(200, 197),
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
        self.spike = Player.get_from_sprite(SpriteCollection({
            "default": SpriteHandler(
                Sprite(
                    "assets/images/object_spike_default.png", 17, 1, size=(155, 100)
                )
            )
        },
        "default",
        position=(800, 270),
        scale=0.4))

        self.spike2 = Player.get_from_sprite(SpriteCollection({
            "default": SpriteHandler(
                Sprite(
                    "assets/images/object_spike_default.png", 17, 1, size=(155, 100)
                )
            )
        },
        "default",
        position=(850, 270),
        scale=0.4))

        self.obstacles = [self.spike, self.spike2]

        # 적
        self.enemy = Enemy("assets/images/chr_raon.png", (1000, 222), 0.4)
        self.enemies = [self.enemy]

        for enemy in self.enemies:
            enemy.grace_period = GracePeriod(1500)
            enemy.hp = 2

        # NPC
        self.emilia = Player("assets/images/chr_emilia.png", (400, 195), 0.4)  # 에밀리아
        self.NPCs = [self.emilia]

        # 기타 아이템
        self.sign = Texture("assets/images/sign_big.png", (300, 100), 0.3)
        self.hp = SpriteCollection({
            "attacked": SpriteHandler(
                Sprite(
                    "assets/images/hp_bar.png", 31, 1, size=(500, 165)
                    )),
            "healed": SpriteHandler(
                Sprite(
                    "assets/images/hp_bar_heal.png", 8, 1, size=(500, 165)
                       ))
            },
            "attacked",
            position=(0, 0),
            scale=0.4
            )
        
        # 배경
        self.background = Texture("assets/images/background_sky.png", (0, 0), 1, repeat_x=2, fit=True)
        self.ground = Texture("assets/images/grass.png", (0, 287), 0.4, repeat_x=2)

    def update_ingame(self):
        def process_ingame_movement():
            """키 동시 입력 처리를 위한 움직임 이벤트 처리"""
            keys = pygame.key.get_pressed()  # 키 동시 입력 처리

            if CONFIG.is_movable():  # 플레이어가 움직일 수 있을 때 (상호작용 포함)
                is_moved = False

                if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # 왼쪽으로 이동
                    self.player.move_x(-1)
                    is_moved = True
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # 오른쪽으로 이동
                    self.player.move_x(1)
                    is_moved = True

                if is_moved:
                    self.player.sprites.status = "walk"
                else:
                    self.player.sprites.status = "stay"

        def process_ingame(event: pygame.event.Event):
            """인게임 이벤트 처리용 (process() child 함수)"""

            match event.type:
                case pygame.KEYDOWN:
                    if CONFIG.is_interactive():
                        match event.key:
                            case pygame.K_SPACE | pygame.K_w | pygame.K_UP:
                                if self.emilia.is_bound(80, 80):
                                    TextEvent.process_next_event()

                                    if TextEvent.dialog_delayed:
                                        self.sign.refresh()

                                    if not TextEvent.dialog_closed:
                                        pygame.time.set_timer(CONST.PYGAME_EVENT_DIALOG, 1, 1)

                                    # 주인공 애니메이션 기본으로 설정
                                    self.player.sprites.status = "stay"

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

                            case pygame.K_e:  # 체력 회복 or 상호작용
                                self.player.healed = True

                case pygame.KEYUP:
                    pass
                    if CONFIG.is_interactive():
                        match event.key:
                            case pygame.K_ESCAPE:
                                update_pause_menu()

                case CONST.PYGAME_EVENT_DIALOG:  # 텍스트 애니메이션 이벤트
                    if CONFIG.is_interactive():
                        TextEvent.process_animation_event(self.sign.image)

                case pygame.MOUSEBUTTONDOWN:
                    if CONFIG.game_dead:  # 사망 시
                        if self.button_retry.check_for_input(self.mouse_pos):  # 재도전
                            self.reload = True
                            self.need_to_exit = True

                        if self.button_menu.check_for_input(self.mouse_pos):  # 메뉴화면으로 나가기
                            self.need_to_exit = True

        TextEvent.dialog = TextCollection(
            [
                Text("*안녕!*"),
                Text("나는 에밀리아야."),
                Text("*J키*는 #기본공격#이야!"),
                Text("그럼 즐거운 여행되길 바래!")
            ],
            self.sign.width
        )

        count = 0

        hp_attacked_count = 0  # 애니메이션 (피공격)
        hp_healed_count = 7  # 애니메이션 (회복)

        while CONFIG.is_running and not self.need_to_exit:
            CONFIG.clock.tick(CONFIG.FPS)  # 프레임 조절

            count += 1
            self.mouse_pos = CONFIG.get_mouse_pos()

            # region 카메라
            hp_sprite = self.hp.get_sprite_handler().sprite
            hp_sprite.set_pos((CONFIG.camera_x, hp_sprite.position[1]))

            self.background.set_pos(CONFIG.camera_x // 1.1, self.background.y)  # 조금씩 움직이게 하고 싶어요
            #self.ground.set_pos(CONFIG.camera_x, self.ground.y)
            # endregion

            CONFIG.surface.blit(self.background.image.convert(), self.background.get_pos())
            CONFIG.surface.blit(self.ground.image, self.ground.get_pos())

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
            for obstacle in self.obstacles:
                self.player.check_if_attacked(obstacle.is_bound(-5, 24))

            for enemy in self.enemies:
                enemy.apply_movement_flipped(enemy.image)

                if enemy.hp <= 0:
                    enemy_surface = self.enemy.get_surface_or_sprite()
                    enemy_alpha = enemy_surface.get_alpha()
                    reduced = 30
                    enemy_next_alpha = max(0, enemy_alpha - reduced)

                    enemy_surface.set_alpha(enemy_next_alpha)

                    if enemy_next_alpha == 0:  # 적 사망
                        index = self.enemies.index(enemy)
                        self.enemies.pop(index)
                
                if not enemy.grace_period.is_grace_period():  # 스턴 시간이 끝난 경우
                    enemy.follow_player(self.obstacles)
                    self.player.check_if_attacked(enemy.is_bound(40, 100) and enemy.hp > 0 and not enemy.grace_period.is_grace_period())

            World.process_gravity(self.enemies + [self.player], 305)  # 중력 구현
            # endregion
            # region 체력 + 피공격
            self.hp.get_sprite_handler().group.draw(CONFIG.surface)

            hp_attacked_sprite = self.hp.sprites['attacked']
            hp_healed_sprite = self.hp.sprites['healed']

            if self.player.attacked:  # 공격을 받은 경우
                if hp_attacked_count == 24:
                    CONFIG.game_dead = True
                    SFX.DEAD.play()

                hp_attacked_count += 6
                hp_healed_count -= 2

                hp_healed_sprite.sprite.update(added_index=-2)  # hp 애니메이션 동기화

                self.player.hp -= 1
                self.player.move_y(5)

                self.player.grace_period.update()
                SFX.ATTACKED.play()

                self.hp.status = 'attacked'
                self.player.attacked = False

            if self.player.healed:  # 체력을 회복한 경우
                if self.player.hp < 5:
                    hp_attacked_count -= 6
                    hp_healed_count += 2

                    hp_attacked_sprite.sprite.update(added_index=-6)  # hp 애니메이션 동기화

                    self.player.hp += 1

                    SFX.ENEMY_ATTACKED.play()

                    self.hp.status = 'healed'
                    
                self.player.healed = False

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
                # hp 애니메이션 업데이트
                if hp_attacked_count > hp_attacked_sprite.sprite.index:
                    hp_attacked_sprite.sprite.update()
                if hp_healed_count > hp_healed_sprite.sprite.index:
                    hp_healed_sprite.sprite.update()

                # 장애물 애니메이션
                for obstacle in self.obstacles:
                    if obstacle.is_sprite():
                        obstacle.sprites.get_sprite_handler().sprite.update()
            # endregion
            # region 대화
            if not TextEvent.dialog_closed:
                self.emilia.speech(self.sign)
            else:
                self.emilia.unspeech()
            # endregion
            status_player = self.player.sprites.status

            if count % 3 == 0:
                if status_player == "walk":
                    sprite_player.update()

            if count == 10:
                count = 0

                if status_player == "stay":
                    sprite_player.update()

            process(process_ingame)
            process_ingame_movement()

            # 장애물
            for obstacle in self.obstacles:
                obstacle.render()

            # NPC
            self.emilia.render()

            # 적
            for enemy in self.enemies:
                enemy.render()

            # 플레이어
            self.player.render()
            #self.player.generate_hitbox()

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

                CONFIG.surface.blit(self.dead_background, (180 + CONFIG.camera_x, 120 + CONFIG.camera_y))
                CONFIG.surface.blit(
                    self.dead_text, self.dead_text.get_rect(center=(320 + CONFIG.camera_x, 160 + CONFIG.camera_y))
                )

                for button in [self.button_retry, self.button_menu]:
                    button.change_color(self.mouse_pos)
                    button.update(CONFIG.surface)

                # 플레이어 행동을 stay로 설정
                self.player.sprites.status = "stay"

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

                CONFIG.surface.blit(fps_text, (585 + CONFIG.camera_x, 10 + CONFIG.camera_y))
            # endregion

            CONFIG.update_screen()

        # 초기화
        TextEvent.dialog_closed = True
        TextEvent.dialog_delayed = True
        TextEvent.dialog_paused = True

        self.player.set_pos(200, 225)

        CONFIG.game_dead = False
        CONFIG.camera_x = 0
        CONFIG.camera_y = 0

        CONFIG.surface.fill(CONST.COL_WHITE)

        if self.reload:
            Ingame.default = Ingame()
            Ingame.default.update_ingame()

        pygame.mixer.music.stop()

        pygame.mixer.pause()
        pygame.mixer.unpause()
