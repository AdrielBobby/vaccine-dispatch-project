"""
Vaccine Dispatch System
=======================
Entry point. Run with:  python main.py
"""

from dotenv import load_dotenv
import os

from db.setup import initialize_db
from db.connection import get_connection
from modules.vaccine import add_vaccine
from modules.order import place_order
from modules.dispatch import record_dispatch
from modules.reports import sales_report, pending_report, dispatch_graph

load_dotenv()
DB_NAME = os.getenv("DB_NAME", "VaccineDispatch")


def get_db_connection():
    conn = get_connection()
    conn.cursor().execute(f"USE {DB_NAME}")
    return conn


MENU = """
╔══════════════════════════════════════════════════════╗
║     BIOPHARM — VACCINE DISPATCH MANAGEMENT SYSTEM    ║
╠══════════════════════════════════════════════════════╣
║  1. Add New Vaccine          (Admin only)            ║
║  2. Place a New Order                                ║
║  3. Record Vaccine Dispatch                          ║
║  4. View Sales Report                                ║
║  5. View Pending Dispatch Report                     ║
║  6. Show Dispatch Graph                              ║
║  7. Exit                                             ║
╚══════════════════════════════════════════════════════╝
"""

ACTIONS = {
    1: add_vaccine,
    2: place_order,
    3: record_dispatch,
    4: sales_report,
    5: pending_report,
    6: dispatch_graph,
}


def main():
    initialize_db()
    conn = get_db_connection()

    while True:
        print(MENU)
        try:
            choice = int(input("Enter your choice: ").strip())
        except ValueError:
            print("[!] Please enter a number between 1 and 7.")
            continue

        if choice == 7:
            print("\nExiting Vaccine Dispatch System. Have a nice day!")
            conn.close()
            break
        elif choice in ACTIONS:
            ACTIONS[choice](conn)
        else:
            print("[!] Invalid choice. Please try again.")


if __name__ == "__main__":
    main()