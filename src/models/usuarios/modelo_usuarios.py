from __future__ import annotations

import os
from typing import Any

try:
    import mysql.connector
    from mysql.connector import Error
except Exception:  # pragma: no cover - fallback cuando mysql-connector no esta disponible
    mysql = None
    Error = Exception


class ModeloUsuarios:
    """Modelo MVC para operaciones CRUD de usuarios en MySQL."""

    def __init__(self, db_config: dict[str, Any] | None = None) -> None:

        self._db_config = db_config or {
            "host": os.getenv("DB_HOST", "127.0.0.1"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_NAME", "moscato_db"),
            
            "autocommit": False,
        }

    def obtener_empleados(self) -> list[dict[str, Any]]:
        connection = self._connect()
        if connection is None:
            return []

        sql = """
            SELECT
                u.id_usuario,
                CONCAT(e.nombres, ' ', e.apellidos) AS nombre,
                u.username,
                u.rol,
                u.activo,
                u.fecha_actualizacion
            FROM usuarios AS u
            INNER JOIN empleados AS e ON e.id_empleado = u.id_empleado
            ORDER BY e.nombres ASC, e.apellidos ASC
        """

        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall() or []
        except Error:
            return []
        finally:
            connection.close()

        empleados = []
        for row in rows:
            empleados.append(
                {
                    "id": int(row.get("id_usuario") or 0),
                    "name": str(row.get("nombre") or "-"),
                    "username": str(row.get("username") or "-"),
                    "role": self._rol_db_a_ui(str(row.get("rol") or "Mesero")),
                    "status": "Fichado" if int(row.get("activo") or 0) == 1 else "Fuera de Turno",
                    "time": row.get("fecha_actualizacion"),
                }
            )
        return empleados

    def autenticar_usuario(self, username: str, password: str) -> dict[str, Any] | None:
        connection = self._connect()
        if connection is None:
            raise ConnectionError("No fue posible conectar a MySQL")
        
        sql = """
            SELECT
                u.id_usuario,
                CONCAT(e.nombres, ' ', e.apellidos) AS nombre,
                u.username,
                u.rol
            FROM usuarios AS u
            INNER JOIN empleados AS e ON e.id_empleado = u.id_empleado
            WHERE u.username = %s
              AND u.password = %s
              AND u.activo = 1
              AND e.activo = 1
        """
        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(sql, (username, password))
                user = cursor.fetchone()
                return user
        except Error as exc:
            raise ConnectionError(f"Error al verificar credenciales: {exc}")
        finally:
            connection.close()

    def crear_empleado(self, nombre: str, rol_ui: str, username: str | None = None, password: str | None = None) -> bool:

        connection = self._connect()
        if connection is None:
            return False

        rol_db = self._rol_ui_a_db(rol_ui)
        try:
            nombres, apellidos = self._separar_nombre(nombre)
            username = (username or self._slug_username(nombre)).strip()
            if not password:
                raise ValueError("La contraseña no puede estar vacía para un nuevo usuario.")
            documento = self._build_unique_documento(connection, username)
            with connection.cursor() as cursor:

                cursor.execute(
                    """INSERT INTO empleados (nombres, apellidos, documento_identidad, cargo, activo)
                       VALUES (%s, %s, %s, %s, 1)""",
                    (nombres, apellidos, documento, rol_db),
                )
                empleado_id = cursor.lastrowid
                cursor.execute(
                    """INSERT INTO usuarios (id_empleado, username, password, rol, activo)
                       VALUES (%s, %s, %s, %s, 1)""",
                    (empleado_id, username, password, rol_db),
                )
            connection.commit()
            return True

        except Error:

            connection.rollback()

            return False
        finally:
            connection.close()

    def actualizar_empleado(self, emp_id: int, nombre: str, rol_ui: str, username: str | None = None, password: str | None = None) -> bool:
        connection = self._connect()
        if connection is None:
            return False

        rol_db = self._rol_ui_a_db(rol_ui)
        try:
            with connection.cursor() as cursor:
                nombres, apellidos = self._separar_nombre(nombre)
                cursor.execute(
                    """UPDATE empleados AS e
                       INNER JOIN usuarios AS u ON u.id_empleado = e.id_empleado
                       SET e.nombres = %s, e.apellidos = %s, e.cargo = %s
                       WHERE u.id_usuario = %s""",
                    (nombres, apellidos, rol_db, emp_id),
                )
                fields = ["rol = %s"]
                params: list[Any] = [rol_db]
                if username:
                    fields.append("username = %s")
                    params.append(username.strip())
                if password:
                    fields.append("password = %s")
                    params.append(password)
                params.append(emp_id)
                cursor.execute(f"UPDATE usuarios SET {', '.join(fields)} WHERE id_usuario = %s", tuple(params))
            connection.commit()
            return True
        except Error:
            connection.rollback()
            return False
        finally:
            connection.close()

    def eliminar_empleado(self, emp_id: int) -> bool:
        connection = self._connect()
        if connection is None:
            return False

        sql = "DELETE FROM usuarios WHERE id_usuario = %s"

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (emp_id,))
            connection.commit()
            return True
        except Error:
            connection.rollback()
            return False
        finally:
            connection.close()

    def _build_unique_username(self, connection, base: str) -> str:
        base = base or "empleado"
        candidate = base
        seq = 1

        sql = "SELECT 1 FROM usuarios WHERE username = %s LIMIT 1"
        with connection.cursor() as cursor:
            while True:
                cursor.execute(sql, (candidate,))
                exists = cursor.fetchone() is not None
                if not exists:
                    return candidate
                seq += 1
                candidate = f"{base}{seq}"

    def _build_unique_documento(self, connection, base: str) -> str:
        candidate = f"USR-{base or 'empleado'}"
        seq = 1
        with connection.cursor() as cursor:
            while True:
                cursor.execute("SELECT 1 FROM empleados WHERE documento_identidad = %s LIMIT 1", (candidate,))
                if cursor.fetchone() is None:
                    return candidate
                seq += 1
                candidate = f"USR-{base or 'empleado'}-{seq}"

    @staticmethod
    def _separar_nombre(nombre: str) -> tuple[str, str]:
        partes = str(nombre).strip().split(None, 1)
        return partes[0], partes[1] if len(partes) > 1 else "Sin apellido"

    def _connect(self):

        if mysql is None:

            return None
        try:
            return mysql.connector.connect(**self._db_config)

        except Error:

            return None

    @staticmethod
    def _slug_username(nombre: str) -> str:
        cleaned = "".join(ch.lower() if ch.isalnum() else "" for ch in nombre)
        return cleaned[:14] or "empleado"

    @staticmethod
    def _rol_ui_a_db(rol: str) -> str:
        if rol == "Mesero":
            return "Mesero"
        return rol

    @staticmethod
    def _rol_db_a_ui(rol: str) -> str:
        raw = str(rol or "").strip().lower()
        if raw in {"admin", "administrador"}:
            return "Administrador"
        if raw in {"mesero", "mesero", "waiter"}:
            return "Mesero"
        if raw in {"cocinero", "chef", "kitchen"}:
            return "Cocinero"
        return "Mesero"
