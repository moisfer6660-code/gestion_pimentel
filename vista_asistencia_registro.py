import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

class VistaAsistenciaRegistro(ttk.Frame):
    """Módulo de asistencia estilo matriz interactiva con casillas cuadradas, colores y edición histórica."""

    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self.estudiantes_datos = []
        self._construir_interfaz(self)

    def _construir_interfaz(self, contenedor):
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(2, weight=1)

        # Panel de Filtros y Fecha (Permite ver y editar fechas pasadas)
        filtros_frame = ttk.LabelFrame(contenedor, text=" Parámetros de Cátedra y Fecha (Actual o Histórica) ", padding=12)
        filtros_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        filtros_frame.columnconfigure(7, weight=1)

        ttk.Label(filtros_frame, text="Año:", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=3)
        self.combo_anio = ttk.Combobox(filtros_frame, values=["1er Año", "2do Año", "3er Año", "4to Año", "5to Año"], state="readonly", width=10)
        self.combo_anio.grid(row=0, column=1, sticky="ew", padx=3)
        self.combo_anio.set("1er Año")

        ttk.Label(filtros_frame, text="Sección:", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="w", padx=3)
        self.combo_seccion = ttk.Combobox(filtros_frame, values=["Sección A", "Sección B", "Sección C", "Sección Única"], state="readonly", width=10)
        self.combo_seccion.grid(row=0, column=3, sticky="ew", padx=3)
        self.combo_seccion.set("Sección A")

        ttk.Label(filtros_frame, text="Materia:", font=("Segoe UI", 9, "bold")).grid(row=0, column=4, sticky="w", padx=3)
        self.combo_materia = ttk.Combobox(filtros_frame, values=["Matemáticas I", "Castellano y Literatura", "Inglés", "Educación Física"], state="readonly", width=14)
        self.combo_materia.grid(row=0, column=5, sticky="ew", padx=3)
        self.combo_materia.set("Matemáticas I")

        ttk.Label(filtros_frame, text="Fecha:", font=("Segoe UI", 9, "bold")).grid(row=0, column=6, sticky="w", padx=(10, 3))
        self.entrada_fecha = ttk.Entry(filtros_frame, width=11)
        self.entrada_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entrada_fecha.grid(row=0, column=7, sticky="w", padx=3)

        self.btn_cargar = ttk.Button(filtros_frame, text="🔍 Cargar Planilla", command=self._on_cargar_asistencias)
        self.btn_cargar.grid(row=0, column=8, padx=6)

        # Leyenda visual de casillas cuadradas
        leyenda_frame = ttk.Frame(contenedor)
        leyenda_frame.grid(row=1, column=0, sticky="ew", pady=(0, 4))
        ttk.Label(leyenda_frame, text="💡 Clic en la casilla: Verde = [ ☑ ] Asistió | Rojo = [ ☒ ] Faltó | Amarillo = [ 🗹 ] Justificado", font=("Segoe UI", 8, "italic"), foreground="#7F8C8D").pack(side="left")

        # Tabla Matricial (Treeview)
        tabla_container = ttk.LabelFrame(contenedor, text=" Planilla Interactiva de Estudiantes ", padding=8)
        tabla_container.grid(row=2, column=0, sticky="nsew")
        tabla_container.columnconfigure(0, weight=1)
        tabla_container.rowconfigure(0, weight=1)

        columnas = ("nro", "cedula", "nombre", "asistio", "falto", "justificado", "motivo")
        self.tree_matriz = ttk.Treeview(tabla_container, columns=columnas, show="headings", height=12)

        self.tree_matriz.heading("nro", text="N°")
        self.tree_matriz.heading("cedula", text="Cédula / ID")
        self.tree_matriz.heading("nombre", text="Apellidos y Nombres del Estudiante")
        self.tree_matriz.heading("asistio", text="[ ☑ ] Asistió")
        self.tree_matriz.heading("falto", text="[ ☒ ] Faltó")
        self.tree_matriz.heading("justificado", text="[ 🗹 ] Justificado")
        self.tree_matriz.heading("motivo", text="Motivo / Observación")

        self.tree_matriz.column("nro", width=35, anchor="center")
        self.tree_matriz.column("cedula", width=95, anchor="center")
        self.tree_matriz.column("nombre", width=260, anchor="w")
        self.tree_matriz.column("asistio", width=90, anchor="center")
        self.tree_matriz.column("falto", width=90, anchor="center")
        self.tree_matriz.column("justificado", width=100, anchor="center")
        self.tree_matriz.column("motivo", width=200, anchor="w")

        self.tree_matriz.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tabla_container, orient="vertical", command=self.tree_matriz.yview)
        self.tree_matriz.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Configuración de colores de fondo para las filas
        self.tree_matriz.tag_configure("verde", background="#D4EFDF")
        self.tree_matriz.tag_configure("rojo", background="#FADBD8")
        self.tree_matriz.tag_configure("amarillo", background="#FCF3CF")

        self.tree_matriz.bind("<Button-1>", self._on_clic_celda_matriz)

        # Botones inferiores
        inferior_frame = ttk.Frame(contenedor)
        inferior_frame.grid(row=3, column=0, sticky="ew", pady=(8, 0))

        self.btn_guardar = ttk.Button(inferior_frame, text="💾 Guardar Cambios de Planilla", command=self._on_guardar_db)
        self.btn_guardar.pack(side="left", padx=2)

        self.btn_exportar = ttk.Button(inferior_frame, text="🖨️ Exportar Planilla en Formato Físico", command=self._on_exportar_pdf)
        self.btn_exportar.pack(side="left", padx=5)

        self._inicializar_datos_prueba()

    def _inicializar_datos_prueba(self):
        self.estudiantes_datos = [
            {"nro": "1", "cedula": "V-34567890", "nombre": "Alvarez Blanco, Sofía Valentina", "estatus": "Asistió", "motivo": "-"},
            {"nro": "2", "cedula": "V-34123456", "nombre": "Benítez Silva, Carlos Daniel", "estatus": "Asistió", "motivo": "-"},
            {"nro": "3", "cedula": "V-35678901", "nombre": "Contreras Mendoza, Gabriela", "estatus": "Justificado", "motivo": "Cita médica odontológica"},
            {"nro": "4", "cedula": "V-34987654", "nombre": "Díaz Morales, Alejandro José", "estatus": "Faltó", "motivo": "-"},
            {"nro": "5", "cedula": "V-35111222", "nombre": "Fernández Rincón, Mariángel", "estatus": "Asistió", "motivo": "-"}
        ]
        self._actualizar_tabla()

    def _actualizar_tabla(self):
        for item in self.tree_matriz.get_children():
            self.tree_matriz.delete(item)

        for est in self.estudiantes_datos:
            chk_asistio = "[ ☑ ]" if est["estatus"] == "Asistió" else "[   ]"
            chk_falto = "[ ☒ ]" if est["estatus"] == "Faltó" else "[   ]"
            chk_justificado = "[ 🗹 ]" if est["estatus"] == "Justificado" else "[   ]"

            tag_color = "verde" if est["estatus"] == "Asistió" else ("rojo" if est["estatus"] == "Faltó" else "amarillo")

            self.tree_matriz.insert(
                "", "end", 
                values=(est["nro"], est["cedula"], est["nombre"], chk_asistio, chk_falto, chk_justificado, est["motivo"]),
                tags=(tag_color,)
            )

    def _on_clic_celda_matriz(self, event):
        region = self.tree_matriz.identify("region", event.x, event.y)
        if region != "cell":
            return
        
        columna_id = self.tree_matriz.identify_column(event.x)
        item_id = self.tree_matriz.identify_row(event.y)
        if not item_id:
            return
        
        valores_fila = self.tree_matriz.item(item_id, "values")
        cedula_est = valores_fila[1]
        
        estudiante_objetivo = next((est for est in self.estudiantes_datos if est["cedula"] == cedula_est), None)
        if not estudiante_objetivo:
            return

        if columna_id == "#4":
            estudiante_objetivo["estatus"] = "Asistió"
            estudiante_objetivo["motivo"] = "-"
            self._actualizar_tabla()
        elif columna_id == "#5":
            estudiante_objetivo["estatus"] = "Faltó"
            estudiante_objetivo["motivo"] = "-"
            self._actualizar_tabla()
        elif columna_id == "#6":
            motivo_ingresado = simpledialog.askstring("Motivo de Inasistencia", f"Ingrese el motivo de la justificación para {estudiante_objetivo['nombre']}:", parent=self)
            estudiante_objetivo["estatus"] = "Justificado"
            estudiante_objetivo["motivo"] = motivo_ingresado.strip() if motivo_ingresado else "Justificado sin descripción"
            self._actualizar_tabla()

    def _on_cargar_asistencias(self):
        fecha = self.entrada_fecha.get()
        materia = self.combo_materia.get()
        messagebox.showinfo("Planilla Cargada", f"Cargando registros de [{materia}] para la fecha: {fecha}\n(Permite consultar o editar registros anteriores).")
        self._actualizar_tabla()

    def _on_guardar_db(self):
        messagebox.showinfo("Guardado Exitoso", "Los cambios en la planilla han sido guardados correctamente.")

    def _on_exportar_pdf(self):
        messagebox.showinfo("Exportar", "Generando formato físico en PDF...")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("L.N. Evelia A. de Pimentel - vista_asistencia_registro")
    root.geometry("1120x680")
    app = VistaAsistenciaRegistro(parent=root, controlador=None)
    app.pack(fill="both", expand=True, padx=10, pady=10)
    root.mainloop()