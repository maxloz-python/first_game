import pygame.transform
from main import display


class Hero:
    def __init__ (self, name):
        self.name = name
        self.lives = 3
        self.level = 1

    def greetings(self):
            print("привет, я" " " + self.name)
hero1 = Hero ('superman')

class Player:
    def __init__(self):
        self.image = pygame.image.load('img_sprite/player1.png')
        self.image = pygame.transform.scale(self.image, (35,70))
        self.rect = self.image.get_rect()

    def update(self):
       display.blit(self.image, self.rect)

hero1.greetings()
