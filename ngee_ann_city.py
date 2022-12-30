#Import needed packages
import random
import time
from flask import Flask, render_template, request

#Funtions for the games

#Score function
#Note: This is the base code that I placed
#Just make sure all the different types of buildings are accounted for
#in scoring and change the output below to return instead of print
#So thet the returned value can be outputted to the front end
#If u cannot finish by 1-2 am, I will resolve it by tmr when I wake up
#Before the sprint review
def score(grid, poolList):
  scoreBCH = 0
  scoreFAC = 0
  scoreHSE = 0
  scoreHWY = 0
  scoreSHP = 0
  scoreMON = 0
  
  for building in poolList:
    if building[0] == 'HSE':
      # HSE Scoring
      print('HSE:', end = ' ')
      firstrun = 0
      scoreHSE = 0
      
      for row in range(len(grid)):
        for col in range(len(grid[row])):
          if grid[row][col] == 'HSE':
            indiv_scoreHSE = 0
            adjBuildings = []
            if row != 0:
              adjBuildings.append(grid[row-1][col])
            if row != 3:
              adjBuildings.append(grid[row+1][col])
            if col != 0:
              adjBuildings.append(grid[row][col-1])
            if col != 3:
              adjBuildings.append(grid[row][col+1])

            if 'FAC' in adjBuildings:
              scoreHSE = 1
              if firstrun == 0:
                print('1', end = ' ')
                firstrun = 1
              else:
                print('+ 1', end = ' ')
            else:
              for building in adjBuildings:
                if building == 'HSE' or building == 'SHP':
                  indiv_scoreHSE += 1
                elif building == 'BCH':
                  indiv_scoreHSE += 2
            
              scoreHSE += indiv_scoreHSE
              if firstrun == 0:
                print('{}'.format(indiv_scoreHSE), end = ' ')
                firstrun = 1
              else:
                print('+ {}'.format(indiv_scoreHSE), end = ' ')
                  
      if scoreHSE == 0:
        print('0')
      else:
        print('= {}'.format(scoreHSE)) # show total
    
    elif building[0] == 'FAC':
      # FAC Scoring
      print('FAC:', end = ' ')
      # check how many factories are there
      countFAC = 0
      scoreFAC = 0
      for row in grid:
        for col in row:
          if col == 'FAC':
            countFAC += 1
      
      if countFAC < 5:
        firstrun = 0
        for i in range(countFAC):
          scoreFAC += countFAC
          if firstrun == 0:
            print('{}'.format(countFAC), end = ' ')
            firstrun = 1
          else:
            print('+ {}'.format(countFAC), end = ' ')
      
      elif countFAC > 4:
        firstrun = 0
        for i in range(4):
          scoreFAC += 4
          if firstrun == 0:
            print('{}'.format(4), end = ' ')
            firstrun = 1
          else:
            print('+ {}'.format(4), end = ' ')
        
        remaining = countFAC - 4
        for i in range(remaining):
          print('+ {}'.format(1), end = ' ')
          scoreFAC += 1

      if scoreFAC == 0:
        print('0')
      else:
        print('= {}'.format(scoreFAC)) # show total
    
    elif building[0] == 'SHP':
      #SHP Scoring
      print('SHP:', end = ' ')
      scoreSHP = 0
      firstrun = 0
      for row in range(len(grid)):
        for col in range(len(grid[row])):
          
          # for 1 SHP
          if grid[row][col] == 'SHP':
            unique_adjList = [] # adjacent list
            indivScore = 0
            check_adj = []

            if row != 0:
              check_adj.append(grid[row-1][col])
            if row != 3:
              check_adj.append(grid[row+1][col])
            if col != 0:
              check_adj.append(grid[row][col-1])
            if col != 3:
              check_adj.append(grid[row][col+1])

            for building in check_adj:
              if building not in unique_adjList:
                unique_adjList.append(building)

            indivScore = len(unique_adjList)
            if firstrun == 0:
              print('{}'.format(indivScore), end = ' ')
              firstrun = 1
            else:
              print('+ {}'.format(indivScore), end = ' ')

            scoreSHP += indivScore

      if scoreSHP == 0:
        print('0')
      else:
        print('= {}'.format(scoreSHP)) # show total
    
    elif building[0] == 'HWY':
      #HWY Scoring
      scoreHWYList = []
      for row in grid:
        countHWY = 0
        for x in row:
          if x == 'HWY':
            countHWY += 1
          else:
            if countHWY != 0:
              scoreHWYList.append(countHWY)
            countHWY = 0
        if countHWY != 0:
          scoreHWYList.append(countHWY)
      
      firstrun = 0
      scoreHWY = 0
      print('HWY:', end = ' ')
      for score in scoreHWYList:
        scoreHWY += score ** 2
        for i in range(score):
          if firstrun == 0:
            print('{}'.format(score), end = ' ')
            firstrun = 1
          else:
            print('+ {}'.format(score), end = ' ')

      if scoreHWY == 0:
        print('0')
      else:
        print('= {}'.format(scoreHWY)) # show total

    elif building[0] == 'BCH':
      # BCH Scoring
      print('BCH:', end = ' ')
      scoreBCH = 0
      firstrun = 0
      for row in range(len(grid)):
        for col in range(len(grid[row])):
          # BCH scoring
          if grid[row][col] == 'BCH':
            if col == 0 or col == 3:
              scoreBCH += 3
              if firstrun == 0:
                print('3', end = ' ')
                firstrun = 1
              else:
                print('+ 3', end = ' ')
            else:
              scoreBCH += 1
              if firstrun == 0:
                print('1', end = ' ')
                firstrun = 1
              else:
                print('+ 1', end = ' ')

      if scoreBCH == 0:
        print('0')
      else:
        print('= {}'.format(scoreBCH)) # show total
  
    elif building[0] == 'MON':
      # MON Scoring
      print('MON:', end = ' ')
      scoreMON = 0
      firstrun = 0
      checkMONlist = []

      checkMONlist.append(grid[0][0])
      checkMONlist.append(grid[3][0])
      checkMONlist.append(grid[0][3])
      checkMONlist.append(grid[3][3])

      if checkMONlist.count('MON') >= 3:
        for row in range(len(grid)):
          for col in range(len(grid[row])):
            if grid[row][col] == 'MON':
              scoreMON += 4
              if firstrun == 0:
                print('4', end = ' ')
                firstrun = 1
              else:
                print('+ 4', end = ' ')
      else:
        for row in range(len(grid)):
          for col in range(len(grid[row])):
            if grid[row][col] == 'MON':
              if row == 0 or row == 3 or col == 0 or col == 3:
                scoreMON += 2
                if firstrun == 0:
                  print('2', end = ' ')
                  firstrun = 1
                else:
                  print('+ 2', end = ' ')
              else:
                scoreMON += 1
                if firstrun == 0:
                  print('1', end = ' ')
                  firstrun = 1
                else:
                  print('+ 1', end = ' ')

      if scoreMON == 0:
        print('0')
      else:
        print('= {}'.format(scoreMON)) # show total  



  totalScore = scoreBCH + scoreFAC + scoreHSE + scoreHWY + scoreSHP + scoreMON
  print('Total score:', totalScore)
  print()

  return totalScore

#Functions(s) to build a building in game
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

#Variable for building choice

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
   if request.method == "POST":
      plot = request.form["Plt"]
      choice = request.form["C"]
      if choice == "1":
         build_building(grid, choice1[0], turns, plot)
      elif choice == "2":
         build_building(grid, choice2[0], turns, plot)
      return render_template("start_game.html", gridz = grid, c1 = choice1_building, c2 = choice2_building, cn = coins, tn = turns)
   else:

      return render_template("start_game.html", gridz = grid, c1 = choice1_building, c2 = choice2_building, cn = coins, tn = turns)
    
@app.route("/exit_game")
def exit_game():
   return render_template("exit_game.html")

#Main program
if __name__ == '__main__':
   app.run()