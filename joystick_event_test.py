# MAIN LOOP
import pygame
import time
from joymap import GPIO_to_Keyboard  # Assuming the name of your class file
from events import JOY_LEFT_EVENT, JOY_RIGHT_EVENT, JOY_UP_EVENT, JOY_DOWN_EVENT, BUTTON_1_EVENT, BUTTON_2_EVENT

# Initialize pygame
pygame.init()

# Instantiate GPIO_to_Keyboard
joystick = GPIO_to_Keyboard()



# Set screen dimensions
screen_width, screen_height = 640, 480

# Create a display surface
screen = pygame.display.set_mode((screen_width, screen_height))

# Set a font for text display
font = pygame.font.Font(None, 36)

# Main game loop
running = True
while running:
    # Clear the screen
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle custom joystick and button events
        elif event.type == JOY_LEFT_EVENT:
            text = font.render('Joystick moved left', True, (255, 255, 255))
            screen.blit(text, (200, 200))
        elif event.type == JOY_RIGHT_EVENT:
            text = font.render('Joystick moved right', True, (255, 255, 255))
            screen.blit(text, (200, 230))
        elif event.type == JOY_UP_EVENT:
            text = font.render('Joystick moved up', True, (255, 255, 255))
            screen.blit(text, (200, 260))
        elif event.type == JOY_DOWN_EVENT:
            text = font.render('Joystick moved down', True, (255, 255, 255))
            screen.blit(text, (200, 290))
        elif event.type == BUTTON_1_EVENT:
            text = font.render('Button 1 pressed', True, (255, 255, 255))
            screen.blit(text, (200, 320))
        elif event.type == BUTTON_2_EVENT:
            text = font.render('Button 2 pressed', True, (255, 255, 255))
            screen.blit(text, (200, 350))

    # Update the display
    pygame.display.flip()

    # Sleep for a bit to control the frame rate
    time.sleep(0.01)

pygame.quit()