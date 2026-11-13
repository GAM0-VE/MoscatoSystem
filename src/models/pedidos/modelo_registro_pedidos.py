import os
from datetime import datetime

try:
    import mysql.connector
except Exception:
    mysql = None

class RegistroPedidosModel:
    def __init__(self, db_config=None):
        self._db_config = db_config or {
            "host": os.getenv("DB_HOST", "127.0.0.1"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_NAME", "moscato_db"),
        }

    def _connect(self):
        if mysql is None:
            raise ConnectionError("mysql-connector-python no está instalado.")
        return mysql.connector.connect(**self._db_config)

    def obtener_kpis_mensuales(self):
        data = {
            "ventas_mensuales": 0.0,
            "pedidos_mensuales": 0,
            "ticket_promedio": 0.0
        }
        
        try:
            conn = self._connect()
        except Exception:
            return data
            
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT 
                    COUNT(DISTINCT p.id_pedido) as total_pedidos,
                    COALESCE(SUM(dp.subtotal), 0) as total_ventas,
                    COALESCE(SUM(dp.subtotal) / NULLIF(COUNT(DISTINCT p.id_pedido), 0), 0) as ticket_promedio
                FROM pedidos p
                LEFT JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
                WHERE MONTH(p.fecha_apertura) = MONTH(CURRENT_DATE())
                  AND YEAR(p.fecha_apertura) = YEAR(CURRENT_DATE())
                  AND p.estado_pedido NOT IN ('Cancelado')
            """
            cursor.execute(query)
            resultado = cursor.fetchone()
            
            if resultado:
                data["pedidos_mensuales"] = resultado["total_pedidos"] or 0
                data["ventas_mensuales"] = float(resultado["total_ventas"] or 0.0)
                data["ticket_promedio"] = float(resultado["ticket_promedio"] or 0.0)

        except Exception as e:
            print("Error en obtener_kpis_mensuales:", e)
        finally:
            cursor.close()
            conn.close()
            
        return data

    def obtener_historial_pedidos(self, fecha=None):
        try:
            conn = self._connect()
        except Exception:
            return []
            
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT 
                    p.id_pedido,
                    DATE_FORMAT(p.fecha_apertura, '%d/%m - %H:%i') as hora,
                    DATE_FORMAT(p.fecha_apertura, '%Y-%m-%d %H:%i') as fecha_completa,
                    m.numero_mesa,
                    p.tipo_pedido,
                    u.username as mesero_nombre,
                    e.id_empleado as mesero_id,
                    COALESCE(SUM(dp.subtotal), 0) as total,
                    p.metodo_pago,
                    p.estado_pedido
                FROM pedidos p
                LEFT JOIN mesas m ON p.id_mesa = m.id_mesa
                LEFT JOIN usuarios u ON p.id_usuario = u.id_usuario
                LEFT JOIN empleados e ON u.id_empleado = e.id_empleado
                LEFT JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
                WHERE DATE(p.fecha_apertura) = %s
                GROUP BY p.id_pedido, p.fecha_apertura, m.numero_mesa, p.tipo_pedido, u.username, e.id_empleado, p.metodo_pago, p.estado_pedido
                ORDER BY p.fecha_apertura DESC
            """
            
            if not fecha:
                fecha = datetime.now().strftime('%Y-%m-%d')
            elif isinstance(fecha, datetime):
                fecha = fecha.strftime('%Y-%m-%d')
            elif hasattr(fecha, 'strftime'):
                fecha = fecha.strftime('%Y-%m-%d')
                
            cursor.execute(query, (fecha,))
            return cursor.fetchall()

        except Exception as e:
            print("Error en obtener_historial_pedidos:", e)
            return []
        finally:
            cursor.close()
            conn.close()

    def obtener_detalle_pedido(self, id_pedido):
        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT 
                    dp.id_producto,
                    pr.nombre as producto_nombre,
                    dp.cantidad,
                    dp.subtotal,
                    dp.estado_item
                FROM detalle_pedido dp
                JOIN productos pr ON dp.id_producto = pr.id_producto
                WHERE dp.id_pedido = %s
            """
            cursor.execute(query, (id_pedido,))
            detalle = cursor.fetchall()
            
            cursor.close()
            conn.close()
            return detalle
        except Exception as e:
            print("Error al obtener detalle pedido:", e)
            return []

