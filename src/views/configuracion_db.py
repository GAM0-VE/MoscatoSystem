import customtkinter as ctk
from tkinter import messagebox
from src.utils.db_config import save_db_config, get_current_config

class DBConfigWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Configuración de Red (LAN)")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")
        
        # Make it a modal window
        self.transient(master)
        self.grab_set()

        self._build_layout()
        self._load_current_config()

    def _build_layout(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color="#1A1C1E", corner_radius=0)
        main_frame.pack(fill="both", expand=True)

        # Header
        ctk.CTkLabel(
            main_frame, 
            text="Conexión a Base de Datos", 
            font=("Segoe UI", 20, "bold"),
            text_color="#F4EBD0"
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            main_frame, 
            text="Configure los datos del servidor (LAN) o localhost.", 
            font=("Segoe UI", 12),
            text_color="#D6C9A8"
        ).pack(pady=(0, 20))

        # Formulario
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=30)

        # Variables
        self.host_var = ctk.StringVar()
        self.port_var = ctk.StringVar()
        self.user_var = ctk.StringVar()
        self.password_var = ctk.StringVar()
        self.db_var = ctk.StringVar()

        # Campos
        self._create_field(form_frame, "IP del Servidor (Host):", self.host_var, 0)
        self._create_field(form_frame, "Puerto:", self.port_var, 1)
        self._create_field(form_frame, "Usuario de BD:", self.user_var, 2)
        self._create_field(form_frame, "Contraseña:", self.password_var, 3, show="*")
        self._create_field(form_frame, "Nombre de BD:", self.db_var, 4)

        # Botones
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=20, padx=30)
        
        ctk.CTkButton(
            btn_frame, 
            text="Cancelar", 
            fg_color="#34393D", 
            hover_color="#4A5258",
            command=self.destroy,
            width=120
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            btn_frame, 
            text="Guardar Configuración", 
            fg_color="#8C1A11", 
            hover_color="#A1241A",
            command=self._save_config
        ).pack(side="right", fill="x", expand=True)

    def _create_field(self, parent, label_text, variable, row, show=""):
        ctk.CTkLabel(
            parent, 
            text=label_text, 
            font=("Segoe UI", 12, "bold"),
            text_color="#F4EBD0"
        ).grid(row=row*2, column=0, sticky="w", pady=(10, 2))
        
        entry = ctk.CTkEntry(
            parent, 
            textvariable=variable, 
            show=show,
            fg_color="#151719", 
            border_color="#35393D", 
            text_color="#F4EBD0",
            width=390,
            height=32
        )
        entry.grid(row=row*2+1, column=0, sticky="ew")

    def _load_current_config(self):
        config = get_current_config()
        self.host_var.set(config["host"])
        self.port_var.set(config["port"])
        self.user_var.set(config["user"])
        self.password_var.set(config["password"])
        self.db_var.set(config["database"])

    def _save_config(self):
        host = self.host_var.get().strip()
        port = self.port_var.get().strip()
        user = self.user_var.get().strip()
        password = self.password_var.get().strip()
        db = self.db_var.get().strip()

        if not host or not port or not user or not db:
            messagebox.showwarning("Campos Requeridos", "Por favor complete todos los campos (la contraseña puede estar vacía).", parent=self)
            return

        success, msg = save_db_config(host, port, user, password, db)
        if success:
            messagebox.showinfo("Éxito", "Configuración guardada correctamente.\nLa aplicación usará esta conexión de ahora en adelante.", parent=self)
            self.destroy()
        else:
            messagebox.showerror("Error", msg, parent=self)
