from enum import nonmember

from database.db import DatabaseManager
from elo import EloCalculator

db = DatabaseManager()
elo = EloCalculator()

db.create_database()
db.create_table_players()
db.create_table_matches()

def start_menu():
    while True:
        print("1 - Add Player")
        print("2 - Remove Player")
        print("3 - Show Player List")
        print("4 - Add Match")
        print("5 - Leaderboard")
        print("6 - Match History")

        try:
            choice = int(input("\nWhat would you like to do?\n"))
        except ValueError:
            print("Please enter a valid Number!")

        if choice == 1:
            player = input("Enter the name of the new player:\n")
            if not player.isalpha():
                print("The name can only contain letters!")
            else:
                db.create_player(player)
                print("Player was created")
        elif choice == 2:
            try:
                player_remove = int(input("Enter the id of the player:\n"))
            except ValueError:
                print("Please enter a valid number!")
            db.remove_player(player_remove)
            print("Player was removed")
        elif choice == 3:
            player_playerlist = db.get_players()
            for i in player_playerlist:
                print(f"ID: {i[0]} | Name: {i[1]} | Elo: {i[2]}")
            print("\n")
        elif choice == 4:
            winner_id = input("Enter the player ID of the winner\n")
            loser_id = input("Enter the player ID of the loser\n")

            winner = db.get_player(winner_id)
            loser = db.get_player(loser_id)

            elo_change = elo.calculate(winner["elo"], loser["elo"])

            db.update_elo(winner["elo"] + elo_change, winner_id)
            db.update_elo(loser["elo"] - elo_change, loser_id)

            db.create_match(winner["id"], loser["id"], elo_change)
            print(f"Match was created! The elo change is: {elo_change}\n")
        elif choice == 5:
            player_leaderboard = db.get_leaderboard()

            for p in player_leaderboard:
                print(f"ID: {p[0]} | Name: {p[1]} | Elo: {p[2]}")
            print("\n")
        elif choice == 6:
            try:
                player_match_history = int(input("Enter the id of the player:\n"))
            except ValueError:
                print("Please enter a valid number!")
            player_matches = db.get_matches(player_match_history)
            if not player_matches:
                print("This player does not exists or haven´t played a match!")
            else:
                matches = len(player_matches)
                for m in player_matches:
                    player_winner = db.get_player(m[1])
                    player_loser = db.get_player(m[2])
                    print(f"Match #{matches}")
                    print(f"{player_winner["name"]} defeated {player_loser["name"]} (+/-{m[3]})")
                    print(f"{m[4]}\n")
                    matches -= 1
start_menu()