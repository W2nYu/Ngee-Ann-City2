# Import needed packages
import random
from flask import Flask, render_template, request
import sqlite3

#Function for the database connection
def get_db_connection():
    conn = sqlite3.connect('ngeeanncity.db')
    conn.row_factory = sqlite3.Row
    return conn

# Functions(s) to build a building in game
def build_building(grid, build_choice, turns, option):
  x_axis = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 'x', 't', ]
  y_axis = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

  option = option.lower()
  if len(option) == 2 and option[1].isnumeric():
    x = option[0]
    y = int(option[1])
    if x in x_axis and y in y_axis: #Validate if input option within the grid
      col = x_axis.index(x)
      row = y_axis.index(y)

      if turns == 0:
        grid[row][col] = build_choice #Build choice is string value
        turns+=1

      #If a build has already been built in the grid
      elif turns > 0:
        #Find if new plot that is gonna be built is connected (adjacent)
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
          if grid[row][col] == " ":
            grid[row][col] = build_choice
            turns+=1
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
    return [randInt, randDraw]


# Variable setting
grid_size = 20
grid = [[" " for col in range(grid_size)]for row in range(grid_size)]
building_list_symbols = [' R ', ' I ', ' C ', ' O ', ' * ']
building_list = ['Residential', 'Industry', 'Commercial', 'Park', 'Road']
turns = 0
coins = 16
totalScore = 0

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
    return render_template("start_game.html", gridz = grid, c1 = choice1_building, c2 = choice2_building, cn = coins, tn = turns, totscore = totalScore)
  else:
    return render_template("start_game.html", gridz = grid, c1 = choice1_building, c2 = choice2_building, cn = coins, tn = turns, totscore = totalScore)
    
@app.route("/exit_game")
def exit_game():
  return render_template("exit_game.html")

# Main programs
if __name__ == '__main__':
  app.run()

   