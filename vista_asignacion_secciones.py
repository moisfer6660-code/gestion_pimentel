import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.style import Style
from componentes import FormularioConfiguracionAcademica

class VistaAsignacionSecciones(ttk.Frame):
    
    """Vista principal para la asignación y creación de secciones con diseño institucional unificado #F3F3E0."""
    
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
        contenedor.rowconfigure(4, weight=1)

        # 1. Encabezado simétrico con Grid de 2 columnas (Títulos a la izquierda, Logo a la derecha)
        marco_encabezado = ttk.Frame(contenedor, padding=(20, 15, 20, 5))
        marco_encabezado.pack(fill="x")
        marco_encabezado.columnconfigure(0, weight=1)
        marco_encabezado.columnconfigure(1, weight=0)

        marco_titulos = ttk.Frame(marco_encabezado)
        marco_titulos.grid(row=0, column=0, sticky="w")

        etiqueta_titulo = tk.Label(
            marco_titulos, 
            text="Creación y asignación de secciones", 
            font=("Segoe UI", 22, "bold"), 
            fg="#b91c1c",
            bg=color_fondo
        )
        etiqueta_titulo.pack(anchor="w")

        etiqueta_subtitulo = tk.Label(
            marco_titulos,
            text="Panel de Configuración Académica",
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

        # 2. Formulario de configuración integrado con armonía visual
        self.form_config = FormularioConfiguracionAcademica(contenedor)
        self.form_config.pack(fill="x", padx=20, pady=8)

        # 3. Panel de botones de acciones unificados
        accion_botones = ttk.Frame(contenedor, padding=(0, 5))
        accion_botones.pack(fill="x", padx=20, pady=5)

        self.btn_crear = ttk.Button(
            accion_botones, 
            text="➕ Crear Sección", 
            command=self._on_crear_seccion_click
        )
        self.btn_crear.pack(side="left", padx=(0, 6))
        self._aplicar_cursor_mano(self.btn_crear)

        self.btn_regresar = ttk.Button(
            accion_botones, 
            text="← Regresar", 
            bootstyle="secondary",
            command=self._on_regresar
        )
        self.btn_regresar.pack(side="left", padx=6)
        self._aplicar_cursor_mano(self.btn_regresar)

        self.btn_cerrarsesion = ttk.Button(
            accion_botones,  
            text="Cerrar Sesión",
            bootstyle="secondary",
            command=self._on_cerrar_sesion_click
        )
        self.btn_cerrarsesion.pack(side="left", padx=6)
        self._aplicar_cursor_mano(self.btn_cerrarsesion)

        self.btn_eliminar = ttk.Button(
            accion_botones, 
            text="🗑️ Eliminar Seleccionada", 
            bootstyle="danger",
            command=self._on_eliminar_click
        )
        self.btn_eliminar.pack(side="right", padx=(6, 0))
        self._aplicar_cursor_mano(self.btn_eliminar)

        # 4. Tabla resumen (Treeview) con diseño limpio y adaptado
        frame_tabla = ttk.LabelFrame(contenedor, text=" Secciones Académicas Activas ", padding=12)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=(5, 15))

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
    root = ttk.Window(title="Gestión Académica 2026 - Asignación de Secciones", themename="flatly", size=(850, 680))
    root.configure(bg="#F3F3E0")
    
    app = VistaAsignacionSecciones(contenedor_principal=root, controlador_externo=None)
    app.pack(fill="both", expand=True, padx=10, pady=10)
        
    root.mainloop()