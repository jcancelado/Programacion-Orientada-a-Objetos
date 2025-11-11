"""
POO_Tkinter_Firebase_demo.py

Proyecto didáctico que combina:
 - Programación orientada a objetos (clases, herencia, polimorfismo)
 - Interfaz gráfica con Tkinter (vistas con frames apilados)
 - Persistencia opcional con Firebase Realtime Database (firebase_admin)

El archivo incluye explicaciones línea por línea (comentarios) para que entiendas
qué hace cada instrucción y cómo encajan las piezas.

USO:
 - Si tienes un archivo `serviceAccountKey.json` y tu URL de Realtime Database,
   colócalos en el mismo directorio y rellena DATABASE_URL más abajo.
 - Si no tienes Firebase, el programa arrancará en modo "offline" (solo memoria)
   para que puedas probar la interfaz y la lógica de POO sin errores.

Ejecuta:
    python POO_Tkinter_Firebase_demo.py

"""

# ----------------------- IMPORTS -----------------------
# Importamos tkinter y ttk para crear la interfaz.
import tkinter as tk  # El módulo base de Tkinter
from tkinter import ttk, messagebox  # ttk = widgets con estilo, messagebox para diálogos

# Importaciones relacionadas con Firebase están en try/except
# para permitir ejecutar el ejemplo sin tener firebase configurado.
try:
    import firebase_admin  # SDK admin de Firebase
    from firebase_admin import credentials, db  # para inicializar y usar Realtime DB
    _FIREBASE_AVAILABLE = True
except Exception:
    # Si falla la importación (no instalado), marcamos que no está disponible.
    _FIREBASE_AVAILABLE = False

# ----------------------- CLASES DE DOMINIO (POO) -----------------------
# Clase base: Usuario
class Usuario:
    """Clase base que representa un usuario genérico.

    Atributos:
        nombre (str): nombre del usuario
        correo (str): correo electrónico
    """

    def __init__(self, nombre: str, correo: str):
        # Guardamos los atributos en la instancia
        self.nombre = nombre
        self.correo = correo

    def mostrar_info(self) -> str:
        # Método que devuelve una representación legible.
        # Será sobrescrito por subclases para demostrar polimorfismo.
        return f"Usuario: {self.nombre}, correo: {self.correo}"

    def tipo(self) -> str:
        # Retorna el tipo de la clase. Subclases devolverán otros valores.
        return "Usuario"

    def to_dict(self) -> dict:
        # Método de utilidad para convertir el objeto a diccionario
        # listo para persistir (por ejemplo en Firebase).
        return {
            "nombre": self.nombre,
            "correo": self.correo,
            "tipo": self.tipo(),
        }


# Subclase: Admin
class Admin(Usuario):
    """Admin hereda de Usuario y añade permisos."""

    def __init__(self, nombre: str, correo: str, permisos: str = "total"):
        # Llamamos al constructor de la clase base para inicializar nombre y correo
        super().__init__(nombre, correo)
        # Atributo extra exclusivo de Admin
        self.permisos = permisos

    def mostrar_info(self) -> str:
        # Sobrescribimos mostrar_info para dar una representación distinta
        return f"[Admin] {self.nombre} - permisos: {self.permisos}"

    def tipo(self) -> str:
        # Indica que esta instancia es de tipo Admin
        return "Admin"

    def to_dict(self) -> dict:
        # Extiende la representación en diccionario con el campo permisos
        d = super().to_dict()
        d.update({"permisos": self.permisos})
        return d


# Subclase: Cliente
class Cliente(Usuario):
    """Cliente hereda de Usuario y añade puntos de fidelidad."""

    def __init__(self, nombre: str, correo: str, puntos: int = 0):
        super().__init__(nombre, correo)
        self.puntos = puntos

    def mostrar_info(self) -> str:
        # Representación distinta para clientes
        return f"[Cliente] {self.nombre} - Puntos: {self.puntos}"

    def tipo(self) -> str:
        return "Cliente"

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"puntos": self.puntos})
        return d


