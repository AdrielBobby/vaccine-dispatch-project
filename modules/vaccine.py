ADMIN_CODE = "BIOpharmAdMiN"

def add_vaccine(conn):
    """Admin-only: add a new vaccine to the database."""
    code = input("Enter Admin Code: ").strip()
    if code != ADMIN_CODE:
        print("[!] Wrong Admin Key — Entry Denied.")
        return

    while True:
        try:
            v_id  = int(input("Vaccine ID (4-digit): ").strip())
            name  = input("Vaccine Name: ").strip()
            mfr   = input("Manufacturer: ").strip()
            cost  = int(input("Production Cost per vial: ").strip())
            price = int(input("Selling Price per vial: ").strip())
        except ValueError:
            print("[!] Invalid input — please enter numbers where required.")
            continue

        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO AD_Vaccine (V_ID, V_Name, Manufacturer, Cost, Price) "
                "VALUES (%s, %s, %s, %s, %s)",
                (v_id, name, mfr, cost, price)
            )
            conn.commit()
            print(f"[✓] Vaccine '{name}' added successfully.")
        except Exception as e:
            print(f"[ERROR] {e}")
        finally:
            cur.close()

        if input("Add another vaccine? (Y/N): ").strip().upper() != "Y":
            break