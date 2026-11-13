import os
import tkinter as tk
import threading
from typing import Callable

try:
    import winsound
except ImportError:  # pragma: no cover - fallback fuera de Windows
    winsound = None

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk

from src.core.event_bus import event_bus
from src.controllers.mesas.controlador_mesas import MesasController
from src.controllers.pedidos.controlador_pedido_actual import ControladorPedidoActual
from src.controllers.pedidos.controlador_mesero import ControladorMesero
from src.models.mesas.modelo_mesas import MesasModel
from src.models.pedidos.modelo_pedido_actual import ModeloPedidoActual
from src.models.pedidos.modelo_mesero import ModeloMesero
from src.models.productos.imagenes_menu import buscar_imagen_local
from src.views.mesas.vista_mesas import MesasView
from src.views.pedidos.vista_pedido_actual import VistaPedidoActual


class MeseroDesignWindow(ctk.CTkFrame):
    """Vista de referencia del terminal de mesero (solo diseno UI)."""

    SYNC_PEDIDOS_MS = 3000

    def __init__(self, master: tk.Misc, usuario: str, mesa_actual: str = "Seleccione Mesa") -> None:
        super().__init__(master)
        self.parent = master
        self.configure(fg_color="#141517")

        self.usuario = usuario
        self.mesa_actual = mesa_actual
        self._icon_refs: list[ImageTk.PhotoImage] = []
        self._product_cards: list[ctk.CTkFrame] = []
        self._product_card_pool: list[ctk.CTkFrame] = []
        self._catalog_layout_pending = False
        self._catalog_canvas: tk.Canvas | None = None
        self._catalog_content: ctk.CTkFrame | None = None
        self._catalog_host: ctk.CTkFrame | None = None
        self._catalog_window_id: int | None = None
        self._center_frame: ctk.CTkFrame | None = None
        self._order_frame: ctk.CTkFrame | None = None
        self._section_frame: ctk.CTkFrame | None = None
        self._mesa_badge_label: ctk.CTkLabel | None = None
        self._nav_buttons: dict[str, ctk.CTkButton] = {}
        self._active_section = "orders"
        self._ticket_numero = 1
        self._ticket_label: ctk.CTkLabel | None = None
        self._pedido_items_container: ctk.CTkFrame | None = None
        self._pedido_vacio_label: ctk.CTkLabel | None = None
        self._categoria_botones: dict[str, ctk.CTkButton] = {}
        self._categoria_actual = "Comida China"
        
        self.modelo_mesero = ModeloMesero()
        self.controlador_mesero = ControladorMesero(self.modelo_mesero)
        
        self._pedido_actual_model: ModeloPedidoActual | None = None
        self._pedido_actual_view: VistaPedidoActual | None = None
        self._pedido_actual_controller: ControladorPedidoActual | None = None
        self._mesas_model: MesasModel | None = None
        self._mesas_view: MesasView | None = None
        self._mesas_controller: MesasController | None = None
        self._mesa_seleccionada_id: int | None = None
        self._mesas_por_id: dict[int, dict[str, object]] = {}
        
        self._ordenes_pendientes: list[dict[str, object]] = []
        self._ordenes_auditoria: list[dict[str, object]] = []
        
        self._notificacion_label: ctk.CTkLabel | None = None
        self._notificacion_after_id: str | None = None
        self._pendientes_window: ctk.CTkToplevel | None = None
        self._pendientes_list_container: ctk.CTkFrame | None = None
        self._pendientes_detail_container: ctk.CTkFrame | None = None
        self._ultimo_error_bd: str | None = None
        self._pedidos_estado_notificado: dict[int, str] = {}
        self._tickets_por_pedido: dict[int, int] = {}
        
        self._evento_pedido_listo = self._on_pedido_listo_event
        self._evento_mesa_seleccionada = self._on_mesa_seleccionada_event
        self._evento_pedidos_actualizados = self._on_pedidos_actualizados
        self._evento_items_cambiados = self._on_pedido_actual_items_cambiados
        
        event_bus.subscribe("pedido.listo", self._evento_pedido_listo)
        event_bus.subscribe("mesa.seleccionada", self._evento_mesa_seleccionada)
        event_bus.subscribe("pedidos.pendientes_actualizados", self._evento_pedidos_actualizados)
        event_bus.subscribe("pedido_actual.items_cambiados", self._evento_items_cambiados)

        self._productos_por_categoria: dict[str, list[dict[str, object]]] = {}
        self._cargar_productos_catalogo()

        self._build_layout()
        self.controlador_mesero.start_polling(5)

    def _build_layout(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self._center_frame = self._build_center_panel()
        self._order_frame = self._build_order_panel()
        self._section_frame = ctk.CTkFrame(self, fg_color="#141517", corner_radius=0)
        self._section_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self._section_frame.grid_remove()
        self._show_section("orders")

    def _nav_button(
        self,
        parent: tk.Misc,
        text: str,
        icon_name: str,
        section: str,
        active: bool = False,
    ) -> ctk.CTkButton:
        bg = "#9E1F14" if active else "#1A0D0C"
        hover = "#B52619" if active else "#2A1A18"
        icon = self._make_icon(icon_name, "#F4EBD0")

        return ctk.CTkButton(
            parent,
            text=f"  {text}",
            image=icon,
            compound="left",
            anchor="w",
            corner_radius=8,
            fg_color=bg,
            hover_color=hover,
            text_color="#F4EBD0",
            font=("Segoe UI", 14, "bold"),
            height=42,
            command=lambda s=section: self._show_section(s),
        )

    def _build_center_panel(self) -> ctk.CTkFrame:
        center = ctk.CTkFrame(self, fg_color="#16181A", corner_radius=0)
        center.grid(row=0, column=0, sticky="nsew")
        center.grid_columnconfigure(0, weight=1)
        center.grid_rowconfigure(3, weight=1)

        top = ctk.CTkFrame(center, fg_color="#201011", corner_radius=0, height=102)
        top.grid(row=0, column=0, sticky="ew")
        top.grid_propagate(False)

        ctk.CTkLabel(
            top,
            text="MOSCATO",
            text_color="#F4EBD0",
            font=("Segoe UI", 20, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(8, 0))

        ctk.CTkLabel(
            top,
            text="Plano de Mesas",
            text_color="#F4EBD0",
            font=("Segoe UI", 29, "bold"),
        ).grid(row=1, column=0, sticky="w", padx=14, pady=(0, 0))

        ctk.CTkLabel(
            top,
            text="Seleccione una mesa para iniciar o editar pedido",
            text_color="#E5D7BC",
            font=("Segoe UI", 11, "bold"),
        ).grid(row=2, column=0, sticky="w", padx=14, pady=(1, 8))

        legend = ctk.CTkFrame(top, fg_color="transparent")
        legend.grid(row=2, column=1, sticky="e", padx=12)
        self._legend_item(legend, "#78F0A6", "LIBRE").grid(row=0, column=0, padx=8)
        self._legend_item(legend, "#FF8E7A", "OCUPADA").grid(row=0, column=1, padx=8)
        self._legend_item(legend, "#FFC94A", "ATENCION").grid(row=0, column=2, padx=8)

        mesas_wrap = ctk.CTkFrame(center, fg_color="transparent")
        mesas_wrap.grid(row=1, column=0, sticky="ew", padx=12, pady=(8, 6))
        mesas_wrap.grid_columnconfigure(0, weight=1)

        mesas_canvas = tk.Canvas(mesas_wrap, bg="#16181A", bd=0, highlightthickness=0, height=92)
        mesas_canvas.grid(row=0, column=0, sticky="ew")

        mesas_scroll = tk.Scrollbar(
            mesas_wrap,
            orient="horizontal",
            command=mesas_canvas.xview,
            troughcolor="#16181A",
            bg="#16181A",
            activebackground="#2A2324",
            width=5,
            highlightthickness=0,
            bd=0,
            relief="flat",
        )
        mesas_scroll.grid(row=1, column=0, sticky="ew", pady=(2, 0))
        mesas_canvas.configure(xscrollcommand=mesas_scroll.set)

        self._mesas_view = MesasView(mesas_canvas, columnas=10)
        mesas_canvas_window = mesas_canvas.create_window((0, 0), window=self._mesas_view.frame, anchor="nw")

        def _sync_mesas_scrollregion(_event: tk.Event | None = None) -> None:
            mesas_canvas.configure(scrollregion=mesas_canvas.bbox("all"))

        def _sync_mesas_canvas(event: tk.Event) -> None:
            mesas_canvas.itemconfigure(mesas_canvas_window, height=event.height)
            mesas_canvas.configure(scrollregion=mesas_canvas.bbox("all"))

        self._mesas_view.frame.bind("<Configure>", _sync_mesas_scrollregion)
        mesas_canvas.bind("<Configure>", _sync_mesas_canvas)
        self._inicializar_plano_mesas()
        mesas_canvas.xview_moveto(0.0)

        categorias = ctk.CTkFrame(center, fg_color="transparent")
        categorias.grid(row=2, column=0, sticky="ew", padx=12, pady=(4, 8))
        categorias.grid_columnconfigure((0, 1, 2, 3), weight=1)

        chips = ["Comida China", "Combos", "Promos", "Bebidas"]
        for idx, chip in enumerate(chips):
            boton = self._chip(
                categorias,
                chip,
                active=(chip == self._categoria_actual),
                command=lambda c=chip: self._mostrar_productos_categoria(c),
            )
            boton.grid(row=0, column=idx, sticky="ew", padx=4)
            self._categoria_botones[chip] = boton

        self._build_catalog(center)
        return center

    def _legend_item(self, parent: tk.Misc, color: str, text: str) -> ctk.CTkFrame:
        wrap = ctk.CTkFrame(parent, fg_color="transparent")
        ctk.CTkLabel(wrap, text="●", text_color=color, font=("Segoe UI", 10, "bold")).pack(side="left")
        ctk.CTkLabel(wrap, text=f" {text}", text_color="#E5D7BC", font=("Segoe UI", 9, "bold")).pack(side="left")
        return wrap

    def _mesa_card(self, parent: tk.Misc, mesa: str, estado: str, bg_card: str) -> ctk.CTkFrame:
        border = "#3A3030"
        hover_bg = "#3A3030"
        card = ctk.CTkFrame(
            parent,
            fg_color=bg_card,
            border_color=border,
            border_width=1,
            corner_radius=6,
            height=72,
            width=176,
        )
        card.pack_propagate(False)
        card.configure(cursor="hand2")

        mesa_label = ctk.CTkLabel(card, text=mesa, text_color="#F3E6CC", font=("Segoe UI", 26, "bold"))
        mesa_label.pack(anchor="w", padx=10, pady=(8, 0))

        estado_label = ctk.CTkLabel(card, text=estado, text_color="#F3E6CC", font=("Segoe UI", 11, "bold"))
        estado_label.pack(anchor="w", padx=10, pady=(1, 8))

        def _on_click(_event: tk.Event | None = None) -> None:
            self._select_mesa(mesa)

        def _on_enter(_event: tk.Event | None = None) -> None:
            card.configure(fg_color=hover_bg)

        def _on_leave(_event: tk.Event | None = None) -> None:
            card.configure(fg_color=bg_card)

        for widget in (card, mesa_label, estado_label):
            widget.bind("<Button-1>", _on_click)
            widget.bind("<Enter>", _on_enter)
            widget.bind("<Leave>", _on_leave)
        return card

    def _normalize_mesa_text(self, mesa: str) -> str:
        value = str(mesa).strip().upper()
        if value.startswith("MESA "):
            return value
        if value.startswith("M") and value[1:].isdigit():
            return f"MESA {value[1:]}"
        return value

    def _select_mesa(self, mesa: str) -> None:
        self.mesa_actual = self._normalize_mesa_text(mesa)
        if self._pedido_actual_controller is not None:
            self._pedido_actual_controller.establecer_mesa(self.mesa_actual)
        if self._mesa_badge_label is not None:
            self._mesa_badge_label.configure(text=self.mesa_actual)

    def _chip(
        self,
        parent: tk.Misc,
        text: str,
        active: bool = False,
        command: Callable[[], None] | None = None,
    ) -> ctk.CTkButton:
        bg = "#8C1A11" if active else "#3A2B2A"
        return ctk.CTkButton(
            parent,
            text=text,
            corner_radius=8,
            fg_color=bg,
            hover_color="#A62216",
            text_color="#F4EBD0",
            font=("Segoe UI", 11, "bold"),
            height=34,
            command=command if command is not None else (lambda: None),
        )

    def _build_catalog(self, center: tk.Misc) -> None:
        list_wrap = ctk.CTkFrame(center, fg_color="#0F1012", corner_radius=8)
        list_wrap.grid(row=3, column=0, sticky="nsew", padx=12, pady=(0, 12))
        list_wrap.grid_columnconfigure(0, weight=1)
        list_wrap.grid_rowconfigure(0, weight=1)

        canvas = tk.Canvas(list_wrap, bg="#0F1012", bd=0, highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(
            list_wrap,
            orient="vertical",
            command=canvas.yview,
            troughcolor="#0F1012",
            bg="#16181A",
            activebackground="#2A2324",
            width=5,
            highlightthickness=0,
            bd=0,
            relief="flat",
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        content = ctk.CTkFrame(canvas, fg_color="#0F1012", corner_radius=0)
        self._catalog_window_id = canvas.create_window((0, 0), window=content, anchor="nw")

        self._catalog_canvas = canvas
        self._catalog_content = content
        self._catalog_host = list_wrap

        content.bind("<Configure>", self._update_catalog_scrollregion)
        list_wrap.bind("<Configure>", self._schedule_catalog_layout)
        canvas.bind("<Configure>", self._on_catalog_canvas_configure)

        self._mostrar_productos_categoria(self._categoria_actual)

    def _schedule_catalog_layout(self, _event: tk.Event | None = None) -> None:
        if self._catalog_layout_pending:
            return
        self._catalog_layout_pending = True
        self.after_idle(self._layout_catalog_cards)

    def _layout_catalog_cards(self) -> None:
        self._catalog_layout_pending = False
        if not self._catalog_content or not self._catalog_canvas:
            return

        available_width = max(1, self._catalog_canvas.winfo_width() - 20)
        columns = 4

        for index, card in enumerate(self._product_cards):
            card.grid_forget()
            row = index // columns
            column = index % columns
            card.grid(row=row, column=column, sticky="nsew", padx=7, pady=7)
            card.configure(width=max(235, available_width // columns - 16))
            if hasattr(card, "descripcion_label"):
                card.descripcion_label.configure(wraplength=max(170, available_width // columns - 28))

        for col_idx in range(len(self._product_cards)):
            self._catalog_content.grid_columnconfigure(col_idx, weight=0)
        for col_idx in range(columns):
            self._catalog_content.grid_columnconfigure(col_idx, weight=1, uniform="catalog")

        self._update_catalog_scrollregion()

    def _mostrar_productos_categoria(self, categoria: str) -> None:
        if self._catalog_content is None:
            return

        self._categoria_actual = categoria
        self._actualizar_estilo_categorias()

        # Limpiar catálogo (sin widget pooling para evitar cruce de estados)
        for widget in self._catalog_content.winfo_children():
            widget.destroy()
        self._product_cards.clear()

        productos = self._productos_por_categoria.get(categoria, [])

        import re
        for producto in productos:
            nombre_limpio = re.sub(r'(?i)familiares?', '', str(producto["nombre"]))
            nombre_limpio = ' '.join(nombre_limpio.split())
            precio_formateado = f"${producto['precio']:,.0f}".replace(',', '.')
            
            card = self._product_card(
                self._catalog_content,
                nombre_limpio,
                precio_formateado,
                str(producto.get("descripcion", "")),
                None
            )
            card.image_label.configure(text="Sin foto")
            
            # Hover effects
            def on_enter(e, c=card):
                c.configure(border_width=2, border_color="#DCCAA8")
            def on_leave(e, c=card):
                c.configure(border_width=0)
                
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)
            
            self._enlazar_click_producto(card, producto)
            self._product_cards.append(card)

        if not self._product_cards:
            lbl = ctk.CTkLabel(
                self._catalog_content,
                text="Sin productos en esta categoria por ahora",
                text_color="#DCCAA8",
                font=("Segoe UI", 13, "bold"),
            )
            lbl.grid(row=0, column=0, padx=12, pady=12, sticky="w")

        self._layout_catalog_cards()

    def _actualizar_estilo_categorias(self) -> None:
        for nombre, boton in self._categoria_botones.items():
            boton.configure(fg_color="#8C1A11" if nombre == self._categoria_actual else "#3A2B2A")

    def _cargar_productos_catalogo(self) -> None:
        self._productos_por_categoria = self.controlador_mesero.cargar_catalogo()

    def _enlazar_click_producto(self, card: ctk.CTkFrame, producto: dict[str, float | str]) -> None:
        def _on_click(_event: tk.Event | None = None) -> None:
            # Agregamos feedback visual al hacer click
            card.configure(fg_color="#3A2A2A")
            self.after(100, lambda: card.configure(fg_color="#1E1E1E"))
            self.agregar_producto_a_ticket(producto)

        card.configure(cursor="hand2")
        
        # Funcion recursiva para atar todos los sub-widgets
        def bind_recursive(widget):
            widget.bind("<Button-1>", _on_click)
            for child in widget.winfo_children():
                bind_recursive(child)
                
        bind_recursive(card)

    def _update_catalog_scrollregion(self, _event: tk.Event | None = None) -> None:
        if self._catalog_canvas is not None:
            self._catalog_canvas.configure(scrollregion=self._catalog_canvas.bbox("all"))

    def _on_catalog_canvas_configure(self, event: tk.Event) -> None:
        if self._catalog_canvas is not None and self._catalog_window_id is not None:
            # Forza el ancho del frame interno al viewport para evitar desborde horizontal.
            self._catalog_canvas.itemconfigure(self._catalog_window_id, width=event.width)
        self._schedule_catalog_layout()

    def _product_card(self, parent: tk.Misc, nombre: str, precio: str, descripcion: str, image_path: str = None) -> ctk.CTkFrame:
        card = ctk.CTkFrame(parent, fg_color="#1E1E1E", corner_radius=15)
        # Evita que el contenedor encoja o cambie su tamaño por el contenido
        card.pack_propagate(False)
        card.grid_propagate(False)

        # Frame interno invisible que aplica el padding de 15px
        padding = 15
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=padding, pady=padding)

        # AREA DE IMAGEN (Top)
        img_height = 130
        if image_path:
            try:
                from PIL import Image
                pil_img = Image.open(image_path)
                ctk_image = ctk.CTkImage(
                    light_image=pil_img, 
                    dark_image=pil_img, 
                    size=(200, img_height) # El ancho será responsivo
                )
                image_label = ctk.CTkLabel(content_frame, text="", image=ctk_image)
            except Exception:
                image_label = ctk.CTkLabel(
                    content_frame, text="Imagen no encontrada", 
                    fg_color="#333333", height=img_height, corner_radius=8
                )
        else:
            image_label = ctk.CTkLabel(
                content_frame, text="Sin Foto Disponible", 
                fg_color="#333333", height=img_height, corner_radius=8
            )
        
        image_label.pack(fill="x", pady=(0, 15))

        # FILA DE TITULO Y PRECIO (Middle)
        middle_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        middle_frame.pack(fill="x", pady=(0, 5))

        middle_frame.grid_columnconfigure(0, weight=1)
        middle_frame.grid_columnconfigure(1, weight=0)

        title_label = ctk.CTkLabel(
            middle_frame, 
            text=nombre, 
            text_color="#FFFFFF", 
            font=("Segoe UI", 16, "bold"),
            anchor="w"
        )
        title_label.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        price_label = ctk.CTkLabel(
            middle_frame, 
            text=precio, 
            text_color="#FFB347", 
            font=("Segoe UI", 16, "bold"),
            anchor="e"
        )
        price_label.grid(row=0, column=1, sticky="e")

        # DESCRIPCION (Bottom)
        descripcion_label = ctk.CTkLabel(
            content_frame,
            text=descripcion,
            justify="left",
            wraplength=190, # Será reconfigurado dinámicamente en _layout_catalog_cards
            text_color="#AAAAAA",
            font=("Segoe UI", 12),
            anchor="nw",
        )
        descripcion_label.pack(fill="both", expand=True)
        
        card.descripcion_label = descripcion_label
        card.title_label = title_label
        card.price_label = price_label
        card.image_label = image_label
        return card

    def _build_order_panel(self) -> ctk.CTkFrame:
        self._pedido_actual_model = ModeloPedidoActual()
        self._pedido_actual_view = VistaPedidoActual(
            self,
            ticket_numero=self._ticket_numero,
            mesa_texto=self._normalize_mesa_text(self.mesa_actual),
        )
        self._pedido_actual_controller = ControladorPedidoActual(
            self._pedido_actual_model,
            self._pedido_actual_view,
            on_send_to_kitchen=self._enviar_pedido_a_cocina,
            on_request_precuenta=self._on_precuenta_solicitada,
            on_close_table_paid=self._on_cerrar_mesa_y_pagar,
            on_exit=self._logout_to_login,
        )
        self._pedido_actual_view.tipo_pedido_var.trace_add("write", self._on_tipo_pedido_changed)
        self._pedido_items_container = self._pedido_actual_view._items_container
        self._pedido_vacio_label = self._pedido_actual_view._empty_label
        self._ticket_label = self._pedido_actual_view._ticket_label
        return self._pedido_actual_view.frame

    def _reproducir_campanita(self) -> None:
        try:
            import winsound
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)
        except Exception:
            pass

    def _actualizar_label_ticket(self) -> None:
        if self._ticket_label is not None:
            self._ticket_label.configure(text=f"TICKET #{self._ticket_numero:05d}")
        if self._pedido_actual_controller is not None:
            self._pedido_actual_controller.establecer_ticket(self._ticket_numero)

    def agregar_producto_a_ticket(self, producto: dict[str, float | str]) -> None:
        if self._pedido_actual_controller is None:
            return
        era_primer_item = self._pedido_actual_model is not None and not self._pedido_actual_model.tiene_items()
        nombre = str(producto.get("nombre", "Producto")).strip()
        precio = float(producto.get("precio", 0.0) or 0.0)
        categoria_db = str(producto.get("categoria_db", "Comida"))
        id_item = str(producto.get("id_producto") or f"{categoria_db}:{nombre.lower()}")
        tipo_pedido = self._pedido_actual_view.tipo_pedido_var.get() if self._pedido_actual_view else "Mesa"
        if tipo_pedido == "Mesa" and self._mesa_seleccionada_id is None:
            self._mostrar_notificacion("Mesa no seleccionada. Por favor, seleccione una mesa libre primero.", "#6F2C2C")
            return
            
        self._pedido_actual_controller.agregar_item(
            id_item=id_item,
            nombre=nombre,
            precio=precio,
            cantidad=1,
            categoria_db=categoria_db,
        )
        if era_primer_item and self._mesa_seleccionada_id is not None and self._mesas_controller is not None:
            if tipo_pedido == "Mesa":
                self._mesas_controller.registrar_primer_item(self._mesa_seleccionada_id)
            else:
                self._mesas_controller.liberar_mesa(self._mesa_seleccionada_id)
        self._actualizar_label_ticket()

    def _on_precuenta_solicitada(self) -> None:
        self._abrir_ordenes_pendientes()

    def _on_cerrar_mesa_y_pagar(self) -> None:
        if self._mesa_seleccionada_id is None or self._mesas_controller is None:
            return
        self._mesas_controller.liberar_mesa(self._mesa_seleccionada_id)

    def _enviar_pedido_a_cocina(self, items: list[dict[str, object]] | None = None) -> bool:
        items_actuales = items or (self._pedido_actual_model.obtener_items() if self._pedido_actual_model is not None else [])
        if not items_actuales:
            self._mostrar_notificacion("No hay productos para enviar", "#6F2C2C")
            return False

        ticket = self._ticket_numero
        
        tipo_pedido_ui = self._pedido_actual_view.tipo_pedido_var.get() if self._pedido_actual_view else "Mesa"
        mesa_str = "Para llevar" if tipo_pedido_ui == "Para llevar" else self._normalize_mesa_text(self.mesa_actual)
        pagado_bool = False
        
        orden = {
            "ticket": ticket,
            "mesa": mesa_str,
            "estado": "En cocina",
            "items": [dict(item) for item in items_actuales],
            "id_pedido": 0,
            "pagado": pagado_bool,
            "metodo_pago": "",
        }
        if self._pedido_actual_controller:
            id_edicion = self._pedido_actual_controller.obtener_id_pedido_en_edicion()
            if id_edicion:
                orden["id_pedido_edicion"] = id_edicion
        if "id_pedido_edicion" in orden:
            self._ordenes_pendientes = [o for o in self._ordenes_pendientes if int(o.get("id_pedido") or 0) != orden["id_pedido_edicion"]]
        self._ordenes_pendientes.append(orden)
        id_pedido = self._guardar_orden_en_bd(orden)
        if id_pedido is None:
            detalle = f": {self._ultimo_error_bd}" if self._ultimo_error_bd else ""
            self._mostrar_notificacion(f"No se pudo enviar a cocina (BD){detalle}", "#6F2C2C")
            self._ordenes_pendientes.pop()
            return False
        orden["id_pedido"] = int(id_pedido)
        self._tickets_por_pedido[int(id_pedido)] = int(ticket)

        event_bus.emit(
            "pedido.creado",
            {
                "id_pedido": id_pedido,
                "ticket": ticket,
                "mesa": orden["mesa"],
            },
        )
        self._mostrar_notificacion(f"Ticket #{ticket:05d} enviado a cocina", "#2F5C36")
        self._reproducir_campanita()

        if tipo_pedido_ui == "Mesa" and self._mesa_seleccionada_id is not None and self._mesas_controller is not None:
            self._mesas_controller._cambiar_estado_mesa(self._mesa_seleccionada_id, "Atencion")

        self.after(5000, lambda t=ticket: self._marcar_orden_en_espera(t))
        self._ticket_numero += 1
        self._actualizar_label_ticket()
        self._refrescar_ventana_pendientes()
        self._mesa_seleccionada_id = None
        self.mesa_actual = "Seleccione Mesa"
        if self._pedido_actual_view:
            self._pedido_actual_view._mesa_label.configure(text="Seleccione Mesa")
        if self._mesa_badge_label is not None:
            self._mesa_badge_label.configure(text="Seleccione Mesa")

        if self._pedido_actual_controller is not None:
            self._pedido_actual_controller.limpiar()
            
        return True

    def _guardar_orden_en_bd(self, orden: dict[str, object]) -> int | None:
        return self.controlador_mesero.guardar_orden(orden, self.usuario)

    def _on_pedido_listo_event(self, evento: dict[str, object]) -> None:
        pedido_id = int(evento.get("id_pedido") or 0)
        if pedido_id <= 0:
            return

        raw_item = str(evento.get("estado_item") or "")
        raw_ped = str(evento.get("estado_pedido") or "")
        if "prepara" in raw_item.lower():
            estado_item = "En preparación"
        else:
            estado_item = self._normalizar_estado_pendiente(raw_item or raw_ped)

        if self._pedidos_estado_notificado.get(pedido_id) == estado_item:
            return

        self._pedidos_estado_notificado[pedido_id] = estado_item
        orden = self._buscar_orden_por_id_pedido(pedido_id)
        if orden is not None:
            orden["estado"] = estado_item
            
            if estado_item in {"En preparación", "Listo"}:
                mesa_texto = str(orden.get("mesa", ""))
                if "MESA" in mesa_texto.upper() and self._mesas_controller is not None:
                    numero = self._extraer_numero_mesa(mesa_texto)
                    if numero is not None:
                        for m_id, m_data in self._mesas_por_id.items():
                            try:
                                m_num = int(m_data.get("numero_mesa") or 0)
                            except ValueError:
                                m_num = 0
                            if m_num == numero:
                                nuevo_estado = "Atencion" if estado_item == "En preparación" else "Ocupada"
                                self._mesas_controller._cambiar_estado_mesa(m_id, nuevo_estado)
                                break
                                
            if estado_item == "Listo":
                self._mover_orden_a_auditoria(orden)
                self._refrescar_ventana_pendientes()
            else:
                self._refrescar_ventana_pendientes(int(orden.get("ticket") or 0))

        if estado_item == "En preparación":
            self._mostrar_notificacion(f"El pedido #{pedido_id:05d} ya entró En preparación", "#8A6317")
            self._reproducir_campanita()
        elif estado_item == "Listo":
            self._mostrar_notificacion(f"El pedido #{pedido_id:05d} está LISTO para entregar", "#2F5C36")
            self._reproducir_campanita()

    def _mover_orden_a_auditoria(self, orden: dict[str, object]) -> None:
        # Se conserva en la lista de pendientes como historial (a petición del usuario)
        # if orden in self._ordenes_pendientes:
        #     self._ordenes_pendientes.remove(orden)

        # Se conserva copia para la vista de auditoría sin mostrarla en pendientes.
        snapshot = dict(orden)
        snapshot["estado"] = "Listo"
        snapshot["items"] = [dict(item) for item in list(orden.get("items", []))]
        self._ordenes_auditoria.append(snapshot)

    def _inicializar_plano_mesas(self) -> None:
        if self._mesas_view is None:
            return

        self._mesas_model = MesasModel()
        self._mesas_controller = MesasController(self._mesas_model, self._mesas_view)
        self._mesas_view.configurar_accion_click(self._on_click_mesa_plano)

        mesas_db = self._mesas_model.obtener_mesas()
        mesas_por_numero: dict[int, dict[str, object]] = {}
        for mesa in mesas_db:
            try:
                numero = int(mesa.get("numero_mesa") or 0)
            except (TypeError, ValueError):
                continue
            if 1 <= numero <= 10:
                mesas_por_numero[numero] = mesa

        mesas_1_a_10 = [mesas_por_numero[num] for num in range(1, 11) if num in mesas_por_numero]
        if mesas_1_a_10:
            self._mesas_view.dibujar_mesas(mesas_1_a_10)

        self._mesas_por_id.clear()
        for mesa in mesas_1_a_10:
            id_mesa = int(mesa.get("id_mesa") or 0)
            if id_mesa > 0:
                self._mesas_por_id[id_mesa] = mesa

        # No auto-seleccionar mesa 1 para forzar al usuario a elegir una mesa libre
        # mesa_inicial = mesas_por_numero.get(1)
        # if mesa_inicial is not None:
        #     self._on_mesa_seleccionada_event(
        #         {
        #             "id_mesa": mesa_inicial.get("id_mesa"),
        #             "numero_mesa": mesa_inicial.get("numero_mesa"),
        #         }
        #     )


    def _on_pedido_actual_items_cambiados(self, evento: dict[str, object]) -> None:
        tiene_items = bool(evento.get("tiene_items", False))
        if not tiene_items and self._mesa_seleccionada_id is not None and self._mesas_controller is not None:
            if self._pedido_actual_controller and self._pedido_actual_controller.obtener_id_pedido_en_edicion() is None:
                self._mesas_controller.liberar_mesa(self._mesa_seleccionada_id)
        elif tiene_items and self._mesa_seleccionada_id is not None and self._mesas_controller is not None:
            if self._pedido_actual_view and self._pedido_actual_view.tipo_pedido_var.get() == "Mesa":
                self._mesas_controller.registrar_primer_item(self._mesa_seleccionada_id)

    def _on_click_mesa_plano(self, id_mesa: int) -> None:
        id_mesa_int = int(id_mesa)
        mesa_anterior = self._mesa_seleccionada_id
        
        if self._mesas_view is not None:
            estado_nueva = self._mesas_view._estado_mesas.get(id_mesa_int, "Libre")
            if str(estado_nueva).strip().lower() != "libre" and id_mesa_int != mesa_anterior:
                self._mostrar_notificacion("Mesa ocupada. Cierre el pedido antes de tomar otro.", "#8A6317")
                return

        if mesa_anterior is not None and mesa_anterior != id_mesa_int:
            if self._mesas_controller is not None:
                estado_anterior = self._mesas_view._estado_mesas.get(mesa_anterior, "Libre") if self._mesas_view else "Libre"
                if str(estado_anterior).strip().lower() in ["atencion", "atención"]:
                    mesa_ant_data = self._mesas_por_id.get(mesa_anterior, {})
                    num_ant = mesa_ant_data.get("numero_mesa", mesa_anterior)
                    def _coincide_mesa(m_val: object, m_num: int) -> bool:
                        if isinstance(m_val, int): return m_val == m_num
                        texto = str(m_val).upper()
                        return f"MESA {m_num}" in texto or texto == str(m_num)
                        
                    tiene_orden = any(_coincide_mesa(o.get("mesa"), num_ant) and str(o.get("estado", "")).strip().lower() not in ["servido", "cancelado"] for o in self._ordenes_pendientes)
                    if not tiene_orden:
                        self._mesas_controller.liberar_mesa(mesa_anterior)

        self._mesa_seleccionada_id = id_mesa_int
        if self._mesas_controller is not None:
            self._mesas_controller.seleccionar_mesa(id_mesa_int)

    def _on_mesa_seleccionada_event(self, evento: dict[str, object]) -> None:
        id_mesa = int(evento.get("id_mesa") or 0)
        if id_mesa <= 0:
            return
        self._mesa_seleccionada_id = id_mesa
        numero = evento.get("numero_mesa")
        if numero is None:
            mesa_cache = self._mesas_por_id.get(id_mesa, {})
            numero = mesa_cache.get("numero_mesa", id_mesa)

        self.mesa_actual = f"Mesa {numero}"
        mesa_ui = self._normalize_mesa_text(self.mesa_actual)
        
        if self._pedido_actual_view is not None:
            self._pedido_actual_view.tipo_pedido_var.set("Mesa")
            pass
            
        if self._pedido_actual_controller is not None:
            self._pedido_actual_controller.establecer_mesa(mesa_ui)
            
        if self._mesa_badge_label is not None:
            self._mesa_badge_label.configure(text=mesa_ui)
            
        if self._mesas_view is not None:
            self._mesas_view.marcar_mesa_seleccionada(id_mesa)

        if self._pedido_actual_model and self._pedido_actual_model.obtener_items():
            if self._mesas_controller is not None:
                self._mesas_controller.registrar_primer_item(id_mesa)

    def _on_tipo_pedido_changed(self, *args) -> None:
        if not self._pedido_actual_view or not self._mesas_controller or not self._mesa_seleccionada_id:
            return
        tipo = self._pedido_actual_view.tipo_pedido_var.get()
        if tipo == "Para llevar":
            self._pedido_actual_view._mesa_label.configure(text="Para llevar")
            if self._mesa_badge_label is not None:
                self._mesa_badge_label.configure(text="Para llevar")
            self._mesas_controller.liberar_mesa(self._mesa_seleccionada_id)
        else:
            self._pedido_actual_view._mesa_label.configure(text=self._normalize_mesa_text(self.mesa_actual))
            if self._mesa_badge_label is not None:
                self._mesa_badge_label.configure(text=self._normalize_mesa_text(self.mesa_actual))
            if self._pedido_actual_model and self._pedido_actual_model.obtener_items():
                self._mesas_controller.registrar_primer_item(self._mesa_seleccionada_id)

    def _limpiar_panel_pedido_actual(self) -> None:
        if self._pedido_actual_controller is not None:
            self._pedido_actual_controller.limpiar()

    def _marcar_orden_en_espera(self, ticket: int) -> None:
        orden = self._buscar_orden(ticket)
        if orden is None or str(orden.get("estado")) != "En cocina":
            return
        orden["estado"] = "En espera"
        self._refrescar_ventana_pendientes()

    def _buscar_orden(self, ticket: int) -> dict[str, object] | None:
        for orden in self._ordenes_pendientes:
            if int(orden.get("ticket", 0)) == ticket:
                return orden
        return None

    def _buscar_orden_por_id_pedido(self, id_pedido: int) -> dict[str, object] | None:
        for orden in self._ordenes_pendientes:
            if int(orden.get("id_pedido", 0)) == int(id_pedido):
                return orden
        return None

    def _abrir_ordenes_pendientes(self) -> None:
        self._cargar_ordenes_pendientes_desde_bd()

        if self._pendientes_window is not None and self._pendientes_window.winfo_exists():
            self._pendientes_window.focus()
            self._refrescar_ventana_pendientes()
            return

        win = ctk.CTkToplevel(self)
        win.title("Ordenes Pendientes")
        win.geometry("860x520")
        win.minsize(760, 460)
        win.configure(fg_color="#141517")
        win.grid_columnconfigure(0, weight=0)
        win.grid_columnconfigure(1, weight=1)
        win.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            win,
            text="Ordenes pendientes",
            text_color="#F4EBD0",
            font=("Segoe UI", 24, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(12, 8))

        lista = ctk.CTkScrollableFrame(win, fg_color="#1E1415", corner_radius=10, width=280)
        lista.grid(row=1, column=0, sticky="nsw", padx=(16, 8), pady=(0, 14))
        #lista.grid_propagate(False)  # Not needed for scrollable frame

        detalle = ctk.CTkFrame(win, fg_color="#1B1C1F", corner_radius=10)
        detalle.grid(row=1, column=1, sticky="nsew", padx=(8, 16), pady=(0, 14))

        self._pendientes_window = win
        self._pendientes_list_container = lista
        self._pendientes_detail_container = detalle
        self._refrescar_ventana_pendientes()

    def _cargar_ordenes_pendientes_desde_bd(self) -> None:
        if self.controlador_mesero and self.controlador_mesero.modelo:
            ordenes = self.controlador_mesero.modelo.obtener_ordenes_pendientes()
            grouped = {}
            for row in ordenes:
                t = row.get("id_pedido")
                if not t: continue
                if t not in grouped:
                    mesa_db = str(row.get("mesa", ""))
                    if mesa_db.isdigit(): mesa_db = f"Mesa {mesa_db}"
                    elif not mesa_db: mesa_db = "Mesa X"
                    
                    grouped[t] = {
                        "ticket": row.get("ticket_numero") or t,
                        "mesa": mesa_db,
                        "estado": row.get("estado_pedido", ""),
                        "pagado": bool(row.get("pagado")),
                        "metodo_pago": row.get("metodo_pago") or "",
                        "id_pedido": row.get("id_pedido"),
                        "items": []
                    }
                grouped[t]["items"].append({
                    "id_detalle": row.get("id_detalle"),
                    "id_producto": row.get("id_producto"),
                    "nombre": row.get("nombre"),
                    "precio": row.get("precio"),
                    "cantidad": row.get("cantidad"),
                    "notas": row.get("descripcion_preparacion", ""),
                    "estado_item": row.get("estado_item", "")
                })

            for orden in grouped.values():
                items_estados = [str(it.get("estado_item") or "").lower() for it in orden.get("items", [])]
                estado_base = str(orden.get("estado") or "")
                if estado_base == "Cancelado" or (items_estados and all("cancel" in e for e in items_estados)):
                    orden["estado"] = "Cancelado"
                elif estado_base == "Servido":
                    orden["estado"] = "Servido"
                elif estado_base == "Listo" or any("listo" in e for e in items_estados):
                    orden["estado"] = "Listo"
                elif any("prepara" in e for e in items_estados):
                    orden["estado"] = "En preparación"
                elif estado_base:
                    orden["estado"] = estado_base
                else:
                    orden["estado"] = "En cocina"
            
            self._on_pedidos_actualizados({"ordenes": list(grouped.values())})

    def _on_pedidos_actualizados(self, payload: dict) -> None:
        nuevas_ordenes = payload.get("ordenes", [])
        
        # Evitar parpadeos: solo refrescamos la UI si hubo cambios reales en los pedidos
        import json
        from decimal import Decimal
        
        def custom_encoder(obj):
            if isinstance(obj, Decimal):
                return float(obj)
            raise TypeError(f"Object not serializable: {type(obj)}")
            
        estado_actual = json.dumps(self._ordenes_pendientes, sort_keys=True, default=custom_encoder)
        nuevo_estado = json.dumps(nuevas_ordenes, sort_keys=True, default=custom_encoder)
        
        if estado_actual != nuevo_estado:
            self._ordenes_pendientes = nuevas_ordenes
            if self._pendientes_window is not None and self._pendientes_window.winfo_exists():
                # Mantener el ticket seleccionado si existe
                ticket_actual = getattr(self, "_ticket_seleccionado_actual", None)
                self._refrescar_ventana_pendientes(ticket_seleccionado=ticket_actual)

    def _refrescar_ventana_pendientes(self, ticket_seleccionado: int | None = None) -> None:
        if (
            self._pendientes_window is None
            or not self._pendientes_window.winfo_exists()
            or self._pendientes_list_container is None
            or self._pendientes_detail_container is None
        ):
            return

        scroll_pos = None
        if hasattr(self._pendientes_list_container, "_parent_canvas"):
            scroll_pos = self._pendientes_list_container._parent_canvas.yview()
            
        for widget in self._pendientes_list_container.winfo_children():
            widget.destroy()
        for widget in self._pendientes_detail_container.winfo_children():
            widget.destroy()

        if not self._ordenes_pendientes:
            ctk.CTkLabel(
                self._pendientes_list_container,
                text="No hay ordenes pendientes",
                text_color="#D6C9A8",
                font=("Segoe UI", 12, "bold"),
            ).pack(anchor="w", padx=12, pady=12)
            ctk.CTkLabel(
                self._pendientes_detail_container,
                text="Selecciona un ticket para ver detalle",
                text_color="#D6C9A8",
                font=("Segoe UI", 12, "bold"),
            ).pack(anchor="w", padx=14, pady=14)
            return

        if ticket_seleccionado is None:
            ticket_seleccionado = int(self._ordenes_pendientes[0]["ticket"])

        self._ticket_seleccionado_actual = ticket_seleccionado

        for orden in self._ordenes_pendientes:
            ticket = int(orden["ticket"])
            estado = str(orden.get("estado", ""))
            es_listo = "listo" in estado.lower()
            es_servido = "servido" in estado.lower()
            es_prep = "prepara" in estado.lower()
            es_cancelado = "cancel" in estado.lower()
            es_seleccionado = (ticket == ticket_seleccionado)
            pagado = bool(orden.get("pagado", False))
            
            if es_cancelado:
                fg_color = "#333333" if es_seleccionado else "#1A1A1A"
                hover_color = "#444444" if es_seleccionado else "#222222"
            elif es_servido:
                fg_color = "#2E2A2B" if es_seleccionado else "#1B1718"
                hover_color = "#3C3839" if es_seleccionado else "#2E2A2B"
            elif es_listo:
                fg_color = "#2F5C36" if es_seleccionado else "#1F4225"
                hover_color = "#387040" if es_seleccionado else "#2F5C36"
            elif es_prep:
                fg_color = "#997300" if es_seleccionado else "#664D00"
                hover_color = "#B38600" if es_seleccionado else "#997300"
            else:
                fg_color = "#8C1A11" if es_seleccionado else "#2A1B1B"
                hover_color = "#A62216"
                
            texto_pago = " (PAGO)" if pagado else ""
            texto = f"TICKET #{ticket:05d}  |  {orden['mesa']}  |  {estado}{texto_pago}"
            ctk.CTkButton(
                self._pendientes_list_container,
                text=texto,
                anchor="w",
                fg_color=fg_color,
                hover_color=hover_color,
                text_color="#F4EBD0",
                font=("Segoe UI", 11, "bold"),
                command=lambda t=ticket: self._refrescar_ventana_pendientes(t),
            ).pack(fill="x", padx=10, pady=(10, 0))

        orden_activa = self._buscar_orden(ticket_seleccionado)
        if orden_activa is None:
            return

        ctk.CTkLabel(
            self._pendientes_detail_container,
            text=f"TICKET #{ticket_seleccionado:05d}",
            text_color="#F4EBD0",
            font=("Segoe UI", 22, "bold"),
        ).pack(anchor="w", padx=14, pady=(14, 4))
        ctk.CTkLabel(
            self._pendientes_detail_container,
            text=f"Mesa: {orden_activa['mesa']}",
            text_color="#DCCAA8",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", padx=14)
        ctk.CTkLabel(
            self._pendientes_detail_container,
            text=f"Estado: {orden_activa['estado']}",
            text_color="#E8A27E",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", padx=14, pady=(4, 10))

        es_editable = self._pedido_pendiente_editable(orden_activa)
        ayuda_estado = "Editable antes de que cocina lo ponga En preparación." if es_editable else "Este pedido ya esta En preparación o listo y no se puede editar."
        ctk.CTkLabel(
            self._pendientes_detail_container,
            text=ayuda_estado,
            text_color="#D6C9A8",
            font=("Segoe UI", 10, "italic"),
        ).pack(anchor="w", padx=14, pady=(0, 10))

        ctk.CTkLabel(
            self._pendientes_detail_container,
            text="Productos",
            text_color="#F4EBD0",
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w", padx=14)

        for index, item in enumerate(list(orden_activa.get("items", []))):
            item_frame = ctk.CTkFrame(self._pendientes_detail_container, fg_color="#241516", corner_radius=8)
            item_frame.pack(fill="x", padx=14, pady=(8, 0))
            item_frame.grid_columnconfigure(0, weight=1)

            cantidad = max(1, int(item.get("cantidad") or 1))
            precio = float(item.get("precio") or 0.0)
            subtotal = precio * cantidad
            ctk.CTkLabel(
                item_frame,
                text=f"{cantidad}x {item['nombre']}",
                text_color="#F4EBD0",
                font=("Segoe UI", 12, "bold"),
            ).grid(row=0, column=0, sticky="w", padx=10, pady=(8, 2))
            ctk.CTkLabel(
                item_frame,
                text=f"${subtotal:.2f}",
                text_color="#F0A58E",
                font=("Segoe UI", 12, "bold"),
            ).grid(row=0, column=1, sticky="e", padx=10, pady=(8, 2))

            notas = str(item.get("notas") or "").strip()
            if notas:
                ctk.CTkLabel(
                    item_frame,
                    text=notas,
                    text_color="#F19B95",
                    font=("Segoe UI", 10, "italic"),
                    wraplength=360,
                    justify="left",
                ).grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 4))
                
        estado_norm = self._normalizar_estado_pendiente(str(orden_activa.get("estado") or ""))
        es_listo = estado_norm in {"Listo", "Servido"}
        es_servido = estado_norm == "Servido"
        es_cancelado = estado_norm == "Cancelado"
        es_cancelable = estado_norm in {"Enviado a cocina", "En preparación", "En espera"}
        
        # Total
        total_suma = sum(float(it.get("precio", 0.0)) * max(1, int(it.get("cantidad", 1))) for it in orden_activa.get("items", []))
        total_frame = ctk.CTkFrame(self._pendientes_detail_container, fg_color="#180C0D", corner_radius=8)
        total_frame.pack(fill="x", padx=14, pady=(14, 0))
        ctk.CTkLabel(total_frame, text="Total:", text_color="#F4EBD0", font=("Segoe UI", 16, "bold")).pack(side="left", padx=10, pady=10)
        ctk.CTkLabel(total_frame, text=f"${total_suma:,.0f}".replace(",", "."), text_color="#4FA64F", font=("Segoe UI", 16, "bold")).pack(side="right", padx=10, pady=10)
        
        if es_servido:
            metodo = str(orden_activa.get("metodo_pago") or "Efectivo")
            metodo_frame = ctk.CTkFrame(self._pendientes_detail_container, fg_color="#1B1C1F", corner_radius=8)
            metodo_frame.pack(fill="x", padx=14, pady=(5, 0))
            ctk.CTkLabel(metodo_frame, text="Método de pago:", text_color="#DCCAA8", font=("Segoe UI", 12)).pack(side="left", padx=10, pady=5)
            ctk.CTkLabel(metodo_frame, text=metodo, text_color="#F4EBD0", font=("Segoe UI", 12, "bold")).pack(side="right", padx=10, pady=5)
        
        if not es_servido and not es_cancelado:
            acciones = ctk.CTkFrame(self._pendientes_detail_container, fg_color="transparent")
            acciones.pack(anchor="w", padx=14, pady=(14, 0))
    
            ctk.CTkButton(
                acciones,
                text="Editar en panel",
                fg_color="#3A2524" if es_editable else "#1C1414",
                hover_color="#503231" if es_editable else "#1C1414",
                text_color="#F4EBD0" if es_editable else "#555555",
                font=("Segoe UI", 11, "bold"),
                state="normal" if es_editable else "disabled",
                command=lambda t=ticket_seleccionado: self._cargar_pedido_pendiente_en_panel(t),
            ).pack(side="left", padx=(0, 8))

            ctk.CTkButton(
                acciones,
                text="Cancelar pedido",
                fg_color="#8C1A11" if es_cancelable else "#2A1B1B",
                hover_color="#A1241A" if es_cancelable else "#2A1B1B",
                text_color="#F4EBD0" if es_cancelable else "#555555",
                font=("Segoe UI", 11, "bold"),
                state="normal" if es_cancelable else "disabled",
                command=lambda t=ticket_seleccionado: self._cancelar_pedido_pendiente(t),
            ).pack(side="left", padx=(0, 8))

            es_para_llevar = "para llevar" in str(orden_activa.get("mesa", "")).lower()
            if not es_para_llevar:
                ctk.CTkButton(
                    acciones,
                    text="🥡 Para llevar",
                    fg_color="#B45309",
                    hover_color="#D97706",
                    text_color="#FFFFFF",
                    font=("Segoe UI", 11, "bold"),
                    command=lambda t=ticket_seleccionado: self._cambiar_orden_a_para_llevar(t),
                ).pack(side="left", padx=(0, 8))
            else:
                ctk.CTkButton(
                    acciones,
                    text="🥡 Para llevar",
                    fg_color="#2A241A",
                    text_color="#A89070",
                    font=("Segoe UI", 11, "bold"),
                    state="disabled",
                ).pack(side="left", padx=(0, 8))
            
            ctk.CTkButton(
                acciones,
                text="Cerrar y Pagar",
                fg_color="#4FA64F",
                hover_color="#66BB66",
                text_color="#0F2010",
                font=("Segoe UI", 11, "bold"),
                state="normal",
                command=lambda t=ticket_seleccionado: self._abrir_modal_pago(t),
            ).pack(side="left")

        if scroll_pos is not None and hasattr(self._pendientes_list_container, "_parent_canvas"):
            self._pendientes_list_container.update_idletasks()
            self._pendientes_list_container._parent_canvas.yview_moveto(scroll_pos[0])

    def _actualizar_estado_pedido_desde_cocina(self, ticket: int, estado: str) -> None:
        orden = self._buscar_orden(ticket)
        if orden is None:
            import logging
            logging.error(f"Error: _buscar_orden({ticket}) retorno None. _ordenes_pendientes={self._ordenes_pendientes}")
            return

        orden["estado"] = estado
        if estado == "Listo":
            self._mostrar_notificacion(f"Pedido listo: TICKET #{ticket:05d}", "#2F5C36")
            # Cambiar mesa a Ocupada (Rojo)
            mesa_texto = str(orden.get("mesa", ""))
            if "MESA" in mesa_texto.upper() and self._mesas_controller is not None:
                numero = self._extraer_numero_mesa(mesa_texto)
                if numero is not None:
                    for m_id, m_data in self._mesas_por_id.items():
                        if m_data.get("numero_mesa") == numero:
                            self._mesas_controller._cambiar_estado_mesa(m_id, "Ocupada")
                            break
        self._refrescar_ventana_pendientes(ticket)

    def _pedido_pendiente_editable(self, orden: dict[str, object]) -> bool:
        estado = self._normalizar_estado_pendiente(str(orden.get("estado") or ""))
        return estado not in {"En preparación", "Listo", "Servido", "Cancelado"}

    @staticmethod
    def _normalizar_estado_pendiente(estado: str) -> str:
        texto = (estado or "").strip().lower()
        if "prepara" in texto:
            return "En preparación"
        if "listo" in texto:
            return "Listo"
        if "espera" in texto:
            return "En espera"
        if "servido" in texto:
            return "Servido"
        if "cancel" in texto:
            return "Cancelado"
        if "cocina" in texto:
            return "En cocina"
        return "En cocina"

    def _incrementar_item_pendiente(self, ticket: int, item_index: int) -> None:
        orden = self._buscar_orden(ticket)
        if orden is None or not self._pedido_pendiente_editable(orden):
            return
        items = list(orden.get("items", []))
        if item_index < 0 or item_index >= len(items):
            return
        item = items[item_index]
        item["cantidad"] = max(1, int(item.get("cantidad") or 1)) + 1
        if self._persistir_item_pendiente(orden, item):
            self._refrescar_ventana_pendientes(ticket)

    def _reducir_item_pendiente(self, ticket: int, item_index: int) -> None:
        orden = self._buscar_orden(ticket)
        if orden is None or not self._pedido_pendiente_editable(orden):
            return
        items = list(orden.get("items", []))
        if item_index < 0 or item_index >= len(items):
            return
        item = items[item_index]
        cantidad_actual = max(1, int(item.get("cantidad") or 1))
        if cantidad_actual <= 1:
            self._eliminar_item_pendiente(ticket, item_index)
            return
        item["cantidad"] = cantidad_actual - 1
        if self._persistir_item_pendiente(orden, item):
            self._refrescar_ventana_pendientes(ticket)

    def _editar_nota_item_pendiente(self, ticket: int, item_index: int) -> None:
        orden = self._buscar_orden(ticket)
        if orden is None or not self._pedido_pendiente_editable(orden):
            return
        items = list(orden.get("items", []))
        if item_index < 0 or item_index >= len(items) or self._pedido_actual_view is None:
            return
        item = items[item_index]
        nueva_nota = self._pedido_actual_view.pedir_nota(f"Nota para {item['nombre']}")
        if nueva_nota is None:
            return
        item["notas"] = nueva_nota
        if self._persistir_item_pendiente(orden, item):
            self._refrescar_ventana_pendientes(ticket)

    def _eliminar_item_pendiente(self, ticket: int, item_index: int) -> None:
        orden = self._buscar_orden(ticket)
        if orden is None or not self._pedido_pendiente_editable(orden):
            return
        items = list(orden.get("items", []))
        if item_index < 0 or item_index >= len(items):
            return
        item = items[item_index]
        if not self.controlador_mesero.eliminar_item_pendiente(int(item.get("id_detalle") or 0)):
            self._mostrar_notificacion("No se pudo eliminar el item del pedido", "#6F2C2C")
            return
        items.pop(item_index)
        orden["items"] = items
        if items:
            self._refrescar_ventana_pendientes(ticket)
            return
        if orden in self._ordenes_pendientes:
            self._ordenes_pendientes.remove(orden)
        if getattr(self, "_ticket_seleccionado_actual", None) == int(orden.get("ticket", 0)):
            self._ticket_seleccionado_actual = None
        self._refrescar_ventana_pendientes(None)
        self._mostrar_notificacion(f"Pedido #{int(orden.get('id_pedido') or 0):05d} cancelado", "#8C1A11")

    def _abrir_modal_pago(self, ticket: int) -> None:
        orden = self._buscar_orden(ticket)
        if orden is None:
            import logging
            logging.error(f"Error: _buscar_orden({ticket}) retorno None. _ordenes_pendientes={self._ordenes_pendientes}")
            return
            
        if hasattr(self, "_pago_modal") and self._pago_modal is not None and self._pago_modal.winfo_exists():
            self._pago_modal.focus()
            return
            
        self._pago_modal = ctk.CTkToplevel(self)
        self._pago_modal.title(f"Pagar Pedido - Ticket #{ticket:05d}")
        self._pago_modal.geometry("400x550")
        self._pago_modal.grab_set()
        self._pago_modal.configure(fg_color="#180C0D")
        
        # Centrar en pantalla
        self._pago_modal.update_idletasks()
        width = self._pago_modal.winfo_width()
        height = self._pago_modal.winfo_height()
        x = (self._pago_modal.winfo_screenwidth() // 2) - (width // 2)
        y = (self._pago_modal.winfo_screenheight() // 2) - (height // 2)
        self._pago_modal.geometry(f"+{x}+{y}")
        
        # Ticket Content
        header = ctk.CTkFrame(self._pago_modal, fg_color="#2A1718", corner_radius=0)
        header.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(header, text=f"TICKET #{ticket:05d}", text_color="#F4EBD0", font=("Segoe UI", 20, "bold")).pack(pady=10)
        ctk.CTkLabel(header, text=f"Mesa: {orden['mesa']}", text_color="#DCCAA8", font=("Segoe UI", 12)).pack(pady=(0, 10))
        
        items_frame = ctk.CTkScrollableFrame(self._pago_modal, fg_color="#1B1C1F")
        items_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        total_suma = 0.0
        for item in orden.get("items", []):
            cantidad = max(1, int(item.get("cantidad") or 1))
            precio = float(item.get("precio") or 0.0)
            subtotal = precio * cantidad
            total_suma += subtotal
            
            row = ctk.CTkFrame(items_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"{cantidad}x {item['nombre']}", text_color="#F4EBD0", font=("Segoe UI", 12)).pack(side="left")
            ctk.CTkLabel(row, text=f"${subtotal:.2f}", text_color="#F0A58E", font=("Segoe UI", 12)).pack(side="right")
            
        total_frame = ctk.CTkFrame(self._pago_modal, fg_color="#180C0D")
        total_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(total_frame, text="TOTAL A PAGAR:", text_color="#F4EBD0", font=("Segoe UI", 18, "bold")).pack(side="left")
        ctk.CTkLabel(total_frame, text=f"${total_suma:,.0f}".replace(",", "."), text_color="#4FA64F", font=("Segoe UI", 20, "bold")).pack(side="right")
        
        ctk.CTkLabel(self._pago_modal, text="Método de Pago:", text_color="#F4EBD0", font=("Segoe UI", 14, "bold")).pack(pady=(10, 5))
        self._metodo_var = ctk.StringVar(value="Efectivo")
        metodo_var = self._metodo_var
        metodos = ctk.CTkSegmentedButton(
            self._pago_modal,
            values=["Efectivo", "Pago Móvil", "Tarjeta"],
            variable=metodo_var,
            font=("Segoe UI", 12, "bold"),
            fg_color="#3A1E18",
            selected_color="#E8A995",
            selected_hover_color="#F8B7A5",
            unselected_color="#2A1718"
        )
        metodos.pack(fill="x", padx=20, pady=5)
        
        # Cerrar Mesa Button
        ctk.CTkButton(
            self._pago_modal,
            text="Confirmar Pago y Cerrar Mesa",
            fg_color="#4FA64F",
            hover_color="#66BB66",
            text_color="#0F2010",
            font=("Segoe UI", 14, "bold"),
            height=40,
            command=lambda t=ticket: self._cerrar_pedido_listo_y_pagado(t, metodo_var.get())
        ).pack(fill="x", padx=20, pady=20)

    def _cerrar_pedido_listo_y_pagado(self, ticket: int, metodo_pago: str = "") -> None:
        import logging
        logging.info(f"Intentando cerrar pedido. Ticket={ticket}, Metodo={metodo_pago}")
        orden = self._buscar_orden(ticket)
        if orden is None:
            import logging
            logging.error(f"Error: _buscar_orden({ticket}) retorno None. _ordenes_pendientes={self._ordenes_pendientes}")
            return
        id_pedido = int(orden.get("id_pedido") or 0)
        if id_pedido <= 0:
            return
            
        connection = self.controlador_mesero.modelo._connect_db()
        if connection is not None:
            try:
                cursor = connection.cursor()
                cursor.execute("UPDATE pedidos SET estado_pedido = 'Servido', pagado = 1, metodo_pago = %s WHERE id_pedido = %s", (metodo_pago, id_pedido))
                cursor.execute("UPDATE detalle_pedido SET estado_item = 'Servido' WHERE id_pedido = %s", (id_pedido,))
                connection.commit()
            except Exception as exc:
                self._ultimo_error_bd = str(exc)
                connection.rollback()
                self._mostrar_notificacion("Error al cerrar pedido", "#6F2C2C")
                return
            finally:
                connection.close()

        orden["estado"] = "Servido"
        orden["pagado"] = True
        orden["metodo_pago"] = metodo_pago
        for item in orden.get("items", []):
            item["estado_item"] = "Servido"
            
        self._mostrar_notificacion(f"Pedido #{id_pedido:05d} cerrado y pagado", "#2F5C36")
        if hasattr(self, "_pago_modal") and self._pago_modal is not None and self._pago_modal.winfo_exists():
            self._pago_modal.destroy()
            self._pago_modal = None
            
        # Mantener la orden localmente para que se vea como "Servido"
        self._refrescar_ventana_pendientes(ticket)
        
        self._liberar_mesa_de_orden(orden)

    def _cancelar_pedido_pendiente(self, ticket: int) -> None:
        orden = self._buscar_orden(ticket)
        if orden is None:
            import logging
            logging.error(f"Error: _buscar_orden({ticket}) retorno None. _ordenes_pendientes={self._ordenes_pendientes}")
            return
        id_pedido = int(orden.get("id_pedido") or 0)
        if id_pedido <= 0:
            return
        if not self.controlador_mesero.cancelar_pedido_pendiente(id_pedido):
            self._mostrar_notificacion("No se pudo cancelar el pedido", "#6F2C2C")
            return
        orden["estado"] = "Cancelado"
        self._refrescar_ventana_pendientes(ticket)
        self._liberar_mesa_de_orden(orden)
        self._mostrar_notificacion(f"Pedido #{id_pedido:05d} cancelado", "#8C1A11")
        
        from src.core.event_bus import event_bus
        event_bus.emit("pedido.cancelado", {"id_pedido": id_pedido, "ticket": ticket})

    def _retirar_orden_pendiente(self, orden: dict[str, object]) -> None:
        if orden in self._ordenes_pendientes:
            self._ordenes_pendientes.remove(orden)
        self._refrescar_ventana_pendientes()
        self._liberar_mesa_de_orden(orden)

    @staticmethod
    def _extraer_numero_mesa(texto: str) -> int | None:
        import re
        match = re.search(r'\d+', texto)
        if match:
            return int(match.group())
        return None

    def _liberar_mesa_de_orden(self, orden: dict[str, object]) -> None:
        mesa_texto = str(orden.get("mesa", ""))
        if "MESA" not in mesa_texto.upper() or self._mesas_controller is None:
            return

        numero = self._extraer_numero_mesa(mesa_texto)
        if numero is None:
            return

        for id_mesa, mesa in self._mesas_por_id.items():
            if int(mesa.get("numero_mesa") or 0) == numero:
                self._mesas_controller.liberar_mesa(id_mesa)
                return

        if hasattr(self._mesas_controller, "_cache_mesas"):
            for id_m, m_info in self._mesas_controller._cache_mesas.items():
                if int(m_info.get("numero_mesa") or 0) == numero:
                    self._mesas_controller.liberar_mesa(id_m)
                    return

    def _cambiar_orden_a_para_llevar(self, ticket: int) -> None:
        orden = self._buscar_orden(ticket)
        if orden is None:
            return
        id_pedido = int(orden.get("id_pedido") or 0)
        if id_pedido <= 0:
            return

        # Liberar la mesa antes de cambiar el texto de la mesa
        self._liberar_mesa_de_orden(orden)

        if not self.controlador_mesero.cambiar_a_para_llevar(id_pedido):
            self._mostrar_notificacion("No se pudo cambiar a para llevar", "#6F2C2C")
            return

        orden["mesa"] = "Para llevar"
        self._refrescar_ventana_pendientes(ticket)
        self._mostrar_notificacion(f"Ticket #{ticket:05d} cambiado a Para llevar", "#2F5C36")

        from src.core.event_bus import event_bus
        event_bus.emit("pedido.actualizado", {"id_pedido": id_pedido, "ticket": ticket, "tipo_pedido": "Para llevar"})

    def _cargar_pedido_pendiente_en_panel(self, ticket: int) -> None:
        orden = self._buscar_orden(ticket)
        if orden is None or not self._pedido_pendiente_editable(orden) or self._pedido_actual_controller is None:
            return
        mesa = str(orden.get("mesa") or self._normalize_mesa_text(self.mesa_actual))
        self.mesa_actual = mesa.replace("MESA", "Mesa")
        self._pedido_actual_controller.establecer_mesa(mesa)
        self._pedido_actual_controller.limpiar()
        id_pedido = int(orden.get("id_pedido") or 0)
        self._pedido_actual_controller.establecer_id_pedido_en_edicion(id_pedido if id_pedido > 0 else None)
        for item in list(orden.get("items", [])):
            self._pedido_actual_controller.agregar_item(
                id_item=str(item.get("id_item") or item.get("id_producto") or item.get("nombre") or ""),
                nombre=str(item.get("nombre") or "Producto"),
                precio=float(item.get("precio") or 0.0),
                cantidad=max(1, int(item.get("cantidad") or 1)),
                notas=str(item.get("notas") or ""),
                categoria_db=str(item.get("categoria_db") or "Comida"),
            )

        if self._pendientes_window and self._pendientes_window.winfo_exists():
            self._pendientes_window.destroy()

    def _persistir_item_pendiente(self, orden: dict[str, object], item: dict[str, object]) -> bool:
        id_detalle = int(item.get("id_detalle") or 0)
        if id_detalle <= 0:
            self._ultimo_error_bd = "El item no tiene detalle asociado en BD"
            return False

        connection = self.controlador_mesero.modelo._connect_db()
        if connection is None:
            return False

        try:
            with connection.cursor() as cursor:
                cantidad = max(1, int(item.get("cantidad") or 1))
                precio = float(item.get("precio") or 0.0)
                subtotal = round(precio * cantidad, 2)
                notas = str(item.get("notas") or "").strip() or None
                cursor.execute(
                    """
                    UPDATE detalle_pedido
                    SET cantidad = %s,
                        descripcion_preparacion = %s,
                        subtotal = %s
                    WHERE id_detalle = %s
                    """,
                    (cantidad, notas, subtotal, id_detalle),
                )
            connection.commit()
            return True
        except Exception as exc:
            self._ultimo_error_bd = str(exc)
            connection.rollback()
            return False
        finally:
            connection.close()

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

        if section == "orders":
            if self._section_frame is not None:
                self._section_frame.grid_remove()
            if self._center_frame is not None:
                self._center_frame.grid()
            if self._order_frame is not None:
                self._order_frame.grid()
            return

        if self._center_frame is not None:
            self._center_frame.grid_remove()
        if self._order_frame is not None:
            self._order_frame.grid_remove()

        if self._section_frame is not None:
            self._section_frame.grid()
            for child in self._section_frame.winfo_children():
                child.destroy()

            title_map = {
                "kitchen": "Vista Kitchen",
                "inventory": "Vista Inventory",
                "menu": "Vista Menu",
                "help": "Centro de Ayuda",
            }
            subtitle_map = {
                "kitchen": "Aqui se mostrara el monitoreo de cocina integrado para el mesero.",
                "inventory": "Aqui se mostraran existencias e indicadores del inventario.",
                "menu": "Aqui se mostrara la administracion visual del menu del dia.",
                "help": "Aqui se mostraran guias rapidas y atajos operativos.",
            }

            placeholder = ctk.CTkFrame(
                self._section_frame,
                fg_color="#1E1F22",
                border_color="#383B40",
                border_width=1,
                corner_radius=12,
            )
            placeholder.pack(fill="both", expand=True, padx=24, pady=24)

            ctk.CTkLabel(
                placeholder,
                text=title_map.get(section, "Modulo"),
                text_color="#F4EBD0",
                font=("Segoe UI", 34, "bold"),
            ).pack(anchor="w", padx=24, pady=(24, 8))
            ctk.CTkLabel(
                placeholder,
                text=subtitle_map.get(section, "Seccion en construccion."),
                text_color="#D7CBAE",
                font=("Segoe UI", 14),
                wraplength=780,
                justify="left",
            ).pack(anchor="w", padx=24)

    def _update_nav_state(self) -> None:
        for section, button in self._nav_buttons.items():
            is_active = section == self._active_section
            button.configure(
                fg_color="#9E1F14" if is_active else "#1A0D0C",
                hover_color="#B52619" if is_active else "#2A1A18",
            )



    def _cleanup_event_listeners(self) -> None:
        sync_id = getattr(self, "_sync_pedidos_after_id", None)
        if sync_id is not None:
            self.after_cancel(sync_id)
            self._sync_pedidos_after_id = None
        event_bus.unsubscribe("pedido.listo", self._evento_pedido_listo)
        event_bus.unsubscribe("mesa.seleccionada", self._evento_mesa_seleccionada)
        event_bus.unsubscribe("pedidos.pendientes_actualizados", self._evento_pedidos_actualizados)
        event_bus.unsubscribe("pedido_actual.items_cambiados", self._evento_items_cambiados)

    def destroy(self) -> None:
        self.controlador_mesero.stop_polling()
        self._cleanup_event_listeners()
        if self._pendientes_window is not None and self._pendientes_window.winfo_exists():
            self._pendientes_window.destroy()
        super().destroy()

    def _preparation_notes_section(self, parent: tk.Misc) -> ctk.CTkFrame:
        section = ctk.CTkFrame(parent, fg_color="#241516", border_color="#4A3131", border_width=1, corner_radius=8)
        section.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(section, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=(8, 4))
        ctk.CTkLabel(header, text="Detalle de preparacion", text_color="#F4EBD0", font=("Segoe UI", 11, "bold")).pack(side="left")
        ctk.CTkLabel(
            header,
            text="Opcional",
            fg_color="#5B352E",
            text_color="#F4EBD0",
            corner_radius=8,
            font=("Segoe UI", 8, "bold"),
            padx=7,
            pady=2,
        ).pack(side="right")

        ctk.CTkLabel(
            section,
            text="Escribe aqui observaciones como: sin queso, sin cebolla, bien cocido, extra salsa.",
            text_color="#D9C8A9",
            justify="left",
            wraplength=260,
            font=("Segoe UI", 10),
        ).grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 6))

        notes_box = ctk.CTkTextbox(
            section,
            height=90,
            fg_color="#161011",
            border_width=0,
            text_color="#F4EBD0",
            font=("Segoe UI", 11),
        )
        notes_box.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        notes_box.insert("1.0", "Detalle adicional del producto seleccionado...")
        notes_box.configure(state="disabled")
        return section

    def _order_item(self, parent: tk.Misc, nombre: str, cantidad: str, subtotal: str) -> ctk.CTkFrame:
        item = ctk.CTkFrame(parent, fg_color="transparent")
        ctk.CTkLabel(item, text=nombre, text_color="#F4EBD0", font=("Segoe UI", 15, "bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(item, text=subtotal, text_color="#F4EBD0", font=("Segoe UI", 15, "bold")).grid(row=0, column=1, sticky="e", padx=(10, 0))

        controls = ctk.CTkFrame(item, fg_color="transparent")
        controls.grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 0))

        minus_icon = self._make_icon("minus", "#F4EBD0", size=12)
        plus_icon = self._make_icon("plus", "#F4EBD0", size=12)

        ctk.CTkButton(
            controls,
            text="",
            image=minus_icon,
            width=22,
            height=22,
            corner_radius=5,
            fg_color="#3A2524",
            hover_color="#503231",
            command=lambda: None,
        ).pack(side="left", padx=(0, 4))
        ctk.CTkLabel(controls, text=cantidad, text_color="#F4EBD0", fg_color="#3A2524", corner_radius=5, width=24).pack(
            side="left", padx=(0, 4)
        )
        ctk.CTkButton(
            controls,
            text="",
            image=plus_icon,
            width=22,
            height=22,
            corner_radius=5,
            fg_color="#3A2524",
            hover_color="#503231",
            command=lambda: None,
        ).pack(side="left", padx=(0, 4))
        ctk.CTkLabel(
            controls,
            text="Sin picante",
            text_color="#D9C8A9",
            font=("Segoe UI", 9, "italic"),
        ).pack(side="left", padx=(8, 0))

        item.grid_columnconfigure(0, weight=1)
        return item

    def _total_row(self, parent: tk.Misc, label: str, value: str, strong: bool = False) -> ctk.CTkFrame:
        row = ctk.CTkFrame(parent, fg_color="transparent")
        size = 20 if strong else 13
        color = "#F4B39C" if strong else "#E5D7BC"

        ctk.CTkLabel(row, text=label, text_color="#F4EBD0", font=("Segoe UI", size, "bold" if strong else "normal")).pack(side="left")
        ctk.CTkLabel(row, text=value, text_color=color, font=("Segoe UI", size, "bold")).pack(side="right")
        return row

    def _make_icon(self, name: str, color: str, size: int = 18) -> ImageTk.PhotoImage:
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        padding = max(2, size // 8)
        stroke = max(1, size // 8)

        if name == "orders":
            draw.rounded_rectangle((padding, padding, size - padding, size - padding), radius=3, outline=color, width=stroke)
            draw.line((padding * 2, padding + 3, size - padding * 2, padding + 3), fill=color, width=stroke)
            draw.line((padding * 2, size // 2, size - padding * 2, size // 2), fill=color, width=stroke)
        elif name == "kitchen":
            draw.arc((padding, padding + 1, size - padding, size - padding), start=180, end=360, fill=color, width=stroke)
            draw.line((padding + 2, size // 2, size - padding - 2, size // 2), fill=color, width=stroke)
            draw.line((size // 2, padding + 2, size // 2, padding + 6), fill=color, width=stroke)
        elif name == "inventory":
            draw.polygon(
                [(padding + 1, size // 2), (size // 2, padding + 1), (size - padding - 1, size // 2), (size // 2, size - padding - 1)],
                outline=color,
                fill=None,
            )
            draw.line((padding + 4, size // 2, size - padding - 4, size // 2), fill=color, width=stroke)
        elif name == "menu":
            for y in (padding + 2, size // 2, size - padding - 2):
                draw.line((padding, y, size - padding, y), fill=color, width=stroke)
        elif name == "help":
            draw.ellipse((padding, padding, size - padding, size - padding), outline=color, width=stroke)
            draw.line((size // 2, padding + 5, size // 2, size // 2), fill=color, width=stroke)
            draw.point((size // 2, size - padding - 4), fill=color)
        elif name == "logout":
            draw.rectangle((padding + 5, padding, size - padding - 2, size - padding), outline=color, width=stroke)
            draw.line((padding, size // 2, size - padding - 4, size // 2), fill=color, width=stroke)
            draw.polygon([(size - padding - 6, size // 2 - 4), (size - padding - 1, size // 2), (size - padding - 6, size // 2 + 4)], fill=color)
        elif name == "receipt":
            draw.rounded_rectangle((padding + 1, padding, size - padding - 1, size - padding), radius=2, outline=color, width=stroke)
            for y in range(padding + 4, size - padding - 2, 4):
                draw.line((padding + 4, y, size - padding - 4, y), fill=color, width=1)
        elif name == "send":
            draw.line((padding, size // 2, size - padding - 5, size // 2), fill=color, width=stroke)
            draw.polygon([(size - padding - 8, size // 2 - 5), (size - padding - 1, size // 2), (size - padding - 8, size // 2 + 5)], fill=color)
        elif name == "cash":
            draw.rounded_rectangle((padding, padding + 2, size - padding, size - padding - 2), radius=3, outline=color, width=stroke)
            draw.rectangle((padding + 4, padding + 5, size - padding - 4, padding + 8), fill=color)
            draw.ellipse((size // 2 - 2, size // 2 - 2, size // 2 + 2, size // 2 + 2), fill=color)
        elif name == "dish":
            draw.ellipse((padding, padding + 6, size - padding, size - padding - 1), outline=color, width=stroke)
            draw.arc((padding + 5, padding - 1, size - padding - 5, size - padding - 5), start=180, end=360, fill=color, width=stroke)
            draw.line((size // 2, padding + 2, size // 2, padding + 7), fill=color, width=stroke)
            draw.line((size // 2 - 3, padding + 4, size // 2 + 3, padding + 4), fill=color, width=stroke)
        elif name == "minus":
            draw.line((padding + 2, size // 2, size - padding - 2, size // 2), fill=color, width=stroke)
        elif name == "plus":
            draw.line((padding + 2, size // 2, size - padding - 2, size // 2), fill=color, width=stroke)
            draw.line((size // 2, padding + 2, size // 2, size - padding - 2), fill=color, width=stroke)
        else:
            draw.ellipse((padding, padding, size - padding, size - padding), outline=color, width=stroke)

        icon = ImageTk.PhotoImage(image)
        self._icon_refs.append(icon)
        return icon

    def _logout_to_login(self) -> None:
        self.controlador_mesero.stop_polling()
        self._cleanup_event_listeners()
        if hasattr(self.parent, "show_login"):
            self.parent.show_login()
        else:
            self.destroy()
