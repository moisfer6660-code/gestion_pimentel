import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.style import Style

# Intentamos importar tkcalendar para el selector gráfico interactivo de fechas
try:
    from tkcalendar import DateEntry
    EXISTS_TKCALENDAR = True
except ImportError:
    EXISTS_TKCALENDAR = False

class VistaAsistenciaEstadistica(ttk.Frame):
    """Módulo profesional de consulta, auditoría y estadísticas de asistencia escolar con diseño institucional unificado."""

    def __init__(self, contenedor_principal, controlador_externo=None):
        super().__init__(contenedor_principal)
        self.controlador_externo = controlador_externo
        
        # Configuración del tema y paleta institucional unificada
        self.estilo_app = Style(theme="flatly")
        self._configurar_estilos_institucionales()
        self._construir_interfaz(self)

    def _configurar_estilos_institucionales(self):
        """Aplica la paleta con fondo #F3F3E0 y acentos en rojo institucional (#b91c1c)."""
        color_rojo = "#b91c1c"
        color_rojo_hover = "#991b1b"
        color_fondo = "#F3F3E0"
        
        # Estilos globales para eliminar fondos blancos o grises
        self.estilo_app.configure("TFrame", background=color_fondo)
        self.estilo_app.configure("TLabel", background=color_fondo)
        self.estilo_app.configure("TLabelframe", background=color_fondo, bordercolor=color_rojo)
        self.estilo_app.configure("TLabelframe.Label", background=color_fondo, foreground=color_rojo, font=("Segoe UI", 10, "bold"))
        
        # Botones unificados con profundidad y estética profesional
        self.estilo_app.configure("TButton", background=color_rojo, foreground="#ffffff", bordercolor=color_rojo, font=("Segoe UI", 9, "bold"))
        self.estilo_app.map("TButton", 
            background=[("active", color_rojo_hover), ("pressed", "#7f1d1d")],
            bordercolor=[("active", color_rojo_hover)]
        )

    def _aplicar_cursor_mano(self, boton):
        """Asigna el cambio de cursor a formato de mano interactiva al pasar por encima."""
        boton.bind("<Enter>", lambda e: self.winfo_toplevel().config(cursor="hand2"))
        boton.bind("<Leave>", lambda e: self.winfo_toplevel().config(cursor=""))

    def _construir_interfaz(self, contenedor):
        color_fondo = "#F3F3E0"
        contenedor.configure(style="TFrame")
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(3, weight=1)

        # 1. Encabezado simétrico con Grid de 2 columnas (Títulos a la izquierda, Logo a la derecha)
        marco_encabezado = ttk.Frame(contenedor, padding=(20, 15, 20, 5))
        marco_encabezado.grid(row=0, column=0, sticky="ew")
        marco_encabezado.columnconfigure(0, weight=1)
        marco_encabezado.columnconfigure(1, weight=0)

        marco_titulos = ttk.Frame(marco_encabezado)
        marco_titulos.grid(row=0, column=0, sticky="w")

        etiqueta_titulo = tk.Label(
            marco_titulos, 
            text="Control y Estadísticas de Asistencia", 
            font=("Segoe UI", 22, "bold"),
            fg="#b91c1c",
            bg=color_fondo
        )
        etiqueta_titulo.pack(anchor="w")

        etiqueta_subtitulo = tk.Label(
            marco_titulos, 
            text="Módulo profesional de consulta, auditoría y estadísticas escolares", 
            font=("Segoe UI", 10, "italic"),
            fg="#64748b",
            bg=color_fondo
        )
        etiqueta_subtitulo.pack(anchor="w", pady=(1, 0))

        # Marco flotante protegido para el logotipo institucional
        marco_logo = ttk.Frame(marco_encabezado, width=110, height=110)
        marco_logo.grid(row=0, column=1, sticky="e", padx=(10, 0))
        marco_logo.pack_propagate(False)

        try:
            ruta_logo = os.path.join(os.path.dirname(__file__), "logon.png")
            if os.path.exists(ruta_logo):
                imagen_pil = Image.open(ruta_logo)
                imagen_pil.thumbnail((100, 100), Image.Resampling.LANCZOS)
                self.imagen_logo = ImageTk.PhotoImage(imagen_pil)
                
                etiqueta_logo = tk.Label(marco_logo, image=self.imagen_logo, bg=color_fondo)
                etiqueta_logo.pack(expand=True, anchor="center")
        except Exception as error_logo:
            print(f"No se pudo cargar el logo: {error_logo}")

        # ==========================================
        # 2. PANEL DE FILTRADO (AÑO, SECCIÓN, CÁTEDRA, FECHAS)
        # ==========================================
        panel_filtros = ttk.LabelFrame(contenedor, text=" Panel de Control y Filtros Académicos ", padding=12)
        panel_filtros.grid(row=1, column=0, sticky="ew", padx=20, pady=(4, 8))
        panel_filtros.columnconfigure(1, weight=1)
        panel_filtros.columnconfigure(3, weight=1)
        panel_filtros.columnconfigure(5, weight=1)

        # Fila 0: Año, Sección y Cátedra
        ttk.Label(panel_filtros, text="Año Escolar:", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=6)
        self.combo_ano = ttk.Combobox(panel_filtros, values=["1er Año", "2do Año", "3er Año", "4to Año", "5to Año"], state="readonly", width=14)
        self.combo_ano.grid(row=0, column=1, sticky="ew", padx=5, pady=6)
        self.combo_ano.set("1er Año")
        self.combo_ano.bind("<<ComboboxSelected>>", self._actualizar_materias)

        ttk.Label(panel_filtros, text="Sección:", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="w", padx=(15, 5), pady=6)
        self.combo_seccion = ttk.Combobox(panel_filtros, values=["Sección A", "Sección B", "Sección Única"], state="readonly", width=14)
        self.combo_seccion.grid(row=0, column=3, sticky="ew", padx=5, pady=6)
        self.combo_seccion.set("Sección A")

        ttk.Label(panel_filtros, text="Cátedra:", font=("Segoe UI", 9, "bold")).grid(row=0, column=4, sticky="w", padx=(15, 5), pady=6)
        self.combo_materia = ttk.Combobox(panel_filtros, values=["Matemáticas I", "Castellano y Literatura", "Inglés", "Educación Física"], state="readonly", width=18)
        self.combo_materia.grid(row=0, column=5, sticky="ew", padx=5, pady=6)
        self.combo_materia.set("Matemáticas I")

        # Fila 1: Rango de Fechas y Botones de Consulta
        ttk.Label(panel_filtros, text="Desde:", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=6)
        if EXISTS_TKCALENDAR:
            self.entry_desde = DateEntry(panel_filtros, width=12, background='#1f2937', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy', cursor="hand2", locale="es_VE")
            self.entry_desde.set_date("01/10/2026")
        else:
            self.entry_desde = ttk.Entry(panel_filtros, width=12)
            self.entry_desde.insert(0, "01/10/2026")
        self.entry_desde.grid(row=1, column=1, sticky="ew", padx=5, pady=6)

        ttk.Label(panel_filtros, text="Hasta:", font=("Segoe UI", 9, "bold")).grid(row=1, column=2, sticky="w", padx=(15, 5), pady=6)
        if EXISTS_TKCALENDAR:
            self.entry_hasta = DateEntry(panel_filtros, width=12, background='#1f2937', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy', cursor="hand2", locale="es_VE")
            self.entry_hasta.set_date(datetime.now())
        else:
            self.entry_hasta = ttk.Entry(panel_filtros, width=12)
            self.entry_hasta.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_hasta.grid(row=1, column=3, sticky="ew", padx=5, pady=6)

        # Botones de Acción principales
        acciones_frame = ttk.Frame(panel_filtros)
        acciones_frame.grid(row=1, column=4, columnspan=2, sticky="e", pady=6)

        self.btn_consultar = ttk.Button(acciones_frame, text="🔍 Ejecutar Consulta", command=self._on_consultar)
        self.btn_consultar.pack(side="left", padx=4)
        self._aplicar_cursor_mano(self.btn_consultar)

        self.btn_volver = ttk.Button(acciones_frame, text="↩ Volver", bootstyle="secondary", command=self._on_volver)
        self.btn_volver.pack(side="left", padx=4)
        self._aplicar_cursor_mano(self.btn_volver)

        # ==========================================
        # 3. TARJETAS DE RESULTADOS ESTADÍSTICOS
        # ==========================================
        resultados_frame = ttk.LabelFrame(contenedor, text=" Resumen Analítico e Indicadores de Asistencia ", padding=12)
        resultados_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 8))
        resultados_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.card_total = tk.Label(resultados_frame, text="Matrícula Activa: 32", font=("Segoe UI", 9), fg="#1e293b", bg=color_fondo)
        self.card_total.grid(row=0, column=0, padx=5)

        self.card_asistio = tk.Label(resultados_frame, text="Asistencias: 29 (90.6%)", font=("Segoe UI", 10, "bold"), fg="#166534", bg=color_fondo)
        self.card_asistio.grid(row=0, column=1, padx=5)

        self.card_falto = tk.Label(resultados_frame, text="Inasistencias: 3 (9.4%)", font=("Segoe UI", 10, "bold"), fg="#b91c1c", bg=color_fondo)
        self.card_falto.grid(row=0, column=2, padx=5)

        self.card_estatus = tk.Label(resultados_frame, text="Estatus Cátedra: Óptimo", font=("Segoe UI", 10, "bold"), fg="#0369a1", bg=color_fondo)
        self.card_estatus.grid(row=0, column=3, padx=5)

        self.btn_grafico = ttk.Button(resultados_frame, text="Ver Gráfica Detallada", command=self._mostrar_reporte_grafico)
        self.btn_grafico.grid(row=0, column=4, padx=5, sticky="ew")
        self._aplicar_cursor_mano(self.btn_grafico)

        # ==========================================
        # 4. TABLA DE AUDITORÍA Y BÚSQUEDA DE ESTUDIANTES
        # ==========================================
        detalle_container = ttk.LabelFrame(contenedor, text=" Historial de Registros Guardados (Modo Solo Lectura - Auditoría) ", padding=12)
        detalle_container.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 15))
        detalle_container.columnconfigure(0, weight=1)
        detalle_container.rowconfigure(1, weight=1)

        # Apartado de búsqueda de estudiante
        barra_busqueda_frame = ttk.Frame(detalle_container)
        barra_busqueda_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        
        ttk.Label(barra_busqueda_frame, text="Buscar Estudiante :", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 8))
        
        self.entrada_buscar_estudiante = ttk.Entry(barra_busqueda_frame, width=32)
        self.entrada_buscar_estudiante.pack(side="left", padx=4)
        self.entrada_buscar_estudiante.insert(0, "Escriba nombre o cédula...")
        
        self.btn_filtrar_tabla = ttk.Button(barra_busqueda_frame, text="Filtrar Lista", command=self._on_buscar_estudiante_tabla)
        self.btn_filtrar_tabla.pack(side="left", padx=8)
        self._aplicar_cursor_mano(self.btn_filtrar_tabla)

        # Treeview de auditoría
        cols_stat = ("nro", "fecha", "cedula", "nombre", "estatus", "motivo")
        self.tree_asistencia = ttk.Treeview(detalle_container, columns=cols_stat, show="headings", height=10)
        
        self.tree_asistencia.heading("nro", text="N°")
        self.tree_asistencia.heading("fecha", text="Fecha de Clase")
        self.tree_asistencia.heading("cedula", text="Cédula / ID")
        self.tree_asistencia.heading("nombre", text="Apellidos y Nombres del Estudiante")
        self.tree_asistencia.heading("estatus", text="Estatus Registrado")
        self.tree_asistencia.heading("motivo", text="Motivo / Observación del Alumno")

        self.tree_asistencia.column("nro", width=45, anchor="center")
        self.tree_asistencia.column("fecha", width=110, anchor="center")
        self.tree_asistencia.column("cedula", width=110, anchor="center")
        self.tree_asistencia.column("nombre", width=300, anchor="w")
        self.tree_asistencia.column("estatus", width=140, anchor="center")
        self.tree_asistencia.column("motivo", width=280, anchor="w")

        self.tree_asistencia.grid(row=1, column=0, sticky="nsew")
        
        scrollbar_stat = ttk.Scrollbar(detalle_container, orient="vertical", command=self.tree_asistencia.yview)
        self.tree_asistencia.configure(yscrollcommand=scrollbar_stat.set)
        scrollbar_stat.grid(row=1, column=1, sticky="ns", padx=(2, 0))

        self._cargar_datos_ejemplo()

    def _actualizar_materias(self, event):
        ano = self.combo_ano.get()
        if "1er Año" in ano:
            self.combo_materia.config(values=["Matemáticas I", "Castellano y Literatura", "Inglés", "Educación Física"])
            self.combo_materia.set("Matemáticas I")
        else:
            self.combo_materia.config(values=["Matemáticas II", "Física", "Química", "Historia de Venezuela"])
            self.combo_materia.set("Matemáticas II")

    def _on_consultar(self):
        ano = self.combo_ano.get()
        seccion = self.combo_seccion.get()
        materia = self.combo_materia.get()
        
        desde = self.entry_desde.get() if hasattr(self.entry_desde, 'get') else self.entry_desde.get_date().strftime("%d/%m/%Y")
        hasta = self.entry_hasta.get() if hasattr(self.entry_hasta, 'get') else self.entry_hasta.get_date().strftime("%d/%m/%Y")
        
        messagebox.showinfo(
            "Consulta Procesada", 
            f"Filtros Académicos Aplicados:\n\n"
            f"Grupo: {ano} - {seccion}\n"
            f"Cátedra: {materia}\n"
            f"Intervalo: {desde} al {hasta}"
        )

    def _on_buscar_estudiante_tabla(self):
        criterio = self.entrada_buscar_estudiante.get().strip()
        messagebox.showinfo("Búsqueda en Lista", f"Buscando al estudiante o cédula: '{criterio}' dentro de los registros cargados.")

    def _mostrar_reporte_grafico(self):
        messagebox.showinfo("Reporte Gráfico", "Abriendo vista gráfica de porcentajes de asistencia por cátedra...")

    def _cargar_datos_ejemplo(self):
        datos = [
            ("1", "13/10/2026", "V-34567890", "Alvarez Blanco, Sofía Valentina", "Asistió", "-"),
            ("2", "13/10/2026", "V-34123456", "Benítez Silva, Carlos Daniel", "Asistió", "-"),
            ("3", "13/10/2026", "V-35678901", "Contreras Mendoza, Gabriela", "Justificado", "Cita médica odontológica"),
            ("4", "10/10/2026", "V-34987654", "Díaz Morales, Alejandro José", "Faltó", "-"),
            ("5", "10/10/2026", "V-35111222", "Fernández Rincón, Mariángel", "Asistió", "-")
        ]
        for row in datos:
            self.tree_asistencia.insert("", "end", values=row)
    
    def _on_volver(self):
        if self.controlador_externo and hasattr(self.controlador_externo, "regresar_menu_principal"):
            self.controlador_externo.regresar_menu_principal()
        else:
            messagebox.showinfo("Navegación", "Saliendo del módulo de estadísticas...")      

if __name__ == "__main__":
    root = ttk.Window(title="L.N. Evelia A. de Pimentel - Módulo de Auditoría y Estadísticas", themename="flatly", size=(950, 720))
    root.configure(bg="#F3F3E0")
    
    app = VistaAsistenciaEstadistica(contenedor_principal=root, controlador_externo=None)
    app.pack(fill="both", expand=True, padx=10, pady=10)
    root.mainloop()