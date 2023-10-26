import numpy as np 
import numpy as np 
import time 
import requests
import json
import random

#Game Paramaters
games = 1000
min_foods = 10
max_foods = 100

#get the price of bitcoin in Canadian Dollars
bitcoin_api_url = "https://api.coingecko.com/api/v3/simple/price"
parameters = {
    "ids": "bitcoin",
    "vs_currencies": "cad"
}

response = requests.get(bitcoin_api_url, params=parameters)
response_json = response.json()
btc_price = response_json["bitcoin"]["cad"]
#btc_price = 100000

#Creating a scoring modifier depeding on the price of bitcoin for once Canadain Quarter
price_modifier = float(btc_price)/8000
sats_per_quarter = round(0.25/(float(btc_price)/100000000))

# Create an array for 10 colors
colors = np.array(['red', 'blue', 'green', 'yellow', 'orange', 'black', 'gray', 'purple', 'brown', 'gold'])

scores = np.zeros(games) #Create a matrix to store the scores, the scores all start at zero

total_score=0 #Starting score for each game
game_no = 1 #starting the count of games

color_matrix = np.zeros((10,games)) #Create a matrix to store the number of times each color is chosen

# Create a loop to choose colors randomly from colors array and assign a point to each color
for i in range(games): #N GAMES
    stdDeviations = [10, 5, 1, .5, 0.1, 0.01, 0.005, 0.001, 0.0005, 0.0003]
    score = 0
    for i in range(random.randint(min_foods,max_foods)): #ONE GAME
        i = 0
        chosen_color = np.random.choice(colors, p=stdDeviations/np.sum(stdDeviations)) #
        if chosen_color == 'red':
            points = round(10/float(price_modifier))
        elif chosen_color == 'blue': 
            points = round(50/float(price_modifier))
        elif chosen_color == 'green': 
            points = round(100/float(price_modifier))
        elif chosen_color == 'yellow': 
            points = round(250/float(price_modifier))
        elif chosen_color == 'orange': 
            points = round(500/float(price_modifier))
        elif chosen_color == 'black': 
            points = round(1000/float(price_modifier))
        elif chosen_color == 'gray': 
            points = round(25000/float(price_modifier))
        elif chosen_color == 'purple': 
            points = round(50000/float(price_modifier))
        elif chosen_color == 'brown': 
            points = round(75000/float(price_modifier))
        elif chosen_color == 'gold': 
            points = round(10000/float(price_modifier))

        #print(chosen_color + str(points)) #print out colors chosen for each game
        #time.sleep(.001)
        score = points + score # loop for chosing colors
        
        # update the matrix with the count of each color
        color_index = np.where(colors == chosen_color)[0][0]
        color_matrix[color_index, game_no-1]+=1


    print("Game " + str(game_no) + " Score: %d" %(score)) # Print out a summary of each game.

    # add each score to the scores matrix
    scores[game_no-1] = score
    
    total_score = total_score + score
    game_no += 1

# #print out the color matrix game by game for each color
# print("Color Matrix:")
# for i in range(len(colors)):
#     print(colors[i], color_matrix[i,:])


# create summing series for each color
red_sum = np.sum(color_matrix[0,:])
blue_sum = np.sum(color_matrix[1,:])
green_sum = np.sum(color_matrix[2,:])
yellow_sum = np.sum(color_matrix[3,:])
orange_sum = np.sum(color_matrix[4,:])
black_sum = np.sum(color_matrix[5,:])
gray_sum = np.sum(color_matrix[6,:])
purple_sum = np.sum(color_matrix[7,:])
brown_sum = np.sum(color_matrix[8,:])
gold_sum = np.sum(color_matrix[9,:])

# Create a matrix to store the sium of each color
#rows = 10 colors, columns = 1
color_sum_matrix = np.array([[red_sum], [blue_sum], [green_sum], [yellow_sum], [orange_sum], [black_sum], [gray_sum], [purple_sum], [brown_sum], [gold_sum]])

# print out the color matrix for the sum of each color
print("Sum Matrix:")
for i in range(len(colors)):
    print(colors[i], color_sum_matrix[i,:])

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
