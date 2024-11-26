import pygame
import numpy as np

pygame.init()

# config in screen
width, height = 800, 600 # here is config resolution ( 800x600 ) 
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Box3D")

# color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Defines the 3D cube (coordinates of each vertex)
cube_vertices = np.array([
    [-1, -1, -1],
    [ 1, -1, -1],
    [ 1,  1, -1],
    [-1,  1, -1],
    [-1, -1,  1],
    [ 1, -1,  1],
    [ 1,  1,  1],
    [-1,  1,  1]
])

# Defines the edges of the cube (pairs of vertices that form each edge)
cube_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Function to project 3D points to 2D
def project(point3D):
    """ Project a 3D point to 2D using a simple projection """
    distance = 5  # distance from the "observer" to the center of the screen
    factor = width / (point3D[2] + distance)
    x = int(point3D[0] * factor) + width // 2
    y = int(point3D[1] * factor) + height // 2
    return x, y

# Cube rotation function
def rotate(vertices, angle_x, angle_y):
    rotation_x = np.array([
        [1, 0, 0],
        [0, np.cos(angle_x), -np.sin(angle_x)],
        [0, np.sin(angle_x), np.cos(angle_x)]
    ])
    rotation_y = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y)],
        [0, 1, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y)]
    ])
    rotated_vertices = vertices @ rotation_x @ rotation_y
    return rotated_vertices

# Control variables
running = True
clock = pygame.time.Clock()
angle_x = angle_y = 0  # rotation angles
vsync_enabled = True   # V-Sync enabled
fullscreen = False     # mode Fullscreen

# loop
while running:
    if vsync_enabled:
        dt = clock.tick(60)  
    else:
        dt = clock.tick()     

    fps = clock.get_fps()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e: 
                vsync_enabled = not vsync_enabled
            elif event.key == pygame.K_f:  
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((width, height))

    angle_x += 0.02
    angle_y += 0.03

    screen.fill(BLACK)

    rotated_vertices = rotate(cube_vertices, angle_x, angle_y)
    projected_points = [project(vertex) for vertex in rotated_vertices]

    for edge in cube_edges:
        start, end = edge
        pygame.draw.line(screen, WHITE, projected_points[start], projected_points[end], 2)

    font = pygame.font.SysFont("Arial", 24)
    fps_text = font.render(f"FPS: {int(fps)} | V-Sync: {'ON' if vsync_enabled else 'OFF'}", True, WHITE)
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()

# Encerra o pygame
pygame.quit()
