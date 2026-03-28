import mysql.connector as mycon
import matplotlib.pyplot as pp

# Connect to MySQL (change user/password if needed)
scon = mycon.connect(host='localhost', user='root', passwd='rootl23')
cl = scon.cursor()
c1 = scon.cursor()

# Create database and tables if they do not exist
cl.execute('CREATE DATABASE IF NOT EXISTS VaccineDispatch')
cl.execute('USE VaccineDispatch')

cl.execute("""
CREATE TABLE IF NOT EXISTS AD_Vaccine(
    V_ID int(4) PRIMARY KEY,
    V_Name varchar(50),
    Manufacturer varchar(100),
    Cost int(6),
    price int(7)
);
""")

cl.execute("""
CREATE TABLE IF NOT EXISTS AD_Order(
    O_ID int(5) PRIMARY KEY,
    vaccine_ID int(4),
    QTY int(3),
    Hospital varchar(100),
    State varchar(70),
    FOREIGN KEY (vaccine_ID) REFERENCES AD_Vaccine(V_ID)
);
""")

cl.execute("CREATE INDEX IF NOT EXISTS hospital_idx ON AD_Order (Hospital);")

cl.execute("""
CREATE TABLE IF NOT EXISTS Dispatch(
    Order_ID int(5) PRIMARY KEY,
    Vaccine_ID int(4),
    QTY int(3),
    Hospital varchar(100),
    State varchar(70),
    date_Dispatch date,
    FOREIGN KEY (Order_ID) REFERENCES AD_Order(O_ID),
    FOREIGN KEY (Vaccine_ID) REFERENCES AD_Vaccine(V_ID)
);
""")

scon.commit()


# Function to add new vaccine (Admin only)
def new_Vaccine():
    while True:
        ad = input("Enter Admin Code : ")
        if ad == 'BIOpharmAdMiN':
            V_ID = int(input("Enter the ID of the vaccine (4) : "))
            V_Name = input("Enter name of Vaccine : ")
            Man = input("Enter the name of the Manufacturer: ")
            Cost = int(input("Enter the production Cost per vaccine (6 digits): "))
            Price = int(input("Enter the selling price of the vaccine (7 digits): "))
            q = (
                "INSERT INTO AD_Vaccine (V_ID, V_Name, Manufacturer, Cost, Price) "
                "VALUES ({}, '{}', '{}', {}, {});"
            ).format(V_ID, V_Name, Man, Cost, Price)
            cl.execute(q)
            scon.commit()
            ch = input("Do you want to continue (Y/N): ")
            if ch in 'Nn':
                break
        else:
            print("Wrong Admin Key, Entry Denied")
            break


# Function to insert a new order
def insert_Order():
    while True:
        try:
            cl.execute('SELECT * FROM AD_Vaccine')
            data = cl.fetchall()
            for i in data:
                print(i)
                print()
            O_ID = int(input("Enter the Order ID (4): "))
            Vaccine_ID = int(input("Enter the ID of the vaccine you want : "))
            QTY = int(input("Enter the vials of vaccine needed : "))
            Hos = input("Enter Hospital: ")
            St = input("Enter State: ")
            q1 = "INSERT INTO AD_order VALUES ({},{},{},'{}','{}')".format(
                O_ID, Vaccine_ID, QTY, Hos, St
            )
            cl.execute(q1)
            scon.commit()
            ch = input("Do you want to Continue? (Y/N) : ")
            if ch in 'Nn':
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            continue


# Function to update Dispatch table
def update_Dispatch():
    while True:
        cl.execute("SELECT * FROM AD_Order")
        data = cl.fetchall()
        for i in data:
            print(i)
        print()
        Ord = int(input("Enter Order ID: "))
        Vac = int(input("Enter Vaccine ID: "))
        QTY = int(input("Enter vials of vaccines needed: "))
        Hospital = input("Enter Hospital name: ")
        St = input("Enter State: ")
        D_O_D = input("Enter Date of Dispatch in YYYY-MM-DD format: ")
        cl.execute(
            "INSERT INTO Dispatch VALUES ({},{},{},'{}','{}','{}')".format(
                Ord, Vac, QTY, Hospital, St, D_O_D
            )
        )
        scon.commit()
        ch = input("Do you want to Continue? (Y/N) : ")
        if ch in 'Nn':
            break


