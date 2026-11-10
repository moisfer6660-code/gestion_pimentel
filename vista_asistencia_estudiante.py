import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.style import Style

class VistaAsistenciaEstudiante(ttk.Frame):
    """Módulo de consulta de récord global e historial consolidado por estudiante con diseño institucional unificado."""

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
            text="Récord Global por Estudiante", 
            font=("Segoe UI", 22, "bold"),
            fg="#b91c1c",
            bg=color_fondo
        )
        etiqueta_titulo.pack(anchor="w")

        etiqueta_subtitulo = tk.Label(
            marco_titulos, 
            text="Módulo de consulta de récord e historial consolidado por alumno", 
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

        # 2. Barra de Búsqueda Individual
        busqueda_frame = ttk.LabelFrame(contenedor, text=" Consulta de Récord Global por Estudiante ", padding=12)
        busqueda_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(4, 8))
        busqueda_frame.columnconfigure(1, weight=1)

        ttk.Label(busqueda_frame, text="Cédula o Apellidos:", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=5)
        self.entrada_buscar_est = ttk.Entry(busqueda_frame, width=35)
        self.entrada_buscar_est.grid(row=0, column=1, sticky="ew", padx=5)
        self.entrada_buscar_est.insert(0, "Alvarez Blanco, Sofía")

        self.btn_consultar_est = ttk.Button(busqueda_frame, text="📊 Calcular Récord y Porcentaje Total", command=self._on_consultar_estudiante)
        self.btn_consultar_est.grid(row=0, column=2, padx=10)
        self._aplicar_cursor_mano(self.btn_consultar_est)

        # 3. Panel de Resumen Consolidado (Tarjetas visuales)
        marco_resumen_est = ttk.LabelFrame(contenedor, text=" Porcentaje Consolidado del Estudiante (Todas las Materias) ", padding=12)
        marco_resumen_est.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 8))
        marco_resumen_est.columnconfigure((0, 1, 2, 3), weight=1)

        self.lbl_est_total = tk.Label(marco_resumen_est, text="Total Clases Vistas: 45", font=("Segoe UI", 9), fg="#1e293b", bg=color_fondo)
        self.lbl_est_total.grid(row=0, column=0, padx=5)
        
        self.lbl_est_asistio = tk.Label(marco_resumen_est, text="Asistencias: 42 (93.3%)", font=("Segoe UI", 9, "bold"), fg="#166534", bg=color_fondo)
        self.lbl_est_asistio.grid(row=0, column=1, padx=5)
        
        self.lbl_est_faltas = tk.Label(marco_resumen_est, text="Inasistencias: 3 (6.7%)", font=("Segoe UI", 9, "bold"), fg="#b91c1c", bg=color_fondo)
        self.lbl_est_faltas.grid(row=0, column=2, padx=5)
        
        self.lbl_est_porcentaje = tk.Label(marco_resumen_est, text="Estatus: Excelente (Aprobado)", font=("Segoe UI", 9, "bold"), fg="#0369a1", bg=color_fondo)
        self.lbl_est_porcentaje.grid(row=0, column=3, padx=5)

        # 4. Historial Detallado por Materia (Treeview)
        hist_container = ttk.LabelFrame(contenedor, text=" Historial Detallado de Asistencia por Asignatura ", padding=10)
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
    root = ttk.Window(title="L.N. Evelia A. de Pimentel - Récord de Asistencia por Estudiante", themename="flatly", size=(950, 720))
    root.configure(bg="#F3F3E0")
    
    app = VistaAsistenciaEstudiante(contenedor_principal=root, controlador_externo=None)
    app.pack(fill="both", expand=True, padx=10, pady=10)
    root.mainloop()