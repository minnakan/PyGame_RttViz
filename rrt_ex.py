import pygame
import random
import math

# Initialize Pygame
pygame.init()


WIDTH, HEIGHT = 800, 600
START = (50, 50)
GOAL = (750, 550)
GOAL_RADIUS = 10
NODE_RADIUS = 3
STEP_SIZE = 20
GOAL_BIAS = 0.1 
ANGLE_LIMIT = 70

#Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BRIGHT_GREEN = (0, 255, 127)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)

# Obstacles
obstacles = [
    #pygame.Rect(200, 150, 100, 300),
    #pygame.Rect(400, 300, 200, 50),
    #pygame.Rect(600, 100, 50, 400)
]

# Initialize display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RRT with Goal Bias")

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None

def distance(node1, node2):
    return math.hypot(node2.x - node1.x, node2.y - node1.y)

def get_random_node(nearest_node):
    if random.random() < GOAL_BIAS:
        return Node(*GOAL)
    else:
        angle_to_goal = math.atan2(GOAL[1] - nearest_node.y, GOAL[0] - nearest_node.x)
        angle_offset = random.uniform(-ANGLE_LIMIT / 2, ANGLE_LIMIT / 2) * (math.pi / 180)
        random_angle = angle_to_goal + angle_offset

        random_distance = random.uniform(0, min(WIDTH, HEIGHT) / 2)

        new_x = nearest_node.x + random_distance * math.cos(random_angle)
        new_y = nearest_node.y + random_distance * math.sin(random_angle)

        return Node(int(new_x), int(new_y))

def get_random_existing_node(nodes):
    if(len(nodes) > 100):
        return random.choice(nodes[-100:])
    return random.choice(nodes)

def get_nearest_node(nodes, random_node):
    return min(nodes, key=lambda node: distance(node, random_node))

def steer(from_node, to_node, step_size):
    theta = math.atan2(to_node.y - from_node.y, to_node.x - from_node.x)
    new_x = from_node.x + step_size * math.cos(theta)
    new_y = from_node.y + step_size * math.sin(theta)
    return Node(int(new_x), int(new_y))

def is_goal_reached(node):
    return distance(node, Node(*GOAL)) <= GOAL_RADIUS

def is_collision(node):
    point = pygame.Rect(node.x, node.y, NODE_RADIUS, NODE_RADIUS)
    for obstacle in obstacles:
        if obstacle.colliderect(point):
            return True
    return False

def draw_node(node, color=BLACK):
    pygame.draw.circle(screen, color, (node.x, node.y), NODE_RADIUS)

def draw_edge(node1, node2, color=BLUE):
    pygame.draw.line(screen, color, (node1.x, node1.y), (node2.x, node2.y))

def draw_obstacles():
    for obstacle in obstacles:
        pygame.draw.rect(screen, GRAY, obstacle)

def main():
    nodes = [Node(*START)]
    goal_node = Node(*GOAL)
    clock = pygame.time.Clock()
    path_found = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not path_found:
            for _ in range(100):
                random_existing_node = get_random_existing_node(nodes)
                random_node = get_random_node(random_existing_node)
                new_node = steer(random_existing_node, random_node, STEP_SIZE)
                new_node.parent = random_existing_node

                if not is_collision(new_node):
                    nodes.append(new_node)
                    

                    if is_goal_reached(new_node):
                        path_found = True
                        break

        screen.fill(WHITE)
        draw_obstacles()
        draw_node(goal_node, BRIGHT_GREEN) 

        for node in nodes:
            draw_node(node)
            if node.parent:
                draw_edge(node, node.parent)

        if path_found:
            path_node = nodes[-1]
            while path_node:
                draw_node(path_node, RED)
                if path_node.parent:
                    draw_edge(path_node, path_node.parent, RED)
                path_node = path_node.parent

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
