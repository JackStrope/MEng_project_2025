# Simple user interface for editing parameters

import pygame,pigame
from pygame.locals import *
import os
import sys
import time
from time import sleep
import RPi.GPIO as GPIO
from enum import Enum
import json

# Colors
WHITE = (255,255,255)
BLACK = (0, 0, 0)

# Screen size
size = width, height = 320, 240

# Env variables to display/control on monitor (fb0) or piTFT (fb1)
os.putenv('SDL_VIDEODRV','fbcon')
os.putenv('SDL_FBDEV', '/dev/fb-pitft')
os.putenv('SDL_MOUSEDRV','dummy')
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY','')

# Set up pygame display and piTFT for touch events
pygame.init()
lcd = pygame.display.set_mode(size)
lcd.fill(BLACK)
pygame.mouse.set_visible(False) # hide mouse
pitft = pigame.PiTft()
pygame.display.update()

# Load parameters
PARAM_FILE = "params_grating_acuity.json"

with open(PARAM_FILE, "r") as f:
    params = json.load(f)

# Fonts
font_big   = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 30)

# Dictionary of buttons for touch screen
touch_buttons_select = {'bar width':(160,30), 'speed':(160,70), 'bars to move':(160,110),
                        'bar angle (deg)':(160,150), '< Done >':(160,200)}
touch_buttons_bar_width = {'Enter bar width:':(160,90)}

# Define pages
class Page(Enum):
    SELECT    = "select"
    BAR_WIDTH = "bar_width"

# Initialize screen
page = Page.SELECT

start_time = time.time()
pygame.display.update()
running = True

while running:
    pitft.update()
    # Scan touchscreen events
    for event in pygame.event.get():
        if (event.type is MOUSEBUTTONUP):
            x,y = pygame.mouse.get_pos()
            # Events on select screen
            if page == Page.SELECT:
                # Check if a button was pressed
                if x > 110 and x < 210:
                    if y < 50:
                        page = Page.BAR_WIDTH
                    else:
                        running = False
    
    # Print screen for appropriate level
    if page == Page.SELECT:
        lcd.fill(BLACK) # Erase the Work space
        # Display select screen buttons
        for k,v in touch_buttons_select.items():
            text_surface = font_big.render('%s'%k, True, WHITE)
            rect = text_surface.get_rect(center=v)
            lcd.blit(text_surface, rect)
    elif page == Page.BAR_WIDTH:
        lcd.fill(BLACK) # Erase the Work space
        # Display bar width screen buttons
        for k,v in touch_buttons_bar_width.items():
            text_surface = font_big.render('%s'%k, True, WHITE)
            rect = text_surface.get_rect(center=v)
            lcd.blit(text_surface, rect)
    
    pygame.display.flip() # display workspace on screen
    pygame.time.delay(16) # delay for 16ms (60fps)
    sleep(0.1)  # Check for button press or touch event every 100 ms

print("exiting param editor UI")
del(pitft)
pygame.quit()
sys.exit()