# ----------------------- SERVICIO DE PERSISTENCIA (FIREBASE) -----------------------
class FirebaseService:
    """Clase que encapsula las operaciones con Firebase Realtime Database.

    Si Firebase no está disponible (por ejemplo, no está instalado o no se puso la
    credencial), la clase se inicializará en modo 'offline' y almacenará datos en memoria.
    """

    def __init__(self, cred_path: str = "serviceAccountKey.json", database_url: str = ""):
        # Guardamos variables de configuración
        self.cred_path = cred_path
        self.database_url = database_url
        self.online = False  # Indicador de si estamos conectados a Firebase

        # Contenedor en memoria como fallback si Firebase no está disponible
        self._in_memory = {}

        # Intentamos inicializar Firebase solo si el paquete está disponible
        if _FIREBASE_AVAILABLE:
            try:
                # Cargamos credenciales desde archivo JSON de la cuenta de servicio
                cred = credentials.Certificate(self.cred_path)
                # Inicializamos la app admin con la URL especificada
                firebase_admin.initialize_app(cred, {"databaseURL": self.database_url})
                # Obtenemos la referencia raíz deseada; aquí usamos '/usuarios'
                self.ref = db.reference("/usuarios")
                self.online = True
                print("[FirebaseService] Conectado a Firebase Realtime Database.")
            except Exception as ex:
                # Si algo falla en la inicialización, caemos a modo offline
                print("[FirebaseService] No se pudo inicializar Firebase:", ex)
                print("[FirebaseService] Usando modo OFFLINE (memoria local).")
                self.online = False
                self.ref = None
        else:
            # Paquete firebase_admin no disponible
            print("[FirebaseService] paquete 'firebase_admin' no encontrado.")
            print("[FirebaseService] Usando modo OFFLINE (memoria local).")
            self.online = False
            self.ref = None

    def push(self, obj: dict) -> str:
        """Inserta un objeto en la base de datos.

        Si estamos online, usamos `push()` de Firebase que devuelve la clave única.
        Si estamos offline, generamos una clave simple y lo guardamos en el dict.
        Retornamos la clave generada.
        """
        if self.online and self.ref is not None:
            new_ref = self.ref.push(obj)
            # new_ref.key es la clave generada por Firebase
            print(f"[FirebaseService] Guardado en Firebase con clave: {new_ref.key}")
            return new_ref.key
        else:
            # Modo offline: generamos una clave simple con longitud incremental
            key = f"local_{len(self._in_memory) + 1}"
            self._in_memory[key] = obj
            print(f"[FirebaseService] (OFFLINE) Guardado en memoria con clave: {key}")
            return key

    def get_all(self) -> dict:
        """Recupera todos los objetos.

        Si estamos online, hacemos ref.get(), de lo contrario devolvemos el dict en memoria.
        """
        if self.online and self.ref is not None:
            data = self.ref.get() or {}
            print(f"[FirebaseService] Recuperados {len(data)} elementos desde Firebase.")
            return data
        else:
            print(f"[FirebaseService] (OFFLINE) Recuperados {len(self._in_memory)} elementos desde memoria.")
            return dict(self._in_memory)

    def update(self, key: str, values: dict) -> None:
        """Actualiza un nodo por clave.

        Si online, usamos child(key).update(values). En offline, actualizamos el dict.
        """
        if self.online and self.ref is not None:
            self.ref.child(key).update(values)
            print(f"[FirebaseService] Actualizado {key} en Firebase.")
        else:
            if key in self._in_memory:
                self._in_memory[key].update(values)
                print(f"[FirebaseService] (OFFLINE) Actualizado {key}.")

    def delete(self, key: str) -> None:
        """Borra un nodo por clave."""
        if self.online and self.ref is not None:
            self.ref.child(key).delete()
            print(f"[FirebaseService] Borrado {key} en Firebase.")
        else:
            if key in self._in_memory:
                del self._in_memory[key]
                print(f"[FirebaseService] (OFFLINE) Borrado {key} de memoria.")


