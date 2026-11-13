import platform
platform.win32_ver = lambda *args, **kwargs: ("10", "10.0.0", "", "")
import os
import logging
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk
import mysql.connector
from mysql.connector import Error

# Re-importando config LAN que se habia perdido
from src.utils.db_config import load_db_config
from src.views.configuracion_db import DBConfigWindow

from src.controllers.cocina.controlador_cocina import ControladorCocina
from src.controllers.admin.controlador_admin import ControladorAdmin
from src.models.cocina.modelo_cocina import ModeloCocina
from src.views.cocina.vista_cocina import CocinaDesignWindow
from src.views.admin.vista_admin import UnifiedDashboardWindow
from src.views.pedidos.vista_mesero import MeseroDesignWindow

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class DatabaseConnection:
    def __init__(self) -> None:
        self.config = {
            "host": os.getenv("DB_HOST", "127.0.0.1"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_NAME", "moscato_db"),
            "autocommit": True,
            "connection_timeout": 4,
        }

    def connect(self):
        try:
            return mysql.connector.connect(**self.config)
        except Error as exc:
            raise ConnectionError(f"No fue posible conectar a MySQL: {exc}") from exc


class MoscatoApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Restaurante Moscato - Inicio de Sesión")
        self.geometry("900x600")
        self.minsize(800, 500)
        self.configure(fg_color="#0D0D0D")
        
        # Cargar icono de la ventana
        import sys
        from src.utils.paths import get_project_root
        try:
            if getattr(sys, 'frozen', False):
                icon_path = os.path.join(sys._MEIPASS, "moscato_logo.ico")
            else:
                icon_path = os.path.join(get_project_root(), "moscato_logo.ico")
                
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            logging.warning(f"No se pudo cargar el icono: {e}")

        # Se carga la configuracion de base de datos desde db_config.json
        load_db_config()
        self.db = DatabaseConnection()
        self._build_layout()

    def _build_layout(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        container = ctk.CTkFrame(self, fg_color="#0D0D0D", corner_radius=0)
        self.login_container = container
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        glow_1 = ctk.CTkFrame(container, fg_color="#100505", corner_radius=30, width=730, height=580)
        glow_1.grid(row=0, column=0)
        glow_1.grid_propagate(False)
        glow_1.grid_columnconfigure(0, weight=1)
        glow_1.grid_rowconfigure(0, weight=1)

        glow_2 = ctk.CTkFrame(glow_1, fg_color="#180608", corner_radius=24, width=690, height=540)
        glow_2.grid(row=0, column=0)
        glow_2.grid_propagate(False)
        glow_2.grid_columnconfigure(0, weight=1)
        glow_2.grid_rowconfigure(0, weight=1)

        glow_3 = ctk.CTkFrame(glow_2, fg_color="#22080A", corner_radius=20, width=660, height=510)
        glow_3.grid(row=0, column=0)
        glow_3.grid_propagate(False)
        glow_3.grid_columnconfigure(0, weight=1)
        glow_3.grid_rowconfigure(0, weight=1)

        card = ctk.CTkFrame(
            glow_3,
            fg_color="#121212",
            border_width=1,
            border_color="#3A0A0F",
            corner_radius=16,
            width=650,
            height=500,
        )
        card.grid(row=0, column=0)
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)
        # Hacemos que la fila justo antes de la barra de estado se expanda
        card.grid_rowconfigure(5, weight=1)
        
        icon_frame = ctk.CTkFrame(card, fg_color="#240A0D", corner_radius=12, width=48, height=48)
        icon_frame.grid(row=0, column=0, pady=(36, 12))
        icon_frame.grid_propagate(False)
        icon_frame.grid_columnconfigure(0, weight=1)
        icon_frame.grid_rowconfigure(0, weight=1)
        ctk.CTkLabel(icon_frame, text="🍴", font=("Segoe UI", 24), text_color="#E50914").grid(row=0, column=0)

        ctk.CTkLabel(
            card,
            text="Restaurante Moscato",
            text_color="#FFFFFF",
            font=("Segoe UI", 32, "bold"),
        ).grid(row=1, column=0, pady=(0, 4))
        
        ctk.CTkLabel(
            card,
            text="Sistema de gestión de pedidos • Acceso de personal",
            text_color="#808080",
            font=("Segoe UI", 13),
        ).grid(row=2, column=0, pady=(0, 32))

        form_frame = ctk.CTkFrame(card, fg_color="transparent")
        form_frame.grid(row=3, column=0, padx=80, sticky="ew")
        form_frame.grid_columnconfigure(0, weight=1)

        user_labels = ctk.CTkFrame(form_frame, fg_color="transparent")
        user_labels.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        user_labels.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(user_labels, text="Usuario o identificador", text_color="#E0E0E0", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(user_labels, text="ID / Nick", text_color="#606060", font=("Segoe UI", 11)).grid(row=0, column=1, sticky="e")

        self.username_var = tk.StringVar()
        self.username_entry = ctk.CTkEntry(
            form_frame,
            textvariable=self.username_var,
            height=48,
            fg_color="#0D0D0D",
            border_color="#2A2A2A",
            text_color="#FFFFFF",
            placeholder_text="👤 admin",
            placeholder_text_color="#606060",
            font=("Segoe UI", 14),
            corner_radius=8
        )
        self.username_entry.grid(row=1, column=0, sticky="ew", pady=(0, 20))

        pass_labels = ctk.CTkFrame(form_frame, fg_color="transparent")
        pass_labels.grid(row=2, column=0, sticky="ew", pady=(0, 6))
        pass_labels.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(pass_labels, text="Contraseña", text_color="#E0E0E0", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(pass_labels, text="Teclado numérico", text_color="#606060", font=("Segoe UI", 11)).grid(row=0, column=1, sticky="e")

        self.password_var = tk.StringVar()
        self.password_var.trace_add("write", self._validate_password)

        self.password_entry = ctk.CTkEntry(
            form_frame,
            textvariable=self.password_var,
            show="•",
            height=48,
            fg_color="#0D0D0D",
            border_color="#2A2A2A",
            text_color="#FFFFFF",
            placeholder_text="🔒 ••••",
            placeholder_text_color="#606060",
            font=("Segoe UI", 14),
            corner_radius=8
        )
        self.password_entry.grid(row=3, column=0, sticky="ew", pady=(0, 4))

        self.password_warning_label = ctk.CTkLabel(
            form_frame,
            text="",
            text_color="#D91627",
            font=("Segoe UI", 11, "bold")
        )
        self.password_warning_label.grid(row=4, column=0, sticky="w", pady=(0, 16))

        self.login_btn = ctk.CTkButton(
            form_frame,
            text="Iniciar sesión  →   [ENTER]",
            fg_color="#D91627",
            hover_color="#B0121F",
            text_color="#FFFFFF",
            font=("Segoe UI", 15, "bold"),
            height=50,
            corner_radius=8,
            command=self._attempt_login,
        )
        self.login_btn.grid(row=5, column=0, sticky="ew")

        status_frame = ctk.CTkFrame(card, fg_color="#151515", corner_radius=0, height=44)
        status_frame.grid(row=6, column=0, sticky="sew")
        status_frame.grid_columnconfigure(1, weight=1)
        status_frame.grid_propagate(False)

        left_status = ctk.CTkFrame(status_frame, fg_color="transparent")
        left_status.grid(row=0, column=0, sticky="w", padx=20, pady=10)
        ctk.CTkLabel(left_status, text="●", text_color="#10B981", font=("Segoe UI", 10)).grid(row=0, column=0, padx=(0, 6))
        self.status_var = tk.StringVar(value="Listo para autenticar")
        ctk.CTkLabel(left_status, textvariable=self.status_var, text_color="#A0A0A0", font=("Segoe UI", 11)).grid(row=0, column=1)

        # Boton LAN Config Flotante
        btn_lan = ctk.CTkButton(
            self.login_container, 
            text="⚙️", 
            fg_color="transparent", 
            hover_color="#1A1A1A", 
            text_color="#606060", 
            font=("Segoe UI", 20), 
            width=40,
            height=40,
            corner_radius=20,
            command=self._open_db_config
        )
        btn_lan.place(relx=0.98, rely=0.97, anchor="se")

        self.bind("<Return>", lambda _event: self._attempt_login())
        self.username_entry.bind("<KeyRelease>", self._validate_password)
        self.username_entry.bind("<FocusIn>", self._validate_password)
        self.password_entry.bind("<KeyRelease>", self._validate_password)
        self.password_entry.bind("<FocusIn>", self._validate_password)
        
        self.username_entry.focus_set()

    def _open_db_config(self) -> None:
        DBConfigWindow(self)

    def _validate_password(self, *args) -> None:
        warnings = []
        caps_on = False
        try:
            import ctypes
            hllDll = ctypes.WinDLL("User32.dll")
            caps_on = hllDll.GetKeyState(0x14) & 1
        except Exception:
            pass
            
        if caps_on:
            warnings.append("Bloq Mayús Activado")

        val = self.password_var.get()
        if val and not val.isdigit():
            warnings.append("La contraseña es solo numérica")
            clean_val = "".join(c for c in val if c.isdigit())
            self.password_var.set(clean_val)
            
        if warnings:
            self.password_warning_label.configure(text="⚠️ " + " | ".join(warnings))
        else:
            self.password_warning_label.configure(text="")

    def _attempt_login(self) -> None:
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showwarning("Campos requeridos", "Debe ingresar usuario y contraseña.")
            return

        self.status_var.set("Verificando credenciales...")
        self.update_idletasks()

        # Recargar configuración antes de conectar para asegurar usar LAN
        self.db.config["host"] = os.getenv("DB_HOST", "127.0.0.1")
        self.db.config["port"] = int(os.getenv("DB_PORT", "3306"))
        self.db.config["user"] = os.getenv("DB_USER", "root")
        self.db.config["password"] = os.getenv("DB_PASSWORD", "")
        self.db.config["database"] = os.getenv("DB_NAME", "moscato_db")

        try:
            connection = self.db.connect()
            try:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        "SELECT u.id_usuario, e.nombres as nombre, u.username, u.rol "
                        "FROM usuarios u "
                        "LEFT JOIN empleados e ON u.id_empleado = e.id_empleado "
                        "WHERE u.username = %s AND u.password = %s AND u.activo = 1",
                        (username, password),
                    )
                    user = cursor.fetchone()
            finally:
                connection.close()

            if not user:
                self.status_var.set("Credenciales invalidas")
                messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")
                return

            self.status_var.set(f"Sesion iniciada: {user['nombre']} ({user['rol']})")
            self._open_dashboard(user)

        except ConnectionError as exc:
            self.status_var.set("Error de conexion")
            messagebox.showerror("Base de datos", str(exc))
        except Error as exc:
            self.status_var.set("Error en autenticación")
            messagebox.showerror("Error", f"No se pudo validar el usuario: {exc}")

    def show_login(self) -> None:
        for child in self.winfo_children():
            if child != self.login_container:
                child.destroy()
        self.password_var.set("")
        self.login_container.grid(row=0, column=0, sticky="nsew")
        self.username_entry.focus_set()

    def _open_dashboard(self, user: dict) -> None:
        self.login_container.grid_remove()
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        rol = str(user.get("rol", "")).strip().lower()
        nombre_real = str(user.get("nombre", "")).strip()
        id_usuario = user.get("id_usuario")

        try:
            from src.models.auditoria.auditoria_model import AuditoriaModel
            am = AuditoriaModel()
            am.registrar_accion(id_usuario, "LOGIN", "usuarios", f"Inicio de sesión exitoso ({rol})")
        except Exception:
            pass

        if rol == "administrador":
            vista = UnifiedDashboardWindow(self, usuario=nombre_real, id_usuario=id_usuario)
            vista.grid(row=0, column=0, sticky="nsew")
            self.update_idletasks()
            ControladorAdmin(vista)
        elif rol == "cocinero":
            modelo = ModeloCocina()
            vista = CocinaDesignWindow(self, usuario=nombre_real)
            vista.grid(row=0, column=0, sticky="nsew")
            controlador = ControladorCocina(vista, modelo)
            vista.controlador = controlador
            controlador.actualizar_pantalla()
        else:
            vista = MeseroDesignWindow(self, usuario=nombre_real)
            vista.grid(row=0, column=0, sticky="nsew")

