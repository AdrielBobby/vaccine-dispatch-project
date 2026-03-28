def list_vaccines(conn):
    cur = conn.cursor()
    cur.execute("SELECT V_ID, V_Name, Manufacturer, Price FROM AD_Vaccine")
    rows = cur.fetchall()
    cur.close()
    if not rows:
        print("[!] No vaccines in database yet.")
        return False
    print("\n{:<8} {:<20} {:<20} {:<10}".format("ID", "Name", "Manufacturer", "Price"))
    print("-" * 60)
    for r in rows:
        print("{:<8} {:<20} {:<20} {:<10}".format(*r))
    print()
    return True


def place_order(conn):
    """Place a new vaccine order."""
    if not list_vaccines(conn):
        return
    while True:
        try:
            o_id   = int(input("Order ID: ").strip())
            v_id   = int(input("Vaccine ID: ").strip())
            qty    = int(input("Quantity (vials): ").strip())
            hos    = input("Hospital Name: ").strip()
            state  = input("State: ").strip()
        except ValueError:
            print("[!] Invalid input.")
            continue

        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO AD_Order (O_ID, vaccine_ID, QTY, Hospital, State) "
                "VALUES (%s, %s, %s, %s, %s)",
                (o_id, v_id, qty, hos, state)
            )
            conn.commit()
            print(f"[✓] Order #{o_id} placed successfully.")
        except Exception as e:
            print(f"[ERROR] {e}")
        finally:
            cur.close()

        if input("Place another order? (Y/N): ").strip().upper() != "Y":
            break