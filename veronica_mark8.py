import pygame
import random
import math
from collections import deque

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Futuristic Drone Swarm Simulation")

# Colors
BLACK = (0, 0, 0)
NEON_BLUE = (0, 255, 255)
NEON_RED = (255, 0, 102)
NEON_GREEN = (0, 255, 0)
NEON_PURPLE = (180, 0, 255)
GRID_COLOR = (30, 30, 30)

# Drone settings
NUM_DRONES = 10
DRONE_MAX_SPEED = 3
DRONE_ACCELERATION = 0.1
MASTER_DRONE_INDEX = 0
RADAR_RANGE = 150
COMMUNICATION_RANGE = 100
OBSTACLES = [(400, 300, 50)]  # List of obstacles (x, y, radius)

# Initialize drones
class Drone:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.speed = random.uniform(1, DRONE_MAX_SPEED)
        self.angle = random.uniform(0, 2 * math.pi)
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)
        self.name = f"Mark_{index + 1}"
        self.communicating = False

    def move(self):
        self.speed = min(self.speed + DRONE_ACCELERATION, DRONE_MAX_SPEED)
        self.x += self.dx
        self.y += self.dy
        
        # Bounce off walls
        if self.x <= 0 or self.x >= WIDTH:
            self.dx *= -1
        if self.y <= 0 or self.y >= HEIGHT:
            self.dy *= -1

        # Random movement adjustment
        if random.random() < 0.02:
            self.angle = random.uniform(0, 2 * math.pi)
            self.dx = self.speed * math.cos(self.angle)
            self.dy = self.speed * math.sin(self.angle)

# Initialize drones
drones = [Drone(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), i) for i in range(NUM_DRONES)]

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(BLACK)
    
    # Draw sleek grid background
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Move drones
    master_drone = drones[MASTER_DRONE_INDEX]
    for drone in drones:
        drone.move()
        
        # Check communication status
        distance = math.hypot(drone.x - master_drone.x, drone.y - master_drone.y)
        drone.communicating = distance <= COMMUNICATION_RANGE
    
    # Draw drones and update table
    drone_table = []
    for drone in drones:
        color = NEON_GREEN if drone.communicating else NEON_BLUE
        pygame.draw.circle(screen, color, (int(drone.x), int(drone.y)), 6)
        drone_table.append(f"{drone.name}: {'Communicating' if drone.communicating else 'Not Communicating'}")
    
    # Display communication status
    font = pygame.font.Font(None, 24)
    y_offset = 10
    for entry in drone_table:
        text_surface = font.render(entry, True, NEON_BLUE)
        screen.blit(text_surface, (10, y_offset))
        y_offset += 20
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
