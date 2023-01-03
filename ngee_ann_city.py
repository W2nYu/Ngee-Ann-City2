#Import needed packages
import random
from flask import Flask, render_template, request

#Functio(s) for score
def score(grid, pool_List):
  scoreR = 0
  scoreI = 0
  scoreC = 0
  scoreO = 0
  scoreRd = 0

  for building in pool_List:
  
    if building == 'I':
      scoreI= 1
      
      for row in range(len(grid)):
        for col in range(len(grid[row])):    
          if grid[row][col] == 'R':
            coins += 1
            
    elif building == 'R':
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

    elif building == 'C':
      for rows in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == 'C':
                scoreC += 1
            elif grid[row][col] == 'R':
                coins += 1

    elif building == '*':
        for score in scoreRd:
            if score != 0:
                for i in range(score):
                    scoreRd += score
                    
    elif building == 'O':
        for rows in range(len(grid)):
            for col in range(len(grid)):
                if grid[row][col] == 'O':
                    scoreO += 1

  totalScore = scoreR + scoreI + scoreC + scoreO + scoreRd
  
  return totalScore

#Functions(s) to build a building in game
def build_building(grid, build_choice, turns, option):
  x_axis = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 'x', 't', ]
  y_axis = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

  #Standardise input by lower casing it
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
          if grid[row][col] == '   ':
            grid[row][col] = build_choice
            turns+=1
          else:
            print('Square is unavailable!')
        else:
          print("You must build next to an existing building!")
    else:
      print("The input is not within the grid.")
  else:
    print("The plot input is invalid format :)")
    
def increase_turns(turns):
  turns+=1

def rand_pool(pool_list):  
  while True:
    randInt = random.randint(0,4)
    randDraw = [pool_list[randInt], randInt]
    return randDraw

#Variable setting
grid_size = 20
grid = [[" " for col in range(grid_size)]for row in range(grid_size)]
building_list_symbols = [' R ', ' I ', ' C ', ' O ', ' * ']
building_list = ['Residential', 'Industry', 'Commercial', 'Park', 'Road']
turns = 0
coins = 16
totalScore = 0

#Various web pages
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
  #totalScore = score(grid, building_list_symbols)
  if request.method == "POST":
    plot = request.form["Plt"]
    choice = request.form["C"]
    if choice == "1":
      build_building(grid, choice1[0], turns, plot)
      increase_turns(turns)
    elif choice == "2":
      build_building(grid, choice2[0], turns, plot)
      increase_turns(turns)
    return render_template("start_game.html", gridz = grid, c1 = choice1_building, c2 = choice2_building, cn = coins, tn = turns, totscore = totalScore)
  else:
    return render_template("start_game.html", gridz = grid, c1 = choice1_building, c2 = choice2_building, cn = coins, tn = turns, totScore = totalScore)
    
@app.route("/exit_game")
def exit_game():
  return render_template("exit_game.html")

#Main program
if __name__ == '__main__':
  app.run()