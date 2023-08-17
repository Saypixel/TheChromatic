from random import Random

import pygame

from characters.player import Player

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
    default: 'Ingame'

    def __init__(self):
        self.need_to_exit = False
        self.reload = False

        self.button_retry = None
        self.button_menu = None
        self.mouse_pos = CONFIG.get_mouse_pos()

        self.player = Player.get_from_sprite(SpriteCollection({
        'stay': SpriteHandler(Sprite('assets/images/chr_player_stay.png', 4, 1, size=(160, 270)))
        }, 'stay', position=(200, 225), scale=0.4), True)  # 주인공

        self.emilia = Player('assets/images/chr_emilia.png', (400, 220), 0.4)  # 에밀리아

        self.sign = Player('assets/images/sign_big.png', (300, 100), 0.3)
        self.hp = SpriteHandler(Sprite('assets/images/hp_bar.png', 31, 1, size=(500, 165), scale=0.4))

        self.spike = Player('assets/images/object_spike.png', (300, 315), 0.2)

        self.background = Player('assets/images/background.png', (0, 0), 1, True)
        self.ground = Player('assets/images/ground.png', (0, 0), 1, True, False)

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
                            case pygame.K_SPACE:
                                if self.emilia.is_bound(100, 100):
                                    TextEvent.process_next_event()

                                    if not TextEvent.dialog_delayed:
                                        self.sign.refresh()
                                    
                                    if not TextEvent.dialog_closed:
                                        pygame.time.set_timer(CONST.PYGAME_EVENT_DIALOG, 1, 1)
                                else:
                                    if not self.player.is_air:  # 다중 점프 금지
                                        self.player.move_y(10)  # 점프

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

        TextEvent.dialog = TextCollection([Text('*안녕!*'), Text('나는 에밀리아야.'), Text('*절대 *#하는게 #/아니라구../ 알겠지?')], self.sign.width)

        count = 0

        hp_count = 0 # 애니메이션
        last_grace_period = False

        while CONFIG.is_running and not self.need_to_exit:
            CONFIG.clock.tick(CONFIG.FPS)  # 프레임 조절

            count += 1
            self.mouse_pos = CONFIG.get_mouse_pos()

            CONFIG.surface.blit(self.background.image.convert(), (0, 0))
            CONFIG.surface.blit(self.ground.image, (0, 0))

            #region 플레이어 움직임
            sprite_player = self.player.sprites.get_sprite_handler().sprite

            if (self.player.velocity_x > 0 and sprite_player.flipped) or (self.player.velocity_x < 0 and not sprite_player.flipped):  # 방향이 반대인 경우
                    sprite_player.flip()
            #endregion
            #region 체력
            self.hp.group.draw(CONFIG.surface)

            if self.spike.is_bound(45, 100) and not GracePeriod.is_grace_period() and CONFIG.is_interactive() and CONFIG.is_movable():
                if hp_count == 24:
                    CONFIG.game_dead = True

                hp_count += 6
                self.player.hp -= 1
                self.player.move_y(5)
                
                GracePeriod.update()
                SFX.ATTACKED.play()

            if GracePeriod.is_grace_period():  # 무적시간인 경우
                alpha = CONFIG.random.randint(50, 200)
                sprite_player.set_alpha(alpha)

                last_grace_period = True
            elif last_grace_period:
                sprite_player.set_alpha(255)

                last_grace_period = False

            if count % 5 == 0:
                if self.hp.sprite.index < hp_count:  # hp 애니메이션 동기화
                    self.hp.group.update()
            #endregion
            #region 대화
            if not TextEvent.dialog_closed: 
                self.emilia.speech(self.sign)
            else:
                self.emilia.unspeech()
            #endregion

            if count == 10:
                count = 0
                
                sprite_player.update()

            process(process_ingame)
            process_ingame_movement()

            self.spike.render()

            self.emilia.render()
            self.player.render()

            World.process_gravity(self.player, 333)  # 중력 구현

            #region 사망 이벤트
            if CONFIG.game_dead:
                dead_background = pygame.image.load('assets/images/status3.png')
                dead_background = pygame.transform.rotate(dead_background, 90)
                dead_background = pygame.transform.scale_by(dead_background, 0.25)
                dead_background = pygame.transform.scale(dead_background, (dead_background.get_width() + 20, dead_background.get_height() - 20))

                dead = Font(Fonts.TITLE2, 40).render('죽었다이', (255, 255, 255))

                button_retry_image = pygame.image.load('assets/images/menu_play_rect.png')
                button_retry_image = pygame.transform.scale(button_retry_image, (150, 50))

                button_menu_image = pygame.image.load('assets/images/menu_play_rect.png')
                button_menu_image = pygame.transform.scale(button_retry_image, (210, 50))

                self.button_retry = Button(image=button_retry_image, pos=(320, 220),
                                           text_input='재도전', font=Font(Fonts.TITLE2, 30).to_pygame(), base_color='#ffffff',
                                           hovering_color='White')
                self.button_menu = Button(image=button_menu_image, pos=(320, 280),
                                           text_input='메뉴 화면으로', font=Font(Fonts.TITLE2, 30).to_pygame(), base_color='#ffffff',
                                           hovering_color='White')

                CONFIG.surface.blit(dead_background, (180, 120))
                CONFIG.surface.blit(dead, dead.get_rect(center=(320, 160)))

                for button in [self.button_retry, self.button_menu]:
                    button.change_color(self.mouse_pos)
                    button.update(CONFIG.surface)
            #endregion
            #region FPS 표시
            if CONFIG.game_fps:
                fps = round(CONFIG.clock.get_fps(), 1)
                fps_text = Font(Fonts.TITLE3, 20).render(str(fps), (255, 255, 255))

                CONFIG.surface.blit(fps_text, (585, 10))
            #endregion

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