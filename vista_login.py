import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk

class VistaLogin(ttk.Frame):
    """Interfaz gráfica de inicio de sesión con identidad institucional destacada y soporte para logotipo grande."""

    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self.imagenes_referencia = []  # Para evitar que el recolector de basura elimine la imagen de Pillow
        self._construir_interfaz(self)

    def _construir_interfaz(self, contenedor):
        # Configurar adaptabilidad de la ventana principal
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(0, weight=1)

        # Marco central contenedor del Login (centrado en la pantalla)
        marco_principal = ttk.Frame(contenedor, padding=25)
        marco_principal.grid(row=0, column=0)
        marco_principal.columnconfigure(0, weight=1)

        # ==========================================
        # 1. LOGOTIPO INSTITUCIONAL GRANDE Y VISIBLE
        # ==========================================
        try:
            if os.path.exists("logon.png"):
                # Cargar y redimensionar el logo

                img_pil = Image.open("logon.png").resize((170, 170), Image.Resampling.LANCZOS)
                logo_tk = ImageTk.PhotoImage(img_pil)
                self.imagenes_referencia.append(logo_tk)
                
                lbl_logo = ttk.Label(marco_principal, image=logo_tk)
                lbl_logo.pack(anchor="center", pady=(0, 15))
        except Exception as e:
            print(f"No se pudo cargar la imagen logon.png: {e}")

        # ==========================================
        # 2. ENCABEZADO INSTITUCIONAL
        # ==========================================
        ttk.Label(
            marco_principal, 
            text="L.N. Evelia A. de Pimentel", 
            font=("Segoe UI", 16, "bold"), 
            foreground="#A93226"
        ).pack(anchor="center")

        ttk.Label(
            marco_principal, 
            text="Sistema de gestión academica", 
            font=("Segoe UI", 9, "italic"), 
            foreground="#7F8C8D"
        ).pack(anchor="center", pady=(2, 20))

        # ==========================================
        # 3. FORMULARIO DE ACCESO (CREDENCIALES)
        # ==========================================
        marco_formulario = ttk.LabelFrame(marco_principal, text=" Credenciales de acceso ", padding=20)
        marco_formulario.pack(fill="x", pady=(0, 15))
        marco_formulario.columnconfigure(1, weight=1)

        # Nombre de Usuario
        ttk.Label(
            marco_formulario, 
            text="Usuario:", 
            font=("Segoe UI", 9, "bold")
        ).grid(row=0, column=0, sticky="w", pady=8, padx=5)

        self.entrada_usuario = ttk.Entry(marco_formulario, width=28, font=("Segoe UI", 10))
        self.entrada_usuario.grid(row=0, column=1, sticky="ew", pady=8, padx=5)
        self.entrada_usuario.focus()

        # Contraseña
        ttk.Label(
            marco_formulario, 
            text="Contraseña:", 
            font=("Segoe UI", 9, "bold")
        ).grid(row=1, column=0, sticky="w", pady=8, padx=5)

        self.entrada_clave = ttk.Entry(marco_formulario, width=28, show="*", font=("Segoe UI", 10))
        self.entrada_clave.grid(row=1, column=1, sticky="ew", pady=8, padx=5)

        # Checkbox para mostrar / ocultar contraseña
        self.var_mostrar_clave = tk.BooleanVar(value=False)
        chk_mostrar = ttk.Checkbutton(
            marco_formulario, 
            text="Mostrar contraseña", 
            variable=self.var_mostrar_clave,
            command=self._on_alternar_visibilidad_clave
        )
        chk_mostrar.grid(row=2, column=1, sticky="w", pady=(4, 5), padx=5)

        # ==========================================
        # 4. BOTÓN DE INGRESO
        # ==========================================
        btn_ingresar = ttk.Button(
            marco_principal, 
            text="Iniciar Sesión", 
            command=self._on_ingresar_click
        )
        btn_ingresar.pack(fill="x", ipady=5, pady=(5, 0))

        # Pie de página institucional
        ttk.Label(
            marco_principal, 
            text="© 2026 - Todos los derechos reservados", 
            font=("Segoe UI", 8), 
            foreground="#95A5A6"
        ).pack(anchor="center", pady=(20, 0))

    def _on_alternar_visibilidad_clave(self):
        """Muestra u oculta los caracteres del campo de contraseña."""
        if self.var_mostrar_clave.get():
            self.entrada_clave.config(show="")
        else:
            self.entrada_clave.config(show="*")

    def _on_ingresar_click(self):
        """Valida las credenciales ingresadas e inicia sesión en el sistema."""
        usuario = self.entrada_usuario.get().strip()
        clave = self.entrada_clave.get().strip()

        if not usuario or not clave:
            messagebox.showwarning("Campos Vacíos", "Por favor ingrese su usuario y contraseña para continuar.")
            return

        if self.controlador:
            self.controlador.autenticar_usuario(usuario, clave)
        else:
            # Simulación de acceso exitoso por defecto si no hay un controlador externo
            messagebox.showinfo("Acceso Exitoso", f"Bienvenido al sistema, {usuario}.")
            print(f"Usuario autenticado: {usuario}")

if __name__ == "__main__":
    root = tk.Tk()  
    root.title("L.N Evelia A. de Pimentel - Iniciar Sesión")
    root.geometry("450x535")
    root.resizable(False, False)
    
    app = VistaLogin(parent=root, controlador=None)
    app.pack(fill="both", expand=True)
        
    root.mainloop()