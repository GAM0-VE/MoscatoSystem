from __future__ import annotations

from collections.abc import Callable
from tkinter import messagebox

from src.models.pedidos.modelo_pedido_actual import ModeloPedidoActual
from src.views.pedidos.vista_pedido_actual import VistaPedidoActual


class ControladorPedidoActual:
    """Controlador del panel Pedido Actual."""

    def __init__(
        self,
        modelo: ModeloPedidoActual,
        vista: VistaPedidoActual,
        on_send_to_kitchen: Callable[[list[dict[str, object]]], bool] | None = None,
        on_request_precuenta: Callable[[], None] | None = None,
        on_close_table_paid: Callable[[], None] | None = None,
        on_exit: Callable[[], None] | None = None,
    ) -> None:
        self.modelo = modelo
        self.vista = vista
        self._on_send_to_kitchen = on_send_to_kitchen
        self._on_request_precuenta = on_request_precuenta
        self._on_close_table_paid = on_close_table_paid
        self._on_exit = on_exit

        self.vista.configurar_acciones(
            on_sumar=self.incrementar_item,
            on_restar=self.reducir_item,
            on_nota=self.agregar_nota,
            on_precuenta=self.precuenta,
            on_a_cocina=self.enviar_a_cocina,
            on_cerrar_y_pagar=self.cerrar_mesa_y_pagar,
            on_salir=self.salir,
            on_limpiar=self.limpiar,
        )
        self.refrescar()

    def agregar_item(self, id_item: str, nombre: str, precio: float, cantidad: int = 1, notas: str = "", **extra) -> None:
        self.modelo.agregar_item(id_item=id_item, nombre=nombre, precio=precio, cantidad=cantidad, notas=notas, **extra)
        self.refrescar()

    def incrementar_item(self, id_item: str) -> None:
        item = self._buscar_item(id_item)
        if item is None:
            return
        self.modelo.agregar_item(
            id_item=str(item["id_item"]),
            nombre=str(item["nombre"]),
            precio=float(item["precio"]),
            cantidad=1,
            notas=str(item.get("notas", "")),
            **{k: v for k, v in item.items() if k not in {"id_item", "nombre", "precio", "cantidad", "notas", "enviado_a_cocina"}},
        )
        self.refrescar()

    def reducir_item(self, id_item: str) -> None:
        self.modelo.reducir_cantidad(id_item)
        self.refrescar()

    def eliminar_item(self, id_item: str) -> None:
        self.modelo.eliminar_item(id_item)
        self.refrescar()

    def agregar_nota(self, id_item: str) -> None:
        nota = self.vista.pedir_nota()
        if nota is None:
            return
        self.modelo.agregar_nota(id_item, nota)
        self.refrescar()

    def precuenta(self) -> None:
        if self._on_request_precuenta is not None:
            self._on_request_precuenta()

    def enviar_a_cocina(self) -> None:
        if not self.modelo.tiene_items():
            messagebox.showwarning("Pedido vacío", "No hay productos en el pedido actual.")
            return
        if self._on_send_to_kitchen is not None:
            enviado = self._on_send_to_kitchen(self.modelo.obtener_items())
            if enviado:
                self.modelo.marcar_enviado()
                self.modelo.limpiar()
                self.refrescar()

    def cerrar_mesa_y_pagar(self) -> None:
        if self._on_close_table_paid is not None:
            self._on_close_table_paid()
        messagebox.showinfo("Cerrar mesa", "La acción de cierre y pago queda conectada al flujo de negocio.")

    def salir(self) -> None:
        if self.modelo.tiene_items_sin_enviar():
            confirmar = messagebox.askyesno(
                "Salir",
                "Hay productos sin enviar a cocina. ¿Deseas descartar los cambios?",
            )
            if not confirmar:
                return
        self.modelo.limpiar()
        self.refrescar()
        if self._on_exit is not None:
            self._on_exit()

    
    def establecer_id_pedido_en_edicion(self, id_pedido: int | None) -> None:
        self._id_pedido_en_edicion = id_pedido

    def obtener_id_pedido_en_edicion(self) -> int | None:
        return getattr(self, "_id_pedido_en_edicion", None)

    def refrescar(self) -> None:
        items = self.modelo.obtener_items()
        self.vista.redibujar(items)
        self.vista.actualizar_totales(self.modelo.calcular_totales())
        from src.core.event_bus import event_bus
        event_bus.emit("pedido_actual.items_cambiados", {"tiene_items": len(items) > 0})

    def establecer_ticket(self, numero_ticket: int) -> None:
        self.vista.actualizar_ticket(numero_ticket)

    def establecer_mesa(self, mesa_texto: str) -> None:
        self.vista.actualizar_mesa(mesa_texto)

    def limpiar(self) -> None:
        self.modelo.limpiar()
        self._id_pedido_en_edicion = None
        self.refrescar()

    def _buscar_item(self, id_item: str) -> dict[str, object] | None:
        for item in self.modelo.obtener_items():
            if str(item.get("id_item")) == str(id_item):
                return item
        return None