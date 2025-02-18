import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drone Swarm Simulation with Radar")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Drone settings
NUM_DRONES = 10
DRONE_SPEED = 2
MASTER_DRONE_INDEX = 0  # The first drone acts as the master
RADAR_RANGE = 150  # Detection range of radar
RADAR_SWEEP_SPEED = 2  # Speed of radar sweep

# Initialize drones at random positions
drones = []
velocities = []
for _ in range(NUM_DRONES):
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    angle = random.uniform(0, 2 * math.pi)
    dx = DRONE_SPEED * math.cos(angle)
    dy = DRONE_SPEED * math.sin(angle)
    drones.append([x, y])
    velocities.append([dx, dy])

# Radar settings
radar_x, radar_y = WIDTH // 2, HEIGHT // 2  # Radar at center
radar_angle = 0

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update drone positions
    for i in range(NUM_DRONES):
        drones[i][0] += velocities[i][0]
        drones[i][1] += velocities[i][1]

        # Keep drones within bounds
        if drones[i][0] <= 0 or drones[i][0] >= WIDTH:
            velocities[i][0] *= -1
        if drones[i][1] <= 0 or drones[i][1] >= HEIGHT:
            velocities[i][1] *= -1

    # Draw radar circle
    pygame.draw.circle(screen, BLACK, (radar_x, radar_y), RADAR_RANGE, 1)
    
    # Radar sweep effect
    radar_angle += RADAR_SWEEP_SPEED
    radar_x_end = radar_x + RADAR_RANGE * math.cos(math.radians(radar_angle))
    radar_y_end = radar_y + RADAR_RANGE * math.sin(math.radians(radar_angle))
    pygame.draw.line(screen, GREEN, (radar_x, radar_y), (radar_x_end, radar_y_end), 2)

    # Draw drones and detect within radar range
    for i in range(NUM_DRONES):
        drone_x, drone_y = drones[i]
        color = RED if i == MASTER_DRONE_INDEX else BLUE
        pygame.draw.circle(screen, color, (int(drone_x), int(drone_y)), 5)

        # Check if drone is within radar range
        distance = math.sqrt((drone_x - radar_x) ** 2 + (drone_y - radar_y) ** 2)
        if distance <= RADAR_RANGE:
            pygame.draw.circle(screen, GREEN, (int(drone_x), int(drone_y)), 5, 1)  # Highlight detected drones
    
    pygame.display.flip()
    clock.tick(30)  # Limit FPS

pygame.quit()
