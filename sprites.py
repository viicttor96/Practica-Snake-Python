import pygame
from settings import *
import random

class Snake(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.head_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.head_image.fill(YELLOW)
        self.rect = self.head_image.get_rect()
        self.tail_part_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.tail_part_image.fill(ORANGE)
        self.game = game
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.speed = 10
        self.cool_down = 1
        self.tail = []
        self.tail_length = 2
        self.alive = True

    def update(self):
        self.move()
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE

    def grow(self):
        self.tail_length += 1
        if self.speed <30:
            self.speed +=1
    
    def draw(self, surface):
        surface.blit(self.head_image, self.rect)
        for part in self.tail:
            screen_x = part[0] * TILE_SIZE
            screen_y = part[1] * TILE_SIZE
            surface.blit(self.tail_part_image, (screen_x, screen_y))

    def move(self):
        self.cool_down -= self.speed * self.game.dt
        self.keyboard_input()
        if self.cool_down < 0:           #acumula el turno para controlar la velocidad
            self.update_tail()
            self.x += self.dx
            self.y += self.dy
            self.cool_down = 1
            self.stay_within_world()
            self.check_death()

    def check_death(self):
        is_moving = self.dx != 0 or self.dy != 0
        head = (self.x, self.y)
        if head in self.tail and is_moving:
            self.alive = False
    
    def update_tail(self):
        self.tail.insert(0, (self.x, self.y))
        if len(self.tail) >= self.tail_length:
            self.tail.pop()
        
    def stay_within_world(self):        #controla que cuando se salga por un lado vuelva por el opuesto
        if self.x > GRID_WIDTH-1:
            self.x = 0
        elif self.x < 0:
            self.x = GRID_WIDTH-1 
        if self.y > GRID_HEIGHT-1:
            self.y = 0
        elif self.y < 0:
            self.y = GRID_HEIGHT-1

    def keyboard_input(self):
        key_state = pygame.key.get_pressed()       #lee que teclas se están pulsando
        if key_state[pygame.K_LEFT] and self.dx == 0:
            self.dx = -1
            self.dy = 0
        elif key_state[pygame.K_RIGHT] and self.dx == 0:
            self.dx = 1
            self.dy = 0
        if key_state[pygame.K_UP]and self.dy == 0:
            self.dy = -1
            self.dx = 0
        elif key_state[pygame.K_DOWN] and self.dy == 0:
            self.dy = 1
            self.dx = 0

class Fruit(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.teleport()

    def teleport(self):
        self.x = random.randint(0, GRID_WIDTH-1)
        self.y = random.randint(0, GRID_HEIGHT-1)
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE

    def draw(self, surface):
        surface.blit(self.image, self.rect)