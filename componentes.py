import os
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from tkinter import filedialog

class FormularioEstudiante(ttk.LabelFrame):
    """Molde reutilizable para los datos del estudiante con diseño institucional unificado."""
    def __init__(self, parent):
        super().__init__(parent, text=" Datos del Estudiante ", padding=12)
        self._construir_campos()

    def _construir_campos(self):
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)

        # Fila 0: Cédula y Género
        ttk.Label(self, text="Cédula de Identidad:", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", pady=6, padx=5)
        self.ingreso_cedula = ttk.Entry(self, width=22)
        self.ingreso_cedula.grid(row=0, column=1, sticky="ew", pady=6, padx=5)

        ttk.Label(self, text="Género:", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="w", pady=6, padx=5)
        self.combo_genero = ttk.Combobox(self, width=20, values=["Masculino", "Femenino", "Otro"], state="readonly")
        self.combo_genero.grid(row=0, column=3, sticky="ew", pady=6, padx=5)
        self.combo_genero.set("Masculino")

        # Fila 1: Nombre y Apellido
        ttk.Label(self, text="Nombres:", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w", pady=6, padx=5)
        self.ingreso_nombre = ttk.Entry(self, width=25)
        self.ingreso_nombre.grid(row=1, column=1, sticky="ew", pady=6, padx=5)

        ttk.Label(self, text="Apellidos:", font=("Segoe UI", 9, "bold")).grid(row=1, column=2, sticky="w", pady=6, padx=5)
        self.ingreso_apellido = ttk.Entry(self, width=25)
        self.ingreso_apellido.grid(row=1, column=3, sticky="ew", pady=6, padx=5)
        
        # Fila 2: Teléfono y Correo
        ttk.Label(self, text="Teléfono:", font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", pady=6, padx=5)
        self.ingreso_Telefono = ttk.Entry(self, width=22)
        self.ingreso_Telefono.grid(row=2, column=1, sticky="ew", pady=6, padx=5)

        ttk.Label(self, text="Correo Electrónico:", font=("Segoe UI", 9, "bold")).grid(row=2, column=2, sticky="w", pady=6, padx=5)
        self.ingreso_CorreoElectronico = ttk.Entry(self, width=25)
        self.ingreso_CorreoElectronico.grid(row=2, column=3, sticky="ew", pady=6, padx=5)

        # Fila 3: Dirección (ocupa ancho extendido)
        ttk.Label(self, text="Dirección de Habitación:", font=("Segoe UI", 9, "bold")).grid(row=3, column=0, sticky="w", pady=6, padx=5)
        self.ingreso_Dirección = ttk.Entry(self, width=30)
        self.ingreso_Dirección.grid(row=3, column=1, columnspan=3, sticky="ew", pady=6, padx=5)

        # Fila 4: Fecha de nacimiento
        ttk.Label(self, text="Fecha de Nacimiento:", font=("Segoe UI", 9, "bold")).grid(row=4, column=0, sticky="w", pady=6, padx=5)
        frame_fecha = ttk.Frame(self)
        frame_fecha.grid(row=4, column=1, columnspan=3, sticky="w", pady=6, padx=5)

        self.combo_dia = ttk.Combobox(frame_fecha, width=4, values=[str(i).zfill(2) for i in range(1, 32)], state="readonly")
        self.combo_dia.pack(side="left", padx=(0, 4))
        self.combo_dia.set("01")

        self.combo_mes = ttk.Combobox(frame_fecha, width=4, values=[str(i).zfill(2) for i in range(1, 13)], state="readonly")
        self.combo_mes.pack(side="left", padx=4)
        self.combo_mes.set("01")

        self.combo_anio = ttk.Combobox(frame_fecha, width=8, values=[str(i) for i in range(2026, 1939, -1)], state="readonly")
        self.combo_anio.pack(side="left", padx=(4, 0))
        self.combo_anio.set("2000")

    def obtener_datos(self):
        fecha_nac = f"{self.combo_dia.get()}-{self.combo_mes.get()}-{self.combo_anio.get()}"
        return {
            "cedula": self.ingreso_cedula.get().strip(),
            "nombre": self.ingreso_nombre.get().strip(),
            "apellido": self.ingreso_apellido.get().strip(),
            "telefono": self.ingreso_Telefono.get().strip(),
            "direccion": self.ingreso_Dirección.get().strip(),
            "correo": self.ingreso_CorreoElectronico.get().strip(),
            "genero": self.combo_genero.get().strip(),
            "fecha_nacimiento": fecha_nac
        }

    def limpiar(self):
        self.ingreso_cedula.delete(0, tk.END)
        self.ingreso_nombre.delete(0, tk.END)
        self.ingreso_apellido.delete(0, tk.END)
        self.ingreso_Telefono.delete(0, tk.END)
        self.ingreso_Dirección.delete(0, tk.END)
        self.ingreso_CorreoElectronico.delete(0, tk.END)
        self.combo_genero.set("Masculino")
        self.combo_dia.set("01")
        self.combo_mes.set("01")
        self.combo_anio.set("2000")

class FormularioRepresentante(ttk.LabelFrame):
    """Molde reutilizable y avanzado para los datos completos del representante legal."""

    def __init__(self, parent, titulo=" Datos del Representante "):
        super().__init__(parent, text=titulo, padding=12)
        self._construir_campos()

    def _construir_campos(self):
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)

        # Fila 0: Cédula y Parentesco
        ttk.Label(self, text="Cédula:", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", pady=6, padx=5)
        self.entry_cedula = ttk.Entry(self, width=20)
        self.entry_cedula.grid(row=0, column=1, sticky="ew", pady=6, padx=5)

        ttk.Label(self, text="Parentesco:", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="w", pady=6, padx=5)
        self.combo_parentesco = ttk.Combobox(
            self, width=18, 
            values=["Madre", "Padre", "Tutor(a) Legal", "Abuelo(a)", "Tío(a)", "Otro"], 
            state="readonly"
        )
        self.combo_parentesco.grid(row=0, column=3, sticky="ew", pady=6, padx=5)
        self.combo_parentesco.set("Madre")

        # Fila 1: Nombres y Apellidos
        ttk.Label(self, text="Nombres:", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w", pady=6, padx=5)
        self.entry_nombres = ttk.Entry(self, width=25)
        self.entry_nombres.grid(row=1, column=1, sticky="ew", pady=6, padx=5)

        ttk.Label(self, text="Apellidos:", font=("Segoe UI", 9, "bold")).grid(row=1, column=2, sticky="w", pady=6, padx=5)
        self.entry_apellidos = ttk.Entry(self, width=25)
        self.entry_apellidos.grid(row=1, column=3, sticky="ew", pady=6, padx=5)

        # Fila 2: Teléfono Móvil y Teléfono Alternativo
        ttk.Label(self, text="Teléfono Móvil:", font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", pady=6, padx=5)
        self.entry_telefono = ttk.Entry(self, width=20)
        self.entry_telefono.grid(row=2, column=1, sticky="ew", pady=6, padx=5)

        ttk.Label(self, text="Teléfono Alt.:", font=("Segoe UI", 9, "bold")).grid(row=2, column=2, sticky="w", pady=6, padx=5)
        self.entry_telefono_alt = ttk.Entry(self, width=20)
        self.entry_telefono_alt.grid(row=2, column=3, sticky="ew", pady=6, padx=5)

        # Fila 3: Correo Electrónico
        ttk.Label(self, text="Correo Electrónico:", font=("Segoe UI", 9, "bold")).grid(row=3, column=0, sticky="w", pady=6, padx=5)
        self.entry_correo = ttk.Entry(self, width=30)
        self.entry_correo.grid(row=3, column=1, columnspan=3, sticky="ew", pady=6, padx=5)

        # Fila 4: Dirección de Habitación
        ttk.Label(self, text="Dirección:", font=("Segoe UI", 9, "bold")).grid(row=4, column=0, sticky="w", pady=6, padx=5)
        self.entry_direccion = ttk.Entry(self, width=30)
        self.entry_direccion.grid(row=4, column=1, columnspan=3, sticky="ew", pady=6, padx=5)

    def obtener_datos(self):
        return {
            "cedula": self.entry_cedula.get().strip(),
            "parentesco": self.combo_parentesco.get().strip(),
            "nombres": self.entry_nombres.get().strip(),
            "apellidos": self.entry_apellidos.get().strip(),
            "telefono": self.entry_telefono.get().strip(),
            "telefono_alternativo": self.entry_telefono_alt.get().strip(),
            "correo": self.entry_correo.get().strip(),
            "direccion": self.entry_direccion.get().strip()
        }

    def limpiar(self):
        self.entry_cedula.delete(0, tk.END)
        self.combo_parentesco.set("Madre")
        self.entry_nombres.delete(0, tk.END)
        self.entry_apellidos.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_telefono_alt.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)

class FormularioConfiguracionAcademica(ttk.Frame):
    """Molde reutilizable para la configuración de secciones con diseño institucional unificado."""

    def __init__(self, parent):
        super().__init__(parent)
        self._construir_campos()

    def _construir_campos(self):
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)

        ttk.Label(self, text="Período Escolar:", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", pady=6, padx=5)
        self.combo_periodo = ttk.Combobox(self, width=22, values=["2026-2027", "2027-2028", "2028-2029", "2029-2030"], state="readonly")
        self.combo_periodo.grid(row=0, column=1, sticky="ew", pady=6, padx=5)
        self.combo_periodo.set("2026-2027")

        ttk.Label(self, text="Turno / Jornada:", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="w", pady=6, padx=5)
        self.combo_turno = ttk.Combobox(self, width=22, values=["Mañana", "Tarde", "Integral / Completa"], state="readonly")
        self.combo_turno.grid(row=0, column=3, sticky="ew", pady=6, padx=5)
        self.combo_turno.set("Mañana")

        ttk.Label(self, text="Año / Grado:", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w", pady=6, padx=5)
        self.combo_anio = ttk.Combobox(self, width=22, values=["1er Año", "2do Año", "3er Año", "4to Año", "5to Año"], state="readonly")
        self.combo_anio.grid(row=1, column=1, sticky="ew", pady=6, padx=5)
        self.combo_anio.set("1er Año")

        ttk.Label(self, text="Sección (Letra):", font=("Segoe UI", 9, "bold")).grid(row=1, column=2, sticky="w", pady=6, padx=5)
        letras_az = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        self.combo_seccion = ttk.Combobox(self, width=22, values=letras_az, state="readonly")
        self.combo_seccion.grid(row=1, column=3, sticky="ew", pady=6, padx=5)
        self.combo_seccion.set("A")

        ttk.Label(self, text="Aula / Salón:", font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", pady=6, padx=5)
        self.datos_aula = ttk.Entry(self, width=22)
        self.datos_aula.grid(row=2, column=1, sticky="ew", pady=6, padx=5)

        ttk.Label(self, text="Capacidad Máx:", font=("Segoe UI", 9, "bold")).grid(row=2, column=2, sticky="w", pady=6, padx=5)
        self.datos_capacidad_seccion = ttk.Entry(self, width=22)
        self.datos_capacidad_seccion.grid(row=2, column=3, sticky="ew", pady=6, padx=5)
        self.datos_capacidad_seccion.insert(0, "35")

    def obtener_datos(self):
        return {
            "periodo": self.combo_periodo.get().strip(),
            "turno": self.combo_turno.get().strip(),
            "anio": self.combo_anio.get().strip(),
            "seccion": self.combo_seccion.get().strip(),
            "aula": self.datos_aula.get().strip() or "Sin Asignar",
            "capacidad": self.datos_capacidad_seccion.get().strip() or "35"
        }

    def limpiar(self):
        self.combo_periodo.set("2026-2027")
        self.combo_turno.set("Mañana")
        self.combo_anio.set("1er Año")
        self.combo_seccion.set("A")
        self.datos_aula.delete(0, tk.END)
        self.datos_capacidad_seccion.delete(0, tk.END)
        self.datos_capacidad_seccion.insert(0, "35")

class FormularioRegistroProfesor(ttk.Frame):
    """Componente reutilizable de formulario para el registro y carga de documentos de docentes."""

    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self._construir_componente(self)

    def _construir_componente(self, contenedor):
        contenedor.columnconfigure(0, weight=3)
        contenedor.columnconfigure(1, weight=2)
        contenedor.rowconfigure(0, weight=1)

        marco_datos = ttk.LabelFrame(contenedor, text=" Información Personal y Académica ", padding=15)
        marco_datos.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        marco_datos.columnconfigure(1, weight=1)

        campos = [
            ("Cédula de Identidad:", "entry"),
            ("Apellidos y Nombres:", "entry"),
            ("Teléfono de Contacto:", "entry"),
            ("Correo Electrónico:", "entry"),
            ("Especialidad / Área:", "entry"),
            ("Año / Sección Asignada:", "combo_seccion")
        ]

        self.entradas_profesor = {}
        for indice, (etiqueta, tipo) in enumerate(campos):
            ttk.Label(marco_datos, text=etiqueta, font=("Segoe UI", 9, "bold")).grid(row=indice, column=0, sticky="w", pady=8, padx=5)
            
            if tipo == "entry":
                widget = ttk.Entry(marco_datos, width=28)
                widget.grid(row=indice, column=1, sticky="ew", pady=8, padx=5)
                self.entradas_profesor[etiqueta] = widget
            elif tipo == "combo_seccion":
                widget = ttk.Combobox(marco_datos, values=["1er Año - Sección A", "1er Año - Sección B", "2do Año - Sección Única"], state="readonly")
                widget.set("1er Año - Sección A")
                widget.grid(row=indice, column=1, sticky="ew", pady=8, padx=5)
                self.entradas_profesor[etiqueta] = widget

        marco_docs = ttk.LabelFrame(contenedor, text=" Carga de Títulos y Documentos Legales ", padding=15)
        marco_docs.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        marco_docs.columnconfigure(0, weight=1)

        self.docs_cargados = {
            "Título Universitario / TSU": None,
            "Copia de Cédula de Identidad": None,
            "Certificados / Constancias": None
        }

        self.labels_docs_estado = {}
        for doc_nombre in self.docs_cargados.keys():
            sub_frame = ttk.Frame(marco_docs, padding=8)
            sub_frame.pack(fill="x", pady=6)
            sub_frame.columnconfigure(0, weight=1)

            ttk.Label(sub_frame, text=doc_nombre, font=("Segoe UI", 9, "bold")).pack(anchor="w")
            
            estado_lbl = ttk.Label(sub_frame, text="Estado: Pendiente por adjuntar", font=("Segoe UI", 8), foreground="#C0392B")
            estado_lbl.pack(anchor="w", pady=(2, 4))
            self.labels_docs_estado[doc_nombre] = estado_lbl

            btn_cargar = ttk.Button(sub_frame, text=f"Examinar {doc_nombre}...", command=lambda d=doc_nombre: self._on_cargar_documento(d))
            btn_cargar.pack(anchor="w", fill="x")

    def _on_cargar_documento(self, nombre_doc):
        archivo = filedialog.askopenfilename(
            title=f"Cargar {nombre_doc}",
            filetypes=[("Documentos PDF e Imágenes", "*.pdf;*.png;*.jpg;*.jpeg")]
        )
        if archivo:
            self.docs_cargados[nombre_doc] = archivo
            nombre_corto = os.path.basename(archivo)
            self.labels_docs_estado[nombre_doc].config(text=f"Archivo: {nombre_corto}", foreground="#27AE60")
            messagebox.showinfo("Documento Adjunto", f"El archivo para '{nombre_doc}' se ha cargado correctamente.")

    def obtener_datos(self):
        datos = {etiqueta: widget.get().strip() for etiqueta, widget in self.entradas_profesor.items()}
        datos["documentos"] = self.docs_cargados
        return datos