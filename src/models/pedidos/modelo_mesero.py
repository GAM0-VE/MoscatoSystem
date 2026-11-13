import os

from typing import Any

import mysql.connector

from mysql.connector import Error



class ModeloMesero:

    def __init__(self):

        self._db_config = {

            "host": os.getenv("DB_HOST", "127.0.0.1"),

            "port": int(os.getenv("DB_PORT", "3306")),

            "user": os.getenv("DB_USER", "root"),

            "password": os.getenv("DB_PASSWORD", ""),

            "database": os.getenv("DB_NAME", "moscato_db"),

            "autocommit": False,

        }



    def _connect_db(self):

        try:

            return mysql.connector.connect(**self._db_config)

        except Error:

            return None



    def obtener_categorias_y_productos(self) -> dict:

        categorias_map = {

            "moscato chino - compartir": "Combos",

            "moscato chino - personal": "Comida China",

            "moscato broaster": "Combos",

            "promociones": "Promos",

            "comida": "Comida China",

            "bebida": "Bebidas",

            "bebidas": "Bebidas",

            "postre": "Comida China",

        }

        

        connection = self._connect_db()

        if not connection:

            return {}

            

        productos_por_categoria = {

            "Comida China": [],

            "Combos": [],

            "Promos": [],

            "Bebidas": [],

        }



        try:

            with connection.cursor(dictionary=True) as cursor:

                cursor.execute(

                    """

                    SELECT pr.id_producto, pr.nombre, pr.precio,

                            ca.nombre AS categoria_db, pr.descripcion

                    FROM productos pr

                    INNER JOIN categorias ca ON ca.id_categoria = pr.id_categoria

                    WHERE ca.activo = 1 AND pr.activo = 1 AND pr.disponible = 1

                    ORDER BY ca.id_categoria, pr.id_producto

                    """

                )

                filas = cursor.fetchall()

                

                for producto in filas:

                    categoria_db = str(producto["categoria_db"]).strip().casefold()

                    boton_categoria = categorias_map.get(categoria_db, "Comida China")

                    

                    producto["categoria_db"] = str(producto["categoria_db"])

                    producto["precio"] = float(producto["precio"])

                    

                    if boton_categoria not in productos_por_categoria:

                        productos_por_categoria[boton_categoria] = []

                        

                    productos_por_categoria[boton_categoria].append(producto)

                    

            return productos_por_categoria

        except Exception:

            return {}

        finally:

            connection.close()



    def guardar_orden(self, orden: dict, usuario: str) -> int | None:

        connection = self._connect_db()

        if not connection:

            return None



        try:

            with connection.cursor(dictionary=True) as cursor:

                id_usuario = self._resolver_id_usuario(cursor, usuario)

                id_usuario = id_usuario or 1



                id_mesa = self._resolver_id_mesa(cursor, str(orden.get("mesa", "")))

                tipo_pedido = "Mesa" if id_mesa is not None else "Para llevar"



                id_pedido_edicion = orden.get("id_pedido_edicion")

                if id_pedido_edicion:

                    # Update existing order

                    cursor.execute(

                        """

                        UPDATE pedidos SET id_mesa = %s, tipo_pedido = %s WHERE id_pedido = %s

                        """,

                        (id_mesa, tipo_pedido, id_pedido_edicion)

                    )

                    id_pedido = id_pedido_edicion

                    

                    # Delete old items so we can re-insert the updated list

                    cursor.execute("DELETE FROM detalle_pedido WHERE id_pedido = %s", (id_pedido,))

                else:

                    # Insert new order

                    cursor.execute(

                        """

                        INSERT INTO pedidos (id_mesa, id_usuario, tipo_pedido, estado_pedido, pagado)

                        VALUES (%s, %s, %s, 'En cocina', %s)

                        """,

                        (id_mesa, id_usuario, tipo_pedido, 1 if orden.get("pagado") else 0),

                    )

                    id_pedido = int(cursor.lastrowid)

                if id_mesa is not None:
                    cursor.execute("UPDATE mesas SET estado = 'Atencion' WHERE id_mesa = %s", (id_mesa,))




                self._asegurar_tabla_tickets(cursor)

                cursor.execute(

                    """

                    INSERT INTO pedidos_ticket_map (id_pedido, ticket_numero)

                    VALUES (%s, %s)

                    ON DUPLICATE KEY UPDATE ticket_numero = VALUES(ticket_numero)

                    """,

                    (id_pedido, int(orden.get("ticket") or id_pedido)),

                )



                for item in list(orden.get("items", [])):

                    nombre = str(item.get("nombre", "")).strip()

                    precio = float(item.get("precio", 0.0) or 0.0)

                    cantidad = max(1, int(item.get("cantidad") or 1))

                    notas = str(item.get("notas") or "").strip() or None

                    categoria_db = str(item.get("categoria_db", "Comida"))

                    if not nombre:

                        continue



                    id_producto, is_custom = self._resolver_producto(cursor, nombre)

                    

                    if is_custom:

                        # A├▒adir el nombre original y precio al inicio de las notas para que cocina/factura lo sepa

                        notas = f"[{nombre} - ${precio:,.0f}] " + notas if notas else f"[{nombre} - ${precio:,.0f}]"

                        

                    subtotal = round(precio * cantidad, 2)

                    cursor.execute(

                        """

                        INSERT INTO detalle_pedido (

                            id_pedido,

                            id_producto,

                            cantidad,

                            descripcion_preparacion,

                            subtotal,

                            estado_item

                        )

                        VALUES (%s, %s, %s, %s, %s, 'Pendiente')

                        """,

                        (id_pedido, id_producto, cantidad, notas, subtotal),

                    )

                    item["id_detalle"] = int(cursor.lastrowid)
                    item["id_producto"] = int(id_producto)
                    item["cantidad"] = cantidad
                    item["notas"] = notas or ""
                    item["estado_item"] = "Pendiente"



                connection.commit()

                return int(id_pedido)

        except Error:

            connection.rollback()

            return None

        finally:

            connection.close()



    def obtener_ordenes_pendientes(self) -> list[dict[str, Any]]:

        connection = self._connect_db()

        if not connection:

            return []



        sql = """

            SELECT

                p.id_pedido,

                p.estado_pedido,

                p.pagado,

                p.metodo_pago,

                ptm.ticket_numero,

                CASE

                    WHEN p.id_mesa IS NULL OR p.tipo_pedido = 'Para llevar' THEN 'Para llevar'

                    ELSE CONCAT('Mesa ', m.numero_mesa)

                END AS mesa,

                dp.id_detalle,

                pr.id_producto,

                pr.nombre,

                pr.precio,

                dp.cantidad,

                dp.descripcion_preparacion,

                dp.estado_item

            FROM pedidos p

            INNER JOIN detalle_pedido dp

                ON dp.id_pedido = p.id_pedido

            INNER JOIN productos pr

                ON pr.id_producto = dp.id_producto

            LEFT JOIN mesas m

                ON m.id_mesa = p.id_mesa

            LEFT JOIN pedidos_ticket_map ptm

                ON ptm.id_pedido = p.id_pedido

            WHERE dp.estado_item IN ('Pendiente', 'En cocina', 'En preparación', 'Listo', 'Servido', 'Cancelado')

            AND (DATE(p.fecha_apertura) = CURDATE() OR (p.pagado = 0 AND p.estado_pedido != 'Cancelado'))

            ORDER BY p.id_pedido DESC, dp.id_detalle ASC

        """



        try:

            with connection.cursor(dictionary=True) as cursor:

                cursor.execute(sql)

                return cursor.fetchall()

        except Error:

            return []

        finally:

            connection.close()



    def _resolver_id_usuario(self, cursor, usuario: str) -> int | None:

        cursor.execute(

            """

            SELECT id_usuario

            FROM usuarios u

            INNER JOIN empleados e

                ON e.id_empleado = u.id_empleado

            WHERE TRIM(CONCAT(e.nombres, ' ', e.apellidos)) = %s

              AND u.rol IN ('Mesero', 'Mesero')

              AND u.activo = 1

              AND e.activo = 1

            ORDER BY id_usuario ASC

            LIMIT 1

            """,

            (usuario,),

        )

        row = cursor.fetchone()

        if row:

            return int(row["id_usuario"])



        cursor.execute(

            """

            SELECT id_usuario

            FROM usuarios

            WHERE username = %s AND rol IN ('Mesero', 'Mesero') AND activo = 1

            ORDER BY id_usuario ASC

            LIMIT 1

            """,

            (usuario,),

        )

        username_match = cursor.fetchone()

        if username_match:

            return int(username_match["id_usuario"])



        cursor.execute(

            """

            SELECT id_usuario

            FROM usuarios

            WHERE rol IN ('Mesero', 'Mesero') AND activo = 1

            ORDER BY id_usuario ASC

            LIMIT 1

            """

        )

        fb_row = cursor.fetchone()

        if fb_row:

            return int(fb_row["id_usuario"])

        return None



    def _resolver_id_mesa(self, cursor, mesa_texto: str) -> int | None:

        numero = self._extraer_numero_mesa(mesa_texto)

        if numero is None:

            return None



        cursor.execute("SELECT id_mesa FROM mesas WHERE numero_mesa = %s LIMIT 1", (numero,))

        row = cursor.fetchone()

        if row:

            return int(row["id_mesa"])



        cursor.execute(

            "INSERT INTO mesas (numero_mesa, estado, activo) VALUES (%s, 'Libre', 1)",

            (numero,),

        )

        return int(cursor.lastrowid)



    def _extraer_numero_mesa(self, mesa_texto: str) -> int | None:

        digitos = "".join(ch for ch in str(mesa_texto) if ch.isdigit())

        if not digitos:

            return None

        try:

            return int(digitos)

        except ValueError:

            return None



    def _resolver_producto(self, cursor, nombre: str) -> tuple[int, bool]:

        cursor.execute(

            "SELECT id_producto FROM productos WHERE nombre = %s LIMIT 1",

            (nombre,),

        )

        row = cursor.fetchone()

        if row:

            return int(row["id_producto"]), False



        # Si no existe, usamos o creamos un producto gen├®rico "Producto Personalizado"

        nombre_generico = "Producto Personalizado"

        cursor.execute(

            "SELECT id_producto FROM productos WHERE nombre = %s LIMIT 1",

            (nombre_generico,),

        )

        row = cursor.fetchone()

        if row:

            return int(row["id_producto"]), True



        # Crear categor├¡a "Varios" si no existe

        cursor.execute("SELECT id_categoria FROM categorias WHERE nombre = 'Varios' LIMIT 1")

        cat_row = cursor.fetchone()

        if cat_row:

            id_categoria = int(cat_row["id_categoria"])

        else:

            cursor.execute("INSERT INTO categorias (nombre) VALUES ('Varios')")

            id_categoria = int(cursor.lastrowid)



        # Crear el producto gen├®rico

        cursor.execute(

            """

            INSERT INTO productos (nombre, precio, id_categoria)

            VALUES (%s, 0.0, %s)

            """,

            (nombre_generico, id_categoria),

        )

        return int(cursor.lastrowid), True



    def _asegurar_tabla_tickets(self, cursor) -> None:

        cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS pedidos_ticket_map (

                id_pedido INT PRIMARY KEY,

                ticket_numero INT NOT NULL,

                FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE

            )

            """

        )

    def eliminar_item_pendiente(self, id_detalle: int) -> bool:

        connection = self._connect_db()

        if not connection:

            return False

        try:

            with connection.cursor() as cursor:

                cursor.execute(

                    "DELETE FROM detalle_pedido WHERE id_detalle = %s AND estado_item = 'Pendiente'",

                    (id_detalle,)

                )

            connection.commit()

            return True

        except Error:

            connection.rollback()

            return False

        finally:

            connection.close()



    def cancelar_pedido_pendiente(self, id_pedido: int) -> bool:
        connection = self._connect_db()
        if not connection:
            return False
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_mesa FROM pedidos WHERE id_pedido = %s", (id_pedido,))
                row = cursor.fetchone()
                id_mesa = row[0] if (row and row[0]) else None

                cursor.execute(
                    "UPDATE pedidos SET estado_pedido = 'Cancelado' WHERE id_pedido = %s",
                    (id_pedido,)
                )
                cursor.execute(
                    "UPDATE detalle_pedido SET estado_item = 'Cancelado' WHERE id_pedido = %s",
                    (id_pedido,)
                )

                if id_mesa is not None:
                    cursor.execute("""
                        SELECT COUNT(*) FROM pedidos 
                        WHERE id_mesa = %s 
                          AND estado_pedido IN ('Abierto', 'En cocina', 'Listo')
                          AND id_pedido != %s
                    """, (id_mesa, id_pedido))
                    row_act = cursor.fetchone()
                    activos = row_act[0] if row_act else 0
                    if activos == 0:
                        cursor.execute("UPDATE mesas SET estado = 'Libre' WHERE id_mesa = %s AND activo = 1", (id_mesa,))

            connection.commit()
            return True
        except Error:
            connection.rollback()
            return False
        finally:
            connection.close()

    def cambiar_a_para_llevar(self, id_pedido: int) -> bool:
        """Actualiza tipo_pedido a 'Para llevar', desvincula la mesa y la libera en DB."""
        connection = self._connect_db()
        if not connection:
            return False
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_mesa FROM pedidos WHERE id_pedido = %s", (id_pedido,))
                row = cursor.fetchone()
                id_mesa = row[0] if (row and row[0]) else None

                cursor.execute(
                    "UPDATE pedidos SET tipo_pedido = 'Para llevar', id_mesa = NULL WHERE id_pedido = %s",
                    (id_pedido,)
                )

                if id_mesa is not None:
                    cursor.execute("""
                        SELECT COUNT(*) FROM pedidos 
                        WHERE id_mesa = %s 
                          AND estado_pedido IN ('Abierto', 'En cocina', 'Listo')
                          AND id_pedido != %s
                    """, (id_mesa, id_pedido))
                    row_act = cursor.fetchone()
                    activos = row_act[0] if row_act else 0
                    if activos == 0:
                        cursor.execute("UPDATE mesas SET estado = 'Libre' WHERE id_mesa = %s AND activo = 1", (id_mesa,))

            connection.commit()
            return True
        except Error:
            connection.rollback()
            return False
        finally:
            connection.close()

    def cambiar_tipo_pedido(self, id_pedido: int, nuevo_tipo: str) -> bool:
        if nuevo_tipo == "Para llevar":
            return self.cambiar_a_para_llevar(id_pedido)
        connection = self._connect_db()
        if not connection:
            return False
        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE pedidos SET tipo_pedido = %s WHERE id_pedido = %s", (nuevo_tipo, id_pedido))
            connection.commit()
            return True
        except Error:
            connection.rollback()
            return False
        finally:
            connection.close()

    def consultar_ticket_por_id(self, id_pedido: int) -> int | None:

        connection = self._connect_db()

        if not connection:

            return None

        try:

            with connection.cursor(dictionary=True) as cursor:

                cursor.execute(

                    "SELECT ticket_numero FROM pedidos_ticket_map WHERE id_pedido = %s",

                    (id_pedido,)

                )

                row = cursor.fetchone()

                return int(row["ticket_numero"]) if row else None

        except Error:

            return None

        finally:

            connection.close()

