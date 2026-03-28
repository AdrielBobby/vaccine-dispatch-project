import mysql.connector as mycon
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    """Create and return a MySQL connection using .env credentials."""
    try:
        conn = mycon.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            passwd=os.getenv("DB_PASSWORD", ""),
        )
        return conn
    except mycon.Error as e:
        print(f"[ERROR] Could not connect to MySQL: {e}")
        raise SystemExit(1)