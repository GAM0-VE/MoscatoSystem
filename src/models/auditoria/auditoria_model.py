from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Any

try:
    import mysql.connector
    from mysql.connector import Error
except Exception:  # pragma: no cover - fallback para entornos sin mysql-connector
    mysql = None
    Error = Exception


class AuditoriaModel:
    """Modelo para registrar y consultar eventos del sistema."""

    def __init__(self, db_config: dict[str, Any] | None = None) -> None:
        self._db_config = db_config or {
            "host": os.getenv("DB_HOST", "127.0.0.1"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_NAME", "moscato_db"),
            "autocommit": False,
        }
        self.ultimo_error: str | None = None

    def _connect(self):
        if mysql is None:
            raise ConnectionError("mysql-connector-python no está instalado o no está disponible.")
        try:
            return mysql.connector.connect(**self._db_config)
        except Error as exc:
            raise ConnectionError(f"No fue posible conectar con MySQL: {exc}") from exc

    def registrar_accion(
        self,
        id_usuario: int,
        accion: str,
        tabla_afectada: str,
        detalles: str,
    ) -> bool:
        """Inserta un registro de auditoría."""
        self.ultimo_error = None

        if id_usuario is None or int(id_usuario) <= 0:
            self.ultimo_error = "Debe indicar un usuario válido."
            return False

        accion = (accion or "").strip()
        tabla_afectada = (tabla_afectada or "").strip()
        detalles = detalles or ""

        if not accion:
            self.ultimo_error = "La acción no puede estar vacía."
            return False
        if not tabla_afectada:
            self.ultimo_error = "La tabla afectada no puede estar vacía."
            return False

        sql = """
            INSERT INTO auditoria (id_usuario, accion, tabla_afectada, detalles)
            VALUES (%s, %s, %s, %s)
        """

        try:
            connection = self._connect()
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql, (id_usuario, accion.upper(), tabla_afectada, detalles))
                connection.commit()
                return True
            except Error as exc:
                connection.rollback()
                raise exc
            finally:
                connection.close()
        except (ConnectionError, Error, ValueError) as exc:
            self.ultimo_error = str(exc)
            return False

    def obtener_usuarios(self) -> list[dict[str, Any]]:
        """Devuelve los usuarios registrados para completar filtros de auditoría."""
        self.ultimo_error = None

        sql = """
            SELECT
                u.id_usuario,
                CONCAT(COALESCE(e.nombres, ''), ' ', COALESCE(e.apellidos, '')) AS nombre_usuario,
                u.username
            FROM usuarios AS u
            LEFT JOIN empleados AS e ON e.id_empleado = u.id_empleado
            ORDER BY nombre_usuario ASC, u.id_usuario ASC
        """

        try:
            connection = self._connect()
            try:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(sql)
                    registros = cursor.fetchall() or []
                    return [self._normalizar_usuario(registro) for registro in registros]
            finally:
                connection.close()
        except (ConnectionError, Error, ValueError) as exc:
            self.ultimo_error = str(exc)
            return []

    @staticmethod
    def _normalizar_usuario(registro: dict[str, Any]) -> dict[str, Any]:
        nombre = (registro.get("nombre_usuario") or "").strip()
        if not nombre:
            nombre = str(registro.get("username") or f"Usuario {registro.get('id_usuario') or '-'}").strip()

        return {
            "id": int(registro.get("id_usuario") or 0),
            "nombre": nombre,
        }

    @staticmethod
    def _normalizar_filtro_fecha(valor: str | None) -> str | None:
        if valor is None:
            return None

        texto = str(valor).strip()
        if not texto:
            return None

        texto_limpio = texto.lower()
        if texto_limpio in {"todos", "todas", "todo", "cualquier", "cualquier fecha", "all"}:
            return None

        try:
            return datetime.strptime(texto, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            pass

        for pattern in ("%d/%m/%Y", "%d-%m-%Y", "%d %b %Y", "%d %B %Y"):
            try:
                return datetime.strptime(texto, pattern).strftime("%Y-%m-%d")
            except ValueError:
                continue

        if "," in texto:
            for parte in texto.split(","):
                parte = parte.strip()
                if not parte:
                    continue
                for pattern in ("%d %b %Y", "%d %B %Y"):
                    try:
                        return datetime.strptime(parte, pattern).strftime("%Y-%m-%d")
                    except ValueError:
                        continue

        today = datetime.today()
        if texto_limpio.startswith("hoy"):
            return today.strftime("%Y-%m-%d")
        if texto_limpio.startswith("ayer"):
            return (today - timedelta(days=1)).strftime("%Y-%m-%d")
        if texto_limpio.startswith("esta semana"):
            return (today - timedelta(days=7)).strftime("%Y-%m-%d")
        if texto_limpio.startswith("ultimos 7 dias") or texto_limpio.startswith("ultimos 7 días"):
            return (today - timedelta(days=7)).strftime("%Y-%m-%d")
        if texto_limpio.startswith("este mes"):
            return today.replace(day=1).strftime("%Y-%m-%d")

        return None

    @staticmethod
    def _normalizar_accion_filtro(valor: str | None) -> str | None:
        if valor is None:
            return None

        texto = str(valor).strip()
        if not texto or texto.lower() in {"cualquier acción", "todos", "todas", "todo", "all"}:
            return None

        mapa = {
            "inicio de sesión": "LOGIN",
            "login": "LOGIN",
            "creación": "INSERTAR",
            "creacion": "INSERTAR",
            "insertar": "INSERTAR",
            "eliminación": "ELIMINAR",
            "eliminacion": "ELIMINAR",
            "actualización": "ACTUALIZAR",
            "actualizacion": "ACTUALIZAR",
            "descuento": "DESCUENTO",
            "precio": "ACTUALIZAR",
        }

        clave = texto.lower()
        return mapa.get(clave, texto.upper())

    def obtener_auditoria(
        self,
        fecha_inicio: str | None = None,
        fecha_fin: str | None = None,
        id_usuario: int | None = None,
        accion: str | None = None,
    ) -> list[dict[str, Any]]:
        """Obtiene el historial de auditoría con filtros opcionales."""
        self.ultimo_error = None

        fecha_inicio = self._normalizar_filtro_fecha(fecha_inicio)
        fecha_fin = self._normalizar_filtro_fecha(fecha_fin)
        accion = self._normalizar_accion_filtro(accion)

        sql = """
            SELECT
                a.id_registro,
                a.id_usuario,
                a.accion,
                a.tabla_afectada,
                a.fecha_hora,
                a.detalles,
                CONCAT(COALESCE(e.nombres, ''), ' ', COALESCE(e.apellidos, '')) AS nombre_usuario
            FROM auditoria AS a
            LEFT JOIN usuarios AS u ON u.id_usuario = a.id_usuario
            LEFT JOIN empleados AS e ON e.id_empleado = u.id_empleado
            WHERE 1 = 1
        """
        params: list[Any] = []

        if fecha_inicio:
            sql += " AND a.fecha_hora >= %s "
            params.append(fecha_inicio)
        if fecha_fin:
            sql += " AND a.fecha_hora <= %s "
            params.append(f"{fecha_fin} 23:59:59")
        if id_usuario not in (None, ""):
            sql += " AND a.id_usuario = %s "
            params.append(int(id_usuario))
        if accion:
            sql += " AND a.accion = %s "
            params.append(accion)

        sql += " ORDER BY a.fecha_hora DESC, a.id_registro DESC "

        try:
            connection = self._connect()
            try:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(sql, tuple(params))
                    registros = cursor.fetchall() or []
                    return [self._normalizar_registro(registro) for registro in registros]
            finally:
                connection.close()
        except (ConnectionError, Error, ValueError) as exc:
            self.ultimo_error = str(exc)
            return []

    @staticmethod
    def _normalizar_registro(registro: dict[str, Any]) -> dict[str, Any]:
        nombre = (registro.get("nombre_usuario") or "").strip()
        if not nombre:
            nombre = f"Usuario {registro.get('id_usuario') or '-'}"

        return {
            "id_registro": int(registro.get("id_registro") or 0),
            "id_usuario": int(registro.get("id_usuario") or 0),
            "usuario": nombre,
            "accion": str(registro.get("accion") or "-"),
            "tabla_afectada": str(registro.get("tabla_afectada") or "-"),
            "fecha_hora": registro.get("fecha_hora"),
            "detalles": str(registro.get("detalles") or "-"),
        }
