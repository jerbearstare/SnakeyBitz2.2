import pygame
import time
import requests
import json
import datetime
import numpy as np
import random
import io
import os
import csv



# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600

# Game mechanics
stdDeviations = [10, 5, 1, .5, 0.1, 0.01, 0.005, 0.001, 0.0005, 0.0001]
scaler = 6500

# LNbitz API Initialization
url = "https://legend.lnbits.com/withdraw/api/v1/links"
API_KEY_write = '4f185c43df804edbb0ab8cbad4973566'
method_get = "get"
write_key_header = {"X-Api-Key": API_KEY_write}

# Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.mouse.set_visible(False)
pygame.display.set_caption('SnakeyBitz')
clock = pygame.time.Clock()

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
font_score.set_bold(False)

# Initial variables
scaler = 6500 #tweek the game mechanics player over house based upon sats per quarter.
counter = 0
running = True
highest_score = 0
credits = 0 
history_file = 'history.txt'

#function for calling BTC price
def get_bitcoin_price_in_cad():
    bitcoin_api_url = "https://api.coingecko.com/api/v3/simple/price"
    parameters = {
        "ids": "bitcoin",
        "vs_currencies": "cad"
    }

    response = requests.get(bitcoin_api_url, params=parameters)
    response_json = response.json()
    btc_price = response_json["bitcoin"]["cad"]
    return btc_price

# All your class declarations...

