import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.style import Style

class VistaUsuariosRoles(ttk.Frame):
    """Interfaz gráfica institucional para el registro de usuarios, credenciales y asignación modular de permisos con renderizado optimizado."""

    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self.variables_modulos = {}
        self.id_usuario_seleccionado = None  # Control de estado de edición
        self.formulario_visible = False
        self.imagenes_referencia = []
        
        # Aplicar estilo institucional unificado con fondo #EDECD1
        self.estilo_app = Style(theme="flatly")
        self._configurar_estilos_institucionales()
        self._configurar_scroll(parent)
        self._construir_interfaz(self.scrollable_frame)

    def _configurar_estilos_institucionales(self):
        color_rojo = "#b91c1c"
        color_rojo_hover = "#991b1b"
        color_fondo = "#EDECD1"
        
        self.estilo_app.configure("TFrame", background=color_fondo)
        self.estilo_app.configure("TLabel", background=color_fondo)
        self.estilo_app.configure("TLabelframe", background=color_fondo, bordercolor=color_rojo)
        self.estilo_app.configure("TLabelframe.Label", background=color_fondo, foreground=color_rojo, font=("Segoe UI", 10, "bold"))
        
        self.estilo_app.configure("TButton", background=color_rojo, foreground="#ffffff", bordercolor=color_rojo, font=("Segoe UI", 9, "bold"))
        self.estilo_app.map("TButton", 
            background=[("active", color_rojo_hover), ("pressed", "#7f1d1d")],
            bordercolor=[("active", color_rojo_hover)]
        )

    def _aplicar_cursor_mano(self, widget):
        widget.bind("<Enter>", lambda e: self.winfo_toplevel().config(cursor="hand2"))
        widget.bind("<Leave>", lambda e: self.winfo_toplevel().config(cursor=""))

    def _on_mouse_wheel(self, event):
        """Desplazamiento suave optimizado para eliminar tirones y rayados visuales."""
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

    def _configurar_scroll(self, parent):
        color_fondo = "#EDECD1"
        self.canvas = tk.Canvas(parent, highlightthickness=0, bg=color_fondo)
        self.scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = ttk.Frame(self.canvas, padding=15)
        self.scrollable_frame.configure(style="TFrame")

        def _actualizar_region_scroll(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.scrollable_frame.bind("<Configure>", _actualizar_region_scroll)

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        def _ajustar_ancho_canvas(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)

        self.canvas.bind('<Configure>', _ajustar_ancho_canvas)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)
        self.canvas.bind_all("<Button-4>", self._on_mouse_wheel)
        self.canvas.bind_all("<Button-5>", self._on_mouse_wheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _construir_interfaz(self, contenedor):
        color_fondo = "#EDECD1"
        contenedor.columnconfigure(0, weight=1)

        # ==========================================
        # 1. ENCABEZADO INSTITUCIONAL SIMÉTRICO
        # ==========================================
        header_card = tk.Frame(contenedor, bg="#FFFFFF", padx=25, pady=18, highlightbackground="#d1d5db", highlightthickness=1)
        header_card.pack(fill="x", pady=(0, 15))
        header_card.columnconfigure(0, weight=1)
        header_card.columnconfigure(1, weight=0)

        marco_textos = tk.Frame(header_card, bg="#FFFFFF")
        marco_textos.grid(row=0, column=0, sticky="w")

        tk.Label(
            marco_textos, 
            text="L.N. EVELIA A. DE PIMENTEL", 
            font=("Impact", 28),
            fg="#b91c1c",
            bg="#FFFFFF"
        ).pack(anchor="w")

        tk.Label(
            marco_textos, 
            text="Control de Usuarios y Módulos", 
            font=("Segoe UI", 11, "bold"),
            fg="#1e293b",
            bg="#FFFFFF"
        ).pack(anchor="w", pady=(1, 2))

        tk.Label(
            marco_textos, 
            text="Gestión de credenciales y permisos de acceso por rol institucional", 
            font=("Segoe UI", 9, "italic"),
            fg="#64748b",
            bg="#FFFFFF"
        ).pack(anchor="w", pady=(0, 6))

        # Insignia interactiva sutil UPTMA
        badge_frame = tk.Frame(marco_textos, bg="#F8FAFC", padx=8, pady=4, highlightbackground="#fca5a5", highlightthickness=1)
        badge_frame.pack(anchor="w", pady=(2, 0))
        
        lbl_uptma = tk.Label(
            badge_frame, 
            text="🎓 UPTMA 2026-2027 · Sección 3401", 
            font=("Segoe UI", 8, "bold"),
            fg="#b91c1c",
            bg="#F8FAFC",
            cursor="hand2"
        )
        lbl_uptma.pack(anchor="center")
        
        badge_frame.bind("<Enter>", lambda e: (badge_frame.config(bg="#FEF2F2"), lbl_uptma.config(bg="#FEF2F2")))
        badge_frame.bind("<Leave>", lambda e: (badge_frame.config(bg="#F8FAFC"), lbl_uptma.config(bg="#F8FAFC")))
        badge_frame.bind("<Button-1>", lambda e: self._mostrar_creditos_autores())
        lbl_uptma.bind("<Button-1>", lambda e: self._mostrar_creditos_autores())
        self._aplicar_cursor_mano(badge_frame)
        self._aplicar_cursor_mano(lbl_uptma)

        # Logotipo limpio de 150x150 px
        marco_logo = tk.Frame(header_card, bg="#FFFFFF", width=150, height=150)
        marco_logo.grid(row=0, column=1, sticky="e", padx=(20, 0))
        marco_logo.pack_propagate(False)

        logo_cargado = False
        try:
            rutas_posibles = [
                os.path.join(os.path.dirname(__file__), "logo.png"),
                "logo.png",
                os.path.join(os.path.dirname(__file__), "logon.png"),
                "logon.png"
            ]
            for ruta in rutas_posibles:
                if os.path.exists(ruta):
                    imagen_pil = Image.open(ruta)
                    imagen_pil.thumbnail((140, 140), Image.Resampling.LANCZOS)
                    self.imagen_logo = ImageTk.PhotoImage(imagen_pil)
                    self.imagenes_referencia.append(self.imagen_logo)
                    
                    etiqueta_logo = tk.Label(marco_logo, image=self.imagen_logo, bg="#FFFFFF")
                    etiqueta_logo.pack(expand=True, anchor="center")
                    logo_cargado = True
                    break
        except Exception as e:
            print(f"Error cargando logo: {e}")

        if not logo_cargado:
            tk.Label(marco_logo, text="🏫", font=("Segoe UI", 45), bg="#FFFFFF").pack(expand=True, anchor="center")

        # ==========================================
        # 2. BARRA DE ACCIÓN SUPERIOR LOCAL
        # ==========================================
        acciones_globales = ttk.Frame(contenedor)
        acciones_globales.pack(fill="x", pady=(0, 10))

        self.btn_crear_usuario_toggle = ttk.Button(
            acciones_globales, text="➕ Crear Usuario", command=self._on_alternar_formulario_creacion
        )
        self.btn_crear_usuario_toggle.pack(side="left")
        self._aplicar_cursor_mano(self.btn_crear_usuario_toggle)

        self.btn_volver = ttk.Button(
            acciones_globales, text="⬅️ Volver al Panel", command=self._on_volver_click, bootstyle="secondary"
        )
        self.btn_volver.pack(side="right")
        self._aplicar_cursor_mano(self.btn_volver)

        # ==========================================
        # 3. CONTENEDOR PRINCIPAL DIVIDIDO EN DOS SECCIONES
        # ==========================================
        self.layout_principal = ttk.Frame(contenedor)
        self.layout_principal.pack(fill="both", expand=True, pady=(0, 10))
        self.layout_principal.columnconfigure(0, weight=1)  # Panel izquierdo (Formulario)
        self.layout_principal.columnconfigure(1, weight=1)  # Panel derecho (Listado maestro)

        # PANEL IZQUIERDO: FORMULARIO (Oculto por defecto)
        self.panel_izquierdo = ttk.Frame(self.layout_principal)

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

        botones_frame = ttk.Frame(self.panel_izquierdo)
        botones_frame.pack(fill="x", pady=5)
        botones_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.btn_guardar_usuario = ttk.Button(
            botones_frame, text="💾 Guardar", command=self._on_guardar_usuario
        )
        self.btn_guardar_usuario.grid(row=0, column=0, sticky="ew", padx=2)
        self._aplicar_cursor_mano(self.btn_guardar_usuario)

        self.btn_modificar_usuario = ttk.Button(
            botones_frame, text="✏️ Modificar", command=self._on_modificar_usuario, bootstyle="warning"
        )
        self.btn_modificar_usuario.grid(row=0, column=1, sticky="ew", padx=2)
        self._aplicar_cursor_mano(self.btn_modificar_usuario)

        self.btn_eliminar_usuario = ttk.Button(
            botones_frame, text="🗑️ Eliminar", command=self._on_eliminar_usuario, bootstyle="danger"
        )
        self.btn_eliminar_usuario.grid(row=0, column=2, sticky="ew", padx=2)
        self._aplicar_cursor_mano(self.btn_eliminar_usuario)

        self.btn_limpiar_formulario = ttk.Button(
            botones_frame, text="🧹 Limpiar", command=self._on_limpiar_formulario, bootstyle="secondary"
        )
        self.btn_limpiar_formulario.grid(row=0, column=3, sticky="ew", padx=2)
        self._aplicar_cursor_mano(self.btn_limpiar_formulario)

        # PANEL DERECHO: LISTADO Y CONTROL DE USUARIOS
        self.listado_control_usuario = ttk.Frame(self.layout_principal)
        self.listado_control_usuario.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=0)

        tabla_frame = ttk.LabelFrame(self.listado_control_usuario, text=" Usuarios Registrados (Doble clic para seleccionar y editar) ", padding=12)
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("usuario", "nombre", "correo", "estado")
        self.tree_usuarios = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=14)

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

        self.tree_usuarios.bind("<Double-1>", self._on_seleccionar_usuario_tabla)

        self._cargar_datos_ejemplo()

    def _on_alternar_formulario_creacion(self):
        """Muestra u oculta dinámicamente el panel del formulario al hacer clic en 'Crear Usuario'."""
        if self.formulario_visible:
            self.panel_izquierdo.grid_forget()
            self.listado_control_usuario.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=0)
            self.btn_crear_usuario_toggle.config(text="➕ Crear Usuario")
            self.formulario_visible = False
            self._on_limpiar_formulario()
        else:
            self.listado_control_usuario.grid_forget()
            self.panel_izquierdo.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
            self.listado_control_usuario.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
            self.btn_crear_usuario_toggle.config(text="✖️ Ocultar Formulario")
            self.formulario_visible = True

    def _cargar_datos_ejemplo(self):
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
        nombres = self.entrada_datos_usuario["Nombres:"].get().strip()
        apellidos = self.entrada_datos_usuario["Apellidos:"].get().strip()
        usuario = self.entrada_datos_usuario["Nombre de Usuario:"].get().strip()
        clave = self.entrada_datos_usuario["Clave Asignada:"].get().strip()

        if not nombres or not apellidos or not usuario or not clave:
            messagebox.showwarning("Campos Vacíos", "Por favor complete los campos obligatorios de identificación y credenciales.", parent=self)
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
            messagebox.showinfo("Éxito", f"Usuario '{usuario}' registrado correctamente.", parent=self)
        else:
            item_id = self.tree_usuarios.insert("", "end", values=(usuario, f"{apellidos}, {nombres}", datos_nuevo_usuario["correo"], f"{len(modulos_asignados)} Módulos"))
            if not hasattr(self, "_mapeo_mods_prueba"):
                self._mapeo_mods_prueba = {}
            self._mapeo_mods_prueba[item_id] = modulos_asignados
            messagebox.showinfo("Registro Exitoso", f"El usuario '{usuario}' ha sido creado con éxito.", parent=self)
            self._on_limpiar_formulario()
            self._on_alternar_formulario_creacion()

    def _on_seleccionar_usuario_tabla(self, event):
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            return
        
        item_id = seleccion[0]
        valores = self.tree_usuarios.item(item_id, "values")
        
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

        modulos_del_usuario = getattr(self, "_mapeo_mods_prueba", {}).get(item_id, [])
        for nombre_modulo, variable in self.variables_modulos.items():
            if nombre_modulo in modulos_del_usuario:
                variable.set(True)
            else:
                variable.set(False)

        messagebox.showinfo("Usuario Seleccionado", f"Se han cargado los datos de '{valores[0]}'. Modifique lo que necesite y presione 'Modificar'.", parent=self)

    def _on_modificar_usuario(self):
        if not self.id_usuario_seleccionado:
            messagebox.showwarning("Selección Requerida", "Por favor seleccione un usuario de la tabla haciendo doble clic antes de modificar.", parent=self)
            return

        usuario = self.entrada_datos_usuario["Nombre de Usuario:"].get().strip()
        apellidos = self.entrada_datos_usuario["Apellidos:"].get().strip()
        nombres = self.entrada_datos_usuario["Nombres:"].get().strip()
        correo = self.entrada_datos_usuario["Correo Electrónico:"].get().strip()
        
        modulos_asignados = [modulo for modulo, variable in self.variables_modulos.items() if variable.get()]

        self.tree_usuarios.item(self.id_usuario_seleccionado, values=(usuario, f"{apellidos}, {nombres}", correo, f"{len(modulos_asignados)} Módulos"))
        
        if hasattr(self, "_mapeo_mods_prueba"):
            self._mapeo_mods_prueba[self.id_usuario_seleccionado] = modulos_asignados

        messagebox.showinfo("Modificación Exitosa", f"Los datos y permisos del usuario '{usuario}' han sido actualizados.", parent=self)
        self._on_limpiar_formulario()
        self._on_alternar_formulario_creacion()

    def _on_eliminar_usuario(self):
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            messagebox.showwarning("Selección Requerida", "Por favor seleccione el usuario que desea eliminar de la tabla.", parent=self)
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
            messagebox.showinfo("Usuario Eliminado", f"El usuario '{usuario}' fue dado de baja con éxito.", parent=self)
            self._on_limpiar_formulario()
            if self.formulario_visible:
                self._on_alternar_formulario_creacion()

    def _on_limpiar_formulario(self):
        for entrada in self.entrada_datos_usuario.values():
            entrada.delete(0, tk.END)
        for variable in self.variables_modulos.values():
            variable.set(False)
        self.id_usuario_seleccionado = None

    def _mostrar_creditos_autores(self):
        ventana_creditos = tk.Toplevel(self)
        ventana_creditos.title("Créditos del Sistema - UPTMA")
        ventana_creditos.geometry("480x440")
        ventana_creditos.configure(bg="#EDECD1")
        ventana_creditos.resizable(False, False)
        ventana_creditos.transient(self)
        ventana_creditos.grab_set()

        main_frame = tk.Frame(ventana_creditos, bg="#FFFFFF", padx=20, pady=20, highlightbackground="#b91c1c", highlightthickness=2)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(main_frame, text="🏫 UPTMA 2026-2027 · Sección 3401", font=("Segoe UI", 12, "bold"), fg="#b91c1c", bg="#FFFFFF").pack(anchor="center", pady=(0, 12))
        tk.Label(main_frame, text="AUTORES DEL PROYECTO:", font=("Segoe UI", 9, "bold"), fg="#475569", bg="#FFFFFF").pack(anchor="w", pady=(0, 4))

        autores = ["• Bravo, Jhordan", "• Chacín, Luis", "• Gonzales, Rafael", "• Torregroza, Josemith", "• Cordoba, Jose"]
        for autor in autores:
            tk.Label(main_frame, text=autor, font=("Segoe UI", 9), fg="#1e293b", bg="#FFFFFF").pack(anchor="w", padx=10, pady=1)

        dev_frame = tk.Frame(main_frame, bg="#FEF2F2", padx=12, pady=10, highlightbackground="#fca5a5", highlightthickness=1)
        dev_frame.pack(fill="x", pady=(15, 10))

        tk.Label(dev_frame, text="💻 PROGRAMADOR, DISEÑADOR Y DESARROLLADOR", font=("Segoe UI", 9, "bold"), fg="#b91c1c", bg="#FEF2F2").pack(anchor="w")
        tk.Label(dev_frame, text="Moisfer Enrique Urdaneta Barrios", font=("Segoe UI", 10, "bold"), fg="#0f172a", bg="#FEF2F2").pack(anchor="w", pady=(2, 2))
        tk.Label(dev_frame, text="GitHub: https://github.com/MoisferIT\nCorreo: moisferit.dev@gmail.com", font=("Segoe UI", 8, "italic"), fg="#334155", bg="#FEF2F2", justify="left").pack(anchor="w")

        btn_cerrar = ttk.Button(main_frame, text="Cerrar", command=ventana_creditos.destroy, bootstyle="danger")
        btn_cerrar.pack(anchor="center", pady=(8, 0))
        self._aplicar_cursor_mano(btn_cerrar)

    def _on_volver_click(self):
        if messagebox.askyesno("Volver al Dashboard", "¿Desea regresar al panel principal?", parent=self):
            self.master.destroy()

if __name__ == "__main__":
    root = ttk.Window(title="Control de roles 2026 - Gestión de Usuarios y Accesos", themename="flatly", size=(1150, 720))
    root.configure(bg="#EDECD1")
    root.minsize(850, 580)
    
    app = VistaUsuariosRoles(parent=root, controlador=None)
    app.pack(fill="both", expand=True, padx=12, pady=12)
        
    root.mainloop()