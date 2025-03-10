import pygame
import os
import sys
import RPi.GPIO as GPIO

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen size
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

circle_radius = 20  # radius of the white circle

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Clear screen and draw the white circle at the mouse position
    screen.fill(BLACK)
    pygame.draw.circle(screen, WHITE, (mouse_x, mouse_y), circle_radius)
    pygame.display.flip()
    # pygame.time.delay(16)

pygame.quit()
# sys.exit()