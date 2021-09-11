import pygame
import math
import random
from pygame.math import Vector2

songs = ["battle1.mp3", "battle2.mp3", "battle3.mp3"]

BACK_GREY = (120,120,120)
WHITE = (255,255,255)
BACKGROUND = (255, 254, 216)
BLACK = (0,0,0)
BROWN = (119, 78, 34)
YELLOW = (255, 242, 104)
DARK_GREY = (220,220,220)
RED = (255,0,0)

SONG_END = pygame.USEREVENT + 1

pygame.mixer.music.set_endevent(SONG_END)

score = 0
life = 3
n = 0
enemy_speed = 5

ymovement = 0
xmovement = 0

x_speed = 0
y_speed = 0

x_coord = 300
y_coord = 300

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

class Monster(pygame.sprite.Sprite):

    def __init__(self, width, height):

        super().__init__()
        
        self.image = pygame.image.load("monster.png").convert()

        self.image.set_colorkey(BACK_GREY)

        self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect()

        self.change_x = 0
        self.change_y = 0

    def update(self):

        self.x = SCREEN_WIDTH / 2 - self.rect.x
        self.y = SCREEN_HEIGHT / 2- self.rect.y

        hyp = (self.x **2 + self.y **2)**(1/2)
        self.x /= hyp
        self.y /= hyp

        self.rect.x += self.x * enemy_speed + self.change_x
        self.rect.y += self.y * enemy_speed + self.change_y
        
    def left(self):
        self.change_x = -4
        
    def right(self):
        self.change_x = 4
        
    def up(self):
        self.change_y = -4
        
    def down(self):
        self.change_y = 4

    def stop_x(self):
        self.change_x = 0

    def stop_y(self):
        self.change_y = 0
        
class Player(pygame.sprite.Sprite):

    def __init__(self, width, height):

        super().__init__()
        
        self.image = pygame.image.load("character_down.png").convert()

        self.image.set_colorkey(BACK_GREY)

        self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect()

        self.change_x = 0
        self.change_y = 0

        self.rect.x = 800
        self.rect.y = 450

class Sword(pygame.sprite.Sprite):

    def __init__(self, pos):
        
        super().__init__()

        self.image = pygame.image.load("sword.png").convert()
        self.image.set_colorkey(BLACK)

        self.orig_image = self.image

        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.offset = Vector2(30, 0)
        
        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.rotate()

    def rotate(self):

        direction = pygame.mouse.get_pos() - self.pos
        coords = direction.as_polar()
        radius = coords[0]
        angle = coords[1]
        self.image = pygame.transform.rotate(self.orig_image, -angle)

        rotate_offset = self.offset.rotate(angle)
        
        self.rect = self.image.get_rect(center=self.pos+rotate_offset)

class Gun(pygame.sprite.Sprite):

    def __init__(self, pos):
        
        super().__init__()

        self.image = pygame.image.load("tec_9.png").convert()
        self.image.set_colorkey(BLACK)

        self.orig_image = self.image

        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)

    def update(self):
        self.rotate()

    def rotate(self):

        direction = pygame.mouse.get_pos() - self.pos
        coords = direction.as_polar()
        radius = coords[0]
        angle = coords[1]
        self.image = pygame.transform.rotate(self.orig_image, -angle)
        
        self.rect = self.image.get_rect(center=self.rect.center)

class Bullet(pygame.sprite.Sprite):
 
    def __init__(self, start_x, start_y, dest_x, dest_y, xmovement, ymovement):
 
        super().__init__()
 
        self.image = pygame.Surface([4, 4])
        self.image.fill(BLACK)
 
        self.rect = self.image.get_rect()
 
        self.rect.x = start_x
        self.rect.y = start_y
 
        self.floating_point_x = start_x
        self.floating_point_y = start_y
 
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff);
 
        velocity = 10
        self.change_x = math.cos(angle) * velocity
        self.change_y = math.sin(angle) * velocity
 
    def update(self):
 
        self.floating_point_y += self.change_y + ymovement
        self.floating_point_x += self.change_x + xmovement
 
        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)
 
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()

