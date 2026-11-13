import unittest
import tkinter as tk

import customtkinter as ctk

from src.controllers.admin.controlador_admin import ControladorAdmin
from src.models.auditoria.auditoria_model import AuditoriaModel
from src.views.auditoria.auditoria_view import AuditoriaView


class TestAuditoriaFilters(unittest.TestCase):
    def test_normalizar_fecha_humana(self):
        self.assertEqual(AuditoriaModel._normalizar_filtro_fecha("Hoy, 24 May 2024"), "2024-05-24")
        self.assertEqual(AuditoriaModel._normalizar_filtro_fecha("2024-05-24"), "2024-05-24")
        self.assertIsNone(AuditoriaModel._normalizar_filtro_fecha(""))

    def test_fila_auditoria_ocupa_ancho_completo(self):
        root = tk.Tk()
        root.withdraw()
        try:
            parent = ctk.CTkFrame(root)
            parent.grid_columnconfigure(0, weight=1)
            view = AuditoriaView(parent)
            view.poblar_tabla([
                {
                    "fecha_hora": "2024-05-24 12:34:56",
                    "usuario": "UALI",
                    "accion": "ACTUALIZAR",
                    "tabla_afectada": "productos",
                    "detalles": "Actualizó precio del producto 1",
                }
            ])
            row = view._rows[0]
            self.assertEqual(row.grid_info()["sticky"], "ew")
            self.assertEqual(row.grid_info()["column"], 0)
            self.assertEqual(row.grid_info()["columnspan"], 6)
        finally:
            root.destroy()

    def test_mapea_categoria_accion(self):
        self.assertEqual(AuditoriaModel._normalizar_accion_filtro("Actualización"), "ACTUALIZAR")
        self.assertEqual(AuditoriaModel._normalizar_accion_filtro("Creación"), "INSERTAR")
        self.assertIsNone(AuditoriaModel._normalizar_accion_filtro("Cualquier acción"))

    def test_detalle_cambio_precio_producto(self):
        detalle = ControladorAdmin._detalle_cambio_producto(
            {"name": "Ceviche", "price": 25.0, "category_id": 1, "description": "Original"},
            ("Ceviche", "Especial", 32.5, 1),
        )
        self.assertIn("Ceviche", detalle)
        self.assertIn("25.0", detalle)
        self.assertIn("32.5", detalle)
        self.assertIn("precio", detalle.lower())


if __name__ == "__main__":
    unittest.main()
