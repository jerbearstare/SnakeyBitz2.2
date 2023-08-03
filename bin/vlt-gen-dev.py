#newcode
import numpy as np 
import time 
import requests
import json
import random

#margin = 0.9 #ensures to take 10% when calculating modifer.
games = 100
game_no = 1
min_foods = 10
max_foods = 100


bitcoin_api_url = "https://api.newton.co/dashboard/api/rates/"
response = requests.get(bitcoin_api_url)
response_json = response.json()
btc_price = response_json['rates'][48]['spot'] #['FOLDER']['LINENUMBER']['FILTER']
#btc_price = 100000
price_modifier = float(btc_price)/9000
sats_per_quarter = round(0.25/(float(btc_price)/100000000))
# Create an array for 10 colors
colors = np.array(['red', 'blue', 'green', 'yellow', 'orange', 'black', 'gray', 'purple', 'brown', 'gold'])

#Create a matrix to store the scores
scores = np.zeros(games)

total_score=0

#Create a matrix to store the number of times each color is chosen
#rows = 10 colors, columns = games
color_matrix = np.zeros((10,games))

# Create a loop to choose colors randomly from colors array and assign a point to each color
for i in range(games): #N GAMES

    #Create a loop to count the number of times each color is chosen per game
    for i in range(games):
        num_red = 0
        num_blue = 0
        num_green = 0 
        num_yellow = 0
        num_orange = 0
        num_black = 0
        num_gray = 0
        num_purple = 0
        num_brown = 0
        num_gold = 0

    stdDeviations = [10, 4, 3, 2, 1, 0.1, 0.01, 0.001, 0.0001, 0.00001]
    score = 0
    color_matrix = np.zeros((1,10))
    for i in range(random.randint(min_foods,max_foods)): #ONE GAME
        i = 0
        chosen_color = np.random.choice(colors, p=stdDeviations/np.sum(stdDeviations)) 
        if chosen_color == 'red':
            points = round(10/float(price_modifier))
            color_matrix[0][0] += 1
        elif chosen_color == 'blue': 
            points = round(25/float(price_modifier))
            color_matrix[0][1] += 1
        elif chosen_color == 'green': 
            points = round(50/float(price_modifier))
            color_matrix[0][2] += 1
        elif chosen_color == 'yellow': 
            points = round(100/float(price_modifier))
            color_matrix[0][3] += 1
        elif chosen_color == 'orange': 
            points = round(250/float(price_modifier))
            color_matrix[0][4] += 1
        elif chosen_color == 'black': 
            points = round(500/float(price_modifier))
            color_matrix[0][5] += 1
        elif chosen_color == 'gray': 
            points = round(1000/float(price_modifier))
            color_matrix[0][6] += 1
        elif chosen_color == 'purple': 
            points = round(50000/float(price_modifier))
            color_matrix[0][7] += 1
        elif chosen_color == 'brown': 
            points = round(75000/float(price_modifier))
            color_matrix[0][8] += 1
        elif chosen_color == 'gold': 
            points = round(10000/float(price_modifier))
            color_matrix[0][9] += 1

        print(chosen_color + str(points)) #print out colors chosen for each game
        #time.sleep(.001)
        score = points + score # loop for chosing colors

    print("Game " + str(game_no) + " Score: %d" %(score) + ", Color Matrix: " + str(color_matrix)) # Print out a summary of each game.

    # add each score to the scores matrix
    scores[game_no-1] = score
    
    total_score = total_score + score
    game_no += 1

# Print out the top five highest scores 
print("Top five highest scores:")
top_5_highest_scores = np.sort(scores)[-5:]
for i in range(len(top_5_highest_scores)):
    print("Game score: ", top_5_highest_scores[i])

# calculate and print out the average score
average_score = total_score/games
print('Average score = ' + str(average_score))

print('sats per quarter: ' + str(sats_per_quarter))

margin = float(sats_per_quarter)/float(average_score)

print(str(margin))