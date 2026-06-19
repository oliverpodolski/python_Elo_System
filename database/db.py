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