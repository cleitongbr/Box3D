import pygame
import numpy as np
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Initialize pygame
pygame.init()

# Screen settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Box3D")

icon = pygame.image.load('icon.ico') 
pygame.display.set_icon(icon)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Function to load geometry from a .3d file
def load_geometry(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    vertices = []
    edges = []
    section = None

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line == "vertices":
            section = "vertices"
            continue
        elif line == "edges":
            section = "edges"
            continue
        
        if section == "vertices":
            vertices.append(list(map(float, line.split())))
        elif section == "edges":
            edges.append(tuple(map(int, line.split())))
    
    return np.array(vertices), edges

# Function to project 3D points to 2D
def project(point3D):
    """ Projects a 3D point to 2D using a simple projection """
    distance = 5  # Distance from "viewer" to the screen center
    factor = width / (point3D[2] + distance)
    x = int(point3D[0] * factor) + width // 2
    y = int(point3D[1] * factor) + height // 2
    return x, y

# Function to rotate the object
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

# File selector if no argument is provided
def select_file():
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = askopenfilename(
        filetypes=[("3D Files", "*.3d"), ("All Files", "*.*")]
    )
    root.destroy()
    if not file_path:
        print("No file selected.")
        sys.exit(1)
    return file_path

# Check if a .3d file is provided
if len(sys.argv) != 3 or sys.argv[1] != "-load":
    print("No file provided, opening file selector...")
    file_path = select_file()
else:
    file_path = sys.argv[2]

# Load file data
try:
    vertices, edges = load_geometry(file_path)
except Exception as e:
    print(f"Error loading file {file_path}: {e}")
    sys.exit(1)

# Control variables
running = True
clock = pygame.time.Clock()
angle_x = angle_y = 0  # Rotation angles
vsync_enabled = False   
auto_rotate = False     
mouse_dragging = False
last_mouse_pos = None

# Main loop
while running:
    # FPS control with V-Sync
    if vsync_enabled:
        dt = clock.tick(60)  # Limit to 60 FPS
    else:
        dt = clock.tick()

    fps = clock.get_fps()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:  # Toggle V-Sync
                vsync_enabled = not vsync_enabled
            elif event.key == pygame.K_g:  # Toggle auto-rotation
                auto_rotate = not auto_rotate
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_dragging = True
                last_mouse_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                mouse_dragging = False
        elif event.type == pygame.MOUSEMOTION and mouse_dragging:
            current_mouse_pos = pygame.mouse.get_pos()
            dx = current_mouse_pos[0] - last_mouse_pos[0]
            dy = current_mouse_pos[1] - last_mouse_pos[1]
            angle_x += dy * 0.01  # Adjust rotation speed
            angle_y += dx * 0.01
            last_mouse_pos = current_mouse_pos

    # Update rotation angles if auto-rotation is enabled
    if auto_rotate and not mouse_dragging:
        angle_x += 0.02
        angle_y += 0.03

    # Clear the screen
    screen.fill(BLACK)

    # Rotate and project the object's vertices
    rotated_vertices = rotate(vertices, angle_x, angle_y)
    projected_points = [project(vertex) for vertex in rotated_vertices]

    # Draw the edges of the object
    for edge in edges:
        start, end = edge
        pygame.draw.line(screen, WHITE, projected_points[start], projected_points[end], 2)

    # Display FPS, V-Sync, and auto-rotation status on screen
    font = pygame.font.SysFont("Arial", 12)
    status_text = font.render(
        f"FPS: {int(fps)} | V-Sync: {'ON' if vsync_enabled else 'OFF'} | Auto-Rotate: {'ON' if auto_rotate else 'OFF'}", 
        True, WHITE
    )
    screen.blit(status_text, (10, 10))

    # Update the screen
    pygame.display.flip()

# Quit pygame
pygame.quit()
