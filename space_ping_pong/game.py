# команда для сборки игры в один исходный файл
# pyinstaller --onefile --name MyGame --icon=icon.ico -F --noconsole main5.py

import pygame as PG
import sys
from random import randint, shuffle
from math import sin, cos, radians
PG.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
SCREEN = PG.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )
FPS = 60
CLOCK = PG.time.Clock()

PG.mouse.set_visible(False)

PG.mixer.init()

sound_hit_1 = PG.mixer.Sound('./src/sounds/snd_bell.mp3')
sound_hit_2 = PG.mixer.Sound('./src/sounds/goal.mp3')

PG.mixer.music.load('./src/music/bgm_space_4.mp3')
PG.mixer.music.set_volume(0.7)
PG.mixer.music.play()

bg_music_list = [
    'space_ping_pong/src/music/deltarune_08 The Legend.mp3',
    'space_ping_pong/src/music/bgm_space_8.mp3',
    'space_ping_pong/src/music/bgm_space_7.mp3',
    'space_ping_pong/src/music/bgm_space_6.mp3',
    'space_ping_pong/src/music/bgm_space_5.mp3',
]

bg_music_index = 0

bg_image = PG.image.load('./src/images/space_bg_tile_1524x802px.jpg')
#bg_image = PG.transform.scale( bg_image, (960, 701) )
bg_draw_point = (-(1524 - SCREEN_WIDTH) / 2, -(802 - SCREEN_HEIGHT) / 2)

ball_image = PG.image.load('./src/images/ball_116x116px.png')
ball_image = PG.transform.scale( ball_image, (32, 32) )

player_left_image = PG.image.load('./src/images/p1_128x512px.png')
player_left_image = PG.transform.scale( player_left_image, (32, 128) )

player_right_image = PG.image.load('./src/images/p2_128x512px.png')
player_right_image = PG.transform.scale( player_right_image, (32, 128) )

enemy_image = PG.image.load('./src/images/p0_128x512px.png')
enemy_image = PG.transform.scale( enemy_image, (32, 200) )

class Label():
    def __init__(self, text, x, y, align = 'left', font_size = 36, color = (255, 255, 255)):
        self.font = PG.font.Font(None, font_size)
        self.align = align
        self.color = color
        self.x = x
        self.y = y
        self.render(text)
    
    def render(self, text):
        self.text = self.font.render(text, True, self.color)
        self.rect = self.text.get_rect()
        self.rect.centery = self.y
        if self.align == 'left': self.rect.left = self.x
        elif self.align == 'right': self.rect.right = self.x
        else : self.rect.centerx = self.x

class Ball(PG.sprite.Sprite):
    def __init__(self):
        PG.sprite.Sprite.__init__(self)
        self.image = ball_image
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH * 0.5
        self.rect.centery = SCREEN_HEIGHT * 0.5
        self.speed = 5
        self.r_speed = 1
        self.r_angle = 0
        self.speed_label = Label(f'Ball speed: {self.speed}', SCREEN_WIDTH * 0.5, 30, 'center', 36, (255, 255, 0))
        if randint(0, 1) == 1:
            if randint(0, 1) == 1 : self.direction = 315
            else : self.direction = 45
        else:
            if randint(0, 1) == 1 : self.direction = 135
            else : self.direction = 225

    def move(self):
        radians_direction = radians(self.direction)
        self.rect.centerx += cos(radians_direction) * self.speed
        self.rect.centery += sin(radians_direction) * self.speed

        if self.rect.top < 0:
            self.rect.top = 0
            if self.direction == 315 : self.direction = 45
            else : self.direction = 135

        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            if self.direction == 45 : self.direction = 315
            else : self.direction = 225

        elif self.rect.x < 0:
            p2.get_score()
            self.restart()

        elif self.rect.right > SCREEN_WIDTH:
            p1.get_score()
            self.restart()

        elif self.rect.colliderect(p1.rect):
            self.rect.left = p1.rect.right
            self.speed += 1
            self.r_speed += 1
            if self.direction == 135 : self.direction = 45
            else : self.direction = 315
            '''if self.direction == 150 : self.direction = 30
            else : self.direction = 210'''

            '''if self.direction == 165 : self.direction = 14
            else : self.direction = 195'''

        elif self.rect.colliderect(p2.rect):
            self.rect.right = p2.rect.left
            self.speed += 1
            self.r_speed += 1
            if self.direction == 45 : self.direction = 135
            else : self.direction = 225
            
        elif self.rect.colliderect(enemy.rect):
            self.rect.left = enemy.rect.right
            if self.direction > 270 and  self.direction < 90:  
                if self.direction == 45 : self.direction = 135
                else : self.direction = 315
                '''if self.direction == 30 : self.direction = 150
                else : self.direction = 330
                if self.direction == 15 : self.direction = 165
                else : self.direction = 345
                if self.direction == 60 : self.direction = 120
                else : self.direction = 300
                if self.direction == 75 : self.direction = 285
                else : self.direction = 105'''

                if self.direction == 315 : self.direction = 225
                else : self.direction = 45
                '''if self.direction == 330 : self.direction = 210
                else : self.direction = 30
                if self.direction == 345 : self.direction = 195
                else : self.direction = 15
                if self.direction == 300 : self.direction = 240
                else : self.direction = 60
                if self.direction == 105 : self.direction = 285
                else : self.direction = 75'''
                

            else: 

                if self.direction == 165 : self.direction = 14
                else : self.direction = 195

                if self.direction == 135 : self.direction = 45
                else : self.direction = 315

                if self.direction == 150 : self.direction = 30
                else : self.direction = 210

                if self.direction == 165 : self.direction = 14
                else : self.direction = 195


            

    def restart(self):
        self.rect.centerx = SCREEN_WIDTH * 0.5
        self.rect.centery = SCREEN_HEIGHT * 0.5
        self.speed = 5
        self.r_speed = 1
        self.speed_label.render(f'Ball speed: {self.speed}')
        self.direction = randint(0, 355)

    def update(self):
        self.move()
        self.r_angle += self.r_speed
        self.rotated_image = PG.transform.rotate(self.image, self.r_angle)
        self.rotated_rect = self.rotated_image.get_rect(center=self.rect.center)
        SCREEN.blit(self.rotated_image, self.rotated_rect)
        SCREEN.blit(self.speed_label.text, self.speed_label.rect)

