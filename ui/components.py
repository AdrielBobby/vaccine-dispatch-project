import customtkinter as ctk
from tkinter import ttk

class StyledTable(ctk.CTkFrame):
    """A wrapper around ttk.Treeview to make it look decent in CustomTkinter."""
    def __init__(self, master, columns, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Style for Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
                        background="#ffffff",
                        foreground="#000000",
                        rowheight=25,
                        fieldbackground="#ffffff",
                        bordercolor="#cccccc",
                        borderwidth=0)
        style.map("Treeview", background=[('selected', '#4C72B0')])
        style.configure("Treeview.Heading", 
                        background="#eeeeee", 
                        foreground="#000000", 
                        relief="flat",
                        font=('Segoe UI', 10, 'bold'))

        self.tree = ttk.Treeview(self, columns=columns, show="headings", style="Treeview")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

    def update_theme(self, mode):
        """Update the underlying Tkinter Treeview colors manually."""
        style = ttk.Style()
        if mode == "Dark":
            style.configure("Treeview", 
                            background="#24283b", 
                            foreground="#c0caf5", 
                            fieldbackground="#24283b")
            style.configure("Treeview.Heading", 
                            background="#1a1b26", 
                            foreground="#c0caf5")
        else:
            style.configure("Treeview", 
                            background="#ffffff", 
                            foreground="#000000", 
                            fieldbackground="#ffffff")
            style.configure("Treeview.Heading", 
                            background="#eeeeee", 
                            foreground="#000000")

    def insert(self, *args, **kwargs):
        return self.tree.insert(*args, **kwargs)

    def delete_all(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

class StatCard(ctk.CTkFrame):
    """Dashboard stat card."""
    def __init__(self, master, title, value, color="#4C72B0", **kwargs):
        super().__init__(master, border_width=2, border_color=color, **kwargs)
        
        self.label_title = ctk.CTkLabel(self, text=title, font=("Segoe UI", 14))
        self.label_title.pack(pady=(10, 0), padx=20)
        
        self.label_value = ctk.CTkLabel(self, text=str(value), font=("Segoe UI", 24, "bold"), text_color=color)
        self.label_value.pack(pady=(5, 15), padx=20)

    def update_value(self, new_value):
        self.label_value.configure(text=str(new_value))

class AdminGate(ctk.CTkToplevel):
    """Admin verification modal."""
    def __init__(self, master, callback, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Admin Verification")
        self.geometry("320x200")
        self.callback = callback
        
        # Make it modal
        self.after(10, self.grab_set)
        
        self.label = ctk.CTkLabel(self, text="Enter Admin Code to continue:", font=("Segoe UI", 12))
        self.label.pack(pady=(20, 10))
        
        self.entry = ctk.CTkEntry(self, show="*", width=200)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", lambda e: self.confirm())
        
        self.error_label = ctk.CTkLabel(self, text="", text_color="red", font=("Segoe UI", 10))
        self.error_label.pack()
        
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=20)
        
        self.btn_confirm = ctk.CTkButton(self.btn_frame, text="Confirm", command=self.confirm, width=100)
        self.btn_confirm.pack(side="left", padx=5)
        
        self.btn_cancel = ctk.CTkButton(self.btn_frame, text="Cancel", command=self.destroy, width=100, fg_color="gray")
        self.btn_cancel.pack(side="left", padx=5)

    def confirm(self):
        code = self.entry.get()
        if code == "BIOpharmAdMiN":
            self.destroy()
            self.callback()
        else:
            self.error_label.configure(text="Incorrect admin code.")
