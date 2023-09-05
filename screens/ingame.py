import pygame
import pygame.mixer as mixer

from characters.player import Player
from characters.texture import Texture

from components.button import Button
from components.config import CONFIG, CONST, debug
from components.events import process
from components.sfx_collection import SFX
from components.inventory import Inventory

from components.font import Font, Fonts

from components.events.text import TextEvent
from components.events.grace_period import GracePeriod
from components.events.time import TimeEvent
from components.events.noise import NoiseEvent

from components.sprites.sprite_collection import SpriteCollection
from components.sprites.sprite_handler import SpriteHandler
from components.sprites.sprite import Sprite

from maps.map_main import MapMain
from maps.map_training import MapTraining
from maps.map_manager import MapManager

from screens.pause_menu import update_pause_menu


class Ingame:
    default: "Ingame"

    def __init__(self):
        self.need_to_exit = False
        self.reload = False

        # 사망 이벤트 관련 변수 초기화
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
                position=(200, 347),
                scale=0.4,
            ),
            True,
        )
        self.player.grace_period = GracePeriod()
        self.player.name = "player"

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

        # 기타 아이템
        self.sign = Texture("assets/images/sign_big.png", (300, 100), 0.4)
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
            scale=0.6
            )
        
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
                                speeched = self.speech_npc()  # 키가 눌러진 대화 관련 이벤트 처리 후 대화를 하고 있는지 여부를 변수로 저장

                                if TextEvent.dialog_closed and not MapManager.current.player.is_air and not speeched:  # 다중 점프 금지
                                    MapManager.current.player.move_y(13)  # 점프
                                    SFX.JUMP.play()  # 점프 효과음 재생

                                if not speeched:  # 주변에 NPC가 없는 경우 대화하는 NPC 변수 갱신
                                    TextEvent.NPC = None

                            case pygame.K_j:  # 기본 공격
                                self.player.attack = True
                                SFX.ATTACK.play()

                                for enemy in MapManager.current.enemies:
                                    if enemy.is_bound(80, 100) and not enemy.grace_period.is_grace_period():  # 적이 근처에 있고 무적시간이 아닌 경우
                                        enemy.hp -= 1  # 적 체력 감소
                                        enemy.grace_period.update()  # 적 무적시간 업데이트
                                        SFX.ENEMY_ATTACKED.play()  # 적 피공격 효과음 재생

                            case pygame.K_e:  # 아이템 상호작용
                                item = Inventory.pop_item()  # 현재 들고 있는 아이템 가져오기

                                if item is not None:  # 현재 들고 있는 아이템이 있는 경우
                                    MapManager.current.process_item_use_event(item)  # 아이템 사용 이벤트
                                    SFX.ENEMY_ATTACKED.play()  # 아이템 상호작용 효과음 재생

                            case pygame.K_LSHIFT:  # 아이템 변경
                                if Inventory.shift_item():
                                    SFX.SELECT.play()  # 아이템을 변경한 경우 효과음 재생

                            case pygame.K_r:  # 시간 관리
                                if TextEvent.dialog_closed:  # 대화창이 닫혀 있는 경우 (버그 방지)
                                    TimeEvent.is_rewind = True  # 시간 관리 변수 갱신
                                    mixer.music.pause()  # 메인 음악 일시정지
                                    SFX.REWIND.play()  # 시간 관리 효과음 재생

                case pygame.KEYUP:
                    pass
                    if CONFIG.is_interactive():
                        match event.key:
                            case pygame.K_ESCAPE:
                                update_pause_menu()

                case CONST.PYGAME_EVENT_DIALOG:  # 텍스트 애니메이션 이벤트
                    if CONFIG.is_interactive():  # 플레이어와 상호작용이 가능한 경우
                        TextEvent.process_animation_event(self.sign.image)  # 텍스트 애니메이션 이벤트 처리

                case pygame.MOUSEBUTTONDOWN:
                    if CONFIG.game_dead:  # 사망 시
                        if self.button_retry.check_for_input(self.mouse_pos):  # 재도전
                            self.reload = True
                            self.need_to_exit = True

                        if self.button_menu.check_for_input(self.mouse_pos):  # 메뉴화면으로 나가기
                            self.need_to_exit = True

        MapManager.maps = {
            "main": MapMain(self.player, self.sign),
            "training": MapTraining(self.player, self.sign)
        }
        MapManager.apply("main")

        mixer.music.load("assets/audio/bg_untitled_theme_1.ogg")
        mixer.music.set_volume(SFX.volume)
        mixer.music.play(-1)

        count = 0

        hp_attacked_index = 0  # 애니메이션 (피공격)
        hp_healed_index = 7  # 애니메이션 (회복)

        while CONFIG.is_running and not self.need_to_exit:
            CONFIG.clock.tick(CONFIG.FPS)  # 프레임 조절

            count += 1
            self.mouse_pos = CONFIG.get_mouse_pos()

            # region 카메라
            hp_sprite = self.hp.get_sprite_handler().sprite
            hp_sprite.set_pos((CONFIG.camera_x, hp_sprite.position[1]))

            Inventory.image.set_pos(CONFIG.camera_x + 30, 120)
            # endregion

            self.process_time_event() # 시간 관리 이벤트
            MapManager.current.render(count)  # 현재 맵 렌더링

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

            # hp 이벤트 처리 후 hp 애니메이션 index 변수 갱신
            hp_indicies = self.process_hp_event(hp_attacked_index, hp_healed_index)
            hp_attacked_index = hp_indicies[0]
            hp_healed_index = hp_indicies[1]

            # region 대화
            if not TextEvent.dialog_closed:
                TextEvent.NPC.speech(self.sign)
            elif TextEvent.NPC is not None:
                TextEvent.NPC.unspeech()
            # endregion
            
            status_player = self.player.sprites.status

            if count % 3 == 0:
                if status_player == "walk":
                    sprite_player.update()

            if count % 5 == 0:
                self.process_hp_animation(hp_attacked_index, hp_healed_index) # hp 애니메이션 업데이트

            if count == 10:
                count = 0

                if status_player == "stay":
                    sprite_player.update()

            Inventory.image.refresh()
            Inventory.render_item()
            Inventory.image.render()

            process(process_ingame)
            process_ingame_movement()

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
                if self.dead_background is None:  # 사망 이벤트 배경 변수가 초기화 되어있는 경우
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
                            self.dead_background.get_width() + 60,
                            self.dead_background.get_height() - 20,
                        ),
                    )

                if self.dead_text is None:  # 사망 이벤트 텍스트 변수가 초기화 되어있는 경우
                    self.dead_text = Font(Fonts.TITLE2, 40).render(
                        "죽었다이", CONST.COL_WHITE
                    )

                if self.button_retry is None:  # 사망 이벤트 재도전 변수가 초기화 되어있는 경우
                    button_retry_image = pygame.image.load(
                        "assets/images/menu_play_rect.png"
                    )
                    button_retry_image = pygame.transform.scale(
                        button_retry_image, (150, 50)
                    )

                    self.button_retry = Button(
                        image=button_retry_image,
                        pos=(480, 225),
                        text_input="재도전",
                        font=Font(Fonts.TITLE2, 30).to_pygame(),
                        base_color="#ffffff",
                        hovering_color="White",
                    )

                if self.button_menu is None:  # 사망 이벤트 메뉴 화면으로 변수가 초기화 되어있는 경우
                    button_menu_image = pygame.image.load(
                        "assets/images/menu_play_rect.png"
                    )
                    button_menu_image = pygame.transform.scale(
                        button_retry_image, (210, 50)
                    )

                    self.button_menu = Button(
                        image=button_menu_image,
                        pos=(480, 280),
                        text_input="메뉴 화면으로",
                        font=Font(Fonts.TITLE2, 30).to_pygame(),
                        base_color="#ffffff",
                        hovering_color="White",
                    )

                # 사망 이벤트 관련 변수 렌더링
                CONFIG.surface.blit(self.dead_background, (320 + CONFIG.camera_x, 120 + CONFIG.camera_y))
                CONFIG.surface.blit(
                    self.dead_text, self.dead_text.get_rect(center=(483 + CONFIG.camera_x, 160 + CONFIG.camera_y))
                )

                for button in [self.button_retry, self.button_menu]:
                    button.change_color(self.mouse_pos)
                    button.update(CONFIG.surface)

                # 플레이어 행동을 stay로 설정
                self.player.sprites.status = "stay"

                # 흐려지며 사라지다
                self.player.fade_out()
            # endregion
            # region FPS 표시
            if CONFIG.game_fps:
                fps = round(CONFIG.clock.get_fps(), 1)
                fps_text = Font(Fonts.TITLE3, 32).render(str(fps), CONST.COL_WHITE)

                CONFIG.surface.blit(fps_text, (870 + CONFIG.camera_x, 15 + CONFIG.camera_y))
            # endregion

            CONFIG.update_screen()

        # 변수 초기화
        TextEvent.reset()
        Inventory.reset()

        CONFIG.reset()
        CONFIG.surface.fill(CONST.COL_WHITE)

        self.player.set_pos(200, 347)  # 카메라 좌표를 초기화하기 위함

        if self.reload:
            Ingame.default = Ingame()
            Ingame.default.update_ingame()

        pygame.mixer.music.stop()

        pygame.mixer.pause()
        pygame.mixer.unpause()

    # region 체력
    def process_hp_event(self, hp_attacked_index: int, hp_healed_index: int) -> tuple[int, int]:
        """
        체력 관련 이벤트를 처리합니다.
        :param hp_attacked_index: hp 공격받은 애니메이션 현재 index
        :param hp_healed_index: hp 회복하는 애니메이션 현재 index
        :return: 갱신해야할 hp 애니메이션 index 변수 2개
        """
        self.hp.get_sprite_handler().group.draw(CONFIG.surface)

        hp_attacked_sprite = self.hp.sprites['attacked']
        hp_healed_sprite = self.hp.sprites['healed']

        if self.player.attacked:  # 공격을 받은 경우
            if hp_attacked_index == 24:  # 사망
                CONFIG.game_dead = True
                SFX.DEAD.play()  # 사망 효과음 재생

            hp_attacked_index += 6  # hp 공격받은 index 업데이트
            hp_healed_index -= 2  # hp 회복하는 index 업데이트

            hp_healed_sprite.sprite.update(added_index=-2)  # hp 회복하는 애니메이션 동기화

            self.player.hp -= 1  # 체력 1 감소
            self.player.move_y(5)  # 무조건 반사로 약간 점프

            self.player.grace_period.update()  # 무적 시간 활성화
            SFX.ATTACKED.play()  # 공격 받았을 때 효과음 재생

            self.hp.status = 'attacked'  # hp 공격받은 애니메이션으로 변경
            self.player.attacked = False  # 공격 여부 변수 초기화

        if self.player.healed:  # 체력을 회복한 경우
            if self.player.hp < 5:  # 체력이 꽉 차있지 않은 경우
                hp_attacked_index -= 6  # hp 공격받은 index 업데이트
                hp_healed_index += 2  # hp 회복하는 index 업데이트

                hp_attacked_sprite.sprite.update(added_index=-6)  # hp 공격받은 애니메이션 동기화

                self.player.hp += 1  # 체력 1 증가
                self.hp.status = 'healed'  #  hp 회복하는 애니메이션으로 변경
                
            self.player.healed = False  # 회복 여부 변수 초기화

        return (hp_attacked_index, hp_healed_index)

    def process_hp_animation(self, hp_attacked_index: int, hp_healed_index: int):
        """
        체력 관련 애니메이션을 처리합니다.
        :param hp_attacked_index: hp 공격받은 애니메이션 현재 index
        :param hp_healed_index: hp 회복하는 애니메이션 현재 index
        """
        hp_attacked_sprite = self.hp.sprites['attacked']  # 피공격 스프라이트 애니메이션
        hp_healed_sprite = self.hp.sprites['healed']  # 회복 스프라이트 애니메이션

        # 각 체력 스프라이트 애니메이션 동기화
        if hp_attacked_index > hp_attacked_sprite.sprite.index:
            hp_attacked_sprite.sprite.update()
        if hp_healed_index > hp_healed_sprite.sprite.index:
            hp_healed_sprite.sprite.update()
    # endregion
    # region 시간 관리
    def process_time_event(self):
        """시간 관리 이벤트를 처리합니다."""
        if TimeEvent.is_rewind:  # 시간을 되감아야 할 경우
            values = TimeEvent.rewind()  # 이전의 플레이어와 적의 위치 데이터 가져오기
            
            if values is not None:  # 되감을 값들이 아직 있는 경우
                for chr in values:
                    x_prev = chr.character.x  # 전 프레임의 캐릭터 X 좌표

                    # 현재 프레임과 전 프레임의 캐릭터 X 좌표 비교하여 현재 속도값 지정
                    velocity = -1  # 현재 속도값
                    compared = chr.x - x_prev  

                    if compared == 0:
                        velocity = 0
                    elif compared < 0:
                        velocity = 1
                    
                    if chr.character.name == "player":  # 캐릭터가 플레이어인 경우
                        if velocity != 0:  # 속도에 맞게 플레이어의 스프라이트 애니메이션 지정
                            chr.character.sprites.status = "walk"
                        else:
                            chr.character.sprites.status = "stay"

                    chr.character.velocity_x = velocity  # 캐릭터의 현재 속도값 지정
                    chr.character.set_pos(chr.x, chr.y)  # 캐릭터 좌표 지정

            else:  # 더 이상 되감을 값들이 없는 경우
                TimeEvent.is_rewind = False  # 시간 되감는 변수 갱신
                mixer.music.unpause()  # 메인 음악 다시 재생

        else:
            characters = MapManager.current.enemies + [self.player]
            TimeEvent.update(characters)  # 매 프레임마다 캐릭터들의 위치 저장
    # endregion
    # region NPC 대화
    def speech_npc(self) -> bool:
        """
        대화 키를 누른 경우 대화 관련 이벤트를 처리합니다.
        :return: NPC와 대화를 하고 있는지 여부
        """
        for npc in MapManager.current.NPCs:
            if npc.is_bound(80, 80):  # 플레이어가 NPC 일정 범위 안에 들어와 있는 경우
                if TextEvent.dialog is None and npc.dialog is not None:  # 현재 대화창이 NPC의 대화로 설정 되어있지 않은 경우
                    TextEvent.dialog = npc.dialog
                if TextEvent.NPC is None or TextEvent.NPC is not npc:  # 주변에 NPC가 있는 경우 대화하는 NPC 변수 갱신
                    TextEvent.NPC = npc

                if TextEvent.dialog is not None:  # 현재 대화창이 설정되어 있는 경우
                    TextEvent.process_next_event()  # 다음 대화창 이벤트 처리

                    if TextEvent.dialog_delayed: # 다음 대화로 진행되어야 하는 경우
                        self.sign.refresh()  # 말풍선 재렌더링

                    if not TextEvent.dialog_closed:  # 대화창이 닫혀 있지 않은 경우
                        pygame.time.set_timer(CONST.PYGAME_EVENT_DIALOG, 1, 1)  # 대화 하는동안 관련 이벤트 처리

                    # 주인공 애니메이션을 기본으로 설정
                    MapManager.current.player.sprites.status = "stay"

                    return True
        return False
    # endregion