# ----------------------- INTERFAZ GRÁFICA (Tkinter) -----------------------
class AppGUI(tk.Tk):
    """Clase principal de la aplicación gráfica que hereda de tk.Tk.

    Esta clase crea un contenedor donde se apilan distintas vistas (frames).
    """

    def __init__(self, firebase_service: FirebaseService):
        # Llamamos al constructor de tk.Tk que crea la ventana real.
        super().__init__()

        # Guardamos la referencia al servicio de persistencia (inyección de dependencias).
        self.firebase = firebase_service

        # Configuramos la ventana principal: título y tamaño inicial.
        self.title("POO + Tkinter + Firebase - Demo")
        self.geometry("560x380")

        # Creamos un contenedor que alojará las vistas apiladas.
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        # Diccionario de frames: nombre_clase -> instancia
        self.frames = {}

        # Creamos las vistas y las guardamos en el diccionario.
        for ViewClass in (HomeView, RegisterView, ListView):
            # Instanciamos la vista pasando el contenedor y el controlador (self)
            view_instance = ViewClass(container, self)
            name = ViewClass.__name__
            self.frames[name] = view_instance
            # Colocamos cada vista en la misma celda de la grilla para apilarlas
            view_instance.grid(row=0, column=0, sticky="nsew")

        # Imprimimos el diccionario de frames para depuración (petición previa).
        print("Diccionario de frames creado:")
        for nombre, frame in self.frames.items():
            print(f"  {nombre}: {frame}")

        # Mostramos la vista inicial
        self.show_frame("HomeView")

    def show_frame(self, name: str) -> None:
        """Eleva la vista con nombre `name` al frente usando tkraise()."""
        frame = self.frames[name]
        frame.tkraise()


# ----------------------- VISTAS / FRAMES -----------------------
class HomeView(ttk.Frame):
    """Vista principal con botones de navegación."""

    def __init__(self, parent, controller: AppGUI):
        super().__init__(parent)
        # Título
        ttk.Label(self, text="Menú principal", font=(None, 16, "bold")).pack(pady=(18, 8))

        # Botones de navegación
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Registrar usuario",
                   command=lambda: controller.show_frame("RegisterView")).pack(side="left", padx=8)

        ttk.Button(btn_frame, text="Listar usuarios",
                   command=lambda: controller.show_frame("ListView")).pack(side="left", padx=8)

        # Estado de conexión de Firebase
        status = "ONLINE" if controller.firebase.online else "OFFLINE"
        ttk.Label(self, text=f"Estado persistencia: {status}").pack(pady=(20, 0))


