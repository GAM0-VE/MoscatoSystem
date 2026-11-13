from __future__ import annotations

from typing import Callable

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk


class AuditoriaView:
    """Vista MVC para consultar y mostrar registros de auditoría."""

    COLORS = {
        "window": "#1A1C1E",
        "panel": "#231719",
        "panel_soft": "#2D1E21",
        "panel_border": "#4A3134",
        "header_cell": "#312326",
        "row_a": "#281B1E",
        "row_b": "#24181B",
        "text_primary": "#F4EBD0",
        "text_secondary": "#867370",
        "text_warm": "#D8CDB2",
        "accent": "#8C1A11",
        "accent_hover": "#A1241A",
        "accent_soft": "#DFA99D",
        "muted": "#B4A791",
        "input_bg": "#0F1113",
        "input_hover": "#352D2D",
    }

    def __init__(self, parent: tk.Misc) -> None:
        self.parent = parent
        self._buscar_callback: Callable[[], None] | None = None
        self._rows: list[ctk.CTkFrame] = []
        self._pagina_actual = 1
        self._tamano_pagina = 10
        self._total_registros = 0
        self._registros_totales: list[dict[str, object]] = []
        self._page_buttons: list[ctk.CTkButton] = []

        self.frame = ctk.CTkFrame(
            parent,
            fg_color=self.COLORS["window"],
            corner_radius=0,
            border_width=0,
        )
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_rowconfigure(1, weight=0)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=0)

        self._build_header()
        self._build_filters()
        self._build_table()
        self._build_pagination()

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self.frame, fg_color="transparent", corner_radius=0, border_width=0)
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=(6, 10))
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)

        title_wrap = ctk.CTkFrame(header, fg_color="transparent", corner_radius=0)
        title_wrap.grid(row=0, column=0, sticky="w")

        self.title = ctk.CTkLabel(
            title_wrap,
            text="Auditoría del Sistema",
            text_color=self.COLORS["text_primary"],
            font=("Segoe UI", 30, "bold"),
            anchor="w",
        )
        self.title.grid(row=0, column=0, sticky="w")

        self.subtitle = ctk.CTkLabel(
            title_wrap,
            text="Registro cronológico de operaciones y cambios críticos",
            text_color=self.COLORS["text_secondary"],
            font=("Segoe UI", 12),
            anchor="w",
        )
        self.subtitle.grid(row=1, column=0, sticky="w", pady=(2, 0))

        self.export_btn = ctk.CTkButton(
            header,
            text="📥 Exportar Excel",
            width=140,
            height=32,
            corner_radius=6,
            fg_color="#2EA44F",
            hover_color="#268841",
            border_width=0,
            text_color="#FFFFFF",
            font=("Segoe UI", 12, "bold"),
            command=self._exportar_excel,
        )
        self.export_btn.grid(row=0, column=1, sticky="e", pady=(10, 0))

    def _build_filters(self) -> None:
        filters = ctk.CTkFrame(
            self.frame,
            fg_color=self.COLORS["panel"],
            corner_radius=10,
            border_width=1,
            border_color=self.COLORS["panel_border"],
        )
        filters.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        filters.grid_columnconfigure((0, 1, 2, 3), weight=1)

        labels = [
            ("Rango de Fecha", 0, 0),
            ("Usuario", 0, 1),
            ("Categoría", 0, 2),
        ]

        for text, row, col in labels:
            ctk.CTkLabel(
                filters,
                text=text,
                text_color=self.COLORS["text_warm"],
                font=("Segoe UI", 11, "bold"),
                anchor="w",
            ).grid(row=row, column=col, sticky="w", padx=(14, 10), pady=(12, 6))

        fecha_options = ["Hoy", "Ayer", "Últimos 7 días", "Todos"]
        self.fecha_inicio_var = tk.StringVar(value="Hoy")
        self.fecha_input = ctk.CTkOptionMenu(
            filters,
            variable=self.fecha_inicio_var,
            values=fecha_options,
            fg_color=self.COLORS["input_bg"],
            button_color="#221E1F",
            button_hover_color=self.COLORS["input_hover"],
            text_color=self.COLORS["text_primary"],
            dropdown_fg_color=self.COLORS["panel"],
            dropdown_text_color=self.COLORS["text_primary"],
            width=210,
            height=34,
            corner_radius=6,
        )
        self.fecha_input.grid(row=1, column=0, sticky="ew", padx=(14, 10), pady=(0, 12))

        self.usuario_lookup: dict[str, int | None] = {"Todos los usuarios": None}
        self.usuario_var = tk.StringVar(value="Todos los usuarios")
        self.usuario_input = ctk.CTkOptionMenu(
            filters,
            variable=self.usuario_var,
            values=["Todos los usuarios"],
            fg_color=self.COLORS["input_bg"],
            button_color="#221E1F",
            button_hover_color=self.COLORS["input_hover"],
            text_color=self.COLORS["text_primary"],
            dropdown_fg_color=self.COLORS["panel"],
            dropdown_text_color=self.COLORS["text_primary"],
            width=210,
            height=34,
            corner_radius=6,
        )
        self.usuario_input.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(0, 12))

        self.categoria_var = tk.StringVar(value="Cualquier acción")
        self.categoria_input = ctk.CTkOptionMenu(
            filters,
            variable=self.categoria_var,
            values=["Cualquier acción", "Inicio de sesión", "Creación", "Eliminación", "Actualización", "Descuento"],
            fg_color=self.COLORS["input_bg"],
            button_color="#221E1F",
            button_hover_color=self.COLORS["input_hover"],
            text_color=self.COLORS["text_primary"],
            dropdown_fg_color=self.COLORS["panel"],
            dropdown_text_color=self.COLORS["text_primary"],
            width=210,
            height=34,
            corner_radius=6,
        )
        self.categoria_input.grid(row=1, column=2, sticky="ew", padx=(0, 10), pady=(0, 12))

        self.btn_buscar = ctk.CTkButton(
            filters,
            text="Aplicar filtros",
            fg_color=self.COLORS["accent"],
            hover_color=self.COLORS["accent_hover"],
            border_width=0,
            text_color="#F4EBD0",
            font=("Segoe UI", 11, "bold"),
            height=34,
            corner_radius=6,
            command=self._ejecutar_busqueda,
        )
        self.btn_buscar.grid(row=1, column=3, sticky="ew", padx=(0, 14), pady=(0, 12))

    def _build_table(self) -> None:
        table_shell = ctk.CTkFrame(
            self.frame,
            fg_color="transparent",
            corner_radius=8,
            border_width=0,
            border_color=self.COLORS["panel_border"],
        )
        table_shell.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
        table_shell.grid_columnconfigure(0, weight=1)

        table_frame = ctk.CTkFrame(
            table_shell,
            fg_color="#2A1C1D",
            corner_radius=6,
            border_width=1,
            border_color=self.COLORS["panel_border"],
        )
        table_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        table_frame.grid_columnconfigure(0, weight=1)

        self.table_header = ctk.CTkFrame(
            table_frame,
            fg_color=self.COLORS["header_cell"],
            corner_radius=6,
            border_width=1,
            border_color=self.COLORS["panel_border"],
        )
        self.table_header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        for idx, weight in enumerate([12, 17, 10, 18, 40, 15]):
            self.table_header.grid_columnconfigure(idx, weight=weight, uniform="audit_cols")

        header_texts = ["TIMESTAMP", "USUARIO", "ACCIÓN", "ENTIDAD", "DETALLE", "IP"]
        for index, text in enumerate(header_texts):
            ctk.CTkLabel(
                self.table_header,
                text=text,
                text_color=self.COLORS["text_warm"],
                font=("Segoe UI", 10, "bold"),
                anchor="center",
            ).grid(row=0, column=index, sticky="ew", padx=(12, 10), pady=(12, 12))

        self.rows_container = ctk.CTkFrame(table_frame, fg_color="transparent")
        self.rows_container.grid(row=1, column=0, sticky="nsew", padx=(0, 0), pady=(2, 2))
        for idx, weight in enumerate([12, 17, 10, 18, 40, 15]):
            self.rows_container.grid_columnconfigure(idx, weight=weight, uniform="audit_cols")

    def _build_pagination(self) -> None:
        self.footer = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.footer.grid(row=3, column=0, sticky="ew", pady=(12, 0))
        self.footer.grid_columnconfigure(0, weight=1)

        self.summary_label = ctk.CTkLabel(
            self.footer,
            text="Mostrando 0-0 de 0 resultados",
            text_color=self.COLORS["muted"],
            font=("Segoe UI", 11),
            anchor="w",
        )
        self.summary_label.grid(row=0, column=0, sticky="w")

        self.page_box = ctk.CTkFrame(self.footer, fg_color="transparent")
        self.page_box.grid(row=0, column=1, sticky="e")

        self._page_buttons = []
        self._update_pagination_buttons()

    @staticmethod
    def _calcular_total_paginas(total_registros: int, tamano_pagina: int = 7) -> int:
        if total_registros <= 0:
            return 1
        return max(1, (total_registros + tamano_pagina - 1) // tamano_pagina)

    def _set_pagina(self, numero_pagina: int) -> None:
        if self._total_registros <= 0:
            self._pagina_actual = 1
            return

        total_paginas = self._calcular_total_paginas(self._total_registros, self._tamano_pagina)
        self._pagina_actual = max(1, min(int(numero_pagina), total_paginas))
        if self._buscar_callback is not None:
            self._buscar_callback()
        else:
            self.poblar_tabla(self._registros_totales)

    def _update_pagination_buttons(self) -> None:
        for btn in self._page_buttons:
            btn.destroy()
        self._page_buttons.clear()

        total_paginas = self._calcular_total_paginas(self._total_registros, self._tamano_pagina)
        botones = ["<"]

        if total_paginas <= 5:
            botones.extend(str(i) for i in range(1, total_paginas + 1))
        else:
            inicio = max(1, self._pagina_actual - 1)
            fin = min(total_paginas, self._pagina_actual + 1)

            if self._pagina_actual > 2:
                botones.append("1")
                botones.append("...")

            for i in range(inicio, fin + 1):
                botones.append(str(i))

            if self._pagina_actual < total_paginas - 1:
                botones.append("...")
                botones.append(str(total_paginas))

        botones.append(">")

        for idx, value in enumerate(botones):
            is_active = value.isdigit() and int(value) == self._pagina_actual
            fg = self.COLORS["text_primary"] if is_active else self.COLORS["text_warm"]
            bgcolor = self.COLORS["accent"] if is_active else "#2A2D2F"
            border = self.COLORS["accent"] if is_active else self.COLORS["panel_border"]
            btn = ctk.CTkButton(
                self.page_box,
                text=value,
                width=28,
                height=28,
                fg_color=bgcolor,
                hover_color="#3A3E42",
                border_width=1,
                border_color=border,
                text_color=fg,
                font=("Segoe UI", 10, "bold"),
                command=lambda v=value: self._on_pagination_click(v),
            )
            btn.grid(row=0, column=idx, padx=(0, 6))
            self._page_buttons.append(btn)

    def _on_pagination_click(self, value: str) -> None:
        if value == "<":
            self._set_pagina(self._pagina_actual - 1)
            return
        if value == ">":
            self._set_pagina(self._pagina_actual + 1)
            return
        if value == "...":
            return
        try:
            self._set_pagina(int(value))
        except ValueError:
            return

    def configurar_busqueda(self, callback: Callable[[], None]) -> None:
        self._buscar_callback = callback

    def _ejecutar_busqueda(self) -> None:
        if self._buscar_callback is not None:
            self._buscar_callback()

    def set_usuarios(self, usuarios: list[dict[str, object]]) -> None:
        opciones = ["Todos los usuarios"]
        self.usuario_lookup = {"Todos los usuarios": None}
        for usuario in usuarios or []:
            nombre = str(usuario.get("nombre") or usuario.get("username") or "Usuario sin nombre").strip()
            if not nombre:
                continue
            user_id = usuario.get("id")
            if user_id is not None:
                self.usuario_lookup[nombre] = int(user_id)
            opciones.append(nombre)

        if self.usuario_input is not None:
            self.usuario_input.configure(values=opciones)
        if self.usuario_var.get() not in self.usuario_lookup:
            self.usuario_var.set("Todos los usuarios")

    def obtener_filtros(self) -> dict[str, str | int | None]:
        usuario = self.usuario_var.get().strip()
        usuario_id = self.usuario_lookup.get(usuario)
        fecha_seleccionada = self.fecha_inicio_var.get().strip() or None
        accion = self.categoria_var.get().strip() or None
        return {
            "fecha_inicio": fecha_seleccionada,
            "fecha_fin": fecha_seleccionada,
            "id_usuario": usuario_id,
            "accion": accion,
        }

    def limpiar_tabla(self) -> None:
        for row in self._rows:
            row.destroy()
        self._rows.clear()

        if hasattr(self, "empty_state_label") and self.empty_state_label.winfo_exists():
            self.empty_state_label.destroy()

    def _mostrar_sin_registros(self) -> None:
        self.empty_state_label = ctk.CTkLabel(
            self.rows_container,
            text="No se encontraron resultados para los filtros seleccionados.",
            text_color=self.COLORS["text_secondary"],
            font=("Segoe UI", 12),
            anchor="center",
        )
        self.empty_state_label.grid(row=0, column=0, sticky="nsew", padx=18, pady=28)
        self.summary_label.configure(text="Mostrando 0-0 de 0 resultados")

    def poblar_tabla(self, registros: list[dict[str, object]]) -> None:
        self._registros_totales = list(registros or [])
        self._total_registros = len(self._registros_totales)

        if self._total_registros <= 0:
            self.limpiar_tabla()
            self._mostrar_sin_registros()
            self._pagina_actual = 1
            self._update_pagination_buttons()
            return

        total_paginas = self._calcular_total_paginas(self._total_registros, self._tamano_pagina)
        self._pagina_actual = max(1, min(self._pagina_actual, total_paginas))
        inicio = (self._pagina_actual - 1) * self._tamano_pagina
        fin = inicio + self._tamano_pagina
        pagina_actual = self._registros_totales[inicio:fin]

        self.limpiar_tabla()
        total = len(self._registros_totales)
        primer = inicio + 1 if total else 0
        ultimo = min(fin, total)
        self.summary_label.configure(text=f"Mostrando {primer}-{ultimo} de {total} resultados")

        for idx, registro in enumerate(pagina_actual):
            row = ctk.CTkFrame(
                self.rows_container,
                fg_color=self.COLORS["row_a"] if idx % 2 == 0 else self.COLORS["row_b"],
                corner_radius=6,
                border_width=1,
                border_color=self.COLORS["panel_border"],
            )
            row.grid(row=idx, column=0, columnspan=6, sticky="ew", pady=(0, 2), padx=(0, 0))
            for col_idx, weight in enumerate([12, 17, 10, 18, 40, 15]):
                row.grid_columnconfigure(col_idx, weight=weight, uniform="audit_cols")
            self._rows.append(row)

            timestamp = str(registro.get("fecha_hora", "-")).split(" ")
            timestamp_value = timestamp[0] if timestamp else "-"
            time_value = timestamp[1] if len(timestamp) > 1 else "-"

            labels = [
                f"{timestamp_value}\n{time_value}",
                str(registro.get("usuario", "-") or "-"),
                "",
                str(registro.get("tabla_afectada", "-") or "-"),
                str(registro.get("detalles", "-") or "-"),
                "192.168.1.12",
            ]

            accion = str(registro.get("accion", "-") or "-")
            action_bg = {
                "INSERTAR": self.COLORS["accent"],
                "ACTUALIZAR": self.COLORS["accent"],
                "ELIMINAR": self.COLORS["accent"],
                "LOGIN": self.COLORS["accent"],
                "DESCUENTO": self.COLORS["accent"],
                "PRECIO": self.COLORS["accent"],
                "STOCK": self.COLORS["accent"],
            }.get(accion.upper(), self.COLORS["accent"])

            for col_index, content in enumerate(labels[:2] + [" "] + labels[3:]):
                if col_index == 2:
                    badge = ctk.CTkFrame(row, fg_color=action_bg, corner_radius=4, width=118, height=34)
                    badge.grid(row=0, column=2, sticky="w", padx=(12, 10), pady=(10, 10))
                    badge.grid_propagate(False)
                    ctk.CTkLabel(
                        badge,
                        text=accion.upper(),
                        text_color="#F7E8D6",
                        font=("Segoe UI", 10, "bold"),
                        anchor="center",
                    ).place(relx=0.5, rely=0.5, anchor="center")
                    continue

                widget = ctk.CTkLabel(
                    row,
                    text=content,
                    text_color=self.COLORS["text_primary"],
                    font=("Segoe UI", 11),
                    anchor="w" if col_index == 4 else "center",
                    justify="left" if col_index == 4 else "center",
                    wraplength=380 if col_index == 4 else 0,
                )
                widget.grid(row=0, column=col_index, sticky="ew", padx=(14, 12), pady=(12, 12))

            self.rows_container.grid_rowconfigure(idx, weight=1)

        self._update_pagination_buttons()

    def _exportar_excel(self) -> None:
        if not hasattr(self, '_registros_totales') or not self._registros_totales:
            self.mostrar_info("No hay registros para exportar.")
            return
            
        from tkinter import filedialog
        
        filepath = filedialog.asksaveasfilename(
            parent=self.frame,
            title="Exportar Auditoría",
            defaultextension=".xlsx",
            filetypes=[("Archivos Excel", "*.xlsx")],
            initialfile="Auditoria_Moscato.xlsx"
        )
        if not filepath:
            return
            
        try:
            try:
                from src.utils.excel_export import guardar_como_excel
            except ImportError:
                import sys
                import os
                current_dir = os.path.dirname(os.path.abspath(__file__))
                src_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
                if src_dir not in sys.path:
                    sys.path.insert(0, src_dir)
                from utils.excel_export import guardar_como_excel
            
            filas = []
            filas.append(["FECHA Y HORA", "USUARIO", "ACCIÓN", "TABLA AFECTADA", "DETALLES", "IP ORIGEN"])
            for reg in self._registros_totales:
                filas.append([
                    str(reg.get("fecha_hora", "-")),
                    str(reg.get("usuario", "-")),
                    str(reg.get("accion", "-")),
                    str(reg.get("tabla_afectada", "-")),
                    str(reg.get("detalles", "-")),
                    "192.168.1.12"
                ])
                
            guardar_como_excel(filepath, filas)
            self.mostrar_info(f"Datos exportados correctamente a:\n{filepath}")
        except ImportError:
            self.mostrar_error("Falta la librería openpyxl.\nEjecuta: pip install openpyxl")
        except Exception as e:
            self.mostrar_error(f"Error al exportar:\n{e}")

    def mostrar_error(self, mensaje: str) -> None:
        messagebox.showerror("Auditoría", mensaje)

    def mostrar_info(self, mensaje: str) -> None:
        messagebox.showinfo("Auditoría", mensaje)
