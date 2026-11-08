import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk

class VistaDashboard(ttk.Frame):
    """Dashboard principal del sistema académico con diseño institucional adaptativo (Responsive) y filtrado dinámico."""
    
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
        self._construir_interfaz(self)

    def _construir_interfaz(self, contenedor):
        # 1. Configurar la adaptabilidad total de la ventana raíz y contenedor principal
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(0, weight=1)

        # Usar un Canvas con Scrollbar integrado para que si la pantalla es muy baja, se pueda desplazar sin perder contenido
        self.canvas_principal = tk.Canvas(contenedor, highlightthickness=0)
        self.scrollbar_vertical = ttk.Scrollbar(contenedor, orient="vertical", command=self.canvas_principal.yview)
        
        self.scrollable_frame = ttk.Frame(self.canvas_principal, padding=15)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas_principal.configure(scrollregion=self.canvas_principal.bbox("all"))
        )

        self.window_id = self.canvas_principal.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas_principal.configure(yscrollcommand=self.scrollbar_vertical.set)

        # Hacer que el marco interno se escale dinámicamente al ancho de la ventana
        self.canvas_principal.bind('<Configure>', lambda event: self.canvas_principal.itemconfig(self.window_id, width=event.width))

        self.canvas_principal.pack(side="left", fill="both", expand=True)
        self.scrollbar_vertical.pack(side="right", fill="y")

        # Configurar pesos internos del marco desplazable
        self.scrollable_frame.columnconfigure(0, weight=1)

        # ==========================================
        # 2. BARRA SUPERIOR INSTITUCIONAL (HEADER)
        # ==========================================
        header_frame = ttk.Frame(self.scrollable_frame, padding=10)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)

        try:
            if os.path.exists("logo.png"):
                img_pil = Image.open("logo.png").resize((50, 50), Image.Resampling.LANCZOS)
                logo_tk = ImageTk.PhotoImage(img_pil)
                self.imagenes_referencia.append(logo_tk)
                ttk.Label(header_frame, image=logo_tk).grid(row=0, column=0, rowspan=2, padx=(0, 12))
        except Exception:
            pass

        ttk.Label(
            header_frame, 
            text="L.N. Evelia A. de Pimentel", 
            font=("Segoe UI", 15, "bold"), 
            foreground="#A93226"
        ).grid(row=0, column=1, sticky="w")

        info_sesion = f"Sesión activa: {self.usuario_actual['nombre']} | Usuario: {self.usuario_actual['usuario']} ({self.usuario_actual['rol']})"
        ttk.Label(
            header_frame, 
            text=info_sesion, 
            font=("Segoe UI", 9, "italic"), 
            foreground="#7F8C8D"
        ).grid(row=1, column=1, sticky="w", pady=(2, 0))

        btn_salir = ttk.Button(header_frame, text="Cerrar Sesión", command=self._on_cerrar_sesion)
        btn_salir.grid(row=0, column=2, rowspan=2, padx=5)

        # ==========================================
        # 3. SECCIÓN DE ESTADÍSTICAS (KPIs ADAPTATIVOS)
        # ==========================================
        stats_frame = ttk.LabelFrame(self.scrollable_frame, text=" Resumen y Estadísticas del Plantel ", padding=12)
        stats_frame.pack(fill="x", pady=(0, 15))
        stats_frame.columnconfigure((0, 1, 2), weight=1)

        self._crear_tarjeta_stat(stats_frame, "👨‍🎓 Total Estudiantes", "148 Activos", "Matrícula general", 0)
        self._crear_tarjeta_stat(stats_frame, "🏫 Secciones Registradas", "12 Secciones", "Turnos activos", 1)
        total_asignados = len(self.usuario_actual["modulos_permitidos"])
        self._crear_tarjeta_stat(stats_frame, "🔐 Sus Módulos", f"{total_asignados} Disponibles", "Permisos actuales", 2)

        # ==========================================
        # 4. MÓDULOS ACADÉMICOS (GRILLA ADAPTATIVA)
        # ==========================================
        self.modulos_container = ttk.LabelFrame(self.scrollable_frame, text=" Módulos Académicos Autorizados ", padding=15)
        self.modulos_container.pack(fill="both", expand=True, pady=(0, 10))
        
        # Configurar 3 columnas flexibles para las tarjetas de módulos
        self.modulos_container.columnconfigure(0, weight=1)
        self.modulos_container.columnconfigure(1, weight=1)
        self.modulos_container.columnconfigure(2, weight=1)

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
                "desc": "Planilla interactiva tipo Excel para cálculo automatizado de calificaciones y promedios.",
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
                "nombre": "Control de Profesores, Materias, Años y Secciones",
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
                if columna_indice > 2:  # Máximo 3 columnas
                    columna_indice = 0
                    fila_indice += 1

        if modulos_visibles_count == 0:
            ttk.Label(
                self.modulos_container, 
                text="⚠️ Su usuario no tiene módulos autorizados asignados en este momento.", 
                font=("Segoe UI", 10, "bold"), 
                foreground="#C0392B"
            ).grid(row=0, column=0, columnspan=3, pady=20)

    def _crear_tarjeta_stat(self, parent, titulo, valor, subtitulo, col):
        """Crea una tarjeta de indicador adaptativa."""
        card = ttk.Frame(parent, padding=10, relief="solid", borderwidth=1)
        card.grid(row=0, column=col, sticky="nsew", padx=4)
        
        ttk.Label(card, text=titulo, font=("Segoe UI", 8, "bold"), foreground="#7F8C8D").pack(anchor="center")
        ttk.Label(card, text=valor, font=("Segoe UI", 14, "bold"), foreground="#A93226").pack(anchor="center", pady=(2, 1))
        ttk.Label(card, text=subtitulo, font=("Segoe UI", 7, "italic"), foreground="#95A5A6").pack(anchor="center")

    def _crear_tarjeta_modulo(self, parent, datos_mod, row, col):
        """Crea una tarjeta de módulo flexible que se estira y adapta al ancho disponible."""
        card = ttk.Frame(parent, padding=12, relief="groove")
        card.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)
        card.columnconfigure(0, weight=1)

        ttk.Label(card, text=datos_mod["icono"], font=("Segoe UI", 24)).pack(anchor="center", pady=(0, 4))
        ttk.Label(card, text=datos_mod["nombre"], font=("Segoe UI", 10, "bold"), foreground="#2C3E50", anchor="center").pack(anchor="center", pady=(0, 2))
        
        # Ajustar el wraplength dinámicamente para que el texto nunca se desborde
        lbl_desc = ttk.Label(card, text=datos_mod["desc"], font=("Segoe UI", 8), foreground="#566573", wraplength=210, justify="center")
        lbl_desc.pack(anchor="center", pady=(0, 10), fill="x", expand=True)
        
        btn_entrar = ttk.Button(card, text=datos_mod["etiqueta_btn"], command=datos_mod["comando"])
        btn_entrar.pack(anchor="center", fill="x", ipady=2)

    def _abrir_directorio_alumnos(self):
        messagebox.showinfo("Navegación", "Abriendo módulo: Directorio de Alumnos...")

    def _abrir_control_notas(self):
        messagebox.showinfo("Navegación", "Abriendo módulo: Control de Notas...")

    def _abrir_control_secciones(self):
        messagebox.showinfo("Navegación", "Abriendo el módulo: Control de Secciones...")

    def _abrir_control_profesores(self):
        messagebox.showinfo("Navegación", "Abriendo el módulo: Control de Profesores...")

    def _abrir_control_usuarios(self):
        messagebox.showinfo("Navegación", "Abriendo el módulo: Control de Usuarios...")

    def _on_cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Desea salir del sistema académico?"):
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()  
    root.title("L.N. Evelia A. de Pimentel - Dashboard Adaptativo")
    root.geometry("1100x680")
    
    # Permitir que la ventana raíz se pueda redimensionar libremente en cualquier dirección
    root.minsize(800, 500)
    
    usuario_prueba = {
        "usuario": "cmendoza",
        "nombre": "Prof. Carlos Mendoza",
        "rol": "Docente Titular",
        "modulos_permitidos": [
            "Directorio de Alumnos",
            "Control de Notas",
            "Control de Secciones",
            "Control de Profesores, Materias, Años y Secciones"
        ]
    }
    
    app = VistaDashboard(parent=root, controlador=None, usuario_actual=usuario_prueba)
    app.pack(fill="both", expand=True)
        
    root.mainloop()