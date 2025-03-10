import pygame#,pigame
import os
import sys
import RPi.GPIO as GPIO

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen size
# size = width, height = 1024, 768
size = width, height = 1280, 720
tft_size = tft_width, tft_height = 320, 240

size = width, height = 1024, 768

# Env variables to display/control on projector (fb0) or piTFT (fb1)
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
# screen.fill(BLACK)
pygame.mouse.set_visible(False)
# pygame.display.update()
# pitft = pigame.PiTft()

circle_radius = 20  # radius of the white circle
recording = False  # whether we are recording a path
playback = False  # whether the circle is moving along the path
path = []  # list to store the path points
path_idx = 0  # current position in the path

running = True
while running:
    # pitft.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            path = []  # Clear the previous path
            recording = True  # Start recording
            playback = False  # Reset playback
        elif event.type == pygame.MOUSEBUTTONUP:
            recording = False  # Stop recording
            playback = True  # Start playback
            path_idx = 0  # Reset playback index

    # Track mouse movement while left click is held
    if recording:
        x, y = pygame.mouse.get_pos()

        # Apply 90-degree rotation transformation
        transformed_x = int(y * (1024 / 768))
        transformed_y = int((1024 - x) * (768 / 1024))

        path.append((transformed_x, transformed_y))
    
    # Move along the recorded path
    if playback and path:
        if path_idx < len(path):
            circle_x, circle_y = path[path_idx]
            path_idx += 1
        else:
            playback = False  # Stop playback when the end is reached
    else:
        circle_x, circle_y = None, None  # Hide the circle initially
    
    # Clear screen and draw the circle if needed
    screen.fill(BLACK)
    if circle_x is not None and circle_y is not None:
        pygame.draw.circle(screen, WHITE, (circle_x, circle_y), circle_radius)
    pygame.display.flip()
    pygame.time.delay(16)  # 60 FPS

# del(pitft)
pygame.quit()
# sys.exit()
