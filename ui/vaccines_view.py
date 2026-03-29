import customtkinter as ctk
from ui.components import StyledTable, AdminGate
from modules.vaccine import get_all_vaccines, add_vaccine_direct, delete_vaccine_direct, update_vaccine_direct
from tkinter import messagebox

class VaccinesFrame(ctk.CTkFrame):
    def __init__(self, master, conn):
        super().__init__(master, fg_color="transparent")
        self.conn = conn
        self.is_admin = False

        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=(20, 10))
        
        self.title = ctk.CTkLabel(self.header, text="Vaccines", font=("Segoe UI", 24, "bold"))
        self.title.pack(side="left")

        # Admin Buttons container (hidden by default)
        self.admin_btn_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        
        self.add_btn = ctk.CTkButton(self.admin_btn_frame, text="+ Add Vaccine", command=self.open_add_dialog)
        self.add_btn.pack(side="right", padx=5)

        self.edit_btn = ctk.CTkButton(self.admin_btn_frame, text="✎ Edit Selected", command=self.open_edit_dialog)
        self.edit_btn.pack(side="right", padx=5)

        self.remove_btn = ctk.CTkButton(self.admin_btn_frame, text="🗑 Remove", fg_color="transparent", border_width=1, text_color="red", border_color="red", hover_color="#ffecec", command=self.remove_vaccine)
        self.remove_btn.pack(side="right", padx=5)

        self.table = StyledTable(self, columns=("V_ID", "Name", "Manufacturer", "Cost (₹)", "Price (₹)"))
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
        vaccines = get_all_vaccines(self.conn)
        for v in vaccines:
            self.table.insert("", "end", values=(v["V_ID"], v["V_Name"], v["Manufacturer"], v["Cost"], v["Price"]))

    def open_add_dialog(self):
        AddVaccineDialog(self, self.conn, self.refresh)

    def open_edit_dialog(self):
        selected = self.table.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a vaccine to edit.")
            return
        values = self.table.tree.item(selected[0])['values']
        EditVaccineDialog(self, self.conn, values, self.refresh)

    def remove_vaccine(self):
        selected = self.table.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a vaccine to remove.")
            return
        
        values = self.table.tree.item(selected[0])['values']
        v_id = values[0]
        v_name = values[1]
        
        if messagebox.askyesno("Confirm Removal", f"Are you sure you want to permanently delete {v_name} (ID: {v_id})?"):
            success, msg = delete_vaccine_direct(self.conn, v_id)
            if success:
                self.refresh()
            else:
                messagebox.showerror("Error", msg)

class AddVaccineDialog(ctk.CTkToplevel):
    def __init__(self, master, conn, refresh_callback):
        super().__init__(master)
        self.conn = conn
        self.refresh_callback = refresh_callback
        self.title("Add New Vaccine")
        self.geometry("400x420")
        self.after(10, self.grab_set)

        ctk.CTkLabel(self, text="Vaccine ID (4-digit):").pack(pady=(20, 0))
        self.e_id = ctk.CTkEntry(self, width=250)
        self.e_id.pack(pady=5)

        ctk.CTkLabel(self, text="Vaccine Name:").pack(pady=5)
        self.e_name = ctk.CTkEntry(self, width=250)
        self.e_name.pack(pady=5)

        ctk.CTkLabel(self, text="Manufacturer:").pack(pady=5)
        self.e_mfr = ctk.CTkEntry(self, width=250)
        self.e_mfr.pack(pady=5)

        ctk.CTkLabel(self, text="Cost per vial (₹):").pack(pady=5)
        self.e_cost = ctk.CTkEntry(self, width=250)
        self.e_cost.pack(pady=5)

        ctk.CTkLabel(self, text="Selling Price (₹):").pack(pady=5)
        self.e_price = ctk.CTkEntry(self, width=250)
        self.e_price.pack(pady=5)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=5)

        self.btn_save = ctk.CTkButton(self, text="Save", command=self.save)
        self.btn_save.pack(pady=20)

    def save(self):
        try:
            v_id = int(self.e_id.get())
            name = self.e_name.get()
            mfr = self.e_mfr.get()
            cost = int(self.e_cost.get())
            price = int(self.e_price.get())
            
            if not name or not mfr:
                raise ValueError("Fields cannot be empty")

            success, msg = add_vaccine_direct(self.conn, v_id, name, mfr, cost, price)
            if success:
                self.refresh_callback()
                self.destroy()
            else:
                self.error_label.configure(text=msg)
        except ValueError as e:
            self.error_label.configure(text=str(e))

class EditVaccineDialog(ctk.CTkToplevel):
    def __init__(self, master, conn, values, refresh_callback):
        super().__init__(master)
        self.conn = conn
        self.v_id = values[0]
        self.refresh_callback = refresh_callback
        self.title(f"Edit Vaccine - ID: {self.v_id}")
        self.geometry("400x420")
        self.after(10, self.grab_set)

        ctk.CTkLabel(self, text=f"Updating Vaccine ID: {self.v_id}").pack(pady=(20, 5))

        ctk.CTkLabel(self, text="Vaccine Name:").pack(pady=5)
        self.e_name = ctk.CTkEntry(self, width=250)
        self.e_name.insert(0, values[1])
        self.e_name.pack(pady=5)

        ctk.CTkLabel(self, text="Manufacturer:").pack(pady=5)
        self.e_mfr = ctk.CTkEntry(self, width=250)
        self.e_mfr.insert(0, values[2])
        self.e_mfr.pack(pady=5)

        ctk.CTkLabel(self, text="Cost per vial (₹):").pack(pady=5)
        self.e_cost = ctk.CTkEntry(self, width=250)
        self.e_cost.insert(0, str(values[3]))
        self.e_cost.pack(pady=5)

        ctk.CTkLabel(self, text="Selling Price (₹):").pack(pady=5)
        self.e_price = ctk.CTkEntry(self, width=250)
        self.e_price.insert(0, str(values[4]))
        self.e_price.pack(pady=5)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=5)

        self.btn_save = ctk.CTkButton(self, text="Update Vaccine", command=self.save)
        self.btn_save.pack(pady=20)

    def save(self):
        try:
            name = self.e_name.get()
            mfr = self.e_mfr.get()
            cost = int(self.e_cost.get())
            price = int(self.e_price.get())
            
            if not name or not mfr:
                raise ValueError("Fields cannot be empty")

            success, msg = update_vaccine_direct(self.conn, self.v_id, name, mfr, cost, price)
            if success:
                self.refresh_callback()
                self.destroy()
            else:
                self.error_label.configure(text=msg)
        except ValueError as e:
            self.error_label.configure(text=str(e))
