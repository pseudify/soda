import sqlite3

class Database:
    def __init__(self, db_name="bot_database.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS server_greet_channel (
            server_id INTEGER PRIMARY KEY,
            channel_id INTEGER
        )
        """)
        self.conn.commit()

    def get_greet_channel(self, server_id):
        self.cursor.execute("SELECT channel_id FROM server_greet_channel WHERE server_id = ?", (server_id,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def set_greet_channel(self, server_id, channel_id):
        self.cursor.execute("INSERT OR REPLACE INTO server_greet_channel (server_id, channel_id) VALUES (?, ?)",
                            (server_id, channel_id))
        self.conn.commit()
