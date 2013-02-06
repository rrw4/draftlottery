import random
import sys

class DraftLottery:
    teams = {}
    balls = []
    order = []

    def addteam(self, name=None, num_balls=None):
        """ Add team and number of balls to lottery
        """
        self.teams[name] = num_balls

    def seedlottery(self):
        """ Seeds the lottery
        """
        self.balls = []
        for team, num_balls in self.teams.iteritems():
            start = len(self.balls)
            for i in range(start, start+num_balls):
                self.balls.append(team)
        print "Lottery balls: " + str(self.balls)

    def runlottery(self):
        """ Runs the lottery and outputs each pick
        """
        self.order = []
        for i in range(1, len(self.teams)+1):
            print "-----------------------------"
            print "Remaining balls: " + str(self.balls)
            self.pullball(i)
        print "-----------------------------"
        print "Lottery is done!  Results:"
        for i, team in enumerate(self.order):
            print "Pick " + str(i+1) + ": " + team

    def pullball(self, num_pick):
        """ Pulls random ball and removes all other balls of that team
        """
        lower = 0
        upper = len(self.balls)-1
        print "Drawing pick " + str(num_pick) + ", random number between " + str(lower) + " and " + str(upper)  + "..."
        selection = random.randint(lower, upper)
        print "Selected: " + str(selection)
        selected_team = self.balls[selection]
        self.order.append(selected_team)
        selected_team_num_balls = len(filter(lambda a: a == selected_team, self.balls))
        print "Pick " + str(num_pick)  +" is: " + selected_team + ", with " + str(selected_team_num_balls) + "/" + str(len(self.balls)) + " balls"
        print "Removing " + selected_team + "'s balls"
        self.balls = filter(lambda a: a != selected_team, self.balls)

if __name__ == "__main__":
    args = sys.argv
    args.pop(0)
    draft = DraftLottery()
    if len(args) == 1:
        draftfile = open(args[0], 'r')
        while True:
            line = draftfile.readline()
            if line == '':
                break
            else:
                parameters = line.strip().split()
                if len(parameters) == 2:
                    #name, number of balls
                    draft.addteam(name=parameters[0], num_balls=int(parameters[1]))
                elif len(parameters) == 3:
                    #name, email, number of balls
                    pass
        draft.seedlottery()
        draft.runlottery()
