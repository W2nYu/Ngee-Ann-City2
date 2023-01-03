# Import needed packages
import random
import time
from flask import Flask, render_template, request
import sqlite3


def get_db_connection():
    conn = sqlite3.connect('ngeeanncity.db')
    conn.row_factory = sqlite3.Row
    return conn

# Funtions for the games
# Score function
# Note: This is the base code that I placed
# Just make sure all the different types of buildings are accounted for
# in scoring and change the output below to return instead of print
# So thet the returned value can be outputted to the front end
# If u cannot finish by 1-2 am, I will resolve it by tmr when I wake up
# Before the sprint review


def score(grid, pool_List):
    scoreR = 0
    scoreI = 0
    scoreC = 0
    scoreO = 0
    scoreRd = 0

    for building in pool_List:

        if building[0] == 'I':
            scoreI = 1

            for row in range(len(grid)):
                for col in range(len(grid[row])):
                    if grid[row][col] == 'R':
                        coins += 1

        elif building[0] == 'R':
            for row in grid:
                for x in row:
                    if x == 'I':
                        scoreR += 1

            for row in range(len(grid)):
                for col in range(len(grid[row])):
                    if grid[row][col] == 'R' or grid[row][col] == 'C' & grid[row][col] == 'O':
                        scoreR += 1

                    elif grid[row][col] == 'O':
                        scoreR += 2

        elif building[0] == 'C':
            for rows in range(len(grid)):
                for col in range(len(grid)):
                    if grid[row][col] == 'C':
                        scoreC += 1
                    elif grid[row][col] == 'R':
                        coins += 1

        elif building[0] == '*':
            totalRdScore = 0
            for score in scoreRd:
                if score != 0:
                    for i in range(score):
                        totalRdScore += score

        elif building[0] == 'O':
            for rows in range(len(grid)):
                for col in range(len(grid)):
                    if grid[row][col] == 'O':
                        scoreO += 1
        else:
            continue

    totalScore = scoreR + scoreI + scoreC + scoreO + totalRdScore

    return totalScore

# Functions(s) to build a building in game


def build_building(grid, build_choice, turns, option):
    x_axis = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
              'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 'x', 't', ]
    y_axis = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
              11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    option = option.lower()
    if len(option) == 2 and option[1].isnumeric():
        x = option[0]
        y = int(option[1])
        if x in x_axis and y in y_axis:  # Validate if input option within the grid
            col = x_axis.index(x)
            row = y_axis.index(y)

            if turns == 0:
                grid[row][col] = build_choice  # Build choice is string value

            # If a build has already been built in the grid
            elif turns > 0:
                # Find if new plot that is gonna be built is connected (adjacent)
                nxt_buildings = []
                if row != 0:
                    nxt_buildings.append(grid[row-1][col])
                if row != 19:
                    nxt_buildings.append(grid[row+1][col])
                if col != 0:
                    nxt_buildings.append(grid[row][col-1])
                if col != 19:
                    nxt_buildings.append(grid[row][col+1])

                count_nxt_buildings = 0
                for building in building_list:
                    count_nxt_buildings += nxt_buildings.count(building)

                if count_nxt_buildings != 0:
                    if grid[row][col] == '   ':
                        grid[row][col] = build_choice
                        print()
                    else:
                        print('Square is unavailable!')
                else:
                    print("You must build next to an existing building!")
        else:
            print("Input is not within grid, please re-enter valid plot!")
    else:
        print("Please re-enter a valid plot :)")


def rand_pool(pool_list):
    while True:
        randInt = random.randint(0, 4)
        randDraw = [pool_list[randInt], randInt]
        return randDraw


# Variable setting
grid_size = 20
grid = [[" " for col in range(grid_size)]for row in range(grid_size)]
building_list_symbols = [' R ', ' I ', ' C ', ' O ', ' * ']
building_list = ['Residential', 'Industry', 'Commercial', 'Park', 'Road']
turns = 0
coins = 16
totalScore = 0

# Variable for building choice

# Various web pages
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start_game", methods=["POST", "GET"])
def start_game():
    choice1 = rand_pool(building_list_symbols)
    choice2 = rand_pool(building_list_symbols)
    choice1_building = building_list[choice1[1]]
    choice2_building = building_list[choice2[1]]
    if request.method == "POST":
        plot = request.form["Plt"]
        choice = request.form["C"]
        if choice == "1":
            build_building(grid, choice1[0], turns, plot)
        elif choice == "2":
            build_building(grid, choice2[0], turns, plot)
        return render_template("start_game.html", gridz=grid, c1=choice1_building, c2=choice2_building, cn=coins, tn=turns)
    else:

        return render_template("start_game.html", gridz=grid, c1=choice1_building, c2=choice2_building, cn=coins, tn=turns)


@app.route("/save_game", methods=["POST"])
def save_gamePOST():
    name = "test1234"
    password = "pwdtest1234"

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO saved_games (name, password, grid, turns, coins, total_score) VALUES (?, ?, ?, ?, ?, ?)",
                (name, password, grid, turns, coins, totalScore))

    conn.commit()
    conn.close()

    return render_template("index.html")


@app.route("/save_game")
def save_game():
    return render_template("save_game.html")


@app.route("/exit_game")
def exit_game():
    return render_template("exit_game.html")


# Main program
if __name__ == '__main__':
    app.run()
