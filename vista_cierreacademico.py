import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class VistaCierreAcademico(ttk.Frame):
    """Interfaz para la gestión de cierres de lapso y transiciones de año escolar con clave de seguridad."""

    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self._construir_interfaz(self)

    def _construir_interfaz(self, contenedor):
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(1, weight=1)

        # 1. Encabezado
        encabezado = ttk.Frame(contenedor, padding=15)
        encabezado.grid(row=0, column=0, sticky="ew")
        encabezado.columnconfigure(1, weight=1)

        titulo_frame = ttk.Frame(encabezado)
        titulo_frame.pack(side="left")

        ttk.Label(
            titulo_frame, 
            text="Procesos de cierre", 
            font=("Segoe UI", 15, "bold"), 
            foreground="#A93226"
        ).pack(anchor="w")

        ttk.Label(
            titulo_frame, 
            text="Gestión de cierres de lapsos, bloqueo de actas y promoción de año escolar", 
            font=("Segoe UI", 9, "italic"), 
            foreground="#7F8C8D"
        ).pack(anchor="w", pady=(2, 0))

        btn_volver = ttk.Button(encabezado, text="Volver", command=self._on_volver_click)
        btn_volver.pack(side="right", padx=5)

        # 2. Cuerpo con opciones de cierre
        cuerpo = ttk.Frame(contenedor, padding=20)
        cuerpo.grid(row=1, column=0, sticky="nsew")
        cuerpo.columnconfigure((0, 1), weight=1)

        # SECCIÓN A: Cierre de Lapso Actual
        marco_lapso = ttk.LabelFrame(cuerpo, text=" Cierre del lapso vigente ", padding=15)
        marco_lapso.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ttk.Label(
            marco_lapso, 
            text="Lapso actual en curso: I Lapso (Octubre - Diciembre)\n\n"
                 "Al cerrar el lapso:\n"
                 "• Se bloqueará la carga y edición de notas para los docentes.\n"
                 "• Se calcularán los promedios parciales automáticos.\n"
                 "• Se habilitará la generación de boletines informativos.",
            font=("Segoe UI", 9),
            wraplength=320
        ).pack(anchor="w", pady=(0, 15))

        self.btn_cerrar_lapso = ttk.Button(
            marco_lapso, text="Ejecutar cierre del I Lapso", command=self._on_ejecutar_cierre_lapso
        )
        self.btn_cerrar_lapso.pack(anchor="w", fill="x", ipady=4)

        # SECCIÓN B: Cierre y Transición de Año Escolar
        marco_anio = ttk.LabelFrame(cuerpo, text=" Cierre y transición de año escolar ", padding=15)
        marco_anio.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        ttk.Label(
            marco_anio, 
            text="Año escolar activo: 2025-2026\n\n"
                 "Al cerrar el año escolar:\n"
                 "• Se evaluará la promoción de cada alumno (Aprobado/Repitiente).\n"
                 "• Se archivarán las actas definitivas en la base de datos.\n"
                 "• Se abrirá formalmente el período 2026-2027.",
            font=("Segoe UI", 9),
            wraplength=320
        ).pack(anchor="w", pady=(0, 15))

        self.btn_cerrar_anio = ttk.Button(
            marco_anio, text="Procesar Cierre del Año Escolar 2025-2026", command=self._on_ejecutar_cierre_anio
        )
        self.btn_cerrar_anio.pack(anchor="w", fill="x", ipady=4)

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
            return # El usuario canceló la ventana
        
        # Simulación de validación de clave (aquí validarías con tu BD o variable de control)
        CLAVE_MAESTRA = "1234" # Cambiar por tu lógica real de verificación
        
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

        CLAVE_MAESTRA = "1234" # Cambiar por tu lógica real de verificación

        if clave_ingresada == CLAVE_MAESTRA:
            respuesta = messagebox.showwarning(
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
        if messagebox.askyesno("Volver", "¿Desea regresar al panel principal?"):
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()  
    root.title("L.N. Evelia A. de Pimentel - Gestión de cierres academicos")
    root.geometry("800x450")
    
    app = VistaCierreAcademico(parent=root, controlador=None)
    app.pack(fill="both", expand=True)
        
    root.mainloop()
    