import pygame
import pygame.image
import pygame.transform
import json
import pygame.sprite
# import Test_hero
pygame.init()   # Инициализация кода (включение)

width = 800
height = 800

game_over = 0
title_size = 40
clock = pygame.time.Clock () # объект отвечающий за работу со временем

fps = 60

score = 0
display = pygame.display.set_mode((width, height)) # Задает размер окна

pygame.display.set_caption("Counter-Strike 3") # Задает название окна
sound_jump = pygame.mixer.Sound('music/jump.wav')
sound_game_over = pygame.mixer.Sound('music/game_over.wav')
image = pygame.image.load('img_sprite/Fon.jpg') # загрузка изображения
rect = image.get_rect() # функция получения рамки

with open('levels/level1.json', 'r') as file:
    world_data = json.load(file)
level = 1
max_level = 2
def reset_level():

    player.rect.x = 100
    player.rect.y = 130
    lava_group.empty()
    exit_group.empty()
    with open(f'levels/level{level}.json', 'r') as file:
        world_data = json.load(file)
    world = World(world_data)
    return world
#pl1_image= pygame.image.load('img_sprite/player1.png')
#pl1_rect = pl1_image.get_rect()
class Hero:
    def __init__ (self, name):
        self.name = name
        self.lives = 3
        self.level = 1



    def greetings(self):
            print("привет, я" " " + self.name)
hero1 = Hero ('superman')
hero1.greetings()

class Player:
    def __init__(self):
        self.image = pygame.image.load('img_sprite/player1.png')
        self.image = pygame.transform.scale(self.image, (35, 70))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = height - 330
        self.gravity = 0
        self.jumped = False
        self.width = self.image.get_width()
        self.heigt = self.image.get_height()
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.direction = 0
        for num in range (1, 5):
            img_right = pygame.image.load(f'img_sprite/player{num}.png')
            img_right = pygame.transform.scale(img_right, (35, 70))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
            self.image = self.images_right[self.index]

    def update(self):
        global game_over
        x = 0
        y = 0
        walk_speed = 10
        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                self.gravity = -15
                self.jumped = True
                sound_jump.play()
            if key[pygame.K_a]:
                x -= 5
                self.direction = -1
                self.counter += 1
            if key[pygame.K_d]:
                x += 5
                self.direction = 1
                self.counter += 1

        if self.counter > walk_speed :
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            else:
                self.image = self.images_left[self.index]
        self.gravity +=1
        if self.gravity > 10:
            self.gravity = 10

        y += self.gravity
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + x, self.rect.y, self.width, self.heigt):
                x = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + y, self.width, self.heigt):
                if self.gravity < 0:
                    y = tile[1].bottom - self.rect.top
                    self.gravity = 0
                elif self.gravity > 0:
                    y = tile[1].top - self.rect.bottom
                    self.gravity = 0
                    self.jumped = False
        if self.rect.bottom > height:
            self.rect.bottom = height
        if pygame.sprite.spritecollide(self, lava_group, False):
            game_over = -1
        if pygame.sprite.spritecollide(self, exit_group, False):
            game_over = 1
        elif  game_over == -1:
            print("Game over")

        self.rect.x += x
        self.rect.y += y
        display.blit(self.image, self.rect)


class World():
    def __init__(self, data):
        dirtImg = pygame.image.load('img_sprite/dirt4.png')
        grassImg = pygame.image.load('img_sprite/grass.png')
        self.tile_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for title in row:
                 if title == 1 or title == 2:
                     images ={1 : dirtImg, 2 : grassImg }
                     img = pygame.transform.scale(images[title], (title_size, title_size))
                     img_rect = img.get_rect()
                     img_rect.x = col_count * title_size
                     img_rect.y = row_count * title_size
                     title = (img, img_rect)
                     self.tile_list.append(title)
                 elif title == 3:
                     lava = Lava(col_count * title_size, row_count * title_size + (title_size // 2))
                     lava_group.add(lava)
                 elif title == 5:
                     exit = Exit(col_count * title_size, row_count * title_size + (title_size // 2))
                     exit_group.add(exit)
                 elif title == 6:
                     coin = Coin(col_count * title_size, row_count * title_size + (title_size // 2))
                     coin_group.add(coin)
                 col_count += 1
            row_count += 1

    def draw (self):
        for tile in self.tile_list:
            display.blit(tile[0], tile[1])

class Lava (pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load('img_sprite/lava.png')
        self.image = pygame.transform.scale(img, (title_size, title_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Button:
    def __init__(self, x, y, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(center = (x, y))

    def draw(self):
        action = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        display.blit(self.image, self.rect)
        return action

restart_button = Button(width// 2, height//2, image = 'img_sprite/restart_btn.png')
start_button = Button(width// 2 - 150, height//2, image = 'img_sprite/start_btn.png')
exit_button = Button(width// 2 + 150, height//2, image = 'img_sprite/exit_btn.png')

class Exit (pygame.sprite.Sprite):
    def __init__(self, x , y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img_sprite/exit.png')
        self.image = pygame.transform.scale(img,(title_size, int (title_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin (pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img_sprite/coin.png')
        self.image = pygame.transform.scale(img, (title_size // 2, title_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

def draw_text (text, color, size, x, y):
    font = pygame.font.SysFont('Arial', size)
    img = font.render(text, True, color)
    display.blit(img, (x, y))

coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()

world = World(world_data)
player = Player()

run = True
main_menu = True
while run:
    clock.tick(fps) # ограничение работы цикла

    display.blit(image, rect) # функция отображения спрайтов на экране
    if main_menu:
        if start_button.draw():
            main_menu = False
            score = 0
        if exit_button.draw():
            run = False
            level = 1
            world = reset_level()
     #display.blit(pl1_image, pl1_rect)
    else:
        world.draw()
        lava_group.draw(display)
        exit_group.draw(display)
        coin_group.draw(display)
        draw_text(str(score), (255, 255, 255), 30,10, 10)
        player.update()
        lava_group.update()
        if pygame.sprite.spritecollide(player, coin_group, True):
            score +=1
            print(f'{score}')
        if game_over == -1:
            sound_game_over.play()
            if restart_button.draw():
                player = Player()
                #world = World(world_data)
                world = reset_level()
                game_over = 0

        if game_over == 1:
            game_over = 0
            if level < max_level:
                level +=1
                world = reset_level()
            else:
                print('win')
                main_menu = True
    for event in pygame.event.get(): # обработка различных событий
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update() # обновление экрана



pygame.quit()









