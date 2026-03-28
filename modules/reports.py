import matplotlib.pyplot as plt

DIVIDER = "=" * 72

def sales_report(conn):
    """Print a full sales + dispatch summary."""
    cur = conn.cursor()

    cur.execute("SELECT SUM(QTY) FROM AD_Order")
    total_ordered = cur.fetchone()[0] or 0

    cur.execute("SELECT Hospital, State FROM AD_Order")
    ordered_hospitals = cur.fetchall()

    cur.execute("SELECT SUM(QTY) FROM Dispatch")
    total_dispatched = cur.fetchone()[0] or 0

    cur.execute(
        "SELECT SUM(a.Price * b.QTY) "
        "FROM AD_Vaccine a JOIN Dispatch b ON a.V_ID = b.Vaccine_ID"
    )
    revenue = cur.fetchone()[0] or 0

    cur.execute(
        "SELECT (a.Price - a.Cost) * b.QTY, a.V_Name "
        "FROM AD_Vaccine a JOIN Dispatch b ON a.V_ID = b.Vaccine_ID"
    )
    profits = cur.fetchall()
    cur.close()

    print(f"\n{DIVIDER}")
    print("  BIOPHARM PHARMACEUTICAL COMPANY — SALES REPORT")
    print(DIVIDER)
    print(f"  Total Vaccines Ordered   : {total_ordered}")
    print("  Ordered Hospitals:")
    for h in ordered_hospitals:
        print(f"    • {h[0]}, {h[1]}")
    print(f"\n  Total Dispatched         : {total_dispatched}")
    print(f"  Total Revenue            : ₹{revenue:,}")
    print("\n  Profit Breakdown:")
    for p in profits:
        print(f"    • {p[1]:<20} ₹{p[0]:,}")
    print(DIVIDER + "\n")


def pending_report(conn):
    """Print all orders that have NOT been dispatched yet."""
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM AD_Order WHERE O_ID NOT IN (SELECT Order_ID FROM Dispatch)"
    )
    pending = cur.fetchall()

    print(f"\n{DIVIDER}")
    print("  PENDING DISPATCH REPORT")
    print(DIVIDER)

    if not pending:
        print("  No pending orders — all orders have been dispatched!")
        print(DIVIDER + "\n")
        cur.close()
        return

    for order in pending:
        cur.execute(
            "SELECT * FROM AD_Vaccine WHERE V_ID = %s", (order[1],)
        )
        vac = cur.fetchone()
        profit = (vac[4] - vac[3]) * order[2] if vac else "N/A"
        print(f"  Order ID      : {order[0]}")
        print(f"  Vaccine       : {vac[1] if vac else 'Unknown'}")
        print(f"  Manufacturer  : {vac[2] if vac else 'Unknown'}")
        print(f"  Qty Requested : {order[2]}")
        print(f"  Destination   : {order[3]}, {order[4]}")
        print(f"  Potential Val : ₹{profit:,}")
        print("  " + "-" * 50)
    print(DIVIDER + "\n")
    cur.close()


def dispatch_graph(conn):
    """Bar chart of total vaccines dispatched per vaccine."""
    cur = conn.cursor()
    cur.execute(
        "SELECT a.V_Name, SUM(b.QTY) "
        "FROM AD_Vaccine a JOIN Dispatch b ON a.V_ID = b.Vaccine_ID "
        "GROUP BY a.V_ID"
    )
    results = cur.fetchall()
    cur.close()

    if not results:
        print("[!] No dispatch data to plot.")
        return

    names = [r[0] for r in results]
    totals = [r[1] for r in results]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(names, totals, color="#4C72B0", edgecolor="white", width=0.5)
    ax.bar_label(bars, padding=4, fontsize=10)
    ax.set_title("Vaccines Dispatched per Vaccine", fontsize=14, fontweight="bold")
    ax.set_xlabel("Vaccine Name", fontsize=11)
    ax.set_ylabel("Total Vials Dispatched", fontsize=11)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.show()