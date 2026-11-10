import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk
from componentes import FormularioEstudiante, FormularioRepresentante
import ttkbootstrap as ttk
from ttkbootstrap.style import Style

class VistaEstudiantesRegistro(ttk.Frame):
    """Vista principal que ensambla los moldes de estudiantes y representantes con diseño institucional unificado y scroll fluido."""

    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador  
        self.imagenes_referencia = []
        
        self.estilo_app = Style(theme="flatly")
        self._configurar_estilos_institucionales()
        self._configurar_scroll(parent)
        self._construir_interfaz(self.scrollable_frame)

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

    def _aplicar_cursor_mano(self, widget):
        widget.bind("<Enter>", lambda e: self.winfo_toplevel().config(cursor="hand2"))
        widget.bind("<Leave>", lambda e: self.winfo_toplevel().config(cursor=""))

    def _on_mouse_wheel(self, event):
        """Desplazamiento suave optimizado para eliminar tirones."""
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

    def _configurar_scroll(self, parent):
        color_fondo = "#EDECD1"
        self.canvas = tk.Canvas(parent, highlightthickness=0, bg=color_fondo)
        self.scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = ttk.Frame(self.canvas, padding=15)
        self.scrollable_frame.configure(style="TFrame")

        def _actualizar_region_scroll(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.scrollable_frame.bind("<Configure>", _actualizar_region_scroll)

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        def _ajustar_ancho_canvas(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)

        self.canvas.bind('<Configure>', _ajustar_ancho_canvas)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)
        self.canvas.bind_all("<Button-4>", self._on_mouse_wheel)
        self.canvas.bind_all("<Button-5>", self._on_mouse_wheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _construir_interfaz(self, contenedor):
        color_fondo = "#EDECD1"
        
        # ==========================================
        # 1. ENCABEZADO INSTITUCIONAL SIMÉTRICO
        # ==========================================
        header_card = tk.Frame(contenedor, bg="#FFFFFF", padx=25, pady=18, highlightbackground="#d1d5db", highlightthickness=1)
        header_card.pack(fill="x", pady=(0, 15))
        header_card.columnconfigure(0, weight=1)
        header_card.columnconfigure(1, weight=0)

        marco_textos = tk.Frame(header_card, bg="#FFFFFF")
        marco_textos.grid(row=0, column=0, sticky="w")

        tk.Label(
            marco_textos, 
            text="L.N. EVELIA A. DE PIMENTEL", 
            font=("Impact", 28),
            fg="#b91c1c",
            bg="#FFFFFF"
        ).pack(anchor="w")

        tk.Label(
            marco_textos, 
            text="Directorio y Registro Oficial de Estudiantes", 
            font=("Segoe UI", 10, "bold italic"),
            fg="#64748b",
            bg="#FFFFFF"
        ).pack(anchor="w", pady=(1, 6))

        # Logotipo limpio de 150x150 px
        marco_logo = tk.Frame(header_card, bg="#FFFFFF", width=150, height=150)
        marco_logo.grid(row=0, column=1, sticky="e", padx=(20, 0))
        marco_logo.pack_propagate(False)

        logo_cargado = False
        try:
            rutas_posibles = [
                os.path.join(os.path.dirname(__file__), "logo.png"),
                "logo.png",
                os.path.join(os.path.dirname(__file__), "logon.png"),
                "logon.png"
            ]
            for ruta in rutas_posibles:
                if os.path.exists(ruta):
                    imagen_pil = Image.open(ruta)
                    imagen_pil.thumbnail((140, 140), Image.Resampling.LANCZOS)
                    self.imagen_logo = ImageTk.PhotoImage(imagen_pil)
                    self.imagenes_referencia.append(self.imagen_logo)
                    
                    etiqueta_logo = tk.Label(marco_logo, image=self.imagen_logo, bg="#FFFFFF")
                    etiqueta_logo.pack(expand=True, anchor="center")
                    logo_cargado = True
                    break
        except Exception as e:
            print(f"Error cargando logo: {e}")

        if not logo_cargado:
            tk.Label(marco_logo, text="🏫", font=("Segoe UI", 45), bg="#FFFFFF").pack(expand=True, anchor="center")

        # ==========================================
        # 2. FORMULARIOS DE REGISTRO
        # ==========================================
        self.seccion_estudiante = FormularioEstudiante(contenedor)
        self.seccion_estudiante.pack(fill="x", pady=(0, 12))

        self.seccion_rep1 = FormularioRepresentante(contenedor, titulo=" Datos del Representante Principal ")
        self.seccion_rep1.pack(fill="x", pady=(0, 12))

        self.seccion_rep2 = FormularioRepresentante(contenedor, titulo=" Datos del Segundo Representante (Opcional) ")

        # ==========================================
        # 3. BOTONERA Y ACCIONES
        # ==========================================
        btn_frame = ttk.Frame(contenedor)
        btn_frame.pack(fill="x", pady=(5, 10))

        self.btn_toggle_rep2 = ttk.Button(
            btn_frame, 
            text="➕ Añadir otro representante (Opcional)", 
            command=self._toggle_segundo_representante,
            bootstyle="secondary"
        )
        self.btn_toggle_rep2.pack(anchor="w", pady=(0, 12))
        self._aplicar_cursor_mano(self.btn_toggle_rep2)

        acciones_frame = ttk.Frame(btn_frame)
        acciones_frame.pack(fill="x", pady=5)

        self.btn_guardar = ttk.Button(acciones_frame, text="💾 Guardar Registro", command=self._on_guardar_click)
        self.btn_guardar.pack(side="left", padx=(0, 8))
        self._aplicar_cursor_mano(self.btn_guardar)

        self.btn_limpiar = ttk.Button(acciones_frame, text="🧹 Vaciar Casillas", command=self._corregir_formulario, bootstyle="secondary")
        self.btn_limpiar.pack(side="left", padx=8)
        self._aplicar_cursor_mano(self.btn_limpiar)

    def _toggle_segundo_representante(self):
        if self.seccion_rep2.winfo_ismapped():
            self.seccion_rep2.pack_forget()
            self.btn_toggle_rep2.configure(text="➕ Añadir otro representante (Opcional)")
        else:
            self.seccion_rep2.pack(fill="x", pady=(0, 12), before=self.btn_toggle_rep2.master)
            self.btn_toggle_rep2.configure(text="➖ Quitar segundo representante")

    def _on_guardar_click(self):
        datos = {
            "estudiante": self.seccion_estudiante.obtener_datos(),
            "representante_1": self.seccion_rep1.obtener_datos()
        }

        if self.seccion_rep2.winfo_ismapped():
            datos["representante_2"] = self.seccion_rep2.obtener_datos()
        
        if self.controlador:
            self.controlador.procesar_registro(datos)
        else:
            messagebox.showinfo("Registro Exitoso", "Los datos del estudiante han sido procesados correctamente.", parent=self)

    def _corregir_formulario(self):
        if messagebox.askyesno("Limpiar Formulario", "¿Desea vaciar todos los campos ingresados?", parent=self):
            self.seccion_estudiante.limpiar()
            self.seccion_rep1.limpiar()
            self.seccion_rep2.limpiar()

if __name__ == "__main__":
    root = ttk.Window(title="L.N. Evelia A. de Pimentel - Registro de Estudiantes", themename="flatly", size=(1150, 720))
    root.configure(bg="#EDECD1")
    root.minsize(850, 550)
    
    app = VistaEstudiantesRegistro(parent=root, controlador=None)
    app.pack(fill="both", expand=True, padx=12, pady=12)
        
    root.mainloop()