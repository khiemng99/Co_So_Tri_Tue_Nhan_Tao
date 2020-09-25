import pygame
import numpy as np
import itertools as itt
import copy
import sys
from algos import Point
from algos import BFS
from algos import GREEDY
from algos import ASTAR
from grid3 import Grid
import time
from bresenham import bresenham
from colors3 import BLOCK_SIZE
from colors3 import START_COLOR
from colors3 import OBSTACLE_COLOR
from colors3 import GOAL_COLOR
from colors3 import PATH_COLOR
from colors3 import MUST_PASS_COLOR


f = open("input.txt", mode="r")

# Read the first line which contains numbers <width,height> limiting space
line = f.readline()
value = line.strip('\n').split(',')
WIDTH, HEIGHT = map(int, value)

# Read the second line which contains Cartesian Coordinates for starting point, goal point and maybe other target points 
line = f.readline()
value = line.strip('\n').split(',')  # Put all coordinates (string) to list
# Casting coordinates from string to int and create Point from these, then put them in list 
points = [Point(int(x), int(y)) for x, y in zip(value[::2], value[1::2])]  
start = points[0]
goal = points[1]

# Read the third line to get the number of polygons
line = f.readline()
poly_num = int(line.strip('\n'))
poly = []
for i in range(0, poly_num):  # Every lines contain a set of coordinates to make polygon points
    line = f.readline()
    value = line.strip('\n').split(',')
    poly.append([Point(int(x), int(y)) for x, y in zip(value[::2], value[1::2])])  


def to_matrix_index(point):
    res = Point(-point.y + HEIGHT, point.x)
    return res


class PathInfo:
    def __init__(self, path, cost):
        self.path = path  # Type: List of tuples(x, y) eg: [(0, 0), (1, 1),...]
        self.cost = cost


