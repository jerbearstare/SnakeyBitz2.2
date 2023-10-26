
# ────────────────────────────────────────
#   :::::: I M P O R T S : :  :  :  :  :
# ────────────────────────────────────────
# WINDOWS UI
import os
from tkinter import Y

if not os.environ.get('XDG_RUNTIME_DIR'): #try to run on remote desktop
    os.environ['XDG_RUNTIME_DIR'] = '/tmp' # set to temp

import pygame
import time
import requests
import json
import datetime
import numpy as np
import random
import io
#import csv
import serial


# ────────────────────────────────────────
#   :::::: C O N S T A N T S : :  :  :  :
# ────────────────────────────────────────


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600

# GAME MECHANICS
stdDeviations = [10, 5, 1, .5, 0.1, 0.01, 0.005, 0.001, 0.0005, 0.0001]
scaler = 6500

# JOYSTICK CONFIGURATION FOR SENSITIVITY
JOYSTICK_DEBOUNCE_TIME = 0.1  # Time in seconds
JOYSTICK_NEGATIVE_THRESHOLD = -0.5  # Replace with your desired value
JOYSTICK_POSITIVE_THRESHOLD = 0.5   # Replace with your desired value

JOYSTICK_DEADZONE = 0.2  # Adjust this value based on how sensitive you want to make the joystick.

# User events for joystick encoder
JOY_LEFT_EVENT = pygame.USEREVENT + 1
JOY_RIGHT_EVENT = pygame.USEREVENT + 2
JOY_UP_EVENT = pygame.USEREVENT + 3
JOY_DOWN_EVENT = pygame.USEREVENT + 4
BUTTON_1_EVENT = pygame.USEREVENT + 5
BUTTON_2_EVENT = pygame.USEREVENT + 6

#Global history Variable
HISTORY_FILE = 'history.txt'

#LNBITZ
url = "https://legend.lnbits.com/withdraw/api/v1/links"
API_KEY_write = '4f185c43df804edbb0ab8cbad4973566'
write_key_header = {"X-Api-Key": API_KEY_write}


# ─────────────────────────────────
#   :::::: P Y G A M E : :  :  :  :
# ────────────────────────────────-
# Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
pygame.display.set_caption('SnakeyBitz')
clock = pygame.time.Clock()

### Coinreader Initialation of Serial###
if __name__ == '__main__':
    Serial_channel = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    Serial_channel.flush()

# Fonts
font_header = pygame.font.Font(os.path.join("font", "8-BIT WONDER.TTF"), 80)
font_header.set_bold(True)
font_subheader = pygame.font.Font(os.path.join("font", "8-BIT WONDER.TTF"), 30)
font_subheader.set_bold(False)
font_highscore = pygame.font.Font(os.path.join("font", "8-BIT WONDER.TTF"), 20)
font_highscore.set_bold(False)
font_inst = pygame.font.SysFont('gill sans', 30, bold=False)
font_inst1 = pygame.font.SysFont('gill sans', 15, bold=False)
font_score = pygame.font.Font('font/8-BIT WONDER.TTF', 40)
font_score.set_bold(True)

# ────────────────────────────────────────────────
#   :::::: H E L P E R   F U N C T I O N S : :  :
# ────────────────────────────────────────────────

# Function for calling BTC price
def get_bitcoin_price_in_cad():
    bitcoin_api_url = "https://api.coingecko.com/api/v3/simple/price"
    parameters = {
        "ids": "bitcoin",
        "vs_currencies": "cad"
    }

    response = requests.get(bitcoin_api_url, params=parameters)
    response_json = response.json()
    btc_price = response_json["bitcoin"]["cad"]
    response.close()
    return btc_price
# Function for Reading Coins

def check_coin_inserted(Serial_channel, previousBank):  # Nested function to check if a coin has been inserted
    if Serial_channel.in_waiting > 0:  # Check if there are bytes to read from the serial channel
        b = Serial_channel.readline()  # Read a line from the serial channel
        raw = b.decode()  # Decode the bytes read to a string
        ardBank = raw.rstrip('utf-8')  # Remove trailing 'utf-8' characters from the string
        if float(ardBank) > previousBank:  # Check if the bank balance has increased, indicating a coin insertion
            return True  # Return True if a coin has been inserted
    return False  # Return False if no coin has been inserted

