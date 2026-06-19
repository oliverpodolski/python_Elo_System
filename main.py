from database.db import DatabaseManager

db = DatabaseManager()

db.create_database()
db.create_table_players()
db.create_table_matches()

def start_menu():
    while True:
        print("1 - Add Player")
        print("2 - Remove Player")
        print("3 - Add Match")
        print("4 - Ranklist")

        try:
            choice = int(input("\nWhat would you like to do?\n"))
        except ValueError:
            print("Please enter a valid Number!")

        if choice == 1:
            pass
        if choice == 2:
            pass
        if choice == 3:
            pass
        if choice == 4:
            pass