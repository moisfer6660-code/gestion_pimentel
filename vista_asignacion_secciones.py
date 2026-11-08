import tkinter as tk
from tkinter import ttk, messagebox
from componentes import FormularioConfiguracionAcademica

class VistaAsignacionSecciones(ttk.Frame):
    
    """Vista principal para la asignación y creación de secciones por año y período."""
    
    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self._construir_interfaz(self)

    def _construir_interfaz(self, contenedor):
        encabezado = ttk.Frame(contenedor)
        encabezado.pack(fill="x", padx=20, pady=15)

        ttk.Label(
            encabezado, 
            text="Creación y asignación de secciones", 
            font=("Arial", 14, "bold"), 
            foreground="#A93226"
        ).pack(side="left")

        # Instanciamos el molde del componente dentro de la vista
        self.form_config = FormularioConfiguracionAcademica(contenedor)
        self.form_config.pack(fill="x", padx=20, pady=5)

        # para dar botones  para de acciones
        accion_botones = ttk.Frame(contenedor)
        accion_botones.pack(fill="x", padx=20, pady=12)

        self.btn_crear = ttk.Button(
            accion_botones, 
            text="Crear Sección", 
            command=self._on_crear_seccion_click
        )
        self.btn_crear.pack(side="left", padx=(0, 8))

        self.btn_limpiar = ttk.Button(
            accion_botones, 
            text="Limpiar Casillas", 
            command=self.form_config.limpiar
        )
        self.btn_limpiar.pack(side="left", padx=8)

        self.btn_eliminar = ttk.Button(
            accion_botones, 
            text="Eliminar Seleccionada", 
            command=self._on_eliminar_click
        )
        self.btn_eliminar.pack(side="right", padx=(8, 0))

        self.btn_cerrarsesion = ttk.Button(
            accion_botones,  
            text="Cerrar Sesión",
            command=self._on_cerrar_sesion_click
        )
        self.btn_cerrarsesion.pack(side="left", padx=(8, 0))

        # Tabla resumen (Treeview)
        
        frame_tabla = ttk.LabelFrame(contenedor, text=" Secciones Académicas Activas ", padding=15)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        columnas = ("periodo", "anio", "seccion", "turno", "aula", "capacidad")
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=6)
        
        self.tree.heading("periodo", text="Período")
        self.tree.heading("anio", text="Año")
        self.tree.heading("seccion", text="Sec.")
        self.tree.heading("turno", text="Turno")
        self.tree.heading("aula", text="Aula")
        self.tree.heading("capacidad", text="Cap.")

        self.tree.column("periodo", width=100, anchor="center")
        self.tree.column("anio", width=80, anchor="center")
        self.tree.column("seccion", width=50, anchor="center")
        self.tree.column("turno", width=90, anchor="center")
        self.tree.column("aula", width=70, anchor="center")
        self.tree.column("capacidad", width=60, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def _on_crear_seccion_click(self):
        datos = self.form_config.obtener_datos()

        for item in self.tree.get_children():
            valores = self.tree.item(item, "values")
            if valores[0] == datos["periodo"] and valores[1] == datos["anio"] and valores[2] == datos["seccion"]:
                messagebox.showwarning("Duplicado", f"La sección {datos['anio']} - '{datos['seccion']}' ya existe en este período.")
                return

        self.tree.insert("", "end", values=(
            datos["periodo"], datos["anio"], datos["seccion"], 
            datos["turno"], datos["aula"], datos["capacidad"]
        ))
        
        if self.controlador:
            self.controlador.guardar_seccion(datos)
        else:
            messagebox.showinfo("Éxito", "Sección creada y añadida a la vista correctamente.")

    def _on_eliminar_click(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione una sección de la tabla para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Desea eliminar la sección seleccionada?"):
            for item in seleccion:
                self.tree.delete(item)

    def _on_cerrar_sesion_click(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar sesión?"):
            self.master.destroy()            

if __name__ == "__main__":
    root = tk.Tk()  
    root.title("Gestión academica 2026 - Asignación de secciones")
    root.geometry("700x650")
    
    app = VistaAsignacionSecciones(parent=root, controlador=None)
    app.pack(fill="both", expand=True)
        
    root.mainloop()