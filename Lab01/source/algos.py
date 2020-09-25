import pygame
import queue as qe
import time
from colors3 import BLOCK_SIZE
from colors3 import OPENING_COLOR
from colors3 import VISITED_COLOR
from colors3 import PATH_COLOR


# directions for opening frontier
rowNum = (-1, 0, 0, 1)
colNum = (0, -1, 1, 0)


def is_valid(row, col, mat):
    return (row >= 0) and (row < len(mat)) and (col >= 0) and (col < len(mat[0]))


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Node:
    def __init__(self, pt, dis):
        self.pt = pt  # type : Point
        self.dis = dis


class GreedyNode:
    def __init__(self, pt, g=None, h=None):
        self.pt = pt  # type : Point
        self.g = g
        self.h = h

    def __lt__(self, other):
        return self.h < other.h


def heuristic(a, b):
    # Manhattan distance on a square grid
    return abs(a.x - b.x) + abs(a.y - b.y)


def BFS(mat, src, dest, surface):
    if mat[src.x][src.y] == 0 or mat[dest.x][dest.y] == 0:  # OBSTACLES?
        return -1,-1
    s = Node(src, 0)
    # in bfs, frontier is a queue
    frontier = qe.Queue()
    frontier.put(s)
    came_from = {}
    came_from[(src.x, src.y)] = None
    while not (frontier.empty()):
        time.sleep(0.0005)
        curr = frontier.get()
        pt = curr.pt
        if (pt.x != src.x or pt.y != src.y) and (pt.x != dest.x or pt.y != dest.y):
            pygame.draw.rect(surface, VISITED_COLOR,
                             (pt.y * (BLOCK_SIZE + 1), pt.x * (BLOCK_SIZE + 1), BLOCK_SIZE, BLOCK_SIZE))
            pygame.display.update()
        if pt.x == dest.x and pt.y == dest.y:
            path = []
            cur = (dest.x, dest.y)
            while (1):
                path.append(cur)
                if came_from[cur] != None:
                    cur = came_from[cur]
                else:
                    break
            path.reverse()

            return path, curr.dis
        # adjacent cell
        for i in range(0, 4):
            row = pt.x + rowNum[i]
            col = pt.y + colNum[i]
            temp_point = Point(row, col)
            if is_valid(row, col, mat) and mat[row][col] != 0 and (temp_point.x, temp_point.y) not in came_from:
                # visited[row][col] = True
                # mat[row][col] = 0
                if (row != src.x or col != src.y) and (row != dest.x or col != dest.y):
                    pygame.draw.rect(surface, OPENING_COLOR,
                                     (col * (BLOCK_SIZE + 1), row * (BLOCK_SIZE + 1), BLOCK_SIZE, BLOCK_SIZE))
                    pygame.display.update()
                Adjcell = Node(temp_point, curr.dis+1)
                frontier.put(Adjcell)
                came_from[(temp_point.x, temp_point.y)] = (pt.x, pt.y)

    return -1,-1


def GREEDY(mat, src, dest, surface):
    if mat[src.x][src.y] == 0 or mat[dest.x][dest.y] == 0:
        return -1,-1
    s = GreedyNode(pt=src, h=0, g=0)
    # in GREEDY search , frontier is a priority queue
    frontier = qe.PriorityQueue()
    frontier.put((s.h, s))

    came_from = {}
    came_from[(src.x, src.y)] = None
    while not (frontier.empty()):
        time.sleep(0.005)
        curr = frontier.get()
        pt = curr[1].pt
        print(f'visiting ({pt.x},{pt.y}) h={curr[1].h}')
        if (pt.x != src.x or pt.y != src.y) and (pt.x != dest.x or pt.y != dest.y):
            pygame.draw.rect(surface, VISITED_COLOR,
                             (pt.y * (BLOCK_SIZE + 1), pt.x * (BLOCK_SIZE + 1), BLOCK_SIZE, BLOCK_SIZE))
            pygame.display.update()
        if pt.x == dest.x and pt.y == dest.y:
            path = []
            cur = (dest.x, dest.y)
            while (1):
                path.append(cur)
                if came_from[cur] != None:
                    cur = came_from[cur]
                else:
                    break
            path.reverse()

            return path, curr[1].g
        # adjacent cell
        for i in range(0, 4):
            row = pt.x + rowNum[i]
            col = pt.y + colNum[i]
            temp_point = Point(row, col)
            if is_valid(row, col, mat) and mat[row][col] != 0 and (temp_point.x, temp_point.y) not in came_from:
                # mat[row][col] = 0
                if (row != src.x or col != src.y) and (row != dest.x or col != dest.y):
                    pygame.draw.rect(surface, OPENING_COLOR,
                                     (col * (BLOCK_SIZE + 1), row * (BLOCK_SIZE + 1), BLOCK_SIZE, BLOCK_SIZE))
                    pygame.display.update()
                Adjcell = GreedyNode(temp_point, g=1)
                priority = heuristic(dest, temp_point)
                Adjcell.h = priority
                Adjcell.g = curr[1].g + 1
                print(f'neighbour with h= {priority}')
                frontier.put((priority, Adjcell))
                came_from[(temp_point.x, temp_point.y)] = (pt.x, pt.y)

    return -1,-1

class AstarNode():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def ASTAR(mat, start, goal, surface):
    if mat[start.x][start.y] == 0 or mat[goal.x][goal.y] == 0:
        return -1, -1

    # Create start and end node
    start_node = AstarNode(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = AstarNode(None, goal)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        # pygame.draw.rect(surface, VISITED_COLOR,
        #                  (current_node.position.y * (BLOCK_SIZE + 1), current_node.position.x * (BLOCK_SIZE + 1), BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.update()
        # Find node with min(f)
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        # Found the goal
        if current_node.position.x == end_node.position.x and current_node.position.y == end_node.position.y :
            path = []
            current = current_node
            while current is not None:
                path.append((current.position.x,current.position.y))
                current = current.parent
            return path[::-1], len(path)  # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:

            # Get node position
            node_position = Point(current_node.position.x + new_position[0], current_node.position.y + new_position[1])
            # Make sure within range
            if node_position.x > (len(mat) - 1) or node_position.y < 0 or node_position.x > (
                    len(mat[len(mat) - 1]) - 1) or node_position.y < 0:
                continue
            # Make sure walkable terrain
            if mat[node_position.x][node_position.y] == 0:
                continue

            # Create new node
            new_node = AstarNode(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

                # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position.x - end_node.position.x) ** 2) + ((child.position.y - end_node.position.y) ** 2)
            child.f = child.g + child.h
            if (child.position.x != start_node.position.x or child.position.y != start_node.position.y) and (child.position.x != end_node.position.x or child.position.y != end_node.position.y):
                pygame.draw.rect(surface, OPENING_COLOR,
                                 (child.position.y * (BLOCK_SIZE + 1), child.position.x * (BLOCK_SIZE + 1), BLOCK_SIZE,
                                  BLOCK_SIZE))
                pygame.display.update()

            pygame.display.update()
            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

                # Add the child to the open list
            open_list.append(child)

    return -1,-1