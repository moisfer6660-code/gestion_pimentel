import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from componentes import FormularioConfiguracionAcademica

class VistaAsignacionSecciones(ttk.Frame):
    
    """Vista principal para la asignación y creación de secciones por año y período."""
    
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
        
        # Forzamos el color de fondo institucional libre de grises en marcos y contenedores
        estilo_ttk.configure("TFrame", background="#f8fafc")
        estilo_ttk.configure("TLabelframe", background="#f8fafc", bordercolor="#cbd5e1")
        estilo_ttk.configure("TLabelframe.Label", background="#f8fafc", foreground="#1e293b", font=("Segoe UI", 9, "bold"))
        
        # Configuración de botones institucionales
        estilo_ttk.configure("TButton", padding=(10, 6), relief="flat", background="#b91c1c", borderwidth=0, font=("Segoe UI", 9, "bold"), foreground="#FFFFFF")
        estilo_ttk.map("TButton", background=[("active", "#991b1b"), ("pressed", "#7f1d1d")])

        estilo_ttk.configure("Accent.TButton", background="#32B855", foreground="#ffffff")
        estilo_ttk.map("Accent.TButton", background=[("active", "#289e47"), ("pressed", "#1e7835")])

        estilo_ttk.configure("Danger.TButton", background="#b91c1c", foreground="#ffffff")
        estilo_ttk.map("Danger.TButton", background=[("active", "#b91c1c"), ("pressed", "#7f1d1d")])

        estilo_ttk.configure("Secondary.TButton", background="#b91c1c", foreground="#ffffff")
        estilo_ttk.map("Secondary.TButton", background=[("active", "#b91c1c"), ("pressed", "#7f1d1d")])

    def _aplicar_cursor_mano(self, boton):
        """Asigna el cambio de cursor a formato de mano interactiva al pasar por encima."""
        boton.bind("<Enter>", lambda e: self.winfo_toplevel().config(cursor="hand2"))
        boton.bind("<Leave>", lambda e: self.winfo_toplevel().config(cursor=""))

    def _construir_interfaz(self, contenedor):
        contenedor.configure(style="TFrame")

        # Encabezado institucional con margen derecho protegido para el logotipo
        encabezado = ttk.Frame(contenedor, style="TFrame", height=75)
        encabezado.pack(fill="x", padx=(20, 190), pady=(15, 5))
        encabezado.pack_propagate(False)

        frame_titulos = ttk.Frame(encabezado, style="TFrame")
        frame_titulos.place(x=0, y=8)

        ttk.Label(
            frame_titulos, 
            text="Creación y asignación de secciones", 
            font=("Segoe UI", 22, "bold"), 
            foreground="#A93226",
            background="#f8fafc"
        ).pack(anchor="w")

        ttk.Label(
            frame_titulos,
            text="Panel de Configuración Académica",
            font=("Segoe UI", 11, "italic"),
            foreground="#64748b",
            background="#f8fafc"
        ).pack(anchor="w", pady=(1, 0))

        # Logotipo institucional grande en la esquina superior derecha
        try:
            ruta_logo = os.path.join(os.path.dirname(__file__), "logon.png")
            if os.path.exists(ruta_logo):
                imagen_pil = Image.open(ruta_logo).resize((170, 170), Image.Resampling.LANCZOS)
                self.imagen_logo = ImageTk.PhotoImage(imagen_pil)
                etiqueta_logo = ttk.Label(contenedor, image=self.imagen_logo, style="TLabel", background="#f8fafc")
                etiqueta_logo.place(relx=0.98, x=0, y=10, anchor="ne")
                etiqueta_logo.lift()
        except Exception as error_logo:
            print(f"No se pudo cargar el logo: {error_logo}")

        # Formulario de configuración integrado sin fondos grises
        self.form_config = FormularioConfiguracionAcademica(contenedor)
        self.form_config.pack(fill="x", padx=(20, 190), pady=10)

        # Panel de botones de acciones
        accion_botones = ttk.Frame(contenedor, style="TFrame")
        accion_botones.pack(fill="x", padx=(20, 190), pady=12)

        self.btn_crear = ttk.Button(
            accion_botones, 
            text="Crear Sección", 
            style="Accent.TButton",
            command=self._on_crear_seccion_click
        )
        self.btn_crear.pack(side="left", padx=(0, 8))
        self._aplicar_cursor_mano(self.btn_crear)

        self.btn_regresar = ttk.Button(
            accion_botones, 
            text="← Regresar al Menú", 
            style="Secondary.TButton",
            command=self._on_regresar
        )
        self.btn_regresar.pack(side="left", padx=8)
        self._aplicar_cursor_mano(self.btn_regresar)

        self.btn_cerrarsesion = ttk.Button(
            accion_botones,  
            text="Cerrar Sesión",
            style="Secondary.TButton",
            command=self._on_cerrar_sesion_click
        )
        self.btn_cerrarsesion.pack(side="left", padx=8)
        self._aplicar_cursor_mano(self.btn_cerrarsesion)

        self.btn_eliminar = ttk.Button(
            accion_botones, 
            text="Eliminar Seleccionada", 
            style="Danger.TButton",
            command=self._on_eliminar_click
        )
        self.btn_eliminar.pack(side="right", padx=(8, 0))
        self._aplicar_cursor_mano(self.btn_eliminar)

        # Tabla resumen (Treeview) con diseño limpio adaptado
        frame_tabla = ttk.LabelFrame(contenedor, text=" Secciones Académicas Activas ", padding=15, style="TLabelframe")
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        columnas = ("periodo", "anio", "seccion", "turno", "aula", "capacidad")
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=6)
        
        self.tree.heading("periodo", text="Período")
        self.tree.heading("anio", text="Año")
        self.tree.heading("seccion", text="Sec.")
        self.tree.heading("turno", text="Turno")
        self.tree.heading("aula", text="Aula")
        self.tree.heading("capacidad", text="Cap.")

        self.tree.column("periodo", width=110, anchor="center")
        self.tree.column("anio", width=90, anchor="center")
        self.tree.column("seccion", width=60, anchor="center")
        self.tree.column("turno", width=100, anchor="center")
        self.tree.column("aula", width=80, anchor="center")
        self.tree.column("capacidad", width=70, anchor="center")
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
        
        if self.controlador_externo:
            self.controlador_externo.guardar_seccion(datos)
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

    def _on_regresar(self):
        """Acción al presionar el botón Regresar al Menú."""
        if self.controlador_externo and hasattr(self.controlador_externo, "regresar_menu_principal"):
            self.controlador_externo.regresar_menu_principal()
        else:
            messagebox.showinfo("Navegación", "Regresando al menú principal...")

    def _on_cerrar_sesion_click(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar sesión?"):
            self.master.destroy()            

if __name__ == "__main__":
    root = tk.Tk()  
    root.title("Gestión Académica 2026 - Asignación de Secciones")
    root.geometry("820x650")
    
    app = VistaAsignacionSecciones(contenedor_principal=root, controlador_externo=None)
    app.pack(fill="both", expand=True)
        
    root.mainloop()