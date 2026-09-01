from db.setup import initialize_db
from ui.app import App
import os
import sys
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")

def main():
    # Load env and initialize DB
    load_dotenv()
    initialize_db()
    
    # Launch GUI
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
