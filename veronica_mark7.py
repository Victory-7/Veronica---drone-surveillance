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
WHITE = (255, 255, 255)

# Drone settings
NUM_DRONES = 10
DRONE_MAX_SPEED = 3
DRONE_ACCELERATION = 0.1
MASTER_DRONE_INDEX = 0
RADAR_RANGE = 150
RADAR_SWEEP_SPEED = 3
OBSTACLES = [(400, 300, 50)]  # List of obstacles (x, y, radius)

# Communication settings
PACKET_LOSS_PROBABILITY = 0.1
LATENCY_RANGE = (10, 100)
message_queue = deque()
acks = {i: False for i in range(1, NUM_DRONES)}

# Initialize drones
class Drone:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.speed = random.uniform(1, DRONE_MAX_SPEED)
        self.angle = random.uniform(0, 2 * math.pi)
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)
        self.name = f"Mark_{index+1}"
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

# Initialize drones
drones = [Drone(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), i) for i in range(NUM_DRONES)]

# Radar settings
radar_x, radar_y = WIDTH // 2, HEIGHT // 2
radar_angle = 0
blips = deque(maxlen=20)  # Store detected positions for fading effect

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
    
    # Master drone sends commands
    master_drone = drones[MASTER_DRONE_INDEX]
    for i, drone in enumerate(drones):
        if i != MASTER_DRONE_INDEX:
            if random.random() > PACKET_LOSS_PROBABILITY:
                drone.dx, drone.dy = master_drone.dx, master_drone.dy
                drone.communicating = True
            else:
                drone.communicating = False
    
    # Move drones
    for drone in drones:
        drone.move()

    # Draw obstacles with sleek outlines
    for ox, oy, radius in OBSTACLES:
        pygame.draw.circle(screen, NEON_RED, (ox, oy), radius, 3)

    # Draw radar circle
    pygame.draw.circle(screen, NEON_BLUE, (radar_x, radar_y), RADAR_RANGE, 2)
    
    # Radar sweep effect with glow
    radar_angle = (radar_angle + RADAR_SWEEP_SPEED) % 360
    radar_x_end = radar_x + RADAR_RANGE * math.cos(math.radians(radar_angle))
    radar_y_end = radar_y + RADAR_RANGE * math.sin(math.radians(radar_angle))
    pygame.draw.line(screen, NEON_GREEN, (radar_x, radar_y), (radar_x_end, radar_y_end), 3)
    
    # Drones and radar detection
    for i, drone in enumerate(drones):
        color = NEON_BLUE if not drone.communicating else NEON_GREEN
        pygame.draw.circle(screen, color, (int(drone.x), int(drone.y)), 6)
    
    # Draw communication table
    font = pygame.font.Font(None, 24)
    table_x, table_y = 10, 10
    screen.blit(font.render("Drone Name        Status", True, WHITE), (table_x, table_y))
    table_y += 20
    for drone in drones:
        status = "Communicating" if drone.communicating else "Not Communicating"
        screen.blit(font.render(f"{drone.name}        {status}", True, WHITE), (table_x, table_y))
        table_y += 20
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()