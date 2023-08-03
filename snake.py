### imports
import pygame
import time
import requests
import json
import datetime
import numpy as np
import io
import Serial
import cairosvg 

#Joystick and button initialization
from joymap import *

#### GAME MECHANICS #####
stdDeviations = [10, 5, 1, .5, 0.1, 0.01, 0.005, 0.001, 0.0005, 0.0001]
scaler = 6500

### COIN READER ###
if __name__ == '__main__':
    Serial_channel = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    Serial_channel.flush()

startmenu = True
gameloop = False
gameover = False



#### LNbitz API INITIALATION #####
url = "https://legend.lnbits.com/withdraw/api/v1/links"
API_KEY_write = '4f185c43df804edbb0ab8cbad4973566' #write key for creating, updating and>
method_get = "get"
write_key_header = {"X-Api-Key": API_KEY_write}

##### PYGAME INITIALZATION #######
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.mouse.set_visible(False) #disable to mouse
running = True

# Set the title of the window
pygame.display.set_caption('SnakeyBitz')

# starting variables

# Fonts
pygame.font.init()
font_header = pygame.font.Font('font/8-BIT WONDER.TTF', 80, bold=True)
font_subheader = pygame.font.Font('font/8-BIT WONDER.TTF', 30, bold=True)
font_highscore = pygame.font.Font('font/8-BIT WONDER.TTF', 20, bold=True)

