import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

class VistaConfiguracion(ttk.Frame):
    """Interfaz gráfica modular para la configuración general del sistema y parámetros del plantel."""

    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self._construir_interfaz(self)

    def _construir_interfaz(self, contenedor):
        # Configurar adaptabilidad total de la ventana
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(1, weight=1)

        # ==========================================
        # 1. ENCABEZADO INSTITUCIONAL
        # ==========================================
        encabezado = ttk.Frame(contenedor, padding=15)
        encabezado.grid(row=0, column=0, sticky="ew")
        encabezado.columnconfigure(1, weight=1)

        titulo_frame = ttk.Frame(encabezado)
        titulo_frame.pack(side="left")

        ttk.Label(
            titulo_frame, 
            text="Configuración", 
            font=("Segoe UI", 15, "bold"), 
            foreground="#A93226"
        ).pack(anchor="w")

        ttk.Label(
            titulo_frame, 
            text="Parámetros institucionales, períodos académicos y opciones de respaldo", 
            font=("Segoe UI", 9, "italic"), 
            foreground="#7F8C8D"
        ).pack(anchor="w", pady=(2, 0))

        # Botón para volver al Dashboard

        self.btn_volver = ttk.Button(
            encabezado, text="Volver al Panel", command=self._on_volver_click
        )
        self.btn_volver.pack(side="right", padx=5)

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

        ttk.Label(
            marco_logo, 
            text="Imagen actual utilizada en el sistema (logo.png):", 
            font=("Segoe UI", 9), 
            foreground="#566573"
        ).pack(anchor="w", pady=(0, 10))

        self.lbl_estado_logo = ttk.Label(marco_logo, text="Archivo cargado correctamente en el directorio", font=("Segoe UI", 9, "bold"), foreground="#27AE60")
        self.lbl_estado_logo.pack(anchor="w", pady=(0, 15))

        btn_cambiar_logo = ttk.Button(marco_logo, text="📂 Seleccionar Nuevo Logo...", command=self._on_seleccionar_logo)
        btn_cambiar_logo.pack(anchor="w", fill="x", pady=5)

        # Botón guardar cambios plantel
        btn_guardar_plantel = ttk.Button(pestana_plantel, text="Guardar Cambios Institucionales", command=self._on_guardar_plantel)
        btn_guardar_plantel.grid(row=1, column=0, columnspan=2, sticky="e", pady=(15, 0))

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
        chk_bloquear = ttk.Checkbutton(marco_academico, text="Bloquear carga de notas automáticamente al cerrar el lapso escolar", variable=self.var_bloquear_lapso)
        chk_bloquear.grid(row=3, column=0, columnspan=2, sticky="w", pady=15, padx=5)

        btn_guardar_academico = ttk.Button(pestana_academica, text="Actualizar Parámetros Académicos", command=self._on_guardar_academico)
        btn_guardar_academico.pack(anchor="e", pady=(15, 0))

        # ==========================================
        # PESTAÑA 3: RESPALDO Y SEGURIDAD
        # ==========================================
        pestana_respaldo.columnconfigure(0, weight=1)

        marco_respaldo = ttk.LabelFrame(pestana_respaldo, text=" Gestión de Respaldo y Mantenimiento de Datos ", padding=15)
        marco_respaldo.pack(fill="both", expand=True)

        ttk.Label(
            marco_respaldo, 
            text="Genera copias de seguridad de la base de datos institucional o restaura información previa en caso de contingencia técnica.", 
            font=("Segoe UI", 9), 
            foreground="#566573"
        ).pack(anchor="w", pady=(0, 15))

        # Botones de respaldo
        btn_backup = ttk.Button(marco_respaldo, text="📥 Generar Respaldo Manual de la Base de Datos", command=self._on_generar_backup)
        btn_backup.pack(anchor="w", fill="x", pady=8, ipady=4)

        btn_restaurar = ttk.Button(marco_respaldo, text="📂 Restaurar Base de Datos desde un Archivo...", command=self._on_restaurar_backup)
        btn_restaurar.pack(anchor="w", fill="x", pady=8, ipady=4)

        btn_auditoria = ttk.Button(marco_respaldo, text="📋 Ver Registro de Auditoría y Bitácora del Sistema", command=self._on_ver_auditoria)
        btn_auditoria.pack(anchor="w", fill="x", pady=8, ipady=4)

    def _on_seleccionar_logo(self):
        """Permite buscar y seleccionar una nueva imagen para el logotipo."""
        archivo = filedialog.askopenfilename(
            title="Seleccionar Escudo Institucional",
            filetypes=[("Archivos de Imagen", "*.png;*.jpg;*.jpeg")]
        )
        if archivo:
            self.lbl_estado_logo.config(text=f"✅ Nuevo logo seleccionado: {os.path.basename(archivo)}")
            messagebox.showinfo("Imagen Seleccionada", "El archivo de imagen ha sido seleccionado con éxito. Guarde los cambios para aplicarlo.")

    def _on_guardar_plantel(self):
        """Guarda la información general de la institución."""
        messagebox.showinfo("Configuración Guardada", "Los datos institucionales del plantel han sido actualizados con éxito.")

    def _on_guardar_academico(self):
        """Guarda los parámetros de año escolar y notas."""
        messagebox.showinfo("Configuración Guardada", "Los parámetros del período escolar y evaluación han sido actualizados.")

    def _on_generar_backup(self):
        """Simula la creación de un respaldo."""
        messagebox.showinfo("Respaldo Exitoso", "La copia de seguridad de la base de datos se ha generado y guardado correctamente.")

    def _on_restaurar_backup(self):
        """Simula la restauración del sistema."""
        if messagebox.askyesno("Advertencia de Restauración", "¿Está seguro de sobreescribir los datos actuales con un respaldo externo?"):
            messagebox.showinfo("Restauración Completa", "El sistema se ha restaurado con éxito a partir del archivo seleccionado.")

    def _on_ver_auditoria(self):
        """Muestra ventana o aviso de auditoría."""
        messagebox.showinfo("Bitácora", "Abriendo el registro de auditoría y acciones de usuarios...")

    def _on_volver_click(self):
        """Cierra la vista de configuración y regresa al dashboard."""
        if messagebox.askyesno("Volver", "¿Desea regresar al panel principal?"):
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()  
    root.title("L.N. Evelia A. de Pimentel - Menú de Configuración")
    root.geometry("850x550")
    root.minsize(750, 500)
    
    app = VistaConfiguracion(parent=root, controlador=None)
    app.pack(fill="both", expand=True)
        
    root.mainloop()