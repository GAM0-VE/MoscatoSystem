import os
try:
    import mysql.connector
    from mysql.connector import Error
except Exception:
    mysql = None
    Error = Exception

class AnalisisModel:
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

    def get_dashboard_data(self, fecha_inicio=None, fecha_fin=None):
        data = {
            "producto_estrella": None,
            "ticket_promedio": 0.0,
            "pico_demanda": None,
            "categoria_rentable": None,
            "top_5": [],
            "ventas_por_hora": []
        }
        
        try:
            conn = self._connect()
        except Exception:
            return data
            
        cursor = conn.cursor(dictionary=True)
        try:
            date_filter = ""
            params = []
            if fecha_inicio and fecha_fin:
                date_filter = " AND DATE(pe.fecha_apertura) BETWEEN %s AND %s"
                params = [str(fecha_inicio), str(fecha_fin)]
            elif fecha_inicio:
                date_filter = " AND DATE(pe.fecha_apertura) >= %s"
                params = [str(fecha_inicio)]
            elif fecha_fin:
                date_filter = " AND DATE(pe.fecha_apertura) <= %s"
                params = [str(fecha_fin)]

            # Producto Estrella (más unidades vendidas)
            q_estrella = f"""
                SELECT p.nombre, SUM(dp.cantidad) as total_vendido
                FROM detalle_pedido dp
                JOIN productos p ON dp.id_producto = p.id_producto
                JOIN pedidos pe ON dp.id_pedido = pe.id_pedido
                WHERE pe.estado_pedido NOT IN ('Cancelado') {date_filter}
                GROUP BY p.id_producto
                ORDER BY total_vendido DESC
                LIMIT 1
            """
            cursor.execute(q_estrella, params)
            estrella = cursor.fetchone()
            if estrella:
                data["producto_estrella"] = estrella["nombre"]

            # Comandas por día (promedio)
            q_comandas = f"""
                SELECT COUNT(pe.id_pedido) / GREATEST(COUNT(DISTINCT DATE(pe.fecha_apertura)), 1) as promedio_diario
                FROM pedidos pe
                WHERE pe.estado_pedido NOT IN ('Cancelado') {date_filter}
            """
            cursor.execute(q_comandas, params)
            comandas = cursor.fetchone()
            if comandas and comandas["promedio_diario"]:
                data["ticket_promedio"] = float(comandas["promedio_diario"])

            # Categoría más rentable
            q_categoria = f"""
                SELECT c.nombre, SUM(dp.subtotal) as ingresos
                FROM detalle_pedido dp
                JOIN productos p ON dp.id_producto = p.id_producto
                JOIN categorias c ON p.id_categoria = c.id_categoria
                JOIN pedidos pe ON dp.id_pedido = pe.id_pedido
                WHERE pe.estado_pedido NOT IN ('Cancelado') {date_filter}
                GROUP BY c.id_categoria
                ORDER BY ingresos DESC
                LIMIT 1
            """
            cursor.execute(q_categoria, params)
            categoria = cursor.fetchone()
            if categoria:
                data["categoria_rentable"] = categoria["nombre"]
                
            # Top 5 Platos
            q_top5 = f"""
                SELECT p.nombre, SUM(dp.cantidad) as total_vendido
                FROM detalle_pedido dp
                JOIN productos p ON dp.id_producto = p.id_producto
                JOIN pedidos pe ON dp.id_pedido = pe.id_pedido
                WHERE pe.estado_pedido NOT IN ('Cancelado') {date_filter}
                GROUP BY p.id_producto
                ORDER BY total_vendido DESC
                LIMIT 5
            """
            cursor.execute(q_top5, params)
            data["top_5"] = cursor.fetchall()
            
            # Pico demanda (hora)
            q_hora = f"""
                SELECT HOUR(pe.fecha_apertura) as hora, COUNT(*) as cantidad_pedidos
                FROM pedidos pe
                WHERE pe.estado_pedido NOT IN ('Cancelado')
                  AND HOUR(pe.fecha_apertura) BETWEEN 9 AND 20
                  {date_filter}
                GROUP BY HOUR(pe.fecha_apertura)
                ORDER BY cantidad_pedidos DESC
            """
            cursor.execute(q_hora, params)
            horas = cursor.fetchall()
            
            # Format ventas_por_hora for chart (9 to 20 hours)
            ventas_dict = {h: 0 for h in range(9, 21)}
            for h in horas:
                if h["hora"] is not None:
                    ventas_dict[h["hora"]] = h["cantidad_pedidos"]
                    
            def _fmt_ampm(h):
                if h == 0: return "12:00 AM"
                elif h < 12: return f"{h}:00 AM"
                elif h == 12: return "12:00 PM"
                else: return f"{h - 12}:00 PM"
            data["ventas_por_hora"] = [{"hora": _fmt_ampm(h), "hora_24": h, "pedidos": count} for h, count in ventas_dict.items()]
            
            if horas and horas[0]["hora"] is not None:
                pico_h = horas[0]["hora"]
                data["pico_demanda"] = f"{_fmt_ampm(pico_h)} - {_fmt_ampm((pico_h + 1) % 24)}"
            else:
                data["pico_demanda"] = "N/A"

        except Exception as e:
            print("Error en AnalisisModel:", e)
        finally:
            cursor.close()
            conn.close()
            
        return data
