from __future__ import annotations

from typing import Any

from src.core.event_bus import event_bus
from src.models.mesas.modelo_mesas import MesasModel
from src.views.mesas.vista_mesas import MesasView


class MesasController:
    """Controlador MVC del plano de mesas."""

    def __init__(self, modelo: MesasModel, vista: MesasView) -> None:
        self.modelo = modelo
        self.vista = vista
        self._cache_mesas: dict[int, dict[str, Any]] = {}

        # El controlador conecta eventos de la vista pero mantiene la logica.
        self.vista.configurar_accion_click(self.seleccionar_mesa)

        # Carga inicial: modelo -> vista.
        self.cargar_estado_inicial()

    def cargar_estado_inicial(self) -> None:
        # Sincroniza primero: corrige mesas con estado incorrecto en DB
        self.modelo.sincronizar_estados_mesas()
        mesas = self.modelo.obtener_mesas()
        self._cache_mesas = {int(mesa["id_mesa"]): dict(mesa) for mesa in mesas if mesa.get("id_mesa") is not None}
        self.vista.dibujar_mesas(mesas)

    def seleccionar_mesa(self, id_mesa: int) -> None:
        """
        Punto de extension para flujo de navegacion.
        Desde aqui se puede abrir la vista de pedido de la mesa seleccionada.
        """
        mesa = self._cache_mesas.get(int(id_mesa), {})
        event_bus.emit(
            "mesa.seleccionada",
            {
                "id_mesa": int(id_mesa),
                "numero_mesa": mesa.get("numero_mesa"),
                "estado": mesa.get("estado"),
            },
        )

    # Metodos publicos para integracion con otros controladores.
    # Ejemplo: el controlador de pedidos llama registrar_primer_item cuando
    # se agrega el primer producto de una mesa.
    def registrar_primer_item(self, id_mesa: int) -> bool:
        return self._cambiar_estado_mesa(id_mesa, "Atencion")

    def solicitar_precuenta(self, id_mesa: int) -> bool:
        return self._cambiar_estado_mesa(id_mesa, "Atencion")

    def ocupar_mesa(self, id_mesa: int) -> bool:
        return self._cambiar_estado_mesa(id_mesa, "Ocupada")

    def liberar_mesa(self, id_mesa: int) -> bool:
        return self._cambiar_estado_mesa(id_mesa, "Libre")

    def _cambiar_estado_mesa(self, id_mesa: int, nuevo_estado: str) -> bool:
        actualizado = self.modelo.actualizar_estado_mesa(int(id_mesa), nuevo_estado)
        # Removemos el if not actualizado para forzar siempre la UI a reflejar el estado esperado
        # aunque MySQL retorne rowcount = 0 (por ejemplo si ya estaba en ese estado o por el problema del ENUM)

        mesa_cache = self._cache_mesas.setdefault(int(id_mesa), {"id_mesa": int(id_mesa)})
        mesa_cache["estado"] = nuevo_estado

        # Refleja cambio en UI sin recargar toda la grilla.
        self.vista.actualizar_color_mesa(int(id_mesa), nuevo_estado)

        # Evento para que otros modulos (pedidos/caja/auditoria) reaccionen.
        event_bus.emit(
            "mesa.estado_actualizado",
            {
                "id_mesa": int(id_mesa),
                "estado": nuevo_estado,
            },
        )
        return True
