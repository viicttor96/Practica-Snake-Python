import pygame
import sys
import random
import math

from sprites import *
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH,HEIGHT])
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_assets()
        self.reset()

    def load_assets(self):
        self.large_font = pygame.font.SysFont('arial', 100)
        self.small_font = pygame.font.SysFont('arial', 32)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            self.event()
            self.update()
            self.draw()
        self.game_over()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        self.snake.update()
        self.playing = self.playing and self.snake.alive
        hit = pygame.sprite.collide_rect(self.snake, self.fruit)
        if hit:
            self.snake.grow()
            self.fruit.teleport()
            self.score += 1

    def reset(self):
        self.snake = Snake(self, GRID_WIDTH//2, GRID_HEIGHT//2)
        self.fruit = Fruit()
        self.score = 0

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.draw_mobs()
        self.draw_HUD()
        pygame.display.flip()

    def draw_mobs(self):
        self.snake.draw(self.screen)
        self.fruit.draw(self.screen)

    def draw_HUD(self):
        score_text = self.small_font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10,10))

    def draw_grid(self):
        for x in range(0, WIDTH, TILE_SIZE):
            pygame.draw.line(self.screen, DARK_GREY, (x,0),(x, HEIGHT), 1)
            for y in range(0, HEIGHT, TILE_SIZE):
                pygame.draw.line(self.screen, DARK_GREY, (0,y),(WIDTH, y), 1)


    def main_menu(self):
        title_text = self.large_font.render(f'SNAAAKE', True, WHITE)
        subtite_text = self.small_font.render('PULSA UNA TECLA PARA EMPEZAR', True, LIGHT_GREY)
        self.screen.fill(BGCOLOR)
        self.screen.blit(title_text, (WIDTH//2 - title_text.get_rect().centerx,
                            HEIGHT//2 - title_text.get_rect().centery - 64))
        self.screen.blit(subtite_text, (WIDTH//2 - subtite_text.get_rect().centerx,
                            HEIGHT//2 - subtite_text.get_rect().centery))
        pygame.display.flip()
        in_main_menu = True
        while in_main_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    in_main_menu = False
        self.reset()
        self.run()


    def game_over(self):
        title_text = self.large_font.render(f'GAME OVER', True, WHITE)
        subtite_text = self.small_font.render(f'Score: {self.score} (press any key to continue)', True, LIGHT_GREY)
        self.screen.fill(BGCOLOR)
        self.screen.blit(title_text, (WIDTH//2 - title_text.get_rect().centerx,
                            HEIGHT//2 - title_text.get_rect().centery - 64))
        self.screen.blit(subtite_text, (WIDTH//2 - subtite_text.get_rect().centerx,
                            HEIGHT//2 - subtite_text.get_rect().centery))
        pygame.display.flip()
        in_game_over = True
        while in_game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    in_game_over = False
        self.main_menu()


game = Game()
game.main_menu()