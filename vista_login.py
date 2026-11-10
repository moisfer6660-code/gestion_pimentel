import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.style import Style

class VistaLogin(ttk.Frame):
    """Interfaz gráfica de inicio de sesión compacta, centrada y con logotipo prominente."""

    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self.imagenes_referencia = []
        
        # Aplicar estilo institucional unificado con fondo #EDECD1
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
        self.estilo_app.configure("TLabelframe.Label", background=color_fondo, foreground=color_rojo, font=("Segoe UI", 9, "bold"))
        
        self.estilo_app.configure("TButton", background=color_rojo, foreground="#ffffff", bordercolor=color_rojo, font=("Segoe UI", 9, "bold"))
        self.estilo_app.map("TButton", 
            background=[("active", color_rojo_hover), ("pressed", "#7f1d1d")],
            bordercolor=[("active", color_rojo_hover)]
        )

    def _aplicar_cursor_mano(self, widget):
        widget.bind("<Enter>", lambda e: self.winfo_toplevel().config(cursor="hand2"))
        widget.bind("<Leave>", lambda e: self.winfo_toplevel().config(cursor=""))

    def _construir_interfaz(self, contenedor):
        color_fondo = "#EDECD1"
        contenedor.configure(style="TFrame")
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(0, weight=1)

        # Marco central compacto para la ventana de login
        marco_principal = ttk.Frame(contenedor, padding=15)
        marco_principal.grid(row=0, column=0)
        marco_principal.columnconfigure(0, weight=1)

        # ==========================================
        # 1. LOGOTIPO INSTITUCIONAL MÁS GRANDE Y LIMPIO
        # ==========================================
        marco_logo = tk.Frame(marco_principal, bg=color_fondo, width=150, height=150)
        marco_logo.pack(anchor="center", pady=(0, 5))
        marco_logo.pack_propagate(False)

        logo_cargado = False
        try:
            rutas_posibles = [
                os.path.join(os.path.dirname(__file__), "logon.png"),
                "logon.png",
                os.path.join(os.path.dirname(__file__), "logo.png"),
                "logo.png"
            ]
            for ruta in rutas_posibles:
                if os.path.exists(ruta):
                    imagen_pil = Image.open(ruta)
                    imagen_pil.thumbnail((145, 145), Image.Resampling.LANCZOS)
                    logo_tk = ImageTk.PhotoImage(imagen_pil)
                    self.imagenes_referencia.append(logo_tk)
                    
                    lbl_logo = tk.Label(marco_logo, image=logo_tk, bg=color_fondo)
                    lbl_logo.pack(expand=True, anchor="center")
                    logo_cargado = True
                    break
        except Exception as e:
            print(f"Error cargando logotipo: {e}")

        if not logo_cargado:
            tk.Label(marco_logo, text="🏫", font=("Segoe UI", 48), bg=color_fondo).pack(expand=True, anchor="center")

        # ==========================================
        # 2. ENCABEZADO INSTITUCIONAL IMPOBENTE
        # ==========================================
        tk.Label(
            marco_principal, 
            text="L.N. EVELIA A. DE PIMENTEL", 
            font=("Impact", 22),
            fg="#b91c1c",
            bg=color_fondo
        ).pack(anchor="center")

        tk.Label(
            marco_principal, 
            text="Portal de Acceso al Sistema Académico", 
            font=("Segoe UI", 8, "bold italic"),
            fg="#64748b",
            bg=color_fondo
        ).pack(anchor="center", pady=(0, 12))

        # ==========================================
        # 3. FORMULARIO DE ACCESO COMPACTO
        # ==========================================
        marco_formulario = ttk.LabelFrame(marco_principal, text=" Credenciales de Acceso ", padding=12)
        marco_formulario.pack(fill="x", pady=(0, 10))
        marco_formulario.columnconfigure(0, weight=1)

        # Usuario
        ttk.Label(
            marco_formulario, 
            text="Usuario del Sistema:", 
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", pady=(0, 2))

        self.entrada_usuario = ttk.Entry(marco_formulario, width=28, font=("Segoe UI", 9))
        self.entrada_usuario.pack(fill="x", pady=(0, 8), ipady=2)
        self.entrada_usuario.focus()

        # Contraseña
        ttk.Label(
            marco_formulario, 
            text="Contraseña de Acceso:", 
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", pady=(0, 2))

        self.entrada_clave = ttk.Entry(marco_formulario, width=28, show="*", font=("Segoe UI", 9))
        self.entrada_clave.pack(fill="x", pady=(0, 6), ipady=2)
        self.entrada_clave.bind("<Return>", lambda event: self._on_ingresar_click())

        # Checkbox mostrar contraseña
        self.var_mostrar_clave = tk.BooleanVar(value=False)
        chk_mostrar = ttk.Checkbutton(
            marco_formulario, 
            text="Mostrar contraseña", 
            variable=self.var_mostrar_clave,
            command=self._on_alternar_visibilidad_clave
        )
        chk_mostrar.pack(anchor="w", pady=(2, 0))

        # ==========================================
        # 4. BOTÓN DE INGRESO
        # ==========================================
        btn_ingresar = ttk.Button(
            marco_principal, 
            text="Iniciar Sesión", 
            command=self._on_ingresar_click
        )
        btn_ingresar.pack(fill="x", ipady=3, pady=(2, 8))
        self._aplicar_cursor_mano(btn_ingresar)

        # ==========================================
        # 5. PIE DE PÁGINA Y CRÉDITOS OCULTOS (DISCRETOS)
        # ==========================================
        footer_frame = ttk.Frame(marco_principal)
        footer_frame.pack(fill="x")

        tk.Label(
            footer_frame, 
            text="© 2026 - Todos los derechos reservados", 
            font=("Segoe UI", 7), 
            fg="#94a3b8",
            bg=color_fondo
        ).pack(anchor="center", pady=(0, 2))

        badge_oculto = tk.Label(
            footer_frame, 
            text="• UPTMA •", 
            font=("Segoe UI", 7, "bold"), 
            fg="#cbd5e1",
            bg=color_fondo,
            cursor="hand2"
        )
        badge_oculto.pack(anchor="center")
        badge_oculto.bind("<Button-1>", lambda e: self._mostrar_creditos_autores())
        self._aplicar_cursor_mano(badge_oculto)

        badge_oculto.bind("<Enter>", lambda e: badge_oculto.config(fg="#b91c1c"))
        badge_oculto.bind("<Leave>", lambda e: badge_oculto.config(fg="#cbd5e1"))

    def _on_alternar_visibilidad_clave(self):
        """Muestra u oculta los caracteres del campo de contraseña."""
        if self.var_mostrar_clave.get():
            self.entrada_clave.config(show="")
        else:
            self.entrada_clave.config(show="*")

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

    def _on_ingresar_click(self):
        usuario = self.entrada_usuario.get().strip()
        clave = self.entrada_clave.get().strip()

        if not usuario or not clave:
            messagebox.showwarning("Campos Vacíos", "Por favor ingrese su usuario y contraseña para continuar.", parent=self)
            return

        if self.controlador:
            self.controlador.autenticar_usuario(usuario, clave)
        else:
            messagebox.showinfo("Acceso Exitoso", f"Bienvenido al sistema, {usuario}.", parent=self)
            print(f"Usuario autenticado: {usuario}")

if __name__ == "__main__":
    # Ventana de login compacta de 450x540
    root = ttk.Window(title="L.N. Evelia A. de Pimentel - Iniciar Sesión", themename="flatly", size=(450, 540))
    root.configure(bg="#EDECD1")
    root.resizable(False, False)
    
    app = VistaLogin(parent=root, controlador=None)
    app.pack(fill="both", expand=True, padx=10, pady=10)
        
    root.mainloop()