class Grass(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = pygame.image.load("grass.png").convert()
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()

        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y

    def left(self):
        self.change_x = -4
        
    def right(self):
        self.change_x = 4
        
    def up(self):
        self.change_y = -4
        
    def down(self):
        self.change_y = 4

    def stop_x(self):
        self.change_x = 0

    def stop_y(self):
        self.change_y = 0

def play_next_song():
    global songs
    songs = songs[1:] + [songs[0]]
    pygame.mixer.music.load(songs[0])
    pygame.mixer.music.play()
    
pygame.init()
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("King of the Dungeon")

pygame.mixer.music.load("battle3.mp3")
pygame.mixer.music.play(0)

pygame.mixer.music.set_volume(0.4)

gunshot = pygame.mixer.Sound('shoot.wav')
pygame.mixer.Sound.set_volume(gunshot, 0.05)

gameover = pygame.mixer.Sound("game_over.wav")
pygame.mixer.Sound.set_volume(gameover, 0.1)

font = pygame.font.SysFont("comicsansms", 72)

monster_list = pygame.sprite.Group()

bullet_list = pygame.sprite.Group()

all_sprites_list = pygame.sprite.Group()

hit = pygame.sprite.Group()

grass_list = pygame.sprite.Group()

for i in range(40):

    grass = Grass()
    
    grass.rect.y = random.randrange(0, 900)
    grass.rect.x = random.randrange(0, 1600)

    grass_list.add(grass)
    all_sprites_list.add(grass)
    
for i in range(15):
    aMonster = Monster(40, 60)
    left = random.randrange(10)
    top = random.randrange(10)
    right = random.randrange(10)
    bottom = random.randrange(10)

    if left >= top and left >= right and left >= bottom:
        aMonster.rect.y = random.randrange(-100, 1000)
        aMonster.rect.x = random.randrange(-100, 0)
    elif top > left and top > right and top > bottom:
        aMonster.rect.y = random.randrange(-100, 0)
        aMonster.rect.x = random.randrange(-100, 1700)
    elif right > left and right > top and right > bottom:
        aMonster.rect.y = random.randrange(-100, 1000)
        aMonster.rect.x = random.randrange(1600, 1700)
    elif bottom > left and bottom > top and bottom > right:
        aMonster.rect.y = random.randrange(900, 1000)
        aMonster.rect.x = random.randrange(-100, 1700)

    monster_list.add(aMonster)
    all_sprites_list.add(aMonster)

character = Player(40, 60)
all_sprites_list.add(character)
gun = Gun((835, 495))
all_sprites_list.add(gun)
guns = True
sword = Sword((835, 495))

done = False

clock = pygame.time.Clock()

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT or event.key == pygame.K_a:

                for monster in monster_list:
                    
                    monster.right()

                for grass in grass_list:
                    grass.right()

                xmovement = 4
                
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:

                for monster in monster_list:
                    
                    monster.left()

                for grass in grass_list:
                    grass.left()

                xmovement = -4
                
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                
                for monster in monster_list:
                    
                    monster.down()

                for grass in grass_list:
                    grass.down()

                ymovement = 4

                
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                
                for monster in monster_list:
                    
                    monster.up()
                    
                for grass in grass_list:
                    grass.up()

                ymovement = -4

            if event.key == pygame.K_1:

                all_sprites_list.remove(gun)
                all_sprites_list.remove(sword)

                all_sprites_list.add(gun)
                
                guns = True

            if event.key == pygame.K_2:

                all_sprites_list.remove(sword)
                all_sprites_list.remove(gun)

                all_sprites_list.add(sword)
                
                guns = False

        elif event.type == pygame.KEYUP:
                     
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                
                for monster in monster_list:
                    
                    monster.stop_x()
                    
                for grass in grass_list:
                    
                    grass.stop_x()
                xmovement = 0
                    
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                
                for monster in monster_list:
                    
                    monster.stop_y()

                for grass in grass_list:
                    
                    grass.stop_y()

                ymovement = 0

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
 
            mouse_x = pos[0]
            mouse_y = pos[1]

            if guns == True:

                bullet = Bullet(character.rect.x + 40, character.rect.y + 40, mouse_x, mouse_y, xmovement, ymovement)

                all_sprites_list.add(bullet)
                bullet_list.add(bullet)

                gunshot.play()

        if event.type == SONG_END:
            play_next_song()
            
    screen.fill(BACKGROUND)

    if guns == False:

        hit = pygame.sprite.spritecollide(sword, monster_list, False)

        for aMonster in hit:

            left = random.randrange(10)
            top = random.randrange(10)
            right = random.randrange(10)
            bottom = random.randrange(10)

            if left >= top and left >= right and left >= bottom:
                aMonster.rect.y = random.randrange(-100, 1000)
                aMonster.rect.x = random.randrange(-100, 0)
            elif top > left and top > right and top > bottom:
                aMonster.rect.y = random.randrange(-100, 0)
                aMonster.rect.x = random.randrange(-100, 1700)
            elif right > left and right > top and right > bottom:
                aMonster.rect.y = random.randrange(-100, 1000)
                aMonster.rect.x = random.randrange(1600, 1700)
            elif bottom > left and bottom > top and bottom > right:
                aMonster.rect.y = random.randrange(900, 1000)
                aMonster.rect.x = random.randrange(-100, 1700)
        
            score += 1
            print("monster destroyed with sword. Score: ", score)

    for bullet in bullet_list:
        
        hit2 = pygame.sprite.spritecollide(bullet, monster_list, False)       

        for aMonster in hit2:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

            left = random.randrange(10)
            top = random.randrange(10)
            right = random.randrange(10)
            bottom = random.randrange(10)

            if left >= top and left >= right and left >= bottom:
                aMonster.rect.y = random.randrange(-100, 1000)
                aMonster.rect.x = random.randrange(-100, 0)
            elif top > left and top > right and top > bottom:
                aMonster.rect.y = random.randrange(-100, 0)
                aMonster.rect.x = random.randrange(-100, 1700)
            elif right > left and right > top and right > bottom:
                aMonster.rect.y = random.randrange(-100, 1000)
                aMonster.rect.x = random.randrange(1600, 1700)
            elif bottom > left and bottom > top and bottom > right:
                aMonster.rect.y = random.randrange(900, 1000)
                aMonster.rect.x = random.randrange(-100, 1700)
                
            score += 1
            print("monster destroyed with bullet. Score: ", score)

        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

    for grass in grass_list:

        if grass.rect.x < -10 or grass.rect.x > 1610:
                left = random.randrange(10)
                top = random.randrange(10)
                right = random.randrange(10)
                bottom = random.randrange(10)

                if left >= top and left >= right and left >= bottom:
                    grass.rect.y = random.randrange(-100, 1000)
                    grass.rect.x = random.randrange(-100, 0)
                elif top > left and top > right and top > bottom:
                    grass.rect.y = random.randrange(-100, 0)
                    grass.rect.x = random.randrange(-100, 1700)
                elif right > left and right > top and right > bottom:
                    grass.rect.y = random.randrange(-100, 1000)
                    grass.rect.x = random.randrange(1600, 1700)
                elif bottom > left and bottom > top and bottom > right:
                    grass.rect.y = random.randrange(900, 1000)
                    grass.rect.x = random.randrange(-100, 1700)

        if grass.rect.y < -10 or grass.rect.y > 910:
            
                left = random.randrange(10)
                top = random.randrange(10)
                right = random.randrange(10)
                bottom = random.randrange(10)

                if left >= top and left >= right and left >= bottom:
                    grass.rect.y = random.randrange(-100, 1000)
                    grass.rect.x = random.randrange(-100, 0)
                elif top > left and top > right and top > bottom:
                    grass.rect.y = random.randrange(-100, 0)
                    grass.rect.x = random.randrange(-100, 1700)
                elif right > left and right > top and right > bottom:
                    grass.rect.y = random.randrange(-100, 1000)
                    grass.rect.x = random.randrange(1600, 1700)
                elif bottom > left and bottom > top and bottom > right:
                    grass.rect.y = random.randrange(900, 1000)
                    grass.rect.x = random.randrange(-100, 1700)
                

        

    hit3 = pygame.sprite.spritecollide(character, monster_list, False)

    for aMonster in hit3:
        
        life -= 1
        left = random.randrange(10)
        top = random.randrange(10)
        right = random.randrange(10)
        bottom = random.randrange(10)

        if left >= top and left >= right and left >= bottom:
            aMonster.rect.y = random.randrange(-100, 1000)
            aMonster.rect.x = random.randrange(-100, 0)
        elif top > left and top > right and top > bottom:
            aMonster.rect.y = random.randrange(-100, 0)
            aMonster.rect.x = random.randrange(-100, 1700)
        elif right > left and right > top and right > bottom:
            aMonster.rect.y = random.randrange(-100, 1000)
            aMonster.rect.x = random.randrange(1600, 1700)
        elif bottom > left and bottom > top and bottom > right:
            aMonster.rect.y = random.randrange(900, 1000)
            aMonster.rect.x = random.randrange(-100, 1700)

    all_sprites_list.update()

    all_sprites_list.draw(screen)

    if life == 3:
        pygame.draw.polygon(screen, RED, [(20, 50), (10, 20), (30, 10), (50, 20), (70, 10), (90, 20), (80, 50), (50, 70)])
        pygame.draw.polygon(screen, RED, [(100, 50), (90, 20), (110, 10), (130, 20), (150, 10), (170, 20), (160, 50), (130, 70)])
        pygame.draw.polygon(screen, RED, [(180, 50), (170, 20), (190, 10), (210, 20), (230, 10), (250, 20), (240, 50), (210, 70)])

    if life == 2:
        pygame.draw.polygon(screen, RED, [(20, 50), (10, 20), (30, 10), (50, 20), (70, 10), (90, 20), (80, 50), (50, 70)])
        pygame.draw.polygon(screen, RED, [(100, 50), (90, 20), (110, 10), (130, 20), (150, 10), (170, 20), (160, 50), (130, 70)])

    if life == 1:
        pygame.draw.polygon(screen, RED, [(20, 50), (10, 20), (30, 10), (50, 20), (70, 10), (90, 20), (80, 50), (50, 70)])

    text = font.render("Score : "+(str(score)), True, BLACK)

    screen.blit(text,(10, SCREEN_HEIGHT - 20 - text.get_height()))

    pygame.display.flip()
    clock.tick(60)

    if life <= 0:
        print("game over")

        gameover_text = font.render("Game Over", True, BLACK)

        screen.blit(gameover_text,(SCREEN_WIDTH / 2 - text.get_width(), SCREEN_HEIGHT / 2 - text.get_height()))

        pygame.display.flip()

        done = True

pygame.mixer.music.set_volume(0)
pygame.time.delay(300)
gameover.play()
pygame.time.delay(2000)
pygame.quit()
