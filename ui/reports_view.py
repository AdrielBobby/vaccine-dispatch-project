import customtkinter as ctk
from ui.components import StyledTable
from modules.reports import get_sales_summary, get_pending_report_data, dispatch_graph

class ReportsFrame(ctk.CTkFrame):
    def __init__(self, master, conn):
        super().__init__(master, fg_color="transparent")
        self.conn = conn

        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=(20, 10))
        
        self.title = ctk.CTkLabel(self.header, text="Reports", font=("Segoe UI", 24, "bold"))
        self.title.pack(side="left")

        # Tabs-like button frame
        self.tab_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tab_frame.pack(fill="x", padx=20, pady=5)
        
        self.btn_sales = ctk.CTkButton(self.tab_frame, text="Sales Report", width=120, command=self.show_sales)
        self.btn_sales.pack(side="left", padx=5)
        
        self.btn_pending = ctk.CTkButton(self.tab_frame, text="Pending Orders", width=120, command=self.show_pending)
        self.btn_pending.pack(side="left", padx=5)
        
        self.btn_graph = ctk.CTkButton(self.tab_frame, text="Show Graph", width=120, command=lambda: dispatch_graph(self.conn))
        self.btn_graph.pack(side="left", padx=5)

        # Content area for reports
        self.report_container = ctk.CTkScrollableFrame(self, fg_color=("white", "#24283b"), corner_radius=10)
        self.report_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.content_label = ctk.CTkLabel(self.report_container, text="Select a report to view", justify="left", font=("Consolas", 12))
        self.content_label.pack(fill="both", expand=True, padx=20, pady=20)

    def on_theme_change(self, mode):
        pass # CTK labels inside ScrollableFrame handle themselves

    def refresh(self):
        self.show_sales()

    def show_sales(self):
        data = get_sales_summary(self.conn)
        if not data:
            self.content_label.configure(text="No data available.")
            return

        report = f"""
BIOPHARM PHARMACEUTICAL COMPANY — SALES REPORT
============================================================

Total Vaccines Ordered   : {data['total_ordered']}
Total Dispatched         : {data['total_dispatched']}
Total Revenue            : ₹{data['revenue']:,}

Ordered Hospitals:
------------------
"""
        for h in data['ordered_hospitals']:
            report += f" • {h[0]}, {h[1]}\n"

        report += "\nProfit Breakdown:\n------------------\n"
        for p in data['profits']:
            report += f" • {p[1]:<20} ₹{p[0]:,}\n"

        self.content_label.configure(text=report)

    def show_pending(self):
        data = get_pending_report_data(self.conn)
        if not data:
            self.content_label.configure(text="No pending orders — all orders have been dispatched!")
            return

        report = "PENDING DISPATCH REPORT\n============================================================\n\n"
        for d in data:
            report += f"Order ID      : {d['O_ID']}\n"
            report += f"Vaccine       : {d['V_Name']}\n"
            report += f"Manufacturer  : {d['Manufacturer']}\n"
            report += f"Qty Requested : {d['QTY']}\n"
            report += f"Destination   : {d['Hospital']}, {d['State']}\n"
            report += f"Potential Val : ₹{d['potential_profit']:,}\n"
            report += "-" * 50 + "\n"

        self.content_label.configure(text=report)
