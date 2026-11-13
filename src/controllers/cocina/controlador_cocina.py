from __future__ import annotations

from datetime import datetime
import unicodedata
from typing import Any

from src.core.event_bus import event_bus
from src.models.cocina.modelo_cocina import ModeloCocina
from src.views.cocina.vista_cocina import CocinaDesignWindow


class ControladorCocina:
    """Controlador MVC del monitor de cocina."""

    REFRESH_MS = 3000
    _pedidos_ocultos_global: set[int] = set()

    def __init__(self, vista: CocinaDesignWindow, modelo: ModeloCocina | None = None) -> None:
        self.vista = vista
        self.modelo = modelo or ModeloCocina()
        self._refresh_after_id: str | None = None
        self._pedidos_ocultos = set()
        self._pedidos_ocultos = self._pedidos_ocultos_global
        self._evento_pedido_creado = self._on_pedido_creado
        self._evento_pedido_cancelado = self._on_pedido_cancelado
        self._evento_pedido_actualizado = self._on_pedido_actualizado
        
        event_bus.subscribe("pedido.creado", self._evento_pedido_creado)
        event_bus.subscribe("pedido.cancelado", self._evento_pedido_cancelado)
        event_bus.subscribe("pedido.actualizado", self._evento_pedido_actualizado)

    def actualizar_pantalla(self) -> None:
        """Consulta pedidos reales en segundo plano y actualiza la vista."""
        if not getattr(self.vista, "winfo_exists", lambda: False)():
            return
            
        def _fetch_and_update():
            try:
                pedidos_reales = self.modelo.obtener_pedidos_activos()
                pedidos_reales = [p for p in pedidos_reales if p.get("id_pedido") not in self._pedidos_ocultos]
                pedidos_activos, tiempo_promedio, en_prep, pendientes = self._calcular_estadisticas(pedidos_reales)
                datos_mapeados = self._agrupar_items_a_tarjetas(pedidos_reales)
                
                if getattr(self.vista, "winfo_exists", lambda: False)():
                    self.vista.after(0, lambda: self._apply_update(
                        datos_mapeados, pedidos_activos, tiempo_promedio, en_prep, pendientes
                    ))
            except Exception:
                pass
            finally:
                if getattr(self.vista, "winfo_exists", lambda: False)():
                    self.vista.after(0, self._programar_refresco)

        import threading
        threading.Thread(target=_fetch_and_update, daemon=True).start()

    def _apply_update(self, datos_mapeados, pedidos_activos, tiempo_promedio, en_prep, pendientes) -> None:
        if not getattr(self.vista, "winfo_exists", lambda: False)():
            return
        self.vista.actualizar_monitor(datos_mapeados, self.al_hacer_clic_en_listo)
        self.vista.actualizar_estadisticas(
            pedidos_activos=pedidos_activos,
            tiempo_promedio=tiempo_promedio,
            en_prep=en_prep,
            pendientes=pendientes,
        )

    def al_hacer_clic_en_listo(self, id_pedido: int, siguiente_estado: str) -> None:
        """Avanza el estado del pedido completo y refresca la pantalla."""
        if siguiente_estado == "Ocultar":
            self.modelo.ocultar_pedido_cocina(id_pedido)
            self._pedidos_ocultos.add(id_pedido)
            self.actualizar_pantalla()
            return

        estado_item = "En preparación" if siguiente_estado == "En preparación" else "Listo"
        estado_pedido = "En cocina" if siguiente_estado == "En preparación" else "Listo"
        self.modelo.actualizar_estado_pedido(id_pedido, estado_item, estado_pedido)
        event_bus.emit(
            "pedido.listo",
            {
                "id_pedido": id_pedido,
                "estado_item": estado_item,
                "estado_pedido": estado_pedido,
            },
        )
        self.actualizar_pantalla()

    def desactivar(self) -> None:
        if self._refresh_after_id is not None and getattr(self.vista, "winfo_exists", lambda: False)():
            self.vista.after_cancel(self._refresh_after_id)
            self._refresh_after_id = None
        event_bus.unsubscribe("pedido.creado", self._evento_pedido_creado)
        event_bus.unsubscribe("pedido.cancelado", self._evento_pedido_cancelado)
        event_bus.unsubscribe("pedido.actualizado", self._evento_pedido_actualizado)

    def _on_pedido_creado(self, evento: dict[str, Any]) -> None:
        if not getattr(self.vista, "winfo_exists", lambda: False)():
            return
        ticket = int(evento.get("ticket") or 0)
        id_pedido = int(evento.get("id_pedido") or 0)

        def _notificar_y_refrescar() -> None:
            self.vista.notificar_nueva_comanda(ticket=ticket, id_pedido=id_pedido)
            self.actualizar_pantalla()

        self.vista.after(0, _notificar_y_refrescar)

    def _on_pedido_cancelado(self, evento: dict[str, Any]) -> None:
        if not getattr(self.vista, "winfo_exists", lambda: False)():
            return
        ticket = int(evento.get("ticket") or 0)
        
        def _notificar_y_refrescar() -> None:
            if hasattr(self.vista, "notificar_cancelacion"):
                self.vista.notificar_cancelacion(ticket=ticket)
            self.actualizar_pantalla()
            
        self.vista.after(0, _notificar_y_refrescar)

    def _on_pedido_actualizado(self, evento: dict[str, Any]) -> None:
        if not getattr(self.vista, "winfo_exists", lambda: False)():
            return
        self.vista.after(0, self.actualizar_pantalla)

    def _agrupar_items_a_tarjetas(self, filas: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Agrupa filas por id_pedido (si existe) o por numero_mesa para renderizar una tarjeta por pedido."""
        grupos: dict[str, dict[str, Any]] = {}

        for fila in filas:
            numero_mesa = str(fila.get("numero_mesa") or "Para llevar")
            id_pedido = fila.get("id_pedido")
            llave = f"pedido:{id_pedido}" if id_pedido not in (None, "") else f"mesa:{numero_mesa.strip().lower()}"

            # Obtener timestamp de envío
            fecha_val = fila.get("fecha_envio_cocina")
            ts = 0.0
            if isinstance(fecha_val, datetime):
                ts = fecha_val.timestamp()
                
            if llave not in grupos:
                grupos[llave] = {
                    "id_pedido": int(fila.get("id_pedido") or 0),
                    "mesa": self._normalizar_mesa(numero_mesa),
                    "tiempo": self._formatear_hora(fecha_val),
                    "timestamp_envio": ts,
                    "estado": "ENVIADO A COCINA",
                    "header_bg": "#6A0E0E",
                    "estado_bg": "#8E1D1D",
                    "borde": "#A12A2A",
                    "accion_texto": "EN PREPARACION",
                    "accion_bg": "#49A54A",
                    "accion_hover": "#5EB95E",
                    "siguiente_estado": "En preparación",
                    "accion_habilitada": True,
                    "items": [],
                    "_estados": set(),
                }
            elif ts and (not grupos[llave].get("timestamp_envio") or ts < grupos[llave]["timestamp_envio"]):
                grupos[llave]["timestamp_envio"] = ts
                grupos[llave]["tiempo"] = self._formatear_hora(fecha_val)

            cantidad = int(fila.get("cantidad") or 1)
            nombre = str(fila.get("nombre") or "ITEM").upper()
            detalle = str(fila.get("descripcion_preparacion") or "").strip()
            grupos[llave]["items"].append(
                {
                    "cantidad": cantidad,
                    "nombre": nombre,
                    "detalle": detalle,
                }
            )

            estado_item = self._normalizar_estado(str(fila.get("estado_item") or ""))
            grupos[llave]["_estados"].add(estado_item)

        for grupo in grupos.values():
            estados = grupo.pop("_estados", set())
            if "cancelado" in estados:
                grupo["estado"] = "CANCELADO"
                grupo["header_bg"] = "#333333"
                grupo["estado_bg"] = "#1A1A1A"
                grupo["borde"] = "#555555"
                grupo["accion_texto"] = "OCULTAR TICKET"
                grupo["accion_bg"] = "#555555"
                grupo["accion_hover"] = "#777777"
                grupo["siguiente_estado"] = "Ocultar"
                grupo["accion_habilitada"] = True
            elif "listo" in estados:
                grupo["estado"] = "LISTO"
                grupo["header_bg"] = "#1F5D35"
                grupo["estado_bg"] = "#2E8F48"
                grupo["borde"] = "#49A54A"
                grupo["accion_texto"] = "PEDIDO LISTO"
                grupo["accion_bg"] = "#2E8F48"
                grupo["accion_hover"] = "#3EA35A"
                grupo["siguiente_estado"] = "Listo"
                grupo["accion_habilitada"] = False
            elif "en preparacion" in estados:
                grupo["estado"] = "EN PREPARACION"
                grupo["header_bg"] = "#5B430E"
                grupo["estado_bg"] = "#C49315"
                grupo["borde"] = "#D3A437"
                grupo["accion_texto"] = "PEDIDO LISTO"
                grupo["accion_bg"] = "#C49315"
                grupo["accion_hover"] = "#D9AB33"
                grupo["siguiente_estado"] = "Listo"
                grupo["accion_habilitada"] = True
            else:
                grupo["estado"] = "ENVIADO A COCINA"
                grupo["header_bg"] = "#6A0E0E"
                grupo["estado_bg"] = "#8E1D1D"
                grupo["borde"] = "#A12A2A"
                grupo["accion_texto"] = "EN PREPARACION"
                grupo["accion_bg"] = "#49A54A"
                grupo["accion_hover"] = "#5EB95E"
                grupo["siguiente_estado"] = "En preparación"
                grupo["accion_habilitada"] = True

        return list(grupos.values())

    def _programar_refresco(self) -> None:
        if not getattr(self.vista, "winfo_exists", lambda: False)():
            return
        if self._refresh_after_id is not None:
            self.vista.after_cancel(self._refresh_after_id)
        self._refresh_after_id = self.vista.after(self.REFRESH_MS, self._refrescar_desde_timer)

    def _refrescar_desde_timer(self) -> None:
        self._refresh_after_id = None
        if not getattr(self.vista, "winfo_exists", lambda: False)():
            return
        self.actualizar_pantalla()

    @staticmethod
    def _normalizar_mesa(numero_mesa: str) -> str:
        texto = str(numero_mesa or "").strip()
        if texto.lower() == "para llevar":
            return "#PARA LLEVAR"
        if texto.upper().startswith("T-"):
            return texto.upper()
        if texto.isdigit():
            return f"T-{int(texto):02d}"
        return f"T-{texto.upper()}"

    @staticmethod
    def _formatear_hora(valor: Any) -> str:
        if isinstance(valor, datetime):
            return valor.strftime("%H:%M")
        texto = str(valor or "")
        if len(texto) >= 16 and "-" in texto:
            return texto[11:16]
        return texto[:5] if texto else "--:--"

    def _calcular_estadisticas(self, filas: list[dict[str, Any]]) -> tuple[int, str, int, int]:
        pedidos_unicos: set[str] = set()
        pendientes = 0
        en_prep = 0
        tiempos_segundos: list[float] = []
        ahora = datetime.now()

        for fila in filas:
            id_pedido = fila.get("id_pedido")
            numero_mesa = str(fila.get("numero_mesa") or "").strip().lower()
            id_detalle = fila.get("id_detalle")

            if id_pedido not in (None, ""):
                pedidos_unicos.add(f"pedido:{id_pedido}")
            elif numero_mesa:
                pedidos_unicos.add(f"mesa:{numero_mesa}")
            elif id_detalle not in (None, ""):
                pedidos_unicos.add(f"detalle:{id_detalle}")

            estado_raw = fila.get("estado_item") or fila.get("estado") or ""
            estado = self._normalizar_estado(str(estado_raw))
            if estado == "pendiente":
                pendientes += 1
            if estado in {"en cocina", "en preparacion"}:
                en_prep += 1

            fecha_envio = self._parse_datetime(fila.get("fecha_envio_cocina"))
            if fecha_envio is not None:
                delta = (ahora - fecha_envio).total_seconds()
                if delta >= 0:
                    tiempos_segundos.append(delta)

        promedio = sum(tiempos_segundos) / len(tiempos_segundos) if tiempos_segundos else 0.0
        promedio_entero = int(round(promedio))
        minutos = promedio_entero // 60
        segundos = promedio_entero % 60
        tiempo_promedio = f"{minutos:02d}:{segundos:02d}"

        return len(pedidos_unicos), tiempo_promedio, en_prep, pendientes

    @staticmethod
    def _normalizar_estado(estado: str) -> str:
        texto = estado.strip().lower()
        texto = unicodedata.normalize("NFKD", texto)
        texto = "".join(ch for ch in texto if not unicodedata.combining(ch))
        return " ".join(texto.split())

    @staticmethod
    def _parse_datetime(valor: Any) -> datetime | None:
        if isinstance(valor, datetime):
            return valor

        texto = str(valor or "").strip()
        if not texto:
            return None

        formatos = (
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
        )
        for formato in formatos:
            try:
                return datetime.strptime(texto, formato)
            except ValueError:
                continue
        return None
