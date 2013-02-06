import random, smtplib, sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email_settings import MANDRILL_USERNAME, MANDRILL_PASSWORD, FROM_EMAIL

class DraftLottery:
    teams = {}
    balls = []
    order = []
    output = ""

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
        self.print_and_append("Lottery balls: " + str(self.balls))

    def runlottery(self):
        """ Runs the lottery and outputs each pick
        """
        self.order = []
        for i in range(1, len(self.teams)+1):
            self.print_and_append("-----------------------------")
            self.print_and_append("Remaining balls: " + str(self.balls))
            self.pullball(i)
        self.print_and_append("-----------------------------")
        self.print_and_append("Lottery is done!  Results:")
        for i, team in enumerate(self.order):
            self.print_and_append("Pick " + str(i+1) + ": " + team)

    def pullball(self, num_pick):
        """ Pulls random ball and removes all other balls of that team
        """
        lower = 0
        upper = len(self.balls)-1
        self.print_and_append("Drawing pick " + str(num_pick) + ", random number between " + str(lower) + " and " + str(upper)  + "...")
        selection = random.randint(lower, upper)
        self.print_and_append("Selected: " + str(selection))
        selected_team = self.balls[selection]
        self.order.append(selected_team)
        selected_team_num_balls = len(filter(lambda a: a == selected_team, self.balls))
        self.print_and_append("Pick " + str(num_pick)  +" is: " + selected_team + ", with " + str(selected_team_num_balls) + "/" + str(len(self.balls)) + " balls")
        self.print_and_append("Removing " + selected_team + "'s balls")
        self.balls = filter(lambda a: a != selected_team, self.balls)

    def print_and_append(self, text):
        print text
        self.output += "<div>" + text + "</div>"

    def email(self, recipients):
        #from http://help.mandrill.com/entries/21746308-Sending-via-SMTP-in-various-programming-languages
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Draft lottery results"
        msg['From'] = FROM_EMAIL
        body = MIMEText(self.output, 'html')
        username = MANDRILL_USERNAME
        password = MANDRILL_PASSWORD
        msg.attach(body)
        s = smtplib.SMTP('smtp.mandrillapp.com', 587)
        s.login(username, password)

        for recipient in recipients:
            msg['To'] = str(recipient)
            s.sendmail(msg['From'], msg['To'], msg.as_string())
        s.quit()

if __name__ == "__main__":
    args = sys.argv
    args.pop(0)
    draft = DraftLottery()
    recipients = []
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
                    draft.addteam(name=parameters[0], num_balls=int(parameters[2]))
                    recipients.append(parameters[1])
        draft.seedlottery()
        draft.runlottery()
        if recipients:
            draft.email(recipients=recipients)
