
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

# ────────────────────────────────────────────────
#   :::::: H E L P E R   F U N C T I O N S : :  :
# ────────────────────────────────────────────────


def get_bitcoin_price_in_cad(): # Function for calling BTC price
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

def check_coin_inserted(Serial_channel, previousBank):  # Nested function to check if a coin has been inserted
    if Serial_channel.in_waiting > 0:  # Check if there are bytes to read from the serial channel
        b = Serial_channel.readline()  # Read a line from the serial channel
        raw = b.decode()  # Decode the bytes read to a string
        ardBank = raw.rstrip('utf-8')  # Remove trailing 'utf-8' characters from the string
        if float(ardBank) > previousBank:  # Check if the bank balance has increased, indicating a coin insertion
            return True  # Return True if a coin has been inserted
    return False  # Return False if no coin has been inserted

def render_text(text, size, color, x, y, font_type='8-bit', bold=False):
    """Function to render and blit text on the screen"""
    if font_type == '8-bit':
        font = pygame.font.Font(os.path.join("font", "8-BIT WONDER.TTF"), size)
    else:  # gill sans
        font = pygame.font.SysFont('gill sans', size)
    
    font.set_bold(bold)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x - text_surface.get_width() // 2, y - text_surface.get_height() // 2))

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

class ScreensaverState:
    def __init__(self, scores):
        self.scores = scores
        self.enter_time = pygame.time.get_ticks()
        self.joystick_manager = JoystickManager()

    def handle_events(self, events):
        for event in events:
            self.joystick_manager.handle_joystick_events(events)
            if event.type in [JOY_LEFT_EVENT, JOY_RIGHT_EVENT, JOY_UP_EVENT, JOY_DOWN_EVENT, BUTTON_1_EVENT, BUTTON_2_EVENT]:
                return StartMenuState()
        return self

    def update(self):
        if pygame.time.get_ticks() - self.enter_time > 30000:  # 10 seconds
            return StartMenuState()
        return self

    def render(self):
        screen.fill((0, 0, 0))  # Filling with black background
        render_text('TOP HIGHSCORES', 70, (255, 215, 0), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 220)
        y_offset = SCREEN_HEIGHT // 3  # Starting y position
    
        for idx, score_data in enumerate(self.scores[:10]):  # Only take the top 10 scores
            food, score, initials = score_data
            # aligning score, food, and initials to the center of their max width
            score_text = f"{score:^6} Sats"
            food_text = f"No.Food {food:^7}"
            initials_text = f"{initials:^4}"
        
            # Adjusting the padding around the first "|", making it larger
            text = f"{idx+1}. {score_text}     |     {food_text}   |   {initials_text}"
            render_text(text, 30, (255, 215, 0), SCREEN_WIDTH/2, y_offset, "gill sans", True)
            y_offset += 40  # Move down for the next line
        
    pygame.display.flip()
        
    pygame.display.flip()

class StartMenuState:
    def __init__(self):
        self.score_values = []
        self.initials = ""
        self.highest_score = 0
        self.HISTORY_FILE = 'history.txt'  # Added this line to set the path of the history file
        self.last_switch_time_for_color = pygame.time.get_ticks()
        self.last_switch_time_for_state = pygame.time.get_ticks()
        self.switch_duration = 500
        self.color_state = True
        self.joystick_manager = JoystickManager()
    
    def enter_state(self):
        # Clear out all old events to prevent unwanted triggers
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

    def update(self): #contains timer for screensaver switch time
        if pygame.time.get_ticks() - self.last_switch_time_for_state > 10000:  # 3 minutes = 180000 ticks || screensaver switch time
            scores = self.get_top_scores()
            return ScreensaverState(scores)
        pass

    def get_top_scores(self):
        scores = []
        with open(self.HISTORY_FILE, 'r') as file:
            for line in file:
                row = line.strip().split(",")
                food = int(row[0])
                score = int(row[2])
                initials = row[-1].strip()
                scores.append((food, score, initials))
        scores.sort(key=lambda x: x[1], reverse=True)  # Sort by score in descending order
        return scores

    def render(self):
        screen.fill((0, 0, 0))  # Clear the screen
    
        # Checking elapsed time for color switching
        current_time = pygame.time.get_ticks()
        if current_time - self.last_switch_time_for_color > self.switch_duration:
            self.color_state = not self.color_state
            self.last_switch_time_for_color = current_time

        # Choose color based on self.color_state
        if self.color_state:
            subheader_color = (255, 255, 255)
        else:
            subheader_color = (200, 200, 200)

        # Rendering texts using the helper function
        render_text('SnakeyBitz', 80, (255, 215, 0), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50)
        render_text('Insert 25 cents to win Bitcoin', 30, subheader_color, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20)  # Adjusted font size
        render_text(f"Credits: {credits}", 30, (255, 255, 255), SCREEN_WIDTH//2, 30, 'gill sans')
        render_text("Instructions below to set up a lightning wallet before playing", 20, (255, 255, 255), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 60, 'gill sans')
        render_text("18+ Please Gamble Responsibly", 30, (255, 255, 255), SCREEN_WIDTH/2, SCREEN_HEIGHT - 30, 'gill sans', True)  # Adjusted position

        #if self.initials:
            #highscore_text = 'HIGHSCORE  ' + self.initials + '   ' + str(self.highest_score)
            #render_text(highscore_text, 20, (255, 215, 0), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 60, "gill sans", True)  # Adjusted font size
        
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
        pygame.event.clear()

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
        self._score = score
        self._color_matrix = color_matrix
        self._MAX_CHARS = 3
        self._input_box_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100 * self._MAX_CHARS // 2 + 0,
                                           (SCREEN_HEIGHT + 100) // 2 - 100 // 2,
                                           100 * self._MAX_CHARS, 100)
        self._input_text = ["A", "A", "A"]
        self._cursor_pos = 0
        self._letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.player_name = ""
        self.cursor_position = 0
        self.joystick_manager = JoystickManager()

    def enter_state(self):
        # Clear out all old events to prevent unwanted triggers
        pygame.event.clear()
        self.joystick_manager.reset_joystick()

    def handle_events(self, events):
        self.joystick_manager.handle_joystick_events(events)
        for event in events:
            if event.type == BUTTON_1_EVENT:
                name = "".join(self._input_text)
                return GameOverState(self._score, self._color_matrix, self._btc_price, self._counter, name)
            elif event.type in [JOY_LEFT_EVENT, JOY_RIGHT_EVENT, JOY_UP_EVENT, JOY_DOWN_EVENT]:
                self._handle_joy_events(event.type)
        return self

    def _handle_joy_events(self, event_type):
        if event_type == JOY_LEFT_EVENT:
            self._cursor_pos = max(0, self._cursor_pos - 1)
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
        
        # Use centralized text generation function
        render_text('HIGH SCORE', 100, (255, 215, 0), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 220)
        render_text('Hold Yellow to Continue', 15, (255, 215, 0), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 280)
        
        input_text_surface = pygame.font.Font(os.path.join("font", "8-BIT WONDER.TTF"), 100).render("".join(self._input_text), True, (255, 255, 255))
        cursor_rect = pygame.Rect(self._input_box_rect.x + self._cursor_pos * 100, self._input_box_rect.y + 5, 2, 100)
        pygame.draw.rect(input_text_surface, (255, 255, 255), cursor_rect)
        screen.blit(input_text_surface, (self._input_box_rect.x + 5, self._input_box_rect.y + 5))

