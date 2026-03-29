import customtkinter as ctk
from ui.components import StyledTable
from modules.order import get_all_orders, place_order_direct, update_order_direct
from modules.vaccine import get_all_vaccines
from tkinter import messagebox

class OrdersFrame(ctk.CTkFrame):
    def __init__(self, master, conn):
        super().__init__(master, fg_color="transparent")
        self.conn = conn
        self.is_admin = False

        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=(20, 10))
        
        self.title = ctk.CTkLabel(self.header, text="Orders", font=("Segoe UI", 24, "bold"))
        self.title.pack(side="left")

        # Admin Buttons container
        self.admin_btn_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        
        self.add_btn = ctk.CTkButton(self.admin_btn_frame, text="+ New Order", command=self.open_add_dialog)
        self.add_btn.pack(side="right", padx=5)

        self.edit_btn = ctk.CTkButton(self.admin_btn_frame, text="✎ Edit Order", command=self.open_edit_dialog)
        self.edit_btn.pack(side="right", padx=5)

        self.table = StyledTable(self, columns=("O_ID", "Vaccine", "QTY", "Hospital", "State"))
        self.table.pack(fill="both", expand=True, padx=20, pady=(0, 20))

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
        orders = get_all_orders(self.conn)
        for o in orders:
            self.table.insert("", "end", values=(o["O_ID"], o["V_Name"], o["QTY"], o["Hospital"], o["State"]))

    def open_add_dialog(self):
        NewOrderDialog(self, self.conn, self.refresh)

    def open_edit_dialog(self):
        selected = self.table.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an order to edit.")
            return
        values = self.table.tree.item(selected[0])['values']
        EditOrderDialog(self, self.conn, values, self.refresh)

class NewOrderDialog(ctk.CTkToplevel):
    def __init__(self, master, conn, refresh_callback):
        super().__init__(master)
        self.conn = conn
        self.refresh_callback = refresh_callback
        self.title("Place New Order")
        self.geometry("420x550")
        self.after(10, self.grab_set)

        # Fetch vaccines for dropdown
        self.vaccines = get_all_vaccines(self.conn)
        self.vac_names = [f"{v['V_Name']} (ID: {v['V_ID']})" for v in self.vaccines]

        ctk.CTkLabel(self, text="Order ID:").pack(pady=(20, 0))
        self.e_id = ctk.CTkEntry(self, width=250)
        self.e_id.pack(pady=5)

        ctk.CTkLabel(self, text="Select Vaccine:").pack(pady=5)
        self.e_vac = ctk.CTkComboBox(self, values=self.vac_names, width=250)
        self.e_vac.pack(pady=5)

        ctk.CTkLabel(self, text="Quantity (vials):").pack(pady=5)
        self.e_qty = ctk.CTkEntry(self, width=250)
        self.e_qty.pack(pady=5)

        ctk.CTkLabel(self, text="Hospital:").pack(pady=5)
        self.e_hos = ctk.CTkEntry(self, width=250)
        self.e_hos.pack(pady=5)

        ctk.CTkLabel(self, text="State:").pack(pady=5)
        self.e_state = ctk.CTkEntry(self, width=250)
        self.e_state.pack(pady=5)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=5)

        self.btn_save = ctk.CTkButton(self, text="Place Order", command=self.save)
        self.btn_save.pack(pady=20)

    def save(self):
        try:
            o_id_str = self.e_id.get()
            qty_str = self.e_qty.get()
            hos = self.e_hos.get()
            state = self.e_state.get()
            selected_vac = self.e_vac.get()

            if not o_id_str or not qty_str or not hos or not state or not selected_vac:
                raise ValueError("All fields are required")

            o_id = int(o_id_str)
            qty = int(qty_str)
            v_id = int(selected_vac.split("ID: ")[1].rstrip(")"))

            success, msg = place_order_direct(self.conn, o_id, v_id, qty, hos, state)
            if success:
                self.refresh_callback()
                self.destroy()
            else:
                self.error_label.configure(text=msg)
        except Exception as e:
            self.error_label.configure(text=str(e))

class EditOrderDialog(ctk.CTkToplevel):
    def __init__(self, master, conn, values, refresh_callback):
        super().__init__(master)
        self.conn = conn
        self.o_id = values[0]
        self.refresh_callback = refresh_callback
        self.title(f"Edit Order - ID: {self.o_id}")
        self.geometry("420x520")
        self.after(10, self.grab_set)

        self.vaccines = get_all_vaccines(self.conn)
        self.vac_names = [f"{v['V_Name']} (ID: {v['V_ID']})" for v in self.vaccines]

        ctk.CTkLabel(self, text=f"Updating Order ID: {self.o_id}").pack(pady=(20, 5))

        ctk.CTkLabel(self, text="Select Vaccine:").pack(pady=5)
        self.e_vac = ctk.CTkComboBox(self, values=self.vac_names, width=250)
        # Find index of current vaccine name
        for i, name in enumerate(self.vac_names):
            if values[1] in name:
                self.e_vac.set(name)
                break
        self.e_vac.pack(pady=5)

        ctk.CTkLabel(self, text="Quantity (vials):").pack(pady=5)
        self.e_qty = ctk.CTkEntry(self, width=250)
        self.e_qty.insert(0, str(values[2]))
        self.e_qty.pack(pady=5)

        ctk.CTkLabel(self, text="Hospital:").pack(pady=5)
        self.e_hos = ctk.CTkEntry(self, width=250)
        self.e_hos.insert(0, values[3])
        self.e_hos.pack(pady=5)

        ctk.CTkLabel(self, text="State:").pack(pady=5)
        self.e_state = ctk.CTkEntry(self, width=250)
        self.e_state.insert(0, values[4])
        self.e_state.pack(pady=5)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=5)

        self.btn_save = ctk.CTkButton(self, text="Update Order", command=self.save)
        self.btn_save.pack(pady=20)

    def save(self):
        try:
            qty_str = self.e_qty.get()
            hos = self.e_hos.get()
            state = self.e_state.get()
            selected_vac = self.e_vac.get()

            if not qty_str or not hos or not state or not selected_vac:
                raise ValueError("All fields are required")

            qty = int(qty_str)
            v_id = int(selected_vac.split("ID: ")[1].rstrip(")"))

            success, msg = update_order_direct(self.conn, self.o_id, v_id, qty, hos, state)
            if success:
                self.refresh_callback()
                self.destroy()
            else:
                self.error_label.configure(text=msg)
        except Exception as e:
            self.error_label.configure(text=str(e))
