from __future__ import annotations

import os
from typing import Any

from src.models.productos.imagenes_menu import buscar_imagen_local

try:
    import mysql.connector
    from mysql.connector import Error
except Exception:  # pragma: no cover - fallback cuando mysql-connector no esta disponible
    mysql = None
    Error = Exception


class ModeloMenu:
    """Modelo para consultar y administrar los productos del menu."""

    def __init__(self, db_config: dict[str, Any] | None = None) -> None:
        self._db_config = db_config or {
            "host": os.getenv("DB_HOST", "127.0.0.1"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_NAME", "moscato_db"),
            "autocommit": False,
        }

    def obtener_productos(self) -> list[dict[str, Any]]:
        connection = self._connect()
        if connection is None:
            return []

        sql = """
            SELECT p.id_producto, p.nombre, p.descripcion, p.precio,
                   p.id_categoria, c.nombre AS categoria,
                   p.disponible, p.activo
            FROM productos AS p
            INNER JOIN categorias AS c ON c.id_categoria = p.id_categoria
            ORDER BY p.activo DESC, p.nombre ASC
        """
        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall() or []
        except Error:
            try:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        """SELECT p.id_producto, p.nombre, p.descripcion, p.precio,
                                  p.id_categoria, c.nombre AS categoria,
                                  p.disponible, p.activo
                           FROM productos AS p
                           INNER JOIN categorias AS c ON c.id_categoria = p.id_categoria
                           ORDER BY p.activo DESC, p.nombre ASC"""
                    )
                    rows = cursor.fetchall() or []
            except Error:
                return []
        finally:
            connection.close()
        return [self._normalizar_producto(row) for row in rows]

    def obtener_categorias(self) -> list[dict[str, Any]]:
        connection = self._connect()
        if connection is None:
            return []
        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id_categoria, nombre FROM categorias WHERE activo = 1 ORDER BY nombre")
                return cursor.fetchall() or []
        except Error:
            return []
        finally:
            connection.close()

    def crear_producto(self, nombre: str, descripcion: str, precio: float, id_categoria: int, imagen: str | None = None) -> bool:
        return self._execute_change(
            """INSERT INTO productos (nombre, descripcion, precio, id_categoria, disponible, activo)
               VALUES (%s, %s, %s, %s, 1, 1)""",
            (nombre, descripcion, precio, id_categoria),
        )

    def actualizar_producto(self, product_id: int, nombre: str, descripcion: str, precio: float, id_categoria: int, imagen: str | None = None) -> bool:
        return self._execute_change(
            """UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, id_categoria = %s
               WHERE id_producto = %s""",
            (nombre, descripcion, precio, id_categoria, product_id),
        )

    def cambiar_disponibilidad(self, product_id: int, disponible: bool) -> bool:
        return self._execute_change(
            "UPDATE productos SET disponible = %s WHERE id_producto = %s",
            (1 if disponible else 0, product_id),
        )

    def eliminar_producto(self, product_id: int) -> bool:
        return self._execute_change("UPDATE productos SET activo = 0 WHERE id_producto = %s", (product_id,))

    def _execute_change(self, sql: str, params: tuple[Any, ...]) -> bool:
        connection = self._connect()
        if connection is None:
            return False
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
            connection.commit()
            return True
        except Error:
            connection.rollback()
            return False
        finally:
            connection.close()

    def _connect(self):
        if mysql is None:
            return None
        try:
            return mysql.connector.connect(**self._db_config)
        except Error:
            return None

    @staticmethod
    def _normalizar_producto(row: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": int(row.get("id_producto") or 0),
            "name": str(row.get("nombre") or "-"),
            "description": str(row.get("descripcion") or ""),
            "image": buscar_imagen_local(str(row.get("nombre") or "")) or "",
            "category_id": int(row.get("id_categoria") or 0),
            "category": str(row.get("categoria") or "Sin categoria"),
            "price": float(row.get("precio") or 0),
            "available": bool(row.get("disponible")),
            "active": bool(row.get("activo", 1)),
        }