class StartMenuState:
    def __init__(self):
        self.history_file = 'history.txt'
        self.score_values = []
        self.initials = ""
        self.highest_score = 0
        self.header = font_header.render('SnakeyBitz', True, (255, 215, 0))
        self.subheader = font_subheader.render('Insert dirty fiat to win BTC', True, (255, 255, 255), pygame.BLEND_RGB_ADD)
        self.highscore_header = font_highscore.render('', True, (255, 215, 0))
        self.process_history_file()

    def handle_events(self, events):
        global credits
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and credits > 0:
                btc_price = get_bitcoin_price_in_cad()
                return GameLoopState(self.highest_score, btc_price)
        return self

    def update(self):
        pass

    def process_history_file(self):
        with open(self.history_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                score = int(row[2])
                initials = row[15]
                
                if score > self.highest_score:
                    self.highest_score = score
                    self.initials = initials.strip()

    def render(self):
        screen.fill((0, 0, 0))  # Clear the screen
        # Render screen

        credit_text = font_inst.render(f"Credits: {credits}", True, (255, 255, 255))
        screen.blit(credit_text, (SCREEN_WIDTH//2 - credit_text.get_width()//2, 10))

        if self.initials:
            highscore_text = 'HIGHSCORE         ' + self.initials + ' . ' + str(self.highest_score) + ' SATS'
            highscore_header = font_highscore.render(highscore_text, True, (255, 215, 0))
            screen.blit(highscore_header, (SCREEN_WIDTH/2 - highscore_header.get_width()/2, SCREEN_HEIGHT/2 - highscore_header.get_height()/2 + 60))
            
        screen.blit(self.header, (SCREEN_WIDTH/2 - self.header.get_width()/2, SCREEN_HEIGHT/2 - self.header.get_height()/2 - 50))
        screen.blit(self.subheader, (SCREEN_WIDTH/2 - self.subheader.get_width()/2, SCREEN_HEIGHT/2 - self.subheader.get_height()/2 + 20))
        
        pygame.display.update()
        pygame.time.delay(500)
        
        self.subheader = font_subheader.render('Insert dirty fiat to win BTC', True, (200, 200, 200), pygame.BLEND_RGB_ADD)
        screen.blit(self.subheader, (SCREEN_WIDTH/2 - self.subheader.get_width()/2, SCREEN_HEIGHT/2 - self.subheader.get_height()/2 + 20))
        
        pygame.display.update()
        pygame.time.delay(500)
        
        self.subheader = font_subheader.render('Insert dirty fiat to win BTC', True, (255, 255, 255), pygame.BLEND_RGB_ADD)
        screen.blit(self.subheader, (SCREEN_WIDTH/2 - self.subheader.get_width()/2, SCREEN_HEIGHT/2 - self.subheader.get_height()/2 + 20))

        pygame.display.update()

class GameLoopState:
    def draw_snake(self, snake_list, snake_size):
        for xy in snake_list:
            pygame.draw.rect(screen, self.GREEN, (xy[0], xy[1], snake_size, snake_size))

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


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.x_change = -self.snake_size
                    self.y_change = 0
                elif event.key == pygame.K_RIGHT:
                    self.x_change = self.snake_size
                    self.y_change = 0
                elif event.key == pygame.K_UP:
                    self.y_change = -self.snake_size
                    self.x_change = 0
                elif event.key == pygame.K_DOWN:
                    self.y_change = self.snake_size
                    self.x_change = 0
        return self

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
        self.btc_price = btc_price
        self.counter = counter
        self.FONT_SIZE = 100
        self.score = score
        self.color_matrix = color_matrix
        self.font = pygame.font.Font(os.path.join("font", "8-BIT WONDER.TTF"), self.FONT_SIZE)
        self.font.set_bold(True)
        self.MAX_CHARS = 3
        self.input_box_rect = pygame.Rect(SCREEN_WIDTH // 2 - self.FONT_SIZE * self.MAX_CHARS // 2 + 0, (SCREEN_HEIGHT+100) // 2 - self.FONT_SIZE // 2, self.FONT_SIZE * self.MAX_CHARS, self.FONT_SIZE)
        self.input_text = ["A", "A", "A"]
        self.cursor_pos = 0
        self.letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # Highscore and Instructions Header
        self.font_high_score_text = pygame.font.Font('font/8-BIT WONDER.TTF', self.FONT_SIZE)
        self.font_high_score_text.set_bold(True)
        self.high_score_text = self.font_high_score_text.render('HIGH SCORE', True, (255, 215, 0))
        self.font_white_button_text1 = pygame.font.SysFont('gill sans', 15)
        self.font_white_button_text1.set_bold(False)
        self.white_button_text_display1 = self.font_white_button_text1.render('press white button to continue', True, (255, 255, 255))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    name = "".join(self.input_text)
                    # Save the high score and exit
                    with open(history_file, 'a') as file:
                        file.write(f"{datetime.datetime.now()},{name},{self.score}\n")
                    return GameOverState(self.score, self.color_matrix, self.btc_price, self.counter)
                elif event.key == pygame.K_LEFT:
                    # Move the cursor to the left
                    self.cursor_pos = max(0, self.cursor_pos - 1)
                    time.sleep(.2)
                elif event.key == pygame.K_RIGHT:
                    # Move the cursor to the right
                    self.cursor_pos = min(self.MAX_CHARS - 1, self.cursor_pos + 1)
                    time.sleep(.2)
                elif event.key == pygame.K_UP:
                    # Move to the previous letter
                    index = self.letters.find(self.input_text[self.cursor_pos])
                    index = (index - 1) % len(self.letters)
                    self.input_text[self.cursor_pos] = self.letters[index]
                    time.sleep(.1)
                elif event.key == pygame.K_DOWN:
                    # Move to the next letter
                    index = self.letters.find(self.input_text[self.cursor_pos])
                    index = (index + 1) % len(self.letters)
                    self.input_text[self.cursor_pos] = self.letters[index]
                    time.sleep(.1)
        return self


    def update(self):
        return self


    def render(self):
        screen.fill((0, 0, 0))
        input_text_surface = self.font.render("".join(self.input_text), True, (255, 255, 255))
        cursor_rect = pygame.Rect(self.input_box_rect.x + self.cursor_pos * self.FONT_SIZE, self.input_box_rect.y + 5, 2, self.FONT_SIZE)
        pygame.draw.rect(input_text_surface, (255, 255, 255), cursor_rect)

        # Rendering High Score Header
        screen.blit(self.high_score_text, (SCREEN_WIDTH/2 - self.high_score_text.get_width()/2, SCREEN_HEIGHT/2 - self.high_score_text.get_height()/2-220))

        # Rendering Instructions
        screen.blit(self.white_button_text_display1, (SCREEN_WIDTH/2 - self.white_button_text_display1.get_width()/2, SCREEN_HEIGHT/2 - self.white_button_text_display1.get_height()/2+280))

        screen.blit(input_text_surface, (self.input_box_rect.x + 5, self.input_box_rect.y + 5))

        pygame.display.update()

class GameOverState:
    TIMER_EVENT = pygame.USEREVENT + 1  # Create a new event type


    def __init__(self, score, color_matrix, btc_price, counter):
        self.gameover_count = 50
        self.score = score
        self.btc_price = btc_price
        self.color_matrix = color_matrix
        self.gameover = True
        self.ran_once = False
        self.counter = counter  # If 'counter' is necessary in your code
        self.btc_price = btc_price  # Replace with actual btc_price value
        self.SCREEN_WIDTH = SCREEN_WIDTH  # Reference to the constant
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.withdraw_id = None
        self.speed = 6

        pygame.time.set_timer(self.TIMER_EVENT, 1000)  # Start a timer that fires every second

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                # Handle quit event here
                pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # If Enter is pressed, return to the Start Menu state
                    return StartMenuState()  # Assuming you have a class called StartMenuState
                elif event.key == pygame.K_SPACE:
                    # If Space is pressed, reduce the counter by 5
                    self.gameover_count -= 5
                    if self.gameover_count  <= 0:
                        # If counter reaches zero, return to the Start Menu state
                        return StartMenuState()  # Assuming you have a class called StartMenuState
            elif event.type == self.TIMER_EVENT:  # Add a handler for the timer event
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
        with open('history.txt', 'a') as open_history: 
            open_history.write(f"{self.counter}, {self.withdraw_id}, {self.score}, {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, ${self.btc_price}, {self.color_matrix}, XXX\n")
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
        clock.tick(self.speed)
 
def run_game():
    global running, credits
    current_state = StartMenuState()

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    credits += 1

        next_state = current_state.handle_events(events)
        if next_state is None:
            break
        else:
            current_state = next_state

        if isinstance(current_state, GameOverState):
            update_state = current_state.update(url, write_key_header)  
        else:
            update_state = current_state.update()

        if update_state is not None:
            current_state = update_state

        current_state.render()

        pygame.display.update()

run_game()