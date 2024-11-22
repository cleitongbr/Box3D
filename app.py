import pygame
import numpy as np

# Inicialize o pygame
pygame.init()

# Configurações da tela
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D Box com FPS e V-Sync")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define o cubo 3D (coordenadas de cada vértice)
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

# Define as arestas do cubo (pares de vértices que formam cada aresta)
cube_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Função para projetar os pontos 3D para 2D
def project(point3D):
    """ Projeta um ponto 3D para 2D usando uma projeção simples """
    distance = 5  # distância do "observador" ao centro da tela
    factor = width / (point3D[2] + distance)
    x = int(point3D[0] * factor) + width // 2
    y = int(point3D[1] * factor) + height // 2
    return x, y

# Função de rotação do cubo
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

# Variáveis de controle
running = True
clock = pygame.time.Clock()
angle_x = angle_y = 0  # ângulos de rotação
vsync_enabled = True   # V-Sync ativado
fullscreen = False     # Modo tela cheia

# Loop principal
while running:
    # Controle de FPS
    if vsync_enabled:
        dt = clock.tick(60)  # Limita a 60 FPS se o V-Sync estiver ativado
    else:
        dt = clock.tick()     # Sem limite de FPS

    fps = clock.get_fps()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:  # Alterna V-Sync
                vsync_enabled = not vsync_enabled
            elif event.key == pygame.K_f:  # Alterna tela cheia
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((width, height))

    # Atualiza os ângulos de rotação
    angle_x += 0.02
    angle_y += 0.03

    # Limpa a tela
    screen.fill(BLACK)

    # Rotaciona e projeta os vértices do cubo
    rotated_vertices = rotate(cube_vertices, angle_x, angle_y)
    projected_points = [project(vertex) for vertex in rotated_vertices]

    # Desenha as arestas do cubo
    for edge in cube_edges:
        start, end = edge
        pygame.draw.line(screen, WHITE, projected_points[start], projected_points[end], 2)

    # Exibe o FPS e estado do V-Sync na tela
    font = pygame.font.SysFont("Arial", 24)
    fps_text = font.render(f"FPS: {int(fps)} | V-Sync: {'ON' if vsync_enabled else 'OFF'}", True, WHITE)
    screen.blit(fps_text, (10, 10))

    # Atualiza a tela
    pygame.display.flip()

# Encerra o pygame
pygame.quit()
