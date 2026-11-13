from __future__ import annotations

from collections.abc import Callable
import tkinter as tk

import customtkinter as ctk


class VistaPedidoActual:
    """Vista del panel Pedido Actual: solo construccion visual."""

    def __init__(self, parent: tk.Misc, ticket_numero: int = 2, mesa_texto: str = "MESA 1") -> None:
        self.parent = parent
        self.ticket_numero = ticket_numero
        self.mesa_texto = mesa_texto

        self.on_sumar: Callable[[str], None] | None = None
        self.on_restar: Callable[[str], None] | None = None
        self.on_nota: Callable[[str], None] | None = None
        self.on_precuenta: Callable[[], None] | None = None
        self.on_a_cocina: Callable[[], None] | None = None
        self.on_cerrar_y_pagar: Callable[[], None] | None = None
        self.on_salir: Callable[[], None] | None = None

        self.frame = ctk.CTkFrame(parent, fg_color="#2A1718", width=320, corner_radius=0)
        self.frame.grid(row=0, column=1, sticky="nsew")
        self.frame.grid_propagate(False)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self._ticket_label: ctk.CTkLabel | None = None
        self._mesa_label: ctk.CTkLabel | None = None
        self._subtotal_value: ctk.CTkLabel | None = None
        self._impuesto_value: ctk.CTkLabel | None = None
        self._total_value: ctk.CTkLabel | None = None
        self._items_container: ctk.CTkScrollableFrame | None = None
        self._empty_label: ctk.CTkLabel | None = None
        self._item_rows: dict[str, ctk.CTkFrame] = {}

        self._construir()

    def _construir(self) -> None:
        header = ctk.CTkFrame(self.frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=14, pady=(14, 10))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(header, text="Ticket", text_color="#F4EBD0", font=("Segoe UI", 29, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        self._mesa_label = ctk.CTkLabel(
            header,
            text=self.mesa_texto,
            text_color="#3A1E18",
            fg_color="#E8A995",
            corner_radius=10,
            font=("Segoe UI", 9, "bold"),
            padx=9,
            pady=3,
        )
        self._mesa_label.grid(row=0, column=1, sticky="e", padx=(12, 0))

        self._ticket_label = ctk.CTkLabel(header, text=f"TICKET #{self.ticket_numero:05d}", text_color="#D6C9A8", font=("Segoe UI", 11, "bold"))
        self._ticket_label.grid(row=1, column=0, sticky="w", pady=(4, 0))
        
        self.tipo_pedido_var = ctk.StringVar(value="Mesa")
        self._tipo_pedido_switch = ctk.CTkSegmentedButton(
            header,
            values=["Mesa", "Para llevar"],
            variable=self.tipo_pedido_var,
            font=("Segoe UI", 11, "bold"),
            fg_color="#3A1E18",
            selected_color="#E8A995",
            selected_hover_color="#F8B7A5",
            unselected_color="#2A1718",
            unselected_hover_color="#3A1E18"
        )
        self._tipo_pedido_switch.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        pass

        self._items_container = ctk.CTkScrollableFrame(self.frame, fg_color="#2A1718", corner_radius=0)
        self._items_container.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 10))
        self._items_container.grid_columnconfigure(0, weight=1)

        self._empty_label = ctk.CTkLabel(
            self._items_container,
            text="Sin productos en el pedido",
            text_color="#D6C9A8",
            font=("Segoe UI", 12, "bold"),
        )
        self._empty_label.grid(row=0, column=0, sticky="w", pady=(4, 0))

        totals = ctk.CTkFrame(self.frame, fg_color="transparent")
        totals.grid(row=2, column=0, sticky="ew", padx=14, pady=(0, 10))
        totals.grid_columnconfigure(1, weight=1)

        self._subtotal_value = self._total_row(totals, 0, "Subtotal")
        self._total_value = self._total_row(totals, 1, "Total a pagar", total=True)

        actions = ctk.CTkFrame(self.frame, fg_color="transparent")
        actions.grid(row=3, column=0, sticky="ew", padx=14, pady=(0, 14))
        actions.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            actions,
            text="Pendientes",
            fg_color="#3A2524",
            hover_color="#503231",
            text_color="#F4EBD0",
            font=("Segoe UI", 12, "bold"),
            command=self._call_precuenta,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6), pady=(0, 10))

        ctk.CTkButton(
            actions,
            text="A Cocina",
            fg_color="#F0A58E",
            hover_color="#F8B7A5",
            text_color="#2A1718",
            font=("Segoe UI", 12, "bold"),
            command=self._call_a_cocina,
        ).grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=(0, 10))

        ctk.CTkButton(
            actions,
            text="Salir",
            corner_radius=8,
            fg_color="#1A0D0C",
            hover_color="#2A1A18",
            text_color="#F4EBD0",
            font=("Segoe UI", 12, "bold"),
            height=34,
            command=self._call_salir,
        ).grid(row=1, column=0, sticky="ew", padx=(0, 6))

        ctk.CTkButton(
            actions,
            text="🗑 Limpiar Ticket",
            corner_radius=8,
            fg_color="#4A1418",
            hover_color="#631B20",
            text_color="#F4EBD0",
            font=("Segoe UI", 12, "bold"),
            height=34,
            command=self._call_limpiar,
        ).grid(row=1, column=1, sticky="ew", padx=(6, 0))

    def configurar_acciones(
        self,
        on_sumar: Callable[[str], None] | None = None,
        on_restar: Callable[[str], None] | None = None,
        on_nota: Callable[[str], None] | None = None,
        on_precuenta: Callable[[], None] | None = None,
        on_a_cocina: Callable[[], None] | None = None,
        on_cerrar_y_pagar: Callable[[], None] | None = None,
        on_salir: Callable[[], None] | None = None,
        on_limpiar: Callable[[], None] | None = None,
    ) -> None:
        self.on_sumar = on_sumar
        self.on_restar = on_restar
        self.on_nota = on_nota
        self.on_precuenta = on_precuenta
        self.on_a_cocina = on_a_cocina
        self.on_cerrar_y_pagar = on_cerrar_y_pagar
        self.on_salir = on_salir
        self.on_limpiar = on_limpiar

    def redibujar(self, items: list[dict[str, object]]) -> None:
        if self._items_container is None:
            return

        for child in self._items_container.winfo_children():
            child.destroy()
        self._item_rows.clear()

        if not items:
            self._empty_label = ctk.CTkLabel(
                self._items_container,
                text="Sin productos en el pedido",
                text_color="#D6C9A8",
                font=("Segoe UI", 12, "bold"),
            )
            self._empty_label.grid(row=0, column=0, sticky="w", pady=(4, 0))
            return

        self._empty_label = None
        for index, item in enumerate(items):
            self.dibujar_item(item, index=index)

    def dibujar_item(self, item: dict[str, object], index: int | None = None) -> ctk.CTkFrame:
        if self._items_container is None:
            raise RuntimeError("La vista del pedido actual no fue construida.")

        item_id = str(item.get("id_item") or "")
        row = ctk.CTkFrame(self._items_container, fg_color="#231819", corner_radius=7)
        row.grid_columnconfigure(0, weight=1)
        if index is None:
            index = len(self._item_rows)
        row.grid(row=index, column=0, sticky="ew", pady=(0, 8))

        top = ctk.CTkFrame(row, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=8, pady=(7, 2))
        top.grid_columnconfigure(0, weight=1)

        nombre = str(item.get("nombre", "Producto"))
        cantidad = int(item.get("cantidad") or 1)
        precio = float(item.get("precio") or 0.0)
        notas = str(item.get("notas") or "").strip()

        ctk.CTkLabel(
            top,
            text=f"{cantidad}x {nombre}",
            text_color="#F4EBD0",
            font=("Segoe UI", 12, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            top,
            text=f"${(precio * cantidad):,.0f}".replace(",", "."),
            text_color="#E8A27E",
            font=("Segoe UI", 12, "bold"),
        ).grid(row=0, column=1, sticky="e")

        acciones = ctk.CTkFrame(row, fg_color="transparent")
        acciones.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 6))
        acciones.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(
            acciones,
            text="+",
            width=34,
            height=30,
            fg_color="#4FA64F",
            hover_color="#66BB66",
            text_color="#0F2010",
            command=lambda ident=item_id: self._call_sumar(ident),
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            acciones,
            text="-",
            width=34,
            height=30,
            fg_color="#8C1A11",
            hover_color="#A1241A",
            text_color="#F4EBD0",
            command=lambda ident=item_id: self._call_restar(ident),
        ).grid(row=0, column=1)

        ctk.CTkButton(
            acciones,
            text="Nota",
            height=30,
            fg_color="#3A2524",
            hover_color="#503231",
            text_color="#F4EBD0",
            command=lambda ident=item_id: self._call_nota(ident),
        ).grid(row=0, column=2, sticky="e")

        if notas:
            ctk.CTkLabel(
                row,
                text=notas,
                text_color="#F19B95",
                font=("Segoe UI", 11, "italic"),
                wraplength=250,
                justify="left",
                anchor="w",
            ).grid(row=2, column=0, sticky="ew", padx=8, pady=(0, 8))

        self._item_rows[item_id] = row
        return row

    def actualizar_totales(self, totales: dict[str, float]) -> None:
        if self._subtotal_value is not None:
            self._subtotal_value.configure(text=f"${totales.get('subtotal', 0.0):,.0f}".replace(",", "."))
        if self._total_value is not None:
            self._total_value.configure(text=f"${totales.get('total', 0.0):,.0f}".replace(",", "."))

    def actualizar_ticket(self, numero_ticket: int) -> None:
        self.ticket_numero = numero_ticket
        if self._ticket_label is not None:
            self._ticket_label.configure(text=f"TICKET #{numero_ticket:05d}")

    def actualizar_mesa(self, mesa_texto: str) -> None:
        self.mesa_texto = str(mesa_texto)
        if self._mesa_label is not None:
            self._mesa_label.configure(text=self.mesa_texto)

    def pedir_nota(self, titulo: str = "Agregar nota") -> str | None:
        owner = self.frame.winfo_toplevel()
        dialog = ctk.CTkToplevel(owner)
        dialog.title(titulo)
        dialog.geometry("460x320")
        dialog.minsize(420, 300)
        dialog.resizable(True, True)
        dialog.configure(fg_color="#180C0D")
        dialog.transient(owner)
        dialog.grab_set()

        result: dict[str, str | None] = {"value": None}

        dialog.grid_columnconfigure(0, weight=1)
        dialog.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(dialog, fg_color="#231112", corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text=titulo,
            text_color="#F4EBD0",
            font=("Segoe UI", 18, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 0))
        ctk.CTkLabel(
            header,
            text="Observacion para cocina o servicio",
            text_color="#F09F86",
            font=("Segoe UI", 10, "bold"),
        ).grid(row=1, column=0, sticky="w", padx=16, pady=(2, 14))

        body = ctk.CTkFrame(
            dialog,
            fg_color="#241516",
            border_color="#F09F86",
            border_width=1,
            corner_radius=10,
        )
        body.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            body,
            text="Escribe una nota para el item:",
            text_color="#E5D7BC",
            font=("Segoe UI", 11, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        textbox = ctk.CTkTextbox(
            body,
            height=130,
            fg_color="#161011",
            border_color="#7A3931",
            border_width=1,
            text_color="#F4EBD0",
            font=("Segoe UI", 11),
            activate_scrollbars=False,
        )
        textbox.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 10))

        actions = ctk.CTkFrame(body, fg_color="transparent")
        actions.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 12))
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)

        def _close_with_value(value: str | None) -> None:
            result["value"] = value
            dialog.grab_release()
            dialog.destroy()

        def _confirmar() -> None:
            _close_with_value(textbox.get("1.0", "end-1c").strip())

        ctk.CTkButton(
            actions,
            text="Cancelar",
            fg_color="#3A2524",
            hover_color="#503231",
            text_color="#F4EBD0",
            font=("Segoe UI", 12, "bold"),
            command=lambda: _close_with_value(None),
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))

        ctk.CTkButton(
            actions,
            text="Guardar",
            fg_color="#F0A58E",
            hover_color="#F8B7A5",
            text_color="#2A1718",
            font=("Segoe UI", 12, "bold"),
            command=_confirmar,
        ).grid(row=0, column=1, sticky="ew", padx=(6, 0))

        dialog.protocol("WM_DELETE_WINDOW", lambda: _close_with_value(None))
        dialog.bind("<Escape>", lambda _event: _close_with_value(None))
        dialog.bind("<Control-Return>", lambda _event: _confirmar())

        dialog.update_idletasks()
        owner_x = owner.winfo_rootx()
        owner_y = owner.winfo_rooty()
        owner_w = owner.winfo_width()
        owner_h = owner.winfo_height()
        dialog_w = dialog.winfo_width()
        dialog_h = dialog.winfo_height()
        pos_x = owner_x + max((owner_w - dialog_w) // 2, 0)
        pos_y = owner_y + max((owner_h - dialog_h) // 2, 0)
        dialog.geometry(f"+{pos_x}+{pos_y}")

        textbox.focus_set()
        owner.wait_window(dialog)
        return result["value"]

    def _total_row(self, parent: tk.Misc, row: int, etiqueta: str, total: bool = False) -> ctk.CTkLabel:
        ctk.CTkLabel(
            parent,
            text=etiqueta,
            text_color="#E5D7BC",
            font=("Segoe UI", 11, "bold" if total else "normal"),
        ).grid(row=row, column=0, sticky="w", pady=2)
        valor = ctk.CTkLabel(
            parent,
            text="$0",
            text_color="#F4EBD0" if total else "#E8A27E",
            font=("Segoe UI", 12 if total else 11, "bold"),
        )
        valor.grid(row=row, column=1, sticky="e", pady=2)
        return valor

    def _call_sumar(self, id_item: str) -> None:
        if self.on_sumar is not None:
            self.on_sumar(id_item)

    def _call_restar(self, id_item: str) -> None:
        if self.on_restar is not None:
            self.on_restar(id_item)

    def _call_nota(self, id_item: str) -> None:
        if self.on_nota is not None:
            self.on_nota(id_item)

    def _call_precuenta(self) -> None:
        if self.on_precuenta is not None:
            self.on_precuenta()

    def _call_a_cocina(self) -> None:
        if self.on_a_cocina is not None:
            self.on_a_cocina()

    def _call_cerrar_y_pagar(self) -> None:
        if self.on_cerrar_y_pagar is not None:
            self.on_cerrar_y_pagar()

    def _call_salir(self) -> None:
        if self.on_salir is not None:
            self.on_salir()

    def _call_limpiar(self) -> None:
        from tkinter import messagebox
        if messagebox.askyesno("Limpiar Ticket", "¿Está seguro de querer vaciar completamente el ticket actual?"):
            if self.on_limpiar is not None:
                self.on_limpiar()