while running:
    # threading
    previousBank = 0.00
    from joymap import *
    coin = False
    # thread function 
    if Serial_channel.in_waiting > 0:
                b = Serial_channel.readline()
                raw =  b.decode() # convert to string
                ardBank =  raw.rstrip('utf-8')# strip away excess characters
                print(ardBank)
                if float(ardBank) > previousBank: #coin has been inserted
                    coin = True

    if coin == True:  ### this will be the event that triggers when a coin is inserted
        gameloop = True
        startmenu = False
        gameover = False
        counter = 0

        # Calls the price of Bitcoin and sets the price of the foods
        bitcoin_api_url = "https://api.newton.co/dashboard/api/rates/"
        response = requests.get(bitcoin_api_url)
        response_json = response.json()
        btc_price = response_json['rates'][48]['spot'] #['FOLDER']['LINENUMBER']['FILTER']
        price_modifier = float(btc_price)/scaler

        
    if startmenu == True:

        history_file = 'history.txt' 
        score_values = []
        with open(history_file) as file:
            for line in file:
                history_fields = line.split(',')
                file_score_float = float(history_fields[2].strip())
                file_score_str = str(file_score_float)
                new_score_float = float(file_score_str[:-2])

                score_values.append(new_score_float)
        highest_score = max(score_values)

        # Render screen
        screen.fill((0, 0, 0))

        #HEADER NAME
        header = font_header.render('SnakeyBitz', True, (255, 215, 0))
        subheader = font_subheader.render('Insert dirty fiat to win BTC', True, (255, 255, 255), pygame.BLEND_RGB_ADD)
        highscore_header = font_highscore.render('HIGHSCORE   ' + str(int(highest_score)) + ' SATS', True, (255, 215, 0))
        screen.blit(header, (SCREEN_WIDTH/2 - header.get_width()/2, SCREEN_HEIGHT/2 - header.get_height()/2 - 50))
        screen.blit(highscore_header, (SCREEN_WIDTH/2 - highscore_header.get_width()/2, SCREEN_HEIGHT/2 - highscore_header.get_height()/2 + 60))

        # Quarters only
        font_label = pygame.font.SysFont('gill sans', 20, bold=True)
        quarters_only_label = font_label.render('QUARTERS ONLY. Insert only one at a time, not during gameplay. No "Credits"', True, (255, 255, 255))
        screen.blit(quarters_only_label, (SCREEN_WIDTH/2 - quarters_only_label.get_width()/2, SCREEN_HEIGHT/2 - quarters_only_label.get_height()/2+275))

        #Flash insert coin
        screen.blit(subheader, (SCREEN_WIDTH/2 - subheader.get_width()/2, SCREEN_HEIGHT/2 - subheader.get_height()/2 + 20))
        pygame.display.update()
        pygame.time.delay(500)
        subheader = font_subheader.render('Insert dirty fiat to win BTC', True, (200, 200, 200), pygame.BLEND_RGB_ADD)
        screen.blit(subheader, (SCREEN_WIDTH/2 - subheader.get_width()/2, SCREEN_HEIGHT/2 - subheader.get_height()/2 + 20))
        pygame.display.update()
        pygame.time.delay(500)
        subheader = font_subheader.render('Insert dirty fiat to win BTC', True, (255, 255, 255), pygame.BLEND_RGB_ADD)
        screen.blit(subheader, (SCREEN_WIDTH/2 - subheader.get_width()/2, SCREEN_HEIGHT/2 - subheader.get_height()/2 + 20))
        pygame.display.update()
        

    if gameloop==True:
        # new game of snake with multiple colors of food
        import random
        import time
        from joymap import *

        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        GREEN = (0, 255, 0)
        YELLOW = (255, 255, 0)
        ORANGE = (255, 165, 0)
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        CYAN = (0, 255, 255)
        PURPLE = (128, 0, 128)
        BROWN = (165, 42, 42)
        GOLD = (255, 215, 0)

        pygame.init()
        score = 50

        # Set the title of the window
        pygame.display.set_caption('SnakeyBitz')

        # List to hold all the sprites 
        all_sprites_list = pygame.sprite.Group()

        # Variables for snake position
        x_position = 300
        y_position = 300
        x_change = 0
        y_change = 0
        snake_size = 10
        snake_list = []
        snake_length = 1

        # Variables for food position
        food_x = round(random.randrange(0, SCREEN_WIDTH - snake_size) / snake_size) * 10
        food_y = round(random.randrange(0, SCREEN_HEIGHT - snake_size) / snake_size) * 10

        #define color distribution
        colors = np.array(['RED', 'BLUE', 'GREEN', 'YELLOW', 'ORANGE', 'WHITE', 'CYAN', 'PURPLE', 'BROWN', 'GOLD'])
        color_matrix = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        chosen_color = np.random.choice(colors, p=stdDeviations/np.sum(stdDeviations)) #choose the color

        # Initial speed of the snake
        speed = 15

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        def draw_snake(snake_list, snake_size):
            for xy in snake_list:
                pygame.draw.rect(screen,  GREEN, (xy[0], xy[1], snake_size, snake_size)) 

        # Set up the loop to run at a certain speed
        game = True


        while game == True:     
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                # Movement of the snake          
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = -snake_size
                        y_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x_change = snake_size
                        y_change = 0
                    elif event.key == pygame.K_UP:
                        y_change = -snake_size
                        x_change = 0
                    elif event.key == pygame.K_DOWN:
                        y_change = snake_size
                        x_change = 0 # move snake loop
            # Set the window background
            screen.fill(BLACK)

            # Move the snake
            x_position += x_change
            y_position += y_change

            # Snake is eaten food
            if x_position == food_x and y_position == food_y: #food eaten loop
                if chosen_color == 'RED':
                    points = round(10/float(price_modifier))
                    color_matrix[0] += 1
                elif chosen_color == 'BLUE': 
                    points = round(25/float(price_modifier))
                    color_matrix[1] += 1
                elif chosen_color == 'GREEN': 
                    points = round(50/float(price_modifier))
                    color_matrix[2] += 1
                elif chosen_color == 'YELLOW': 
                    points = round(100/float(price_modifier))
                    color_matrix[3] += 1
                elif chosen_color == 'ORANGE': 
                    points = round(250/float(price_modifier))
                    color_matrix[4] += 1
                elif chosen_color == 'WHITE': 
                    points = round(500/float(price_modifier))
                    color_matrix[5] += 1
                elif chosen_color == 'CYAN': 
                    points = round(1000/float(price_modifier))
                    color_matrix[6] += 1
                elif chosen_color == 'PURPLE': 
                    points = round(50000/float(price_modifier))
                    color_matrix[7] += 1
                elif chosen_color == 'BROWN': 
                    points = round(75000/float(price_modifier))
                    color_matrix[8] += 1
                elif chosen_color == 'GOLD': 
                    points = round(10000/float(price_modifier))
                    color_matrix[9] += 1
                food_x = round(random.randrange(0, SCREEN_WIDTH - snake_size) / 10.0) * 10.0
                food_y = round(random.randrange(0, SCREEN_HEIGHT - snake_size) / 10.0) * 10.0
                snake_length += 1
                chosen_color = np.random.choice(colors, p=stdDeviations/np.sum(stdDeviations)) #choose the color
                score = points + score
                counter += 1
                
            draw_snake(snake_list, snake_size)

            # Draw food
            pygame.draw.rect(screen, chosen_color, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(x_position)
            head.append(y_position)
            snake_list.append(head)
            
            if len(snake_list) > snake_length:
                del snake_list[0]
                
            # Collision of the snake
            if x_position > SCREEN_WIDTH or x_position <0:
                game = False
                gameloop = False
                gameover = True


            elif y_position > SCREEN_HEIGHT or y_position < 0:
                game = False
                gameloop = False
                gameover = True
                
            elif head in snake_list[:-1]:
                game = False
                gameloop = False
                gameover = True

            # Score
            font = pygame.font.SysFont('gill sans', 30)
            text = font.render("Score " + str(score), True, (255, 255, 255))
            screen.blit(text, (10, 10))
        
            pygame.display.update()
            ran_once = False
            # Update game after certain time
            clock.tick(speed)

    if gameover == True and not ran_once:
        for i in range(1):  
            gameover_counter = 300
            # Create API payload
            create_payload = {
                "title": "Thanks",
                "min_withdrawable": score,
                "max_withdrawable": score,
                "uses": 1,
                "wait_time": 1,
                "is_unique": "true"}
            
            # API Call
            create_response = requests.post(url, headers=write_key_header, json=create_payload )

            # Isolate withdrawal ID
            json_data = create_response.json()
            withdraw_id = json_data['id']
            print(withdraw_id)
            ### HISTORY FILE ####
            open_history = open('history.txt', 'a')   # 'w' stands for write mode 
            open_history.write("\n"+ str(counter) + ', ' + withdraw_id + ', ' + str(score) + ', ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ', $' + str(btc_price) + ', ' + str(color_matrix))
            # 
            open_history.close()
            # Change flag to ensure API call only runs once
            ran_once = True
            i+=1 
            break #lnbit payload, run only once.

        while gameover_counter > 0:
            for event in pygame.event.get():     # Event handler for the buttons queing actions
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameover_counter = 0
                        #game_over = False
                        #startmenu = True# loop that changes menu/game/gameoverloops #event handler that choses what menu the game is on. 

            if Serial_channel.in_waiting > 0:
                b = Serial_channel.readline()
                raw =  b.decode() # convert to string
                ardBank =  raw.rstrip('utf-8')# strip away excess characters
                print(ardBank)
                if float(ardBank) > previousBank: #coin has been inserted
                    gameover_counter = 0
                    coin = True # Listen for coin
                    

            if coin == True:  ### this will be the event that triggers when a coin is inserted
                gameloop = True
                startmenu = False
                gameover = False
                        
            #Render BLACK SCREEN
            screen.fill((0, 0, 0))

            #GET SVG IMAGE FROM LNBITS
            svg_url = "https://legend.lnbits.com/withdraw/img/{}".format(withdraw_id)
            svg_string = requests.get(svg_url).content
            
            # Filter SVG and convert to PNG
            filtered_svg_string = str(svg_string)[42:-3]
            #print(filtered_svg_string)
            with open('QR.svg', 'w') as f:
                f.write(filtered_svg_string)
            SVG_FILENAME = 'QR.svg'
            PNG_FILENAME = 'QR.png'
            cairosvg.svg2png(url=SVG_FILENAME, write_to=PNG_FILENAME)

            # Display QR code
            shift_qr_vert = 130

            imgQR = pygame.image.load('QR.png')
            white_square = pygame.Rect(SCREEN_WIDTH/2 - imgQR.get_width()/2, SCREEN_HEIGHT/2 - imgQR.get_height()/2 + shift_qr_vert, 195,195) #white square
            pygame.draw.rect(screen, (255, 255, 255), white_square)
            screen.blit(imgQR, (SCREEN_WIDTH/2 - imgQR.get_width()/2, SCREEN_HEIGHT/2 - imgQR.get_height()/2 + shift_qr_vert))

            # Display Game Over
            pygame.font.init()
            font_game_over = pygame.font.Font('font/8-BIT WONDER.TTF', 80, bold=True)
            game_over = font_game_over.render('Game Over', True, (255, 215, 0))
            screen.blit(game_over, (SCREEN_WIDTH/2 - game_over.get_width()/2, SCREEN_HEIGHT/2 - game_over.get_height()/2-220))
                
            # Display Score
            font_score = pygame.font.Font('font/8-BIT WONDER.TTF', 40, bold=True)
            score_display = font_score.render('Your Score ' + str(score), True, (255, 255, 255))
            screen.blit(score_display, (SCREEN_WIDTH/2 - score_display.get_width()/2, SCREEN_HEIGHT/2 - score_display.get_height()/2-150))

            #Display Play Again
            font_play_again = pygame.font.SysFont('gill sans', 30, bold=True)
            play_again_display = font_play_again.render('Insert Coin to Play Again or White Button for Menu ', True, (255, 255, 255))
            screen.blit(play_again_display, (SCREEN_WIDTH/2 - play_again_display.get_width()/2, SCREEN_HEIGHT/2 - play_again_display.get_height()/2-0))

            # Display GAME ID
            font_id = pygame.font.SysFont('gill sans', 20, bold=True)
            id_display = font_id.render('Your Game ID ' + withdraw_id, True, (255, 255, 255))
            screen.blit(id_display, (SCREEN_WIDTH/2 - id_display.get_width()/2, SCREEN_HEIGHT/2 - id_display.get_height()/2+250))

            # Display Countdown
            gameover_count_font = pygame.font.SysFont('gill sans', 35, bold=True)
            gameover_count = gameover_count_font.render(str(gameover_counter), True, (255, 255, 255))
            screen.blit(gameover_count, (SCREEN_WIDTH/2 - gameover_count.get_width()/2 + 450, SCREEN_HEIGHT/2 - gameover_count.get_height()/2-270))

            # Display instructions
            font_inst = pygame.font.SysFont('gill sans', 30, bold=True)
            font_inst1 = pygame.font.SysFont('gill sans', 15, bold=False)
            inst_display = font_inst.render('Scan QR code with lightning wallet to collect winnings', True, (255, 215, 0))
            inst_display1 = font_inst1.render('payment rails in development: use Muun(for security) legend.lnbits.com(quick and easy) wallets; if error occurs, provide Game ID to Twitter/Email support.', True, (255, 255, 255))
            screen.blit(inst_display, (SCREEN_WIDTH/2 - inst_display.get_width()/2, SCREEN_HEIGHT/2 - inst_display.get_height()/2-40))
            screen.blit(inst_display1, (SCREEN_WIDTH/2 - inst_display1.get_width()/2, SCREEN_HEIGHT/2 - inst_display1.get_height()/2+280))

            pygame.display.update()
            time.sleep(0.2)
            gameover_counter -= 1

            if gameover_counter == 0:
                gameover = False
                startmenu = True


        clock.tick(speed) #game over loop

#close Serial channel
Serial_channel.close() 

#close Pygame
pygame.quit()

