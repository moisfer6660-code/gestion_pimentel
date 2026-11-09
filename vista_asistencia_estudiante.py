import os
import tkinter as tk
from tkinter import ttk, messagebox

class VistaAsistenciaEstudiante(ttk.Frame):
    """Módulo de consulta de récord global e historial consolidado por estudiante."""

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

        # Botón de acción principal - Verde institucional
        estilo_ttk.configure("Accent.TButton", background="#32B855", foreground="#ffffff")
        estilo_ttk.map("Accent.TButton", background=[("active", "#289e47"), ("pressed", "#1e7835")])

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
            text="Récord Global por Estudiante", 
            font=("Segoe UI", 22, "bold"),
            foreground="#A93226",
            background="#f8fafc"
        )
        etiqueta_titulo.pack(anchor="w")

        etiqueta_subtitulo = tk.Label(
            frame_titulos, 
            text="Módulo de consulta de récord e historial consolidado por alumno", 
            font=("Segoe UI", 11, "italic"),
            foreground="#64748b",
            background="#f8fafc"
        )
        etiqueta_subtitulo.pack(anchor="w", pady=(1, 0))

        # Barra de Búsqueda Individual
        busqueda_frame = ttk.LabelFrame(contenedor, text=" Consulta de Récord Global por Estudiante ", padding=12, style="TLabelframe")
        busqueda_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        busqueda_frame.columnconfigure(1, weight=1)

        ttk.Label(busqueda_frame, text="Cédula o Apellidos:", font=("Segoe UI", 9, "bold"), background="#f8fafc").grid(row=0, column=0, sticky="w", padx=5)
        self.entrada_buscar_est = ttk.Entry(busqueda_frame, width=35)
        self.entrada_buscar_est.grid(row=0, column=1, sticky="ew", padx=5)
        self.entrada_buscar_est.insert(0, "Alvarez Blanco, Sofía")

        self.btn_consultar_est = ttk.Button(busqueda_frame, text="📊 Calcular Récord y Porcentaje Total", style="Accent.TButton", command=self._on_consultar_estudiante)
        self.btn_consultar_est.grid(row=0, column=2, padx=10)
        self._aplicar_cursor_mano(self.btn_consultar_est)

        # Panel de Resumen Consolidado (Tarjetas visuales)
        marco_resumen_est = ttk.LabelFrame(contenedor, text=" Porcentaje Consolidado del Estudiante (Todas las Materias) ", padding=12, style="TLabelframe")
        marco_resumen_est.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
        marco_resumen_est.columnconfigure((0, 1, 2, 3), weight=1)

        self.lbl_est_total = ttk.Label(marco_resumen_est, text="Total Clases Vistas: 45", font=("Segoe UI", 9), background="#f8fafc")
        self.lbl_est_total.grid(row=0, column=0, padx=5)
        
        self.lbl_est_asistio = ttk.Label(marco_resumen_est, text="Asistencias: 42 (93.3%)", font=("Segoe UI", 9, "bold"), foreground="#27AE60", background="#f8fafc")
        self.lbl_est_asistio.grid(row=0, column=1, padx=5)
        
        self.lbl_est_faltas = ttk.Label(marco_resumen_est, text="Inasistencias: 3 (6.7%)", font=("Segoe UI", 9, "bold"), foreground="#C0392B", background="#f8fafc")
        self.lbl_est_faltas.grid(row=0, column=2, padx=5)
        
        self.lbl_est_porcentaje = ttk.Label(marco_resumen_est, text="Estatus: Excelente (Aprobado)", font=("Segoe UI", 9, "bold"), foreground="#2980B9", background="#f8fafc")
        self.lbl_est_porcentaje.grid(row=0, column=3, padx=5)

        # Historial Detallado por Materia (Treeview)
        hist_container = ttk.LabelFrame(contenedor, text=" Historial Detallado de Asistencia por Asignatura ", padding=8, style="TLabelframe")
        hist_container.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 15))
        hist_container.columnconfigure(0, weight=1)
        hist_container.rowconfigure(0, weight=1)

        cols_hist = ("fecha", "materia", "seccion", "estatus", "motivo")
        self.tree_historial = ttk.Treeview(hist_container, columns=cols_hist, show="headings", height=10)
        
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
    root.title("L.N. Evelia A. de Pimentel - Récord de Asistencia por Estudiante")
    root.geometry("900x690")
    app = VistaAsistenciaEstudiante(contenedor_principal=root, controlador_externo=None)
    app.pack(fill="both", expand=True)
    root.mainloop()