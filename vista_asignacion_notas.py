import copy
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class VistaAsignacionNotas(ttk.Frame):
    
    """Interfaz para la gestión y asignación de calificaciones escolares."""

    def __init__(self, contenedor_principal, controlador_externo=None):
        super().__init__(contenedor_principal)
        self.controlador_externo = controlador_externo
        self.registros_celdas = {}  
        
        # Estado inicial base
        self.actividades_iniciales = ["Evaluación Inicial", "Taller N°1"]
        self.datos_estudiantes_iniciales = [
            ("V-33456789", "Pérez González, Alejandro", ["15.0", "19.0"]),
            ("V-33987123", "Rodríguez Silva, María Gabriela", ["14.0", "16.0"]),
            ("V-34112233", "Gómez Blanco, Jesús David", ["11.0", "13.0"]),
            ("V-34556677", "Martínez López, Valeria Sofía", ["20.0", "19.0"]),
        ]
        
        # Copias activas de trabajo
        self.lista_actividades = copy.deepcopy(self.actividades_iniciales)
        self.estudiantes_data = copy.deepcopy(self.datos_estudiantes_iniciales)

        self._configurar_estilos_ttk()
        self._construir_interfaz(self)

    def _configurar_estilos_ttk(self):
        estilo_ttk = ttk.Style()
        if "clam" in estilo_ttk.theme_names():
            estilo_ttk.theme_use("clam")
        
        estilo_ttk.configure(".", font=("Segoe UI", 9))
        estilo_ttk.configure("TFrame", background="#f8fafc")
        
        # Estilo para botones principales en rojo institucional
        estilo_ttk.configure("TButton", padding=(10, 6), relief="flat", background="#b91c1c", borderwidth=0, font=("Segoe UI", 9, "bold"), foreground="#FFFFFF")
        estilo_ttk.map("TButton", background=[("active", "#991b1b"), ("pressed", "#7f1d1d")])

        # Estilo para botón Guardar (Verde armónico)
        estilo_ttk.configure("Accent.TButton", background="#32B855", foreground="#ffffff")
        estilo_ttk.map("Accent.TButton", background=[("active", "#289e47"), ("pressed", "#1e7835")])

        # Estilo para botón Eliminar (Rojo oscuro de alerta)
        estilo_ttk.configure("Danger.TButton", background="#b91c1c", foreground="#ffffff")
        estilo_ttk.map("Danger.TButton", background=[("active", "#b91c1c"), ("pressed", "#7f1d1d")])

        # Estilo para botón Regresar (Gris pizarra elegante que combina con todo)
        estilo_ttk.configure("Secondary.TButton", background="#475569", foreground="#ffffff")
        estilo_ttk.map("Secondary.TButton", background=[("active", "#334155"), ("pressed", "#1e293b")])

        # Estilo para botón Filtrar (rojo institucional coordinado con el tema general)
        estilo_ttk.configure("Filter.TButton", background="#b91c1c", foreground="#ffffff")
        estilo_ttk.map("Filter.TButton", background=[("active", "#b91c1c"), ("pressed", "#7f1d1d")])

        # Estilo para botón Imprimir (rojo institucional coordinado)
        estilo_ttk.configure("Info.TButton", background="#b91c1c", foreground="#ffffff")
        estilo_ttk.map("Info.TButton", background=[("active", "#b91c1c"), ("pressed", "#7f1d1d")])

    def _aplicar_cursor_mano(self, boton):
        """Asigna el cambio de cursor a formato de mano interactiva al pasar por encima."""
        boton.bind("<Enter>", lambda e: self.winfo_toplevel().config(cursor="hand2"))
        boton.bind("<Leave>", lambda e: self.winfo_toplevel().config(cursor=""))

    def _construir_interfaz(self, contenedor):
        contenedor.configure(style="TFrame")
        
        # Encabezado institucional con margen derecho protegido para el logotipo
        marco_encabezado = ttk.Frame(contenedor, style="TFrame", height=75)
        marco_encabezado.pack(fill="x", padx=(20, 190), pady=(10, 0))
        marco_encabezado.pack_propagate(False)

        marco_titulos = ttk.Frame(marco_encabezado, style="TFrame")
        marco_titulos.place(x=0, y=8)

        etiqueta_titulo = tk.Label(
            marco_titulos, 
            text="Control de Calificaciones", 
            font=("Segoe UI", 22, "bold"),
            foreground="#A93226",
            background="#f8fafc"
        )
        etiqueta_titulo.pack(anchor="w")

        etiqueta_subtitulo = tk.Label(
            marco_titulos, 
            text="Planilla Institucional", 
            font=("Segoe UI", 11, "italic"),
            foreground="#64748b",
            background="#f8fafc"
        )
        etiqueta_subtitulo.pack(anchor="w", pady=(1, 0))

        # Logotipo institucional grande en la esquina superior derecha (libre de interferencias)
        try:
            ruta_logo = os.path.join(os.path.dirname(__file__), "logon.png")
            if os.path.exists(ruta_logo):
                imagen_pil = Image.open(ruta_logo).resize((175, 175), Image.Resampling.LANCZOS)
                self.imagen_logo = ImageTk.PhotoImage(imagen_pil)
                etiqueta_logo = ttk.Label(contenedor, image=self.imagen_logo, style="TLabel", background="#f8fafc")
                etiqueta_logo.place(relx=0.98, x=0, y=10, anchor="ne")
                etiqueta_logo.lift()
        except Exception as error_logo:
            print(f"No se pudo cargar el logo: {error_logo}")

        # Selectores de filtros y botón de regresar con colores armónicos y margen protegido
        selector_filtro = ttk.Frame(contenedor, padding=8, style="TFrame")
        selector_filtro.pack(fill="x", padx=(20, 190), pady=(5, 5))

        tk.Label(selector_filtro, text="Año / Grado:", font=("Segoe UI", 9, "bold"), background="#f8fafc").grid(row=0, column=0, sticky="w", pady=6, padx=5)
        self.combo_anio = ttk.Combobox(
            selector_filtro, values=["1er Año", "2do Año", "3er Año", "4to Año", "5to Año"], state="readonly", width=14
        )
        self.combo_anio.grid(row=0, column=1, sticky="w", pady=6, padx=5)
        self.combo_anio.set("1er Año")

        tk.Label(selector_filtro, text="Sección:", font=("Segoe UI", 9, "bold"), background="#f8fafc").grid(row=0, column=2, sticky="w", pady=6, padx=10)
        letras_az = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        self.combo_seccion = ttk.Combobox(
            selector_filtro, values=letras_az, state="readonly", width=6
        )
        self.combo_seccion.grid(row=0, column=3, sticky="w", pady=6, padx=5)
        self.combo_seccion.set("A")

        tk.Label(selector_filtro, text="Materia:", font=("Segoe UI", 9, "bold"), background="#f8fafc").grid(row=0, column=4, sticky="w", pady=6, padx=10)
        self.combo_materia = ttk.Combobox(
            selector_filtro, 
            values=["Matemáticas", "Castellano", "Inglés", "Biología", "Física", "Química", "Geografía e Historia"], 
            state="readonly",
            width=20
        )
        self.combo_materia.grid(row=0, column=5, sticky="w", pady=6, padx=5)
        self.combo_materia.set("Matemáticas")

        self.boton_filtrar = ttk.Button(selector_filtro, text="Filtrar", style="Filter.TButton", command=self._on_aplicar_filtro)
        self.boton_filtrar.grid(row=0, column=6, padx=12, pady=6)
        self._aplicar_cursor_mano(self.boton_filtrar)

        self.boton_regresar = ttk.Button(selector_filtro, text="← Regresar", style="Secondary.TButton", command=self._on_regresar)
        self.boton_regresar.grid(row=0, column=7, padx=12, pady=6)
        self._aplicar_cursor_mano(self.boton_regresar)

        tk.Label(selector_filtro, text="Docente:", font=("Segoe UI", 9, "bold"), background="#f8fafc").grid(row=1, column=0, sticky="w", pady=4, padx=5)
        self.etiqueta_docente_valor = tk.Label(selector_filtro, text="Prof. Carlos Mendoza (Matemáticas)", font=("Segoe UI", 9, "italic"), foreground="#0284c7", background="#f8fafc")
        self.etiqueta_docente_valor.grid(row=1, column=1, columnspan=5, sticky="w", pady=4, padx=5)

        # Panel de operaciones sobre actividades y botón de imprimir con menú desplegable
        gestion_nota = ttk.Frame(contenedor, padding=5, style="TFrame")
        gestion_nota.pack(fill="x", padx=(20, 190), pady=(8, 10))

        tk.Label(gestion_nota, text="Actividad:", font=("Segoe UI", 9, "bold"), background="#f8fafc").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.entrada_nueva_actividad = ttk.Entry(gestion_nota, width=16)
        self.entrada_nueva_actividad.grid(row=0, column=1, sticky="ew", padx=5)
        self.entrada_nueva_actividad.insert(0, "Examen Parcial N°1")

        self.boton_crear_actividad = ttk.Button(gestion_nota, text="Agregar", command=self._on_crear_actividad_global)
        self.boton_crear_actividad.grid(row=0, column=2, padx=3)
        self._aplicar_cursor_mano(self.boton_crear_actividad)

        self.boton_renombrar_actividad = ttk.Button(gestion_nota, text="Renombrar", command=self._on_renombrar_actividad)
        self.boton_renombrar_actividad.grid(row=0, column=3, padx=3)
        self._aplicar_cursor_mano(self.boton_renombrar_actividad)

        self.boton_eliminar_actividad = ttk.Button(gestion_nota, text="Eliminar", command=self._on_eliminar_actividad, style="Danger.TButton")
        self.boton_eliminar_actividad.grid(row=0, column=4, padx=3)
        self._aplicar_cursor_mano(self.boton_eliminar_actividad)

        self.boton_deshacer = ttk.Button(gestion_nota, text="Deshacer", command=self._on_deshacer_cambios)
        self.boton_deshacer.grid(row=0, column=5, padx=3)
        self._aplicar_cursor_mano(self.boton_deshacer)

        self.boton_guardar_bd = ttk.Button(gestion_nota, text="Guardar", command=self._on_guardar_en_bd, style="Accent.TButton")
        self.boton_guardar_bd.grid(row=0, column=6, padx=3)
        self._aplicar_cursor_mano(self.boton_guardar_bd)

        # Menú desplegable para el botón de Imprimir
        self.menu_imprimir = tk.Menu(contenedor, tearoff=0)
        self.menu_imprimir.add_command(label="🖨️ Imprimir Planilla Vacía", command=self._on_exportar_planilla_blanca)
        self.menu_imprimir.add_command(label="📊 Imprimir Planilla con Notas", command=self._on_exportar_planilla_notas)

        def desplegar_menu_imprimir(evento):
            try:
                self.menu_imprimir.tk_popup(evento.x_root, evento.y_root)
            finally:
                self.menu_imprimir.grab_release()

        self.boton_imprimir_opciones = ttk.Button(gestion_nota, text="🖨️ Imprimir ▼", style="Info.TButton")
        self.boton_imprimir_opciones.grid(row=0, column=7, padx=3)
        self.boton_imprimir_opciones.bind("<Button-1>", desplegar_menu_imprimir)
        self._aplicar_cursor_mano(self.boton_imprimir_opciones)

        # Contenedor principal de la tabla
        frame_tabla = ttk.Frame(contenedor, style="TFrame")
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=(5, 15))
        frame_tabla.columnconfigure(0, weight=1)
        frame_tabla.rowconfigure(0, weight=1)

        self.lienzo_tabla = tk.Canvas(frame_tabla, bg="#ffffff", highlightthickness=0)
        self.barra_desplazamiento_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.lienzo_tabla.yview)
        
        self.marco_desplazamiento = ttk.Frame(self.lienzo_tabla, style="TFrame")
        self.marco_desplazamiento.bind(
            "<Configure>",
            lambda evento: self.lienzo_tabla.configure(scrollregion=self.lienzo_tabla.bbox("all"))
        )

        self.lienzo_tabla.create_window((0, 0), window=self.marco_desplazamiento, anchor="nw")
        self.lienzo_tabla.configure(yscrollcommand=self.barra_desplazamiento_y.set)

        self.lienzo_tabla.pack(side="left", fill="both", expand=True)
        self.barra_desplazamiento_y.pack(side="right", fill="y")

        self._construir_planilla_interactiva()

    def _crear_campo_seleccionable(self, contenedor, texto, ancho, color_fondo, justificacion="center", estilo_fuente=("Segoe UI", 9)):
        """Crea un campo plano de solo lectura que permite seleccionar y copiar texto."""
        var_texto = tk.StringVar(value=texto)
        campo = tk.Entry(
            contenedor,
            textvariable=var_texto,
            font=estilo_fuente,
            bg=color_fondo,
            fg="#1e293b",
            relief="flat",
            justify=justificacion,
            state="readonly",
            readonlybackground=color_fondo,
            bd=0,
            highlightthickness=0,
            width=ancho
        )
        return campo

    def _construir_planilla_interactiva(self):
        for widget in self.marco_desplazamiento.winfo_children():
            widget.destroy()
        self.registros_celdas.clear()

        nombres_columnas = ["N°", "Cédula", "Apellidos y nombres del estudiante"] + self.lista_actividades + ["Promedio Real"]
        
        for columna_idx, texto_columna in enumerate(nombres_columnas):
            etiqueta_cabecera = tk.Label(
                self.marco_desplazamiento, 
                text=texto_columna, 
                font=("Segoe UI", 9, "bold"),
                bg="#e2e8f0", 
                fg="#01112c", 
                relief="flat", 
                padx=10, 
                pady=8, 
                anchor="center" if columna_idx != 2 else "w"
            )
            etiqueta_cabecera.grid(row=0, column=columna_idx, sticky="nsew", padx=1, pady=1)

        total_filas = len(self.estudiantes_data)

        for indice_fila, (cedula_estudiante, nombre_estudiante, lista_notas) in enumerate(self.estudiantes_data, start=1):
            while len(lista_notas) < len(self.lista_actividades):
                lista_notas.append("0.0")
            if len(lista_notas) > len(self.lista_actividades):
                lista_notas = lista_notas[:len(self.lista_actividades)]
                self.estudiantes_data[indice_fila - 1] = (cedula_estudiante, nombre_estudiante, lista_notas)

            color_fondo_fila = "#ffffff" if indice_fila % 2 != 0 else "#f8fafc"

            # Celdas de datos con selección habilitada para copiar
            campo_num = self._crear_campo_seleccionable(self.marco_desplazamiento, str(indice_fila), 5, color_fondo_fila)
            campo_num.grid(row=indice_fila, column=0, sticky="nsew", padx=1, pady=1, ipady=4)

            campo_cedula = self._crear_campo_seleccionable(self.marco_desplazamiento, cedula_estudiante, 16, color_fondo_fila, estilo_fuente=("Segoe UI", 10))
            campo_cedula.grid(row=indice_fila, column=1, sticky="nsew", padx=1, pady=1, ipady=4)

            campo_nombre = self._crear_campo_seleccionable(self.marco_desplazamiento, nombre_estudiante, 48, color_fondo_fila, justificacion="left")
            campo_nombre.grid(row=indice_fila, column=2, sticky="nsew", padx=1, pady=1, ipady=4)

            # Entradas de notas editables
            variables_fila = []
            entradas_fila = []
            for act_idx, valor_nota in enumerate(lista_notas):
                variable_nota = tk.StringVar(value=valor_nota)
                entrada_nota = ttk.Entry(self.marco_desplazamiento, textvariable=variable_nota, width=10, justify="center")
                entrada_nota.grid(row=indice_fila, column=3 + act_idx, padx=4, pady=4)
                variables_fila.append(variable_nota)
                entradas_fila.append(entrada_nota)

            columna_promedio_indice = 3 + len(self.lista_actividades)
            etiqueta_promedio = tk.Label(self.marco_desplazamiento, text="0.0", font=("Segoe UI", 9, "bold"), fg="#15803d", bg=color_fondo_fila, relief="flat", anchor="center", padx=8, pady=6)
            etiqueta_promedio.grid(row=indice_fila, column=columna_promedio_indice, sticky="nsew", padx=1, pady=1)

            self.registros_celdas[indice_fila] = {
                "variables": variables_fila,
                "entradas": entradas_fila,
                "etiqueta_promedio": etiqueta_promedio
            }

            for variable_n in variables_fila:
                variable_n.trace_add("write", lambda *args, fila_actual=indice_fila: self._recalcular_promedio(fila_actual))

            self._recalcular_promedio(indice_fila)

        # Configuración de navegación por teclado (Enter para bajar entre filas)
        for fila_idx in range(1, total_filas + 1):
            actividades_en_fila = self.registros_celdas[fila_idx]["entradas"]
            for act_idx, entrada_actual in enumerate(actividades_en_fila):
                if fila_idx < total_filas:
                    siguiente_entrada = self.registros_celdas[fila_idx + 1]["entradas"][act_idx]
                    entrada_actual.bind("<Return>", lambda e, destino=siguiente_entrada: (destino.focus(), destino.select_range(0, tk.END)))
                else:
                    if act_idx + 1 < len(actividades_en_fila):
                        siguiente_actividad_primer_alumno = self.registros_celdas[1]["entradas"][act_idx + 1]
                        entrada_actual.bind("<Return>", lambda e, destino=siguiente_actividad_primer_alumno: (destino.focus(), destino.select_range(0, tk.END)))

    def _recalcular_promedio(self, indice_fila):
        datos_fila = self.registros_celdas.get(indice_fila)
        if not datos_fila:
            return

        try:
            valores_numericos = [float(v.get().strip()) for v in datos_fila["variables"] if v.get().strip()] 
            if any(val < 0 or val > 20 for val in valores_numericos):
                messagebox.showwarning("Valor Inválido", "Las notas deben estar entre 0 y 20.")
                return
            if valores_numericos:
                promedio_calculado = sum(valores_numericos) / len(valores_numericos)
                datos_fila["etiqueta_promedio"].config(text=f"{promedio_calculado:.1f}")
            else:
                datos_fila["etiqueta_promedio"].config(text="0.0")
        except ValueError:
            datos_fila["etiqueta_promedio"].config(text="Inválido")

    def _on_regresar(self):
        """Acción al presionar el botón Regresar."""
        if self.controlador_externo and hasattr(self.controlador_externo, "regresar_menu_principal"):
            self.controlador_externo.regresar_menu_principal()
        else:
            messagebox.showinfo("Navegación", "Regresando al menú principal...")

    def _on_aplicar_filtro(self):
        """Aplica la búsqueda basada en la materia, año y sección seleccionados."""
        materia_seleccionada = self.combo_materia.get()
        anio_seleccionado = self.combo_anio.get()
        seccion_seleccionada = self.combo_seccion.get()
        
        self.etiqueta_docente_valor.configure(text=f"Prof. Titular ({materia_seleccionada})")
        messagebox.showinfo("Filtro Aplicado", f"Cargando registros para:\n{materia_seleccionada} - {anio_seleccionado} Sección '{seccion_seleccionada}'")

    def _on_crear_actividad_global(self):
        nombre_nueva_actividad = self.entrada_nueva_actividad.get().strip()
        if not nombre_nueva_actividad:
            messagebox.showwarning("Campo Vacío", "Ingrese el nombre de la nueva actividad.")
            return
        if nombre_nueva_actividad in self.lista_actividades:
            messagebox.showwarning("Duplicado", "Ya existe una actividad con ese nombre.")
            return

        self.lista_actividades.append(nombre_nueva_actividad)
        for cedula, nombre, notas in self.estudiantes_data:
            notas.append("0.0")

        self._construir_planilla_interactiva()
        self.entrada_nueva_actividad.delete(0, tk.END)
        messagebox.showinfo("Éxito", f"Actividad '{nombre_nueva_actividad}' agregada correctamente.")

    def _on_renombrar_actividad(self):
        if not self.lista_actividades:
            messagebox.showwarning("Aviso", "No hay actividades registradas para renombrar.")
            return

        ventana_emergente = tk.Toplevel(self)
        ventana_emergente.title("Renombrar Actividad")
        ventana_emergente.geometry("340x180")
        ventana_emergente.resizable(False, False)
        ventana_emergente.grab_set()

        tk.Label(ventana_emergente, text="Seleccione la actividad a renombrar:", font=("Segoe UI", 9, "bold")).pack(pady=(12, 5), padx=12, anchor="w")
        
        combo_actividades = ttk.Combobox(ventana_emergente, values=self.lista_actividades, state="readonly", width=28)
        combo_actividades.pack(padx=12, pady=5)
        combo_actividades.set(self.lista_actividades[0])

        tk.Label(ventana_emergente, text="Nuevo nombre de la actividad:").pack(pady=(5, 2), padx=12, anchor="w")
        entrada_nuevo_nombre = ttk.Entry(ventana_emergente, width=30)
        entrada_nuevo_nombre.pack(padx=12, anchor="w")

        def aplicar_renombrado():
            nombre_antiguo = combo_actividades.get()
            nombre_nuevo = entrada_nuevo_nombre.get().strip()
            if not nombre_nuevo:
                messagebox.showerror("Error", "El nuevo nombre no puede estar vacío.", parent=ventana_emergente)
                return
            if nombre_nuevo in self.lista_actividades:
                messagebox.showerror("Error", "Ya existe otra actividad con ese nombre.", parent=ventana_emergente)
                return

            indice_actividad = self.lista_actividades.index(nombre_antiguo)
            self.lista_actividades[indice_actividad] = nombre_nuevo
            self._construir_planilla_interactiva()
            ventana_emergente.destroy()
            messagebox.showinfo("Éxito", f"Actividad renombrada a '{nombre_nuevo}'.")

        btn_guardar = ttk.Button(ventana_emergente, text="Guardar Cambios", command=aplicar_renombrado, style="Accent.TButton")
        btn_guardar.pack(pady=15)
        self._aplicar_cursor_mano(btn_guardar)

    def _on_eliminar_actividad(self):
        if not self.lista_actividades:
            messagebox.showwarning("Aviso", "No hay actividades registradas para eliminar.")
            return

        ventana_emergente = tk.Toplevel(self)
        ventana_emergente.title("Eliminar Actividad")
        ventana_emergente.geometry("340x190")
        ventana_emergente.resizable(False, False)
        ventana_emergente.grab_set()

        tk.Label(ventana_emergente, text="Seleccione la actividad a eliminar:", font=("Segoe UI", 9, "bold")).pack(pady=(12, 2), padx=12, anchor="w")
        
        combo_actividades = ttk.Combobox(ventana_emergente, values=self.lista_actividades, state="readonly", width=30)
        combo_actividades.pack(padx=12, pady=4)
        combo_actividades.set(self.lista_actividades[0])

        etiqueta_advertencia = tk.Label(
            ventana_emergente, 
            text="ADVERTENCIA: Si borra esta actividad,\nse eliminarán todas las notas cargadas.", 
            font=("Segoe UI", 8, "bold"),
            foreground="#b91c1c"
        )
        etiqueta_advertencia.pack(pady=6, padx=12, anchor="w")

        def confirmar_eliminacion():
            actividad_seleccionada = combo_actividades.get()
            respuesta_usuario = messagebox.askyesno(
                "Confirmación de Borrado", 
                f"¿Está completamente seguro de eliminar la actividad '{actividad_seleccionada}'?\nSe perderán permanentemente todas las notas asociadas.",
                parent=ventana_emergente
            )
            if respuesta_usuario:
                indice_act = self.lista_actividades.index(actividad_seleccionada)
                self.lista_actividades.pop(indice_act)
                for cedula, nombre, notas in self.estudiantes_data:
                    if indice_act < len(notas):
                        notas.pop(indice_act)

                self._construir_planilla_interactiva()
                ventana_emergente.destroy()
                messagebox.showinfo("Eliminado", f"La actividad '{actividad_seleccionada}' y sus notas fueron eliminadas.")

        btn_borrar = ttk.Button(ventana_emergente, text="Sí, Eliminar Actividad", command=confirmar_eliminacion, style="Danger.TButton")
        btn_borrar.pack(pady=10)
        self._aplicar_cursor_mano(btn_borrar)

    def _on_deshacer_cambios(self):
        if messagebox.askyesno("Deshacer Cambios", "¿Desea descartar todas las modificaciones y volver al estado inicial de la planilla?"):
            self.lista_actividades = copy.deepcopy(self.actividades_iniciales)
            self.estudiantes_data = copy.deepcopy(self.datos_estudiantes_iniciales)
            self._construir_planilla_interactiva()
            messagebox.showinfo("Restaurado", "Se han deshecho los cambios correctamente.")

    def _on_exportar_planilla_blanca(self):
        messagebox.showinfo(
            "Planilla en Blanco",
            f"Exportando formato vacío para impresión:\nAño: {self.combo_anio.get()}\nSección: {self.combo_seccion.get()}\nMateria: {self.combo_materia.get()}\n\n[Plantilla lista para impresión física]"
        )

    def _on_exportar_planilla_notas(self):
        messagebox.showinfo(
            "Planilla con Notas",
            f"Generando reporte oficial de calificaciones con notas actuales para:\n{self.combo_materia.get()} ({self.combo_anio.get()} Sección '{self.combo_seccion.get()}')\n\n[Documento generado con éxito]"
        )

    def _on_guardar_en_bd(self):
        datos_para_guardar = []
        
        for indice_fila, (cedula_estudiante, nombre_estudiante, _) in enumerate(self.estudiantes_data, start=1):
            controles_fila = self.registros_celdas.get(indice_fila)
            if controles_fila:
                notas_actuales = [var.get().strip() for var in controles_fila["variables"]]
                datos_para_guardar.append({
                    "cedula": cedula_estudiante,
                    "estudiante": nombre_estudiante,
                    "periodo": "2026-2027",
                    "anio": self.combo_anio.get(),
                    "seccion": self.combo_seccion.get(),
                    "materia": self.combo_materia.get(),
                    "actividades": self.lista_actividades,
                    "calificaciones": notas_actuales,
                    "promedio": controles_fila["etiqueta_promedio"]["text"]
                })

        if self.controlador_externo:
            self.controlador_externo.guardar_notas_bd(datos_para_guardar)
            messagebox.showinfo("Base de Datos", "Calificaciones enviadas al controlador con éxito.")
        else:
            print("--- DATOS EMPAQUETADOS PARA LA BD ---")
            for elemento in datos_para_guardar:
                print(elemento)
            messagebox.showinfo(
                "BD Simulada", 
                f"Se han procesado con éxito las notas de {len(datos_para_guardar)} estudiantes.\nEstructura lista para conectar con el backend."
            )

if __name__ == "__main__":
    raiz_aplicacion = tk.Tk()  
    raiz_aplicacion.title("Gestión Académica 2026 - Asignación de Notas")
    raiz_aplicacion.geometry("1220x720")
    
    app = VistaAsignacionNotas(contenedor_principal=raiz_aplicacion, controlador_externo=None)
    app.pack(fill="both", expand=True)
        
    raiz_aplicacion.mainloop()