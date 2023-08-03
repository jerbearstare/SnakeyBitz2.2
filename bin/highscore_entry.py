import pygame
import os
#Joystick and button initialization
#from joymap import *

score = 3000

pygame.init()

history_file = 'history.txt' # replace with the name of your file
score_values = []

with open(history_file) as file:
    for line in file:
        history_fields = line.split(',')
        file_score_value = float(history_fields[2].strip())
        score_values.append(file_score_value)

highest_value = max(score_values)
print(highest_value)

# Set up the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("High Score Entry")



# Set up the font
FONT_SIZE = 100
font = pygame.font.Font(os.path.join("font", "8-BIT WONDER.TTF"), FONT_SIZE, bold=True)

# Set up the input box
MAX_CHARS = 3
input_box_rect = pygame.Rect(SCREEN_WIDTH // 2 - FONT_SIZE * MAX_CHARS // 2 + 0, (SCREEN_WIDTH+100) // 2 - FONT_SIZE // 2, FONT_SIZE * MAX_CHARS, FONT_SIZE)
input_text = ["A", "A", "A"]
cursor_pos = 0
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Main loop
while score > highest_value:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Save the high score and exit
                name = "".join(input_text)
                print(f"High score: {name}")
                score = highest_value
                # pygame.quit()
                # quit()
            elif event.key == pygame.K_LEFT:
                # Move the cursor to the left
                cursor_pos = max(0, cursor_pos - 1)
                time.sleep(.1)
            elif event.key == pygame.K_RIGHT:
                # Move the cursor to the right
                cursor_pos = min(MAX_CHARS - 1, cursor_pos + 1)
                time.sleep(.1)
            elif event.key == pygame.K_UP:
                # Move to the previous letter
                index = letters.find(input_text[cursor_pos])
                index = (index - 1) % len(letters)
                input_text[cursor_pos] = letters[index]
                time.sleep(.1)
            elif event.key == pygame.K_DOWN:
                # Move to the next letter
                index = letters.find(input_text[cursor_pos])
                index = (index + 1) % len(letters)
                input_text[cursor_pos] = letters[index]
                time.sleep(.1)
                
    # Clear the window
    window.fill((0, 0, 0))
    
    # Draw the input box
    #pygame.draw.rect(window, (255, 255, 255), input_box_rect, 2)
    input_text_surface = font.render("".join(input_text), True, (255, 255, 255))
    cursor_rect = pygame.Rect(input_box_rect.x + cursor_pos * FONT_SIZE, input_box_rect.y + 5, 2, FONT_SIZE)
    pygame.draw.rect(input_text_surface, (255, 255, 255), cursor_rect)
    window.blit(input_text_surface, (input_box_rect.x + 5, input_box_rect.y + 5))
    
    # Draw the letter selection box
    letter_box_rect = pygame.Rect(input_box_rect.x + cursor_pos * FONT_SIZE, input_box_rect.y - FONT_SIZE, FONT_SIZE, FONT_SIZE)
    pygame.draw.rect(window, (255, 255, 255), letter_box_rect, 2)
    for i, letter in enumerate(letters):
        x = input_box_rect.x + cursor_pos * FONT_SIZE + i * FONT_SIZE
        y = input_box_rect.y - FONT_SIZE
    letter_surface = font.render(letter, True, (255, 255, 255))
    window.blit(letter_surface, (x + 5, y + 5))
    # Update the display
    pygame.display.update()
