import customtkinter as ctk
import os
import shutil
from tkinter import filedialog

from src.controllers.auditoria.auditoria_controller import AuditoriaController
from src.models.auditoria.auditoria_model import AuditoriaModel
from src.views.auditoria.auditoria_view import AuditoriaView

from src.models.pedidos.modelo_analisis import AnalisisModel
from src.views.pedidos.vista_analisis import AnalisisView
from src.controllers.pedidos.controlador_analisis import AnalisisController

from src.models.pedidos.modelo_registro_pedidos import RegistroPedidosModel
from src.views.pedidos.vista_registro_pedidos import RegistroPedidosView
from src.controllers.pedidos.controlador_registro_pedidos import RegistroPedidosController

from src.models.mesas.admin_mesas_model import AdminMesasModel
from src.views.mesas.admin_mesas_view import AdminMesasView
from src.controllers.mesas.admin_mesas_controller import AdminMesasController

class UnifiedDashboardWindow(ctk.CTkFrame):
    """Vista del panel unificado de administracion (solo UI y eventos)."""

    COLORS = {
        "primary": "#8C1A11",
        "secondary": "#F4EBD0",
        "tertiary": "#1A1C1E",
        "neutral": "#867370",
        "window": "#1A1C1E",
        "sidebar": "#171113",
        "card": "#231719",
        "profile_card": "#2A1B1E",
        "accent": "#8C1A11",
        "accent_hover": "#A1241A",
        "accent_soft": "#DFA99D",
        "wine_bg": "#1A1C1E",
        "wine_panel": "#231719",
        "wine_soft": "#2D1E21",
        "text_primary": "#F4EBD0",
        "text_secondary": "#867370",
        "text_warm": "#D8CDB2",
        "success": "#2EA44F",
        "muted": "#867370",
        "line": "#3A2A2D",
        "header_dark": "#1A1C1E",
        "table_row_a": "#281B1E",
        "table_row_b": "#24181B",
        "panel_border": "#4A3134",
        "chip_bg": "#3A2427",
        "chip_fg": "#F4EBD0",
        "hover_subtle": "#2B181A",
        "hover_surface": "#2F2023",
        "soft_hover": "#E8BBB2",
        "scroll_btn": "#5F3134",
        "scroll_btn_hover": "#754046",
        "role_cook_bg": "#2A2D31",
        "role_default_bg": "#2B2D31",
        "edit_hover": "#514044",
    }

    FONT = "Segoe UI"

    def __init__(self, parent, usuario: str, controller=None, id_usuario: int | None = None, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.usuario = usuario
        self.id_usuario = id_usuario
        self.controller = controller

        self.configure(fg_color=self.COLORS["wine_bg"])

        self._rows = []

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._show_registro_pedidos()

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=236,
            fg_color=self.COLORS["sidebar"],
            corner_radius=0,
            border_width=1,
            border_color=self.COLORS["panel_border"],
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_columnconfigure(0, weight=1)
        self.sidebar.grid_rowconfigure(4, weight=1)

        profile_name = ctk.CTkLabel(
            self.sidebar,
            text="Moscato Admin",
            font=(self.FONT, 17, "bold"),
            text_color=self.COLORS["text_primary"],
            fg_color=self.COLORS["accent"],
            corner_radius=8,
            padx=12,
            pady=7,
            anchor="center",
        )
        profile_name.grid(row=0, column=0, pady=(18, 16))

        nav_wrap = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_wrap.grid(row=1, column=0, sticky="ew", padx=12)
        nav_wrap.grid_columnconfigure(0, weight=1)

        self.nav_buttons = {}
        nav_items = [
            ("registro_pedidos", "Registro de Pedidos", True, self._show_registro_pedidos),
            ("orders", "Análisis de Producto", False, self._show_analisis),
            ("kitchen", "Auditoría de Sistema", False, self._show_auditoria),
            ("categories", "Gestion de Menu", False, self._show_menu),
            ("users", "Gestion de Usuarios", False, self._show_users),
            ("mesas", "Gestión de Mesas", False, self._show_mesas),
        ]

        for idx, (key, text, active, command) in enumerate(nav_items):
            btn = ctk.CTkButton(
                nav_wrap,
                text=text,
                height=38,
                corner_radius=6,
                anchor="w",
                font=(self.FONT, 12, "bold" if active else "normal"),
                fg_color=self.COLORS["accent"] if active else "transparent",
                hover_color=self.COLORS["accent_hover"] if active else self.COLORS["hover_subtle"],
                text_color=self.COLORS["text_primary"] if active else self.COLORS["text_warm"],
                border_width=1 if not active else 0,
                border_color=self.COLORS["panel_border"],
                command=command,
            )
            btn.grid(row=idx, column=0, sticky="ew", pady=5)
            self.nav_buttons[key] = btn

        footer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        footer.grid(row=5, column=0, sticky="ew", padx=12, pady=(8, 16))
        footer.grid_columnconfigure(0, weight=1)


        logout_btn = ctk.CTkButton(
            footer,
            text="Cerrar Sesión",
            height=38,
            corner_radius=10,
            fg_color="transparent",
            hover_color=self.COLORS["hover_surface"],
            text_color=self.COLORS["text_secondary"],
            border_width=1,
            border_color=self.COLORS["panel_border"],
            font=(self.FONT, 12),
            command=self._logout_to_login,
        )
        logout_btn.grid(row=1, column=0, sticky="ew")

    def _activate_nav(self, key: str) -> None:
        for button_key, button in self.nav_buttons.items():
            active = button_key == key
            button.configure(
                fg_color=self.COLORS["accent"] if active else "transparent",
                hover_color=self.COLORS["accent_hover"] if active else self.COLORS["hover_subtle"],
                font=(self.FONT, 12, "bold" if active else "normal"),
                text_color=self.COLORS["text_primary"] if active else self.COLORS["text_warm"],
                border_width=0 if active else 1,
            )

    def _replace_main_panel(self) -> None:
        if hasattr(self, "main_panel") and self.main_panel.winfo_exists():
            self.main_panel.destroy()

    def _show_menu(self) -> None:
        self._activate_nav("categories")
        self._replace_main_panel()
        self._build_menu_panel()
        if self.controller and hasattr(self.controller, "cargar_menu"):
            self.after(150, self.controller.cargar_menu)

    def _show_users(self) -> None:
        self._activate_nav("users")
        self._replace_main_panel()
        self._build_main_panel()
        if self.controller and hasattr(self.controller, "cargar_empleados"):
            self.after(150, self.controller.cargar_empleados)

    def _show_auditoria(self) -> None:
        self._activate_nav("kitchen")
        self._replace_main_panel()
        self._build_auditoria_panel()

    def _show_registro_pedidos(self) -> None:
        self._activate_nav("registro_pedidos")
        self._replace_main_panel()
        self._build_registro_pedidos_panel()

    def _show_analisis(self) -> None:
        self._activate_nav("orders")
        self._replace_main_panel()
        self._build_analisis_panel()

    def _show_mesas(self) -> None:
        self._activate_nav("mesas")
        self._replace_main_panel()
        self._build_mesas_panel()

    def _build_mesas_panel(self):
        self.main_panel = ctk.CTkFrame(self, fg_color=self.COLORS["wine_bg"], corner_radius=0)
        self.main_panel.grid(row=0, column=1, sticky="nsew")
        self.main_panel.grid_columnconfigure(0, weight=1)
        self.main_panel.grid_rowconfigure(0, weight=1)

        panel = ctk.CTkFrame(self.main_panel, fg_color="transparent")
        panel.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(0, weight=1)

        vista_mesas = AdminMesasView(panel)
        modelo_mesas = AdminMesasModel()
        self.current_panel_controller = AdminMesasController(modelo_mesas, vista_mesas)

    def _build_registro_pedidos_panel(self):
        self.main_panel = ctk.CTkFrame(self, fg_color=self.COLORS["wine_bg"], corner_radius=0)
        self.main_panel.grid(row=0, column=1, sticky="nsew")
        self.main_panel.grid_columnconfigure(0, weight=1)
        self.main_panel.grid_rowconfigure(0, weight=1)

        panel = ctk.CTkFrame(self.main_panel, fg_color="transparent")
        panel.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(0, weight=1)

        vista = RegistroPedidosView(panel)
        modelo = RegistroPedidosModel()
        self.current_panel_controller = RegistroPedidosController(modelo, vista)

    def _build_analisis_panel(self):
        self.main_panel = ctk.CTkFrame(self, fg_color=self.COLORS["wine_bg"], corner_radius=0)
        self.main_panel.grid(row=0, column=1, sticky="nsew")
        self.main_panel.grid_columnconfigure(0, weight=1)
        self.main_panel.grid_rowconfigure(0, weight=1)

        panel = ctk.CTkFrame(self.main_panel, fg_color="transparent")
        panel.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(0, weight=1)

        vista_analisis = AnalisisView(panel)
        modelo_analisis = AnalisisModel()
        self.current_panel_controller = AnalisisController(modelo_analisis, vista_analisis)

    def _build_auditoria_panel(self):
        self.main_panel = ctk.CTkFrame(self, fg_color=self.COLORS["wine_bg"], corner_radius=0)
        self.main_panel.grid(row=0, column=1, sticky="nsew")
        self.main_panel.grid_columnconfigure(0, weight=1)
        self.main_panel.grid_rowconfigure(0, weight=1)

        panel = ctk.CTkFrame(self.main_panel, fg_color="transparent")
        panel.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(0, weight=1)

        vista_auditoria = AuditoriaView(panel)
        modelo_auditoria = AuditoriaModel()
        self.current_panel_controller = AuditoriaController(modelo_auditoria, vista_auditoria)

    def _build_menu_panel(self):
        self.main_panel = ctk.CTkFrame(self, fg_color=self.COLORS["wine_bg"], corner_radius=0)
        self.main_panel.grid(row=0, column=1, sticky="nsew")
        self.main_panel.grid_columnconfigure(0, weight=1)
        self.main_panel.grid_rowconfigure(2, weight=1)

        top_bar = ctk.CTkFrame(self.main_panel, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=(14, 8))
        top_bar.grid_columnconfigure(0, weight=1)
        self.menu_search_entry = ctk.CTkEntry(
            top_bar, height=34, placeholder_text="Buscar plato por nombre o categoria...",
            fg_color=self.COLORS["wine_panel"], border_color=self.COLORS["panel_border"],
            text_color=self.COLORS["text_primary"], placeholder_text_color=self.COLORS["text_secondary"],
            corner_radius=6, font=(self.FONT, 12),
        )
        self.menu_search_entry.grid(row=0, column=0, sticky="ew")
        self.menu_search_entry.bind("<KeyRelease>", lambda _event: self._on_menu_search_changed())

        header = ctk.CTkFrame(self.main_panel, fg_color="transparent")
        header.grid(row=1, column=0, sticky="ew", padx=20, pady=(2, 10))
        header.grid_columnconfigure(0, weight=1)
        title_block = ctk.CTkFrame(header, fg_color="transparent")
        title_block.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(title_block, text="Gestion de Menu", font=(self.FONT, 30, "bold"), text_color=self.COLORS["text_primary"], anchor="w").grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(title_block, text="Administra los platos, precios y disponibilidad en tiempo real.", font=(self.FONT, 12), text_color=self.COLORS["neutral"], anchor="w").grid(row=1, column=0, sticky="w", pady=(2, 0))
        ctk.CTkButton(header, text="+ Nuevo Plato", width=140, height=36, corner_radius=6, fg_color=self.COLORS["accent_soft"], hover_color=self.COLORS["soft_hover"], text_color=self.COLORS["tertiary"], font=(self.FONT, 12, "bold"), command=self._on_add_product_clicked).grid(row=0, column=1, sticky="e")

        body = ctk.CTkFrame(self.main_panel, fg_color="transparent")
        body.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 14))
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(0, weight=1)
        self.menu_card = ctk.CTkFrame(body, fg_color=self.COLORS["wine_panel"], corner_radius=8, border_width=1, border_color=self.COLORS["panel_border"])
        self.menu_card.grid(row=0, column=0, sticky="nsew")
        self.menu_card.grid_columnconfigure(0, weight=1)
        self.menu_card.grid_rowconfigure(2, weight=1)
        ctk.CTkLabel(self.menu_card, text="Carta Actual", font=(self.FONT, 20, "bold"), text_color=self.COLORS["text_primary"], anchor="w").grid(row=0, column=0, sticky="w", padx=16, pady=(14, 8))
        self.menu_headers = ctk.CTkFrame(self.menu_card, fg_color=self.COLORS["wine_soft"], corner_radius=6)
        self.menu_headers.grid(row=1, column=0, sticky="ew", padx=12)
        for col, weight in enumerate((4, 3, 2, 2, 3)):
            self.menu_headers.grid_columnconfigure(col, weight=weight, uniform="menu_columns", minsize=(260, 170, 110, 120, 190)[col])
        for col, text in enumerate(("PLATO / DESCRIPCION", "CATEGORIA", "PRECIO", "ESTADO", "ACCIONES")):
            ctk.CTkLabel(self.menu_headers, text=text, font=(self.FONT, 10, "bold"), text_color=self.COLORS["text_warm"], anchor="w").grid(row=0, column=col, sticky="ew", padx=10, pady=8)
        self.menu_scroll = ctk.CTkScrollableFrame(self.menu_card, fg_color="transparent", corner_radius=0, scrollbar_button_color=self.COLORS["scroll_btn"], scrollbar_button_hover_color=self.COLORS["scroll_btn_hover"])
        self.menu_scroll.grid(row=2, column=0, sticky="nsew", padx=8, pady=(8, 12))
        for col, weight in enumerate((4, 3, 2, 2, 3)):
            self.menu_scroll.grid_columnconfigure(col, weight=weight, uniform="menu_columns", minsize=(260, 170, 110, 120, 190)[col])

    def _logout_to_login(self) -> None:
        if hasattr(self.parent, "show_login"):
            self.parent.show_login()
        else:
            self.destroy()

    def _build_main_panel(self):
        self.main_panel = ctk.CTkFrame(self, fg_color=self.COLORS["wine_bg"], corner_radius=0)
        self.main_panel.grid(row=0, column=1, sticky="nsew")
        self.main_panel.grid_columnconfigure(0, weight=1)
        self.main_panel.grid_rowconfigure(2, weight=1)

        top_bar = ctk.CTkFrame(self.main_panel, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=(14, 8))
        top_bar.grid_columnconfigure(0, weight=1)
        top_bar.grid_columnconfigure(1, weight=0)
        top_bar.grid_columnconfigure(2, weight=0)

        self.search_entry = ctk.CTkEntry(
            top_bar,
            height=34,
            placeholder_text="Buscar personal por nombre o rol...",
            fg_color=self.COLORS["wine_panel"],
            border_color=self.COLORS["panel_border"],
            text_color=self.COLORS["text_primary"],
            placeholder_text_color=self.COLORS["text_secondary"],
            corner_radius=6,
            font=(self.FONT, 12),
        )
        self.search_entry.grid(row=0, column=0, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self._on_search_changed)


        header = ctk.CTkFrame(self.main_panel, fg_color="transparent")
        header.grid(row=1, column=0, sticky="ew", padx=20, pady=(2, 10))
        header.grid_columnconfigure(0, weight=1)

        title_block = ctk.CTkFrame(header, fg_color="transparent")
        title_block.grid(row=0, column=0, sticky="w")

        title = ctk.CTkLabel(
            title_block,
            text="Gestion de Usuarios",
            font=(self.FONT, 34, "bold"),
            text_color=self.COLORS["text_primary"],
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="w")

        subtitle = ctk.CTkLabel(
            title_block,
            text="Administra el personal, roles y estado de fichaje en tiempo real.",
            font=(self.FONT, 12),
            text_color=self.COLORS["neutral"],
            anchor="w",
        )
        subtitle.grid(row=1, column=0, sticky="w", pady=(2, 0))

        add_btn = ctk.CTkButton(
            header,
            text="+ Nuevo Empleado",
            width=170,
            height=36,
            corner_radius=6,
            fg_color=self.COLORS["accent_soft"],
            hover_color=self.COLORS["soft_hover"],
            text_color=self.COLORS["tertiary"],
            font=(self.FONT, 12, "bold"),
            command=self._on_add_clicked,
        )
        add_btn.grid(row=0, column=1, sticky="e")

        body = ctk.CTkFrame(self.main_panel, fg_color="transparent")
        body.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 14))
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(0, weight=1)

        directory_card = ctk.CTkFrame(
            body,
            fg_color=self.COLORS["wine_panel"],
            corner_radius=8,
            border_width=1,
            border_color=self.COLORS["panel_border"],
        )
        directory_card.grid(row=0, column=0, sticky="nsew")
        directory_card.grid_columnconfigure(0, weight=1)
        directory_card.grid_rowconfigure(2, weight=1)

        directory_title = ctk.CTkLabel(
            directory_card,
            text="Directorio de Personal",
            font=(self.FONT, 26, "bold"),
            text_color=self.COLORS["text_primary"],
            anchor="w",
        )
        directory_title.grid(row=0, column=0, sticky="w", padx=16, pady=(14, 8))

        headers_frame = ctk.CTkFrame(directory_card, fg_color=self.COLORS["wine_soft"], corner_radius=6)
        headers_frame.grid(row=1, column=0, sticky="ew", padx=12)
        for col, weight in enumerate((3, 2, 2, 3, 2)):
            headers_frame.grid_columnconfigure(col, weight=weight, uniform="user_columns", minsize=(260, 150, 145, 180, 180)[col])

        header_labels = ["EMPLEADO", "ROL", "ESTADO", "ULTIMO ACCESO", "ACCIONES"]
        for col, text in enumerate(header_labels):
            h = ctk.CTkLabel(
                headers_frame,
                text=text,
                font=(self.FONT, 10, "bold"),
                text_color=self.COLORS["text_warm"],
                anchor="w" if col != 4 else "center",
            )
            h.grid(row=0, column=col, sticky="ew", padx=12, pady=8)

        self.table_scroll = ctk.CTkScrollableFrame(
            directory_card,
            fg_color="transparent",
            corner_radius=0,
            scrollbar_button_color=self.COLORS["scroll_btn"],
            scrollbar_button_hover_color=self.COLORS["scroll_btn_hover"],
        )
        self.table_scroll.grid(row=2, column=0, sticky="nsew", padx=8, pady=(8, 12))
        for col, weight in enumerate((3, 2, 2, 3, 2)):
            self.table_scroll.grid_columnconfigure(col, weight=weight, uniform="user_columns", minsize=(260, 150, 145, 180, 180)[col])

        permissions = ctk.CTkFrame(self.main_panel, fg_color="transparent")
        permissions.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 16))
        permissions.grid_columnconfigure((0, 1, 2), weight=1)

        cards = [
            (
                "Administrador",
                ["✓ Gestion total del sistema", "✓ Control de usuarios y auditoria", "✓ Acceso a reportes globales"],
            ),
            (
                "Mesero",
                ["✓ Toma y edicion de pedidos", "✓ Consulta de estado de mesas", "✓ Seguimiento de cocina"],
            ),
            (
                "Cocinero",
                ["✓ Gestion de ordenes en cola", "✓ Actualizacion de estado de platos", "✓ Vista de prioridades"],
            ),
        ]

        for idx, (role, items) in enumerate(cards):
            card = ctk.CTkFrame(
                permissions,
                fg_color=self.COLORS["wine_panel"],
                corner_radius=8,
                border_width=1,
                border_color=self.COLORS["panel_border"],
            )
            card.grid(row=0, column=idx, sticky="ew", padx=(0 if idx == 0 else 6, 0 if idx == 2 else 6), pady=(8, 0))
            card.grid_columnconfigure(0, weight=1)

            role_title = ctk.CTkLabel(
                card,
                text=role,
                font=(self.FONT, 14, "bold"),
                text_color=self.COLORS["text_primary"],
                anchor="w",
            )
            role_title.grid(row=0, column=0, sticky="w", padx=12, pady=(10, 6))

            for line_idx, item in enumerate(items, start=1):
                entry = ctk.CTkLabel(
                    card,
                    text=item,
                    font=(self.FONT, 11),
                    text_color=self.COLORS["success"],
                    anchor="w",
                )
                entry.grid(row=line_idx, column=0, sticky="w", padx=12, pady=2)

            ctk.CTkLabel(card, text="", height=6).grid(row=len(items) + 1, column=0)

    def render_menu(self, productos_list):
        if not hasattr(self, "menu_scroll") or not self.menu_scroll.winfo_exists():
            return
        for widget in self.menu_scroll.winfo_children():
            widget.destroy()
        productos = productos_list or []
        if not productos:
            ctk.CTkLabel(self.menu_scroll, text="No hay platos para mostrar.", font=(self.FONT, 13), text_color=self.COLORS["text_secondary"]).grid(row=0, column=0, columnspan=5, pady=24)
            return
        for row_idx, producto in enumerate(productos):
            row_bg = self.COLORS["table_row_a"] if row_idx % 2 == 0 else self.COLORS["table_row_b"]
            row = ctk.CTkFrame(self.menu_scroll, fg_color=row_bg, corner_radius=6, border_width=1, border_color=self.COLORS["panel_border"])
            row.grid(row=row_idx, column=0, columnspan=5, sticky="ew", padx=4, pady=4)
            for col, weight in enumerate((4, 3, 2, 2, 3)):
                row.grid_columnconfigure(col, weight=weight, uniform="menu_row_columns", minsize=(260, 170, 110, 120, 190)[col])
            info = ctk.CTkFrame(row, fg_color="transparent")
            info.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
            ctk.CTkLabel(info, text=str(producto.get("name", "-")), font=(self.FONT, 12, "bold"), text_color=self.COLORS["text_primary"], anchor="w").grid(row=0, column=0, sticky="w")
            ctk.CTkLabel(info, text=str(producto.get("description", ""))[:58], font=(self.FONT, 10), text_color=self.COLORS["neutral"], anchor="w").grid(row=1, column=0, sticky="ew")
            ctk.CTkLabel(row, text=str(producto.get("category", "Sin categoria")), fg_color=self.COLORS["chip_bg"], text_color=self.COLORS["chip_fg"], corner_radius=12, padx=8, pady=3, font=(self.FONT, 10, "bold")).grid(row=0, column=1, sticky="w", padx=10)
            price_str = f"${int(float(producto.get('price', 0))):,}".replace(',', '.')
            ctk.CTkLabel(row, text=price_str, font=(self.FONT, 11, "bold"), text_color=self.COLORS["text_primary"], anchor="w").grid(row=0, column=2, sticky="w", padx=10)
            disponible = bool(producto.get("available", False))
            ctk.CTkLabel(row, text="● Disponible" if disponible else "● Agotado", font=(self.FONT, 10, "bold"), text_color=self.COLORS["success"] if disponible else self.COLORS["accent_soft"], anchor="w").grid(row=0, column=3, sticky="w", padx=10)
            actions = ctk.CTkFrame(row, fg_color="transparent")
            actions.grid(row=0, column=4, sticky="w", padx=8)
            product_id = producto.get("id")
            ctk.CTkButton(actions, text="Editar", width=58, height=28, corner_radius=6, fg_color=self.COLORS["chip_bg"], hover_color=self.COLORS["edit_hover"], text_color=self.COLORS["text_primary"], font=(self.FONT, 10), command=lambda pid=product_id: self._on_edit_product_clicked(pid)).grid(row=0, column=0, padx=(0, 4))
            ctk.CTkButton(actions, text="Activo" if disponible else "Agotado", width=62, height=28, corner_radius=6, fg_color=self.COLORS["accent"], hover_color=self.COLORS["accent_hover"], text_color=self.COLORS["secondary"], font=(self.FONT, 10), command=lambda pid=product_id: self._on_toggle_product_clicked(pid)).grid(row=0, column=1, padx=(0, 4))
            ctk.CTkButton(actions, text="Quitar", width=52, height=28, corner_radius=6, fg_color=self.COLORS["primary"], hover_color=self.COLORS["accent_hover"], text_color=self.COLORS["secondary"], font=(self.FONT, 10), command=lambda pid=product_id: self._on_delete_product_clicked(pid)).grid(row=0, column=2)

    def get_menu_search_query(self):
        return self.menu_search_entry.get().strip()

    def open_product_form(self, producto, categorias, on_submit):
        form = ctk.CTkToplevel(self)
        form.title("Editar Plato" if producto else "Nuevo Plato")
        form.geometry("520x570")
        form.resizable(False, False)
        form.configure(fg_color=self.COLORS["wine_bg"])
        form.transient(self)
        form.grab_set()

        form.grid_columnconfigure(0, weight=1)
        content = ctk.CTkFrame(form, fg_color=self.COLORS["wine_panel"], corner_radius=8, border_width=1, border_color=self.COLORS["panel_border"])
        content.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        content.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(content, text="Editar Plato" if producto else "Nuevo Plato", font=(self.FONT, 24, "bold"), text_color=self.COLORS["text_primary"], anchor="w").grid(row=0, column=0, sticky="w", padx=20, pady=(20, 3))
        ctk.CTkLabel(content, text="Completa la informacion de la carta.", font=(self.FONT, 11), text_color=self.COLORS["neutral"], anchor="w").grid(row=1, column=0, sticky="w", padx=20, pady=(0, 18))

        def field_label(text, row):
            ctk.CTkLabel(content, text=text, font=(self.FONT, 11, "bold"), text_color=self.COLORS["text_warm"], anchor="w").grid(row=row, column=0, sticky="w", padx=20, pady=(7, 5))

        field_label("Nombre del plato", 2)
        name_entry = ctk.CTkEntry(content, height=36, fg_color=self.COLORS["wine_bg"], border_color=self.COLORS["panel_border"], text_color=self.COLORS["text_primary"], font=(self.FONT, 12))
        name_entry.grid(row=3, column=0, sticky="ew", padx=20)
        name_entry.insert(0, str((producto or {}).get("name", "")))

        field_label("Descripcion", 4)
        description_entry = ctk.CTkEntry(content, height=36, fg_color=self.COLORS["wine_bg"], border_color=self.COLORS["panel_border"], text_color=self.COLORS["text_primary"], font=(self.FONT, 12))
        description_entry.grid(row=5, column=0, sticky="ew", padx=20)
        description_entry.insert(0, str((producto or {}).get("description", "")))

        field_label("Precio", 6)
        price_entry = ctk.CTkEntry(content, height=36, fg_color=self.COLORS["wine_bg"], border_color=self.COLORS["panel_border"], text_color=self.COLORS["text_primary"], font=(self.FONT, 12), placeholder_text="Ej. 26000.00")
        price_entry.grid(row=7, column=0, sticky="ew", padx=20)
        price_entry.insert(0, str((producto or {}).get("price", "")))

        field_label("Categoria", 8)
        category_map = {str(item.get("nombre")): int(item.get("id_categoria")) for item in categorias}
        category_names = list(category_map) or ["Sin categorias disponibles"]
        selected_category = str((producto or {}).get("category", category_names[0]))
        if selected_category not in category_map:
            selected_category = category_names[0]
        category_menu = ctk.CTkOptionMenu(content, values=category_names, variable=ctk.StringVar(value=selected_category), height=36, fg_color=self.COLORS["wine_bg"], button_color=self.COLORS["accent"], button_hover_color=self.COLORS["accent_hover"], text_color=self.COLORS["text_primary"], font=(self.FONT, 12))
        category_menu.grid(row=9, column=0, sticky="ew", padx=20)

        image_path = [str((producto or {}).get("image", ""))]
        image_label = ctk.CTkLabel(content, text=os.path.basename(image_path[0]) if image_path[0] else "Sin imagen seleccionada", font=(self.FONT, 10), text_color=self.COLORS["neutral"], anchor="w")
        image_label.grid(row=11, column=0, sticky="w", padx=20, pady=(8, 0))

        def choose_image():
            selected = filedialog.askopenfilename(
                parent=form,
                title="Seleccionar foto del plato",
                filetypes=[("Imagenes", "*.png *.jpg *.jpeg *.webp"), ("Todos los archivos", "*.*")],
            )
            if selected:
                image_path[0] = self._store_menu_image(selected)
                image_label.configure(text=os.path.basename(image_path[0]))

        ctk.CTkButton(content, text="Seleccionar foto", height=32, corner_radius=6, fg_color=self.COLORS["chip_bg"], hover_color=self.COLORS["edit_hover"], text_color=self.COLORS["text_primary"], font=(self.FONT, 11, "bold"), command=choose_image).grid(row=12, column=0, sticky="w", padx=20, pady=(4, 0))

        buttons = ctk.CTkFrame(content, fg_color="transparent")
        buttons.grid(row=13, column=0, sticky="ew", padx=20, pady=(20, 20))
        buttons.grid_columnconfigure((0, 1), weight=1)

        def save():
            name = name_entry.get().strip()
            description = description_entry.get().strip()
            try:
                price = float(price_entry.get().strip().replace(",", "."))
                if price < 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Precio invalido", "Ingresa un precio numerico mayor o igual a cero.", parent=form)
                price_entry.focus_set()
                return
            if not name:
                messagebox.showwarning("Campo requerido", "Ingresa el nombre del plato.", parent=form)
                name_entry.focus_set()
                return
            if not category_map:
                messagebox.showwarning("Categoria requerida", "No hay categorias activas disponibles.", parent=form)
                return
            on_submit((name, description, price, category_map[category_menu.get()], image_path[0] or None))
            form.destroy()

        ctk.CTkButton(buttons, text="Cancelar", height=36, corner_radius=6, fg_color="transparent", hover_color=self.COLORS["hover_surface"], border_width=1, border_color=self.COLORS["panel_border"], text_color=self.COLORS["text_warm"], font=(self.FONT, 11, "bold"), command=form.destroy).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ctk.CTkButton(buttons, text="Guardar Plato", height=36, corner_radius=6, fg_color=self.COLORS["accent"], hover_color=self.COLORS["accent_hover"], text_color=self.COLORS["text_primary"], font=(self.FONT, 11, "bold"), command=save).grid(row=0, column=1, sticky="ew", padx=(6, 0))
        name_entry.focus_set()
        form.protocol("WM_DELETE_WINDOW", form.destroy)

    @staticmethod
    def _store_menu_image(source_path: str) -> str:
        from src.utils.paths import get_project_root, get_assets_dir
        project_root = get_project_root()
        target_dir = os.path.join(get_assets_dir(), "menu")
        os.makedirs(target_dir, exist_ok=True)
        filename = os.path.basename(source_path)
        stem, extension = os.path.splitext(filename)
        target_path = os.path.join(target_dir, filename)
        counter = 1
        while os.path.exists(target_path) and os.path.abspath(source_path) != os.path.abspath(target_path):
            target_path = os.path.join(target_dir, f"{stem}_{counter}{extension}")
            counter += 1
        if os.path.abspath(source_path) != os.path.abspath(target_path):
            shutil.copy2(source_path, target_path)
        return os.path.relpath(target_path, project_root).replace(os.sep, "/")

    def _on_menu_search_changed(self):
        if self.controller and hasattr(self.controller, "handle_menu_search"):
            self.controller.handle_menu_search()

    def _on_add_product_clicked(self):
        if self.controller and hasattr(self.controller, "handle_add_product"):
            self.controller.handle_add_product()

    def _on_edit_product_clicked(self, product_id):
        if self.controller and hasattr(self.controller, "handle_edit_product"):
            self.controller.handle_edit_product(product_id)

    def _on_toggle_product_clicked(self, product_id):
        if self.controller and hasattr(self.controller, "handle_toggle_product"):
            self.controller.handle_toggle_product(product_id)

    def _on_delete_product_clicked(self, product_id):
        if self.controller and hasattr(self.controller, "handle_delete_product"):
            self.controller.handle_delete_product(product_id)

    def render_table(self, empleados_list):
        if not hasattr(self, "table_scroll") or not self.table_scroll.winfo_exists():
            return
        for widget in self.table_scroll.winfo_children():
            widget.destroy()

        self._rows = empleados_list or []

        if not self._rows:
            empty = ctk.CTkLabel(
                self.table_scroll,
                text="No hay empleados para mostrar.",
                font=(self.FONT, 13),
                text_color=self.COLORS["text_secondary"],
            )
            empty.grid(row=0, column=0, columnspan=5, sticky="nsew", pady=24)
            return

        role_styles = {
            "Administrador": (self.COLORS["primary"], self.COLORS["secondary"]),
            "Mesero": (self.COLORS["chip_bg"], self.COLORS["chip_fg"]),
            "Cocinero": (self.COLORS["role_cook_bg"], self.COLORS["secondary"]),
        }

        for row_idx, emp in enumerate(self._rows):
            row_bg = self.COLORS["table_row_a"] if row_idx % 2 == 0 else self.COLORS["table_row_b"]
            row = ctk.CTkFrame(
                self.table_scroll,
                fg_color=row_bg,
                corner_radius=6,
                border_width=1,
                border_color=self.COLORS["panel_border"],
            )
            row.grid(row=row_idx, column=0, columnspan=5, sticky="ew", padx=4, pady=4)
            for col, weight in enumerate((3, 2, 2, 3, 2)):
                row.grid_columnconfigure(col, weight=weight, uniform="user_row_columns", minsize=(260, 150, 145, 180, 180)[col])

            employee_wrap = ctk.CTkFrame(row, fg_color="transparent")
            employee_wrap.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
            employee_wrap.grid_columnconfigure(0, weight=1)

            employee_label = ctk.CTkLabel(
                employee_wrap,
                text=str(emp.get("name", "-")),
                font=(self.FONT, 12, "bold"),
                text_color=self.COLORS["text_primary"],
                anchor="w",
            )
            employee_label.grid(row=0, column=0, sticky="w")

            employee_id = ctk.CTkLabel(
                employee_wrap,
                text=f"Usuario: {emp.get('username', '-')}  |  ID: #{emp.get('id', '-')}",
                font=(self.FONT, 10),
                text_color=self.COLORS["neutral"],
                anchor="w",
            )
            employee_id.grid(row=1, column=0, sticky="w", pady=(1, 0))

            role_text = str(emp.get("role", "-"))
            role_bg, role_fg = role_styles.get(role_text, (self.COLORS["role_default_bg"], self.COLORS["text_warm"]))
            role_pill = ctk.CTkLabel(
                row,
                text=role_text,
                fg_color=role_bg,
                text_color=role_fg,
                corner_radius=12,
                padx=10,
                pady=3,
                font=(self.FONT, 10, "bold"),
            )
            role_pill.grid(row=0, column=1, sticky="w", padx=12)

            status_text = str(emp.get("status", "Fuera de Turno"))
            status_color = self.COLORS["success"] if status_text == "Fichado" else self.COLORS["muted"]
            status_label = ctk.CTkLabel(
                row,
                text=f"● {status_text}",
                font=(self.FONT, 11, "bold"),
                text_color=status_color,
                anchor="w",
            )
            status_label.grid(row=0, column=2, sticky="w", padx=12)

            time_label = ctk.CTkLabel(
                row,
                text=str(emp.get("time", "-")),
                font=(self.FONT, 11, "bold"),
                text_color=self.COLORS["text_secondary"],
                anchor="w",
            )
            time_label.grid(row=0, column=3, sticky="ew", padx=12)

            actions = ctk.CTkFrame(row, fg_color="transparent")
            actions.grid(row=0, column=4, sticky="e", padx=10)

            emp_id = emp.get("id")

            edit_btn = ctk.CTkButton(
                actions,
                text="Editar",
                width=75,
                height=28,
                corner_radius=6,
                fg_color=self.COLORS["chip_bg"],
                hover_color=self.COLORS["edit_hover"],
                text_color=self.COLORS["text_primary"],
                border_width=1,
                border_color=self.COLORS["panel_border"],
                font=(self.FONT, 11, "bold"),
                command=lambda eid=emp_id: self._on_edit_clicked(eid),
            )
            edit_btn.grid(row=0, column=0, padx=(0, 6))

            delete_btn = ctk.CTkButton(
                actions,
                text="Eliminar",
                width=75,
                height=28,
                corner_radius=6,
                fg_color=self.COLORS["primary"],
                hover_color=self.COLORS["accent_hover"],
                text_color=self.COLORS["secondary"],
                font=(self.FONT, 11, "bold"),
                command=lambda eid=emp_id: self._on_delete_clicked(eid),
            )
            delete_btn.grid(row=0, column=1)

    def get_search_query(self):
        search_entry = getattr(self, "search_entry", None)
        if search_entry is not None and hasattr(search_entry, "get") and search_entry.winfo_exists():
            return search_entry.get().strip()

        menu_entry = getattr(self, "menu_search_entry", None)
        if menu_entry is not None and hasattr(menu_entry, "get") and menu_entry.winfo_exists():
            return menu_entry.get().strip()

        return ""

    def open_employee_form(self, empleado, on_submit):
        form = ctk.CTkToplevel(self)
        form.title("Editar Usuario" if empleado else "Nuevo Usuario")
        form.geometry("500x530")
        form.resizable(False, False)
        form.configure(fg_color=self.COLORS["wine_bg"])
        form.transient(self)
        form.grab_set()
        form.grid_columnconfigure(0, weight=1)

        content = ctk.CTkFrame(form, fg_color=self.COLORS["wine_panel"], corner_radius=8, border_width=1, border_color=self.COLORS["panel_border"])
        content.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        content.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(content, text="Editar Usuario" if empleado else "Nuevo Usuario", font=(self.FONT, 24, "bold"), text_color=self.COLORS["text_primary"], anchor="w").grid(row=0, column=0, sticky="w", padx=20, pady=(20, 3))
        ctk.CTkLabel(content, text="Administra el nombre y rol del personal.", font=(self.FONT, 11), text_color=self.COLORS["neutral"], anchor="w").grid(row=1, column=0, sticky="w", padx=20, pady=(0, 18))

        ctk.CTkLabel(content, text="Nombre completo", font=(self.FONT, 11, "bold"), text_color=self.COLORS["text_warm"], anchor="w").grid(row=2, column=0, sticky="w", padx=20, pady=(7, 5))
        name_entry = ctk.CTkEntry(content, height=36, fg_color=self.COLORS["wine_bg"], border_color=self.COLORS["panel_border"], text_color=self.COLORS["text_primary"], font=(self.FONT, 12))
        name_entry.grid(row=3, column=0, sticky="ew", padx=20)
        name_entry.insert(0, str((empleado or {}).get("name", "")))

        ctk.CTkLabel(content, text="Rol", font=(self.FONT, 11, "bold"), text_color=self.COLORS["text_warm"], anchor="w").grid(row=4, column=0, sticky="w", padx=20, pady=(12, 5))
        roles = ["Administrador", "Mesero", "Cocinero"]
        role_menu = ctk.CTkOptionMenu(content, values=roles, variable=ctk.StringVar(value=str((empleado or {}).get("role", "Mesero"))), height=36, fg_color=self.COLORS["wine_bg"], button_color=self.COLORS["accent"], button_hover_color=self.COLORS["accent_hover"], text_color=self.COLORS["text_primary"], font=(self.FONT, 12))
        role_menu.grid(row=5, column=0, sticky="ew", padx=20)

        ctk.CTkLabel(content, text="Usuario de acceso", font=(self.FONT, 11, "bold"), text_color=self.COLORS["text_warm"], anchor="w").grid(row=6, column=0, sticky="w", padx=20, pady=(12, 5))
        username_entry = ctk.CTkEntry(content, height=36, fg_color=self.COLORS["wine_bg"], border_color=self.COLORS["panel_border"], text_color=self.COLORS["text_primary"], font=(self.FONT, 12), placeholder_text="Ej. jperez")
        username_entry.grid(row=7, column=0, sticky="ew", padx=20)
        username_entry.insert(0, str((empleado or {}).get("username", "")))

        ctk.CTkLabel(content, text="Contraseña (solo números)", font=(self.FONT, 11, "bold"), text_color=self.COLORS["text_warm"], anchor="w").grid(row=8, column=0, sticky="w", padx=20, pady=(12, 5))

        def _validate_numeric_password(val):
            return val.isdigit() or val == ""

        vcmd = (form.register(_validate_numeric_password), '%P')

        pass_container = ctk.CTkFrame(content, fg_color="transparent")
        pass_container.grid(row=9, column=0, sticky="ew", padx=20)
        pass_container.grid_columnconfigure(0, weight=1)

        password_entry = ctk.CTkEntry(
            pass_container,
            height=36,
            show="*",
            fg_color=self.COLORS["wine_bg"],
            border_color=self.COLORS["panel_border"],
            text_color=self.COLORS["text_primary"],
            font=(self.FONT, 12),
            placeholder_text="Obligatoria para nuevos usuarios (solo números)",
            validate="key",
            validatecommand=vcmd
        )
        password_entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        def _toggle_password():
            if password_entry.cget("show") == "*":
                password_entry.configure(show="")
                toggle_btn.configure(text="🔒", fg_color=self.COLORS["accent"], hover_color=self.COLORS["accent_hover"])
            else:
                password_entry.configure(show="*")
                toggle_btn.configure(text="👁", fg_color=self.COLORS["wine_bg"], hover_color=self.COLORS["hover_surface"])

        toggle_btn = ctk.CTkButton(
            pass_container,
            text="👁",
            width=42,
            height=36,
            corner_radius=6,
            fg_color=self.COLORS["wine_bg"],
            hover_color=self.COLORS["hover_surface"],
            border_width=1,
            border_color=self.COLORS["panel_border"],
            text_color=self.COLORS["text_warm"],
            font=(self.FONT, 13),
            command=_toggle_password
        )
        toggle_btn.grid(row=0, column=1)

        buttons = ctk.CTkFrame(content, fg_color="transparent")
        buttons.grid(row=10, column=0, sticky="ew", padx=20, pady=(26, 20))
        buttons.grid_columnconfigure((0, 1), weight=1)

        def save():
            nombre = name_entry.get().strip()
            if not nombre:
                messagebox.showwarning("Campo requerido", "Ingresa el nombre completo.", parent=form)
                name_entry.focus_set()
                return
            username = username_entry.get().strip()
            password = password_entry.get()
            if not username:
                messagebox.showwarning("Campo requerido", "Ingresa el usuario de acceso.", parent=form)
                username_entry.focus_set()
                return
            if not empleado and not password:
                messagebox.showwarning("Campo requerido", "Ingresa una contraseña para el nuevo usuario.", parent=form)
                password_entry.focus_set()
                return
            if password and not password.isdigit():
                messagebox.showwarning("Contraseña inválida", "La contraseña solo debe contener números.", parent=form)
                password_entry.focus_set()
                return
            on_submit((nombre, role_menu.get(), username, password))
            form.destroy()

        ctk.CTkButton(buttons, text="Cancelar", height=36, corner_radius=6, fg_color="transparent", hover_color=self.COLORS["hover_surface"], border_width=1, border_color=self.COLORS["panel_border"], text_color=self.COLORS["text_warm"], font=(self.FONT, 11, "bold"), command=form.destroy).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ctk.CTkButton(buttons, text="Guardar Usuario", height=36, corner_radius=6, fg_color=self.COLORS["accent"], hover_color=self.COLORS["accent_hover"], text_color=self.COLORS["text_primary"], font=(self.FONT, 11, "bold"), command=save).grid(row=0, column=1, sticky="ew", padx=(6, 0))
        name_entry.focus_set()
        form.protocol("WM_DELETE_WINDOW", form.destroy)

    def _on_search_changed(self, event):
        if self.controller and hasattr(self.controller, "handle_search"):
            self.controller.handle_search()

    def _on_add_clicked(self):
        if self.controller and hasattr(self.controller, "handle_add_employee"):
            self.controller.handle_add_employee()

    def _on_edit_clicked(self, emp_id):
        if self.controller and hasattr(self.controller, "handle_edit_employee"):
            self.controller.handle_edit_employee(emp_id)

    def _on_delete_clicked(self, emp_id):
        if self.controller and hasattr(self.controller, "handle_delete_employee"):
            self.controller.handle_delete_employee(emp_id)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    root.withdraw()

    window = UnifiedDashboardWindow(root, usuario="admin_demo")

    demo_data = [
        {"id": 1, "name": "Marcela Ruiz", "role": "Administrador", "status": "Fichado", "time": "Hoy 08:02"},
        {"id": 2, "name": "Diego Pastor", "role": "Mesero", "status": "Fuera de Turno", "time": "Ayer 23:40"},
        {"id": 3, "name": "Valentina Sosa", "role": "Cocinero", "status": "Fichado", "time": "Hoy 07:55"},
        {"id": 4, "name": "Julian Roldan", "role": "Mesero", "status": "Fichado", "time": "Hoy 08:11"},
    ]
    window.render_table(demo_data)

    root.mainloop()
