import customtkinter as ctk
import os
from db.connection import get_connection
from db.setup import initialize_db
from ui.components import AdminGate

# Import views
from ui.dashboard import DashboardFrame
from ui.vaccines_view import VaccinesFrame
from ui.orders_view import OrdersFrame
from ui.dispatch_view import DispatchFrame
from ui.reports_view import ReportsFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Admin State
        self.is_admin = False

        # DB Connection
        try:
            self.conn = get_connection()
            db_name = os.getenv("DB_NAME", "VaccineDispatch")
            self.conn.cursor().execute(f"USE {db_name}")
        except Exception as e:
            print(f"Connection error: {e}")
            self.conn = None

        # Window Setup
        self.title("BIOPHARM — Vaccine Dispatch Tracker")
        self.geometry("1100x680")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Grid Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#1e1e2e")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="BIOPHARM", font=ctk.CTkFont(size=20, weight="bold"), text_color="#cdd6f4")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Navigation Buttons
        self.nav_buttons = []
        self.create_nav_button("Dashboard", 1, self.show_dashboard)
        self.create_nav_button("Vaccines", 2, self.show_vaccines)
        self.create_nav_button("Orders", 3, self.show_orders)
        self.create_nav_button("Dispatch", 4, self.show_dispatch)
        self.create_nav_button("Reports", 5, self.show_reports)

        # Admin Login Button
        self.admin_btn = ctk.CTkButton(self.sidebar, text="Sign In as Admin", corner_radius=5, height=35,
                                      fg_color="#f38ba8", hover_color="#f38ba8", text_color="white",
                                      command=self.admin_login_click)
        self.admin_btn.grid(row=7, column=0, padx=20, pady=(10, 0))

        # DB Status
        self.status_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.status_frame.grid(row=8, column=0, pady=(20, 10), padx=20, sticky="s")
        
        status_color = "green" if self.conn else "red"
        self.status_dot = ctk.CTkLabel(self.status_frame, text="●", text_color=status_color, font=("Arial", 16))
        self.status_dot.pack(side="left", padx=5)
        
        self.status_text = ctk.CTkLabel(self.status_frame, text="DB: Live" if self.conn else "DB: Offline", text_color="#cdd6f4")
        self.status_text.pack(side="left")

        # Appearance Mode Switch
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar, text="Appearance Mode:", text_color="#cdd6f4", anchor="w")
        self.appearance_mode_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar, values=["Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 20))
        self.appearance_mode_optionemenu.set("Light")

        # Content Area
        self.content_area = ctk.CTkFrame(self, corner_radius=0, fg_color=("#f5f5f5", "#1a1b26"))
        self.content_area.grid(row=0, column=1, sticky="nsew")
        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(0, weight=1)

        # Initialize Frames
        self.frames = {}
        self.current_frame_class = None
        self.show_dashboard()

    def create_nav_button(self, text, row, command):
        btn = ctk.CTkButton(self.sidebar, text=text, corner_radius=0, height=40, border_spacing=10, 
                            fg_color="transparent", text_color="#cdd6f4", hover_color="#313244",
                            anchor="w", command=command)
        btn.grid(row=row, column=0, sticky="ew")
        self.nav_buttons.append(btn)

    def select_button(self, index):
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.configure(fg_color="#313244")
            else:
                btn.configure(fg_color="transparent")

    def admin_login_click(self):
        if not self.is_admin:
            AdminGate(self, callback=self.on_admin_success)
        else:
            self.is_admin = False
            self.admin_btn.configure(text="Sign In as Admin", fg_color="#f38ba8")
            self.refresh_current_frame()

    def on_admin_success(self):
        self.is_admin = True
        self.admin_btn.configure(text="Admin: Active", fg_color="#a6e3a1", text_color="black")
        self.refresh_current_frame()

    def refresh_current_frame(self):
        if self.current_frame_class in self.frames:
            frame = self.frames[self.current_frame_class]
            if hasattr(frame, "on_admin_state_change"):
                frame.on_admin_state_change(self.is_admin)
            if hasattr(frame, "refresh"):
                frame.refresh()

    def show_frame(self, frame_class, index):
        self.select_button(index)
        self.current_frame_class = frame_class
        if frame_class not in self.frames:
            self.frames[frame_class] = frame_class(self.content_area, self.conn)
        
        frame = self.frames[frame_class]
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
        
        # Sync admin state
        if hasattr(frame, "on_admin_state_change"):
            frame.on_admin_state_change(self.is_admin)

        if hasattr(frame, "on_theme_change"):
            frame.on_theme_change(self.appearance_mode_optionemenu.get())
            
        if hasattr(frame, "refresh"):
            frame.refresh()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        for frame in self.frames.values():
            if hasattr(frame, "on_theme_change"):
                frame.on_theme_change(new_appearance_mode)

    def show_dashboard(self): self.show_frame(DashboardFrame, 0)
    def show_vaccines(self): self.show_frame(VaccinesFrame, 1)
    def show_orders(self): self.show_frame(OrdersFrame, 2)
    def show_dispatch(self): self.show_frame(DispatchFrame, 3)
    def show_reports(self): self.show_frame(ReportsFrame, 4)

if __name__ == "__main__":
    app = App()
    app.mainloop()
