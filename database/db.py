import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:

    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv("host"),
            user = os.getenv("user"),
            password = os.getenv("password")
        )

        self.cursor = self.connection.cursor()

    def create_database(self):
        self.cursor.execute(
            "CREATE DATABASE IF NOT EXISTS elo_system"
        )

        self.cursor.execute("USE elo_system")
        print("Database was created")

    def create_table_players(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS players (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                elo INT NOT NULL
            );
            """
        )

    def create_table_matches(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS matches (
                id INT AUTO_INCREMENT PRIMARY KEY,
                winnerID INT NOT NULL,
                loserID INT NOT NULL,
                elo_change INT NOT NULL,
                entry_added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

    def create_player(self, player_name):
        self.cursor.execute(
            """
            INSERT INTO players (name, elo)
            VALUES (%s, %s)
            """,(player_name, 1000)
        )
        self.connection.commit()

    def remove_player(self, player_id):
        self.cursor.execute(
            """
            DELETE FROM players
            WHERE id = %s
            """, (player_id,)
        )

        self.connection.commit()

    def get_players(self):
        self.cursor.execute(
            """
            SELECT * FROM players
            """
        )
        return self.cursor.fetchall()

    def get_player(self, player_id):
        self.cursor.execute(
            """
            SELECT * FROM players
            WHERE id = %s
            """,(player_id,)
        )
        player = self.cursor.fetchone()
        if player is None:
            return None
        return {
            "id": player[0],
            "name": player[1],
            "elo": player[2]
        }

    def create_match(self, winnerID, loserID, elo_change):
        self.cursor.execute(
            """
            INSERT INTO matches (winnerID, loserID, elo_change)
            VALUES (%s, %s, %s)
            """, (winnerID, loserID, elo_change)
        )
        self.connection.commit()

    def update_elo(self, new_elo, player_id):
        self.cursor.execute(
            """
            UPDATE players
            SET elo = %s
            WHERE id = %s
            """,(new_elo, player_id)
        )
        self.connection.commit()

    def get_leaderboard(self):
        self.cursor.execute(
            """
            SELECT * FROM players
            ORDER BY elo DESC
            LIMIT 10
            """
        )
        return self.cursor.fetchall()

    def get_matches(self, player_id):
        self.cursor.execute(
            """
            SELECT * FROM matches
            WHERE winnerID = %s OR loserID = %s
            ORDER BY entry_added_at DESC
            """, (player_id, player_id)
        )
        return self.cursor.fetchall()

    def get_stats_wins(self, player_id):
        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM matches
            WHERE winnerID = %s
            """, (player_id,)
        )
        return self.cursor.fetchone()[0]

    def get_stats_losses(self, player_id):
        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM matches
            WHERE loserID = %s
            """, (player_id,)
        )
        return self.cursor.fetchone()[0]