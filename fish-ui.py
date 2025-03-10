# Simple user interface for launching Python programs via the PiTFT touchscreen

import pygame,pigame
from pygame.locals import *
import os
import sys
import time
from time import sleep
import RPi.GPIO as GPIO
from enum import Enum
import subprocess

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

# # Set up GPIO button 27
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# # Exit the program
# def GPIO27_callback(channel):
#     pygame.quit()
#     import sys
#     sys.exit(0)

# # Callbacks
# GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback)

def init_pygame():
    global lcd, font_big, font_small
    pygame.init()
    pygame.font.init()
    lcd = pygame.display.set_mode(size)
    pygame.mouse.set_visible(False) # hide mouse
    font_big   = pygame.font.Font(None, 50)
    font_small = pygame.font.Font(None, 30)

def init_display():
    global lcd
    pygame.display.init()
    lcd = pygame.display.set_mode(size)
    pygame.mouse.set_visible(False) # hide mouse

def init_pitft():
    global pitft
    pitft = pigame.PiTft()

# Set up pygame display and piTFT for touch events
pygame.init()
lcd = pygame.display.set_mode(size)
lcd.fill(BLACK)
pygame.mouse.set_visible(False) # hide mouse
pitft = pigame.PiTft()
pygame.display.update()

# Fonts
font_big   = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 30)

# Dictionary of buttons for touch screen
touch_buttons_start = {'Start':(160,90), 'Exit':(160,150)}
touch_buttons_quit = {'Quit?':(160, 80), 'Yes':(100,160), 'No':(220,160)}
touch_buttons_p1 = {'grating_acuity':(160,30), 'white_circle':(160,70), 'mouse_control':(160,110),
                    'one_boid':(160,150), '< Quit >':(160,200), 'Next >':(260,200)}
touch_buttons_p2 = {'boids':(160,30), 'fish_circle':(160,70), 'trace_path':(160,110),
                    '':(160,150), '< Prev':(60,200), '< Quit >':(160,200)}
touch_buttons_exit = {'Shut Down':(160,60), 'Quit to Terminal':(160,120), 'Cancel':(160,180)}

start_time = time.time()
                        
pygame.display.update()

# Define pages
class Page(Enum):
    START = "start"
    QUIT  = "quit"
    EXIT  = "exit"
    PAGE1 = "page1"
    PAGE2 = "page2"

# Initialize screen
page = Page.START

running = True

