import pygame

from characters.player import Player
from components.config import CONFIG, CONST, debug
from components.events import process
from components.events.text import TextEvent
from components.text import Text
from components.text.text_collection import TextCollection
from components.sprite import Sprite

player = Player.get_from_sprite(Sprite('assets/images/chr_player_stay.png', 4, 1, (200, 225), (160, 315), (35, 50), 0.4), True)  # 주인공
emilia = Player('assets/images/chr_emilia.png', (400, 220), 0.4)  # 에밀리아

sign = Player('assets/images/sign_big.png', (300, 100), 0.3)
hp = pygame.sprite.Group(Sprite('assets/images/hp_bar.png', 31, 1, (0, 0), (500, 165), (0, 0), 0.4))

background = Player('assets/images/background.png', (0, 0), 1, True)
ground = Player('assets/images/ground.png', (0, 0), 1, True, False)

def update_ingame():
    global player

    def process_ingame(event: pygame.event.Event):
        """인게임 이벤트 처리용 (process() child 함수)"""
        global player

        match event.type:
            case pygame.KEYDOWN:
                if CONFIG.is_movable():  # 플레이어가 움직일 수 있을 때 (상호작용 포함)
                    match event.key:
                        case pygame.K_a | pygame.K_LEFT:  # 왼쪽으로 이동
                            player.move(-1)
                        case pygame.K_d | pygame.K_RIGHT:  # 오른쪽으로 이동
                            player.move(1)

            case pygame.KEYUP:
                if CONFIG.is_interactive():
                    match event.key:
                        case pygame.K_SPACE:
                            if emilia.is_bound(100):
                                TextEvent.process_next_event()

                                if not TextEvent.dialog_delayed:
                                    sign.refresh()
                                
                                if not TextEvent.dialog_closed:
                                    pygame.time.set_timer(CONST.PYGAME_EVENT_DIALOG, 1, 1)

            case CONST.PYGAME_EVENT_DIALOG:  # 텍스트 애니메이션 이벤트
                if CONFIG.is_interactive():
                    TextEvent.process_animation_event(sign.image)

            case CONST.PYGAME_EVENT_DIALOG_NEXT_INDEX:
                TextEvent.process_animation_next_event()

    TextEvent.dialog = TextCollection([Text('*안녕!*'), Text('나는 에밀리아야.'), Text('*절대 *#하는게 #/아니라구../ 알겠지?')], sign.width)
    pygame.time.set_timer(CONST.PYGAME_EVENT_DIALOG, 1, 1)
    count = 0

    while CONFIG.is_running:
        CONFIG.clock.tick(CONFIG.FPS)  # 프레임 조절
        CONFIG.surface.blit(background.image, (0, 0))
        CONFIG.surface.blit(ground.image, (0, 0))

        hp.draw(CONFIG.surface)

        count += 1

        if count % 5 == 0:
            hp.update()

        if (player.velocity > 0 and player.sprite.flipped) or (player.velocity < 0 and not player.sprite.flipped):  # 방향이 반대인 경우
                player.sprite.flip()

        if count == 10:
            count = 0
            player.sprite.update()

        if not TextEvent.dialog_closed: 
            emilia.speech(sign)
        else:
            emilia.unspeech()

        process(process_ingame)

        emilia.render()
        player.render()

        CONFIG.update_screen()