# ─────────────────────────────────────────────
#   :::::: H E L P E R   C L A S S E S : :  :
# ─────────────────────────────────────────────


class JoystickManager:
    def __init__(self):
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0) if pygame.joystick.get_count() > 0 else None
        if self.joystick:
            self.joystick.init()
        self.last_horizontal = 0
        self.last_vertical = 0
        self.last_event_time = None

    def handle_joystick_events(self, events):
        if not self.joystick:
            return

        # Only use event-based axis values
        horizontal_axis = 0
        vertical_axis = 0

        for event in events:
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:  # X-axis
                    if abs(event.value) >= JOYSTICK_DEADZONE:
                        horizontal_axis = event.value
                elif event.axis == 1:  # Y-axis
                    if abs(event.value) >= JOYSTICK_DEADZONE:
                        vertical_axis = event.value

            # BUTTON EVENTS
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    pygame.event.post(pygame.event.Event(BUTTON_1_EVENT))
                elif event.button == 1:
                    pygame.event.post(pygame.event.Event(BUTTON_2_EVENT))

        current_time = time.time()

        # Check if the joystick has moved a significant amount since the last event
        significant_horizontal_move = abs(horizontal_axis - self.last_horizontal) > 2 * JOYSTICK_DEADZONE
        significant_vertical_move = abs(vertical_axis - self.last_vertical) > 2 * JOYSTICK_DEADZONE

        if significant_horizontal_move or significant_vertical_move or self.last_event_time is None or current_time - self.last_event_time > JOYSTICK_DEBOUNCE_TIME:
            # Handle left/right movement
            if horizontal_axis < (JOYSTICK_NEGATIVE_THRESHOLD - JOYSTICK_DEADZONE):
                pygame.event.post(pygame.event.Event(JOY_LEFT_EVENT))
                self.last_event_time = current_time
                print(f"[DEBUG - {datetime.datetime.now()}] LEFT event fired!")
            elif horizontal_axis > (JOYSTICK_POSITIVE_THRESHOLD + JOYSTICK_DEADZONE):
                pygame.event.post(pygame.event.Event(JOY_RIGHT_EVENT))
                self.last_event_time = current_time

            # Handle up/down movement
            if vertical_axis < (JOYSTICK_NEGATIVE_THRESHOLD - JOYSTICK_DEADZONE):
                pygame.event.post(pygame.event.Event(JOY_UP_EVENT))
                self.last_event_time = current_time
            elif vertical_axis > (JOYSTICK_POSITIVE_THRESHOLD + JOYSTICK_DEADZONE):
                pygame.event.post(pygame.event.Event(JOY_DOWN_EVENT))
                self.last_event_time = current_time

        self.last_horizontal = horizontal_axis
        self.last_vertical = vertical_axis

    def reset_joystick(self):
        self.last_horizontal = 0
        self.last_vertical = 0
        self.last_event_time = None

    def cleanup(self):
        if self.joystick:
            self.joystick.quit()



# ──────────────────────────────────────────────────────────────
#   :::::: G A M E    S T A T E   C L A S S E S : :  :  :  :  :
# ──────────────────────────────────────────────────────────────