class GameOverState:
    TIMER_EVENT = pygame.USEREVENT + 7  # Create a new event type

    def __init__(self, score, color_matrix, btc_price, counter, initials="XXX"):
        self.gameover_count = 100
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
            elif event.type == self.TIMER_EVENT:
                self.gameover_count -= 1
                if self.gameover_count <= 0:
                    return StartMenuState()

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

    def prepare_and_display_qr(self):
        # Fetch the QR code if it hasn't been fetched already
        if not hasattr(self, 'imgQR'):
            svg_url = "https://legend.lnbits.com/withdraw/img/{}".format(self.withdraw_id)
            svg_string = requests.get(svg_url).content
            with io.BytesIO(svg_string) as f:
                parsed_image = pygame.image.load(f, 'RGBA')
            converted_image = parsed_image.convert_alpha()
            pygame.image.save(converted_image, 'QR.png')
            self.imgQR = pygame.image.load('QR.png')

        shift_qr_vert = 130
        white_square = pygame.Rect(self.SCREEN_WIDTH/2 - self.imgQR.get_width()/2, self.SCREEN_HEIGHT/2 - self.imgQR.get_height()/2 + shift_qr_vert, 195, 195)
        pygame.draw.rect(screen, (255, 255, 255), white_square)
        screen.blit(self.imgQR, (self.SCREEN_WIDTH/2 - self.imgQR.get_width()/2, self.SCREEN_HEIGHT/2 - self.imgQR.get_height()/2 + shift_qr_vert))

    def update(self, url, write_key_header):
        if self.gameover and not self.ran_once:
            self.make_api_call(url, write_key_header)  # Make the API call
            self.log_player()
            # Change flag to ensure API call only runs once
            self.ran_once = True

    def render(self):
        # 1. Clear the screen
        screen.fill((0, 0, 0))
    
        # 2. Game Over and Play Again
        render_text('Game Over', 80, (255, 215, 0), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 220, '8-bit', True)
        render_text('Scan QR Code with lightning wallet to collect Winnings', 30, (255, 255, 255), SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 'gill sans', True)
        render_text(f"Credits: {credits}", 15, (255, 255, 255), SCREEN_WIDTH//2, 30, 'gill sans')

        # 3. Display score
        render_text('Your Score ' + str(self.score), 40, (255, 255, 255), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 150, '8-bit', True)

        # 4. Display QR Code and instructions
        if self.withdraw_id is not None:
            render_text('Hold Yellow to play Again', 25, (255, 215, 0), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 35, 'gill sans', True)
            render_text('Your ID ' + str(self.withdraw_id), 30, (255, 255, 255), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100, 'gill sans', True)
            self.prepare_and_display_qr()

        # 5. Display error message
        render_text('visit legend.lnbits.com to create a wallet. IF ERROR OCCURS SEND GAME ID to Twitter/Email support.', 20, (255, 255, 255), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 280, 'gill sans')

        # Update the screen
        pygame.display.update()

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