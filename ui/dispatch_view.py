import customtkinter as ctk
from ui.components import StyledTable
from modules.dispatch import get_dispatch_status_report, record_dispatch_direct, update_dispatch_direct
from datetime import datetime
from tkinter import messagebox

class DispatchFrame(ctk.CTkFrame):
    def __init__(self, master, conn):
        super().__init__(master, fg_color="transparent")
        self.conn = conn
        self.is_admin = False

        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=(20, 10))
        
        self.title = ctk.CTkLabel(self.header, text="Dispatch Tracker", font=("Segoe UI", 24, "bold"))
        self.title.pack(side="left")

        # Admin Buttons
        self.admin_btn_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        self.edit_btn = ctk.CTkButton(self.admin_btn_frame, text="✎ Edit Dispatch", command=self.open_edit_dialog)
        self.edit_btn.pack(side="right", padx=5)

        # Refresh button (now inside header)
        self.refresh_btn = ctk.CTkButton(self.header, text="↺ Refresh", width=100, command=self.refresh)
        self.refresh_btn.pack(side="right", padx=5)

        self.table = StyledTable(self, columns=("O_ID", "Vaccine", "QTY", "Hospital", "State", "Status"))
        self.table.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.dispatch_btn = ctk.CTkButton(self, text="Record Dispatch for Selected", command=self.open_dispatch_dialog)
        self.dispatch_btn.pack(pady=10)

    def on_admin_state_change(self, is_admin):
        self.is_admin = is_admin
        if is_admin:
            self.admin_btn_frame.pack(side="right")
        else:
            self.admin_btn_frame.pack_forget()

    def on_theme_change(self, mode):
        self.table.update_theme(mode)

    def refresh(self):
        self.table.delete_all()
        data = get_dispatch_status_report(self.conn)
        self.full_data = data 
        for d in data:
            status_symbol = "✅ " if d["Status"] == "Dispatched" else "⏳ "
            self.table.insert("", "end", values=(d["O_ID"], d["V_Name"], d["QTY"], d["Hospital"], d["State"], status_symbol + d["Status"]))

    def open_dispatch_dialog(self):
        selected = self.table.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an order to dispatch.")
            return
        values = self.table.tree.item(selected[0])['values']
        o_id = values[0]
        status = values[5]
        if "Dispatched" in status:
            messagebox.showinfo("Info", "This order has already been dispatched.")
            return
        record = next((item for item in self.full_data if item["O_ID"] == o_id), None)
        if record:
            RecordDispatchDialog(self, self.conn, record, self.refresh)

    def open_edit_dialog(self):
        selected = self.table.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to edit.")
            return
        values = self.table.tree.item(selected[0])['values']
        o_id = values[0]
        status = values[5]
        if "Pending" in status:
            messagebox.showwarning("Warning", "Only dispatched records can be edited here. Use Orders tab to edit pending orders.")
            return
        record = next((item for item in self.full_data if item["O_ID"] == o_id), None)
        if record:
            EditDispatchDialog(self, self.conn, record, self.refresh)

