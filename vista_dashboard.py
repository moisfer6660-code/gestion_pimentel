import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.style import Style

class VistaDashboard(ttk.Frame):
    """Dashboard principal del sistema académico con renderizado optimizado anti-parpadeo y diseño institucional impecable."""
    
    def __init__(self, parent, controlador=None, usuario_actual=None):
        super().__init__(parent)
        self.controlador = controlador
        
        self.usuario_actual = usuario_actual or {
            "usuario": "cmendoza",
            "nombre": "Prof. Carlos Mendoza",
            "rol": "Docente / Administrador Parcial",
            "modulos_permitidos": [
                "Directorio de Alumnos",
                "Control de Notas",
                "Control de Secciones"
            ]
        }
        
        self.imagenes_referencia = []
        
        # Configuración del tema y paleta institucional unificada (#EDECD1)
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

    def _aplicar_cursor_mano(self, widget):
        widget.bind("<Enter>", lambda e: self.winfo_toplevel().config(cursor="hand2"))
        widget.bind("<Leave>", lambda e: self.winfo_toplevel().config(cursor=""))

    def _on_mouse_wheel(self, event):
        """Desplazamiento suave optimizado para Windows que elimina cualquier tirón o rayado visual."""
        if event.delta:
            self.canvas_principal.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            if event.num == 4:
                self.canvas_principal.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas_principal.yview_scroll(1, "units")

    def _construir_interfaz(self, contenedor):
        color_fondo = "#EDECD1"
        contenedor.configure(style="TFrame")
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(0, weight=1)

        # Contenedor principal con doble búfer lógico para evitar parpadeos
        self.canvas_principal = tk.Canvas(contenedor, highlightthickness=0, bg=color_fondo)
        self.scrollbar_vertical = ttk.Scrollbar(contenedor, orient="vertical", command=self.canvas_principal.yview)
        
        self.scrollable_frame = ttk.Frame(self.canvas_principal, padding=15)
        self.scrollable_frame.configure(style="TFrame")

        # Configuración precisa del área de scroll para sincronizar el renderizado
        def _actualizar_region_scroll(event):
            self.canvas_principal.configure(scrollregion=self.canvas_principal.bbox("all"))

        self.scrollable_frame.bind("<Configure>", _actualizar_region_scroll)

        self.window_id = self.canvas_principal.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas_principal.configure(yscrollcommand=self.scrollbar_vertical.set)

        # Ajuste fluido del ancho sin sobrecargar el procesador gráfico
        def _ajustar_ancho_canvas(event):
            self.canvas_principal.itemconfig(self.window_id, width=event.width)

        self.canvas_principal.bind('<Configure>', _ajustar_ancho_canvas)

        # Vincular eventos de scroll para una animación limpia y sin artefactos
        self.canvas_principal.bind_all("<MouseWheel>", self._on_mouse_wheel)
        self.canvas_principal.bind_all("<Button-4>", self._on_mouse_wheel)
        self.canvas_principal.bind_all("<Button-5>", self._on_mouse_wheel)

        self.canvas_principal.pack(side="left", fill="both", expand=True)
        self.scrollbar_vertical.pack(side="right", fill="y")

        self.scrollable_frame.columnconfigure(0, weight=1)

        # ==========================================
        # 1. BARRA SUPERIOR DE SESIÓN
        # ==========================================
        barra_superior = ttk.Frame(self.scrollable_frame)
        barra_superior.pack(fill="x", pady=(0, 8))
        barra_superior.columnconfigure(0, weight=1)

        info_sesion = f"👤 Sesión activa: {self.usuario_actual['nombre']}  |  Usuario: {self.usuario_actual['usuario']}  ({self.usuario_actual['rol']})"
        tk.Label(
            barra_superior, 
            text=info_sesion, 
            font=("Segoe UI", 9, "bold"), 
            fg="#475569",
            bg=color_fondo
        ).pack(side="left", anchor="w")

        btn_salir = ttk.Button(barra_superior, text="🚪 Cerrar Sesión", command=self._on_cerrar_sesion, bootstyle="secondary")
        btn_salir.pack(side="right", anchor="e")
        self._aplicar_cursor_mano(btn_salir)

        # ==========================================
        # 2. ENCABEZADO CON LOGO Y TÍTULO IMPOBENTE
        # ==========================================
        header_card = tk.Frame(self.scrollable_frame, bg="#FFFFFF", padx=25, pady=18, highlightbackground="#d1d5db", highlightthickness=1)
        header_card.pack(fill="x", pady=(0, 12))
        header_card.columnconfigure(0, weight=1)
        header_card.columnconfigure(1, weight=0)

        marco_textos = tk.Frame(header_card, bg="#FFFFFF")
        marco_textos.grid(row=0, column=0, sticky="w")

        tk.Label(
            marco_textos, 
            text="L.N. EVELIA A. DE PIMENTEL", 
            font=("Impact", 30),
            fg="#b91c1c",
            bg="#FFFFFF"
        ).pack(anchor="w")

        tk.Label(
            marco_textos, 
            text="Sistema Integral de Gestión Institucional y Académica", 
            font=("Segoe UI", 10, "bold italic"),
            fg="#64748b",
            bg="#FFFFFF"
        ).pack(anchor="w", pady=(1, 6))

        # Insignia interactiva con diseño refinado y estético
        badge_frame = tk.Frame(marco_textos, bg="#F8FAFC", padx=10, pady=5, highlightbackground="#fca5a5", highlightthickness=1)
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

        # Logotipo limpio de 160x160 px
        marco_logo = tk.Frame(header_card, bg="#FFFFFF", width=160, height=160)
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
                    imagen_pil.thumbnail((150, 150), Image.Resampling.LANCZOS)
                    self.imagen_logo = ImageTk.PhotoImage(imagen_pil)
                    self.imagenes_referencia.append(self.imagen_logo)
                    
                    etiqueta_logo = tk.Label(marco_logo, image=self.imagen_logo, bg="#FFFFFF")
                    etiqueta_logo.pack(expand=True, anchor="center")
                    logo_cargado = True
                    break
        except Exception as e:
            print(f"Error cargando logo: {e}")

        if not logo_cargado:
            tk.Label(marco_logo, text="🏫", font=("Segoe UI", 50), bg="#FFFFFF").pack(expand=True, anchor="center")

        # ==========================================
        # 3. SECCIÓN DE ESTADÍSTICAS (KPIs)
        # ==========================================
        stats_frame = ttk.LabelFrame(self.scrollable_frame, text=" Resumen y Estadísticas del Plantel ", padding=10)
        stats_frame.pack(fill="x", pady=(0, 12))
        stats_frame.columnconfigure((0, 1, 2), weight=1)

        self._crear_tarjeta_stat(stats_frame, "👨‍🎓 Total Estudiantes", "148 Activos", "Matrícula general", 0)
        self._crear_tarjeta_stat(stats_frame, "🏫 Secciones Registradas", "12 Secciones", "Turnos activos", 1)
        total_asignados = len(self.usuario_actual["modulos_permitidos"])
        self._crear_tarjeta_stat(stats_frame, "🔐 Sus Módulos", f"{total_asignados} Disponibles", "Permisos actuales", 2)

        # ==========================================
        # 4. MÓDULOS ACADÉMICOS (GRILLA COMPACTA)
        # ==========================================
        self.modulos_container = ttk.LabelFrame(self.scrollable_frame, text=" Módulos Académicos Autorizados ", padding=12)
        self.modulos_container.pack(fill="both", expand=True, pady=(0, 10))
        
        self.modulos_container.columnconfigure((0, 1, 2), weight=1)

        catalogo_modulos = [
            {
                "nombre": "Directorio de Alumnos",
                "desc": "Inscripción, datos personales, expedientes detallados y estatus de los estudiantes.",
                "icono": "📂",
                "etiqueta_btn": "Abrir directorio",
                "comando": self._abrir_directorio_alumnos
            },
            {
                "nombre": "Control de Notas",
                "desc": "Planilla interactiva para cálculo automatizado de calificaciones y promedios.",
                "icono": "📊",
                "etiqueta_btn": "Gestionar Notas",
                "comando": self._abrir_control_notas
            },
            {
                "nombre": "Control de Secciones",
                "desc": "Configuración de capacidad de salones, distribución de años y turnos escolares.",
                "icono": "🏫",
                "etiqueta_btn": "Ver Secciones",
                "comando": self._abrir_control_secciones
            },
            {
                "nombre": "Control de Profesores y Materias",
                "desc": "Asignación de docentes titulares por cátedra, año, periodo y sección.",
                "icono": "👥",
                "etiqueta_btn": "Asignación académica",
                "comando": self._abrir_control_profesores
            },
            {
                "nombre": "Control de Usuarios",
                "desc": "Gestión de credenciales de acceso, contraseñas y permisos modulares.",
                "icono": "🔐",
                "etiqueta_btn": "Administrar Accesos",
                "comando": self._abrir_control_usuarios
            }
        ]

        columna_indice = 0
        fila_indice = 0
        modulos_visibles_count = 0

        for modulo in catalogo_modulos:
            if modulo["nombre"] in self.usuario_actual["modulos_permitidos"]:
                self._crear_tarjeta_modulo(self.modulos_container, modulo, fila_indice, columna_indice)
                columna_indice += 1
                modulos_visibles_count += 1
                if columna_indice > 2:
                    columna_indice = 0
                    fila_indice += 1

        if modulos_visibles_count == 0:
            tk.Label(
                self.modulos_container, 
                text="⚠️ Su usuario no tiene módulos autorizados asignados en este momento.", 
                font=("Segoe UI", 10, "bold"), 
                fg="#b91c1c",
                bg=color_fondo
            ).grid(row=0, column=0, columnspan=3, pady=15)

        # ==========================================
        # 5. BARRA INFERIOR CON TUERCA DE CONFIGURACIÓN
        # ==========================================
        barra_inferior = ttk.Frame(self.scrollable_frame, padding=(0, 5, 0, 0))
        barra_inferior.pack(fill="x", pady=(5, 0))
        barra_inferior.columnconfigure(0, weight=1)

        btn_config = ttk.Button(
            barra_inferior, 
            text="⚙️ Configuración del Sistema", 
            command=self._abrir_configuracion,
            bootstyle="secondary"
        )
        btn_config.pack(side="right")
        self._aplicar_cursor_mano(btn_config)

    def _crear_tarjeta_stat(self, parent, titulo, valor, subtitulo, col):
        card = tk.Frame(parent, bg="#FFFFFF", padx=10, pady=10, highlightbackground="#cbd5e1", highlightthickness=1)
        card.grid(row=0, column=col, sticky="nsew", padx=5)
        
        tk.Label(card, text=titulo, font=("Segoe UI", 8, "bold"), fg="#64748b", bg="#FFFFFF").pack(anchor="center")
        tk.Label(card, text=valor, font=("Segoe UI", 14, "bold"), fg="#b91c1c", bg="#FFFFFF").pack(anchor="center", pady=(2, 1))
        tk.Label(card, text=subtitulo, font=("Segoe UI", 7, "italic"), fg="#94a3b8", bg="#FFFFFF").pack(anchor="center")

    def _crear_tarjeta_modulo(self, parent, datos_mod, row, col):
        card = tk.Frame(parent, bg="#FFFFFF", padx=12, pady=12, highlightbackground="#cbd5e1", highlightthickness=1)
        card.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)
        card.columnconfigure(0, weight=1)

        tk.Label(card, text=datos_mod["icono"], font=("Segoe UI", 22), bg="#FFFFFF").pack(anchor="center", pady=(0, 4))
        tk.Label(card, text=datos_mod["nombre"], font=("Segoe UI", 10, "bold"), fg="#1e293b", bg="#FFFFFF", anchor="center").pack(anchor="center", pady=(0, 2))
        
        lbl_desc = tk.Label(card, text=datos_mod["desc"], font=("Segoe UI", 8), fg="#64748b", bg="#FFFFFF", wraplength=190, justify="center")
        lbl_desc.pack(anchor="center", pady=(0, 10), fill="x", expand=True)
        
        btn_entrar = ttk.Button(card, text=datos_mod["etiqueta_btn"], command=datos_mod["comando"])
        btn_entrar.pack(anchor="center", fill="x", ipady=2)
        self._aplicar_cursor_mano(btn_entrar)

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

    def _abrir_directorio_alumnos(self):
        messagebox.showinfo("Navegación", "Abriendo módulo: Directorio de Alumnos...", parent=self)

    def _abrir_control_notas(self):
        messagebox.showinfo("Navegación", "Abriendo módulo: Control de Notas...", parent=self)

    def _abrir_control_secciones(self):
        messagebox.showinfo("Navegación", "Abriendo el módulo: Control de Secciones...", parent=self)

    def _abrir_control_profesores(self):
        messagebox.showinfo("Navegación", "Abriendo el módulo: Control de Profesores...", parent=self)

    def _abrir_control_usuarios(self):
        messagebox.showinfo("Navegación", "Abriendo el módulo: Control de Usuarios...", parent=self)

    def _abrir_configuracion(self):
        messagebox.showinfo("Configuración", "Abriendo módulo de Configuración General...", parent=self)

    def _on_cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Desea salir del sistema académico?", parent=self):
            self.master.destroy()

if __name__ == "__main__":
    root = ttk.Window(title="L.N. Evelia A. de Pimentel - Dashboard Institucional", themename="flatly", size=(1150, 680))
    root.configure(bg="#EDECD1")
    root.minsize(800, 500)
    
    usuario_prueba = {
        "usuario": "cmendoza",
        "nombre": "Prof. Carlos Mendoza",
        "rol": "Docente Titular",
        "modulos_permitidos": [
            "Directorio de Alumnos",
            "Control de Notas",
            "Control de Secciones",
            "Control de Profesores y Materias"
        ]
    }
    
    app = VistaDashboard(parent=root, controlador=None, usuario_actual=usuario_prueba)
    app.pack(fill="both", expand=True, padx=10, pady=10)
        
    root.mainloop()