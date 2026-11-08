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

    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self._construir_interfaz(self)

    def _construir_interfaz(self, contenedor):
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(2, weight=1)

        # ==========================================
        # 1. PANEL DE FILTRADO PROFESIONAL
        # ==========================================
        panel_filtros = ttk.LabelFrame(contenedor, text=" Panel de Control y Filtros de Auditoría ", padding=15)
        panel_filtros.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        panel_filtros.columnconfigure(3, weight=1)

        # --- Fila 0: Jerarquía Académica (Año, Sección, Materia) ---
        ttk.Label(panel_filtros, text="Año Escolar:", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.combo_ano = ttk.Combobox(panel_filtros, values=["1er Año", "2do Año", "3er Año", "4to Año", "5to Año"], state="readonly", width=14)
        self.combo_ano.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.combo_ano.set("1er Año")
        self.combo_ano.bind("<<ComboboxSelected>>", self._actualizar_materias)

        ttk.Label(panel_filtros, text="Sección:", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="w", padx=(15, 5), pady=5)
        self.combo_seccion = ttk.Combobox(panel_filtros, values=["Sección A", "Sección B", "Sección Única"], state="readonly", width=14)
        self.combo_seccion.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
        self.combo_seccion.set("Sección A")

        ttk.Label(panel_filtros, text="Cátedra / Materia:", font=("Segoe UI", 9, "bold")).grid(row=0, column=4, sticky="w", padx=(15, 5), pady=5)
        self.combo_materia = ttk.Combobox(panel_filtros, values=["Matemáticas I", "Castellano y Literatura", "Inglés", "Educación Física"], state="readonly", width=22)
        self.combo_materia.grid(row=0, column=5, sticky="ew", padx=5, pady=5)
        self.combo_materia.set("Matemáticas I")


        # Contenedor limpio y expandido para el Rango de Fechas
        fechas_wrapper = ttk.LabelFrame(panel_filtros, text=" Rango Temporal de Consulta ", padding=10)
        fechas_wrapper.grid(row=1, column=4, columnspan=2, sticky="ew", padx=5, pady=(5, 0))
        fechas_wrapper.columnconfigure(1, weight=1)
        fechas_wrapper.columnconfigure(3, weight=1)

        ttk.Label(fechas_wrapper, text="Desde:", font=("Segoe UI", 8, "bold")).grid(row=0, column=0, sticky="w", padx=(2, 5), pady=2)
        
        # Mantenemos exactamente tu variable self.entry_desde con diseño optimizado
        if EXISTS_TKCALENDAR:
            self.entry_desde = DateEntry(fechas_wrapper, width=12, background='#1f2937',
                                         foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy',
                                         cursor="hand2", locale="es_VE")
            self.entry_desde.set_date("01/10/2026")
        else:
            self.entry_desde = ttk.Entry(fechas_wrapper, width=12)
            self.entry_desde.insert(0, "01/10/2026")
        self.entry_desde.grid(row=0, column=1, padx=2, pady=2, sticky="ew")

        ttk.Label(fechas_wrapper, text="Hasta:", font=("Segoe UI", 8, "bold")).grid(row=1, column=0, sticky="w", padx=(2, 5), pady=2)
        
        # Mantenemos exactamente tu variable self.entry_hasta ubicada cómodamente abajo o en columna limpia
        if EXISTS_TKCALENDAR:
            self.entry_hasta = DateEntry(fechas_wrapper, width=12, background='#1f2937',
                                         foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy',
                                         cursor="hand2", locale="es_VE")
            self.entry_hasta.set_date(datetime.now())

        else:
            self.entry_hasta = ttk.Entry(fechas_wrapper, width=12)
            self.entry_hasta.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_hasta.grid(row=1, column=1, padx=2, pady=2, sticky="ew")

        # Mantenemos exactamente tu variable self.entry_hasta convertida a calendario interactivo
        if EXISTS_TKCALENDAR:
            self.entry_hasta = DateEntry(fechas_wrapper, width=11, background='#1f2937',
                                         foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy',
                                         cursor="hand2")
            self.entry_hasta.set_date(datetime.now())


        # --- Fila 2: Botones de Acción Estilizados ---
        acciones_frame = ttk.Frame(panel_filtros)
        acciones_frame.grid(row=2, column=0, columnspan=6, sticky="e", pady=(15, 0))

        self.btn_consultar = ttk.Button(acciones_frame, text="🔍 Ejecutar Consulta y Auditoría", command=self._on_consultar)
        self.btn_consultar.pack(side="left", padx=5)

        self.btn_volver = ttk.Button(acciones_frame, text="↩ Volver al Menú", command=self._on_volver)
        self.btn_volver.pack(side="left", padx=5)


        # ==========================================
        # 2. TARJETAS DE RESULTADOS ESTADÍSTICOS
        # ==========================================
        resultados_frame = ttk.LabelFrame(contenedor, text=" Resumen Analítico e Indicadores de Asistencia ", padding=12)
        resultados_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        resultados_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.card_total = ttk.Label(resultados_frame, text="Matrícula Activa: 32", font=("Segoe UI", 9))
        self.card_total.grid(row=0, column=0, padx=5)

        self.card_asistio = ttk.Label(resultados_frame, text="Asistencias: 29 (90.6%)", font=("Segoe UI", 10, "bold"), foreground="#27AE60")
        self.card_asistio.grid(row=0, column=1, padx=5)

        self.card_falto = ttk.Label(resultados_frame, text="Inasistencias: 3 (9.4%)", font=("Segoe UI", 10, "bold"), foreground="#C0392B")
        self.card_falto.grid(row=0, column=2, padx=5)

        self.card_estatus = ttk.Label(resultados_frame, text="Estatus Cátedra: Óptimo", font=("Segoe UI", 10, "bold"), foreground="#2980B9")
        self.card_estatus.grid(row=0, column=3, padx=5)

        self.btn_grafico = ttk.Button(resultados_frame, text="📊 Ver Gráfica Detallada", command=self._mostrar_reporte_grafico)
        self.btn_grafico.grid(row=0, column=4, padx=5, sticky="ew")


        # ==========================================
        # 3. TABLA DE AUDITORÍA (TREEVIEW DE SOLO LECTURA)
        # ==========================================
        detalle_container = ttk.LabelFrame(contenedor, text=" Historial de Registros Guardados (Modo Solo Lectura - Auditoría) ", padding=8)
        detalle_container.grid(row=2, column=0, sticky="nsew")
        detalle_container.columnconfigure(0, weight=1)
        detalle_container.rowconfigure(0, weight=1)

        cols_stat = ("nro", "fecha", "cedula", "nombre", "estatus", "motivo")
        self.tree_asistencia = ttk.Treeview(detalle_container, columns=cols_stat, show="headings", height=14)
        
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

        self.tree_asistencia.pack(side="left", fill="both", expand=True)
        
        scrollbar_stat = ttk.Scrollbar(detalle_container, orient="vertical", command=self.tree_asistencia.yview)
        self.tree_asistencia.configure(yscrollcommand=scrollbar_stat.set)
        scrollbar_stat.pack(side="right", fill="y")

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
        estudiante = self.combo_estudiante.get()
        
        # Soporta tanto el valor directo del DateEntry como el formato Entry clásico
        desde = self.entry_desde.get() if hasattr(self.entry_desde, 'get') else self.entry_desde.get_date().strftime("%d/%m/%Y")
        hasta = self.entry_hasta.get() if hasattr(self.entry_hasta, 'get') else self.entry_hasta.get_date().strftime("%d/%m/%Y")
        
        messagebox.showinfo(
            "Consulta Procesada", 
            f"Filtros Aplicados Exitosamente:\n\n"
            f"Grupo: {ano} - {seccion}\n"
            f"Cátedra: {materia}\n"
            f"Estudiante: {estudiante}\n"
            f"Intervalo: {desde} al {hasta}"
        )

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
        messagebox.showinfo("Navegación", "Saliendo del módulo de estadísticas...")      

if __name__ == "__main__":
    root = tk.Tk()
    root.title("L.N. Evelia A. de Pimentel - Módulo de Auditoría y Estadísticas")
    root.geometry("1180x720")
    app = VistaAsistenciaEstadistica(parent=root, controlador=None)
    app.pack(fill="both", expand=True, padx=10, pady=10)
    root.mainloop()