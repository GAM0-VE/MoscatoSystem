# Guía de Configuración de Red (LAN) para Restaurante Moscato

Para utilizar el sistema **Restaurante Moscato** en múltiples dispositivos de forma simultánea, necesitas designar una computadora como "Servidor Principal" y las demás como "Clientes". Todas deben estar conectadas a la misma red local (por ejemplo, el mismo módem WiFi o red por cable).

Sigue estos pasos para configurar la red:

---

## 1. Configurar la Computadora Principal (Servidor)

Esta computadora alojará la base de datos MySQL y siempre debe estar encendida cuando el restaurante esté operando.

### A. Permitir conexiones externas en MySQL

Por defecto, MySQL solo permite conexiones desde la misma computadora (`localhost`). Para permitir que otras computadoras se conecten, debes modificar su archivo de configuración:

1. Busca el archivo de configuración de MySQL (usualmente `my.ini` en Windows, ubicado en `C:\ProgramData\MySQL\MySQL Server X.X\my.ini`).
2. Ábrelo con el bloc de notas (como Administrador).
3. Busca la línea que dice `bind-address` y cámbiala a:
   ```ini
   bind-address = 0.0.0.0
   ```
4. Guarda el archivo y **reinicia el servicio de MySQL** (puedes buscar "Servicios" en el menú inicio de Windows, buscar "MySQL" y darle clic derecho -> Reiniciar).

### B. Otorgar permisos al Usuario de Base de Datos

El usuario que utiliza la aplicación necesita permisos para conectarse desde cualquier dirección IP de la red:

1. Abre tu gestor de base de datos favorito en la Computadora Principal (ej. MySQL Workbench o DBeaver).
2. Ejecuta el siguiente comando SQL:
   ```sql
   GRANT ALL PRIVILEGES ON moscato_db.* TO 'root'@'%' IDENTIFIED BY 'tu_contraseña';
   FLUSH PRIVILEGES;
   ```
   *(Sustituye `'tu_contraseña'` por la contraseña real del usuario root, si tienes otra. Si estás usando otro usuario, reemplaza `'root'` por el nombre de ese usuario).*

### C. Descubrir la IP del Servidor

Las otras computadoras necesitarán saber dónde buscar la base de datos.
1. En la Computadora Principal, presiona `Windows + R`, escribe `cmd` y dale a Enter.
2. Escribe el comando `ipconfig` y presiona Enter.
3. Busca la línea que dice **"Dirección IPv4"** (normalmente se ve como `192.168.1.X` o `192.168.0.X`).
4. **Anota esta dirección IP.** (Nota: Se recomienda configurar una IP estática en esta computadora para evitar que cambie al reiniciarse el módem).

---

## 2. Configurar las Computadoras Secundarias (Clientes)

En las computadoras que usarán los meseros, los administradores o la cocina, debes realizar lo siguiente:

1. Inicia la aplicación **Restaurante Moscato** (`python main.py` o su ejecutable correspondiente).
2. En la pantalla de inicio de sesión, haz clic en el botón inferior que dice:
   **"⚙️ Configurar Conexión LAN"**
3. Se abrirá una ventana de configuración. Ingresa los datos correspondientes:
   * **IP del Servidor (Host):** Ingresa la IP que anotaste en el paso *1.C* (ej. `192.168.1.15`).
   * **Puerto:** Déjalo en `3306` (a menos que hayas cambiado el puerto de MySQL).
   * **Usuario de BD:** Escribe el usuario de base de datos (generalmente `root`).
   * **Contraseña:** Escribe la contraseña de la base de datos (déjalo vacío si no tiene).
   * **Nombre de BD:** `moscato_db`
4. Haz clic en **Guardar Configuración**.
5. ¡Listo! Ahora la aplicación se conectará automáticamente a la Computadora Principal. Puedes iniciar sesión normalmente con cualquier empleado registrado.

### Dónde se guarda la configuración
Las computadoras cliente guardan esta información en un archivo llamado `db_config.json` dentro de la carpeta del proyecto. Si en algún momento la IP del servidor cambia, simplemente vuelve a presionar el botón "⚙️ Configurar Conexión LAN" y actualízala.