class Player(PG.sprite.Sprite):
    def __init__(self, is_left):
        PG.sprite.Sprite.__init__(self)
        self.image = player_left_image if is_left else player_right_image
        self.rect = self.image.get_rect()
        self.rect.x = 0 if is_left else SCREEN_WIDTH - self.rect.width
        self.rect.centery = SCREEN_HEIGHT * 0.5
        self.score = 0
        self.speed = 5
        self.isPlayer = True
        if is_left : self.score_label = Label(f'Score: {self.score}', 15, 30, 'left', 36, (0, 255, 255))
        else : self.score_label = Label(f'Score: {self.score}', SCREEN_WIDTH - 15, 30, 'right', 36, (255, 0, 255))

    def get_score(self):
        self.score += 1
        self.score_label.render(f'Score: {self.score}')
class Player_left(Player):
    def __init__(self):
        super().__init__(True)
        
    def update(self):
        if self.isPlayer:
            KEY = PG.key.get_pressed()  
            if KEY[PG.K_w]:
                self.rect.y -= self.speed
                if self.rect.y < 0 : self.rect.y = 0
            elif KEY[PG.K_s]:
                self.rect.y += self.speed
                if self.rect.bottom > SCREEN_HEIGHT : self.rect.bottom = SCREEN_HEIGHT
        else:
            if ball.rect.centery > self.rect.centery : self.rect.centery += 1
            if ball.rect.centery < self.rect.centery : self.rect.centery -= 1
        SCREEN.blit(self.image, self.rect)
        SCREEN.blit(self.score_label.text, self.score_label.rect)

class Player_Right(Player):
    def __init__(self):
        super().__init__(False)

    def update(self):
        if self.isPlayer:
            KEY = PG.key.get_pressed()
            if KEY[PG.K_UP]:
                self.rect.y -= self.speed
                if self.rect.y < 0 : self.rect.y = 0
            elif KEY[PG.K_DOWN]:
                self.rect.y += self.speed
                if self.rect.bottom > SCREEN_HEIGHT : self.rect.bottom = SCREEN_HEIGHT
        else:
            if ball.rect.centery > self.rect.centery : self.rect.centery += 1
            if ball.rect.centery < self.rect.centery : self.rect.centery -= 1
        SCREEN.blit(self.image, self.rect)
        SCREEN.blit(self.score_label.text, self.score_label.rect) 


class Enemy(PG.sprite.Sprite):
    def __init__(self):
        PG.sprite.Sprite.__init__(self)
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH * 0.5
        self.is_to_top = randint(0,1) == 1
        if self.is_to_top : self.rect.bottom = SCREEN_HEIGHT
        else : self.rect.top = 0
        self.speed = 5


    def update(self):
        if self.is_to_top:
            self.rect.y -= self.speed
            if self.rect.top < 0:
                self.rect.top = 0
                self.is_to_top = False
        else:
            self.rect.y += self.speed
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
                self.is_to_top = True
        SCREEN.blit(self.image, self.rect)



        

        
 
p1 = Player_left()
p2 = Player_Right()
ball = Ball()
enemy = Enemy()

tick = 0 # создаем счетчик кадров
game_loop_is = True

# ГЛАВНыЙ ЦИКЛ ИГРЫ
while game_loop_is:
    CLOCK.tick(FPS)
    tick += 1

    for event in PG.event.get():
        if event.type == PG.QUIT or (event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE):
            game_loop_is = False
        elif event.type == PG.KEYUP and event.key == PG.K_1 : p1.isPlayer = not p1.isPlayer
        elif event.type == PG.KEYUP and event.key == PG.K_2 : p2.isPlayer = not p2.isPlayer

    SCREEN.blit(bg_image, bg_draw_point)
    p1.update()
    p2.update()
    ball.update()
    enemy.update()

    PG.display.flip()

PG.quit()
sys.exit()