def record_dispatch(conn):
    """Record a dispatched vaccine order."""
    cur = conn.cursor()
    cur.execute("SELECT O_ID, vaccine_ID, QTY, Hospital, State FROM AD_Order")
    orders = cur.fetchall()
    cur.close()

    if not orders:
        print("[!] No pending orders found.")
        return

    print("\n{:<8} {:<8} {:<8} {:<30} {:<20}".format(
        "O_ID", "V_ID", "QTY", "Hospital", "State"))
    print("-" * 76)
    for o in orders:
        print("{:<8} {:<8} {:<8} {:<30} {:<20}".format(*o))
    print()

    while True:
        try:
            ord_id  = int(input("Order ID to dispatch: ").strip())
            vac_id  = int(input("Vaccine ID: ").strip())
            qty     = int(input("Quantity dispatched: ").strip())
            hosp    = input("Hospital: ").strip()
            state   = input("State: ").strip()
            date    = input("Date of Dispatch (YYYY-MM-DD): ").strip()
        except ValueError:
            print("[!] Invalid input.")
            continue

        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO Dispatch (Order_ID, Vaccine_ID, QTY, Hospital, State, date_Dispatch) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (ord_id, vac_id, qty, hosp, state, date)
            )
            conn.commit()
            print(f"[✓] Dispatch for Order #{ord_id} recorded.")
        except Exception as e:
            print(f"[ERROR] {e}")
        finally:
            cur.close()

        if input("Record another dispatch? (Y/N): ").strip().upper() != "Y":
            break


# --- GUI HELPERS ---

def record_dispatch_direct(conn, ord_id, vac_id, qty, hosp, state, date):
    """GUI helper: record a dispatch directly with parameters."""
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Dispatch (Order_ID, Vaccine_ID, QTY, Hospital, State, date_Dispatch) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (ord_id, vac_id, qty, hosp, state, date)
        )
        conn.commit()
        return True, f"Dispatch for Order #{ord_id} recorded."
    except Exception as e:
        return False, str(e)
    finally:
        cur.close()


def update_dispatch_direct(conn, ord_id, vac_id, qty, hosp, state, date):
    """GUI helper: update an existing dispatch record."""
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE Dispatch 
            SET Vaccine_ID = %s, QTY = %s, Hospital = %s, State = %s, date_Dispatch = %s 
            WHERE Order_ID = %s
        """, (vac_id, qty, hosp, state, date, ord_id))
        conn.commit()
        return True, "Dispatch record updated successfully."
    except Exception as e:
        return False, str(e)
    finally:
        cur.close()


def get_dispatch_status_report(conn):
    """GUI helper: fetch all orders with dispatch status."""
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT o.O_ID, v.V_Name, o.QTY, o.Hospital, o.State, o.vaccine_ID,
              CASE WHEN d.Order_ID IS NOT NULL THEN 'Dispatched' ELSE 'Pending' END AS Status
            FROM AD_Order o
            JOIN AD_Vaccine v ON o.vaccine_ID = v.V_ID
            LEFT JOIN Dispatch d ON o.O_ID = d.Order_ID
        """)
        return cur.fetchall()
    except Exception:
        return []
    finally:
        cur.close()


def update_dispatch_direct(conn, ord_id, vac_id, qty, hosp, state, date):
    """GUI helper: update an existing dispatch record."""
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE Dispatch 
            SET Vaccine_ID = %s, QTY = %s, Hospital = %s, State = %s, date_Dispatch = %s 
            WHERE Order_ID = %s
        """, (vac_id, qty, hosp, state, date, ord_id))
        conn.commit()
        return True, "Dispatch record updated successfully."
    except Exception as e:
        return False, str(e)
    finally:
        cur.close()
