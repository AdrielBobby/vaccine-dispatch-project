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