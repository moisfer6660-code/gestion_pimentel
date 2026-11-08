import tkinter as tk
from tkinter import ttk, messagebox
from componentes import FormularioEstudiante, FormularioRepresentante

class VistaEstudiantesRegistro(ttk.Frame):
    
    """Vista principal que ensambla los moldes y gestiona la adaptabilidad (Scroll)."""

    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador  
        
        self._configurar_estilos()
        self._configurar_scroll(parent)
        self._construir_interfaz(self.scrollable_frame)

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', font=('Segoe UI', 10))
        style.configure('TButton', background='#2c3e50', foreground='white', padding=6)
        style.map('TButton', background=[('active', '#34495e')])

    def _configurar_scroll(self, parent):
        self.canvas = tk.Canvas(parent, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _construir_interfaz(self, contenedor):
        # 1. Instanciamos el molde de Estudiante
        ttk.Label(contenedor, text="Registro de Estudiantes", font=("Segoe UI", 13, "bold"), foreground="#A93226").pack(pady=5, anchor="w", padx=15)
        self.seccion_estudiante = FormularioEstudiante(contenedor)
        self.seccion_estudiante.pack(fill="x", padx=15, pady=5)

        # 2. Instanciamos el molde de Representante Principal
        ttk.Label(contenedor, text="Registro de Representantes", font=("Segoe UI", 13, "bold"), foreground="#A93226").pack(pady=5, anchor="w", padx=15)
        self.seccion_rep1 = FormularioRepresentante(contenedor, titulo=" Datos del Representante Principal ")
        self.seccion_rep1.pack(fill="x", padx=15, pady=5)

        # 3. Instanciamos el segundo molde opcional de Representante (Inicia oculto)
        self.seccion_rep2 = FormularioRepresentante(contenedor, titulo=" Datos del Segundo Representante (Opcional) ")

        # 4. Botonera y acciones
        btn_frame = ttk.Frame(contenedor)
        btn_frame.pack(fill="x", padx=15, pady=10)

        self.btn_toggle_rep2 = ttk.Button(
            btn_frame, 
            text="➕ Añadir otro representante (Opcional)", 
            command=self._toggle_segundo_representante
        )
        self.btn_toggle_rep2.pack(anchor="w", pady=(0, 10))

        acciones_frame = ttk.Frame(btn_frame)
        acciones_frame.pack(fill="x", pady=5)

        self.btn_guardar = ttk.Button(acciones_frame, text="Guardar Registro", command=self._on_guardar_click)
        self.btn_guardar.pack(side="left", padx=(0, 5))

        self.btn_limpiar = ttk.Button(acciones_frame, text="Vaciar casillas", command=self._corregir_formulario)
        self.btn_limpiar.pack(side="left", padx=5)

    def _toggle_segundo_representante(self):
        if self.seccion_rep2.winfo_ismapped():
            self.seccion_rep2.pack_forget()
            self.btn_toggle_rep2.configure(text="➕ Añadir otro representante (Opcional)")
        else:
            self.seccion_rep2.pack(fill="x", padx=15, pady=5, before=self.btn_toggle_rep2.master)
            self.btn_toggle_rep2.configure(text="➖ Quitar segundo representante")

    def _on_guardar_click(self):
        # Recolectamos datos invocando los métodos propios de cada molde
        datos = {
            "estudiante": self.seccion_estudiante.obtener_datos(),
            "representante_1": self.seccion_rep1.obtener_datos()
        }

        if self.seccion_rep2.winfo_ismapped():
            datos["representante_2"] = self.seccion_rep2.obtener_datos()
        
        if self.controlador:
            self.controlador.procesar_registro(datos)
        else:
            messagebox.showinfo("Información SOLID", f"Estructura limpia para JSONB:\n\n{datos}")

    def _corregir_formulario(self):
        self.seccion_estudiante.limpiar()
        self.seccion_rep1.limpiar()
        self.seccion_rep2.limpiar()


if __name__ == "__main__":
    root = tk.Tk()  
    root.title("Control de estudiantes")
    root.geometry("500x600")
    
    # Instanciamos correctamente la vista principal completa (que ya incluye por dentro estudiante y representantes)
    
    app = VistaEstudiantesRegistro(parent=root, controlador=None)
    app.pack(fill="both", expand=True)
        
    root.mainloop()