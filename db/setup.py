from db.connection import get_connection
from dotenv import load_dotenv
import os

load_dotenv()
DB_NAME = os.getenv("DB_NAME", "VaccineDispatch")

def initialize_db():
    """Create the database and all tables if they don't already exist."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cur.execute(f"USE {DB_NAME}")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS AD_Vaccine (
            V_ID         INT          NOT NULL,
            V_Name       VARCHAR(50),
            Manufacturer VARCHAR(100),
            Cost         INT,
            Price        INT,
            PRIMARY KEY (V_ID)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS AD_Order (
            O_ID       INT          NOT NULL,
            vaccine_ID INT,
            QTY        INT,
            Hospital   VARCHAR(100),
            State      VARCHAR(70),
            PRIMARY KEY (O_ID),
            FOREIGN KEY (vaccine_ID) REFERENCES AD_Vaccine(V_ID)
        );
    """)

    # Create index if it does not exist
    cur.execute("""
        SELECT COUNT(1) FROM information_schema.statistics
        WHERE table_schema = DATABASE()
          AND table_name = 'AD_Order'
          AND index_name = 'hospital_idx';
    """)
    if cur.fetchone()[0] == 0:
        cur.execute("CREATE INDEX hospital_idx ON AD_Order (Hospital);")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Dispatch (
            Order_ID      INT          NOT NULL,
            Vaccine_ID    INT,
            QTY           INT,
            Hospital      VARCHAR(100),
            State         VARCHAR(70),
            date_Dispatch DATE,
            PRIMARY KEY (Order_ID),
            FOREIGN KEY (Order_ID)   REFERENCES AD_Order(O_ID),
            FOREIGN KEY (Vaccine_ID) REFERENCES AD_Vaccine(V_ID)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("[✓] Database and tables initialized successfully.")
    return True