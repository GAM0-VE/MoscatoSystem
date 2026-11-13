from __future__ import annotations

from datetime import datetime
from tkinter import messagebox, simpledialog
from typing import Any

from src.models.auditoria.auditoria_model import AuditoriaModel
from src.models.productos.modelo_menu import ModeloMenu
from src.models.productos.imagenes_menu import guardar_imagen_local, buscar_imagen_local
from src.models.usuarios.modelo_usuarios import ModeloUsuarios


class ControladorAdmin:
    """Controlador MVC para gestion de usuarios del panel admin."""

    def __init__(
        self,
        vista,
        modelo: ModeloUsuarios | None = None,
        empleados_seed: list[dict[str, Any]] | None = None,
        modelo_menu: ModeloMenu | None = None,
        menu_seed: list[dict[str, Any]] | None = None,
        id_usuario: int | None = None,
    ) -> None:
        self.vista = vista
        self.modelo = modelo or ModeloUsuarios()
        self.modelo_menu = modelo_menu or ModeloMenu()
        self.auditoria_model = AuditoriaModel()
        self.id_usuario = int(id_usuario) if id_usuario not in (None, "") else getattr(vista, "id_usuario", None)
        self._seed = empleados_seed or []
        self._menu_seed = menu_seed or []
        self._all_empleados: list[dict[str, Any]] = []
        self._all_productos: list[dict[str, Any]] = []
        self._categorias: list[dict[str, Any]] = []

        self.vista.controller = self
        
        if hasattr(self.vista, "after"):
            self.vista.after(150, self._carga_inicial_async)
        else:
            self._carga_inicial_async()

    def _carga_inicial_async(self) -> None:
        self.cargar_empleados()
        self.cargar_menu()

    def cargar_menu(self) -> None:
        productos = self.modelo_menu.obtener_productos()
        self._categorias = self.modelo_menu.obtener_categorias()
        self._all_productos = productos or list(self._menu_seed)
        self._render_menu_filtrado_actual()

    def handle_menu_search(self) -> None:
        self._render_menu_filtrado_actual()

    def handle_add_product(self) -> None:
        if hasattr(self.vista, "open_product_form"):
            self.vista.open_product_form(None, self._categorias, self._save_new_product)
            return
        datos = self._pedir_datos_producto("Nuevo plato")
        if datos is None:
            return
        self._save_new_product(datos)

    def _save_new_product(self, datos) -> None:
        imagen = guardar_imagen_local(datos[0], datos[4])
        if self.modelo_menu.crear_producto(*datos[:4]):
            self._registrar_auditoria("INSERTAR", "productos", f"Se creó el producto '{datos[0]}' en categoria ID {datos[3]}.")
            self.cargar_menu()
            return
        nuevo_id = max([int(item.get("id", 0)) for item in self._all_productos] + [0]) + 1
        categoria = self._categoria_nombre(datos[3])
        self._all_productos.append(self._producto_vista(nuevo_id, datos, categoria, imagen))
        self._render_menu_filtrado_actual()

    def handle_edit_product(self, product_id: int) -> None:
        producto = self._find_product_by_id(product_id)
        if producto is None:
            messagebox.showwarning("Editar plato", "No se encontro el plato seleccionado.", parent=self.vista)
            return
        if hasattr(self.vista, "open_product_form"):
            self.vista.open_product_form(producto, self._categorias, lambda datos: self._save_edited_product(product_id, producto, datos))
            return
        datos = self._pedir_datos_producto("Editar plato", producto)
        if datos is None:
            return
        self._save_edited_product(product_id, producto, datos)

    @staticmethod
    def _detalle_cambio_producto(producto_original: dict[str, Any] | None, datos_nuevos: tuple[str, str, float, int]) -> str:
        nombre_anterior = str((producto_original or {}).get("name", "desconocido"))
        nombre_nuevo = str(datos_nuevos[0])
        precio_anterior = (producto_original or {}).get("price")
        precio_nuevo = datos_nuevos[2]
        categoria_anterior = (producto_original or {}).get("category_id")
        categoria_nueva = datos_nuevos[3]
        descripcion_anterior = str((producto_original or {}).get("description", ""))
        descripcion_nueva = str(datos_nuevos[1])

        cambios: list[str] = []
        if nombre_anterior != nombre_nuevo:
            cambios.append(f"nombre '{nombre_anterior}' -> '{nombre_nuevo}'")
        if descripcion_anterior != descripcion_nueva:
            cambios.append(f"descripción '{descripcion_anterior}' -> '{descripcion_nueva}'")
        if precio_anterior != precio_nuevo:
            cambios.append(f"precio {precio_anterior} -> {precio_nuevo}")
        if categoria_anterior != categoria_nueva:
            cambios.append(f"categoría {categoria_anterior} -> {categoria_nueva}")
        if not cambios:
            cambios.append("datos del producto")

        return f"Se actualizó el producto '{nombre_nuevo}' ({'; '.join(cambios)})."

    def _save_edited_product(self, product_id: int, producto: dict[str, Any], datos) -> None:
        imagen = guardar_imagen_local(datos[0], datos[4])
        if self.modelo_menu.actualizar_producto(product_id, *datos[:4]):
            detalle = self._detalle_cambio_producto(producto, datos[:4])
            self._registrar_auditoria("ACTUALIZAR", "productos", detalle)
            self.cargar_menu()
            return
        producto.update({"name": datos[0], "description": datos[1], "price": datos[2], "category_id": datos[3], "category": self._categoria_nombre(datos[3]), "image": imagen})
        self._render_menu_filtrado_actual()

    def handle_toggle_product(self, product_id: int) -> None:
        producto = self._find_product_by_id(product_id)
        if producto is None:
            return
        disponible = not bool(producto.get("available", False))
        if self.modelo_menu.cambiar_disponibilidad(product_id, disponible):
            self._registrar_auditoria("ACTUALIZAR", "productos", f"Se cambió disponibilidad del producto ID {product_id} a {'disponible' if disponible else 'no disponible'}.")
            self.cargar_menu()
            return
        producto["available"] = disponible
        self._render_menu_filtrado_actual()

    def handle_delete_product(self, product_id: int) -> None:
        producto = self._find_product_by_id(product_id)
        if producto is None:
            return
        if not messagebox.askyesno("Eliminar plato", f"Confirma retirar {producto.get('name', 'este plato')}?", parent=self.vista):
            return
        if self.modelo_menu.eliminar_producto(product_id):
            self._registrar_auditoria("ELIMINAR", "productos", f"Se eliminó el producto ID {product_id}: '{producto.get('name', 'desconocido')}'.")
            self.cargar_menu()
            return
        self._all_productos = [item for item in self._all_productos if int(item.get("id", -1)) != product_id]
        self._render_menu_filtrado_actual()

    def _render_menu_filtrado_actual(self) -> None:
        query = (self.vista.get_menu_search_query() if hasattr(self.vista, "get_menu_search_query") else "") or ""
        query = query.strip().lower()
        productos = self._all_productos
        if query:
            productos = [
                item for item in productos
                if query in str(item.get("name", "")).lower()
                or query in str(item.get("description", "")).lower()
                or query in str(item.get("category", "")).lower()
            ]
        self.vista.render_menu(productos)

    def _pedir_datos_producto(self, titulo: str, producto: dict[str, Any] | None = None):
        nombre = simpledialog.askstring(titulo, "Nombre del plato:", parent=self.vista, initialvalue=str((producto or {}).get("name", "")))
        if not nombre:
            return None
        descripcion = simpledialog.askstring(titulo, "Descripcion:", parent=self.vista, initialvalue=str((producto or {}).get("description", "")))
        if descripcion is None:
            return None
        precio_texto = simpledialog.askstring(titulo, "Precio:", parent=self.vista, initialvalue=str((producto or {}).get("price", "")))
        try:
            precio = float(str(precio_texto).replace(",", "."))
            if precio < 0:
                raise ValueError
        except (TypeError, ValueError):
            messagebox.showwarning("Precio invalido", "Ingresa un precio numerico mayor o igual a cero.", parent=self.vista)
            return None
        categoria_default = (producto or {}).get("category_id", self._categorias[0].get("id_categoria") if self._categorias else 0)
        categoria_texto = simpledialog.askstring(titulo, "ID de categoria:", parent=self.vista, initialvalue=str(categoria_default))
        try:
            categoria_id = int(str(categoria_texto))
        except (TypeError, ValueError):
            messagebox.showwarning("Categoria invalida", "Ingresa el ID numerico de una categoria.", parent=self.vista)
            return None
        if self._categorias and categoria_id not in {int(item["id_categoria"]) for item in self._categorias}:
            messagebox.showwarning("Categoria invalida", "La categoria seleccionada no existe o esta inactiva.", parent=self.vista)
            return None
        return nombre.strip(), descripcion.strip(), precio, categoria_id

    def _find_product_by_id(self, product_id: int) -> dict[str, Any] | None:
        return next((item for item in self._all_productos if int(item.get("id", -1)) == int(product_id)), None)

    def _categoria_nombre(self, categoria_id: int) -> str:
        return next((str(item.get("nombre", "Sin categoria")) for item in self._categorias if int(item.get("id_categoria", -1)) == categoria_id), "Sin categoria")

    @staticmethod
    def _producto_vista(product_id: int, datos, categoria: str, imagen: str | None = None) -> dict[str, Any]:
        return {
            "id": product_id,
            "name": datos[0],
            "description": datos[1],
            "price": datos[2],
            "category_id": datos[3],
            "category": categoria,
            "image": imagen or datos[4],
            "available": True,
            "active": True,
        }

    def cargar_empleados(self) -> None:
        """Carga empleados desde DB y actualiza la tabla en la vista."""
        empleados = self.modelo.obtener_empleados()
        empleados = self._normalizar_empleados_para_vista(empleados)
        if empleados:
            self._all_empleados = empleados
        elif self._seed:
            self._all_empleados = list(self._seed)
        else:
            self._all_empleados = []
        self._render_filtrado_actual()

    def handle_search(self) -> None:
        self._render_filtrado_actual()

    def handle_add_employee(self) -> None:
        if hasattr(self.vista, "open_employee_form"):
            self.vista.open_employee_form(None, self._save_new_employee)
            return
        nombre = simpledialog.askstring("Nuevo empleado", "Nombre completo:", parent=self.vista)
        if not nombre:
            return

        rol = simpledialog.askstring(
            "Nuevo empleado",
            "Rol (Administrador, Mesero, Cocinero):",
            parent=self.vista,
            initialvalue="Mesero",
        )
        if not rol:
            return

        rol = self._normalizar_rol(rol)
        status = "Fichado"
        current_time = self._formatear_time(datetime.now())

        created = self.modelo.crear_empleado(nombre.strip(), rol)
        if created:
            self._registrar_auditoria("INSERTAR", "usuarios", f"Se creó el usuario/empleado '{nombre.strip()}' con rol {rol}.")
            self.cargar_empleados()
            return

        new_id = max([int(emp.get("id", 0)) for emp in self._all_empleados] + [0]) + 1
        self._all_empleados.append(
            {
                "id": new_id,
                "name": nombre.strip(),
                "role": rol,
                "status": status,
                "time": current_time,
            }
        )
        self._render_filtrado_actual()

    def _save_new_employee(self, datos) -> None:
        nombre, rol, username, password = datos
        if self.modelo.crear_empleado(nombre, rol, username, password):
            self._registrar_auditoria("INSERTAR", "usuarios", f"Se creó el usuario/empleado '{nombre}' con rol {rol}.")
            self.cargar_empleados()
            messagebox.showinfo("Usuario creado", f"El usuario '{username}' fue creado correctamente.", parent=self.vista)
            return
        messagebox.showerror(
            "No se pudo crear el usuario",
            self.modelo.ultimo_error or "MySQL rechazo la operacion. Verifica la estructura y los datos de la base de datos.",
            parent=self.vista,
        )

    def handle_edit_employee(self, emp_id: int) -> None:
        empleado = self._find_by_id(emp_id)
        if empleado is None:
            messagebox.showwarning("Editar empleado", "No se encontro el empleado seleccionado.", parent=self.vista)
            return

        if hasattr(self.vista, "open_employee_form"):
            self.vista.open_employee_form(empleado, lambda datos: self._save_edited_employee(emp_id, empleado, datos))
            return

        nuevo_nombre = simpledialog.askstring(
            "Editar empleado",
            "Nombre completo:",
            parent=self.vista,
            initialvalue=str(empleado.get("name", "")),
        )
        if not nuevo_nombre:
            return

        nuevo_rol = simpledialog.askstring(
            "Editar empleado",
            "Rol (Administrador, Mesero, Cocinero):",
            parent=self.vista,
            initialvalue=str(empleado.get("role", "Mesero")),
        )
        if not nuevo_rol:
            return

        nuevo_rol = self._normalizar_rol(nuevo_rol)

        updated = self.modelo.actualizar_empleado(emp_id, nuevo_nombre.strip(), nuevo_rol)
        if updated:
            self._registrar_auditoria("ACTUALIZAR", "usuarios", f"Se actualizó el empleado ID {emp_id}: '{nuevo_nombre.strip()}' con rol {nuevo_rol}.")
            self.cargar_empleados()
            return

        empleado["name"] = nuevo_nombre.strip()
        empleado["role"] = nuevo_rol
        empleado["time"] = self._formatear_time(datetime.now())
        self._render_filtrado_actual()

    def _save_edited_employee(self, emp_id: int, empleado: dict[str, Any], datos) -> None:
        nuevo_nombre, nuevo_rol, username, password = datos
        if self.modelo.actualizar_empleado(emp_id, nuevo_nombre, nuevo_rol, username, password):
            self._registrar_auditoria("ACTUALIZAR", "usuarios", f"Se actualizó el empleado ID {emp_id}: '{nuevo_nombre}' con rol {nuevo_rol}.")
            self.cargar_empleados()
            return
        empleado["name"] = nuevo_nombre
        empleado["username"] = username
        empleado["role"] = nuevo_rol
        empleado["time"] = self._formatear_time(datetime.now())
        self._render_filtrado_actual()

    def handle_delete_employee(self, emp_id: int) -> None:
        empleado = self._find_by_id(emp_id)
        if empleado is None:
            messagebox.showwarning("Eliminar empleado", "No se encontro el empleado seleccionado.", parent=self.vista)
            return

        confirm = messagebox.askyesno(
            "Eliminar empleado",
            f"Confirma eliminar a {empleado.get('name', 'este empleado')}?",
            parent=self.vista,
        )
        if not confirm:
            return

        deleted = self.modelo.eliminar_empleado(emp_id)
        if deleted:
            self._registrar_auditoria("ELIMINAR", "usuarios", f"Se eliminó el empleado ID {emp_id}: '{empleado.get('name', 'desconocido')}'.")
            self.cargar_empleados()
            return

        self._all_empleados = [emp for emp in self._all_empleados if int(emp.get("id", -1)) != int(emp_id)]
        self._render_filtrado_actual()

    def _registrar_auditoria(self, accion: str, tabla_afectada: str, detalles: str) -> None:
        if self.id_usuario in (None, 0):
            return
        try:
            self.auditoria_model.registrar_accion(self.id_usuario, accion, tabla_afectada, detalles)
        except Exception:
            pass

    def _render_filtrado_actual(self) -> None:
        query = (self.vista.get_search_query() if hasattr(self.vista, "get_search_query") else "") or ""
        query = query.strip().lower()

        if not query:
            self.vista.render_table(self._all_empleados)
            return

        filtrados = []
        for emp in self._all_empleados:
            name = str(emp.get("name", "")).lower()
            role = str(emp.get("role", "")).lower()
            status = str(emp.get("status", "")).lower()
            if query in name or query in role or query in status:
                filtrados.append(emp)

        self.vista.render_table(filtrados)

    def _normalizar_empleados_para_vista(self, empleados: list[dict[str, Any]]) -> list[dict[str, Any]]:
        normalizados = []
        for emp in empleados:
            normalizados.append(
                {
                    "id": int(emp.get("id") or 0),
                    "name": str(emp.get("name") or "-"),
                    "username": str(emp.get("username") or "-"),
                    "role": self._normalizar_rol(str(emp.get("role") or "Mesero")),
                    "status": str(emp.get("status") or "Fuera de Turno"),
                    "time": self._formatear_time(emp.get("time")),
                }
            )
        return normalizados

    def _find_by_id(self, emp_id: int) -> dict[str, Any] | None:
        for emp in self._all_empleados:
            if int(emp.get("id", -1)) == int(emp_id):
                return emp
        return None

    @staticmethod
    def _normalizar_rol(rol: str) -> str:
        raw = str(rol or "").strip().lower()
        if raw in {"admin", "administrador"}:
            return "Administrador"
        if raw in {"mesero", "waiter"}:
            return "Mesero"
        if raw in {"cocinero", "chef", "kitchen"}:
            return "Cocinero"
        return "Mesero"

    @staticmethod
    def _formatear_time(valor: Any) -> str:
        if isinstance(valor, datetime):
            return valor.strftime("Hoy %H:%M")

        texto = str(valor or "").strip()
        if not texto:
            return "-"

        formatos = (
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
        )
        for fmt in formatos:
            try:
                dt = datetime.strptime(texto, fmt)
                return dt.strftime("Hoy %H:%M")
            except ValueError:
                continue

        return texto[:16]

