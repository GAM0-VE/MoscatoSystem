import customtkinter as ctk
import tkinter.messagebox as messagebox

class AdminMesasView:
    COLORS = {
        "primary": "#8C1A11",
        "secondary": "#F4EBD0",
        "tertiary": "#1A1C1E",
        "neutral": "#867370",
        "window": "#1A1C1E",
        "wine_bg": "#1A1C1E",
        "wine_panel": "#231719",
        "wine_soft": "#2D1E21",
        "text_primary": "#F4EBD0",
        "text_secondary": "#867370",
        "text_warm": "#D8CDB2",
        "success": "#2EA44F",
        "muted": "#867370",
        "panel_border": "#4A3134",
        "chip_bg": "#3A2427",
        "chip_fg": "#F4EBD0",
        "accent": "#8C1A11",
        "accent_hover": "#A1241A",
        "accent_soft": "#DFA99D",
        "soft_hover": "#E8BBB2",
        "table_row_a": "#281B1E",
        "table_row_b": "#24181B",
        "scroll_btn": "#5F3134",
        "scroll_btn_hover": "#754046",
        "edit_hover": "#514044",
        "card_bg": "#1D1618",
        "card_icon_bg": "#352427",
    }
    FONT = "Segoe UI"

    def __init__(self, parent):
        self.parent = parent
        self.controller = None
        self.current_filter = "TODAS"
        self._build_ui()

    def set_controller(self, controller):
        self.controller = controller

    def _build_ui(self):
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(0, weight=0)
        self.parent.grid_rowconfigure(1, weight=0)
        self.parent.grid_rowconfigure(2, weight=1)

        # Header
        header = ctk.CTkFrame(self.parent, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(14, 10))
        header.grid_columnconfigure(0, weight=1)

        title_block = ctk.CTkFrame(header, fg_color="transparent")
        title_block.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(title_block, text="Gestión de Mesas", font=(self.FONT, 30, "bold"), text_color=self.COLORS["text_primary"], anchor="w").grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(title_block, text="Administra la distribución del salón, capacidad y disponibilidad en tiempo real.", font=(self.FONT, 12), text_color=self.COLORS["neutral"], anchor="w").grid(row=1, column=0, sticky="w", pady=(2, 0))
        
        ctk.CTkButton(header, text="+ Nueva Mesa", width=140, height=36, corner_radius=6, fg_color=self.COLORS["accent_soft"], hover_color=self.COLORS["soft_hover"], text_color=self.COLORS["tertiary"], font=(self.FONT, 12, "bold"), command=self._on_add_clicked).grid(row=0, column=1, sticky="e")

        # Stats Cards
        stats_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        stats_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 14))
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.lbl_total = self._build_stat_card(stats_frame, 0, "TOTAL MESAS", "0", "Capacidad instalada")
        self.lbl_activas = self._build_stat_card(stats_frame, 1, "ACTIVAS / OPERATIVAS", "0", "Listas para servicio", self.COLORS["success"])
        self.lbl_inactivas = self._build_stat_card(stats_frame, 2, "INACTIVAS", "0", "Mantenimiento y revisión", self.COLORS["accent"])

        # Body
        body = ctk.CTkFrame(self.parent, fg_color="transparent")
        body.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 14))
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(1, weight=1)

        # Controls (Search & Filters)
        controls = ctk.CTkFrame(body, fg_color="transparent")
        controls.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        controls.grid_columnconfigure(1, weight=1)

        self.search_entry = ctk.CTkEntry(
            controls, height=34, width=280, placeholder_text="Buscar mesa por número...",
            fg_color=self.COLORS["wine_panel"], border_color=self.COLORS["panel_border"],
            text_color=self.COLORS["text_primary"], placeholder_text_color=self.COLORS["text_secondary"],
            corner_radius=6, font=(self.FONT, 12)
        )
        self.search_entry.grid(row=0, column=0, sticky="w")
        self.search_entry.bind("<KeyRelease>", lambda e: self._on_search_changed())

        self.filters_frame = ctk.CTkFrame(controls, fg_color="transparent")
        self.filters_frame.grid(row=0, column=1, sticky="e")
        self.filter_buttons = {}
        for idx, f_name in enumerate(["TODAS", "ACTIVAS", "INACTIVAS"]):
            btn = ctk.CTkButton(
                self.filters_frame, text=f_name, width=80, height=30, corner_radius=6,
                fg_color="transparent", hover_color=self.COLORS["wine_soft"],
                text_color=self.COLORS["text_secondary"], font=(self.FONT, 11, "bold"),
                command=lambda f=f_name: self._set_filter(f)
            )
            btn.grid(row=0, column=idx, padx=4)
            self.filter_buttons[f_name] = btn
        self._set_filter("TODAS")

        # Table Card
        self.table_card = ctk.CTkFrame(body, fg_color=self.COLORS["wine_panel"], corner_radius=8, border_width=1, border_color=self.COLORS["panel_border"])
        self.table_card.grid(row=1, column=0, sticky="nsew")
        self.table_card.grid_columnconfigure(0, weight=1)
        self.table_card.grid_rowconfigure(2, weight=1)

        # Table Title
        card_header = ctk.CTkFrame(self.table_card, fg_color="transparent")
        card_header.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 8))
        card_header.grid_columnconfigure(0, weight=1)
        self.lbl_dir_title = ctk.CTkLabel(card_header, text="Directorio de Mesas", font=(self.FONT, 20, "bold"), text_color=self.COLORS["text_primary"], anchor="w")
        self.lbl_dir_title.grid(row=0, column=0, sticky="w")
        
        # Legend
        legend_frame = ctk.CTkFrame(card_header, fg_color="transparent")
        legend_frame.grid(row=0, column=1, sticky="e")
        ctk.CTkLabel(legend_frame, text="● Operativas", font=(self.FONT, 11, "bold"), text_color=self.COLORS["success"]).grid(row=0, column=0, padx=8)
        ctk.CTkLabel(legend_frame, text="● Inactivas", font=(self.FONT, 11, "bold"), text_color=self.COLORS["accent"]).grid(row=0, column=1, padx=8)

        # Headers
        headers = ctk.CTkFrame(self.table_card, fg_color=self.COLORS["wine_soft"], corner_radius=6)
        headers.grid(row=1, column=0, sticky="ew", padx=12)
        for col, weight in enumerate((2, 2, 2, 2)):
            headers.grid_columnconfigure(col, weight=weight, uniform="tbl")
        for col, text in enumerate(["MESA", "ESTADO OPERATIVO", "SERVICIO ACTUAL", "ACCIONES"]):
            ctk.CTkLabel(headers, text=text, font=(self.FONT, 10, "bold"), text_color=self.COLORS["text_warm"], anchor="w" if col < 3 else "center").grid(row=0, column=col, sticky="ew", padx=10, pady=8)

        # Scrollable rows
        self.table_scroll = ctk.CTkScrollableFrame(self.table_card, fg_color="transparent", corner_radius=0, scrollbar_button_color=self.COLORS["scroll_btn"], scrollbar_button_hover_color=self.COLORS["scroll_btn_hover"])
        self.table_scroll.grid(row=2, column=0, sticky="nsew", padx=8, pady=(8, 12))
        for col, weight in enumerate((2, 2, 2, 2)):
            self.table_scroll.grid_columnconfigure(col, weight=weight, uniform="tbl")

    def _build_stat_card(self, parent, col, title, value, subtitle, val_color=None):
        if not val_color:
            val_color = self.COLORS["text_primary"]
        card = ctk.CTkFrame(parent, fg_color=self.COLORS["card_bg"], corner_radius=8, border_width=1, border_color=self.COLORS["panel_border"])
        card.grid(row=0, column=col, sticky="nsew", padx=(0 if col == 0 else 6, 0 if col == 2 else 6))
        card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(card, text=title, font=(self.FONT, 11, "bold"), text_color=self.COLORS["neutral"]).grid(row=0, column=0, sticky="w", padx=16, pady=(16, 4))
        lbl_val = ctk.CTkLabel(card, text=value, font=(self.FONT, 32, "bold"), text_color=val_color)
        lbl_val.grid(row=1, column=0, sticky="w", padx=16)
        ctk.CTkLabel(card, text=subtitle, font=(self.FONT, 11), text_color=self.COLORS["text_secondary"]).grid(row=2, column=0, sticky="w", padx=16, pady=(4, 16))
        return lbl_val

    def _set_filter(self, filter_name):
        self.current_filter = filter_name
        for name, btn in self.filter_buttons.items():
            if name == filter_name:
                btn.configure(fg_color=self.COLORS["accent"], text_color=self.COLORS["text_primary"])
            else:
                btn.configure(fg_color="transparent", text_color=self.COLORS["text_secondary"])
        if self.controller:
            self.controller.refresh_mesas()

    def _on_search_changed(self):
        if self.controller:
            self.controller.refresh_mesas()

    def get_search_query(self):
        return self.search_entry.get().strip()

    def update_stats(self, total, activas, inactivas):
        self.lbl_total.configure(text=str(total))
        self.lbl_activas.configure(text=str(activas))
        self.lbl_inactivas.configure(text=str(inactivas))
        
        self.filter_buttons["TODAS"].configure(text=f"TODAS ({total})")
        self.filter_buttons["ACTIVAS"].configure(text=f"ACTIVAS ({activas})")
        self.filter_buttons["INACTIVAS"].configure(text=f"INACTIVAS ({inactivas})")

    def render_table(self, mesas):
        for w in self.table_scroll.winfo_children():
            w.destroy()
            
        if not mesas:
            ctk.CTkLabel(self.table_scroll, text="No se encontraron mesas.", font=(self.FONT, 13), text_color=self.COLORS["text_secondary"]).grid(row=0, column=0, columnspan=4, pady=24)
            return

        for row_idx, mesa in enumerate(mesas):
            row_bg = self.COLORS["table_row_a"] if row_idx % 2 == 0 else self.COLORS["table_row_b"]
            row = ctk.CTkFrame(self.table_scroll, fg_color=row_bg, corner_radius=6, border_width=1, border_color=self.COLORS["panel_border"])
            row.grid(row=row_idx, column=0, columnspan=4, sticky="ew", padx=4, pady=4)
            for col, weight in enumerate((2, 2, 2, 2)):
                row.grid_columnconfigure(col, weight=weight, uniform="tbl")

            # Columna 1: MESA
            col1 = ctk.CTkFrame(row, fg_color="transparent")
            col1.grid(row=0, column=0, sticky="ew", padx=12, pady=10)
            ctk.CTkLabel(col1, text=f"Mesa {mesa['numero_mesa']:02d}", font=(self.FONT, 14, "bold"), text_color=self.COLORS["text_primary"], anchor="w").grid(row=0, column=0, sticky="w")

            # Columna 2: ESTADO OPERATIVO
            is_active = bool(mesa['activo'])
            status_text = "● Activa" if is_active else "● Inactiva"
            status_color = self.COLORS["success"] if is_active else self.COLORS["accent"]
            ctk.CTkLabel(row, text=status_text, font=(self.FONT, 12, "bold"), text_color=status_color, anchor="w").grid(row=0, column=1, sticky="w", padx=12)

            # Columna 3: SERVICIO ACTUAL
            servicio = str(mesa.get('estado') or 'Libre').strip().capitalize()
            if not servicio:
                servicio = 'Libre'
                
            servicio_color = self.COLORS["success"] if servicio.lower() == "libre" else (
                self.COLORS["text_warm"] if servicio.lower() in ("atencion", "atención") else self.COLORS["accent_soft"]
            )
            if not is_active:
                servicio = "Inactiva Temporal"
                servicio_color = self.COLORS["muted"]
            ctk.CTkLabel(row, text=servicio, font=(self.FONT, 12, "bold"), text_color=servicio_color, anchor="w").grid(row=0, column=2, sticky="w", padx=12)

            # Columna 4: ACCIONES
            actions = ctk.CTkFrame(row, fg_color="transparent")
            actions.grid(row=0, column=3, sticky="e", padx=12)
            
            toggle_text = "Inactivar" if is_active else "Activar Mesa"
            toggle_bg = self.COLORS["chip_bg"] if is_active else self.COLORS["accent_soft"]
            toggle_fg = self.COLORS["text_primary"] if is_active else self.COLORS["tertiary"]
            toggle_hover = self.COLORS["edit_hover"] if is_active else self.COLORS["soft_hover"]
            
            ctk.CTkButton(
                actions, text=toggle_text, width=80, height=28, corner_radius=6,
                fg_color=toggle_bg, hover_color=toggle_hover, text_color=toggle_fg, font=(self.FONT, 11, "bold"),
                command=lambda mid=mesa['id_mesa'], act=not is_active: self._on_toggle_clicked(mid, act)
            ).grid(row=0, column=0, padx=(0, 6))

            ctk.CTkButton(
                actions, text="Editar", width=60, height=28, corner_radius=6,
                fg_color=self.COLORS["chip_bg"], hover_color=self.COLORS["edit_hover"], text_color=self.COLORS["text_primary"], font=(self.FONT, 11),
                command=lambda mid=mesa['id_mesa'], num=mesa['numero_mesa']: self._on_edit_clicked(mid, num)
            ).grid(row=0, column=1)

    def open_mesa_form(self, id_mesa, current_num, on_submit):
        form = ctk.CTkToplevel(self.parent)
        form.title("Editar Mesa" if id_mesa else "Nueva Mesa")
        form.geometry("400x260")
        form.resizable(False, False)
        form.configure(fg_color=self.COLORS["wine_bg"])
        form.transient(self.parent.winfo_toplevel())
        form.grab_set()

        form.grid_columnconfigure(0, weight=1)
        content = ctk.CTkFrame(form, fg_color=self.COLORS["wine_panel"], corner_radius=8, border_width=1, border_color=self.COLORS["panel_border"])
        content.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        content.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(content, text="Editar Mesa" if id_mesa else "Nueva Mesa", font=(self.FONT, 20, "bold"), text_color=self.COLORS["text_primary"], anchor="w").grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5))
        
        ctk.CTkLabel(content, text="Número de la mesa", font=(self.FONT, 11, "bold"), text_color=self.COLORS["text_warm"], anchor="w").grid(row=1, column=0, sticky="w", padx=20, pady=(15, 5))
        num_entry = ctk.CTkEntry(content, height=36, fg_color=self.COLORS["wine_bg"], border_color=self.COLORS["panel_border"], text_color=self.COLORS["text_primary"], font=(self.FONT, 12))
        num_entry.grid(row=2, column=0, sticky="ew", padx=20)
        if current_num:
            num_entry.insert(0, str(current_num))

        buttons = ctk.CTkFrame(content, fg_color="transparent")
        buttons.grid(row=3, column=0, sticky="ew", padx=20, pady=(25, 20))
        buttons.grid_columnconfigure((0, 1), weight=1)

        def save():
            num_str = num_entry.get().strip()
            if not num_str.isdigit():
                messagebox.showwarning("Invalido", "El numero de mesa debe ser un numero entero.", parent=form)
                return
            num = int(num_str)
            if num <= 0:
                messagebox.showwarning("Invalido", "El numero de mesa debe ser mayor a 0.", parent=form)
                return
            on_submit(id_mesa, num)
            form.destroy()

        ctk.CTkButton(buttons, text="Cancelar", height=36, corner_radius=6, fg_color="transparent", hover_color=self.COLORS["wine_soft"], border_width=1, border_color=self.COLORS["panel_border"], text_color=self.COLORS["text_warm"], font=(self.FONT, 11, "bold"), command=form.destroy).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ctk.CTkButton(buttons, text="Guardar", height=36, corner_radius=6, fg_color=self.COLORS["accent"], hover_color=self.COLORS["accent_hover"], text_color=self.COLORS["text_primary"], font=(self.FONT, 11, "bold"), command=save).grid(row=0, column=1, sticky="ew", padx=(6, 0))
        
        num_entry.focus_set()

    def _on_add_clicked(self):
        if self.controller:
            self.controller.handle_add_mesa()

    def _on_edit_clicked(self, id_mesa, num):
        if self.controller:
            self.controller.handle_edit_mesa(id_mesa, num)

    def _on_toggle_clicked(self, id_mesa, activate):
        if self.controller:
            self.controller.handle_toggle_mesa(id_mesa, activate)

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def show_success(self, message):
        messagebox.showinfo("Éxito", message)
