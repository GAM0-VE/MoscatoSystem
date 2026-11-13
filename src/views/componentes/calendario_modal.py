import calendar
from datetime import date, datetime, timedelta
import customtkinter as ctk

class CalendarioRangoModal(ctk.CTkToplevel):
    COLORS = {
        "window": "#16181A",
        "panel": "#231719",
        "panel_border": "#4A3134",
        "text_primary": "#F4EBD0",
        "text_secondary": "#A89A98",
        "text_warm": "#D8CDB2",
        "accent": "#8C1A11",
        "accent_hover": "#A1241A",
        "in_range": "#422225",
        "today_border": "#E2B93B",
        "success": "#2EA44F",
        "success_hover": "#268841",
    }

    MESES = [
        "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    DIAS_SEMANA = ["Lu", "Ma", "Mi", "Ju", "Vi", "Sá", "Do"]

    def __init__(self, parent, fecha_inicio=None, fecha_fin=None, on_apply=None):
        super().__init__(parent)
        self.title("Seleccionar Rango de Fechas")
        self.geometry("700x530")
        self.resizable(False, False)
        self.configure(fg_color=self.COLORS["window"])
        
        self.on_apply = on_apply
        self.fecha_inicio = fecha_inicio or (date.today() - timedelta(days=29))
        self.fecha_fin = fecha_fin or date.today()
        self.texto_periodo = "Personalizado"
        
        # Calendar view state (which month/year is shown)
        ref_date = self.fecha_fin or date.today()
        self.current_year = ref_date.year
        self.current_month = ref_date.month
        self.modo_seleccion = "desde"  # 'desde' o 'hasta'

        # Make modal
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self._render_calendar()

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(15, 10))
        
        ctk.CTkLabel(
            header, text="📅 Rango de Fechas", 
            font=("Segoe UI", 20, "bold"), text_color=self.COLORS["text_primary"]
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header, text="Selecciona un período rápido o elige las fechas en el calendario.",
            font=("Segoe UI", 12), text_color=self.COLORS["text_secondary"]
        ).pack(anchor="w", pady=(2, 0))

        # Main content: Left presets + Right calendar
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        content.grid_columnconfigure(0, weight=0) # Presets
        content.grid_columnconfigure(1, weight=1) # Calendar
        content.grid_rowconfigure(0, weight=1)

        # --- Presets (Left) ---
        presets_frame = ctk.CTkFrame(
            content, fg_color=self.COLORS["panel"], 
            corner_radius=8, border_width=1, border_color=self.COLORS["panel_border"],
            width=180
        )
        presets_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        presets_frame.grid_propagate(False)

        ctk.CTkLabel(
            presets_frame, text="ACCESOS RÁPIDOS", 
            font=("Segoe UI", 11, "bold"), text_color=self.COLORS["text_secondary"]
        ).pack(anchor="w", padx=14, pady=(12, 8))

        presets = [
            ("Hoy", self._set_preset_hoy),
            ("Ayer", self._set_preset_ayer),
            ("Últimos 7 días", self._set_preset_7dias),
            ("Últimos 30 días", self._set_preset_30dias),
            ("Este Mes", self._set_preset_este_mes),
            ("Mes Anterior", self._set_preset_mes_anterior),
            ("Todo el Historial", self._set_preset_todo),
        ]

        for label, cmd in presets:
            ctk.CTkButton(
                presets_frame, text=label, anchor="w",
                fg_color="transparent", hover_color="#362225",
                text_color=self.COLORS["text_warm"], font=("Segoe UI", 12),
                height=32, command=cmd
            ).pack(fill="x", padx=8, pady=2)

        # --- Calendar Container (Right) ---
        self.cal_container = ctk.CTkFrame(
            content, fg_color=self.COLORS["panel"], 
            corner_radius=8, border_width=1, border_color=self.COLORS["panel_border"]
        )
        self.cal_container.grid(row=0, column=1, sticky="nsew")
        self.cal_container.grid_columnconfigure(0, weight=1)
        self.cal_container.grid_rowconfigure(2, weight=1)

        # Month Navigation + Mode Selector
        top_cal = ctk.CTkFrame(self.cal_container, fg_color="transparent")
        top_cal.grid(row=0, column=0, sticky="ew", padx=14, pady=(10, 5))
        top_cal.grid_columnconfigure(1, weight=1)

        # Prev / Next month buttons
        ctk.CTkButton(
            top_cal, text="◀", width=32, height=30,
            fg_color="transparent", hover_color="#362225",
            text_color=self.COLORS["text_warm"], font=("Segoe UI", 12, "bold"),
            command=self._prev_month
        ).grid(row=0, column=0)

        self.lbl_mes_ano = ctk.CTkLabel(
            top_cal, text="", font=("Segoe UI", 14, "bold"), text_color=self.COLORS["text_primary"]
        )
        self.lbl_mes_ano.grid(row=0, column=1)

        ctk.CTkButton(
            top_cal, text="▶", width=32, height=30,
            fg_color="transparent", hover_color="#362225",
            text_color=self.COLORS["text_warm"], font=("Segoe UI", 12, "bold"),
            command=self._next_month
        ).grid(row=0, column=2)

        # Mode selector: Selecting Desde or Hasta
        mode_frame = ctk.CTkFrame(self.cal_container, fg_color="transparent")
        mode_frame.grid(row=1, column=0, sticky="ew", padx=14, pady=(2, 6))
        
        self.seg_modo = ctk.CTkSegmentedButton(
            mode_frame, values=["1. Desde (Inicio)", "2. Hasta (Fin)"],
            selected_color=self.COLORS["accent"],
            selected_hover_color=self.COLORS["accent_hover"],
            font=("Segoe UI", 11, "bold"),
            command=self._on_modo_change
        )
        self.seg_modo.pack(fill="x")
        self.seg_modo.set("1. Desde (Inicio)")

        # Days of week and day grid
        self.grid_frame = ctk.CTkFrame(self.cal_container, fg_color="transparent")
        self.grid_frame.grid(row=2, column=0, sticky="nsew", padx=14, pady=(0, 10))
        for col in range(7):
            self.grid_frame.grid_columnconfigure(col, weight=1, uniform="cal_col")

        # --- Bottom bar ---
        bottom_bar = ctk.CTkFrame(self, fg_color="transparent")
        bottom_bar.pack(fill="x", padx=20, pady=(5, 15))
        bottom_bar.grid_columnconfigure(0, weight=1)

        self.lbl_resumen = ctk.CTkLabel(
            bottom_bar, text="",
            font=("Segoe UI", 12, "bold"), text_color=self.COLORS["text_primary"]
        )
        self.lbl_resumen.grid(row=0, column=0, sticky="w")

        btn_box = ctk.CTkFrame(bottom_bar, fg_color="transparent")
        btn_box.grid(row=0, column=1, sticky="e")

        ctk.CTkButton(
            btn_box, text="Cancelar", width=100, height=34,
            fg_color="transparent", border_width=1, border_color=self.COLORS["panel_border"],
            hover_color=self.COLORS["panel"], text_color=self.COLORS["text_warm"], font=("Segoe UI", 12),
            command=self.destroy
        ).grid(row=0, column=0, padx=(0, 10))

        ctk.CTkButton(
            btn_box, text="Aplicar Filtro", width=130, height=34,
            fg_color=self.COLORS["success"], hover_color=self.COLORS["success_hover"],
            text_color="#FFFFFF", font=("Segoe UI", 12, "bold"),
            command=self._apply_and_close
        ).grid(row=0, column=1)

    def _render_calendar(self):
        self.lbl_mes_ano.configure(text=f"{self.MESES[self.current_month]} {self.current_year}")

        # Clear grid frame
        for child in self.grid_frame.winfo_children():
            child.destroy()

        # Weekday headers
        for col, dia_abrev in enumerate(self.DIAS_SEMANA):
            lbl = ctk.CTkLabel(
                self.grid_frame, text=dia_abrev,
                font=("Segoe UI", 11, "bold"),
                text_color=self.COLORS["text_secondary"]
            )
            lbl.grid(row=0, column=col, pady=(2, 6))

        # Month days
        month_cal = calendar.monthcalendar(self.current_year, self.current_month)
        today = date.today()

        for r_idx, week in enumerate(month_cal, start=1):
            for c_idx, day_num in enumerate(week):
                if day_num == 0:
                    continue

                d = date(self.current_year, self.current_month, day_num)
                is_start = (self.fecha_inicio is not None and d == self.fecha_inicio)
                is_end = (self.fecha_fin is not None and d == self.fecha_fin)
                in_range = False
                if self.fecha_inicio and self.fecha_fin:
                    in_range = (self.fecha_inicio < d < self.fecha_fin)

                if is_start or is_end:
                    fg = self.COLORS["accent"]
                    hover = self.COLORS["accent_hover"]
                    txt_color = "#FFFFFF"
                    font = ("Segoe UI", 11, "bold")
                elif in_range:
                    fg = self.COLORS["in_range"]
                    hover = "#572C30"
                    txt_color = self.COLORS["text_primary"]
                    font = ("Segoe UI", 11)
                else:
                    fg = "transparent"
                    hover = "#362225"
                    txt_color = self.COLORS["text_warm"]
                    font = ("Segoe UI", 11)

                border_w = 1 if d == today else 0
                border_c = self.COLORS["today_border"] if d == today else "transparent"

                btn = ctk.CTkButton(
                    self.grid_frame, text=str(day_num),
                    width=36, height=32, corner_radius=6,
                    fg_color=fg, hover_color=hover,
                    text_color=txt_color, font=font,
                    border_width=border_w, border_color=border_c,
                    command=lambda target_date=d: self._on_date_click(target_date)
                )
                btn.grid(row=r_idx, column=c_idx, padx=2, pady=2, sticky="nsew")

        self._update_resumen()

    def _on_date_click(self, d: date):
        self.texto_periodo = "Personalizado"
        if self.modo_seleccion == "desde":
            self.fecha_inicio = d
            if self.fecha_fin is not None and self.fecha_fin < self.fecha_inicio:
                self.fecha_fin = self.fecha_inicio
            # Auto-advance to "hasta"
            self.modo_seleccion = "hasta"
            self.seg_modo.set("2. Hasta (Fin)")
        else:
            if self.fecha_inicio is not None and d < self.fecha_inicio:
                self.fecha_inicio = d
            else:
                self.fecha_fin = d
            # Auto-switch back to desde
            self.modo_seleccion = "desde"
            self.seg_modo.set("1. Desde (Inicio)")

        self._render_calendar()

    def _on_modo_change(self, val):
        if "Desde" in val:
            self.modo_seleccion = "desde"
        else:
            self.modo_seleccion = "hasta"

    def _update_resumen(self):
        f_ini_str = self.fecha_inicio.strftime("%d/%m/%Y") if self.fecha_inicio else "Sin definir"
        f_fin_str = self.fecha_fin.strftime("%d/%m/%Y") if self.fecha_fin else "Sin definir"
        dias = ((self.fecha_fin - self.fecha_inicio).days + 1) if (self.fecha_inicio and self.fecha_fin) else 0
        self.lbl_resumen.configure(
            text=f"Rango: {f_ini_str}  →  {f_fin_str}  ({dias} día{'s' if dias!=1 else ''})"
        )

    def _prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self._render_calendar()

    def _next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self._render_calendar()

    def _set_preset_hoy(self):
        today = date.today()
        self.fecha_inicio = today
        self.fecha_fin = today
        self.current_year = today.year
        self.current_month = today.month
        self.texto_periodo = "Hoy"
        self._render_calendar()

    def _set_preset_ayer(self):
        ayer = date.today() - timedelta(days=1)
        self.fecha_inicio = ayer
        self.fecha_fin = ayer
        self.current_year = ayer.year
        self.current_month = ayer.month
        self.texto_periodo = "Ayer"
        self._render_calendar()

    def _set_preset_7dias(self):
        today = date.today()
        self.fecha_inicio = today - timedelta(days=6)
        self.fecha_fin = today
        self.current_year = today.year
        self.current_month = today.month
        self.texto_periodo = "Últimos 7 días"
        self._render_calendar()

    def _set_preset_30dias(self):
        today = date.today()
        self.fecha_inicio = today - timedelta(days=29)
        self.fecha_fin = today
        self.current_year = today.year
        self.current_month = today.month
        self.texto_periodo = "Últimos 30 días"
        self._render_calendar()

    def _set_preset_este_mes(self):
        today = date.today()
        self.fecha_inicio = date(today.year, today.month, 1)
        self.fecha_fin = today
        self.current_year = today.year
        self.current_month = today.month
        self.texto_periodo = "Este Mes"
        self._render_calendar()

    def _set_preset_mes_anterior(self):
        today = date.today()
        first_this_month = date(today.year, today.month, 1)
        last_day_last_month = first_this_month - timedelta(days=1)
        first_day_last_month = date(last_day_last_month.year, last_day_last_month.month, 1)
        self.fecha_inicio = first_day_last_month
        self.fecha_fin = last_day_last_month
        self.current_year = last_day_last_month.year
        self.current_month = last_day_last_month.month
        self.texto_periodo = f"{self.MESES[last_day_last_month.month]} {last_day_last_month.year}"
        self._render_calendar()

    def _set_preset_todo(self):
        self.fecha_inicio = date(2020, 1, 1)
        self.fecha_fin = date.today()
        self.current_year = date.today().year
        self.current_month = date.today().month
        self.texto_periodo = "Todo el Historial"
        self._render_calendar()

    def _apply_and_close(self):
        if self.on_apply:
            if self.texto_periodo == "Personalizado":
                texto = f"{self.fecha_inicio.strftime('%d/%m/%Y')} - {self.fecha_fin.strftime('%d/%m/%Y')}"
            else:
                texto = self.texto_periodo
            self.on_apply(self.fecha_inicio, self.fecha_fin, texto)
        self.destroy()

