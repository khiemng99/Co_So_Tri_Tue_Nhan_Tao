import pygame
from colors3 import CELL_COLOR
from colors3 import BLOCK_SIZE
from colors3 import GAP_SIZE
from colors3 import BORDER_COLOR


class Grid:

    def __init__(self, width, height):
        self.width = width+1
        self.height = height+1

    def draw(self, surface, CELL_COLOR = CELL_COLOR, BLOCK_SIZE = BLOCK_SIZE, GAP_SIZE = GAP_SIZE):
        for i in range(self.width):
            for j in range(self.height):
                if i == 0 or j == 0 or i == self.width - 1 or j == self.height - 1:
                    pygame.draw.rect(surface, BORDER_COLOR,
                                     (i * (BLOCK_SIZE + GAP_SIZE), j * (BLOCK_SIZE + GAP_SIZE), BLOCK_SIZE, BLOCK_SIZE))
                else:
                    pygame.draw.rect(surface, CELL_COLOR,
                                 (i * (BLOCK_SIZE + GAP_SIZE), j * (BLOCK_SIZE + GAP_SIZE), BLOCK_SIZE, BLOCK_SIZE))

    def get_cell_value(self, x, y):
        return self.grid[y][x]

    def set_cell_value(self, x, y, value):
        self.grid[y][x] = value

    def print_grid(self):
        for row in self.grid:
            print(row)
