import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.style import Style

# Intentamos cargar tkcalendar para el widget gráfico del calendario
try:
    from tkcalendar import DateEntry
    EXISTS_TKCALENDAR = True
except ImportError:
    EXISTS_TKCALENDAR = False

class VistaAsistenciaRegistro(ttk.Frame):
    """Módulo de asistencia interactivo, responsivo y adaptado con alto contraste visual (🟢🔴🟡) y atajos de teclado."""

    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self.estudiantes_datos = []
        
        self.cursor_fila = 0
        self.cursor_col = 0
        
        # Configuración del tema y paleta institucional unificada
        self.estilo_app = Style(theme="flatly")
        self._configurar_estilos_institucionales()
        self._construir_interfaz(self)

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

    def _aplicar_cursor_mano(self, boton):
        boton.bind("<Enter>", lambda e: self.winfo_toplevel().config(cursor="hand2"))
        boton.bind("<Leave>", lambda e: self.winfo_toplevel().config(cursor=""))

    def _construir_interfaz(self, contenedor):
        color_fondo = "#EDECD1"
        contenedor.configure(style="TFrame")
        
        # Configuración de expansión responsiva
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(3, weight=1)  # La tabla se expandirá vertical y horizontalmente

        # 1. Encabezado simétrico y responsivo (2 columnas)
        marco_encabezado = ttk.Frame(contenedor, padding=(20, 10, 20, 2))
        marco_encabezado.grid(row=0, column=0, sticky="ew")
        marco_encabezado.columnconfigure(0, weight=1)
        marco_encabezado.columnconfigure(1, weight=0)

        marco_titulos = ttk.Frame(marco_encabezado)
        marco_titulos.grid(row=0, column=0, sticky="w")

        etiqueta_titulo = tk.Label(
            marco_titulos, 
            text="Control y Registro de Asistencia", 
            font=("Segoe UI", 20, "bold"),
            fg="#b91c1c",
            bg=color_fondo
        )
        etiqueta_titulo.pack(anchor="w")

        etiqueta_subtitulo = tk.Label(
            marco_titulos, 
            text="Planilla Institucional - Matriz Interactiva de Asistencia", 
            font=("Segoe UI", 9, "italic"),
            fg="#64748b",
            bg=color_fondo
        )
        etiqueta_subtitulo.pack(anchor="w", pady=(1, 0))

        marco_logo = ttk.Frame(marco_encabezado, width=85, height=85)
        marco_logo.grid(row=0, column=1, sticky="e", padx=(10, 0))
        marco_logo.pack_propagate(False)

        try:
            ruta_logo = os.path.join(os.path.dirname(__file__), "logon.png")
            if os.path.exists(ruta_logo):
                imagen_pil = Image.open(ruta_logo)
                imagen_pil.thumbnail((75, 75), Image.Resampling.LANCZOS)
                self.imagen_logo = ImageTk.PhotoImage(imagen_pil)
                
                etiqueta_logo = tk.Label(marco_logo, image=self.imagen_logo, bg=color_fondo)
                etiqueta_logo.pack(expand=True, anchor="center")
        except Exception as error_logo:
            print(f"No se pudo cargar el logo: {error_logo}")

        # 2. Panel de Filtros Responsivo
        filtros_frame = ttk.LabelFrame(contenedor, text=" Parámetros de Cátedra, Fecha y Filtrado ", padding=10)
        filtros_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(4, 6))
        
        # Distribuimos peso flexible entre controles
        for i in range(11):
            filtros_frame.columnconfigure(i, weight=0)
        filtros_frame.columnconfigure(10, weight=1)

        ttk.Label(filtros_frame, text="Año:", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=3, pady=4)
        self.combo_anio = ttk.Combobox(filtros_frame, values=["1er Año", "2do Año", "3er Año", "4to Año", "5to Año"], state="readonly", width=10)
        self.combo_anio.grid(row=0, column=1, sticky="w", padx=3, pady=4)
        self.combo_anio.set("1er Año")

        ttk.Label(filtros_frame, text="Sección:", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="w", padx=(6, 3), pady=4)
        letras_az = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        self.combo_seccion = ttk.Combobox(filtros_frame, values=letras_az, state="readonly", width=4)
        self.combo_seccion.grid(row=0, column=3, sticky="w", padx=3, pady=4)
        self.combo_seccion.set("A")

        ttk.Label(filtros_frame, text="Materia:", font=("Segoe UI", 9, "bold")).grid(row=0, column=4, sticky="w", padx=(6, 3), pady=4)
        self.combo_materia = ttk.Combobox(filtros_frame, values=["Matemáticas", "Castellano", "Inglés", "Biología", "Física", "Química"], state="readonly", width=13)
        self.combo_materia.grid(row=0, column=5, sticky="w", padx=3, pady=4)
        self.combo_materia.set("Matemáticas")

        ttk.Label(filtros_frame, text="Fecha:", font=("Segoe UI", 9, "bold")).grid(row=0, column=6, sticky="w", padx=(6, 3), pady=4)
        if EXISTS_TKCALENDAR:
            self.entrada_fecha = DateEntry(
                filtros_frame, width=10, background='#b91c1c', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy', cursor="hand2", locale="es_VE"
            )
            self.entrada_fecha.set_date(datetime.now())
        else:
            self.entrada_fecha = ttk.Entry(filtros_frame, width=10)
            self.entrada_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entrada_fecha.grid(row=0, column=7, sticky="w", padx=3, pady=4)

        self.btn_cargar = ttk.Button(filtros_frame, text="🔍 Filtrar", command=self._on_cargar_asistencias)
        self.btn_cargar.grid(row=0, column=8, padx=(8, 3), pady=4)
        self._aplicar_cursor_mano(self.btn_cargar)

        ttk.Label(filtros_frame, text="Buscar:", font=("Segoe UI", 8, "italic")).grid(row=0, column=9, sticky="e", padx=(8, 2), pady=4)
        self.var_busqueda = tk.StringVar()
        self.var_busqueda.trace_add("write", lambda *args: self._actualizar_tabla())
        self.entrada_busqueda = ttk.Entry(filtros_frame, textvariable=self.var_busqueda, width=14)
        self.entrada_busqueda.grid(row=0, column=10, sticky="w", padx=2, pady=4)

        # 3. Leyenda informativa
        leyenda_frame = ttk.Frame(contenedor)
        leyenda_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 4))
        tk.Label(
            leyenda_frame, 
            text="💡 [ ↑ ↓ ← → ] Mover cursor | [ Enter ] Confirmar estatus y desmarcar fila | Clic directo habilitado", 
            font=("Segoe UI", 8, "italic"), 
            fg="#475569",
            bg=color_fondo
        ).pack(side="left")

        # 4. Tabla de Planilla adaptativa con fondo blanco brillante para máxima visibilidad de los colores
        tabla_container = ttk.LabelFrame(contenedor, text=" Planilla Interactiva de Asistencia ", padding=8)
        tabla_container.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 10))
        tabla_container.columnconfigure(0, weight=1)
        tabla_container.rowconfigure(0, weight=1)

        columnas = ("nro", "cedula", "nombre", "presente", "ausente", "justificado", "motivo")
        self.tree_matriz = ttk.Treeview(tabla_container, columns=columnas, show="headings", height=10)

        self.tree_matriz.heading("nro", text="N°")
        self.tree_matriz.heading("cedula", text="CÉDULA")
        self.tree_matriz.heading("nombre", text="NOMBRE Y APELLIDO")
        self.tree_matriz.heading("presente", text="🟢 PRESENTE")
        self.tree_matriz.heading("ausente", text="🔴 AUSENTE")
        self.tree_matriz.heading("justificado", text="🟡 JUSTIFICADO")
        self.tree_matriz.heading("motivo", text="MOTIVO / OBSERVACIÓN")

        self.tree_matriz.column("nro", width=40, anchor="center")
        self.tree_matriz.column("cedula", width=105, anchor="center")
        self.tree_matriz.column("nombre", width=280, anchor="w")
        self.tree_matriz.column("presente", width=110, anchor="center")
        self.tree_matriz.column("ausente", width=110, anchor="center")
        self.tree_matriz.column("justificado", width=115, anchor="center")
        self.tree_matriz.column("motivo", width=200, anchor="w")

        estilo_arbol = ttk.Style()
        estilo_arbol.configure("Treeview", rowheight=32, font=("Segoe UI", 10, "bold"), background="#FFFFFF", fieldbackground="#FFFFFF")
        estilo_arbol.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

        self.tree_matriz.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tabla_container, orient="vertical", command=self.tree_matriz.yview)
        self.tree_matriz.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Vincular clics y eventos de navegación por teclado
        self.tree_matriz.bind("<Button-1>", self._on_clic_celda_matriz)
        self.tree_matriz.bind("<Return>", self._on_enter_teclado)
        self.tree_matriz.bind("<Up>", lambda e: self._mover_cursor_teclado(-1, 0))
        self.tree_matriz.bind("<Down>", lambda e: self._mover_cursor_teclado(1, 0))
        self.tree_matriz.bind("<Left>", lambda e: self._mover_cursor_teclado(0, -1))
        self.tree_matriz.bind("<Right>", lambda e: self._mover_cursor_teclado(0, 1))

        # 5. Botones inferiores institucionales (Visibles en todo momento)
        inferior_frame = ttk.Frame(contenedor)
        inferior_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 10))

        self.btn_guardar = ttk.Button(inferior_frame, text="💾 Guardar Asistencia", command=self._on_guardar_db)
        self.btn_guardar.pack(side="left", padx=2)
        self._aplicar_cursor_mano(self.btn_guardar)

        self.btn_exportar = ttk.Button(inferior_frame, text="🖨️ Exportar Planilla en PDF", bootstyle="secondary", command=self._on_exportar_pdf)
        self.btn_exportar.pack(side="left", padx=8)
        self._aplicar_cursor_mano(self.btn_exportar)

        self._inicializar_datos_prueba()

    def _inicializar_datos_prueba(self):
        self.estudiantes_datos = [
            {"nro": "1", "cedula": "V-33456789", "nombre": "Pérez González, Alejandro", "estatus": "Presente", "motivo": "-"},
            {"nro": "2", "cedula": "V-33987123", "nombre": "Rodríguez Silva, María Gabriela", "estatus": "Presente", "motivo": "-"},
            {"nro": "3", "cedula": "V-34112233", "nombre": "Gómez Blanco, Jesús David", "estatus": "Justificado", "motivo": "Cita médica odontológica"},
            {"nro": "4", "cedula": "V-34556677", "nombre": "Martínez López, Valeria Sofía", "estatus": "Ausente", "motivo": "-"},
            {"nro": "5", "cedula": "V-35123456", "nombre": "Rojas Morales, Carlos Eduardo", "estatus": "Presente", "motivo": "-"}
        ]
        self._actualizar_tabla()

    def _actualizar_tabla(self, mantener_seleccion=True):
        items_actuales = self.tree_matriz.get_children()
        for item in items_actuales:
            self.tree_matriz.delete(item)

        texto_busqueda = self.var_busqueda.get().strip().lower()
        estudiantes_filtrados = [
            est for est in self.estudiantes_datos 
            if not texto_busqueda or texto_busqueda in est["cedula"].lower() or texto_busqueda in est["nombre"].lower()
        ]

        for idx, est in enumerate(estudiantes_filtrados):
            es_foco_fila = (idx == self.cursor_fila)

            # Cajas de selección limpias con indicadores bien definidos
            p_sel = "[ ▶ ]" if (es_foco_fila and self.cursor_col == 0) else "[     ]"
            a_sel = "[ ▶ ]" if (es_foco_fila and self.cursor_col == 1) else "[     ]"
            j_sel = "[ ▶ ]" if (es_foco_fila and self.cursor_col == 2) else "[     ]"

            box_presente = "[ 🟢 ]" if est['estatus'] == 'Presente' else p_sel
            box_ausente = "[ 🔴 ]" if est['estatus'] == 'Ausente' else a_sel
            box_justificado = "[ 🟡 ]" if est['estatus'] == 'Justificado' else j_sel

            self.tree_matriz.insert(
                "", "end", 
                values=(est["nro"], est["cedula"], est["nombre"], box_presente, box_ausente, box_justificado, est["motivo"])
            )
        
        nuevos_items = self.tree_matriz.get_children()
        if nuevos_items and self.cursor_fila < len(nuevos_items):
            if mantener_seleccion:
                self.tree_matriz.selection_set(nuevos_items[self.cursor_fila])
                self.tree_matriz.focus(nuevos_items[self.cursor_fila])
            else:
                self.tree_matriz.selection_remove(self.tree_matriz.selection())

    def _on_clic_celda_matriz(self, event):
        region = self.tree_matriz.identify("region", event.x, event.y)
        if region != "cell":
            return
        
        columna_id = self.tree_matriz.identify_column(event.x)
        item_id = self.tree_matriz.identify_row(event.y)
        if not item_id:
            return
        
        todos_items = self.tree_matriz.get_children()
        try:
            self.cursor_fila = todos_items.index(item_id)
        except ValueError:
            pass

        if columna_id == "#4":
            self.cursor_col = 0
            self._confirmar_estatus_actual(quitar_seleccion=True)
        elif columna_id == "#5":
            self.cursor_col = 1
            self._confirmar_estatus_actual(quitar_seleccion=True)
        elif columna_id == "#6":
            self.cursor_col = 2
            self._confirmar_estatus_actual(quitar_seleccion=True)

    def _mover_cursor_teclado(self, delta_fila, delta_col):
        todos_items = self.tree_matriz.get_children()
        if not todos_items:
            return

        self.cursor_fila = max(0, min(self.cursor_fila + delta_fila, len(todos_items) - 1))
        self.cursor_col = max(0, min(self.cursor_col + delta_col, 2))
        
        self._actualizar_tabla(mantener_seleccion=True)
        return "break"

    def _on_enter_teclado(self, event):
        self._confirmar_estatus_actual(quitar_seleccion=True)
        
        todos_items = self.tree_matriz.get_children()
        if self.cursor_fila + 1 < len(todos_items):
            self.cursor_fila += 1
            self._actualizar_tabla(mantener_seleccion=True)
            
        return "break"

    def _confirmar_estatus_actual(self, quitar_seleccion=False):
        texto_busqueda = self.var_busqueda.get().strip().lower()
        estudiantes_filtrados = [
            est for est in self.estudiantes_datos 
            if not texto_busqueda or texto_busqueda in est["cedula"].lower() or texto_busqueda in est["nombre"].lower()
        ]

        if not estudiantes_filtrados or self.cursor_fila >= len(estudiantes_filtrados):
            return

        estudiante_objetivo = estudiantes_filtrados[self.cursor_fila]

        if self.cursor_col == 0:
            estudiante_objetivo["estatus"] = "Presente"
            estudiante_objetivo["motivo"] = "-"
        elif self.cursor_col == 1:
            estudiante_objetivo["estatus"] = "Ausente"
            estudiante_objetivo["motivo"] = "-"
        elif self.cursor_col == 2:
            motivo_ingresado = simpledialog.askstring("Motivo de Inasistencia", f"Ingrese el motivo de la justificación para {estudiante_objetivo['nombre']}:", parent=self)
            estudiante_objetivo["estatus"] = "Justificado"
            estudiante_objetivo["motivo"] = motivo_ingresado.strip() if motivo_ingresado else "Justificado sin descripción"

        self._actualizar_tabla(mantener_seleccion=not quitar_seleccion)

    def _on_cargar_asistencias(self):
        anio = self.combo_anio.get()
        seccion = self.combo_seccion.get()
        materia = self.combo_materia.get()
        fecha = self.entrada_fecha.get() if hasattr(self.entrada_fecha, 'get') else self.entrada_fecha.get_date().strftime("%d/%m/%Y")
        
        messagebox.showinfo("Planilla Filtrada", f"Cargando alumnos para:\n{anio} Sección '{seccion}' - {materia}\nFecha: {fecha}")
        self.cursor_fila = 0
        self.cursor_col = 0
        self._actualizar_tabla(mantener_seleccion=True)

    def _on_guardar_db(self):
        messagebox.showinfo("Guardado Exitoso", "Los cambios en la planilla interactiva han sido guardados correctamente.")

    def _on_exportar_pdf(self):
        messagebox.showinfo("Exportar", "Generando reporte de asistencia en PDF...")

if __name__ == "__main__":
    raiz_aplicacion = ttk.Window(title="L.N. Evelia A. de Pimentel - Registro de Asistencia", themename="flatly", size=(1250, 720))
    raiz_aplicacion.configure(bg="#EDECD1")
    
    app = VistaAsistenciaRegistro(parent=raiz_aplicacion, controlador=None)
    app.pack(fill="both", expand=True, padx=10, pady=10)
    raiz_aplicacion.mainloop()