class Player:
    def __init__(self, name, team):
        self.name = name
        self.team = team
        self.xp = 5
    def introduce(self):
        print(f"Hello my name is {self.name} and I play for {self.team}")

class Team:
    def __init__(self, team_name):
        self.team_name = team_name
        self.players = []
    def add_player(self, name):
        new_player = Player(name=name, team=self.team_name)
        self.players.append(new_player)
    def remove_player(self, name):
        for player in self.players:
            if player.name == name:
                self.players.remove(player)
                break
    def show_players(self):
        for player in self.players:
            player.introduce()
    def show_xp(self):
        xp = 0
        for player in self.players:
            xp+=player.xp
        print(f"{self.team_name}'s xp is {xp}")

gorani = Player(
    name="Gorani",
    team="Team X"
)

team_X = Team("Team X")

team_X.add_player("Gorani")
team_X.add_player("Gorani2")
team_X.show_players()

team_Blue = Team("Team Blue")

team_Blue.add_player("Monkey")
team_Blue.show_players()

print("--remove Gorani2")

team_X.remove_player("Gorani2")

team_X.show_players()
team_Blue.show_players()

print("--sum of xp")

team_X.show_xp()
team_Blue.show_xp()