from __future__ import annotations

from src.models.auditoria.auditoria_model import AuditoriaModel
from src.views.auditoria.auditoria_view import AuditoriaView


class AuditoriaController:
    """Controlador para la sección de auditoría del sistema."""

    def __init__(self, modelo: AuditoriaModel, vista: AuditoriaView) -> None:
        self.modelo = modelo
        self.vista = vista
        self.vista.configurar_busqueda(self.buscar)
        if hasattr(self.vista, "after"):
            self.vista.after(150, self._carga_inicial_async)
        else:
            self._carga_inicial_async()

    def _carga_inicial_async(self):
        self.cargar_usuarios()
        self.buscar()

    def cargar_usuarios(self) -> None:
        """Carga los usuarios registrados para el filtro del dropdown."""
        try:
            usuarios = self.modelo.obtener_usuarios()
            self.vista.set_usuarios(usuarios)
        except Exception as exc:  # pragma: no cover - control de errores general
            self.vista.mostrar_error(f"No se pudieron cargar los usuarios: {exc}")

    def buscar(self) -> None:
        """Lee filtros, consulta el modelo y actualiza la tabla."""
        try:
            filtros = self.vista.obtener_filtros()
            fecha_inicio = filtros.get("fecha_inicio")
            fecha_fin = filtros.get("fecha_fin")
            id_usuario = filtros.get("id_usuario")
            accion = filtros.get("accion")

            if id_usuario:
                try:
                    id_usuario = int(id_usuario)
                except ValueError:
                    self.vista.mostrar_error("El usuario debe ser un número entero válido.")
                    return

            registros = self.modelo.obtener_auditoria(
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                id_usuario=id_usuario,
                accion=accion,
            )

            if self.modelo.ultimo_error:
                self.vista.mostrar_error(self.modelo.ultimo_error)
                self.vista.limpiar_tabla()
                return

            self.vista.poblar_tabla(registros)

        except Exception as exc:  # pragma: no cover - control de errores general
            self.vista.limpiar_tabla()
            self.vista.mostrar_error(f"Ocurrió un error al buscar auditoría: {exc}")
