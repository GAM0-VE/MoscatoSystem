from __future__ import annotations

from collections.abc import Callable
import tkinter as tk

import customtkinter as ctk


class MesasView:
    """Vista MVC para pintar el plano de mesas en formato grid."""

    COLORES_ESTADO = {
        "libre": {
            "fg": "#355E49",
            "hover": "#41785C",
            "border": "#78F0A6",
            "text": "#F1F7F1",
        },
        "ocupada": {
            "fg": "#7A2C25",
            "hover": "#95382F",
            "border": "#FF8E7A",
            "text": "#FFF4F1",
        },
        "atencion": {
            "fg": "#7C5A17",
            "hover": "#98701D",
            "border": "#FFC94A",
            "text": "#FFF6E4",
        },
    }

    def __init__(self, parent: tk.Misc, columnas: int = 5) -> None:
        self.parent = parent
        self.columnas = max(1, int(columnas))
        self.on_mesa_click: Callable[[int], None] | None = None

        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.grid_columnconfigure(tuple(range(self.columnas)), weight=1)
        self._botones_mesas: dict[int, ctk.CTkButton] = {}
        self._mesa_seleccionada_id: int | None = None
        self._estado_mesas: dict[int, str] = {}
    def configurar_accion_click(self, callback: Callable[[int], None] | None) -> None:
        """Permite que el controlador conecte el click de cada mesa."""
        self.on_mesa_click = callback

    def dibujar_mesas(self, lista_mesas: list[dict[str, object]]) -> None:
        """Recibe datos del modelo y renderiza botones M1, M2, M3..."""
        for child in self.frame.winfo_children():
            child.destroy()
        self._botones_mesas.clear()

        for idx, mesa in enumerate(lista_mesas):
            id_mesa = int(mesa.get("id_mesa") or 0)
            numero_mesa = mesa.get("numero_mesa")
            estado = str(mesa.get("estado") or "Libre")

            if id_mesa <= 0:
                continue

            row = idx // self.columnas
            column = idx % self.columnas

            boton = ctk.CTkButton(
                self.frame,
                text=f"M{numero_mesa}",
                corner_radius=10,
                font=("Segoe UI", 18, "bold"),
                height=74,
                border_width=3,  # Borde fijo a 3 para que no cambie el layout al seleccionar
                command=lambda mesa_id=id_mesa: self._on_click_mesa(mesa_id),
            )
            boton.grid(row=row, column=column, sticky="ew", padx=8, pady=8)

            self._botones_mesas[id_mesa] = boton
            self.actualizar_color_mesa(id_mesa, estado)

    def actualizar_color_mesa(self, id_mesa: int, estado: str) -> None:
        """Actualiza color de la mesa segun estado: Libre, Ocupada o Atencion."""
        boton = self._botones_mesas.get(int(id_mesa))
        if boton is None:
            return

        self._estado_mesas[int(id_mesa)] = estado
        estado_norm = self._normalizar_estado(estado)
        colores = self.COLORES_ESTADO.get(estado_norm, self.COLORES_ESTADO["libre"])
        
        # Borde blanco si está seleccionada
        if self._mesa_seleccionada_id == int(id_mesa):
            border_color = "#FFFFFF"
        else:
            border_color = colores["border"]

        boton.configure(
            fg_color=colores["fg"],
            hover_color=colores["hover"],
            border_color=border_color,
            text_color=colores["text"],
        )

    def marcar_mesa_seleccionada(self, id_mesa: int) -> None:
        """Resalta la mesa seleccionada y restaura la anterior."""
        id_mesa = int(id_mesa)
        anterior = self._mesa_seleccionada_id
        
        self._mesa_seleccionada_id = id_mesa
        
        # Restaurar mesa anterior
        if anterior is not None and anterior != id_mesa:
            estado_ant = self._estado_mesas.get(anterior, "Libre")
            self.actualizar_color_mesa(anterior, estado_ant)
            
        # Resaltar la nueva
        estado_nueva = self._estado_mesas.get(id_mesa, "Libre")
        self.actualizar_color_mesa(id_mesa, estado_nueva)

    def _on_click_mesa(self, id_mesa: int) -> None:
        if self.on_mesa_click is not None:
            self.on_mesa_click(id_mesa)

    @staticmethod
    def _normalizar_estado(estado: str) -> str:
        texto = (estado or "").strip().lower()
        if texto in {"atencion", "atención"}:
            return "atencion"
        if texto == "ocupada":
            return "ocupada"
        return "libre"