# Sales report for dispatched + ordered
def REPORT():
    # Orders
    c1.execute("SELECT SUM(Qty) FROM AD_Order")
    d1 = c1.fetchall()
    c1.execute("SELECT Hospital, State FROM AD_Order")
    HS = c1.fetchall()

    print(
        """
________________________________________________________________________________
BIOPHARM PHARMACEUTICAL COMPANY
SALES REPORT

Vaccines Ordered : {}
Ordered Hospitals:""".format(
            d1[0][0]
        )
    )
    for i in HS:
        print(i[0], i[1])

    # Dispatched and revenue
    c1.execute("SELECT SUM(QTY) FROM Dispatch")
    d0 = c1.fetchall()
    c1.execute(
        "SELECT SUM(a.price*b.QTY) FROM AD_vaccine a, Dispatch b "
        "WHERE a.V_ID = b.Vaccine_ID"
    )
    d3 = c1.fetchall()
    c1.execute(
        "SELECT SUM(a.cost*b.QTY) FROM AD_vaccine a, Dispatch b "
        "WHERE a.V_ID = b.Vaccine_ID"
    )
    d4 = c1.fetchall()
    c1.execute(
        "SELECT (a.price - a.cost)*b.QTY, a.V_Name "
        "FROM AD_vaccine a, Dispatch b "
        "WHERE a.V_ID = b.Vaccine_ID"
    )
    d5 = c1.fetchall()

    print(
        """DISPATCH
No. of Vaccines dispatched: {}
Revenue                    : {}
SALES
Profit gained:""".format(
            d0[0][0], d3[0][0]
        )
    )
    for i in d5:
        print(i[0], i[1])

    print(
        """
________________________________________________________________________________
"""
    )


# Pending sales report (orders not yet dispatched)
def Pending_Report():
    print(
        """
________________________________________________________________________________
REPORT
PENDING SALES OF VACCINES"""
    )

    c1.execute(
        "SELECT * FROM AD_Order WHERE O_ID NOT IN "
        "(SELECT Order_ID FROM Dispatch)"
    )
    pending_orders = c1.fetchall()

    for order in pending_orders:
        c1.execute(
            "SELECT DISTINCT a.* FROM AD_Vaccine a , AD_Order b "
            "WHERE a.V_ID = b.vaccine_ID AND a.V_ID = {}".format(order[1])
        )
        z = c1.fetchall()
        print("Order ID:", order[0])
        print("Vaccine Name:", z[0][1])
        print("Manufacturer:", z[0][2])
        print("Quantity Requested:", order[2])
        print("Destination:", order[3], ",", order[4])
        print("Value:", (z[0][4] - z[0][3]) * order[2])
        print("-" * 50)

    print(
        """
________________________________________________________________________________
"""
    )


# Graph of dispatched vaccines by vaccine name
def Graph():
    """
    Plots a bar graph of the amount of vaccines dispatched for each vaccine,
    with vaccine name on the x-axis and amount of vaccines dispatched on the y-axis.
    """

    c1.execute(
        "SELECT a.V_Name, SUM(b.QTY) AS Total_Vaccines_Dispatched "
        "FROM AD_Vaccine a, Dispatch b "
        "WHERE a.V_ID = b.Vaccine_ID GROUP BY V_ID;"
    )
    results = c1.fetchall()

    vaccine_names = [row[0] for row in results]
    total_vaccines_dispatched = [row[1] for row in results]

    pp.bar(vaccine_names, total_vaccines_dispatched)
    pp.title('Amount of Vaccines Dispatched for Each Vaccine')
    pp.xlabel('Vaccine Name')
    pp.ylabel('Amount of Vaccines Dispatched')
    pp.show()


# Main menu loop
print("WELCOME TO THE VACCINE DISPATCH DATABASE OF BIOPHARM PHARMACEUTICAL COMPANY")

while True:
    print()
    print("What would you like to do?")
    print("1. Enter details of a new vaccine (Admins only)")
    print("2. Enter a new Order")
    print("3. Enter Details of Vaccine dispatched")
    print("4. Produce a Report on Sales")
    print("5. Produce Pending Sales Report")
    print("6. Graph of Sales of each vaccine")
    print("7. Exit from Database")
    ch = int(input("Enter your choice: "))

    if ch == 1:
        new_Vaccine()
    elif ch == 2:
        insert_Order()
    elif ch == 3:
        update_Dispatch()
    elif ch == 4:
        REPORT()
    elif ch == 5:
        Pending_Report()
    elif ch == 6:
        Graph()
    elif ch == 7:
        print("Exiting from Database........")
        print("        Have a nice day")
        break
    else:
        print("Unspecified choice....................... Try Again")