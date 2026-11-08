import tkinter as tk
from tkinter import ttk, messagebox

class VistaUsuariosRoles(ttk.Frame):
    """Interfaz gráfica profesional para el registro de usuarios, credenciales y asignación modular de permisos."""

    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self.variables_modulos = {}
        self.id_usuario_seleccionado = None  # Control de estado de edición
        
        # Variable de estado para controlar la visibilidad del panel de formulario
        self.formulario_visible = False
        
        self._construir_interfaz(self)

    def _construir_interfaz(self, contenedor):
        # 1. ENCABEZADO INSTITUCIONAL Y BARRA DE ACCIÓN SUPERIOR
        encabezado = ttk.Frame(contenedor, padding=10)
        encabezado.pack(fill="x", padx=20, pady=10)

        titulo_frame = ttk.Frame(encabezado)
        titulo_frame.pack(side="left")

        ttk.Label(
            titulo_frame, 
            text="Control de Usuarios y Módulos", 
            font=("Segoe UI", 14, "bold"), 
            foreground="#A93226"
        ).pack(anchor="w")

        ttk.Label(
            titulo_frame, 
            text="Gestión de credenciales y permisos de acceso por rol institucional", 
            font=("Segoe UI", 9, "italic"), 
            foreground="#7F8C8D"
        ).pack(anchor="w", pady=(2, 0))

        # Botones de control principal globales (Nuevo Usuario y Volver)
        acciones_globales = ttk.Frame(encabezado)
        acciones_globales.pack(side="right")

        self.btn_crear_usuario_toggle = ttk.Button(
            acciones_globales, text="➕ Crear Usuario", command=self._on_alternar_formulario_creacion
        )
        self.btn_crear_usuario_toggle.pack(side="left", padx=5)

        self.btn_volver = ttk.Button(
            acciones_globales, text="⬅️ Volver", command=self._on_volver_click
        )
        self.btn_volver.pack(side="left", padx=5)

        # 2. CONTENEDOR PRINCIPAL DIVIDIDO EN DOS SECCIONES
        self.layout_principal = ttk.Frame(contenedor, padding=10)
        self.layout_principal.pack(fill="both", expand=True, padx=20, pady=5)
        self.layout_principal.columnconfigure(0, weight=1)  # Panel izquierdo (Formulario condicional)
        self.layout_principal.columnconfigure(1, weight=1)  # Panel derecho (Listado maestro)

        # ==========================================
        # PANEL IZQUIERDO: FORMULARIO (Oculto por defecto)
        # ==========================================
        self.panel_izquierdo = ttk.Frame(self.layout_principal)
        # Nota: No se empaqueta ni ubica con grid inicialmente para que aparezca colapsado/oculto

        # A. Marco de Datos Personales y Credenciales
        formulario = ttk.LabelFrame(self.panel_izquierdo, text=" Registro de Personal y Credenciales ", padding=12)
        formulario.pack(fill="x", pady=(0, 10))
        formulario.columnconfigure(1, weight=1)

        campos = [
            ("Nombres:", 0),
            ("Apellidos:", 1),
            ("Cédula / ID:", 2),
            ("Correo Electrónico:", 3),
            ("Nombre de Usuario:", 4),
            ("Clave Asignada:", 5),
            ("Fecha de nacimiento:", 6)
        ]

        self.entrada_datos_usuario = {}
        for texto_etiqueta, indice in campos:
            ttk.Label(formulario, text=texto_etiqueta, font=("Segoe UI", 9, "bold")).grid(row=indice, column=0, sticky="w", pady=4, padx=5)
            
            mostrar_caracter = "*" if "Clave" in texto_etiqueta else None
            entrada = ttk.Entry(formulario, width=28, show=mostrar_caracter)
            entrada.grid(row=indice, column=1, sticky="ew", pady=4, padx=5)
            self.entrada_datos_usuario[texto_etiqueta] = entrada

        # B. Panel de Módulos Asignables
        modulos_frame = ttk.LabelFrame(self.panel_izquierdo, text=" Asignación y edición de módulos de acceso ", padding=12)
        modulos_frame.pack(fill="x", pady=(0, 10))

        lista_modulos = [
            "Directorio de Alumnos",
            "Control de Notas",
            "Control de Secciones",
            "Control de Profesores, Materias, Años y Secciones",
            "Control de Usuarios"
        ]

        for indice_mod, modulo in enumerate(lista_modulos):
            variable_mod = tk.BooleanVar(value=False)
            casilla = ttk.Checkbutton(modulos_frame, text=modulo, variable=variable_mod)
            casilla.grid(row=indice_mod, column=0, sticky="w", pady=3, padx=5)
            self.variables_modulos[modulo] = variable_mod

        # C. Panel de Botones de Acción Operativa Local
        botones_frame = ttk.Frame(self.panel_izquierdo)
        botones_frame.pack(fill="x", pady=5)
        botones_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.btn_guardar_usuario = ttk.Button(
            botones_frame, text="💾 Guardar", command=self._on_guardar_usuario
        )
        self.btn_guardar_usuario.grid(row=0, column=0, sticky="ew", padx=2)

        self.btn_modificar_usuario = ttk.Button(
            botones_frame, text="✏️ Modificar", command=self._on_modificar_usuario
        )
        self.btn_modificar_usuario.grid(row=0, column=1, sticky="ew", padx=2)

        self.btn_eliminar_usuario = ttk.Button(
            botones_frame, text="🗑️ Eliminar", command=self._on_eliminar_usuario
        )
        self.btn_eliminar_usuario.grid(row=0, column=2, sticky="ew", padx=2)

        self.btn_limpiar_formulario = ttk.Button(
            botones_frame, text="🧹 Limpiar", command=self._on_limpiar_formulario
        )
        self.btn_limpiar_formulario.grid(row=0, column=3, sticky="ew", padx=2)

        # ==========================================
        # PANEL DERECHO: LISTADO Y CONTROL DE USUARIOS
        # ==========================================
        self.listado_control_usuario = ttk.Frame(self.layout_principal)
        self.listado_control_usuario.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        tabla_frame = ttk.LabelFrame(self.listado_control_usuario, text=" Usuarios Registrados (Doble clic para seleccionar y editar) ", padding=12)
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("usuario", "nombre", "correo", "estado")
        self.tree_usuarios = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=16)

        self.tree_usuarios.heading("usuario", text="Usuario")
        self.tree_usuarios.heading("nombre", text="Apellidos y Nombres")
        self.tree_usuarios.heading("correo", text="Correo Electrónico")
        self.tree_usuarios.heading("estado", text="Permisos Activos")

        self.tree_usuarios.column("usuario", width=95, anchor="center")
        self.tree_usuarios.column("nombre", width=160, anchor="w")
        self.tree_usuarios.column("correo", width=150, anchor="w")
        self.tree_usuarios.column("estado", width=100, anchor="center")

        self.tree_usuarios.pack(side="left", fill="both", expand=True)

        barra_desplazamiento = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree_usuarios.yview)
        self.tree_usuarios.configure(yscrollcommand=barra_desplazamiento.set)
        barra_desplazamiento.pack(side="right", fill="y")

        # Vincular doble clic en la tabla
        self.tree_usuarios.bind("<Double-1>", self._on_seleccionar_usuario_tabla)

        # Cargar datos de prueba iniciales
        self._cargar_datos_ejemplo()

    def _on_alternar_formulario_creacion(self):
        """Muestra u oculta dinámicamente el panel del formulario al hacer clic en 'Crear Usuario'."""
        if self.formulario_visible:
            # Ocultar formulario y expandir la tabla de usuarios para ocupar todo el ancho
            self.panel_izquierdo.grid_forget()
            self.listado_control_usuario.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=0)
            self.btn_crear_usuario_toggle.config(text="➕ Crear Usuario")
            self.formulario_visible = False
            self._on_limpiar_formulario()
        else:
            # Mostrar formulario en la columna 0 y mover la tabla a la columna 1
            self.listado_control_usuario.grid_forget()
            self.panel_izquierdo.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
            self.listado_control_usuario.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
            self.btn_crear_usuario_toggle.config(text="✖️ Ocultar Formulario")
            self.formulario_visible = True

    def _cargar_datos_ejemplo(self):
        """Carga usuarios de prueba en la tabla lateral."""
        usuarios_prueba = [
            ("cmendoza", "Pérez González, Alejandro", "cperez@email.com", ["Directorio de Alumnos", "Control de Notas", "Control de Secciones"]),
            ("mrodriguez", "Rodríguez Silva, María", "mrodriguez@email.com", ["Directorio de Alumnos", "Control de Notas", "Control de Secciones", "Control de Profesores, Materias, Años y Secciones", "Control de Usuarios"]),
            ("jgomez", "Gómez Blanco, Jesús", "jgomez@email.com", ["Directorio de Alumnos"]),
        ]
        for usuario, nombre, correo, modulos in usuarios_prueba:
            item_id = self.tree_usuarios.insert("", "end", values=(usuario, nombre, correo, f"{len(modulos)} Módulos"))
            if not hasattr(self, "_mapeo_mods_prueba"):
                self._mapeo_mods_prueba = {}
            self._mapeo_mods_prueba[item_id] = modulos

    def _on_guardar_usuario(self):
        """Captura los datos del formulario y registra un nuevo usuario."""
        nombres = self.entrada_datos_usuario["Nombres:"].get().strip()
        apellidos = self.entrada_datos_usuario["Apellidos:"].get().strip()
        usuario = self.entrada_datos_usuario["Nombre de Usuario:"].get().strip()
        clave = self.entrada_datos_usuario["Clave Asignada:"].get().strip()

        if not nombres or not apellidos or not usuario or not clave:
            messagebox.showwarning("Campos Vacíos", "Por favor complete los campos obligatorios de identificación y credenciales.")
            return

        modulos_asignados = [modulo for modulo, variable in self.variables_modulos.items() if variable.get()]

        datos_nuevo_usuario = {
            "nombres": nombres,
            "apellidos": apellidos,
            "cedula": self.entrada_datos_usuario["Cédula / ID:"].get().strip(),
            "correo": self.entrada_datos_usuario["Correo Electrónico:"].get().strip(),
            "usuario": usuario,
            "clave": clave,
            "nacimiento": self.entrada_datos_usuario["Fecha de nacimiento:"].get().strip(),
            "modulos_permitidos": modulos_asignados
        }

        if self.controlador:
            self.controlador.guardar_usuario_bd(datos_nuevo_usuario)
            messagebox.showinfo("Éxito", f"Usuario '{usuario}' registrado correctamente.")
        else:
            item_id = self.tree_usuarios.insert("", "end", values=(usuario, f"{apellidos}, {nombres}", datos_nuevo_usuario["correo"], f"{len(modulos_asignados)} Módulos"))
            if not hasattr(self, "_mapeo_mods_prueba"):
                self._mapeo_mods_prueba = {}
            self._mapeo_mods_prueba[item_id] = modulos_asignados
            messagebox.showinfo("Registro Exitoso", f"El usuario '{usuario}' ha sido creado con éxito.")
            self._on_limpiar_formulario()
            self._on_alternar_formulario_creacion()  # Ocultar formulario tras guardar con éxito

    def _on_seleccionar_usuario_tabla(self, event):
        """Carga automáticamente los datos y marca las casillas del usuario seleccionado al hacer doble clic."""
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            return
        
        item_id = seleccion[0]
        valores = self.tree_usuarios.item(item_id, "values")
        
        # Si el formulario estaba oculto, lo abrimos automáticamente para editar
        if not self.formulario_visible:
            self._on_alternar_formulario_creacion()

        self.id_usuario_seleccionado = item_id
        self.entrada_datos_usuario["Nombre de Usuario:"].delete(0, tk.END)
        self.entrada_datos_usuario["Nombre de Usuario:"].insert(0, valores[0])
        
        partes_nombre = valores[1].split(",")
        if len(partes_nombre) > 1:
            self.entrada_datos_usuario["Apellidos:"].delete(0, tk.END)
            self.entrada_datos_usuario["Apellidos:"].insert(0, partes_nombre[0].strip())
            self.entrada_datos_usuario["Nombres:"].delete(0, tk.END)
            self.entrada_datos_usuario["Nombres:"].insert(0, partes_nombre[1].strip())
            
        self.entrada_datos_usuario["Correo Electrónico:"].delete(0, tk.END)
        self.entrada_datos_usuario["Correo Electrónico:"].insert(0, valores[2])

        # Marcar dinámicamente los módulos asociados
        modulos_del_usuario = getattr(self, "_mapeo_mods_prueba", {}).get(item_id, [])
        for nombre_modulo, variable in self.variables_modulos.items():
            if nombre_modulo in modulos_del_usuario:
                variable.set(True)
            else:
                variable.set(False)

        messagebox.showinfo("Usuario Seleccionado", f"Se han cargado los datos de '{valores[0]}'. Modifique lo que necesite y presione 'Modificar'.")

    def _on_modificar_usuario(self):
        """Actualiza los datos y la selección de módulos del usuario seleccionado."""
        if not self.id_usuario_seleccionado:
            messagebox.showwarning("Selección Requerida", "Por favor seleccione un usuario de la tabla haciendo doble clic antes de modificar.")
            return

        usuario = self.entrada_datos_usuario["Nombre de Usuario:"].get().strip()
        apellidos = self.entrada_datos_usuario["Apellidos:"].get().strip()
        nombres = self.entrada_datos_usuario["Nombres:"].get().strip()
        correo = self.entrada_datos_usuario["Correo Electrónico:"].get().strip()
        
        modulos_asignados = [modulo for modulo, variable in self.variables_modulos.items() if variable.get()]

        self.tree_usuarios.item(self.id_usuario_seleccionado, values=(usuario, f"{apellidos}, {nombres}", correo, f"{len(modulos_asignados)} Módulos"))
        
        if hasattr(self, "_mapeo_mods_prueba"):
            self._mapeo_mods_prueba[self.id_usuario_seleccionado] = modulos_asignados

        messagebox.showinfo("Modificación Exitosa", f"Los datos y permisos del usuario '{usuario}' han sido actualizados.")
        self._on_limpiar_formulario()
        self._on_alternar_formulario_creacion()  # Ocultar formulario tras editar

    def _on_eliminar_usuario(self):
        """Da de baja o elimina al usuario seleccionado."""
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            messagebox.showwarning("Selección Requerida", "Por favor seleccione el usuario que desea eliminar de la tabla.")
            return

        item_id = seleccion[0]
        valores = self.tree_usuarios.item(item_id, "values")
        usuario = valores[0]

        respuesta = messagebox.askyesno(
            "Confirmación de Baja", 
            f"¿Está seguro de eliminar al usuario '{usuario}'?\nEsta acción revoca todos sus accesos al sistema.",
            parent=self
        )
        if respuesta:
            self.tree_usuarios.delete(item_id)
            if hasattr(self, "_mapeo_mods_prueba") and item_id in self._mapeo_mods_prueba:
                del self._mapeo_mods_prueba[item_id]
            messagebox.showinfo("Usuario Eliminado", f"El usuario '{usuario}' fue dado de baja con éxito.")
            self._on_limpiar_formulario()
            if self.formulario_visible:
                self._on_alternar_formulario_creacion()

    def _on_limpiar_formulario(self):
        """Limpia todos los campos del formulario y desmarca los módulos."""
        for entrada in self.entrada_datos_usuario.values():
            entrada.delete(0, tk.END)
        for variable in self.variables_modulos.values():
            variable.set(False)
        self.id_usuario_seleccionado = None

    def _on_volver_click(self):
        """Cierra la vista actual o regresa al panel principal."""
        if messagebox.askyesno("Volver al Dashboard", "¿Desea regresar al panel principal?"):
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()  
    root.title("Control de roles 2026 - Gestión de Usuarios y Accesos")
    root.geometry("1150x680")
    
    app = VistaUsuariosRoles(parent=root, controlador=None)
    app.pack(fill="both", expand=True)
        
    root.mainloop()