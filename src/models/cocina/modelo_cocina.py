import os
from typing import Any

import mysql.connector
from mysql.connector import Error


class ModeloCocina:
    """Modelo MVC para operaciones de cocina en MySQL."""

    def __init__(self) -> None:
        self._db_config = {
            "host": os.getenv("DB_HOST", "127.0.0.1"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_NAME", "moscato_db"),
            "autocommit": False,
        }
        self._asegurar_columna_oculto()

    def _asegurar_columna_oculto(self):
        try:
            conn = self._connect()
            with conn.cursor() as cursor:
                cursor.execute("SHOW COLUMNS FROM detalle_pedido LIKE 'oculto_cocina'")
                if not cursor.fetchone():
                    cursor.execute("ALTER TABLE detalle_pedido ADD COLUMN oculto_cocina TINYINT(1) DEFAULT 0")
                    conn.commit()
            conn.close()
        except Exception:
            pass

    def _connect(self):
        try:
            return mysql.connector.connect(**self._db_config)
        except Error as exc:
            raise ConnectionError(f"No fue posible conectar con MySQL: {exc}") from exc

    def obtener_pedidos_activos(self) -> list[dict[str, Any]]:
        """Obtiene los items activos de cocina con JOIN sobre detalle, pedido, producto y mesa."""
        sql = """
            SELECT
                dp.id_detalle,
                p.id_pedido,
                CASE
                    WHEN p.id_mesa IS NULL OR p.tipo_pedido = 'Para llevar' THEN 'Para llevar'
                    ELSE CAST(m.numero_mesa AS CHAR)
                END AS numero_mesa,
                pr.nombre AS nombre,
                dp.cantidad,
                dp.estado_item AS estado_item,
                dp.descripcion_preparacion,
                dp.fecha_envio_cocina
            FROM detalle_pedido dp
            INNER JOIN pedidos p
                ON p.id_pedido = dp.id_pedido
            INNER JOIN productos pr
                ON pr.id_producto = dp.id_producto
            LEFT JOIN mesas m
                ON m.id_mesa = p.id_mesa
            WHERE dp.estado_item IN ('Pendiente', 'En cocina', 'En preparación', 'Cancelado')
              AND (dp.oculto_cocina = 0 OR dp.oculto_cocina IS NULL)
            ORDER BY dp.fecha_envio_cocina ASC, dp.id_detalle ASC
        """

        connection = self._connect()
        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
        except Error as exc:
            raise RuntimeError(f"Error consultando pedidos activos: {exc}") from exc
        finally:
            connection.close()

    def actualizar_estado_item(self, id_detalle: int, nuevo_estado: str) -> bool:
        """Actualiza el estado_item en detalle_pedido para el id_detalle indicado."""
        sql = """
            UPDATE detalle_pedido
            SET estado_item = %s
            WHERE id_detalle = %s
        """

        connection = self._connect()
        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(sql, (nuevo_estado, id_detalle))
                actualizado = cursor.rowcount > 0
            connection.commit()
            return actualizado
        except Error as exc:
            connection.rollback()
            raise RuntimeError(f"Error actualizando estado del item: {exc}") from exc
        finally:
            connection.close()

    def actualizar_estado_pedido(self, id_pedido: int, nuevo_estado_item: str, nuevo_estado_pedido: str | None = None) -> bool:
        """Actualiza estado de todos los items de un pedido y opcionalmente el estado global del pedido."""
        sql_items = """
            UPDATE detalle_pedido
            SET estado_item = %s
            WHERE id_pedido = %s
              AND estado_item NOT IN ('Cancelado', 'Servido')
        """
        sql_pedido = """
            UPDATE pedidos
            SET estado_pedido = %s
            WHERE id_pedido = %s
        """
        sql_mesa = """
            UPDATE mesas m
            INNER JOIN pedidos p ON m.id_mesa = p.id_mesa
            SET m.estado = %s
            WHERE p.id_pedido = %s
        """

        connection = self._connect()
        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(sql_items, (nuevo_estado_item, id_pedido))
                if nuevo_estado_pedido is not None:
                    cursor.execute(sql_pedido, (nuevo_estado_pedido, id_pedido))
                
                estado_mesa = "Atencion" if "prepara" in nuevo_estado_item.lower() else "Ocupada"
                cursor.execute(sql_mesa, (estado_mesa, id_pedido))
                
                actualizado = cursor.rowcount >= 0
            connection.commit()
            return actualizado
        except Error as exc:
            connection.rollback()
            raise RuntimeError(f"Error actualizando estado del pedido: {exc}") from exc
        finally:
            connection.close()

    def ocultar_pedido_cocina(self, id_pedido: int) -> bool:
        """Marca todos los items de un pedido como ocultos en la cocina."""
        sql = """
            UPDATE detalle_pedido
            SET oculto_cocina = 1
            WHERE id_pedido = %s
        """
        connection = self._connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (id_pedido,))
                actualizado = cursor.rowcount >= 0
            connection.commit()
            return actualizado
        except Error as exc:
            connection.rollback()
            raise RuntimeError(f"Error ocultando pedido en cocina: {exc}") from exc
        finally:
            connection.close()