def _run_demo() -> None:
    """Demo local de la vista de mesas sin dependencia de DB/controlador real."""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTk()
    app.title("Demo - Plano de Mesas")
    app.geometry("1200x380")
    app.minsize(980, 320)
    app.configure(fg_color="#16181A")

    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=1)

    titulo = ctk.CTkLabel(
        app,
        text="Plano de Mesas (Demo)",
        text_color="#F4EBD0",
        font=("Segoe UI", 28, "bold"),
    )
    titulo.grid(row=0, column=0, sticky="w", padx=16, pady=(14, 6))

    contenedor = ctk.CTkFrame(app, fg_color="#16181A")
    contenedor.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 8))
    contenedor.grid_columnconfigure(0, weight=1)

    canvas = tk.Canvas(contenedor, bg="#16181A", bd=0, highlightthickness=0, height=110)
    canvas.grid(row=0, column=0, sticky="ew")

    scroll = tk.Scrollbar(
        contenedor,
        orient="horizontal",
        command=canvas.xview,
        troughcolor="#16181A",
        bg="#16181A",
        activebackground="#2A2324",
        width=6,
        highlightthickness=0,
        bd=0,
        relief="flat",
    )
    scroll.grid(row=1, column=0, sticky="ew", pady=(2, 0))
    canvas.configure(xscrollcommand=scroll.set)

    vista = MesasView(canvas, columnas=10)
    canvas_window = canvas.create_window((0, 0), window=vista.frame, anchor="nw")

    def _sync_scroll(_event: tk.Event | None = None) -> None:
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _sync_canvas(event: tk.Event) -> None:
        canvas.itemconfigure(canvas_window, height=event.height)
        canvas.configure(scrollregion=canvas.bbox("all"))

    vista.frame.bind("<Configure>", _sync_scroll)
    canvas.bind("<Configure>", _sync_canvas)

    mesas_data = [
        {"id_mesa": idx, "numero_mesa": idx, "estado": "Libre"}
        for idx in range(1, 11)
    ]
    vista.dibujar_mesas(mesas_data)

    estado_por_mesa = {idx: "Libre" for idx in range(1, 11)}
    secuencia = {"Libre": "Ocupada", "Ocupada": "Atencion", "Atencion": "Libre"}

    def _on_click_mesa(id_mesa: int) -> None:
        actual = estado_por_mesa.get(id_mesa, "Libre")
        nuevo = secuencia[actual]
        estado_por_mesa[id_mesa] = nuevo
        vista.actualizar_color_mesa(id_mesa, nuevo)
        estado_label.configure(text=f"Mesa seleccionada: M{id_mesa} | Nuevo estado: {nuevo}")

    vista.configurar_accion_click(_on_click_mesa)

    acciones = ctk.CTkFrame(app, fg_color="transparent")
    acciones.grid(row=2, column=0, sticky="ew", padx=14, pady=(6, 12))
    acciones.grid_columnconfigure((0, 1, 2, 3), weight=1)

    def _aplicar_estado_todas(estado: str) -> None:
        for id_mesa in estado_por_mesa:
            estado_por_mesa[id_mesa] = estado
            vista.actualizar_color_mesa(id_mesa, estado)
        estado_label.configure(text=f"Estado aplicado a todas: {estado}")

    ctk.CTkButton(
        acciones,
        text="Todas Libre",
        fg_color="#355E49",
        hover_color="#41785C",
        border_color="#78F0A6",
        border_width=1,
        text_color="#F1F7F1",
        command=lambda: _aplicar_estado_todas("Libre"),
    ).grid(row=0, column=0, sticky="ew", padx=4)

    ctk.CTkButton(
        acciones,
        text="Todas Ocupada",
        fg_color="#7A2C25",
        hover_color="#95382F",
        border_color="#FF8E7A",
        border_width=1,
        text_color="#FFF4F1",
        command=lambda: _aplicar_estado_todas("Ocupada"),
    ).grid(row=0, column=1, sticky="ew", padx=4)

    ctk.CTkButton(
        acciones,
        text="Todas Atencion",
        fg_color="#7C5A17",
        hover_color="#98701D",
        border_color="#FFC94A",
        border_width=1,
        text_color="#FFF6E4",
        command=lambda: _aplicar_estado_todas("Atencion"),
    ).grid(row=0, column=2, sticky="ew", padx=4)

    ctk.CTkButton(
        acciones,
        text="Reset 1..10",
        fg_color="#3A2B2A",
        hover_color="#4A3836",
        text_color="#F4EBD0",
        command=lambda: _aplicar_estado_todas("Libre"),
    ).grid(row=0, column=3, sticky="ew", padx=4)

    estado_label = ctk.CTkLabel(
        app,
        text="Click en una mesa para alternar: Libre -> Ocupada -> Atencion",
        text_color="#D6C9A8",
        font=("Segoe UI", 12, "bold"),
    )
    estado_label.grid(row=3, column=0, sticky="w", padx=16, pady=(0, 12))

    app.mainloop()


if __name__ == "__main__":
    _run_demo()