class Map:
    def __init__(self):
        self.mat = np.zeros((HEIGHT+1, WIDTH+1))
        self.mat[1:-1, 1:-1] = 1
        pygame.init()
        self.surface = pygame.display.set_mode(
            ((WIDTH + 1) * (BLOCK_SIZE + 1), (HEIGHT + 1) * (BLOCK_SIZE + 1)))
        self.surface.fill((0, 0, 0))
        grid = Grid(WIDTH, HEIGHT)
        grid.draw(self.surface)

        self.start, self.goal, *self.must_pass = [to_matrix_index(points[i]) for i in range(0, len(points))]
        self.points = self.start, *self.must_pass, self.goal
        self.poly = []
        for i in range(0, len(poly)):
            self.poly.append([to_matrix_index(poly[i][j]) for j in range(0, len(poly[i]))])

        pygame.draw.rect(self.surface, START_COLOR,
                         (self.start.y * (BLOCK_SIZE + 1), self.start.x * (BLOCK_SIZE + 1), BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.surface, GOAL_COLOR,
                         (self.goal.y * (BLOCK_SIZE + 1), self.goal.x * (BLOCK_SIZE + 1), BLOCK_SIZE, BLOCK_SIZE))
        if len(self.points) > 2:
            for i in range(0, len(self.must_pass)):
                pygame.draw.rect(self.surface, MUST_PASS_COLOR,
                                 (self.must_pass[i].y * (BLOCK_SIZE + 1), self.must_pass[i].x * (BLOCK_SIZE + 1), BLOCK_SIZE,
                                  BLOCK_SIZE))

        for i in range(0, len(poly)):
            self.draw_polygon(self.poly[i])

    def draw_line(self, p0, p1):
            point_set = list(bresenham(p0.x, p0.y, p1.x, p1.y))  # set = [(x,y),...]
            for i in point_set:
                self.mat[i[0]][i[1]] = 0  # i = (x,y), i[0] = x, i[1] = y"""
                pygame.draw.rect(self.surface, OBSTACLE_COLOR,
                                 (i[1] * (BLOCK_SIZE + 1), i[0] * (BLOCK_SIZE + 1), BLOCK_SIZE, BLOCK_SIZE))
                pygame.display.update()

    def draw_polygon(self, point_set):
        for i in range(-1, len(point_set) - 1):
            self.draw_line(point_set[i], point_set[i + 1])
        pygame.display.update()

    def draw_path(self, point_set):
        if point_set != -1:
            for i in range(1, len(point_set) - 1):  # Visualize the path: color points except for the first and last point
                pygame.draw.rect(self.surface, PATH_COLOR,
                                 (point_set[i][1] * (BLOCK_SIZE + 1), point_set[i][0] * (BLOCK_SIZE + 1), BLOCK_SIZE,
                                  BLOCK_SIZE))
                time.sleep(0.04)
                pygame.display.update()


    def run(self, f):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if len(self.points) == 2:  # there're no must-pass points
                            path_info = f(self.mat, self.start, self.goal, self.surface)
                            self.draw_path(path_info[0])
                            print('Total cost = ', path_info[1])
                        elif len(self.points) > 2:  # there're must-pass points
                            n = len(self.points)  # the numbers of important points = start + goal + must-pass points
                            # First, freeze all important points as obstacles
                            for i in range(0, n):
                                self.mat[self.points[i].x, self.points[i].y] = 0
                            # Init a matrix containing PathInfo(path, cost) between 2 points in "points"
                            path_info_mat = np.full((n, n), PathInfo(path=[None], cost=0))
                            # path_info_mat[0,0] = PathInfo between "start" and "start"
                            # path_info_mat[n-1,n-1] = PathInfo between "goal" and "goal"

                            # Get all the path info between important points then put them in the matrix
                            for i in range(0, n):
                                for j in range(i+1, n):
                                    # Release 2 points no more obstacles
                                    self.mat[self.points[i].x, self.points[i].y] = 1
                                    self.mat[self.points[j].x, self.points[j].y] = 1
                                    path_info = f(self.mat, self.points[i], self.points[j], self.surface)
                                    path_info_mat[i, j] = PathInfo(path_info[0], path_info[1])
                                    path_info_mat[j, i] = copy.deepcopy(path_info_mat[i, j])
                                    path_info_mat[j, i].path.reverse()
                                    # Re-freeze 2 points no more obstacles
                                    self.mat[self.points[i].x, self.points[i].y] = 0
                                    self.mat[self.points[j].x, self.points[j].y] = 0

                            total_shortest_cost = sys.maxsize
                            total_shortest_cost_per = ()
                            # for each permutation must_pass[0] = 1 (index in matrix), must_pass[1] = 2 (index in matrix),...a[k] = n-2 (index in matrix) of the must-pass points
                            for i in itt.permutations(list(range(1, n-1)), len(self.must_pass)):
                                total_path = 0

                                # path['start'][must_pass[0]] + path[must_pass[1]][must_pass[2]] + ... + path[must_pass[k]]['goal']
                                total_path += path_info_mat[0, i[0]].cost  # path['start']
                                for j in range(len(self.must_pass)-1):
                                    total_path += path_info_mat[i[j], i[j+1]].cost
                                total_path += path_info_mat[i[len(self.must_pass)-1], n-1].cost  # path[must_pass[k]]['goal']

                                if total_path < total_shortest_cost:
                                    total_shortest_cost = total_path
                                    total_shortest_cost_per = i

                            self.draw_path(path_info_mat[0, total_shortest_cost_per[0]].path)
                            for j in range(len(self.must_pass)-1):
                                self.draw_path(path_info_mat[total_shortest_cost_per[j], total_shortest_cost_per[j+1]].path)
                            self.draw_path(path_info_mat[total_shortest_cost_per[len(self.must_pass)-1], n-1].path)
                            print('Total cost = ', total_shortest_cost)

            pygame.display.update()


def main():
    demo = Map()
    demo.run(ASTAR)
    # demo.run(GREEDY)
    # demo.run(BFS)


if __name__ == '__main__':
    main()

