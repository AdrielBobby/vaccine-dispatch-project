import customtkinter as ctk
from ui.components import StatCard, StyledTable
from modules.reports import get_dashboard_stats
from modules.order import get_all_orders

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, conn):
        super().__init__(master, fg_color="transparent")
        self.conn = conn
        
        # Header
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=(20, 10))

        self.label = ctk.CTkLabel(self.header, text="Welcome, BIOPHARM", font=("Segoe UI", 24, "bold"))
        self.label.pack(side="left")

        # Refresh button
        self.refresh_btn = ctk.CTkButton(self.header, text="↺ Refresh", width=100, command=self.refresh)
        self.refresh_btn.pack(side="right")

        # Stats Cards Frame
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(fill="x", padx=20, pady=10)
        
        self.card_v = StatCard(self.stats_frame, "Total Vaccines", 0)
        self.card_v.pack(side="left", expand=True, padx=5)
        
        self.card_o = StatCard(self.stats_frame, "Total Orders", 0)
        self.card_o.pack(side="left", expand=True, padx=5)
        
        self.card_d = StatCard(self.stats_frame, "Dispatched", 0, color="#a6e3a1")
        self.card_d.pack(side="left", expand=True, padx=5)
        
        self.card_p = StatCard(self.stats_frame, "Pending", 0, color="#fab387")
        self.card_p.pack(side="left", expand=True, padx=5)

        # Recent Orders
        self.recent_label = ctk.CTkLabel(self, text="Recent Orders (last 10)", font=("Segoe UI", 16, "bold"))
        self.recent_label.pack(pady=(20, 10), padx=20, anchor="w")

        self.table = StyledTable(self, columns=("O_ID", "Vaccine", "QTY", "Hospital", "State"))
        self.table.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def on_theme_change(self, mode):
        self.table.update_theme(mode)

    def refresh(self):
        # Update Stats
        stats = get_dashboard_stats(self.conn)
        self.card_v.update_value(stats["vaccines"])
        self.card_o.update_value(stats["orders"])
        self.card_d.update_value(stats["dispatched"])
        self.card_p.update_value(stats["pending"])

        # Update Table
        self.table.delete_all()
        orders = get_all_orders(self.conn)
        # Show last 10
        for o in reversed(orders[-10:]):
            self.table.insert("", "end", values=(o["O_ID"], o["V_Name"], o["QTY"], o["Hospital"], o["State"]))
