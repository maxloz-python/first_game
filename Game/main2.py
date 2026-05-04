import pygame
import pygame.image
import pygame.transform
import json
import pygame.sprite

pygame.init()  # Инициализация кода (включение)
width = 800
height = 800

title_size = 40
clock = pygame.time.Clock()  # объект отвечающий за работу со временем

fps = 60

display = pygame.display.set_mode((width, height))  # Задает размер окна


pygame.display.set_caption("Counter-Strike 3")  # Задает название окна

image = pygame.image.load('img_sprite/Fon.jpg')  # загрузка изображения
rect = image.get_rect()  # функция получения рамки

with open('levels/level1.json', 'r') as file:
    world_data = json.load(file)


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
        for num in range(1, 3):
            img_right = pygame.image.load(f'img_sprite/player{num}.png')
            img_right = pygame.transform.scale(img_right, (35, 70))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
            self.image = self.images_right[self.index]

    def update(self):
        x = 0
        y = 0
        walk_speed = 10
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False:
            self.gravity = -15
            # if self.rect.bottom != height:
            self.jumped = True
        if key[pygame.K_a]:
            x -= 5
            self.direction = -1
            self.counter += 1
        if key[pygame.K_d]:
            x += 5
            self.direction = 1
            self.counter += 1

        if self.counter > walk_speed:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            else:
                self.image = self.images_left[self.index]
        self.gravity += 1
        if self.gravity > 10:
            self.gravity = 10

        y += self.gravity
        for tile in world.tile_list:  ### Тут мы используем не класс World, а объект класса — world
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

        self.rect.x += x
        self.rect.y += y
        display.blit(self.image, self.rect)


class World():
    def __init__(self, data):
        # dirt_img=pygame.image.load('img_sprite')
        dirtImg = pygame.image.load('img_sprite/dirt4.png')
        grassImg = pygame.image.load('img_sprite/grass.png')
        self.tile_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for title in row:
                if title == 1 or title == 2:
                    images = {1: dirtImg, 2: grassImg}
                    img = pygame.transform.scale(images[title], (title_size, title_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * title_size
                    img_rect.y = row_count * title_size
                    title = (img, img_rect)  # Создаем rect для каждого блока
                    self.tile_list.append(title)
                elif title == 3:
                    lava = Lava(col_count * title_size, row_count * title_size + (title_size // 2))
                    lava_group.add(lava)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            display.blit(tile[0], tile[1])


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load('img_sprite/lava.png')
        self.image = pygame.transform.scale(img, (title_size, title_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


lava_group = pygame.sprite.Group()

world = World(world_data)
player = Player()

run = True
while run:
    clock.tick(fps)  # ограничение работы цикла

    display.blit(image, rect)  # функция отображения спрайтов на экране

    # display.blit(pl1_image, pl1_rect)
    world.draw()
    lava_group.draw(display)
    player.update()
    lava_group.update()
    for event in pygame.event.get():  # обработка различных событий
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()  # обновление экрана

pygame.quit()