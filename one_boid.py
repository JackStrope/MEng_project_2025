import pygame
import os
import random
import math
import sys
import RPi.GPIO as GPIO

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen size
# size = width, height = 1024, 768
size = width, height = 1280, 720

# Boid parameters
NUM_BOIDS = 1
BOID_SIZE = 10
SPEED_LIMIT = 10
VISUAL_RANGE = 40
AVOID_RANGE = 20
CENTERING_FACTOR = 0.0005
AVOID_FACTOR = 0.01
MATCHING_FACTOR = 0.01
TURN_FACTOR = 0.075

# Env variables to display/control on piTFT (fb0) or monitor (fb1)
os.putenv('SDL_VIDEODRV','fbcon')
os.putenv('SDL_FBDEV', '/dev/fb-hdmi')

# Set up GPIO button 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Exit the program
def GPIO27_callback(channel):
    global running
    running = False

# Callbacks
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback)

# Set up PyGame
pygame.init()
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(False) # hide mouse
clock = pygame.time.Clock()

# Define Boid class
class Boid:
    def __init__(self):
        self.x = random.uniform(0, width)
        self.y = random.uniform(0, height)
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
    
    def move(self):
        self.x += self.vx
        self.y += self.vy

        # Wrap around screen edges
        if self.x > width:
            self.x = 0
        elif self.x < 0:
            self.x = width
        if self.y > height:
            self.y = 0
        elif self.y < 0:
            self.y = height

    def limit_speed(self):
        speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
        if speed > SPEED_LIMIT:
            self.vx = (self.vx / speed) * SPEED_LIMIT
            self.vy = (self.vy / speed) * SPEED_LIMIT

# Create boids
boids = [Boid() for _ in range(NUM_BOIDS)]

def update_boids():
    for boid in boids:
        # Alignment, cohesion, separation
        vx_avg, vy_avg = 0, 0
        cx, cy = 0, 0
        close_dx, close_dy = 0, 0
        count = 0

        for other in boids:
            if other == boid:
                continue
            dx = other.x - boid.x
            dy = other.y - boid.y
            dist = math.sqrt(dx ** 2 + dy ** 2)

            if dist < VISUAL_RANGE:
                # Alignment
                vx_avg += other.vx
                vy_avg += other.vy

                # Cohesion
                cx += other.x
                cy += other.y
                count += 1

            if dist < AVOID_RANGE:
                # Separation
                close_dx -= dx
                close_dy -= dy

        # Apply rules
        if count > 0:
            # Cohesion
            cx /= count
            cy /= count
            boid.vx += (cx - boid.x) * CENTERING_FACTOR
            boid.vy += (cy - boid.y) * CENTERING_FACTOR

            # Alignment
            vx_avg /= count
            vy_avg /= count
            boid.vx += (vx_avg - boid.vx) * MATCHING_FACTOR
            boid.vy += (vy_avg - boid.vy) * MATCHING_FACTOR

        # Separation
        boid.vx += close_dx * AVOID_FACTOR
        boid.vy += close_dy * AVOID_FACTOR

        # If boid enters top area
        if boid.y < 150:
            boid.vy += TURN_FACTOR
        
        # If boid enters bottom area
        if boid.y > height - 150:
            boid.vy -= TURN_FACTOR
        
        # If boid enters left area
        if boid.x < 150:
            boid.vx += TURN_FACTOR
        
        # If boid enters right area
        if boid.x > width - 150:
            boid.vx -= TURN_FACTOR

        # Limit speed and move
        boid.limit_speed()
        boid.move()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill(BLACK)  # Clear screen

    # Update and draw boids
    update_boids()
    for boid in boids:
        pygame.draw.circle(screen, WHITE, (int(boid.x), int(boid.y)), BOID_SIZE)

    pygame.display.flip()  # Update display
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()
# sys.exit(0)