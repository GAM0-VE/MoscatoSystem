from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ItemPedidoActual:
    id_item: str
    nombre: str
    precio: float
    cantidad: int = 1
    notas: str = ""
    enviado_a_cocina: bool = False
    extra: dict[str, Any] = field(default_factory=dict)

    def subtotal(self) -> float:
        return round(self.precio * self.cantidad, 2)


class ModeloPedidoActual:
    """Modelo del panel Pedido Actual: solo datos y reglas de negocio."""

    def __init__(self, impuesto_porcentaje: float = 0.16) -> None:
        self.impuesto_porcentaje = impuesto_porcentaje
        self._items: list[ItemPedidoActual] = []

    def obtener_items(self) -> list[dict[str, Any]]:
        return [
            {
                "id_item": item.id_item,
                "nombre": item.nombre,
                "precio": round(item.precio, 2),
                "cantidad": item.cantidad,
                "notas": item.notas,
                "enviado_a_cocina": item.enviado_a_cocina,
                **item.extra,
            }
            for item in self._items
        ]

    def agregar_item(
        self,
        id_item: str,
        nombre: str,
        precio: float,
        cantidad: int = 1,
        notas: str = "",
        **extra: Any,
    ) -> dict[str, Any]:
        item = self._buscar_item(id_item)
        if item is None:
            item = ItemPedidoActual(
                id_item=str(id_item),
                nombre=str(nombre),
                precio=float(precio),
                cantidad=max(1, int(cantidad)),
                notas=str(notas).strip(),
                extra=dict(extra),
            )
            self._items.append(item)
            return self._item_a_dict(item)

        item.nombre = str(nombre)
        item.precio = float(precio)
        item.cantidad += max(1, int(cantidad))
        if notas:
            item.notas = str(notas).strip()
        if extra:
            item.extra.update(extra)
        return self._item_a_dict(item)

    def reducir_cantidad(self, id_item: str) -> bool:
        item = self._buscar_item(id_item)
        if item is None:
            return False
        if item.cantidad > 1:
            item.cantidad -= 1
            return True
        return self.eliminar_item(id_item)

    def eliminar_item(self, id_item: str) -> bool:
        item = self._buscar_item(id_item)
        if item is None:
            return False
        self._items.remove(item)
        return True

    def agregar_nota(self, id_item: str, notas: str) -> bool:
        item = self._buscar_item(id_item)
        if item is None:
            return False
        item.notas = str(notas).strip()
        return True

    def marcar_enviado(self) -> None:
        for item in self._items:
            item.enviado_a_cocina = True

    def limpiar(self) -> None:
        self._items.clear()

    def tiene_items(self) -> bool:
        return bool(self._items)

    def tiene_items_sin_enviar(self) -> bool:
        return any(not item.enviado_a_cocina for item in self._items)

    def calcular_totales(self) -> dict[str, float]:
        subtotal = round(sum(item.subtotal() for item in self._items), 2)
        impuesto = round(subtotal * self.impuesto_porcentaje, 2)
        total = round(subtotal + impuesto, 2)
        return {"subtotal": subtotal, "impuesto": impuesto, "total": total}

    def _buscar_item(self, id_item: str) -> ItemPedidoActual | None:
        id_busqueda = str(id_item)
        for item in self._items:
            if item.id_item == id_busqueda:
                return item
        return None

    @staticmethod
    def _item_a_dict(item: ItemPedidoActual) -> dict[str, Any]:
        return {
            "id_item": item.id_item,
            "nombre": item.nombre,
            "precio": round(item.precio, 2),
            "cantidad": item.cantidad,
            "notas": item.notas,
            "enviado_a_cocina": item.enviado_a_cocina,
            **item.extra,
        }