class StartMenuState:
    def __init__(self):
        self.score_values = []
        self.initials = ""
        self.highest_score = 0
        self.HISTORY_FILE = 'history.txt'  # Added this line to set the path of the history file
        self.header = font_header.render('SnakeyBitz', True, (255, 215, 0))
        self.subheader = font_subheader.render('Insert dirty fiat to win BTC', True, (255, 255, 255), pygame.BLEND_RGB_ADD)
        self.highscore_header = font_highscore.render('', True, (255, 215, 0))
        self.last_switch_time = pygame.time.get_ticks()
        self.switch_duration = 500
        self.color_state = True
        self.joystick_manager = JoystickManager()
        self.HISTORY_FILE = 'history.txt'  # Pointing to the file that contains game history
    
    def enter_state(self):
        # Clear out all old events to prevent unwanted triggers
        pygame.event.clear()
        self.process_history_file()
        self.joystick_manager.reset_joystick()

    def handle_events(self, events):
        global credits
        self.joystick_manager.handle_joystick_events(events)
        for event in events:  # Iterate over each event in the list
            if event.type == BUTTON_1_EVENT:
                if credits > 0:
                    btc_price = get_bitcoin_price_in_cad()
                    return GameLoopState(self.highest_score, btc_price)
        return self

    def update(self):
        pass

    def process_history_file(self):
        with open(self.HISTORY_FILE, 'r') as file:
            for line in file:  # Reads the file line by line
                row = line.strip().split(",")  # Split the line by commas
                score = int(row[2])  # Get the score from the third column
                initials = row[-1].strip()  # Get initials from the last column

                if score > self.highest_score:
                    self.highest_score = score
                    self.initials = initials

    def render(self):
        screen.fill((0, 0, 0))  # Clear the screen
    
        # Checking elapsed time for color switching
        current_time = pygame.time.get_ticks()
        if current_time - self.last_switch_time > self.switch_duration:
            self.color_state = not self.color_state
            self.last_switch_time = current_time

        # Choose color based on self.color_state
        if self.color_state:
            subheader_color = (255, 255, 255)
        else:
            subheader_color = (200, 200, 200)

        # Rendering texts using the helper function
        render_text('SnakeyBitz', 80, (255, 215, 0), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50)
        render_text('Insert dirty fiat to win BTC', 30, subheader_color, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20)  # Adjusted font size
        render_text(f"Credits: {credits}", 30, (255, 255, 255), SCREEN_WIDTH//2, 30, 'gill sans')
        render_text("18+ Please gamble responsibly", 30, (255, 255, 255), SCREEN_WIDTH//2, SCREEN_HEIGHT - 30, 'gill sans')  # Adjusted position

        if self.initials:
            highscore_text = 'HIGHSCORE  ' + self.initials + '   ' + str(self.highest_score)
            render_text(highscore_text, 20, (255, 215, 0), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 60)  # Adjusted font size
        
        pygame.display.update()

class GameLoopState: 
    def __init__(self, highest_score, btc_price):
        self.highest_score = highest_score
        self.gmech_modifier = float(btc_price)/scaler
        self.btc_price = btc_price
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.YELLOW = (255, 255, 0)
        self.ORANGE = (255, 165, 0)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.CYAN = (0, 255, 255)
        self.PURPLE = (128, 0, 128)
        self.BROWN = (165, 42, 42)
        self.GOLD = (255, 215, 0)
        self.joystick_manager = JoystickManager()

        self.score = 5

        self.counter = 0

        global credits
        if credits > 0:
            credits -= 1

        self.all_sprites_list = pygame.sprite.Group()

        self.x_position = 300
        self.y_position = 300
        self.x_change = 0
        self.y_change = 0
        self.snake_size = 10
        self.snake_list = []
        self.snake_length = 1

        self.food_x = round(random.randrange(0, SCREEN_WIDTH - self.snake_size) / self.snake_size) * 10
        self.food_y = round(random.randrange(0, SCREEN_HEIGHT - self.snake_size) / self.snake_size) * 10

        self.colors = np.array(['RED', 'BLUE', 'GREEN', 'YELLOW', 'ORANGE', 'WHITE', 'CYAN', 'PURPLE', 'BROWN', 'GOLD'])
        self.color_matrix = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.chosen_color = np.random.choice(self.colors, p=stdDeviations/np.sum(stdDeviations))
        self.speed = 20

        self.clock = pygame.time.Clock()

    def enter_state(self):
        # Clear out all old events to prevent unwanted triggers
        pygame.event.clear()
        self.joystick_manager.reset_joystick()

    def handle_events(self, events):
        self.joystick_manager.handle_joystick_events(events)
        for event in events:
            if event.type == JOY_LEFT_EVENT and not self.x_change > 0:
                self.x_change = -self.snake_size
                self.y_change = 0
                print(f"[DEBUG - {datetime.datetime.now()}] LEFT event received in GAMELOOPState!")
            elif event.type == JOY_RIGHT_EVENT and not self.x_change < 0:
                self.x_change = self.snake_size
                self.y_change = 0
                print("RIGHT from GameLoopState")
            elif event.type == JOY_UP_EVENT and not self.y_change > 0:
                self.y_change = -self.snake_size
                self.x_change = 0
                print("UP from GameLoopState")
            elif event.type == JOY_DOWN_EVENT and not self.y_change < 0:
                self.y_change = self.snake_size
                self.x_change = 0

            if (
            self.x_position > SCREEN_WIDTH
            or self.x_position < 0
            or self.y_position > SCREEN_HEIGHT
            or self.y_position < 0
            or [self.x_position, self.y_position] in self.snake_list[:-1]

            ):
                if self.score > self.highest_score:
                    return HighScoreState(self.score, self.color_matrix, self.btc_price, self.counter)
                else:
                    return GameOverState(self.score, self.color_matrix, self.btc_price, self.counter)

        return self

    def draw_snake(self, snake_list, snake_size):
        for xy in snake_list:
            pygame.draw.rect(screen, self.GREEN, (xy[0], xy[1], snake_size, snake_size))

    def update(self):
        self.x_position += self.x_change
        self.y_position += self.y_change

        if self.x_position == self.food_x and self.y_position == self.food_y:
            if self.chosen_color == 'RED':
                points = round(10 / float(self.gmech_modifier))
                self.color_matrix[0] += 1
            elif self.chosen_color == 'BLUE':
                points = round(25 / float(self.gmech_modifier))
                self.color_matrix[1] += 1
            elif self.chosen_color == 'GREEN':
                points = round(50 / float(self.gmech_modifier))
                self.color_matrix[2] += 1
            elif self.chosen_color == 'YELLOW':
                points = round(100 / float(self.gmech_modifier))
                self.color_matrix[3] += 1
            elif self.chosen_color == 'ORANGE':
                points = round(250 / float(self.gmech_modifier))
                self.color_matrix[4] += 1
            elif self.chosen_color == 'WHITE':
                points = round(500 / float(self.gmech_modifier))
                self.color_matrix[5] += 1
            elif self.chosen_color == 'CYAN':
                points = round(1000 / float(self.gmech_modifier))
                self.color_matrix[6] += 1
            elif self.chosen_color == 'PURPLE':
                points = round(50000 / float(self.gmech_modifier))
                self.color_matrix[7] += 1
            elif self.chosen_color == 'BROWN':
                points = round(75000 / float(self.gmech_modifier))
                self.color_matrix[8] += 1
            elif self.chosen_color == 'GOLD':
                points = round(10000 / float(self.gmech_modifier))
                self.color_matrix[9] += 1
            self.food_x = round(random.randrange(0, SCREEN_WIDTH - self.snake_size) / 10.0) * 10.0
            self.food_y = round(random.randrange(0, SCREEN_HEIGHT - self.snake_size) / 10.0) * 10.0
            self.snake_length += 1
            self.chosen_color = np.random.choice(self.colors, p=stdDeviations/np.sum(stdDeviations))
            self.score = points + self.score
            self.counter += 1

        self.snake_list.append([self.x_position, self.y_position])
        if len(self.snake_list) > self.snake_length:
            del self.snake_list[0]

    def render(self):
        screen.fill(self.BLACK)
        self.draw_snake(self.snake_list, self.snake_size)  # Here we call the draw_snake() method
        pygame.draw.rect(screen, self.chosen_color, [self.food_x, self.food_y, self.snake_size, self.snake_size])
        font = pygame.font.SysFont('gill sans', 30)
        text = font.render("Score " + str(self.score), True, (255, 255, 255))
        screen.blit(text, (10, 10))
        pygame.display.update()
        self.clock.tick(self.speed)

class HighScoreState:
    def __init__(self, score, color_matrix, btc_price, counter):
        self._btc_price = btc_price
        self._counter = counter
        self._FONT_SIZE = 100
        self._score = score
        self._color_matrix = color_matrix
        self._font = pygame.font.Font(os.path.join("font", "8-BIT WONDER.TTF"), self._FONT_SIZE)
        self._font.set_bold(True)
        self._MAX_CHARS = 3
        self._input_box_rect = pygame.Rect(SCREEN_WIDTH // 2 - self._FONT_SIZE * self._MAX_CHARS // 2 + 0,
                                           (SCREEN_HEIGHT + 100) // 2 - self._FONT_SIZE // 2,
                                           self._FONT_SIZE * self._MAX_CHARS, self._FONT_SIZE)
        self._input_text = ["A", "A", "A"]
        self._cursor_pos = 0
        self._letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.player_name = ""
        self.cursor_position = 0
        self._initialize_texts()
        self.joystick_manager = JoystickManager()
    
    def _initialize_texts(self):
        self._high_score_text = self._create_text('HIGH SCORE', self._FONT_SIZE, (255, 215, 0), bold=True)
        self._white_button_text_display1 = self._create_text('press white button to continue', 15, (255, 255, 255))

    def _create_text(self, text, size, color, bold=False):
        font = pygame.font.Font('font/8-BIT WONDER.TTF', size) if '8-BIT WONDER' in text else pygame.font.SysFont('gill sans', size)
        font.set_bold(bold)
        return font.render(text, True, color)

    def enter_state(self):
        # Clear out all old events to prevent unwanted triggers
        pygame.event.clear()
        self.joystick_manager.reset_joystick()

    def handle_events(self, events):
        self.joystick_manager.handle_joystick_events(events)
        for event in events:
            if event.type == BUTTON_1_EVENT:
                name = "".join(self._input_text)
                #with open(HISTORY_FILE, 'a') as file:
                    #file.write(f"{datetime.datetime.now()},{name},{self._score}\n")
                return GameOverState(self._score, self._color_matrix, self._btc_price, self._counter, name)
            elif event.type in [JOY_LEFT_EVENT, JOY_RIGHT_EVENT, JOY_UP_EVENT, JOY_DOWN_EVENT]:
                self._handle_joy_events(event.type)
        return self

    def _handle_joy_events(self, event_type):
        if event_type == JOY_LEFT_EVENT:
            self._cursor_pos = max(0, self._cursor_pos - 1)
            print(f"[DEBUG - {datetime.datetime.now()}] LEFT event received in highscoreState!")
        elif event_type == JOY_RIGHT_EVENT:
            self._cursor_pos = min(self._MAX_CHARS - 1, self._cursor_pos + 1)
        elif event_type in [JOY_UP_EVENT, JOY_DOWN_EVENT]:
            index = self._letters.find(self._input_text[self._cursor_pos])
            index = (index + (-1 if event_type == JOY_UP_EVENT else 1)) % len(self._letters)
            self._input_text[self._cursor_pos] = self._letters[index]
        time.sleep(0.2 if event_type in [JOY_LEFT_EVENT, JOY_RIGHT_EVENT] else 0.1)

    def update(self):
        return self

    def render(self):
        screen.fill((0, 0, 0))
        input_text_surface = self._font.render("".join(self._input_text), True, (255, 255, 255))
        cursor_rect = pygame.Rect(self._input_box_rect.x + self._cursor_pos * self._FONT_SIZE, self._input_box_rect.y + 5, 2, self._FONT_SIZE)
        pygame.draw.rect(input_text_surface, (255, 255, 255), cursor_rect)
        self._render_texts(input_text_surface)
        pygame.display.update()

    def _render_texts(self, input_text_surface):
        screen.blit(self._high_score_text, (SCREEN_WIDTH / 2 - self._high_score_text.get_width() / 2, SCREEN_HEIGHT / 2 - self._high_score_text.get_height() / 2 - 220))
        screen.blit(self._white_button_text_display1, (SCREEN_WIDTH / 2 - self._white_button_text_display1.get_width() / 2, SCREEN_HEIGHT / 2 - self._white_button_text_display1.get_height() / 2 + 280))
        screen.blit(input_text_surface, (self._input_box_rect.x + 5, self._input_box_rect.y + 5))

class GameOverState:
    TIMER_EVENT = pygame.USEREVENT + 7  # Create a new event type

    def __init__(self, score, color_matrix, btc_price, counter, initials="XXX"):
        self.gameover_count = 50
        self.score = score
        self.btc_price = btc_price
        self.color_matrix = color_matrix
        self.gameover = True
        self.ran_once = False
        self.counter = counter
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.withdraw_id = None
        self.initials = initials
        self.joystick_manager = JoystickManager()
      
        pygame.time.set_timer(self.TIMER_EVENT, 1000)  # Start a timer that fires every second

    def enter_state(self):
        # Clear out all old events to prevent unwanted triggers
        pygame.event.clear()
        self.joystick_manager.reset_joystick()

    def handle_events(self, events):
        self.joystick_manager.handle_joystick_events(events)
        for event in events:
            if event.type == BUTTON_1_EVENT:
                return StartMenuState()
            elif event.type == BUTTON_2_EVENT:
                self.gameover_count -= 5
                #if self.gameover_count <= 0:
                    #return StartMenuState()
            elif event.type == self.TIMER_EVENT:
                self.gameover_count -= 1
                if self.gameover_count <= 0:
                    return StartMenuState()
            elif event.type == JOY_LEFT_EVENT:
                print(f"[DEBUG - {datetime.datetime.now()}] LEFT event received in gameoverState!")
            elif event.type == JOY_RIGHT_EVENT:
                print("RIGHT from GameOverState")
            elif event.type == JOY_UP_EVENT:
                print("UP from GameOverState")
            elif event.type == JOY_DOWN_EVENT:
                print("DOWN from GameOverState")

        return self

    def make_api_call(self, url, write_key_header):
        create_payload = {
            "title": "Thanks",
            "min_withdrawable": self.score,
            "max_withdrawable": self.score,
            "uses": 1,
            "wait_time": 1,
            "is_unique": "true"}

        # API Call
        create_response = requests.post(url, headers=write_key_header, json=create_payload)

        # Isolate withdrawal ID
        json_data = create_response.json()
        self.withdraw_id = json_data['id']
        print(self.withdraw_id)

    def log_player(self):
        with open(HISTORY_FILE, 'a') as open_history: 
            open_history.write(f"{self.counter}, {self.withdraw_id}, {self.score}, {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, ${self.btc_price}, {self.color_matrix}, {self.initials}\n")
            open_history.flush()  # Explicitly flush the buffer after each write

    def center_blit(self, screen, text, y_offset=0):
        """Render the text and blit it at the center of the screen with a y_offset"""
        screen.blit(text, (self.SCREEN_WIDTH/2 - text.get_width()/2, self.SCREEN_HEIGHT/2 - text.get_height()/2 + y_offset))

    def update(self, url, write_key_header):
        if self.gameover and not self.ran_once:
            self.make_api_call(url, write_key_header)  # Make the API call
            self.log_player()
            # Change flag to ensure API call only runs once
            self.ran_once = True

    def render(self):
            # Fill the screen
        screen.fill((0, 0, 0))

        # Initialize pygame font
        pygame.font.init()

        # Render and blit each text in the center
        font_game_over = pygame.font.Font('font/8-BIT WONDER.TTF', 80)
        font_game_over.set_bold(True)
        game_over = font_game_over.render('Game Over', True, (255, 215, 0))
        self.center_blit(screen, game_over, -220)

        score_display = font_score.render('Your Score ' + str(self.score), True, (255, 255, 255))
        self.center_blit(screen, score_display, -150)

        font_play_again = pygame.font.SysFont('gill sans', 30)
        font_play_again.set_bold(True)



        play_again_display = font_play_again.render('Insert Coin to Play Again or White Button for Menu ', True, (255, 255, 255))
        self.center_blit(screen, play_again_display, 0)

        if self.withdraw_id is not None:  # Ensure withdraw_id is not None before using
            font_id = pygame.font.SysFont('gill sans', 20)
            font_id.set_bold(True)
            id_display = font_id.render('Your Game ID ' + self.withdraw_id, True, (255, 255, 255))
            self.center_blit(screen, id_display, 250)

            # Prepare the QR code
            svg_url = "https://legend.lnbits.com/withdraw/img/{}".format(self.withdraw_id)
            svg_string = requests.get(svg_url).content
            with io.BytesIO(svg_string) as f:
                parsed_image = pygame.image.load(f, 'RGBA')
            converted_image = parsed_image.convert_alpha()
            pygame.image.save(converted_image, 'QR.png')

            # Display QR code
            shift_qr_vert = 130
            imgQR = pygame.image.load('QR.png')
            white_square = pygame.Rect(self.SCREEN_WIDTH/2 - imgQR.get_width()/2, self.SCREEN_HEIGHT/2 - imgQR.get_height()/2 + shift_qr_vert, 195,195) #white square
            pygame.draw.rect(screen, (255, 255, 255), white_square)
            screen.blit(imgQR, (self.SCREEN_WIDTH/2 - imgQR.get_width()/2, self.SCREEN_HEIGHT/2 - imgQR.get_height()/2 + shift_qr_vert))

        gameover_count_font = pygame.font.SysFont('gill sans', 35, bold=True)
        gameover_count = gameover_count_font.render(str(self.gameover_count), True, (255, 255, 255))
        screen.blit(gameover_count, (SCREEN_WIDTH/2 - gameover_count.get_width()/2+480, SCREEN_HEIGHT/2 - gameover_count.get_height()/2 - 270))

        inst_display = font_inst.render('Scan QR code with lightning wallet to collect winnings', True, (255, 215, 0))
        inst_display1 = font_inst1.render('visit legend.lnbits.com to create a wallet. IF ERROR OCCURS SEND GAME ID to Twitter/Email support.', True, (255, 255, 255))
        self.center_blit(screen, inst_display, -40)
        self.center_blit(screen, inst_display1, 280)

        credit_text = font_inst1.render(f"Credits: {credits}", True, (255, 255, 255))
        screen.blit(credit_text, (SCREEN_WIDTH//2 - credit_text.get_width()//2, 10))

        # Update the screen
        pygame.display.update()
        self.speed = 20

# ──────────────────────────────────────────
#   :::::: M A I N   L O O P  : :  :  :  :  :
# ──────────────────────────────────────────

running = True

def run_game(Serial_channel):
    global running, credits

    FPS = 60  # adjust the frame rate
    credits = 0
    previousBank = 0  # initialize previousBank with an appropriate value
    current_state = StartMenuState()
    #joystick_manager = JoystickManager()

    clock = pygame.time.Clock()  # Initialize the clock

    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Check if a coin has been inserted
        coin = check_coin_inserted(Serial_channel, previousBank)
        if coin:
            credits += 1  # Increase credits by one when a coin is inserted
        
        #

        # State Management
        new_state = current_state.handle_events(events)
        if new_state is not current_state:
            current_state = new_state
            while pygame.event.get():
                pass
            current_state.enter_state()
        
        if isinstance(current_state, GameOverState):
            update_state = current_state.update(url, write_key_header)
        else:
            update_state = current_state.update()

        if update_state is not None:
            current_state = update_state

        current_state.render()

        pygame.display.update()

        clock.tick(FPS)  # Limit the frame rate
    joystick_manager.cleanup() 
    Serial_channel.close()
    pygame.joystick.quit()
    pygame.quit()
    # don't forget to close the Serial_channel when done

run_game(Serial_channel)  # assuming Serial_channel is defined