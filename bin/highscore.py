history_file = 'history.txt' # replace with the name of your file
score_values = []

with open(history_file) as file:
    for line in file:
        history_fields = line.split(',')
        file_score_value = float(history_fields[2].strip())
        score_values.append(file_score_value)

highest_value = max(score_values)
print(highest_value)


