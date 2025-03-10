# Test how to move object around in PyGame

import pygame,pigame
from pygame.locals import *
import os
import math
import sys
import RPi.GPIO as GPIO

# Colors
BLACK = 0,0,0
WHITE = 255, 255, 255

# Set up GPIO button 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Exit the program
def GPIO27_callback(channel):
    global running
    running = False

# Callbacks
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback)

# Env variables to display/control on monitor/projector (fb0) or piTFT (fb1)
os.putenv('SDL_VIDEODRV','fbcon')
os.putenv('SDL_FBDEV', '/dev/fb-hdmi')
os.putenv('SDL_MOUSEDRV','dummy')
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY','')

# Screen size
# size = width, height = 1024, 768
size = width, height = 1280, 720

# Set up PyGame
pygame.init()
screen = pygame.display.set_mode(size)
screen.fill(BLACK)
pygame.mouse.set_visible(False)
pygame.display.update()
angle = 0  # starting angle in radians
center_x, center_y = width / 2, height / 2

# Parameters
r = 200             # radius of circle to swim in
speed = 0.05        # angular speed in radians per frame
circle_radius = 20  # radius of the white circle

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    angle += speed

    # Calculate new position of the circle
    circle_x = center_x + r * math.cos(angle)
    circle_y = center_y + r * math.sin(angle)

    # Clear screen and draw the fish
    screen.fill(BLACK)
    pygame.draw.circle(screen, WHITE, (int(circle_x), int(circle_y)), circle_radius)
    pygame.display.flip()
    pygame.time.delay(16)

pygame.quit()
# sys.exit()