class RecordDispatchDialog(ctk.CTkToplevel):
    def __init__(self, master, conn, record, refresh_callback):
        super().__init__(master)
        self.conn = conn
        self.record = record
        self.refresh_callback = refresh_callback
        self.title(f"Record Dispatch - Order #{record['O_ID']}")
        self.geometry("420x480")
        self.after(10, self.grab_set)

        ctk.CTkLabel(self, text=f"Dispatching Vaccine: {record['V_Name']}").pack(pady=(20, 5))

        ctk.CTkLabel(self, text="Hospital:").pack(pady=5)
        self.e_hos = ctk.CTkEntry(self, width=250)
        self.e_hos.insert(0, record['Hospital'])
        self.e_hos.pack(pady=5)

        ctk.CTkLabel(self, text="State:").pack(pady=5)
        self.e_state = ctk.CTkEntry(self, width=250)
        self.e_state.insert(0, record['State'])
        self.e_state.pack(pady=5)

        ctk.CTkLabel(self, text="Quantity:").pack(pady=5)
        self.e_qty = ctk.CTkEntry(self, width=250)
        self.e_qty.insert(0, str(record['QTY']))
        self.e_qty.pack(pady=5)

        ctk.CTkLabel(self, text="Date (YYYY-MM-DD):").pack(pady=5)
        self.e_date = ctk.CTkEntry(self, width=250)
        self.e_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.e_date.pack(pady=5)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=5)

        self.btn_save = ctk.CTkButton(self, text="Confirm Dispatch", command=self.save)
        self.btn_save.pack(pady=20)

    def save(self):
        try:
            qty = int(self.e_qty.get())
            hos = self.e_hos.get()
            state = self.e_state.get()
            date_str = self.e_date.get()
            datetime.strptime(date_str, "%Y-%m-%d")
            if not hos or not state:
                raise ValueError("Fields cannot be empty")
            success, msg = record_dispatch_direct(self.conn, self.record['O_ID'], self.record['vaccine_ID'], qty, hos, state, date_str)
            if success:
                self.refresh_callback()
                self.destroy()
            else:
                self.error_label.configure(text=msg)
        except Exception as e:
            self.error_label.configure(text=f"Invalid Input: {e}")

class EditDispatchDialog(ctk.CTkToplevel):
    def __init__(self, master, conn, record, refresh_callback):
        super().__init__(master)
        self.conn = conn
        self.record = record
        self.refresh_callback = refresh_callback
        self.title(f"Edit Dispatch - Order #{record['O_ID']}")
        self.geometry("420x480")
        self.after(10, self.grab_set)

        # Get existing dispatch date
        cur = self.conn.cursor()
        cur.execute("SELECT date_Dispatch FROM Dispatch WHERE Order_ID = %s", (record['O_ID'],))
        d_date = cur.fetchone()[0]
        cur.close()

        ctk.CTkLabel(self, text=f"Editing Dispatch for: {record['V_Name']}").pack(pady=(20, 5))

        ctk.CTkLabel(self, text="Hospital:").pack(pady=5)
        self.e_hos = ctk.CTkEntry(self, width=250)
        self.e_hos.insert(0, record['Hospital'])
        self.e_hos.pack(pady=5)

        ctk.CTkLabel(self, text="State:").pack(pady=5)
        self.e_state = ctk.CTkEntry(self, width=250)
        self.e_state.insert(0, record['State'])
        self.e_state.pack(pady=5)

        ctk.CTkLabel(self, text="Quantity:").pack(pady=5)
        self.e_qty = ctk.CTkEntry(self, width=250)
        self.e_qty.insert(0, str(record['QTY']))
        self.e_qty.pack(pady=5)

        ctk.CTkLabel(self, text="Date (YYYY-MM-DD):").pack(pady=5)
        self.e_date = ctk.CTkEntry(self, width=250)
        self.e_date.insert(0, str(d_date))
        self.e_date.pack(pady=5)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=5)

        self.btn_save = ctk.CTkButton(self, text="Update Dispatch", command=self.save)
        self.btn_save.pack(pady=20)

    def save(self):
        try:
            qty = int(self.e_qty.get())
            hos = self.e_hos.get()
            state = self.e_state.get()
            date_str = self.e_date.get()
            datetime.strptime(date_str, "%Y-%m-%d")
            if not hos or not state:
                raise ValueError("Fields cannot be empty")
            success, msg = update_dispatch_direct(self.conn, self.record['O_ID'], self.record['vaccine_ID'], qty, hos, state, date_str)
            if success:
                self.refresh_callback()
                self.destroy()
            else:
                self.error_label.configure(text=msg)
        except Exception as e:
            self.error_label.configure(text=f"Invalid Input: {e}")
