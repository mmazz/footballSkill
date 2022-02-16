import pandas as pd


# For make more eaven time axis
def days(day):
    if int(day)<10:
        day = '0' + day
    return day

# df has only data with the player in question
def player_skill(df, player):
    mean = []
    std = []
    time = []
    for index, row in df.iterrows():
        if (player == row['team1']):
            mean.append(row['p1_mean'])
            std.append(row['p1_std'])
            time.append(int(str(row['year'])+days(str(row['round']))))
        elif (player == row['team2']):
            mean.append(row['p2_mean'])
            std.append(row['p2_std'])
            time.append(int(str(row['year'])+days(str(row['round']))))
    return mean, std, time


