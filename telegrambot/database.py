import pyodbc

DB_CONFIG = {
    "server": "DESKTOP-QQAOEK4",
    "database": "GameDB",
    "username": "",  
    "password": "",  
}

def get_db_connection():
    """Підключення до бази даних MSSQL Server"""
    try:
        conn_str = (f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={DB_CONFIG['server']};"
                    f"DATABASE={DB_CONFIG['database']};"
                    "Trusted_Connection=yes;"
                    "Encrypt=yes;"
                    "TrustServerCertificate=yes;")
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print(f"Помилка під час підключення до бази даних: {e}")
        return None

def get_all_players():
    """Отримання рейтингу всіх гравців"""
    try:
        conn = get_db_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        cursor.execute("SELECT name, level, points, playtime FROM player_progress ORDER BY points DESC")
        players = cursor.fetchall()
        conn.close()
        

        print(f"Отримано {len(players)} гравців з бази даних.")
        
        if not players:
            print("⚠️ Рейтинг поки що порожній.")
        else:
            for player in players:
                print(f"Гравець: {player[0]}, Рівень: {player[1]}, Очки: {player[2]}, Час: {player[3]}")

        return players
    except Exception as e:
        print(f"Помилка під час отримання рейтингу: {e}")
        return []

def get_player(username):
    """Отримання інформації про конкретного гравця"""
    try:
        conn = get_db_connection()
        if not conn:
            return None

        cursor = conn.cursor()
        cursor.execute("SELECT name, level, points, playtime FROM player_progress WHERE name = ?", (username,))
        player = cursor.fetchone()
        conn.close()
        
        if player:
            print(f"Інформація про гравця {username}:")
            print(f"Рівень: {player[1]}, Очки: {player[2]}, Час: {player[3]}")
        
        return player
    except Exception as e:
        print(f"Помилка під час отримання даних гравця: {e}")
        return None
