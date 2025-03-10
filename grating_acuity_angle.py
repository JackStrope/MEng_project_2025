# Display a grating acuity test--black and white bars moving back and forth

import pygame
import os
import sys
import math
import RPi.GPIO as GPIO
import json

# Exit codes
EXIT_OK = 0  # exit normally
EXIT_EDIT = 10  # signal to the main UI to launch the parameter editor

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen size
# size = width, height = 1024, 768
size = width, height = 1280, 720
tft_size = tft_width, tft_height = 320, 240

# Default exit code
exit_code = EXIT_OK

# Set up GPIO buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Exit the program
def quit_callback(channel):
    global running, exit_code
    exit_code = EXIT_OK
    running = False

# Edit parameters
def edit_callback(channel):
    global running, exit_code
    exit_code = EXIT_EDIT
    running = False

# Callbacks
GPIO.add_event_detect(27, GPIO.FALLING, callback=quit_callback)
GPIO.add_event_detect(17, GPIO.FALLING, callback=edit_callback)

# Env variables to display/control on monitor (fb0) or piTFT (fb1)
os.putenv('SDL_VIDEODRV','fbcon')
os.putenv('SDL_FBDEV', '/dev/fb-hdmi')

# Set up PyGame
pygame.init()
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(False)

# Load parameters
with open("params_grating_acuity.json", "r") as f:
    params = json.load(f)

bar_width = params["bar_width"]
speed = params["speed"]
bars_to_move = params["bars_to_move"]  # Number of bar widths the bars move back and forth
bar_angle_deg = params["bar_angle_deg"]  # Angle of bar orientation in degrees relative to horizontal

move_angle_deg = bar_angle_deg + 90  # Move perpendicular to bar orientation
dist_offset = 0
moving_forward = True

# The maximum distance bars move from the starting position
max_dist = bars_to_move*bar_width

# Convert angle to radians
move_angle_rad = math.radians(move_angle_deg)

# Create a pattern surface
surf_width = width + max_dist
surf_height = height + max_dist
diag = int(math.sqrt(surf_width**2 + surf_height**2))
pattern_size = diag*4  # scale up to ensure room for rotation and movement
pattern_surf = pygame.Surface((pattern_size, pattern_size))
pattern_surf.fill(BLACK)

# Draw vertical bars on the surface
for x in range(0, pattern_size, bar_width*2):
    pygame.draw.rect(pattern_surf, WHITE, (x, 0, bar_width, pattern_size))

# Rotate the pattern by angle
rotated_surf = pygame.transform.rotate(pattern_surf, 90 - bar_angle_deg)

running = True
clock = pygame.time.Clock()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Move bars right or left
    if moving_forward:
        dist_offset += speed
        if dist_offset >= bars_to_move*bar_width:
            moving_forward = False
    else:
        dist_offset -= speed
        if dist_offset <= 0:
            moving_forward = True

    # Convert angled offset to x and y offsets
    x_offset = dist_offset*math.cos(move_angle_rad)
    y_offset = dist_offset*math.sin(move_angle_rad)

    # Clear screen
    screen.fill(BLACK)

    rot_rect = rotated_surf.get_rect()
    center_x = width / 2
    center_y = height / 2

    blit_x = int(center_x - rot_rect.width/2 - x_offset)
    blit_y = int(center_y - rot_rect.height/2 - y_offset)

    screen.blit(rotated_surf, (blit_x, blit_y))
    screen.blit(rotated_surf, (blit_x, blit_y))

    pygame.display.flip()
    clock.tick(60)

GPIO.cleanup()
pygame.quit()
print("grating acuity exited safely with code", exit_code)
sys.exit(exit_code)