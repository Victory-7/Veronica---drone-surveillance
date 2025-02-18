import pygame
import random
import math
from collections import deque

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Drone Swarm Simulation")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)

# Drone settings
NUM_DRONES = 10
DRONE_MAX_SPEED = 3
DRONE_ACCELERATION = 0.1
MASTER_DRONE_INDEX = 0
RADAR_RANGE = 150
RADAR_SWEEP_SPEED = 3
OBSTACLES = [(400, 300, 50)]  # List of obstacles (x, y, radius)

# Initialize drones
class Drone:
    def __init__(self, x, y, is_decoy=False, has_stealth=False, has_emp=False):
        self.x = x
        self.y = y
        self.speed = random.uniform(1, DRONE_MAX_SPEED)
        self.angle = random.uniform(0, 2 * math.pi)
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)
        self.is_decoy = is_decoy
        self.has_stealth = has_stealth
        self.has_emp = has_emp
        self.emp_cooldown = 0

    def move(self):
        self.speed = min(self.speed + DRONE_ACCELERATION, DRONE_MAX_SPEED)
        self.x += self.dx
        self.y += self.dy
        
        # Bounce off walls
        if self.x <= 0 or self.x >= WIDTH:
            self.dx *= -1
        if self.y <= 0 or self.y >= HEIGHT:
            self.dy *= -1
        
        # Avoid obstacles
        for ox, oy, radius in OBSTACLES:
            if math.hypot(self.x - ox, self.y - oy) < radius + 5:
                self.angle += math.pi / 2
                self.dx = self.speed * math.cos(self.angle)
                self.dy = self.speed * math.sin(self.angle)
        
        # EMP cooldown
        if self.has_emp and self.emp_cooldown > 0:
            self.emp_cooldown -= 1

# Initialize drones
special_drones = [
    Drone(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), is_decoy=True),
    Drone(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), has_stealth=True),
    Drone(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), has_emp=True)
]
drones = [Drone(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(NUM_DRONES - len(special_drones))]
drones.extend(special_drones)

# Radar settings
radar_x, radar_y = WIDTH // 2, HEIGHT // 2
radar_angle = 0
blips = deque(maxlen=20)  # Store detected positions for fading effect

# Communication settings
PACKET_LOSS_PROBABILITY = 0.1
LATENCY_RANGE = (10, 100)
message_queue = deque()
acks = {i: False for i in range(1, NUM_DRONES)}

# User Controls
manual_control = False
selected_drone = MASTER_DRONE_INDEX

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                manual_control = not manual_control
            elif event.key == pygame.K_UP:
                drones[selected_drone].y -= 5
            elif event.key == pygame.K_DOWN:
                drones[selected_drone].y += 5
            elif event.key == pygame.K_LEFT:
                drones[selected_drone].x -= 5
            elif event.key == pygame.K_RIGHT:
                drones[selected_drone].x += 5
            elif event.key == pygame.K_e:  # EMP activation
                if drones[selected_drone].has_emp and drones[selected_drone].emp_cooldown == 0:
                    drones[selected_drone].emp_cooldown = 300  # 10-second cooldown

    # Move drones
    if not manual_control:
        for drone in drones:
            drone.move()

    # Draw obstacles
    for ox, oy, radius in OBSTACLES:
        pygame.draw.circle(screen, BLACK, (ox, oy), radius)

    # Draw radar circle
    pygame.draw.circle(screen, BLACK, (radar_x, radar_y), RADAR_RANGE, 1)
    
    # Radar sweep effect
    radar_angle = (radar_angle + RADAR_SWEEP_SPEED) % 360
    radar_x_end = radar_x + RADAR_RANGE * math.cos(math.radians(radar_angle))
    radar_y_end = radar_y + RADAR_RANGE * math.sin(math.radians(radar_angle))
    pygame.draw.line(screen, GREEN, (radar_x, radar_y), (radar_x_end, radar_y_end), 2)
    
    # Drones and radar detection
    master_x, master_y = drones[MASTER_DRONE_INDEX].x, drones[MASTER_DRONE_INDEX].y
    for i, drone in enumerate(drones):
        color = RED if i == MASTER_DRONE_INDEX else (PURPLE if drone.is_decoy else BLUE)
        pygame.draw.circle(screen, color, (int(drone.x), int(drone.y)), 5)
        
        # Radar detection, ignore stealth drones
        if not drone.has_stealth:
            distance = math.hypot(drone.x - radar_x, drone.y - radar_y)
            if distance <= RADAR_RANGE:
                blips.append((int(drone.x), int(drone.y)))
                pygame.draw.circle(screen, GREEN, (int(drone.x), int(drone.y)), 5, 1)
        
        # EMP effect
        if drone.has_emp and drone.emp_cooldown > 0:
            pygame.draw.circle(screen, YELLOW, (int(drone.x), int(drone.y)), 8, 2)

    # Display fading blips
    for blip in blips:
        pygame.draw.circle(screen, GREEN, blip, 3)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()