# try:
while running:
    pitft.update()
    # Scan touchscreen events
    for event in pygame.event.get():
        if (event.type is MOUSEBUTTONUP):
            x,y = pygame.mouse.get_pos()
            # Touch events on start screen
            if page == Page.START:
                if x > 110 and x < 210:
                    # Determine which button was pressed
                    if y > 60 and y < 120:
                        # Start button pressed--go to page 1
                        page = Page.PAGE1
                    elif y > 120 and y < 180:
                        # Exit button pressed
                        page = Page.EXIT
            
            # Touch events on quit screen
            elif page == Page.QUIT:
                # Check if touch coords lie on a button
                if y > 130 and y < 190 and x > 60 and x < 260:
                    # Button pressed--check which
                    if x < 160:
                        # 'Yes' button pressed--quit to start screen
                        page = Page.START
                    else:
                        # 'No' button pressed--return to previous screen
                        page = prev_page

            # Touch events on page 1
            elif page == Page.PAGE1:
                if y < 170:
                    if x > 110 and x < 210:
                        if y < 50:
                            print("grating acuity")
                            pygame.display.quit()
                            return_code = subprocess.call(["sudo", "python", "/home/pi/fish/grating_acuity_angle.py"])
                            if return_code == 10:
                                print("editing grating acuity params")
                                del(pitft)
                                subprocess.run(["sudo", "python", "/home/pi/fish/edit_grating_params.py"])
                                init_pitft()
                            init_display()
                        elif y < 90:
                            print("white circle")
                            pygame.display.quit()
                            subprocess.run(["sudo", "python", "/home/pi/fish/white_circle.py"])
                            init_display()
                        elif y < 130:
                            print("mouse control")
                            pygame.display.quit()
                            subprocess.run(["sudo", "python", "/home/pi/fish/mouse_control.py"])
                            init_display()
                        else:
                            pygame.display.quit()
                            subprocess.run(["sudo", "python", "/home/pi/fish/one_boid.py"])
                            init_display()
                            print("one boid")
                else:  # bottom buttons
                    if x > 120 and x < 200:
                        prev_page = page
                        page = Page.QUIT
                    elif x > 220 and x < 300:
                        page = Page.PAGE2
            
            # Touch events on page 2
            elif page == Page.PAGE2:
                if y < 170:
                    if x > 110 and x < 210:
                        if y < 50:
                            print("boids")
                            pygame.display.quit()
                            subprocess.run(["sudo", "python", "/home/pi/fish/boids.py"])
                            init_display()
                        elif y < 90:
                            print("fish circle")
                            pygame.display.quit()
                            subprocess.run(["sudo", "python", "/home/pi/fish/fish_circle.py"])
                            init_display()
                        elif y < 130:
                            print("trace path")
                            del(pitft)
                            pygame.display.quit()
                            subprocess.run(["sudo", "python", "/home/pi/fish/trace_path.py"])
                            init_display()
                            init_pitft()
                else:
                    if x > 20 and x < 100:
                        page = Page.PAGE1
                    elif x > 120 and x < 200:
                        prev_page = page
                        page = Page.QUIT
            
            # Touch events on exit screen
            elif page == Page.EXIT:
                if x > 110 and x < 210:
                    if y < 90:
                        # Shut down the RPi
                        os.system("sudo shutdown -h now")
                    elif y < 150:
                        # Exit to terminal
                        running = False
                    else:
                        # Cancel--back to start screen
                        page = Page.START
                

    # Print screen for appropriate level
    if page == Page.START:
        lcd.fill(BLACK) # Erase the Work space
        # Display start screen buttons
        for k,v in touch_buttons_start.items():
            text_surface = font_big.render('%s'%k, True, WHITE)
            rect = text_surface.get_rect(center=v)
            lcd.blit(text_surface, rect)
    elif page == Page.QUIT:
        lcd.fill(BLACK) # Erase the Work space
        # Display quit screen buttons
        for k,v in touch_buttons_quit.items():
            text_surface = font_big.render('%s'%k, True, WHITE)
            rect = text_surface.get_rect(center=v)
            lcd.blit(text_surface, rect)
    elif page == Page.PAGE1:
        lcd.fill(BLACK) # Erase the Work space
        # Display page 1 buttons
        for k,v in touch_buttons_p1.items():
            text_surface = font_small.render('%s'%k, True, WHITE)
            rect = text_surface.get_rect(center=v)
            lcd.blit(text_surface, rect)
    elif page == Page.PAGE2:
        lcd.fill(BLACK) # Erase the Work space
        # Display page 2 buttons
        for k,v in touch_buttons_p2.items():
            text_surface = font_small.render('%s'%k, True, WHITE)
            rect = text_surface.get_rect(center=v)
            lcd.blit(text_surface, rect)
    elif page == Page.EXIT:
        lcd.fill(BLACK) # Erase the Work space
        # Display page 1 buttons
        for k,v in touch_buttons_exit.items():
            text_surface = font_small.render('%s'%k, True, WHITE)
            rect = text_surface.get_rect(center=v)
            lcd.blit(text_surface, rect)
    
    pygame.display.flip() # display workspace on screen
    pygame.time.delay(16) # delay for 16ms (60fps)
    sleep(0.1)  # Check for button press or touch event every 100 ms

# except KeyboardInterrupt:
#     pass
# finally:
print("exiting UI")
del(pitft)
pygame.quit()
sys.exit(0)