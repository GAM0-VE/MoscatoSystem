import threading
import time
from typing import Any
from src.core.event_bus import event_bus
from src.models.pedidos.modelo_mesero import ModeloMesero

class ControladorMesero:
    def __init__(self, modelo: ModeloMesero):
        self.modelo = modelo
        self._polling = False
        self._thread = None
        self._last_orders = {}
        
    def cargar_catalogo(self) -> dict:
        return self.modelo.obtener_categorias_y_productos()
        
    def guardar_orden(self, orden: dict, usuario: str) -> int | None:
        return self.modelo.guardar_orden(orden, usuario)
        
    def start_polling(self, interval_sec: int = 5):
        if self._polling:
            return
        self._polling = True
        self._thread = threading.Thread(target=self._poll_loop, args=(interval_sec,), daemon=True)
        self._thread.start()
        
    def stop_polling(self):
        self._polling = False
        if self._thread:
            self._thread.join(timeout=1.0)
            
    def _poll_loop(self, interval_sec: int):
        while self._polling:
            try:
                ordenes = self.modelo.obtener_ordenes_pendientes()
                cambios = False
                
                # Check for state changes to emit events
                current_orders = {}
                for orden in ordenes:
                    id_pedido = int(orden.get("id_pedido") or 0)
                    item_st = str(orden.get("estado_item") or "").strip()
                    ped_st = str(orden.get("estado_pedido") or "").strip()
                    if "prepara" in item_st.lower():
                        estado = "En preparación"
                    elif "listo" in item_st.lower() or "listo" in ped_st.lower():
                        estado = "Listo"
                    elif "cancel" in item_st.lower() or "cancel" in ped_st.lower():
                        estado = "Cancelado"
                    else:
                        estado = item_st or ped_st or "En cocina"
                    
                    if id_pedido not in current_orders or estado in ("En preparación", "Listo", "Cancelado"):
                        current_orders[id_pedido] = estado
                    
                    last_estado = self._last_orders.get(id_pedido)
                    if last_estado is not None and last_estado != estado:
                        # Emite evento de que un pedido cambió de estado
                        event_bus.emit("pedido.listo", {"id_pedido": id_pedido, "estado_item": estado, "estado_pedido": estado})
                        cambios = True
                        
                if set(current_orders.keys()) != set(self._last_orders.keys()):
                    cambios = True

                # Update last orders state
                self._last_orders = current_orders
                
                if cambios or not hasattr(self, '_first_poll_done'):
                    setattr(self, '_first_poll_done', True)
                    
                    # Group items by ticket for UI format
                    grouped = {}
                    for row in ordenes:
                        t = row.get("id_pedido")
                        if not t: continue
                        if t not in grouped:
                            grouped[t] = {
                                "ticket": row.get("ticket_numero") or t,
                                "mesa": row.get("mesa", "Mesa X"),
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

                    # Resolver estado real del pedido (priorizar En preparación / Listo según sus items)
                    for t, orden_dict in grouped.items():
                        items_estados = [str(it.get("estado_item") or "").lower() for it in orden_dict["items"]]
                        estado_base = str(orden_dict.get("estado") or "")
                        if estado_base == "Cancelado" or (items_estados and all("cancel" in e for e in items_estados)):
                            orden_dict["estado"] = "Cancelado"
                        elif estado_base == "Servido":
                            orden_dict["estado"] = "Servido"
                        elif estado_base == "Listo" or any("listo" in e for e in items_estados):
                            orden_dict["estado"] = "Listo"
                        elif any("prepara" in e for e in items_estados):
                            orden_dict["estado"] = "En preparación"
                        elif estado_base:
                            orden_dict["estado"] = estado_base
                        else:
                            orden_dict["estado"] = "En cocina"
                    
                    ordenes_agrupadas = list(grouped.values())
                    event_bus.emit("pedidos.pendientes_actualizados", {"ordenes": ordenes_agrupadas})
                    
            except Exception as e:
                import logging
                logging.error(f"Error in ControladorMesero polling: {e}", exc_info=True)
                
            time.sleep(interval_sec)

    def eliminar_item_pendiente(self, id_detalle: int) -> bool:
        return self.modelo.eliminar_item_pendiente(id_detalle)

    def cancelar_pedido_pendiente(self, id_pedido: int) -> bool:
        exito = self.modelo.cancelar_pedido_pendiente(id_pedido)
        if exito:
            event_bus.emit("pedido.cancelado", {"id_pedido": id_pedido})
        return exito

    def consultar_ticket_por_id(self, id_pedido: int) -> int | None:
        return self.modelo.consultar_ticket_por_id(id_pedido)

    def cambiar_a_para_llevar(self, id_pedido: int) -> bool:
        """Cambia el pedido a Para llevar en DB y emite evento para sincronizar vistas."""
        exito = self.modelo.cambiar_a_para_llevar(id_pedido)
        if exito:
            event_bus.emit("pedido.actualizado", {"id_pedido": id_pedido, "tipo_pedido": "Para llevar"})
        return exito

    def cambiar_tipo_pedido_pendiente(self, id_pedido: int, nuevo_tipo: str) -> bool:
        if nuevo_tipo == "Para llevar":
            return self.cambiar_a_para_llevar(id_pedido)
        exito = self.modelo.cambiar_tipo_pedido(id_pedido, nuevo_tipo)
        if exito:
            event_bus.emit("pedido.actualizado", {"id_pedido": id_pedido, "tipo_pedido": nuevo_tipo})
        return exito
