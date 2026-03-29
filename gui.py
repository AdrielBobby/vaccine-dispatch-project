from db.setup import initialize_db
from ui.app import App
import os
from dotenv import load_dotenv

def main():
    # Load env and initialize DB
    load_dotenv()
    initialize_db()
    
    # Launch GUI
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
