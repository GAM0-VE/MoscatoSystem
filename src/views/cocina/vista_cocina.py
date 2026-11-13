import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk

try:
    import winsound
except ImportError:  # pragma: no cover - fallback fuera de Windows
    winsound = None


class CocinaDesignWindow(ctk.CTkFrame):
    """Vista de referencia del monitor de cocina (solo diseno UI)."""

    def __init__(self, master: tk.Misc, usuario: str = "Cocina Central") -> None:
        super().__init__(master)
        self.parent = master
        self.configure(fg_color="#141517")

        self.usuario = usuario
        self._icon_refs: list[ImageTk.PhotoImage] = []
        self._ticket_cards: list[ctk.CTkFrame] = []
        self._board_canvas: tk.Canvas | None = None
        self._board_content: ctk.CTkFrame | None = None
        self.scroll_frame: ctk.CTkFrame | None = None
        self._board_host: ctk.CTkFrame | None = None
        self._board_window_id: int | None = None
        self._board_layout_pending = False
        self._nav_buttons: dict[str, ctk.CTkButton] = {}
        self._active_section = "kitchen"
        self._main_frame: ctk.CTkFrame | None = None
        self._stat_labels: dict[str, ctk.CTkLabel] = {}
        self._notificacion_label: ctk.CTkLabel | None = None
        self._notificacion_after_id: str | None = None
        self.controlador = None

        self._build_layout()
        self._update_timers_loop()

    def _update_timers_loop(self) -> None:
        import time
        ahora = time.time()
        for card in getattr(self, "_ticket_cards", []):
            if hasattr(card, "time_label") and hasattr(card, "ts_envio"):
                ts = card.ts_envio
                if ts > 0:
                    delta = int(ahora - ts)
                    if delta < 0: delta = 0
                    minutos = delta // 60
                    segundos = delta % 60
                    card.time_label.configure(text=f" {minutos:02d}:{segundos:02d}")
        self.after(1000, self._update_timers_loop)

    def _build_layout(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_main_panel()
        self._show_section("kitchen")

    def _build_main_panel(self) -> None:
        self._main_frame = ctk.CTkFrame(self, fg_color="#180C0D", corner_radius=0)
        self._main_frame.grid(row=0, column=0, sticky="nsew")
        self._main_frame.grid_columnconfigure(0, weight=1)
        self._main_frame.grid_rowconfigure(0, weight=1)

    def _render_kitchen_view(self) -> None:
        if self._main_frame is None:
            return

        self._main_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self._main_frame.grid_rowconfigure(0, weight=0)
        self._main_frame.grid_rowconfigure(1, weight=0)
        self._main_frame.grid_rowconfigure(2, weight=1)
        self._build_header(self._main_frame)
        self._build_stats(self._main_frame)
        self._build_board(self._main_frame)

    def _render_placeholder(self, section: str) -> None:
        if self._main_frame is None:
            return

        title_map = {
            "orders": "Vista Orders",
            "inventory": "Vista Inventory",
            "menu": "Vista Menu",
            "help": "Centro de Ayuda",
        }
        subtitle_map = {
            "orders": "Aqui se mostrara el historial y despacho de ordenes para cocina.",
            "inventory": "Aqui se mostraran niveles de stock y alertas de reposicion.",
            "menu": "Aqui se mostraran recetas y estatus de disponibilidad del menu.",
            "help": "Aqui se mostraran guias rapidas y recomendaciones operativas.",
        }

        panel = ctk.CTkFrame(
            self._main_frame,
            fg_color="#1E1314",
            border_color="#3A2A2B",
            border_width=1,
            corner_radius=12,
        )
        panel.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)

        ctk.CTkLabel(
            panel,
            text=title_map.get(section, "Modulo"),
            text_color="#F4EBD0",
            font=("Segoe UI", 34, "bold"),
        ).pack(anchor="w", padx=24, pady=(24, 8))
        ctk.CTkLabel(
            panel,
            text=subtitle_map.get(section, "Seccion en construccion."),
            text_color="#D7CBAE",
            font=("Segoe UI", 14),
            wraplength=840,
            justify="left",
        ).pack(anchor="w", padx=24)

    def _build_header(self, parent: tk.Misc) -> None:
        header = ctk.CTkFrame(parent, fg_color="#180C0D", corner_radius=0, height=50)
        header.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=(8, 2))
        header.grid_propagate(False)

        ctk.CTkLabel(header, text="MOSCATO", text_color="#F4EBD0", font=("Segoe UI", 34, "bold")).pack(side="left", padx=(8, 8))
        ctk.CTkFrame(header, fg_color="#7A3931", width=2, height=38, corner_radius=0).pack(side="left", padx=8, pady=10)
        ctk.CTkLabel(header, text=self.usuario, text_color="#F09F86", font=("Segoe UI", 20, "bold")).pack(side="left")

        # Botón de Salir - Ahora limpio en el extremo derecho superior
        self._nav_buttons["logout"] = ctk.CTkButton(
            header,
            text="Salir",
            image=self._make_icon("logout", "#F4EBD0", size=14),
            compound="left",
            fg_color="#8C1A11",
            hover_color="#A1241A",
            text_color="#F4EBD0",
            font=("Segoe UI", 12, "bold"),
            width=90,
            height=34,
            corner_radius=8,
            command=lambda: self._show_section("logout")
        )
        self._nav_buttons["logout"].pack(side="right", padx=(8, 8), pady=8)

    def _build_stats(self, parent: tk.Misc) -> None:
        self._stat_labels = {}
        wrap = ctk.CTkFrame(parent, fg_color="#180C0D", corner_radius=0)
        wrap.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=(2, 8))
        wrap.grid_columnconfigure((0, 1, 2, 3), weight=1)

        cards = [
            ("PEDIDOS ACTIVOS", "12", "clipboard", "#EFA894"),
            ("TIEMPO PROMEDIO", "14:20", "timer", "#F4EBD0"),
            ("EN PREPARACION", "08", "flame", "#FFB000"),
            ("PENDIENTES", "04", "alert", "#FF9E8F"),
        ]

        for idx, (title, value, icon, accent) in enumerate(cards):
            stat = ctk.CTkFrame(wrap, fg_color="#2A1718", border_color="#4A2D2D", border_width=1, corner_radius=8)
            stat.grid(row=0, column=idx, sticky="ew", padx=6)
            stat.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(stat, text=title, text_color="#E8DABF", font=("Segoe UI", 9, "bold")).grid(
                row=0, column=0, sticky="w", padx=10, pady=(8, 2)
            )
            value_label = ctk.CTkLabel(stat, text=value, text_color=accent, font=("Segoe UI", 38, "bold"))
            value_label.grid(
                row=1, column=0, sticky="w", padx=10, pady=(0, 8)
            )
            self._stat_labels[title] = value_label
            ctk.CTkLabel(stat, text="", image=self._make_icon(icon, accent, size=20), fg_color="transparent").grid(
                row=1, column=1, sticky="e", padx=(0, 10), pady=(0, 6)
            )

    def actualizar_estadisticas(self, pedidos_activos, tiempo_promedio, en_prep, pendientes) -> None:
        stats = {
            "PEDIDOS ACTIVOS": str(pedidos_activos),
            "TIEMPO PROMEDIO": str(tiempo_promedio),
            "EN PREPARACION": str(en_prep).zfill(2),
            "PENDIENTES": str(pendientes).zfill(2),
        }
        for titulo, valor in stats.items():
            label = self._stat_labels.get(titulo)
            if label is not None:
                label.configure(text=valor)

    def _build_board(self, parent: tk.Misc) -> None:
        self.scroll_frame = ctk.CTkScrollableFrame(
            parent,
            fg_color="#180C0D",
            corner_radius=0,
            scrollbar_button_color="#16181A",
            scrollbar_button_hover_color="#2A2324",
        )
        self.scroll_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=(0, 10))
        self.scroll_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="columna_estricta")

        self._board_content = self.scroll_frame
        self._ticket_cards.clear()
        self.after_idle(self._layout_board_cards)

    def _layout_board_cards(self) -> None:
        if not self.scroll_frame:
            return

        for index, card in enumerate(self._ticket_cards):
            row_calc = index // 3
            col_calc = index % 3
            card.grid(row=row_calc, column=col_calc, padx=15, pady=15, sticky="nsew")

    def _kitchen_ticket(self, parent: tk.Misc, data: dict, callback_notificar) -> ctk.CTkFrame:
        card = ctk.CTkFrame(
            parent,
            fg_color="#2A1718",
            border_color=data["borde"],
            border_width=1,
            corner_radius=8,
        )

        header_color = data.get("header_bg", "#4B360F")
        head = ctk.CTkFrame(card, fg_color=header_color, corner_radius=6)
        head.pack(fill="x", padx=4, pady=4)
        head.grid_columnconfigure(0, weight=1)

        label_type = "MESA" if not str(data["mesa"]).startswith("#") else "PARA LLEVAR"
        ctk.CTkLabel(head, text=label_type, text_color="#D5BFA0", font=("Segoe UI", 8, "bold")).grid(
            row=0, column=0, sticky="w", padx=8, pady=(5, 0)
        )

        ctk.CTkLabel(
            head,
            text=f"TICKET #{int(data.get('id_pedido', 0)):05d}",
            text_color="#F4EBD0",
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=1, sticky="e", padx=8, pady=(5, 0))

        mesa_color = "#FFB000" if data["estado"] != "ENVIADO A COCINA" else "#FF7C7C"
        ctk.CTkLabel(head, text=data["mesa"], text_color=mesa_color, font=("Segoe UI", 33, "bold")).grid(
            row=1, column=0, sticky="w", padx=8, pady=(0, 6)
        )

        time_wrap = ctk.CTkFrame(head, fg_color="transparent")
        time_wrap.grid(row=0, column=1, rowspan=2, sticky="ne", padx=8, pady=6)
        ctk.CTkLabel(time_wrap, text="", image=self._make_icon("clock", "#F4EBD0", size=12), fg_color="transparent").pack(side="left")
        
        # Guardamos el label y el timestamp para actualizar el cronometro despues
        time_lbl = ctk.CTkLabel(time_wrap, text=f" 00:00", text_color="#F4EBD0", font=("Segoe UI", 12, "bold"))
        time_lbl.pack(side="left")
        card.time_label = time_lbl
        card.ts_envio = data.get("timestamp_envio", 0.0)

        ctk.CTkLabel(
            head,
            text=data["estado"],
            fg_color=data["estado_bg"],
            text_color="#F4EBD0",
            corner_radius=8,
            font=("Segoe UI", 8, "bold"),
            padx=7,
            pady=2,
        ).grid(row=2, column=1, sticky="e", padx=8, pady=(0, 6))

        body = tk.Frame(card, bg="#2A1718")
        body.pack(fill="both", expand=True, padx=8, pady=(8, 6))

        dishes = tk.Frame(body, bg="#2A1718")
        dishes.pack(side="top", anchor="w", fill="x", expand=False)

        for item in data["items"]:
            qty = f"{int(item.get('cantidad') or 1)}x"
            name = str(item.get("nombre") or "ITEM")
            detalle = str(item.get("detalle") or "").strip()

            row = tk.Frame(dishes, bg="#2A1718")
            row.pack(side="top", anchor="w", fill="x", expand=False, pady=(0, 4))
            ctk.CTkLabel(row, text=qty, text_color="#FF9C00", font=("Segoe UI", 22, "bold"), fg_color="#2A1718").pack(
                side="left", anchor="w", expand=False
            )
            ctk.CTkLabel(
                row,
                text=f" {name}",
                text_color="#F4EBD0",
                font=("Segoe UI", 14, "bold"),
                wraplength=220,
                justify="left",
                fg_color="#2A1718"
            ).pack(side="left", anchor="w", fill="x", expand=False)

            if detalle:
                ctk.CTkLabel(
                    row,
                    text=f"   {detalle}",
                    text_color="#A4A4A4",
                    font=("Segoe UI", 11, "italic"),
                    wraplength=220,
                    justify="left",
                    fg_color="#2A1718"
                ).pack(side="top", anchor="w", expand=False, pady=(0, 6))

            tk.Frame(dishes, bg="#5C3A3A", height=1).pack(
                side="top", anchor="w", fill="x", expand=False, pady=(2, 4)
            )

        tk.Frame(body, bg="#2A1718").pack(side="top", fill="both", expand=True)

        ctk.CTkButton(
            card,
            text=data.get("accion_texto", "EN PREPARACION"),
            image=self._make_icon("check", "#F4EBD0", size=14),
            compound="left",
            fg_color=data.get("accion_bg", "#49A54A"),
            hover_color=data.get("accion_hover", "#5EB95E"),
            text_color="#F4EBD0",
            font=("Segoe UI", 12, "bold"),
            height=38,
            state="normal" if data.get("accion_habilitada", True) else "disabled",
            command=lambda id_p=data.get("id_pedido", 0), s=data.get("siguiente_estado", "En preparación"): callback_notificar(id_p, s),
        ).pack(side="bottom", fill="x", padx=10, pady=10)

        return card

    def actualizar_monitor(self, nuevos_pedidos: list[dict], callback_notificar) -> None:
        """Compara con el estado anterior y solo borra/renderiza los tickets si hubo un cambio."""
        import json
        def _get_sort_key(p):
            return str(p.get("id_pedido", p.get("mesa", "")))
            
        last_pedidos_sorted = sorted(getattr(self, "_last_pedidos", []), key=_get_sort_key)
        nuevos_pedidos_sorted = sorted(nuevos_pedidos, key=_get_sort_key)
        
        estado_actual = json.dumps(last_pedidos_sorted, sort_keys=True)
        nuevo_estado = json.dumps(nuevos_pedidos_sorted, sort_keys=True)

        nuevos_ids = {p.get("id_pedido", 0) for p in nuevos_pedidos}
        
        if not hasattr(self, "_pedidos_activos_ids"):
            self._pedidos_activos_ids = nuevos_ids
        else:
            if nuevos_ids - self._pedidos_activos_ids:
                self._reproducir_campanita()
            self._pedidos_activos_ids = nuevos_ids

        if estado_actual == nuevo_estado:
            return  # No hay cambios estructurales, no redibujamos para no romper el reloj ni parpadear

        self._last_pedidos = nuevos_pedidos

        for card in self._ticket_cards:
            card.destroy()
        self._ticket_cards.clear()

        if self._board_content:
            self._ticket_cards = [
                self._kitchen_ticket(self._board_content, data, callback_notificar)
                for data in nuevos_pedidos
            ]

        self._layout_board_cards()

    def notificar_nueva_comanda(self, ticket: int = 0, id_pedido: int = 0, texto: str | None = None) -> None:
        if texto:
            mensaje = texto
        elif ticket > 0:
            mensaje = f"Nueva comanda: TICKET #{ticket:05d}"
        elif id_pedido > 0:
            mensaje = f"Nueva comanda: PEDIDO #{id_pedido:05d}"
        else:
            mensaje = "Nueva comanda recibida"

        self._mostrar_notificacion(mensaje, "#8A6317")
        self._reproducir_campanita()

    def notificar_cancelacion(self, ticket: int) -> None:
        mensaje = f"ATENCIÓN: TICKET #{ticket:05d} fue CANCELADO"
        self._mostrar_notificacion(mensaje, "#8C1A11")
        try:
            import winsound
            winsound.Beep(500, 300)
            winsound.Beep(400, 400)
        except Exception:
            self.bell()

    def _reproducir_campanita(self) -> None:
        try:
            import winsound
            # Sonido de entrada de comanda en cocina (Doble Ding rápido y agudo)
            winsound.Beep(1200, 150)
            winsound.Beep(1200, 250)
        except Exception:
            self.bell()

    def _mostrar_notificacion(self, texto: str, color: str = "#2F5C36") -> None:
        if self._notificacion_label is None or not self._notificacion_label.winfo_exists():
            self._notificacion_label = ctk.CTkLabel(
                self,
                text=texto,
                fg_color=color,
                text_color="#F4EBD0",
                corner_radius=10,
                font=("Segoe UI", 11, "bold"),
                padx=12,
                pady=6,
            )
        else:
            self._notificacion_label.configure(text=texto, fg_color=color)

        self._notificacion_label.place(relx=1.0, x=-18, y=18, anchor="ne")

        if self._notificacion_after_id is not None:
            self.after_cancel(self._notificacion_after_id)
        self._notificacion_after_id = self.after(3000, self._ocultar_notificacion)

    def _ocultar_notificacion(self) -> None:
        if self._notificacion_label is not None and self._notificacion_label.winfo_exists():
            self._notificacion_label.place_forget()
        self._notificacion_after_id = None

    def _show_section(self, section: str) -> None:
        self._active_section = section
        self._update_nav_state()

        if section == "logout":
            self._logout_to_login()
            return

        if self._main_frame is None:
            return

        for child in self._main_frame.winfo_children():
            child.destroy()

        if section == "kitchen":
            self._render_kitchen_view()
        else:
            self._render_placeholder(section)

    def _update_nav_state(self) -> None:
        for section, button in self._nav_buttons.items():
            if section == "logout":
                continue
            is_active = section == self._active_section
            button.configure(
                fg_color="#9E1F14" if is_active else "#1A0D0C",
                hover_color="#B52619" if is_active else "#2A1A18",
            )

    def _logout_to_login(self) -> None:
        controlador = getattr(self, "controlador", None)
        if controlador is not None and hasattr(controlador, "desactivar"):
            controlador.desactivar()
        if hasattr(self.parent, "show_login"):
            self.parent.show_login()
        else:
            self.destroy()

    def destroy(self) -> None:
        controlador = getattr(self, "controlador", None)
        if controlador is not None and hasattr(controlador, "desactivar"):
            controlador.desactivar()
            self.controlador = None
        super().destroy()

    def _make_icon(self, name: str, color: str, size: int = 18) -> ImageTk.PhotoImage:
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        p = max(2, size // 8)
        s = max(1, size // 8)

        if name == "status":
            draw.ellipse((p + 1, p + 1, size - p - 1, size - p - 1), fill=color)
        elif name == "wifi":
            draw.arc((p, p + 3, size - p, size - p + 1), 200, 340, fill=color, width=s)
            draw.arc((p + 3, p + 6, size - p - 3, size - p + 1), 210, 330, fill=color, width=s)
            draw.ellipse((size // 2 - 1, size - p - 3, size // 2 + 1, size - p - 1), fill=color)
        elif name == "bell":
            draw.arc((p + 1, p + 1, size - p - 1, size - p), 200, 340, fill=color, width=s)
            draw.line((p + 3, size - p - 4, size - p - 3, size - p - 4), fill=color, width=s)
            draw.ellipse((size // 2 - 1, size - p - 2, size // 2 + 1, size - p), fill=color)
        elif name == "user":
            draw.ellipse((p + 3, p + 1, size - p - 3, p + 7), outline=color, width=s)
            draw.arc((p + 1, p + 6, size - p - 1, size - p), 200, 340, fill=color, width=s)
        elif name == "clipboard":
            draw.rounded_rectangle((p, p + 2, size - p, size - p), radius=2, outline=color, width=s)
            draw.rectangle((size // 2 - 3, p, size // 2 + 3, p + 3), outline=color, width=s)
        elif name == "timer":
            draw.ellipse((p + 1, p + 3, size - p - 1, size - p), outline=color, width=s)
            draw.line((size // 2, size // 2 + 1, size // 2, p + 6), fill=color, width=s)
            draw.line((size // 2, size // 2 + 1, size // 2 + 4, size // 2 + 1), fill=color, width=s)
        elif name == "flame":
            draw.polygon([(size // 2, p), (size - p - 2, size - p - 2), (size // 2 + 1, size - p), (p + 2, size - p - 2)], outline=color, fill=None)
        elif name == "alert":
            draw.line((size // 2, p + 1, size // 2, size - p - 5), fill=color, width=s)
            draw.ellipse((size // 2 - 1, size - p - 3, size // 2 + 1, size - p - 1), fill=color)
        elif name == "clock":
            draw.ellipse((p, p, size - p, size - p), outline=color, width=s)
            draw.line((size // 2, size // 2, size // 2, p + 3), fill=color, width=s)
            draw.line((size // 2, size // 2, size - p - 3, size // 2), fill=color, width=s)
        elif name == "check":
            draw.line((p + 1, size // 2, size // 2 - 1, size - p - 2), fill=color, width=s)
            draw.line((size // 2 - 1, size - p - 2, size - p - 1, p + 2), fill=color, width=s)
        elif name == "orders":
            draw.rounded_rectangle((p, p, size - p, size - p), radius=2, outline=color, width=s)
            draw.line((p + 3, size // 2, size - p - 3, size // 2), fill=color, width=s)
        elif name == "kitchen":
            draw.arc((p, p + 1, size - p, size - p), 180, 360, fill=color, width=s)
            draw.line((p + 1, size // 2, size - p - 1, size // 2), fill=color, width=s)
        elif name == "inventory":
            draw.rectangle((p + 2, p + 2, size - p - 2, size - p - 2), outline=color, width=s)
            draw.line((p + 5, size // 2, size - p - 5, size // 2), fill=color, width=s)
        elif name == "menu":
            for y in (p + 3, size // 2, size - p - 3):
                draw.line((p, y, size - p, y), fill=color, width=s)
        elif name == "help":
            draw.ellipse((p, p, size - p, size - p), outline=color, width=s)
            draw.line((size // 2, p + 4, size // 2, size // 2), fill=color, width=s)
            draw.ellipse((size // 2 - 1, size - p - 3, size // 2 + 1, size - p - 1), fill=color)
        elif name == "logout":
            draw.rectangle((p + 5, p, size - p - 1, size - p), outline=color, width=s)
            draw.line((p, size // 2, size - p - 4, size // 2), fill=color, width=s)
            draw.polygon([(size - p - 6, size // 2 - 4), (size - p - 1, size // 2), (size - p - 6, size // 2 + 4)], fill=color)
        else:
            draw.ellipse((p, p, size - p, size - p), outline=color, width=s)

        icon = ImageTk.PhotoImage(image)
        self._icon_refs.append(icon)
        return icon