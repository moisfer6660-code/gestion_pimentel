import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.style import Style

class VistaCierreAcademico(ttk.Frame):
    """Interfaz para la gestión de cierres de lapso y transiciones de año escolar con clave de seguridad y diseño institucional unificado."""

    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        
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
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(1, weight=1)

        # 1. Encabezado simétrico con Grid de 2 columnas (Títulos a la izquierda, Logo a la derecha)
        marco_encabezado = ttk.Frame(contenedor, padding=(20, 15, 20, 5))
        marco_encabezado.grid(row=0, column=0, sticky="ew")
        marco_encabezado.columnconfigure(0, weight=1)
        marco_encabezado.columnconfigure(1, weight=0)

        marco_titulos = ttk.Frame(marco_encabezado)
        marco_titulos.grid(row=0, column=0, sticky="w")

        etiqueta_titulo = tk.Label(
            marco_titulos, 
            text="Procesos de Cierre Académico", 
            font=("Segoe UI", 22, "bold"),
            fg="#b91c1c",
            bg=color_fondo
        )
        etiqueta_titulo.pack(anchor="w")

        etiqueta_subtitulo = tk.Label(
            marco_titulos, 
            text="Gestión de cierres de lapsos, bloqueo de actas y promoción de año escolar", 
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

        # Botón Volver ubicado en la parte superior derecha (junto al logo o integrado)
        btn_volver = ttk.Button(marco_encabezado, text="↩ Volver", bootstyle="secondary", command=self._on_volver_click)
        btn_volver.grid(row=0, column=1, sticky="ne", padx=(0, 120))
        self._aplicar_cursor_mano(btn_volver)

        # 2. Cuerpo con opciones de cierre (Responsivo en dos columnas)
        cuerpo = ttk.Frame(contenedor, padding=20)
        cuerpo.grid(row=1, column=0, sticky="nsew")
        cuerpo.columnconfigure((0, 1), weight=1)
        cuerpo.rowconfigure(0, weight=1)

        # SECCIÓN A: Cierre de Lapso Actual
        marco_lapso = ttk.Labelframe(cuerpo, text=" Cierre del Lapso Vigente ", padding=20)
        marco_lapso.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        marco_lapso.rowconfigure(1, weight=1)
        
        tk.Label(
            marco_lapso, 
            text="Lapso actual en curso: I Lapso (Octubre - Diciembre)\n\n"
                 "Al cerrar el lapso:\n"
                 "• Se bloqueará la carga y edición de notas para los docentes.\n"
                 "• Se calcularán los promedios parciales automáticos.\n"
                 "• Se habilitará la generación de boletines informativos.",
            font=("Segoe UI", 10),
            fg="#1e293b",
            bg=color_fondo,
            justify="left",
            wraplength=340
        ).pack(anchor="w", pady=(0, 20))

        self.btn_cerrar_lapso = ttk.Button(
            marco_lapso, 
            text="🔒 Ejecutar Cierre del I Lapso", 
            command=self._on_ejecutar_cierre_lapso
        )
        self.btn_cerrar_lapso.pack(anchor="s", fill="x", ipady=8)
        self._aplicar_cursor_mano(self.btn_cerrar_lapso)

        # SECCIÓN B: Cierre y Transición de Año Escolar
        marco_anio = ttk.Labelframe(cuerpo, text=" Cierre y Transición de Año Escolar ", padding=20)
        marco_anio.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        marco_anio.rowconfigure(1, weight=1)

        tk.Label(
            marco_anio, 
            text="Año escolar activo: 2025-2026\n\n"
                 "Al cerrar el año escolar:\n"
                 "• Se evaluará la promoción de cada alumno (Aprobado/Repitiente).\n"
                 "• Se archivarán las actas definitivas en la base de datos.\n"
                 "• Se abrirá formalmente el período 2026-2027.",
            font=("Segoe UI", 10),
            fg="#1e293b",
            bg=color_fondo,
            justify="left",
            wraplength=340
        ).pack(anchor="w", pady=(0, 20))

        self.btn_cerrar_anio = ttk.Button(
            marco_anio, 
            text="⚡ Procesar Cierre del Año Escolar 2025-2026", 
            command=self._on_ejecutar_cierre_anio
        )
        self.btn_cerrar_anio.pack(anchor="s", fill="x", ipady=8)
        self._aplicar_cursor_mano(self.btn_cerrar_anio)

    def _solicitar_clave(self, titulo="Autorización Requerida"):
        """Ventana emergente segura para solicitar la clave de acceso del administrador."""
        clave = simpledialog.askstring(
            titulo,
            "Ingrese la clave de seguridad del administrador\npara autorizar esta operación crítica:",
            show="*",
            parent=self
        )
        return clave

    def _on_ejecutar_cierre_lapso(self):
        """Controlador con validación de clave para el cierre de lapso."""
        clave_ingresada = self._solicitar_clave("Autorización - Cierre de Lapso")
        
        if clave_ingresada is None:
            return 
        
        CLAVE_MAESTRA = "1234"
        
        if clave_ingresada == CLAVE_MAESTRA:
            respuesta = messagebox.askyesno(
                "Confirmación de Cierre de Lapso",
                "Clave correcta.\n\n¿Está completamente seguro de cerrar el I Lapso?\nEsta acción bloqueará las notas de todos los docentes.",
                parent=self
            )
            if respuesta:
                messagebox.showinfo("Cierre Exitoso", "El I Lapso ha sido cerrado y las notas han sido congeladas.")
        else:
            messagebox.showerror("Acceso Denegado", "La clave de seguridad es incorrecta. Operación cancelada.", parent=self)

    def _on_ejecutar_cierre_anio(self):
        """Controlador con doble validación y clave para el cierre crítico de año escolar."""
        clave_ingresada = self._solicitar_clave("Autorización Crítica - Cierre de Año Escolar")
        
        if clave_ingresada is None:
            return

        CLAVE_MAESTRA = "1234"

        if clave_ingresada == CLAVE_MAESTRA:
            respuesta = messagebox.askyesno(
                "Alerta de Cierre de Año Escolar",
                "Clave correcta.\n\nEstá a punto de iniciar el proceso de promoción de estudiantes y cierre del período.\n\n"
                "Asegúrese de haber respaldado la base de datos antes de continuar. ¿Desea proceder?",
                parent=self
            )
            if respuesta:
                messagebox.showinfo("Transición Completada", "El año escolar ha finalizado con éxito. Se ha inicializado el período 2026-2027.")
        else:
            messagebox.showerror("Acceso Denegado", "La clave de seguridad es incorrecta. Operación cancelada.", parent=self)

    def _on_volver_click(self):
        if self.controlador and hasattr(self.controlador, "regresar_menu_principal"):
            self.controlador.regresar_menu_principal()
        elif messagebox.askyesno("Volver", "¿Desea regresar al panel principal?", parent=self):
            self.master.destroy()

if __name__ == "__main__":
    root = ttk.Window(title="L.N. Evelia A. de Pimentel - Gestión de Cierres Académicos", themename="flatly", size=(900, 520))
    root.configure(bg="#EDECD1")
    
    app = VistaCierreAcademico(parent=root, controlador=None)
    app.pack(fill="both", expand=True, padx=10, pady=10)
        
    root.mainloop()