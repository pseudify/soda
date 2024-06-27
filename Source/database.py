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
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS infractions (
            infraction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            moderator_id INTEGER,
            reason TEXT,
            punishment_type TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS mod_roles (
            server_id INTEGER,
            role_id INTEGER,
            PRIMARY KEY (server_id, role_id)
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

    def add_infraction(self, user_id, moderator_id, reason, punishment_type):
        self.cursor.execute("""
        INSERT INTO infractions (user_id, moderator_id, reason, punishment_type)
        VALUES (?, ?, ?, ?)
        """, (user_id, moderator_id, reason, punishment_type))
        self.conn.commit()

    def get_infractions(self, user_id):
        self.cursor.execute("""
        SELECT infraction_id, moderator_id, reason, punishment_type, timestamp
        FROM infractions
        WHERE user_id = ?
        """, (user_id,))
        return self.cursor.fetchall()

    def clear_infractions(self, user_id):
        self.cursor.execute("""
        DELETE FROM infractions
        WHERE user_id = ?
        """, (user_id,))
        self.conn.commit()

    def add_mod_role(self, server_id, role_id):
        self.cursor.execute("""
        INSERT OR IGNORE INTO mod_roles (server_id, role_id)
        VALUES (?, ?)
        """, (server_id, role_id))
        self.conn.commit()

    def remove_mod_role(self, server_id, role_id):
        self.cursor.execute("""
        DELETE FROM mod_roles
        WHERE server_id = ? AND role_id = ?
        """, (server_id, role_id))
        self.conn.commit()

    def get_mod_roles(self, server_id):
        self.cursor.execute("""
        SELECT role_id FROM mod_roles
        WHERE server_id = ?
        """, (server_id,))
        return [row[0] for row in self.cursor.fetchall()]
