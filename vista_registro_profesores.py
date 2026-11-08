import tkinter as tk
from tkinter import ttk, messagebox
from componentes import FormularioRegistroProfesor

class VistaVentanaRegistroDocente(ttk.Frame):
    """Módulo de Interfaz Gráfica que ensambla el encabezado, la ventana y el formulario de componentes."""

    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self._construir_interfaz(self)

    def _construir_interfaz(self, contenedor):
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
            text="Registro y Expediente de Docentes", 
            font=("Segoe UI", 15, "bold"), 
            foreground="#A93226"
        ).pack(anchor="w")

        ttk.Label(
            titulo_frame, 
            text="Ingreso de información clave, asignación de cátedra y carga de documentación legal", 
            font=("Segoe UI", 9, "italic"), 
            foreground="#7F8C8D"
        ).pack(anchor="w", pady=(2, 0))

        btn_volver = ttk.Button(encabezado, text="Volver al Panel", command=self._on_volver_click)
        btn_volver.pack(side="right", padx=5)

        # ==========================================
        # 2. CUERPO (Instanciación del componente formulario)
        # ==========================================
        cuerpo = ttk.Frame(contenedor, padding=15)
        cuerpo.grid(row=1, column=0, sticky="nsew")
        cuerpo.columnconfigure(0, weight=1)
        cuerpo.rowconfigure(0, weight=1)

        # Se inserta el formulario modular desde componentes.py
        self.formulario = FormularioRegistroProfesor(cuerpo, self.controlador)
        self.formulario.grid(row=0, column=0, sticky="nsew")

        # ==========================================
        # 3. PANEL DE ACCIÓN INFERIOR
        # ==========================================
        panel_acciones = ttk.Frame(contenedor, padding=(15, 0, 15, 15))
        panel_acciones.grid(row=2, column=0, sticky="ew")

        btn_registrar = ttk.Button(panel_acciones, text="Guardar Expediente y Registrar Docente", command=self._on_guardar_registro)
        btn_registrar.pack(side="right", padx=5, ipady=4)

    def _on_guardar_registro(self):
        """Valida y procesa los datos obtenidos del componente formulario."""
        datos_docente = self.formulario.obtener_datos()
        
        cedula = datos_docente.get("Cédula de Identidad:")
        nombre = datos_docente.get("Apellidos y Nombres:")

        if not cedula or not nombre:
            messagebox.showerror("Campos Incompletos", "Es obligatorio ingresar la Cédula de Identidad y los Apellidos y Nombres del docente.")
            return

        # Aquí conectarías con tu lógica de base de datos (PostgreSQL / SQL Server)
        messagebox.showinfo("Registro Exitoso", f"El expediente del profesor {nombre} (Cédula: {cedula}) ha sido registrado con éxito.")

    def _on_volver_click(self):
        if messagebox.askyesno("Volver", "¿Desea regresar al panel principal?"):
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()  
    root.title("L.N Evelia A. de Pimentel - Registro y Expediente de Docentes")
    root.geometry("950x640")
    root.minsize(850, 580)
    
    app = VistaVentanaRegistroDocente(parent=root, controlador=None)
    app.pack(fill="both", expand=True)
        
    root.mainloop()