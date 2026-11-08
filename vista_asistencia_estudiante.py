import tkinter as tk
from tkinter import ttk, messagebox

class VistaAsistenciaEstudiante(ttk.Frame):
    """Módulo de consulta de récord global e historial consolidado por estudiante."""

    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self._construir_interfaz(self)

    def _construir_interfaz(self, contenedor):
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(2, weight=1)

        # Barra de Búsqueda Individual
        busqueda_frame = ttk.LabelFrame(contenedor, text=" Consulta de Récord Global por Estudiante ", padding=12)
        busqueda_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        busqueda_frame.columnconfigure(1, weight=1)

        ttk.Label(busqueda_frame, text="Cédula o Apellidos:", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=5)
        self.entrada_buscar_est = ttk.Entry(busqueda_frame, width=35)
        self.entrada_buscar_est.grid(row=0, column=1, sticky="ew", padx=5)
        self.entrada_buscar_est.insert(0, "Alvarez Blanco, Sofía")

        self.btn_consultar_est = ttk.Button(busqueda_frame, text="📊 Calcular Récord y Porcentaje Total", command=self._on_consultar_estudiante)
        self.btn_consultar_est.grid(row=0, column=2, padx=10)

        # Panel de Resumen Consolidado (Tarjetas visuales)
        marco_resumen_est = ttk.LabelFrame(contenedor, text=" Porcentaje Consolidado del Estudiante (Todas las Materias) ", padding=12)
        marco_resumen_est.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        marco_resumen_est.columnconfigure((0, 1, 2, 3), weight=1)

        self.lbl_est_total = ttk.Label(marco_resumen_est, text="Total Clases Vistas: 45", font=("Segoe UI", 9))
        self.lbl_est_total.grid(row=0, column=0, padx=5)
        
        self.lbl_est_asistio = ttk.Label(marco_resumen_est, text="Asistencias: 42 (93.3%)", font=("Segoe UI", 9, "bold"), foreground="#27AE60")
        self.lbl_est_asistio.grid(row=0, column=1, padx=5)
        
        self.lbl_est_faltas = ttk.Label(marco_resumen_est, text="Inasistencias: 3 (6.7%)", font=("Segoe UI", 9, "bold"), foreground="#C0392B")
        self.lbl_est_faltas.grid(row=0, column=2, padx=5)
        
        self.lbl_est_porcentaje = ttk.Label(marco_resumen_est, text="Estatus: Excelente (Aprobado)", font=("Segoe UI", 9, "bold"), foreground="#2980B9")
        self.lbl_est_porcentaje.grid(row=0, column=3, padx=5)

        # Historial Detallado por Materia (Treeview)
        hist_container = ttk.LabelFrame(contenedor, text=" Historial Detallado de Asistencia por Asignatura ", padding=8)
        hist_container.grid(row=2, column=0, sticky="nsew")
        hist_container.columnconfigure(0, weight=1)
        hist_container.rowconfigure(0, weight=1)

        cols_hist = ("fecha", "materia", "seccion", "estatus", "motivo")
        self.tree_historial = ttk.Treeview(hist_container, columns=cols_hist, show="headings", height=12)
        
        self.tree_historial.heading("fecha", text="Fecha")
        self.tree_historial.heading("materia", text="Asignatura / Materia")
        self.tree_historial.heading("seccion", text="Sección")
        self.tree_historial.heading("estatus", text="Estatus")
        self.tree_historial.heading("motivo", text="Motivo / Observación")

        self.tree_historial.column("fecha", width=110, anchor="center")
        self.tree_historial.column("materia", width=220, anchor="w")
        self.tree_historial.column("seccion", width=120, anchor="center")
        self.tree_historial.column("estatus", width=130, anchor="center")
        self.tree_historial.column("motivo", width=260, anchor="w")

        self.tree_historial.pack(side="left", fill="both", expand=True)
        
        scrollbar_hist = ttk.Scrollbar(hist_container, orient="vertical", command=self.tree_historial.yview)
        self.tree_historial.configure(yscrollcommand=scrollbar_hist.set)
        scrollbar_hist.pack(side="right", fill="y")

        self._cargar_historial_ejemplo()

    def _on_consultar_estudiante(self):
        estudiante = self.entrada_buscar_est.get()
        messagebox.showinfo("Récord Global", f"Consolidando asistencia total de todas las materias para: {estudiante}")

    def _cargar_historial_ejemplo(self):
        registros = [
            ("2026-10-10", "Matemáticas I", "1er Año - A", "Asistió", "-"),
            ("2026-10-08", "Castellano y Literatura", "1er Año - A", "Asistió", "-"),
            ("2026-10-05", "Inglés", "1er Año - A", "Justificado", "Cita médica odontológica"),
            ("2026-10-01", "Ciencias Naturales", "1er Año - A", "Asistió", "-")
        ]
        for reg in registros:
            self.tree_historial.insert("", "end", values=reg)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("L.N. Evelia A. de Pimentel - vista_asistencia_estudiante")
    root.geometry("1120x680")
    app = VistaAsistenciaEstudiante(parent=root, controlador=None)
    app.pack(fill="both", expand=True, padx=10, pady=10)
    root.mainloop()