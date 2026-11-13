from datetime import date, timedelta
import customtkinter as ctk
import tkinter as tk
from src.views.componentes.calendario_modal import CalendarioRangoModal

class AnalisisView:
    COLORS = {
        "window": "#1A1C1E",
        "panel": "#231719",
        "panel_border": "#4A3134",
        "text_primary": "#F4EBD0",
        "text_secondary": "#867370",
        "text_warm": "#D8CDB2",
        "accent": "#8C1A11",
        "accent_hover": "#A1241A",
        "accent_soft": "#DFA99D",
        "success": "#2EA44F",
        "warning": "#E2B93B",
        "card_bg": "#1D1315",
        "bar_bg": "#3A2A2D",
    }

    def __init__(self, parent):
        self.parent = parent
        self.controller = None
        self._last_data = {}
        
        # Estado del rango de fechas (por defecto: Últimos 30 días)
        self._fecha_fin = date.today()
        self._fecha_inicio = self._fecha_fin - timedelta(days=29)
        self._texto_periodo = "Últimos 30 días"
        
        self.frame = ctk.CTkFrame(
            parent,
            fg_color=self.COLORS["window"],
            corner_radius=0,
            border_width=0,
        )
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        
        self._build_header()
        self._build_body()

    def _build_header(self):
        header = ctk.CTkFrame(self.frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 10))
        header.grid_columnconfigure(0, weight=1)
        
        title_block = ctk.CTkFrame(header, fg_color="transparent")
        title_block.grid(row=0, column=0, sticky="w")
        
        ctk.CTkLabel(
            title_block, text="Análisis de Productos", 
            font=("Segoe UI", 30, "bold"), text_color=self.COLORS["text_primary"]
        ).grid(row=0, column=0, sticky="w")
        
        subtitle_frame = ctk.CTkFrame(title_block, fg_color="transparent")
        subtitle_frame.grid(row=1, column=0, sticky="w", pady=(2, 0))
        
        ctk.CTkLabel(
            subtitle_frame, text="Reporte consolidado del periodo actual: ", 
            font=("Segoe UI", 12), text_color=self.COLORS["text_secondary"]
        ).grid(row=0, column=0, sticky="w")
        
        self.lbl_periodo = ctk.CTkLabel(
            subtitle_frame, text=self._texto_periodo, 
            font=("Segoe UI", 12, "bold"), text_color=self.COLORS["text_warm"]
        )
        self.lbl_periodo.grid(row=0, column=1, sticky="w")
        
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.grid(row=0, column=1, sticky="e")
        
        self.btn_rango = ctk.CTkButton(
            btn_frame, text="📅 Rango de Fechas", width=160, height=36,
            fg_color="transparent", border_width=1, border_color=self.COLORS["panel_border"],
            hover_color=self.COLORS["panel"], text_color=self.COLORS["text_warm"], font=("Segoe UI", 12, "bold"),
            command=self._abrir_modal_calendario
        )
        self.btn_rango.grid(row=0, column=0, padx=(0, 10))
        
        ctk.CTkButton(
            btn_frame, text="📥 Exportar Excel", width=140, height=36,
            fg_color="#2EA44F", hover_color="#268841",
            text_color="#FFFFFF", font=("Segoe UI", 12, "bold"),
            command=self._exportar_reporte
        ).grid(row=0, column=1)

    def _build_body(self):
        self.body = ctk.CTkScrollableFrame(self.frame, fg_color="transparent", corner_radius=0)
        self.body.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.body.grid_columnconfigure(0, weight=1)
        
        # 4 Cards row
        self.cards_frame = ctk.CTkFrame(self.body, fg_color="transparent")
        self.cards_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        for i in range(4):
            self.cards_frame.grid_columnconfigure(i, weight=1, uniform="card")
            
        self.lbl_estrella = self._create_stat_card(self.cards_frame, 0, "PRODUCTO ESTRELLA", "-", "Mayor volumen en el período", self.COLORS["success"])
        self.lbl_ticket = self._create_stat_card(self.cards_frame, 1, "COMANDAS POR DÍA", "0", "Promedio diario", self.COLORS["success"])
        self.lbl_pico = self._create_stat_card(self.cards_frame, 2, "PICO DE DEMANDA", "-", "Horario con más pedidos", self.COLORS["warning"])
        self.lbl_categoria = self._create_stat_card(self.cards_frame, 3, "CATEGORÍA MÁS RENTABLE", "-", "📈 Liderando el volumen de ventas", self.COLORS["text_secondary"])

        # Top 5
        self.top5_frame = ctk.CTkFrame(self.body, fg_color=self.COLORS["panel"], corner_radius=8, border_width=1, border_color=self.COLORS["panel_border"])
        self.top5_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.top5_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            self.top5_frame, text="TOP 5 PLATOS MÁS VENDIDOS", font=("Segoe UI", 14, "bold"), text_color=self.COLORS["text_primary"]
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(20, 0))
        
        ctk.CTkLabel(
            self.top5_frame, text="Volumen de ventas por unidad", font=("Segoe UI", 11), text_color=self.COLORS["text_secondary"]
        ).grid(row=1, column=0, sticky="w", padx=20, pady=(0, 15))
        
        self.top5_container = ctk.CTkFrame(self.top5_frame, fg_color="transparent")
        self.top5_container.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        self.top5_container.grid_columnconfigure(0, weight=1)

        # Bar chart
        self.chart_frame = ctk.CTkFrame(self.body, fg_color=self.COLORS["panel"], corner_radius=8, border_width=1, border_color=self.COLORS["panel_border"])
        self.chart_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        self.chart_frame.grid_columnconfigure(0, weight=1)
        
        header_chart = ctk.CTkFrame(self.chart_frame, fg_color="transparent")
        header_chart.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_chart.grid_columnconfigure(0, weight=1)
        
        title_chart_box = ctk.CTkFrame(header_chart, fg_color="transparent")
        title_chart_box.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(title_chart_box, text="PICOS DE DEMANDA HORARIA", font=("Segoe UI", 14, "bold"), text_color=self.COLORS["text_primary"]).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(title_chart_box, text="Promedio de pedidos por hora (Lunes - Domingo)", font=("Segoe UI", 11), text_color=self.COLORS["text_secondary"]).grid(row=1, column=0, sticky="w")

        self.chart_container = ctk.CTkFrame(self.chart_frame, fg_color="transparent", height=250)
        self.chart_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))
        self.chart_container.grid_propagate(False)

    def _create_stat_card(self, parent, col, title, value, sub, sub_color):
        card = ctk.CTkFrame(parent, fg_color=self.COLORS["card_bg"], corner_radius=8, border_width=1, border_color=self.COLORS["panel_border"])
        card.grid(row=0, column=col, sticky="nsew", padx=(0 if col==0 else 5, 0 if col==3 else 5))
        
        ctk.CTkLabel(card, text=title, font=("Segoe UI", 10, "bold"), text_color=self.COLORS["text_secondary"]).grid(row=0, column=0, sticky="w", padx=15, pady=(15, 10))
        lbl_val = ctk.CTkLabel(card, text=value, font=("Segoe UI", 22, "bold"), text_color=self.COLORS["text_primary"])
        lbl_val.grid(row=1, column=0, sticky="w", padx=15)
        ctk.CTkLabel(card, text=sub, font=("Segoe UI", 10), text_color=sub_color).grid(row=2, column=0, sticky="w", padx=15, pady=(5, 15))
        
        return lbl_val

    def _abrir_modal_calendario(self):
        try:
            parent_window = self.frame.winfo_toplevel()
        except Exception:
            parent_window = self.frame

        CalendarioRangoModal(
            parent=parent_window,
            fecha_inicio=self._fecha_inicio,
            fecha_fin=self._fecha_fin,
            on_apply=self._aplicar_rango_fechas
        )

    def _aplicar_rango_fechas(self, fecha_inicio, fecha_fin, texto_periodo):
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_fin
        self._texto_periodo = texto_periodo
        self.lbl_periodo.configure(text=texto_periodo)

        if fecha_inicio and fecha_fin:
            f1 = fecha_inicio.strftime('%d/%m/%Y')
            f2 = fecha_fin.strftime('%d/%m/%Y')
            if texto_periodo in ("Hoy", "Ayer", "Últimos 7 días", "Últimos 30 días", "Este Mes", "Todo el Historial"):
                btn_txt = f"📅 {texto_periodo}"
            else:
                btn_txt = f"📅 {f1} - {f2}"
        else:
            btn_txt = "📅 Rango de Fechas"
        self.btn_rango.configure(text=btn_txt)

        if self.controller:
            self.controller.cargar_datos(fecha_inicio, fecha_fin)

    def actualizar_dashboard(self, data):
        self._last_data = data
        self.lbl_estrella.configure(text=data.get("producto_estrella", "N/A") or "N/A")
        self.lbl_ticket.configure(text=f"{int(data.get('ticket_promedio', 0))}")
        self.lbl_pico.configure(text=data.get("pico_demanda", "N/A") or "N/A")
        self.lbl_categoria.configure(text=data.get("categoria_rentable", "N/A") or "N/A")
        
        # Actualizar Top 5
        for widget in self.top5_container.winfo_children():
            widget.destroy()
            
        top5 = data.get("top_5", [])
        if not top5:
            ctk.CTkLabel(self.top5_container, text="No hay datos de ventas en este período.", text_color=self.COLORS["text_secondary"]).grid(row=0, column=0, pady=20)
        else:
            max_ventas = float(max(float(item["total_vendido"]) for item in top5)) if top5 else 1.0
            for i, item in enumerate(top5):
                row = ctk.CTkFrame(self.top5_container, fg_color="transparent")
                row.grid(row=i*2, column=0, sticky="ew", pady=(8, 2))
                row.grid_columnconfigure(0, weight=1)
                
                ctk.CTkLabel(row, text=item["nombre"], font=("Segoe UI", 11, "bold"), text_color=self.COLORS["text_primary"]).grid(row=0, column=0, sticky="w")
                ctk.CTkLabel(row, text=f"{int(item['total_vendido']):,} u.", font=("Segoe UI", 11), text_color=self.COLORS["text_secondary"]).grid(row=0, column=1, sticky="e")
                
                bar = ctk.CTkProgressBar(self.top5_container, height=6, fg_color=self.COLORS["bar_bg"], progress_color=self.COLORS["accent"], corner_radius=0)
                bar.grid(row=i*2+1, column=0, sticky="ew", pady=(0, 10))
                bar.set(float(item["total_vendido"]) / max_ventas)
                
        # Actualizar Gráfico de Barras
        for widget in self.chart_container.winfo_children():
            widget.destroy()
            
        ventas_hora = data.get("ventas_por_hora", [])
        if not ventas_hora:
            return
            
        max_pedidos = max(item["pedidos"] for item in ventas_hora) if ventas_hora else 1
        if max_pedidos == 0:
            max_pedidos = 1
            
        num_cols = len(ventas_hora)
        for i in range(num_cols):
            self.chart_container.grid_columnconfigure(i, weight=1, uniform="bar")
            
        self.chart_container.grid_rowconfigure(0, weight=1)
        self.chart_container.grid_rowconfigure(1, weight=0)
        
        for idx, item in enumerate(ventas_hora):
            hora_str = item["hora"]
            pedidos = item["pedidos"]
            
            bar_frame = ctk.CTkFrame(self.chart_container, fg_color="transparent")
            bar_frame.grid(row=0, column=idx, sticky="nsew", padx=2)
            
            porcentaje = (pedidos / max_pedidos) if max_pedidos > 0 else 0
            if porcentaje < 0.03:
                porcentaje = 0.03

            color = self.COLORS["accent"] if pedidos == max_pedidos and pedidos > 0 else self.COLORS["bar_bg"]
            
            bar = ctk.CTkFrame(bar_frame, fg_color=color, corner_radius=2)
            bar.place(relx=0.2, rely=1.0 - porcentaje, relwidth=0.6, relheight=porcentaje)
            
            if pedidos == max_pedidos and pedidos > 0:
                lbl = ctk.CTkLabel(bar_frame, text=hora_str, font=("Segoe UI", 9, "bold"), text_color=self.COLORS["panel"], fg_color=self.COLORS["text_warm"], corner_radius=2)
                lbl.place(relx=0.5, rely=1.0 - porcentaje - 0.05, anchor="s")

            if idx % 2 == 0:
                ctk.CTkLabel(self.chart_container, text=hora_str, font=("Segoe UI", 8), text_color=self.COLORS["text_secondary"]).grid(row=1, column=idx, pady=(5, 0))

    def _exportar_reporte(self):
        if not self._last_data:
            from tkinter import messagebox
            messagebox.showinfo("Exportar", "No hay datos para exportar.")
            return
            
        from tkinter import filedialog
        
        filepath = filedialog.asksaveasfilename(
            parent=self.frame,
            title="Exportar Análisis",
            defaultextension=".xlsx",
            filetypes=[("Archivos Excel", "*.xlsx")],
            initialfile="Analisis_Moscato.xlsx"
        )
        if not filepath:
            return
            
        try:
            try:
                from src.utils.excel_export import guardar_como_excel_analisis
            except ImportError:
                import sys
                import os
                current_dir = os.path.dirname(os.path.abspath(__file__))
                src_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
                if src_dir not in sys.path:
                    sys.path.insert(0, src_dir)
                from utils.excel_export import guardar_como_excel_analisis
            
            top5 = self._last_data.get("top_5", [])
            ventas_hora = self._last_data.get("ventas_por_hora", [])
            resumen = {
                "Período de Análisis": self._texto_periodo,
                "Producto Estrella": self._last_data.get("producto_estrella", "N/A"),
                "Comandas por Día (Promedio)": self._last_data.get("ticket_promedio", 0),
                "Pico de Demanda": self._last_data.get("pico_demanda", "N/A"),
                "Categoría Más Rentable": self._last_data.get("categoria_rentable", "N/A"),
            }
            
            guardar_como_excel_analisis(filepath, resumen, top5, ventas_hora)
            from tkinter import messagebox
            messagebox.showinfo("Exportar", f"Reporte exportado correctamente a:\n{filepath}")
        except ImportError:
            from tkinter import messagebox
            messagebox.showerror("Exportar", "Falta la librería openpyxl.\nEjecuta: pip install openpyxl")
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Exportar", f"Error al exportar:\n{e}")
