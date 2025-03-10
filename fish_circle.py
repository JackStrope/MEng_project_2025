# Displays fish image swimming in a circle

import pygame
import os
import math
import sys
import RPi.GPIO as GPIO

BLACK = (0, 0, 0)
# size = width, height = 1024, 768
size = width, height = 1280, 720

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
screen.fill(BLACK)
pygame.mouse.set_visible(False)
pygame.display.update()
center_x, center_y = width / 2, height / 2
angle = 0  # starting angle in radians

# Parameters
r = 200  # radius of circle to swim in
speed = 0.05  # angular speed in radians per frame

fish = pygame.image.load("fish.png")
fish = pygame.transform.scale(fish, (1102//10, 297//10))
fish = pygame.transform.rotate(fish, 90)  # Starting orientation
fishrect = fish.get_rect(center=(center_x, center_y-r))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    angle += speed

    # Calculate new position and orientation of the fish
    fishrect.center = (center_x + r*math.cos(angle), center_y + r*math.sin(angle))
    rotation_angle = -math.degrees(angle)
    new_fish = pygame.transform.rotate(fish, rotation_angle)
    new_fishrect = new_fish.get_rect(center=fishrect.center)

    # Clear screen and draw the fish
    screen.fill(BLACK)
    screen.blit(new_fish, new_fishrect)
    pygame.display.flip()
    pygame.time.delay(16)

pygame.quit()
# sys.exit()