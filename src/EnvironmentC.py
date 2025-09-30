import random


class EnvironmentC:
    


    # Constructor.
    
    def __init__(self, width=4, height=4, allowClimbWithoutGold=False, pitProb=0.2):

        self.width = width
        self.height = height
        self.allowClimbWithoutGold = allowClimbWithoutGold
        self.pitProb = pitProb

        self.coordinates =  [['X' for x in range(1, self.width)] for y in range(1, self.height)] 

        # Create an occupied_list array.

        occupied_list = []

        # Initialize the Agent.

        self.agent = (1, 1) 
        occupied_list.append(self.agent)

        # Initialize the location of the Wumpus.
        self.wumpus = self.get_random_coordinate(occupied_list)
        occupied_list.append(self.wumpus)

        self.gold = self.get_random_coordinate(occupied_list)
        occupied_list.append(self.gold)

        self.pit = []

        self.pit = self.determine_pit_locations(occupied_list)


#        for i in range(1, 4):
#            print (i)
#            pit_loc = self.get_random_coordinate(occupied_list)
#            self.pit.append(pit_loc)
#            self.pit[i] = self.get_random_coordinate(occupied_list)
#            occupied_list.append(pit_loc)

        print (self.coordinates)

        print ("Agent", self.agent)
        print ("Wumpus", self.wumpus)
        print ("Gold", self.gold)
        print ("Pit", self.pit)


    def display_board(self):

        print("displaying board")

        for i in range(1, self.height+1):

            for j in range(1, self.width+1):

                if ((i, j) == self.agent):
                    print ('A', ' ', end='')
                elif ((i, j) == self.wumpus):
                    print ('W', ' ', end='')
                elif ((i, j) == self.gold):
                    print ('G', ' ', end='')
                elif ((i, j) in self.pit):
                    print ('P', ' ', end='')
                else:
                    print ('X', ' ', end='')

            print()

    def get_random_coordinate(self, occupied_list):

        while True:
            random_row = random.randint(1, 4)
            random_col = random.randint(1, 4)

            if ((random_col, random_row) not in occupied_list):
                break

        return (random_col, random_row)


    def determine_pit_locations(self, occupied_list):

        pit_list = []
        pit_or_nopit = [ 'P', 'X' ]
        pit_probabilities = [0.2, 0.8]

        for i in range(1, self.height+1):

            for j in range(1, self.width+1):

                if ((i, j) not in occupied_list):

                    pit = random.choices(pit_or_nopit, weights=pit_probabilities, k=1)[0]

                    if (pit == 'P'):
                        pit_list.append((i, j))
    #                    print('Pit', pit)

        return pit_list