import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.style import Style

class VistaAsignacionProfesores(ttk.Frame):
    """Módulo de Interfaz Gráfica para la asignación y consulta de cátedras, años y secciones de docentes con pestañas de navegación directa."""

    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self.imagenes_referencia = []
        
        # Aplicar el estilo institucional unificado con fondo #EDECD1
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
            text="Asignación y Consulta de Cátedras y Secciones", 
            font=("Segoe UI", 11, "bold"),
            fg="#1e293b",
            bg="#FFFFFF"
        ).pack(anchor="w", pady=(1, 2))

        tk.Label(
            marco_textos, 
            text="Gestión de materias a cargo, años escolares y listado filtrado de docentes activos", 
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
        # 2. BOTONES DE SELECCIÓN DE VISTA (OPCIONES)
        # ==========================================
        opciones_frame = ttk.Frame(contenedor)
        opciones_frame.pack(fill="x", pady=(0, 15))

        self.btn_opcion_consulta = ttk.Button(
            opciones_frame, text="📋 Consultar Listado y Asignaciones", 
            command=lambda: self._cambiar_pestana("consulta")
        )
        self.btn_opcion_consulta.pack(side="left", padx=(0, 8), ipadx=5, ipady=3)
        self._aplicar_cursor_mano(self.btn_opcion_consulta)

        self.btn_opcion_asignacion = ttk.Button(
            opciones_frame, text="➕ Asignar Materia a Docente", 
            command=lambda: self._cambiar_pestana("asignacion"),
            bootstyle="secondary"
        )
        self.btn_opcion_asignacion.pack(side="left", padx=8, ipadx=5, ipady=3)
        self._aplicar_cursor_mano(self.btn_opcion_asignacion)

        # Contenedor dinámico donde alternan las secciones
        self.contenedor_dinamico = ttk.Frame(contenedor)
        self.contenedor_dinamico.pack(fill="both", expand=True, pady=(0, 10))
        self.contenedor_dinamico.columnconfigure(0, weight=1)

        # Construir ambas secciones internas
        self._construir_seccion_asignacion(self.contenedor_dinamico)
        self._construir_seccion_consulta(self.contenedor_dinamico)

        # Mostrar por defecto la sección de consulta
        self._cambiar_pestana("consulta")

        # ==========================================
        # 3. PANEL INFERIOR DE ACCIONES
        # ==========================================
        panel_acciones = ttk.Frame(contenedor)
        panel_acciones.pack(fill="x", pady=(5, 10))

        btn_volver = ttk.Button(panel_acciones, text="⬅️ Volver al Panel", command=self._on_volver_click, bootstyle="secondary")
        btn_volver.pack(side="right", padx=5, ipady=3)
        self._aplicar_cursor_mano(btn_volver)

    def _construir_seccion_asignacion(self, parent):
        self.marco_asignacion = ttk.LabelFrame(parent, text=" Asignar Cátedra, Año y Sección a Docente ", padding=15)
        self.marco_asignacion.columnconfigure(1, weight=1)
        self.marco_asignacion.columnconfigure(3, weight=1)

        # Docente
        ttk.Label(self.marco_asignacion, text="Seleccionar Docente:", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", pady=8, padx=5)
        self.combo_docente = ttk.Combobox(self.marco_asignacion, values=["Prof. Carlos Mendoza (V-15.432.111)", "Prof. Ana Pérez (V-18.999.888)", "Prof. José Rodríguez (V-12.333.444)"], state="readonly")
        self.combo_docente.grid(row=0, column=1, sticky="ew", pady=8, padx=5)
        self.combo_docente.set("Prof. Carlos Mendoza (V-15.432.111)")

        # Materia / Cátedra
        ttk.Label(self.marco_asignacion, text="Asignatura / Cátedra:", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="w", pady=8, padx=5)
        self.combo_materia = ttk.Combobox(self.marco_asignacion, values=["Matemáticas", "Castellano y Literatura", "Física", "Química", "Biología", "Historia de Venezuela", "Inglés"], state="readonly")
        self.combo_materia.grid(row=0, column=3, sticky="ew", pady=8, padx=5)
        self.combo_materia.set("Matemáticas")

        # Año / Grado
        ttk.Label(self.marco_asignacion, text="Año Escolar:", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w", pady=8, padx=5)
        self.combo_anio = ttk.Combobox(self.marco_asignacion, values=["1er Año", "2do Año", "3er Año", "4to Año", "5to Año"], state="readonly")
        self.combo_anio.grid(row=1, column=1, sticky="ew", pady=8, padx=5)
        self.combo_anio.set("1er Año")

        # Sección
        ttk.Label(self.marco_asignacion, text="Sección:", font=("Segoe UI", 9, "bold")).grid(row=1, column=2, sticky="w", pady=8, padx=5)
        letras_az = [chr(i) for i in range(ord('A'), ord('F') + 1)]
        self.combo_seccion = ttk.Combobox(self.marco_asignacion, values=letras_az, state="readonly")
        self.combo_seccion.grid(row=1, column=3, sticky="ew", pady=8, padx=5)
        self.combo_seccion.set("A")

        # Botón de Guardar Asignación
        btn_guardar_asig = ttk.Button(self.marco_asignacion, text="💾 Guardar Asignación Académica", command=self._on_guardar_asignacion)
        btn_guardar_asig.grid(row=2, column=0, columnspan=4, sticky="e", pady=(12, 0))
        self._aplicar_cursor_mano(btn_guardar_asig)

    def _construir_seccion_consulta(self, parent):
        self.marco_consulta = ttk.LabelFrame(parent, text=" Consulta y Filtrado de Docentes Asignados ", padding=15)
        self.marco_consulta.columnconfigure(1, weight=1)

        # Filtros
        barra_filtros = ttk.Frame(self.marco_consulta)
        barra_filtros.pack(fill="x", pady=(0, 10))

        ttk.Label(barra_filtros, text="Filtrar por Año:", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 5))
        self.filtro_anio = ttk.Combobox(barra_filtros, values=["Todos", "1er Año", "2do Año", "3er Año", "4to Año", "5to Año"], state="readonly", width=15)
        self.filtro_anio.pack(side="left", padx=(0, 15))
        self.filtro_anio.set("Todos")
        self.filtro_anio.bind("<<ComboboxSelected>>", lambda e: self._aplicar_filtros())

        ttk.Label(barra_filtros, text="Buscar Docente/Materia:", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 5))
        self.filtro_busqueda = ttk.Entry(barra_filtros, width=25)
        self.filtro_busqueda.pack(side="left", padx=(0, 10))
        self.filtro_busqueda.bind("<KeyRelease>", lambda e: self._aplicar_filtros())

        btn_filtrar = ttk.Button(barra_filtros, text="🔍 Buscar", command=self._aplicar_filtros, bootstyle="secondary")
        btn_filtrar.pack(side="left")
        self._aplicar_cursor_mano(btn_filtrar)

        # Tabla (Treeview) de Asignaciones
        columns = ("docente", "materia", "anio", "seccion")
        self.tabla = ttk.Treeview(self.marco_consulta, columns=columns, show="headings", height=10)
        
        self.tabla.heading("docente", text="Docente Titular")
        self.tabla.heading("materia", text="Asignatura / Cátedra")
        self.tabla.heading("anio", text="Año")
        self.tabla.heading("seccion", text="Sección")

        self.tabla.column("docente", width=260, anchor="w")
        self.tabla.column("materia", width=200, anchor="w")
        self.tabla.column("anio", width=100, anchor="center")
        self.tabla.column("seccion", width=80, anchor="center")

        self.tabla.pack(fill="both", expand=True, pady=(5, 5))

        # Datos de prueba iniciales en la tabla
        self.datos_maestros = [
            ("Prof. Carlos Mendoza (V-15.432.111)", "Matemáticas", "1er Año", "A"),
            ("Prof. Carlos Mendoza (V-15.432.111)", "Física", "4to Año", "B"),
            ("Prof. Ana Pérez (V-18.999.888)", "Castellano y Literatura", "2do Año", "A"),
            ("Prof. José Rodríguez (V-12.333.444)", "Biología", "3er Año", "C")
        ]
        self._actualizar_tabla(self.datos_maestros)

    def _cambiar_pestana(self, tipo):
        """Alterna dinámicamente entre la sección de consulta y la sección de asignación."""
        if tipo == "consulta":
            self.marco_asignacion.pack_forget()
            self.marco_consulta.pack(fill="both", expand=True)
            self.btn_opcion_consulta.configure(bootstyle="primary")
            self.btn_opcion_asignacion.configure(bootstyle="secondary")
        else:
            self.marco_consulta.pack_forget()
            self.marco_asignacion.pack(fill="x", expand=True)
            self.btn_opcion_asignacion.configure(bootstyle="primary")
            self.btn_opcion_consulta.configure(bootstyle="secondary")

    def _actualizar_tabla(self, datos):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for row in datos:
            self.tabla.insert("", "end", values=row)

    def _aplicar_filtros(self):
        anio_seleccionado = self.filtro_anio.get()
        texto_busqueda = self.filtro_busqueda.get().strip().lower()

        resultados_filtrados = []
        for row in self.datos_maestros:
            docente, materia, anio, seccion = row
            match_anio = (anio_seleccionado == "Todos" or anio == anio_seleccionado)
            match_texto = (texto_busqueda in docente.lower() or texto_busqueda in materia.lower())

            if match_anio and match_texto:
                resultados_filtrados.append(row)

        self._actualizar_tabla(resultados_filtrados)

    def _on_guardar_asignacion(self):
        docente = self.combo_docente.get()
        materia = self.combo_materia.get()
        anio = self.combo_anio.get()
        seccion = self.combo_seccion.get()

        nuevo_registro = (docente, materia, anio, seccion)
        self.datos_maestros.append(nuevo_registro)
        self._aplicar_filtros()

        messagebox.showinfo("Asignación Exitosa", f"Se ha asignado correctamente la cátedra '{materia}' ({anio} Secc. {seccion}) al docente.", parent=self)
        self._cambiar_pestana("consulta") # Regresar automáticamente a ver la tabla tras guardar

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
        if messagebox.askyesno("Volver", "¿Desea regresar al panel principal?", parent=self):
            self.master.destroy()

if __name__ == "__main__":
    root = ttk.Window(title="L.N. Evelia A. de Pimentel - Asignación y Consulta de Docentes", themename="flatly", size=(1150, 720))
    root.configure(bg="#EDECD1")
    root.minsize(850, 580)
    
    app = VistaAsignacionProfesores(parent=root, controlador=None)
    app.pack(fill="both", expand=True, padx=12, pady=12)
        
    root.mainloop()