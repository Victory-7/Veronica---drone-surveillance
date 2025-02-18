import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drone Swarm Simulation")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Drone settings
NUM_DRONES = 10
DRONE_SPEED = 2
MASTER_DRONE_INDEX = 0  # The first drone acts as the master

drones = []  # List to store drone positions
velocities = []  # List to store drone velocities

# Initialize drones at random positions
for _ in range(NUM_DRONES):
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    angle = random.uniform(0, 2 * math.pi)
    dx = DRONE_SPEED * math.cos(angle)
    dy = DRONE_SPEED * math.sin(angle)
    drones.append([x, y])
    velocities.append([dx, dy])

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

    # Draw drones
    for i in range(NUM_DRONES):
        color = RED if i == MASTER_DRONE_INDEX else BLUE
        pygame.draw.circle(screen, color, (int(drones[i][0]), int(drones[i][1])), 5)
    
    pygame.display.flip()
    clock.tick(30)  # Limit FPS

pygame.quit()
