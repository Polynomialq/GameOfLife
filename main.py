import pygame
from pygame.locals import *
from random import randint
from pprint import pprint as pp
from itertools import product
import copy


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 20, max_gen: int = 100, cur_gen: int = 0):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        # Максимальное и нынешнее поколение
        self.max_gen = max_gen
        self.cur_gen = 0
        self.is_changing = True
        self.is_paused = True

    # Рисуем линии
    def draw_lines(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('gray'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('gray'),
                             (0, y), (self.width, y))

    # Заполняем двумерный массив, наше поле
    def create_grid(self, randomize: bool = False):
        if randomize:
            self.grid = [[randint(0, 1) for j in range(self.cell_width)] for i in range(self.cell_height)]
        else:
            self.grid = [[0 for j in range(self.cell_width)] for i in range(self.cell_height)]

        # Для дебага, работает ли нахождение соседей правильно
        #for i in range(self.cell_width):
        #    for j in range(self.cell_height):
        #        print(list(self.get_neighbours((i, j))), len(list(self.get_neighbours((i, j)))))
        return self.grid

    # Заполняем ячейки цветом в зависимости от значения
    def draw_cells(self):
        for i in range(self.cell_width):
            for j in range(self.cell_height):
                if self.grid[j][i] == 1:
                    pygame.draw.rect(self.screen, pygame.Color("yellow"),
                                     pygame.Rect(i * self.cell_size, j * self.cell_size, self.cell_size,
                                                  self.cell_size))

    # Возвращаем список соседних клеток
    def get_neighbours(self, cell):
        size = [self.cell_width, self.cell_height]
        for c in product(*(range(n - 1, n + 2) for n in cell)):
            if c != cell and all(0 <= i < bound for i, bound in zip(c, size)) and self.grid[c[0]][c[1]]:
                yield c

    # Считаем следующее поколение
    def get_next_generation(self):
        next_grid = copy.deepcopy(self.grid)
        for i in range(self.cell_width):
            for j in range(self.cell_height):
                if self.grid[i][j] and len(list(self.get_neighbours((i, j)))) not in (2, 3):
                    next_grid[i][j] = 0
                if self.grid[i][j] == 0 and len(list(self.get_neighbours((i, j)))) == 3:
                    next_grid[i][j] = 1
        if next_grid == self.grid:
            self.is_changing = False
        self.grid = next_grid
        self.cur_gen += 1

    # Обновить экран
    def update(self):
        self.screen.fill(pygame.Color('purple'))
        self.draw_cells()

        # Рисует сетку
        #self.draw_lines()
        self.draw()
        pygame.display.flip()
        clock.tick(self.speed)

    def is_max_generation_exceeded(self):
        if self.max_gen == 0:
            return False
        if self.cur_gen == self.max_gen:
            return True
        return False

    def draw(self):
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            row = y // self.cell_size
            col = x // self.cell_size
            self.grid[row][col] = 1


if __name__ == '__main__':
    # Инициализируем pygame
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Game of Life (Нажмите пробел, чтобы снять с паузы)')

    life = GameOfLife(width=1000, height=1000, cell_size=10, max_gen=0, speed=15)
    grid = life.create_grid(randomize=True)

    life.update()
    while not life.is_max_generation_exceeded():
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            # Пробел ставит на паузу
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    life.is_paused = not life.is_paused
                    pygame.display.set_caption('Game of Life')
        life.update()
        if not life.is_paused:
            life.get_next_generation()

    else:
        pygame.quit()