class RegisterView(ttk.Frame):
    """Vista para registrar usuarios (aplica POO y polimorfismo al crear instancias)."""

    def __init__(self, parent, controller: AppGUI):
        super().__init__(parent)
        self.controller = controller  # Guardamos controlador para usar firebase

        # Título
        ttk.Label(self, text="Registrar usuario", font=(None, 14, "bold")).pack(pady=(12, 8))

        # Campos: Nombre y Correo
        frm = ttk.Frame(self)
        frm.pack(padx=12, pady=6, fill="x")

        ttk.Label(frm, text="Nombre:").grid(row=0, column=0, sticky="w")
        self.nombre_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.nombre_var).grid(row=0, column=1, sticky="ew")

        ttk.Label(frm, text="Correo:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.correo_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.correo_var).grid(row=1, column=1, sticky="ew", pady=(8, 0))

        # Combobox para seleccionar tipo
        ttk.Label(frm, text="Tipo:").grid(row=2, column=0, sticky="w", pady=(8, 0))
        self.tipo_var = tk.StringVar(value="Usuario")
        tipo_cb = ttk.Combobox(frm, textvariable=self.tipo_var,
                               values=["Usuario", "Admin", "Cliente"], state="readonly")
        tipo_cb.grid(row=2, column=1, sticky="ew", pady=(8, 0))

        # Botones de acción
        action = ttk.Frame(self)
        action.pack(pady=12)

        ttk.Button(action, text="Guardar", command=self.guardar).pack(side="left", padx=6)
        ttk.Button(action, text="Volver", command=lambda: controller.show_frame("HomeView")).pack(side="left", padx=6)

        # Aseguramos que la columna 1 crezca (para que Entry se expanda)
        frm.columnconfigure(1, weight=1)

    def guardar(self):
        """Lee los campos, crea el objeto correspondiente (polimorfismo) y lo guarda."""
        nombre = self.nombre_var.get().strip()
        correo = self.correo_var.get().strip()
        tipo = self.tipo_var.get()

        # Validaciones básicas
        if not nombre or not correo:
            messagebox.showwarning("Atención", "Completa los campos Nombre y Correo")
            return

        # Creamos la instancia correcta según el tipo seleccionado
        if tipo == "Admin":
            usuario = Admin(nombre, correo, permisos="total")
        elif tipo == "Cliente":
            usuario = Cliente(nombre, correo, puntos=0)
        else:
            usuario = Usuario(nombre, correo)

        # Convertimos a diccionario para persistir
        data = usuario.to_dict()

        # Guardamos usando el servicio de persistencia inyectado en el controlador
        key = self.controller.firebase.push(data)

        # Mensaje de éxito y limpiar campos
        messagebox.showinfo("Éxito", f"{usuario.tipo()} guardado con clave {key}")
        self.nombre_var.set("")
        self.correo_var.set("")
        self.tipo_var.set("Usuario")


class ListView(ttk.Frame):
    """Vista para listar, actualizar y eliminar registros."""

    def __init__(self, parent, controller: AppGUI):
        super().__init__(parent)
        self.controller = controller

        # Título
        ttk.Label(self, text="Listado de usuarios", font=(None, 14, "bold")).pack(pady=(12, 8))

        # Frame con Treeview para mostrar tabla
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=8, pady=6)

        # Creamos el Treeview: columnas clave, nombre, correo, tipo
        columns = ("key", "nombre", "correo", "tipo")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        # Definimos encabezados
        self.tree.heading("key", text="Clave")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("correo", text="Correo")
        self.tree.heading("tipo", text="Tipo")

        # Ajustes de columnas (anchos relativos)
        self.tree.column("key", width=120, anchor="w")
        self.tree.column("nombre", width=140, anchor="w")
        self.tree.column("correo", width=160, anchor="w")
        self.tree.column("tipo", width=80, anchor="w")

        # Empaquetamos
        self.tree.pack(fill="both", expand=True)

        # Botones de acciones: actualizar y borrar
        action = ttk.Frame(self)
        action.pack(pady=8)
        ttk.Button(action, text="Refrescar", command=self.refrescar).pack(side="left", padx=6)
        ttk.Button(action, text="Eliminar seleccionado", command=self.eliminar_seleccionado).pack(side="left", padx=6)
        ttk.Button(action, text="Volver", command=lambda: controller.show_frame("HomeView")).pack(side="left", padx=6)

        # Cargamos la lista la primera vez
        self.refrescar()

    def refrescar(self):
        """Recupera datos del servicio y muestra en el Treeview."""
        # Limpiamos contenido actual del Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

        datos = self.controller.firebase.get_all()

        # `datos` es un dict: clave -> dict(campos)
        for key, val in datos.items():
            # Mostramos los campos de forma segura (puede faltar alguno)
            nombre = val.get("nombre", "")
            correo = val.get("correo", "")
            tipo = val.get("tipo", "")
            # Insertamos una fila
            self.tree.insert("", "end", values=(key, nombre, correo, tipo))

    def eliminar_seleccionado(self):
        """Elimina la fila seleccionada tanto de la vista como de la persistencia."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona una fila para eliminar")
            return

        # Obtenemos la clave almacenada en la primera columna
        values = self.tree.item(sel[0], "values")
        key = values[0]

        # Confirmación
        if not messagebox.askyesno("Confirmar", "¿Eliminar el registro seleccionado?"):
            return

        # Borramos usando el servicio
        self.controller.firebase.delete(key)
        # Refrescamos la vista
        self.refrescar()
        messagebox.showinfo("Hecho", "Registro eliminado")


# ----------------------- PUNTO DE ENTRADA -----------------------
if __name__ == "__main__":
    # Ruta donde el usuario puede colocar su archivo de credenciales JSON.
    # Si no usas Firebase, puedes dejar el valor por defecto y el programa seguirá
    # funcionando en modo OFFLINE.
    SERVICE_ACCOUNT_PATH = "serviceAccountKey.json"  # <-- coloca aquí tu JSON si lo tienes

    # URL de la Realtime Database de tu proyecto Firebase. Ejemplo:
    # "https://mi-proyecto-default-rtdb.firebaseio.com/"
    DATABASE_URL = ""  # <- PON AQUÍ tu databaseURL si quieres conectar a Firebase

    # Inicializamos el servicio de persistencia
    firebase_service = FirebaseService(cred_path=SERVICE_ACCOUNT_PATH, database_url=DATABASE_URL)

    # Creamos y arrancamos la interfaz (inyectando la dependencia)
    app = AppGUI(firebase_service)
    app.mainloop()

# FIN DEL ARCHIVO
