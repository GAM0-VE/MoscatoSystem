import unittest
from unittest.mock import MagicMock
from src.models.pedidos.modelo_pedido_actual import ModeloPedidoActual
from src.controllers.pedidos.controlador_pedido_actual import ControladorPedidoActual


class TestPedidos(unittest.TestCase):
    def setUp(self):
        self.modelo = ModeloPedidoActual()
        self.vista_mock = MagicMock()
        self.controlador = ControladorPedidoActual(
            self.modelo, 
            self.vista_mock, 
            on_send_to_kitchen=lambda x: True,
            on_request_precuenta=lambda: None,
            on_close_table_paid=lambda: None,
            on_exit=lambda: None
        )

    def test_agregar_item_calcula_subtotal(self):
        # Arrange
        id_item = "1"
        nombre = "Arroz Frito"
        precio = 15.0
        cantidad = 2
        
        # Act
        self.controlador.agregar_item(id_item, nombre, precio, cantidad, "Comida")
        
        # Assert
        items = self.modelo.obtener_items()
        self.assertEqual(len(items), 1)
        
        totales = self.modelo.calcular_totales()
        self.assertEqual(totales["subtotal"], 30.0)

    def test_actualizar_cantidad_recalcula_subtotal(self):
        # Arrange
        self.controlador.agregar_item("1", "Pollo Agridulce", 20.0, 1, "Comida")
        
        # Act
        self.modelo.agregar_item("1", "Pollo Agridulce", 20.0, 2)
        
        # Assert
        items = self.modelo.obtener_items()
        self.assertEqual(items[0]["cantidad"], 3)
        totales = self.modelo.calcular_totales()
        self.assertEqual(totales["subtotal"], 60.0)

    def test_quitar_item(self):
        # Arrange
        self.controlador.agregar_item("1", "Pollo", 20.0, 1, "Comida")
        self.controlador.agregar_item("2", "Res", 25.0, 1, "Comida")
        
        # Act
        self.modelo.eliminar_item("1")
        
        # Assert
        items = self.modelo.obtener_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["nombre"], "Res")

    def test_limpiar_pedido(self):
        # Arrange
        self.controlador.agregar_item("1", "Pollo", 20.0, 1, "Comida")
        self.controlador.agregar_item("2", "Res", 25.0, 1, "Comida")
        
        # Act
        self.controlador.limpiar()
        
        # Assert
        self.assertFalse(self.modelo.tiene_items())


if __name__ == "__main__":
    unittest.main()
