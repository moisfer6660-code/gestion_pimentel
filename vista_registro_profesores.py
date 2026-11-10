import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk
from componentes import FormularioRegistroProfesor
import ttkbootstrap as ttk
from ttkbootstrap.style import Style

class VistaVentanaRegistroDocente(ttk.Frame):
    """Módulo de Interfaz Gráfica para el registro y expediente de docentes con diseño institucional unificado."""

    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self.imagenes_referencia = []
        
        # Aplicar el estilo institucional unificado con fondo #EDECD1
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
        """Desplazamiento suave optimizado para eliminar tirones y rayados visuales."""
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
        contenedor.columnconfigure(0, weight=1)

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
            text="Registro y Expediente de Docentes", 
            font=("Segoe UI", 11, "bold"),
            fg="#1e293b",
            bg="#FFFFFF"
        ).pack(anchor="w", pady=(1, 2))

        tk.Label(
            marco_textos, 
            text="Ingreso de información clave, asignación de cátedra y carga de documentación legal", 
            font=("Segoe UI", 9, "italic"),
            fg="#64748b",
            bg="#FFFFFF"
        ).pack(anchor="w", pady=(0, 6))

        # Insignia interactiva sutil UPTMA
        badge_frame = tk.Frame(marco_textos, bg="#F8FAFC", padx=8, pady=4, highlightbackground="#fca5a5", highlightthickness=1)
        badge_frame.pack(anchor="w", pady=(2, 0))
        
        lbl_uptma = tk.Label(
            badge_frame, 
            text="🎓 UPTMA 2026-2027 · Sección 3401", 
            font=("Segoe UI", 8, "bold"),
            fg="#b91c1c",
            bg="#F8FAFC",
            cursor="hand2"
        )
        lbl_uptma.pack(anchor="center")
        
        badge_frame.bind("<Enter>", lambda e: (badge_frame.config(bg="#FEF2F2"), lbl_uptma.config(bg="#FEF2F2")))
        badge_frame.bind("<Leave>", lambda e: (badge_frame.config(bg="#F8FAFC"), lbl_uptma.config(bg="#F8FAFC")))
        badge_frame.bind("<Button-1>", lambda e: self._mostrar_creditos_autores())
        lbl_uptma.bind("<Button-1>", lambda e: self._mostrar_creditos_autores())
        self._aplicar_cursor_mano(badge_frame)
        self._aplicar_cursor_mano(lbl_uptma)

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
        # 2. CUERPO (Formulario de Profesor)
        # ==========================================
        cuerpo = ttk.Frame(contenedor)
        cuerpo.pack(fill="both", expand=True, pady=(0, 15))
        cuerpo.columnconfigure(0, weight=1)
        cuerpo.rowconfigure(0, weight=1)

        self.formulario = FormularioRegistroProfesor(cuerpo, self.controlador)
        self.formulario.pack(fill="both", expand=True)

        # ==========================================
        # 3. PANEL DE ACCIÓN INFERIOR
        # ==========================================
        panel_acciones = ttk.Frame(contenedor)
        panel_acciones.pack(fill="x", pady=(5, 10))

        btn_registrar = ttk.Button(panel_acciones, text="💾 Guardar Expediente y Registrar Docente", command=self._on_guardar_registro)
        btn_registrar.pack(side="right", padx=(8, 0), ipady=3)
        self._aplicar_cursor_mano(btn_registrar)

        btn_volver = ttk.Button(panel_acciones, text="⬅️ Volver al Panel", command=self._on_volver_click, bootstyle="secondary")
        btn_volver.pack(side="right", padx=8, ipady=3)
        self._aplicar_cursor_mano(btn_volver)

    def _mostrar_creditos_autores(self):
        """Cuadro emergente estilizado de créditos académicos con diseño limpio y profesional."""
        ventana_creditos = tk.Toplevel(self)
        ventana_creditos.title("Créditos del Sistema - UPTMA")
        ventana_creditos.geometry("480x440")
        ventana_creditos.configure(bg="#EDECD1")
        ventana_creditos.resizable(False, False)
        ventana_creditos.transient(self)
        ventana_creditos.grab_set()

        main_frame = tk.Frame(ventana_creditos, bg="#FFFFFF", padx=20, pady=20, highlightbackground="#b91c1c", highlightthickness=2)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(
            main_frame, 
            text="🏫 UPTMA 2026-2027 · Sección 3401", 
            font=("Segoe UI", 12, "bold"), 
            fg="#b91c1c", 
            bg="#FFFFFF"
        ).pack(anchor="center", pady=(0, 12))

        tk.Label(
            main_frame, 
            text="AUTORES DEL PROYECTO:", 
            font=("Segoe UI", 9, "bold"), 
            fg="#475569", 
            bg="#FFFFFF"
        ).pack(anchor="w", pady=(0, 4))

        autores = [
            "• Bravo, Jhordan",
            "• Chacín, Luis",
            "• Gonzales, Rafael",
            "• Torregroza, Josemith",
            "• Cordoba, Jose"
        ]

        for autor in autores:
            tk.Label(
                main_frame, 
                text=autor, 
                font=("Segoe UI", 9), 
                fg="#1e293b", 
                bg="#FFFFFF"
            ).pack(anchor="w", padx=10, pady=1)

        dev_frame = tk.Frame(main_frame, bg="#FEF2F2", padx=12, pady=10, highlightbackground="#fca5a5", highlightthickness=1)
        dev_frame.pack(fill="x", pady=(15, 10))

        tk.Label(
            dev_frame, 
            text="💻 PROGRAMADOR, DISEÑADOR Y DESARROLLADOR", 
            font=("Segoe UI", 9, "bold"), 
            fg="#b91c1c", 
            bg="#FEF2F2"
        ).pack(anchor="w")

        tk.Label(
            dev_frame, 
            text="Moisfer Enrique Urdaneta Barrios", 
            font=("Segoe UI", 10, "bold"), 
            fg="#0f172a", 
            bg="#FEF2F2"
        ).pack(anchor="w", pady=(2, 2))

        tk.Label(
            dev_frame, 
            text="GitHub: https://github.com/MoisferIT\nCorreo: moisferit.dev@gmail.com", 
            font=("Segoe UI", 8, "italic"), 
            fg="#334155", 
            bg="#FEF2F2",
            justify="left"
        ).pack(anchor="w")

        btn_cerrar = ttk.Button(main_frame, text="Cerrar", command=ventana_creditos.destroy, bootstyle="danger")
        btn_cerrar.pack(anchor="center", pady=(8, 0))
        self._aplicar_cursor_mano(btn_cerrar)

    def _on_guardar_registro(self):
        """Valida y procesa los datos obtenidos del componente formulario."""
        datos_docente = self.formulario.obtener_datos()
        
        cedula = datos_docente.get("Cédula de Identidad:")
        nombre = datos_docente.get("Apellidos y Nombres:")

        if not cedula or not nombre:
            messagebox.showerror("Campos Incompletos", "Es obligatorio ingresar la Cédula de Identidad y los Apellidos y Nombres del docente.", parent=self)
            return

        messagebox.showinfo("Registro Exitoso", f"El expediente del profesor {nombre} (Cédula: {cedula}) ha sido registrado con éxito.", parent=self)

    def _on_volver_click(self):
        if messagebox.askyesno("Volver", "¿Desea regresar al panel principal?", parent=self):
            self.master.destroy()

if __name__ == "__main__":
    root = ttk.Window(title="L.N. Evelia A. de Pimentel - Registro y Expediente de Docentes", themename="flatly", size=(1150, 720))
    root.configure(bg="#EDECD1")
    root.minsize(850, 580)
    
    app = VistaVentanaRegistroDocente(parent=root, controlador=None)
    app.pack(fill="both", expand=True, padx=12, pady=12)
        
    root.mainloop()