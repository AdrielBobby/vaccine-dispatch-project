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


# --- GUI HELPERS ---

def add_vaccine_direct(conn, v_id, name, mfr, cost, price):
    """GUI helper: add a vaccine directly with parameters."""
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO AD_Vaccine (V_ID, V_Name, Manufacturer, Cost, Price) "
            "VALUES (%s, %s, %s, %s, %s)",
            (v_id, name, mfr, cost, price)
        )
        conn.commit()
        return True, f"Vaccine '{name}' added successfully."
    except Exception as e:
        return False, str(e)
    finally:
        cur.close()


def update_vaccine_direct(conn, v_id, name, mfr, cost, price):
    """GUI helper: update an existing vaccine."""
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE AD_Vaccine 
            SET V_Name = %s, Manufacturer = %s, Cost = %s, Price = %s 
            WHERE V_ID = %s
        """, (name, mfr, cost, price, v_id))
        conn.commit()
        return True, "Vaccine updated successfully."
    except Exception as e:
        return False, str(e)
    finally:
        cur.close()


def delete_vaccine_direct(conn, v_id):
    """GUI helper: delete a vaccine by ID."""
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM AD_Vaccine WHERE V_ID = %s", (v_id,))
        conn.commit()
        return True, "Vaccine removed successfully."
    except Exception as e:
        return False, str(e)
    finally:
        cur.close()


def update_vaccine_direct(conn, v_id, name, mfr, cost, price):
    """GUI helper: update an existing vaccine."""
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE AD_Vaccine 
            SET V_Name = %s, Manufacturer = %s, Cost = %s, Price = %s 
            WHERE V_ID = %s
        """, (name, mfr, cost, price, v_id))
        conn.commit()
        return True, "Vaccine updated successfully."
    except Exception as e:
        return False, str(e)
    finally:
        cur.close()


def get_all_vaccines(conn):
    """GUI helper: fetch all vaccines as a list of dicts."""
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM AD_Vaccine")
        return cur.fetchall()
    except Exception:
        return []
    finally:
        cur.close()


def update_vaccine_direct(conn, v_id, name, mfr, cost, price):
    """GUI helper: update an existing vaccine."""
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE AD_Vaccine 
            SET V_Name = %s, Manufacturer = %s, Cost = %s, Price = %s 
            WHERE V_ID = %s
        """, (name, mfr, cost, price, v_id))
        conn.commit()
        return True, "Vaccine updated successfully."
    except Exception as e:
        return False, str(e)
    finally:
        cur.close()


def delete_vaccine_direct(conn, v_id):
    """GUI helper: delete a vaccine by ID."""
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM AD_Vaccine WHERE V_ID = %s", (v_id,))
        conn.commit()
        return True, "Vaccine removed successfully."
    except Exception as e:
        return False, str(e)
    finally:
        cur.close()


def update_vaccine_direct(conn, v_id, name, mfr, cost, price):
    """GUI helper: update an existing vaccine."""
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE AD_Vaccine 
            SET V_Name = %s, Manufacturer = %s, Cost = %s, Price = %s 
            WHERE V_ID = %s
        """, (name, mfr, cost, price, v_id))
        conn.commit()
        return True, "Vaccine updated successfully."
    except Exception as e:
        return False, str(e)
    finally:
        cur.close()
