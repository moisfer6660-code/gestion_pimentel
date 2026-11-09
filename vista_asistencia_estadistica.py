import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# Intentamos importar tkcalendar para el selector gráfico interactivo de fechas
try:
    from tkcalendar import DateEntry
    EXISTS_TKCALENDAR = True
except ImportError:
    EXISTS_TKCALENDAR = False

class VistaAsistenciaEstadistica(ttk.Frame):
    """Módulo profesional de consulta, auditoría y estadísticas de asistencia escolar."""

    def __init__(self, contenedor_principal, controlador_externo=None):
        super().__init__(contenedor_principal)
        self.controlador_externo = controlador_externo
        self._configurar_estilos_ttk()
        self._construir_interfaz(self)

    def _configurar_estilos_ttk(self):
        estilo_ttk = ttk.Style()
        if "clam" in estilo_ttk.theme_names():
            estilo_ttk.theme_use("clam")
        
        estilo_ttk.configure(".", font=("Segoe UI", 9))
        estilo_ttk.configure("TFrame", background="#f8fafc")
        estilo_ttk.configure("TLabelframe", background="#f8fafc", bordercolor="#cbd5e1")
        estilo_ttk.configure("TLabelframe.Label", background="#f8fafc", foreground="#1e293b", font=("Segoe UI", 9, "bold"))
        
        # Botones unificados con el rojo institucional principal
        estilo_ttk.configure("TButton", padding=(10, 6), relief="flat", background="#b91c1c", borderwidth=0, font=("Segoe UI", 9, "bold"), foreground="#FFFFFF")
        estilo_ttk.map("TButton", background=[("active", "#991b1b"), ("pressed", "#7f1d1d")])

        # Botón secundario / Regresar - Gris pizarra elegante
        estilo_ttk.configure("Secondary.TButton", background="#475569", foreground="#ffffff")
        estilo_ttk.map("Secondary.TButton", background=[("active", "#334155"), ("pressed", "#1e293b")])

        # Botón informativo / Gráficas - Azul acero institucional
        estilo_ttk.configure("Info.TButton", background="#b91c1c", foreground="#ffffff")
        estilo_ttk.map("Info.TButton", background=[("active", "#991b1b"), ("pressed", "#7f1d1d")])

    def _aplicar_cursor_mano(self, boton):
        """Asigna el cambio de cursor a formato de mano interactiva al pasar por encima."""
        boton.bind("<Enter>", lambda e: self.winfo_toplevel().config(cursor="hand2"))
        boton.bind("<Leave>", lambda e: self.winfo_toplevel().config(cursor=""))

    def _construir_interfaz(self, contenedor):
        contenedor.configure(style="TFrame")
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(3, weight=1)

        # Encabezado institucional limpio
        encabezado = ttk.Frame(contenedor, style="TFrame", height=80)
        encabezado.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))
        encabezado.columnconfigure(0, weight=1)

        frame_titulos = ttk.Frame(encabezado, style="TFrame")
        frame_titulos.pack(side="left", anchor="w")

        etiqueta_titulo = tk.Label(
            frame_titulos, 
            text="Control y Estadísticas de Asistencia", 
            font=("Segoe UI", 22, "bold"),
            foreground="#A93226",
            background="#f8fafc"
        )
        etiqueta_titulo.pack(anchor="w")

        etiqueta_subtitulo = tk.Label(
            frame_titulos, 
            text="Módulo profesional de consulta, auditoría y estadísticas escolares", 
            font=("Segoe UI", 11, "italic"),
            foreground="#64748b",
            background="#f8fafc"
        )
        etiqueta_subtitulo.pack(anchor="w", pady=(1, 0))

        # ==========================================
        # 1. PANEL DE FILTRADO (AÑO, SECCIÓN, CÁTEDRA, FECHAS)
        # ==========================================
        panel_filtros = ttk.LabelFrame(contenedor, text=" Panel de Control y Filtros Académicos ", padding=15, style="TLabelframe")
        panel_filtros.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        panel_filtros.columnconfigure(1, weight=1)
        panel_filtros.columnconfigure(3, weight=1)
        panel_filtros.columnconfigure(5, weight=1)

        # Fila 0: Año, Sección y Cátedra
        ttk.Label(panel_filtros, text="Año Escolar:", font=("Segoe UI", 9, "bold"), background="#f8fafc").grid(row=0, column=0, sticky="w", padx=5, pady=6)
        self.combo_ano = ttk.Combobox(panel_filtros, values=["1er Año", "2do Año", "3er Año", "4to Año", "5to Año"], state="readonly", width=14)
        self.combo_ano.grid(row=0, column=1, sticky="ew", padx=5, pady=6)
        self.combo_ano.set("1er Año")
        self.combo_ano.bind("<<ComboboxSelected>>", self._actualizar_materias)

        ttk.Label(panel_filtros, text="Sección:", font=("Segoe UI", 9, "bold"), background="#f8fafc").grid(row=0, column=2, sticky="w", padx=(15, 5), pady=6)
        self.combo_seccion = ttk.Combobox(panel_filtros, values=["Sección A", "Sección B", "Sección Única"], state="readonly", width=14)
        self.combo_seccion.grid(row=0, column=3, sticky="ew", padx=5, pady=6)
        self.combo_seccion.set("Sección A")

        ttk.Label(panel_filtros, text="Cátedra:", font=("Segoe UI", 9, "bold"), background="#f8fafc").grid(row=0, column=4, sticky="w", padx=(15, 5), pady=6)
        self.combo_materia = ttk.Combobox(panel_filtros, values=["Matemáticas I", "Castellano y Literatura", "Inglés", "Educación Física"], state="readonly", width=18)
        self.combo_materia.grid(row=0, column=5, sticky="ew", padx=5, pady=6)
        self.combo_materia.set("Matemáticas I")

        # Fila 1: Rango de Fechas y Botones de Consulta
        ttk.Label(panel_filtros, text="Desde:", font=("Segoe UI", 9, "bold"), background="#f8fafc").grid(row=1, column=0, sticky="w", padx=5, pady=6)
        if EXISTS_TKCALENDAR:
            self.entry_desde = DateEntry(panel_filtros, width=12, background='#1f2937', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy', cursor="hand2", locale="es_VE")
            self.entry_desde.set_date("01/10/2026")
        else:
            self.entry_desde = ttk.Entry(panel_filtros, width=12)
            self.entry_desde.insert(0, "01/10/2026")
        self.entry_desde.grid(row=1, column=1, sticky="ew", padx=5, pady=6)

        ttk.Label(panel_filtros, text="Hasta:", font=("Segoe UI", 9, "bold"), background="#f8fafc").grid(row=1, column=2, sticky="w", padx=(15, 5), pady=6)
        if EXISTS_TKCALENDAR:
            self.entry_hasta = DateEntry(panel_filtros, width=12, background='#1f2937', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy', cursor="hand2", locale="es_VE")
            self.entry_hasta.set_date(datetime.now())
        else:
            self.entry_hasta = ttk.Entry(panel_filtros, width=12)
            self.entry_hasta.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_hasta.grid(row=1, column=3, sticky="ew", padx=5, pady=6)

        # Botones de Acción principales con estilo rojo institucional
        acciones_frame = ttk.Frame(panel_filtros, style="TFrame")
        acciones_frame.grid(row=1, column=4, columnspan=2, sticky="e", pady=6)

        self.btn_consultar = ttk.Button(acciones_frame, text="🔍 Ejecutar Consulta", command=self._on_consultar)
        self.btn_consultar.pack(side="left", padx=4)
        self._aplicar_cursor_mano(self.btn_consultar)

        self.btn_volver = ttk.Button(acciones_frame, text="↩ Volver al Menú", style="Secondary.TButton", command=self._on_volver)
        self.btn_volver.pack(side="left", padx=4)
        self._aplicar_cursor_mano(self.btn_volver)

        # ==========================================
        # 2. TARJETAS DE RESULTADOS ESTADÍSTICOS
        # ==========================================
        resultados_frame = ttk.LabelFrame(contenedor, text=" Resumen Analítico e Indicadores de Asistencia ", padding=12, style="TLabelframe")
        resultados_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
        resultados_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.card_total = ttk.Label(resultados_frame, text="Matrícula Activa: 32", font=("Segoe UI", 9), background="#f8fafc")
        self.card_total.grid(row=0, column=0, padx=5)

        self.card_asistio = ttk.Label(resultados_frame, text="Asistencias: 29 (90.6%)", font=("Segoe UI", 10, "bold"), foreground="#27AE60", background="#f8fafc")
        self.card_asistio.grid(row=0, column=1, padx=5)

        self.card_falto = ttk.Label(resultados_frame, text="Inasistencias: 3 (9.4%)", font=("Segoe UI", 10, "bold"), foreground="#C0392B", background="#f8fafc")
        self.card_falto.grid(row=0, column=2, padx=5)

        self.card_estatus = ttk.Label(resultados_frame, text="Estatus Cátedra: Óptimo", font=("Segoe UI", 10, "bold"), foreground="#2980B9", background="#f8fafc")
        self.card_estatus.grid(row=0, column=3, padx=5)

        self.btn_grafico = ttk.Button(resultados_frame, text="Ver Gráfica Detallada", style="Info.TButton", command=self._mostrar_reporte_grafico)
        self.btn_grafico.grid(row=0, column=4, padx=5, sticky="ew")
        self._aplicar_cursor_mano(self.btn_grafico)

        # ==========================================
        # 3. TABLA DE AUDITORÍA Y BÚSQUEDA DE ESTUDIANTES
        # ==========================================
        detalle_container = ttk.LabelFrame(contenedor, text=" Historial de Registros Guardados (Modo Solo Lectura - Auditoría) ", padding=12, style="TLabelframe")
        detalle_container.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 15))
        detalle_container.columnconfigure(0, weight=1)
        detalle_container.rowconfigure(1, weight=1)

        # Apartado de búsqueda de estudiante ubicado exactamente arriba de la lista/tabla de resultados
        barra_busqueda_frame = ttk.Frame(detalle_container, style="TFrame")
        barra_busqueda_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        
        ttk.Label(barra_busqueda_frame, text="Buscar Estudiante :", font=("Segoe UI", 9, "bold"), background="#f8fafc").pack(side="left", padx=(0, 8))
        
        self.entrada_buscar_estudiante = ttk.Entry(barra_busqueda_frame, width=35)
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
    root = tk.Tk()
    root.title("L.N. Evelia A. de Pimentel - Módulo de Auditoría y Estadísticas")
    root.geometry("900x700")
    app = VistaAsistenciaEstadistica(contenedor_principal=root, controlador_externo=None)
    app.pack(fill="both", expand=True)
    root.mainloop()