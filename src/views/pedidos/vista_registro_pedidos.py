import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class RegistroPedidosView:
    COLORS = {
        "primary": "#8C1A11",
        "secondary": "#F4EBD0",
        "tertiary": "#1A1C1E",
        "neutral": "#867370",
        "window": "#1A1C1E",
        "sidebar": "#171113",
        "card": "#231719",
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
        "table_row_a": "#281B1E",
        "table_row_b": "#24181B",
        "panel_border": "#4A3134",
        "chip_bg": "#3A2427",
        "chip_fg": "#F4EBD0",
        "hover_surface": "#2F2023",
        "scroll_btn": "#5F3134",
        "scroll_btn_hover": "#754046",
    }
    
    FONT = "Segoe UI"

    def __init__(self, parent, on_date_change=None, on_view_order=None, on_print_order=None):
        self.parent = parent
        self.on_date_change = on_date_change
        self.on_view_order = on_view_order
        self.on_print_order = on_print_order
        self._current_date = datetime.now().date()
        
        self.frame = ctk.CTkFrame(
            parent,
            fg_color=self.COLORS["wine_bg"],
            corner_radius=0,
            border_width=0,
        )
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        
        self._build_header()
        self._build_table_area()
        self._build_kpi_area()

    def _build_header(self):
        header = ctk.CTkFrame(self.frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header.grid_columnconfigure(0, weight=1)
        
        title_block = ctk.CTkFrame(header, fg_color="transparent")
        title_block.grid(row=0, column=0, sticky="w")
        
        ctk.CTkLabel(
            title_block, 
            text="Registro de Pedidos", 
            font=(self.FONT, 30, "bold"), 
            text_color=self.COLORS["accent_soft"]
        ).grid(row=0, column=0, sticky="w")
        
        ctk.CTkLabel(
            title_block, 
            text="Historial completo de transacciones y estados de comanda.", 
            font=(self.FONT, 12), 
            text_color=self.COLORS["text_warm"]
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))
        
        # Right aligned date picker
        date_block = ctk.CTkFrame(header, fg_color="transparent")
        date_block.grid(row=0, column=1, sticky="e")
        
        # Date Navigation
        nav_frame = ctk.CTkFrame(date_block, fg_color=self.COLORS["wine_panel"], corner_radius=6, border_width=1, border_color=self.COLORS["panel_border"])
        nav_frame.grid(row=0, column=0)
        
        ctk.CTkButton(
            nav_frame, text="◀", width=30, height=30,
            fg_color="transparent", hover_color=self.COLORS["hover_surface"],
            text_color=self.COLORS["text_warm"], font=(self.FONT, 12, "bold"),
            command=self._prev_day
        ).grid(row=0, column=0, padx=2)
        
        self.lbl_date = ctk.CTkLabel(
            nav_frame, 
            text=f"Fecha: {self._current_date.strftime('%Y-%m-%d')}", 
            font=(self.FONT, 12, "bold"), 
            text_color=self.COLORS["text_primary"],
            width=120
        )
        self.lbl_date.grid(row=0, column=1, padx=5)
        
        ctk.CTkButton(
            nav_frame, text="▶", width=30, height=30,
            fg_color="transparent", hover_color=self.COLORS["hover_surface"],
            text_color=self.COLORS["text_warm"], font=(self.FONT, 12, "bold"),
            command=self._next_day
        ).grid(row=0, column=2, padx=2)
        
        # Export Button
        ctk.CTkButton(
            date_block, 
            text="📥 Exportar Excel", 
            width=140, height=32,
            fg_color="#2EA44F", 
            hover_color="#268841",
            text_color="#FFFFFF", font=(self.FONT, 12, "bold"),
            command=self._export_excel
        ).grid(row=0, column=1, padx=(15, 0))

    def _prev_day(self):
        from datetime import timedelta
        self._current_date -= timedelta(days=1)
        self._update_date_label()
        
    def _next_day(self):
        from datetime import timedelta
        self._current_date += timedelta(days=1)
        self._update_date_label()
        
    def _update_date_label(self):
        self.lbl_date.configure(text=f"Fecha: {self._current_date.strftime('%Y-%m-%d')}")
        if self.on_date_change:
            self.on_date_change(self._current_date)


    def _export_excel(self):
        if hasattr(self, "on_export_excel") and self.on_export_excel:
            self.on_export_excel(self._current_date)

    def _build_table_area(self):
        table_card = ctk.CTkFrame(
            self.frame, 
            fg_color=self.COLORS["wine_panel"], 
            corner_radius=8, 
            border_width=1, 
            border_color=self.COLORS["panel_border"]
        )
        table_card.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 15))
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(1, weight=1)

        # Headers
        headers_frame = ctk.CTkFrame(table_card, fg_color=self.COLORS["wine_soft"], corner_radius=6)
        headers_frame.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 0))
        
        # Columns weights
        col_weights = (1, 2, 2, 2, 2, 2)
        for col, weight in enumerate(col_weights):
            headers_frame.grid_columnconfigure(col, weight=weight, uniform="table_cols")
            
        header_labels = ["FECHA Y HORA", "MESA", "MESERO", "TOTAL", "MÉTODO DE PAGO", "ACCIONES"]
        for col, text in enumerate(header_labels):
            anchor = "center" if text in ["MÉTODO DE PAGO", "ACCIONES"] else "w"
            h = ctk.CTkLabel(
                headers_frame,
                text=text,
                font=(self.FONT, 10, "bold"),
                text_color=self.COLORS["accent_soft"],
                anchor=anchor
            )
            h.grid(row=0, column=col, sticky="ew", padx=12, pady=10)

        # Scrollable Body
        self.table_scroll = ctk.CTkScrollableFrame(
            table_card,
            fg_color="transparent",
            corner_radius=0,
            scrollbar_button_color=self.COLORS["scroll_btn"],
            scrollbar_button_hover_color=self.COLORS["scroll_btn_hover"],
        )
        self.table_scroll.grid(row=1, column=0, sticky="nsew", padx=8, pady=(8, 12))
        
        for col, weight in enumerate(col_weights):
            self.table_scroll.grid_columnconfigure(col, weight=weight, uniform="table_cols")

    def _build_kpi_area(self):
        kpi_container = ctk.CTkFrame(self.frame, fg_color="transparent")
        kpi_container.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        kpi_container.grid_columnconfigure((0, 1, 2), weight=1, uniform="kpi")

        self.lbl_ventas = self._create_kpi_card(kpi_container, 0, "VENTAS MENSUALES", "$0.00")
        self.lbl_pedidos = self._create_kpi_card(kpi_container, 1, "PEDIDOS MENSUALES", "0")
        self.lbl_ticket = self._create_kpi_card(kpi_container, 2, "TICKET PROMEDIO MENSUAL", "$0.00")

    def _create_kpi_card(self, parent, col, title, initial_value):
        card = ctk.CTkFrame(
            parent, 
            fg_color=self.COLORS["wine_panel"], 
            corner_radius=8, 
            border_width=1, 
            border_color=self.COLORS["panel_border"]
        )
        card.grid(row=0, column=col, sticky="ew", padx=(0 if col == 0 else 10, 0 if col == 2 else 10))
        card.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            card, 
            text=title, 
            font=(self.FONT, 10, "bold"), 
            text_color=self.COLORS["text_secondary"]
        ).grid(row=0, column=0, pady=(15, 5))
        
        lbl_value = ctk.CTkLabel(
            card, 
            text=initial_value, 
            font=(self.FONT, 22, "bold"), 
            text_color=self.COLORS["text_primary"]
        )
        lbl_value.grid(row=1, column=0, pady=(0, 15))
        
        return lbl_value

    def actualizar_kpis(self, data):
        self.lbl_ventas.configure(text=f"${data.get('ventas_mensuales', 0.0):,.0f}")
        self.lbl_pedidos.configure(text=f"{int(data.get('pedidos_mensuales', 0))}")
        self.lbl_ticket.configure(text=f"${data.get('ticket_promedio', 0.0):,.0f}")

    def renderizar_tabla(self, historial):
        for widget in self.table_scroll.winfo_children():
            widget.destroy()

        if not historial:
            empty = ctk.CTkLabel(
                self.table_scroll,
                text="No hay pedidos registrados en la fecha seleccionada.",
                font=(self.FONT, 13),
                text_color=self.COLORS["text_secondary"],
            )
            empty.grid(row=0, column=0, columnspan=6, sticky="nsew", pady=30)
            return

        for row_idx, pedido in enumerate(historial):
            row_bg = self.COLORS["table_row_a"] if row_idx % 2 == 0 else self.COLORS["table_row_b"]
            row = ctk.CTkFrame(
                self.table_scroll,
                fg_color=row_bg,
                corner_radius=6,
                border_width=1,
                border_color=self.COLORS["panel_border"],
            )
            row.grid(row=row_idx, column=0, columnspan=6, sticky="ew", padx=4, pady=4)
            
            # Adjusted weights for better layout
            for col, weight in enumerate((1, 2, 2, 2, 2, 2)):
                row.grid_columnconfigure(col, weight=weight, uniform="table_row_cols")

            # 1. HORA
            ctk.CTkLabel(
                row, text=pedido.get("hora", "-"), 
                font=(self.FONT, 11, "bold"), text_color=self.COLORS["text_primary"]
            ).grid(row=0, column=0, sticky="w", padx=12, pady=12)

            # 2. MESA / TIPO PEDIDO
            mesa_val = pedido.get("numero_mesa")
            mesa_text = f"MESA {mesa_val:02d}" if mesa_val else "PARA LLEVAR"
            ctk.CTkLabel(
                row, text=mesa_text, 
                font=(self.FONT, 9, "bold"), text_color=self.COLORS["text_warm"],
                fg_color=self.COLORS["chip_bg"], corner_radius=6, padx=8, pady=4
            ).grid(row=0, column=1, sticky="w", padx=12)

            # 3. MESERO
            mesero_nombre = str(pedido.get("mesero_nombre", "-")).title()
            ctk.CTkLabel(
                row, text=mesero_nombre, 
                font=(self.FONT, 12, "bold"), text_color=self.COLORS["secondary"], anchor="w"
            ).grid(row=0, column=2, sticky="w", padx=12)

            # 4. TOTAL
            ctk.CTkLabel(
                row, text=pedido.get("total_formateado", "$0"), 
                font=(self.FONT, 12, "bold"), text_color=self.COLORS["text_primary"]
            ).grid(row=0, column=3, sticky="w", padx=12)

            # 5. METODO DE PAGO
            metodo = pedido.get("metodo_pago_desc", "PENDIENTE")
            color_txt = pedido.get("color_pago", "#FFFFFF")
            
            pago_frame = ctk.CTkFrame(row, fg_color="transparent")
            pago_frame.grid(row=0, column=4, sticky="ew")
            pago_frame.grid_columnconfigure(0, weight=1)
            
            ctk.CTkLabel(
                pago_frame, text=metodo, 
                font=(self.FONT, 9, "bold"), text_color=color_txt,
                fg_color=self.COLORS["chip_bg"], corner_radius=12, padx=12, pady=5
            ).grid(row=0, column=0)

            # 6. ACCIONES
            acciones_frame = ctk.CTkFrame(row, fg_color="transparent")
            acciones_frame.grid(row=0, column=5, sticky="ew")
            acciones_frame.grid_columnconfigure(0, weight=1)
            
            id_pedido = pedido.get("id_pedido")
            
            btn_ver = ctk.CTkButton(
                acciones_frame, text="Ver Comanda", height=28, width=110, corner_radius=6,
                fg_color=self.COLORS["accent"], hover_color=self.COLORS["accent_hover"],
                text_color=self.COLORS["text_primary"], font=(self.FONT, 11, "bold"),
                command=lambda p=id_pedido: self._handle_view(p)
            )
            btn_ver.grid(row=0, column=0)

    def _handle_view(self, id_pedido):
        if self.on_view_order:
            self.on_view_order(id_pedido)

    def _handle_print(self, id_pedido):
        if self.on_print_order:
            self.on_print_order(id_pedido)

    def mostrar_detalle_pedido(self, detalle, id_pedido):
        # Un modal sencillo para ver los items del pedido
        modal = ctk.CTkToplevel(self.parent)
        modal.title(f"Detalle Pedido #{id_pedido}")
        modal.geometry("450x500")
        modal.resizable(False, False)
        modal.configure(fg_color=self.COLORS["wine_bg"])
        modal.transient(self.parent)
        modal.grab_set()

        content = ctk.CTkFrame(modal, fg_color=self.COLORS["wine_panel"], corner_radius=8, border_width=1, border_color=self.COLORS["panel_border"])
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            content, text=f"Comanda #{id_pedido}", 
            font=(self.FONT, 20, "bold"), text_color=self.COLORS["text_primary"]
        ).pack(anchor="w", padx=20, pady=(20, 5))
        
        scroll = ctk.CTkScrollableFrame(content, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        if not detalle:
            ctk.CTkLabel(scroll, text="No hay items registrados.", text_color=self.COLORS["text_secondary"]).pack(pady=20)
        else:
            total_calc = 0
            for item in detalle:
                f = ctk.CTkFrame(scroll, fg_color="transparent")
                f.pack(fill="x", pady=4)
                f.grid_columnconfigure(1, weight=1)
                
                ctk.CTkLabel(f, text=f"{item['cantidad']}x", font=(self.FONT, 11, "bold"), text_color=self.COLORS["accent_soft"]).grid(row=0, column=0, sticky="w", padx=(0, 10))
                ctk.CTkLabel(f, text=item['producto_nombre'], font=(self.FONT, 11), text_color=self.COLORS["text_primary"]).grid(row=0, column=1, sticky="w")
                ctk.CTkLabel(f, text=f"${float(item['subtotal']):,.0f}", font=(self.FONT, 11, "bold"), text_color=self.COLORS["text_warm"]).grid(row=0, column=2, sticky="e")
                total_calc += float(item['subtotal'])
                
            separator = ctk.CTkFrame(content, height=1, fg_color=self.COLORS["panel_border"])
            separator.pack(fill="x", padx=20, pady=10)
            
            tot_frame = ctk.CTkFrame(content, fg_color="transparent")
            tot_frame.pack(fill="x", padx=20, pady=(0, 20))
            tot_frame.grid_columnconfigure(0, weight=1)
            
            ctk.CTkLabel(tot_frame, text="TOTAL:", font=(self.FONT, 14, "bold"), text_color=self.COLORS["text_secondary"]).grid(row=0, column=0, sticky="w")
            ctk.CTkLabel(tot_frame, text=f"${total_calc:,.0f}", font=(self.FONT, 18, "bold"), text_color=self.COLORS["success"]).grid(row=0, column=1, sticky="e")
            
        ctk.CTkButton(
            content, text="Cerrar", fg_color=self.COLORS["accent"], hover_color=self.COLORS["accent_hover"],
            command=modal.destroy, font=(self.FONT, 12, "bold")
        ).pack(pady=(0, 20))

