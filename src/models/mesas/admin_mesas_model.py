import os
import mysql.connector

class AdminMesasModel:
    def __init__(self):
        self._db_config = {
            "host": os.getenv("DB_HOST", "127.0.0.1"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_NAME", "moscato_db"),
        }

    def _connect(self):
        return mysql.connector.connect(**self._db_config)

    def obtener_mesas(self):
        query = """
            SELECT 
                m.id_mesa, 
                m.numero_mesa, 
                CASE 
                    WHEN m.estado IN ('Atencion', 'Sirviendo', 'Ocupada') THEN m.estado
                    WHEN (SELECT COUNT(*) FROM pedidos p WHERE p.id_mesa = m.id_mesa AND p.pagado = 0 AND p.estado_pedido != 'Cancelado') > 0 THEN 'Ocupada'
                    WHEN m.estado = '' OR m.estado IS NULL THEN 'Libre'
                    ELSE m.estado 
                END AS estado, 
                m.activo 
            FROM mesas m 
            ORDER BY m.numero_mesa
        """
        try:
            conn = self._connect()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                return cursor.fetchall() or []
        except Exception as e:
            print(f"Error al obtener mesas: {e}")
            return []
        finally:
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def agregar_mesa(self, numero_mesa):
        check_query = "SELECT id_mesa FROM mesas WHERE numero_mesa = %s"
        try:
            conn = self._connect()
            with conn.cursor() as cursor:
                cursor.execute(check_query, (numero_mesa,))
                existente = cursor.fetchone()
                if existente:
                    return False, f"La mesa número {numero_mesa} ya existe."
                    
                query = "INSERT INTO mesas (numero_mesa) VALUES (%s)"
                cursor.execute(query, (numero_mesa,))
                conn.commit()
                return True, "Mesa agregada exitosamente."
        except Exception as e:
            return False, f"Error al agregar mesa: {e}"
        finally:
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def editar_mesa(self, id_mesa, numero_mesa):
        check_query = "SELECT id_mesa FROM mesas WHERE numero_mesa = %s AND id_mesa != %s"
        try:
            conn = self._connect()
            with conn.cursor() as cursor:
                cursor.execute(check_query, (numero_mesa, id_mesa))
                existente = cursor.fetchone()
                if existente:
                    return False, f"La mesa número {numero_mesa} ya existe en otro registro."
                    
                query = "UPDATE mesas SET numero_mesa = %s WHERE id_mesa = %s"
                cursor.execute(query, (numero_mesa, id_mesa))
                conn.commit()
                return True, "Mesa actualizada exitosamente."
        except Exception as e:
            return False, f"Error al actualizar mesa: {e}"
        finally:
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def cambiar_estado_activo(self, id_mesa, activo):
        query = "UPDATE mesas SET activo = %s WHERE id_mesa = %s"
        try:
            conn = self._connect()
            with conn.cursor() as cursor:
                cursor.execute(query, (activo, id_mesa))
                conn.commit()
                return True, "Estado actualizado exitosamente."
        except Exception as e:
            return False, f"Error al cambiar estado: {e}"
        finally:
            if 'conn' in locals() and conn.is_connected():
                conn.close()
