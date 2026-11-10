import os
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.style import Style

class VistaConfiguracion(ttk.Frame):
    """Interfaz gráfica modular para la configuración general del sistema y parámetros del plantel con diseño institucional unificado."""

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

        # ==========================================
        # 1. ENCABEZADO INSTITUCIONAL
        # ==========================================
        marco_encabezado = ttk.Frame(contenedor, padding=(20, 15, 20, 5))
        marco_encabezado.grid(row=0, column=0, sticky="ew")
        marco_encabezado.columnconfigure(0, weight=1)
        marco_encabezado.columnconfigure(1, weight=0)

        marco_titulos = ttk.Frame(marco_encabezado)
        marco_titulos.grid(row=0, column=0, sticky="w")

        etiqueta_titulo = tk.Label(
            marco_titulos, 
            text="Configuración del Sistema", 
            font=("Segoe UI", 22, "bold"),
            fg="#b91c1c",
            bg=color_fondo
        )
        etiqueta_titulo.pack(anchor="w")

        etiqueta_subtitulo = tk.Label(
            marco_titulos, 
            text="Parámetros institucionales, períodos académicos y opciones de respaldo", 
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

        # Botón para volver al Panel
        btn_volver = ttk.Button(marco_encabezado, text="↩ Volver al Panel", bootstyle="secondary", command=self._on_volver_click)
        btn_volver.grid(row=0, column=1, sticky="ne", padx=(0, 120))
        self._aplicar_cursor_mano(btn_volver)

        # ==========================================
        # 2. CONTENEDOR DE PESTAÑAS (NOTEBOOK)
        # ==========================================
        cuerpo_frame = ttk.Frame(contenedor, padding=15)
        cuerpo_frame.grid(row=1, column=0, sticky="nsew")
        cuerpo_frame.columnconfigure(0, weight=1)
        cuerpo_frame.rowconfigure(0, weight=1)

        notebook_configuracion = ttk.Notebook(cuerpo_frame)
        notebook_configuracion.pack(fill="both", expand=True)

        # Crear las pestañas del sistema
        pestana_plantel = ttk.Frame(notebook_configuracion, padding=15)
        pestana_academica = ttk.Frame(notebook_configuracion, padding=15)
        pestana_respaldo = ttk.Frame(notebook_configuracion, padding=15)

        notebook_configuracion.add(pestana_plantel, text="🏛️ Datos del Plantel")
        notebook_configuracion.add(pestana_academica, text="📅 Período y Notas")
        notebook_configuracion.add(pestana_respaldo, text="💾 Respaldo y Base de Datos")

        # ==========================================
        # PESTAÑA 1: DATOS DEL PLANTEL E IDENTIDAD
        # ==========================================
        pestana_plantel.columnconfigure(0, weight=1)
        pestana_plantel.columnconfigure(1, weight=1)

        marco_datos = ttk.LabelFrame(pestana_plantel, text=" Información Oficial de la Institución ", padding=15)
        marco_datos.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        marco_datos.columnconfigure(1, weight=1)

        campos_plantel = [
            ("Nombre del Plantel:", "E.B.N. Evelia A. de Pimentel"),
            ("Código Estadístico:", "OD04391820"),
            ("Zona Educativa:", "Zulia"),
            ("Dirección Fiscal:", "Parroquia Idelfonso Vázquez, Maracaibo"),
            ("Teléfono de Contacto:", "0261-5555555")
        ]

        self.entradas_plantel = {}
        for indice, (etiqueta, valor_defecto) in enumerate(campos_plantel):
            ttk.Label(marco_datos, text=etiqueta, font=("Segoe UI", 9, "bold")).grid(row=indice, column=0, sticky="w", pady=6, padx=5)
            entrada = ttk.Entry(marco_datos, width=32)
            entrada.insert(0, valor_defecto)
            entrada.grid(row=indice, column=1, sticky="ew", pady=6, padx=5)
            self.entradas_plantel[etiqueta] = entrada

        # Marco para gestión de logo institucional
        marco_logo = ttk.LabelFrame(pestana_plantel, text=" Escudo / Logotipo Institucional ", padding=15)
        marco_logo.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        marco_logo.columnconfigure(0, weight=1)

        tk.Label(
            marco_logo, 
            text="Imagen actual utilizada en el sistema (logo.png):", 
            font=("Segoe UI", 9), 
            fg="#566573",
            bg=color_fondo
        ).pack(anchor="w", pady=(0, 10))

        self.lbl_estado_logo = tk.Label(marco_logo, text="Archivo cargado correctamente en el directorio", font=("Segoe UI", 9, "bold"), fg="#166534", bg=color_fondo)
        self.lbl_estado_logo.pack(anchor="w", pady=(0, 15))

        btn_cambiar_logo = ttk.Button(marco_logo, text="📂 Seleccionar Nuevo Logo...", command=self._on_seleccionar_logo)
        btn_cambiar_logo.pack(anchor="w", fill="x", pady=5)
        self._aplicar_cursor_mano(btn_cambiar_logo)

        # Botón guardar cambios plantel
        btn_guardar_plantel = ttk.Button(pestana_plantel, text="Guardar Cambios Institucionales", command=self._on_guardar_plantel)
        btn_guardar_plantel.grid(row=1, column=0, columnspan=2, sticky="e", pady=(15, 0))
        self._aplicar_cursor_mano(btn_guardar_plantel)

        # ==========================================
        # PESTAÑA 2: PERÍODO ESCOLAR Y CALIFICACIONES
        # ==========================================
        pestana_academica.columnconfigure(0, weight=1)

        marco_academico = ttk.LabelFrame(pestana_academica, text=" Configuración del Calendario y Evaluación ", padding=15)
        marco_academico.pack(fill="both", expand=True)
        marco_academico.columnconfigure(1, weight=1)

        # Año escolar vigente
        ttk.Label(marco_academico, text="Año Escolar Vigente:", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", pady=8, padx=5)
        self.combo_anio_escolar = ttk.Combobox(marco_academico, values=["2025-2026", "2026-2027", "2027-2028"], state="readonly")
        self.combo_anio_escolar.set("2025-2026")
        self.combo_anio_escolar.grid(row=0, column=1, sticky="ew", pady=8, padx=5)

        # Lapso activo
        ttk.Label(marco_academico, text="Momento / Lapso Activo:", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w", pady=8, padx=5)
        self.combo_lapso = ttk.Combobox(marco_academico, values=["I Lapso (Octubre - Diciembre)", "II Lapso (Enero - Marzo)", "III Lapso (Abril - Julio)"], state="readonly")
        self.combo_lapso.set("I Lapso (Octubre - Diciembre)")
        self.combo_lapso.grid(row=1, column=1, sticky="ew", pady=8, padx=5)

        # Nota mínima aprobatoria
        ttk.Label(marco_academico, text="Calificación Mínima Aprobatoria:", font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", pady=8, padx=5)
        self.entrada_nota_minima = ttk.Entry(marco_academico, width=15)
        self.entrada_nota_minima.insert(0, "10")
        self.entrada_nota_minima.grid(row=2, column=1, sticky="w", pady=8, padx=5)

        # Check de bloqueo de notas por lapso cerrado
        self.var_bloquear_lapso = tk.BooleanVar(value=True)
        
        # Creamos un Checkbutton adaptado al fondo pergamino
        chk_bloquear = tk.Checkbutton(
            marco_academico, 
            text="Bloquear carga de notas automáticamente al cerrar el lapso escolar", 
            variable=self.var_bloquear_lapso,
            font=("Segoe UI", 9),
            bg=color_fondo,
            activebackground=color_fondo
        )
        chk_bloquear.grid(row=3, column=0, columnspan=2, sticky="w", pady=15, padx=5)

        btn_guardar_academico = ttk.Button(pestana_academica, text="Actualizar Parámetros Académicos", command=self._on_guardar_academico)
        btn_guardar_academico.pack(anchor="e", pady=(15, 0))
        self._aplicar_cursor_mano(btn_guardar_academico)

        # ==========================================
        # PESTAÑA 3: RESPALDO Y SEGURIDAD
        # ==========================================
        pestana_respaldo.columnconfigure(0, weight=1)

        marco_respaldo = ttk.LabelFrame(pestana_respaldo, text=" Gestión de Respaldo y Mantenimiento de Datos ", padding=15)
        marco_respaldo.pack(fill="both", expand=True)

        tk.Label(
            marco_respaldo, 
            text="Genera copias de seguridad de la base de datos institucional o restaura información previa en caso de contingencia técnica.", 
            font=("Segoe UI", 9), 
            fg="#566573",
            bg=color_fondo
        ).pack(anchor="w", pady=(0, 15))

        # Botones de respaldo
        btn_backup = ttk.Button(marco_respaldo, text="📥 Generar Respaldo Manual de la Base de Datos", command=self._on_generar_backup)
        btn_backup.pack(anchor="w", fill="x", pady=8, ipady=4)
        self._aplicar_cursor_mano(btn_backup)

        btn_restaurar = ttk.Button(marco_respaldo, text="📂 Restaurar Base de Datos desde un Archivo...", command=self._on_restaurar_backup)
        btn_restaurar.pack(anchor="w", fill="x", pady=8, ipady=4)
        self._aplicar_cursor_mano(btn_restaurar)

        btn_auditoria = ttk.Button(marco_respaldo, text="📋 Ver Registro de Auditoría y Bitácora del Sistema", command=self._on_ver_auditoria)
        btn_auditoria.pack(anchor="w", fill="x", pady=8, ipady=4)
        self._aplicar_cursor_mano(btn_auditoria)

    def _on_seleccionar_logo(self):
        """Permite buscar y seleccionar una nueva imagen para el logotipo."""
        archivo = filedialog.askopenfilename(
            title="Seleccionar Escudo Institucional",
            filetypes=[("Archivos de Imagen", "*.png;*.jpg;*.jpeg")]
        )
        if archivo:
            self.lbl_estado_logo.config(text=f"✅ Nuevo logo seleccionado: {os.path.basename(archivo)}")
            messagebox.showinfo("Imagen Seleccionada", "El archivo de imagen ha sido seleccionado con éxito. Guarde los cambios para aplicarlo.", parent=self)

    def _on_guardar_plantel(self):
        """Guarda la información general de la institución."""
        messagebox.showinfo("Configuración Guardada", "Los datos institucionales del plantel han sido actualizados con éxito.", parent=self)

    def _on_guardar_academico(self):
        """Guarda los parámetros de año escolar y notas."""
        messagebox.showinfo("Configuración Guardada", "Los parámetros del período escolar y evaluación han sido actualizados.", parent=self)

    def _on_generar_backup(self):
        """Simula la creación de un respaldo."""
        messagebox.showinfo("Respaldo Exitoso", "La copia de seguridad de la base de datos se ha generado y guardado correctamente.", parent=self)

    def _on_restaurar_backup(self):
        """Simula la restauración del sistema."""
        if messagebox.askyesno("Advertencia de Restauración", "¿Está seguro de sobreescribir los datos actuales con un respaldo externo?", parent=self):
            messagebox.showinfo("Restauración Completa", "El sistema se ha restaurado con éxito a partir del archivo seleccionado.", parent=self)

    def _on_ver_auditoria(self):
        """Muestra ventana o aviso de auditoría."""
        messagebox.showinfo("Bitácora", "Abriendo el registro de auditoría y acciones de usuarios...", parent=self)

    def _on_volver_click(self):
        """Cierra la vista de configuración y regresa al dashboard."""
        if self.controlador and hasattr(self.controlador, "regresar_menu_principal"):
            self.controlador.regresar_menu_principal()
        elif messagebox.askyesno("Volver", "¿Desea regresar al panel principal?", parent=self):
            self.master.destroy()

if __name__ == "__main__":
    root = ttk.Window(title="L.N. Evelia A. de Pimentel - Menú de Configuración", themename="flatly", size=(900, 560))
    root.configure(bg="#EDECD1")
    root.minsize(800, 500)
    
    app = VistaConfiguracion(parent=root, controlador=None)
    app.pack(fill="both", expand=True, padx=10, pady=10)
        
    root.mainloop()