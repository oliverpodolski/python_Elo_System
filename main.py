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
        print("5 - Ranklist")

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
        if choice == 2:
            db.remove_player(input("Enter the id of the player:\n"))
            print("Player was removed")
        if choice == 3:
            print(db.get_players())
        if choice == 4:
            winner_id = input("Enter the player ID of the winner")
            loser_id = input("Enter the player ID of the loser")

            winner = db.get_player(winner_id)
            loser = db.get_player(loser_id)

            elo_change = elo.calculate(winner["elo"], loser["elo"])

            db.update_elo(winner["elo"] + elo_change, winner_id)
            db.update_elo(loser["elo"] - elo_change, loser_id)

            db.create_match(winner["id"], loser["id"], elo_change)
            print(f"Match was created! The elo change is: {elo_change}")


start_menu()