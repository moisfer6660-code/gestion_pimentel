import copy
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class VistaAsignacionNotas(ttk.Frame):
    """Interfaz optimizada y profesional con ttk nativo, diseño plano sin líneas divisorias intrusivas."""

    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self.entries_celdas = {}  
        
        # Estado inicial base
        self.lista_actividades_inicial = ["Evaluación Inicial", "Taller N°1"]
        self.estudiantes_data_inicial = [
            ("V-33456789", "Pérez González, Alejandro", ["15.0", "19.0"]),
            ("V-33987123", "Rodríguez Silva, María Gabriela", ["14.0", "16.0"]),
            ("V-34112233", "Gómez Blanco, Jesús David", ["11.0", "13.0"]),
            ("V-34556677", "Martínez López, Valeria Sofía", ["20.0", "19.0"]),
        ]
        
        # Copias activas de trabajo
        self.lista_actividades = copy.deepcopy(self.lista_actividades_inicial)
        self.estudiantes_data = copy.deepcopy(self.estudiantes_data_inicial)

        self._configurar_estilos_ttk()
        self._construir_interfaz(self)

    def _configurar_estilos_ttk(self):
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")
        
        style.configure(".", font=("Segoe UI", 9))
        style.configure("TFrame", background="#f8fafc")
        
        style.configure("TButton", padding=(10, 6), relief="flat", background="#b91c1c", borderwidth=0, font=("Segoe UI", 9, "bold"), foreground="#FFFFFF")
        style.map("TButton", background=[("active", "#991b1b"), ("pressed", "#991b1b")])

        style.configure("Accent.TButton", background="#32B855", foreground="#ffffff")
        style.map("Accent.TButton", background=[("active", "#31B871"), ("pressed", "#31B871")])

        style.configure("Danger.TButton", background="#b91c1c", foreground="#ffffff")
        style.map("Danger.TButton", background=[("active", "#991b1b"), ("pressed", "#7f1d1d")])

    def _construir_interfaz(self, contenedor):
        contenedor.configure(style="TFrame")
        
        # 1. ENCABEZADO INSTITUCIONAL COMPACTO

        encabezado = ttk.Frame(contenedor, style="TFrame", height=75)
        encabezado.pack(fill="x", padx=20, pady=(10, 0))
        encabezado.pack_propagate(False)

        # Título y subtítulo a la izquierda
        frame_titulos = ttk.Frame(encabezado, style="TFrame")
        frame_titulos.place(x=0, y=8)

        lbl_titulo = ttk.Label(
            frame_titulos, 
            text="Control de Calificaciones", 
            font=("Segoe UI", 22, "bold"),
            foreground="#A93226",
            background="#f8fafc"
        )
        lbl_titulo.pack(anchor="w")

        lbl_sub = ttk.Label(
            frame_titulos, 
            text="Planilla Institucional", 
            font=("Segoe UI", 11, "italic"),
            foreground="#64748b",
            background="#f8fafc"
        )
        lbl_sub.pack(anchor="w", pady=(1, 0))

        # 2. PANEL DE SELECCIÓN JERÁRQUICA (Sin líneas divisorias pesadas, separación por espacio limpio)
        selector_filtro = ttk.Frame(contenedor, padding=8, style="TFrame")
        selector_filtro.pack(fill="x", padx=20, pady=(5, 5))
        selector_filtro.columnconfigure((1, 3), weight=1)

        ttk.Label(selector_filtro, text="Año / Grado:", font=("Segoe UI", 9, "bold"), background="#f8fafc").grid(row=0, column=0, sticky="w", pady=6, padx=5)
        self.combo_anio = ttk.Combobox(
            selector_filtro, values=["1er Año", "2do Año", "3er Año", "4to Año", "5to Año"], state="readonly", width=22
        )
        self.combo_anio.grid(row=0, column=1, sticky="w", pady=6, padx=5)
        self.combo_anio.set("1er Año")

        ttk.Label(selector_filtro, text="Sección:", font=("Segoe UI", 9, "bold"), background="#f8fafc").grid(row=0, column=2, sticky="w", pady=6, padx=15)
        letras_az = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        self.combo_seccion = ttk.Combobox(
            selector_filtro, values=letras_az, state="readonly", width=10
        )
        self.combo_seccion.grid(row=0, column=3, sticky="w", pady=6, padx=5)
        self.combo_seccion.set("A")

        ttk.Label(selector_filtro, text="Materia:", font=("Segoe UI", 9, "bold"), background="#f8fafc").grid(row=1, column=0, sticky="w", pady=6, padx=5)
        self.combo_materia = ttk.Combobox(
            selector_filtro, 
            values=["Matemáticas", "Castellano", "Inglés", "Biología", "Física", "Química", "Geografía e Historia"], 
            state="readonly",
            width=22
        )
        self.combo_materia.grid(row=1, column=1, sticky="w", pady=6, padx=5)
        self.combo_materia.set("Matemáticas")
        self.combo_materia.bind("<<ComboboxSelected>>", self._on_cambio_materia)

        ttk.Label(selector_filtro, text="Docente Asignado:", font=("Segoe UI", 9, "bold"), background="#f8fafc").grid(row=1, column=2, sticky="w", pady=6, padx=15)
        self.lbl_docente_valor = ttk.Label(selector_filtro, text="Prof. Carlos Mendoza (Matemáticas)", font=("Segoe UI", 9, "italic"), foreground="#0284c7", background="#f8fafc")
        self.lbl_docente_valor.grid(row=1, column=3, sticky="w", pady=6, padx=5)

        # 3. PANEL DE GESTIÓN DE ACTIVIDADES Y REPORTES (Espaciado limpio sin líneas divisorias)
        gestion_nota = ttk.Frame(contenedor, padding=5, style="TFrame")
        gestion_nota.pack(fill="x", padx=20, pady=(8, 10))

        ttk.Label(gestion_nota, text="Actividad:", font=("Segoe UI", 9, "bold"), background="#f8fafc").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.asignacion_nueva_actividad = ttk.Entry(gestion_nota, width=16)
        self.asignacion_nueva_actividad.grid(row=0, column=1, sticky="ew", padx=5)
        self.asignacion_nueva_actividad.insert(0, "Examen Parcial N°1")

        self.btn_crear_actividad = ttk.Button(gestion_nota, text="Agregar", command=self._on_crear_actividad_global)
        self.btn_crear_actividad.grid(row=0, column=2, padx=4)

        self.btn_renombrar_actividad = ttk.Button(gestion_nota, text="Renombrar", command=self._on_renombrar_actividad)
        self.btn_renombrar_actividad.grid(row=0, column=3, padx=4)

        self.btn_eliminar_actividad = ttk.Button(gestion_nota, text="Eliminar", command=self._on_eliminar_actividad, style="Danger.TButton")
        self.btn_eliminar_actividad.grid(row=0, column=4, padx=4)

        self.btn_deshacer = ttk.Button(gestion_nota, text="Deshacer", command=self._on_deshacer_cambios)
        self.btn_deshacer.grid(row=0, column=5, padx=4)

        self.btn_guardar_bd = ttk.Button(gestion_nota, text="Guardar", command=self._on_guardar_en_bd, style="Accent.TButton")
        self.btn_guardar_bd.grid(row=0, column=6, padx=4)

        self.btn_planilla_blanca = ttk.Button(gestion_nota, text="Planilla en Blanco", command=self._on_exportar_planilla_blanca)
        self.btn_planilla_blanca.grid(row=0, column=7, padx=4)

        self.btn_planilla_notas = ttk.Button(gestion_nota, text="Planilla con Notas", command=self._on_exportar_planilla_notas)
        self.btn_planilla_notas.grid(row=0, column=8, padx=4)

        # 4. PLANILLA DE NOTAS
        frame_tabla = ttk.Frame(contenedor, style="TFrame")
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=(5, 15))

        self.canvas = tk.Canvas(frame_tabla, bg="#ffffff", highlightthickness=0)
        self.scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.canvas.yview)
        
        self.marco_desplazamiento = ttk.Frame(self.canvas, style="TFrame")
        self.marco_desplazamiento.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.marco_desplazamiento, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")

        self._construir_planilla_interactiva()

        # 5. LOGOTIPO GRANDE FLOTANTE (CARGADO AL FINAL PARA QUEDAR EN LA CAPA SUPERIOR)
        try:
            ruta_logo = os.path.join(os.path.dirname(__file__), "logon.png")
            if os.path.exists(ruta_logo):
                img_pil = Image.open(ruta_logo).resize((185, 185), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img_pil)
                lbl_logo = ttk.Label(contenedor, image=self.logo_img, style="TLabel", background="#f8fafc")
                lbl_logo.place(relx=0.98, x=0, y=10, anchor="ne")
                lbl_logo.lift()
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")

    def _construir_planilla_interactiva(self):
        for widget in self.marco_desplazamiento.winfo_children():
            widget.destroy()
        self.entries_celdas.clear()

        nombre_columna = ["N°", "Cédula", "Apellidos y nombres del estudiante"] + self.lista_actividades + ["Promedio Real"]
        
        for columna, text in enumerate(nombre_columna):
            lbl = tk.Label(
                self.marco_desplazamiento, 
                text=text, 
                font=("Segoe UI", 9, "bold"),
                bg="#e2e8f0", 
                fg="#01112c", 
                relief="flat", 
                padx=10, 
                pady=8, 
                anchor="center" if columna != 2 else "w"
            )
            lbl.grid(row=0, column=columna, sticky="nsew", padx=1, pady=1)

        for indice_fila, (cedula, nombre, notas_lista) in enumerate(self.estudiantes_data, start=1):
            while len(notas_lista) < len(self.lista_actividades):
                notas_lista.append("0.0")
            if len(notas_lista) > len(self.lista_actividades):
                notas_lista = notas_lista[:len(self.lista_actividades)]
                self.estudiantes_data[indice_fila - 1] = (cedula, nombre, notas_lista)

            bg_fila = "#ffffff" if indice_fila % 2 != 0 else "#f8fafc"

            tk.Label(self.marco_desplazamiento, text=str(indice_fila), font=("Segoe UI", 9), relief="flat", bg=bg_fila, fg="#475569", anchor="center", padx=6, pady=6).grid(row=indice_fila, column=0, sticky="nsew", padx=1, pady=1)
            tk.Label(self.marco_desplazamiento, text=cedula, font=("Segoe UI", 10), relief="flat", bg=bg_fila, fg="#000000", anchor="center", padx=10, pady=6).grid(row=indice_fila, column=1, sticky="nsew", padx=1, pady=1)
            tk.Label(self.marco_desplazamiento, text=nombre, font=("Segoe UI", 9), relief="flat", bg=bg_fila, fg="#1e293b", anchor="w", padx=12, pady=6).grid(row=indice_fila, column=2, sticky="nsew", padx=1, pady=1)

            vars_fila = []
            for act_idx, nota_val in enumerate(notas_lista):
                var_nota = tk.StringVar(value=nota_val)
                entry_n = ttk.Entry(self.marco_desplazamiento, textvariable=var_nota, width=9, justify="center")
                entry_n.grid(row=indice_fila, column=3 + act_idx, padx=4, pady=4)
                vars_fila.append(var_nota)

            col_prom_idx = 3 + len(self.lista_actividades)
            lbl_promedio = tk.Label(self.marco_desplazamiento, text="0.0", font=("Segoe UI", 9, "bold"), fg="#15803d", bg=bg_fila, relief="flat", anchor="center", padx=6, pady=6)
            lbl_promedio.grid(row=indice_fila, column=col_prom_idx, sticky="nsew", padx=1, pady=1)

            self.entries_celdas[indice_fila] = {
                "vars": vars_fila,
                "lbl_prom": lbl_promedio
            }

            for var_n in vars_fila:
                var_n.trace_add("write", lambda *args, r=indice_fila: self._recalcular_promedio(r))

            self._recalcular_promedio(indice_fila)

    def _recalcular_promedio(self, indice_fila):
        datos = self.entries_celdas.get(indice_fila)
        if not datos:
            return

        try:
            valores = [float(v.get().strip()) for v in datos["vars"] if v.get().strip()] 
            if any(v < 0 or v > 20 for v in valores):
                messagebox.showwarning("Valor Inválido", "Las notas deben estar entre 0 y 20.")
                return
            if valores:
                promedio = sum(valores) / len(valores)
                datos["lbl_prom"].config(text=f"{promedio:.1f}")
            else:
                datos["lbl_prom"].config(text="0.0")
        except ValueError:
            datos["lbl_prom"].config(text="Inválido")

    def _on_cambio_materia(self, event):
        materia = self.combo_materia.get()
        self.lbl_docente_valor.configure(text=f"Prof. Titular ({materia})")

    def _on_crear_actividad_global(self):
        nueva_act = self.asignacion_nueva_actividad.get().strip()
        if not nueva_act:
            messagebox.showwarning("Campo Vacío", "Ingrese el nombre de la nueva actividad.")
            return
        if nueva_act in self.lista_actividades:
            messagebox.showwarning("Duplicado", "Ya existe una actividad con ese nombre.")
            return

        self.lista_actividades.append(nueva_act)
        for cedula, nombre, notas in self.estudiantes_data:
            notas.append("0.0")

        self._construir_planilla_interactiva()
        self.asignacion_nueva_actividad.delete(0, tk.END)
        messagebox.showinfo("Éxito", f"Actividad '{nueva_act}' agregada correctamente.")

    def _on_renombrar_actividad(self):
        if not self.lista_actividades:
            messagebox.showwarning("Aviso", "No hay actividades registradas para renombrar.")
            return

        top = tk.Toplevel(self)
        top.title("Renombrar Actividad")
        top.geometry("340x180")
        top.resizable(False, False)
        top.grab_set()

        ttk.Label(top, text="Seleccione la actividad a renombrar:", 
                  font=("Segoe UI", 9, "bold")).pack(pady=(12, 5), padx=12, anchor="w"), 
        
        combo_act = ttk.Combobox(top, values=self.lista_actividades, state="readonly", width=28)
        combo_act.pack(padx=12, pady=5)
        combo_act.set(self.lista_actividades[0])

        ttk.Label(top, text="Nuevo nombre de la actividad:").pack(pady=(5, 2), padx=12, anchor="w")
        entry_nuevo = ttk.Entry(top, width=30)
        entry_nuevo.pack(padx=12, anchor="w")

        def aplicar_renombrado():
            viejo_nombre = combo_act.get()
            nuevo_nombre = entry_nuevo.get().strip()
            if not nuevo_nombre:
                messagebox.showerror("Error", "El nuevo nombre no puede estar vacío.", parent=top)
                return
            if nuevo_nombre in self.lista_actividades:
                messagebox.showerror("Error", "Ya existe otra actividad con ese nombre.", parent=top)
                return

            idx = self.lista_actividades.index(viejo_nombre)
            self.lista_actividades[idx] = nuevo_nombre
            self._construir_planilla_interactiva()
            top.destroy()
            messagebox.showinfo("Éxito", f"Actividad renombrada a '{nuevo_nombre}'.")

        ttk.Button(top, text="Guardar Cambios", command=aplicar_renombrado, style="Accent.TButton").pack(pady=15)

    def _on_eliminar_actividad(self):
        if not self.lista_actividades:
            messagebox.showwarning("Aviso", "No hay actividades registradas para eliminar.")
            return

        top = tk.Toplevel(self)
        top.title("Eliminar Actividad")
        top.geometry("340x190")
        top.resizable(False, False)
        top.grab_set()

        ttk.Label(top, text="Seleccione la actividad a eliminar:", font=("Segoe UI", 9, "bold")).pack(pady=(12, 2), padx=12, anchor="w")
        
        combo_act = ttk.Combobox(top, values=self.lista_actividades, state="readonly", width=30)
        combo_act.pack(padx=12, pady=4)
        combo_act.set(self.lista_actividades[0])

        lbl_advertencia = ttk.Label(
            top, 
            text="ADVERTENCIA: Si borra esta actividad,\nse eliminarán todas las notas cargadas.", 
            font=("Segoe UI", 8, "bold"),
            foreground="#b91c1c"
        )
        lbl_advertencia.pack(pady=6, padx=12, anchor="w")

        def confirmar_eliminacion():
            act_a_borrar = combo_act.get()
            respuesta = messagebox.askyesno(
                "Confirmación de Borrado", 
                f"¿Está completamente seguro de eliminar la actividad '{act_a_borrar}'?\nSe perderán permanentemente todas las notas asociadas.",
                parent=top
            )
            if respuesta:
                idx = self.lista_actividades.index(act_a_borrar)
                self.lista_actividades.pop(idx)
                for cedula, nombre, notas in self.estudiantes_data:
                    if idx < len(notas):
                        notas.pop(idx)

                self._construir_planilla_interactiva()
                top.destroy()
                messagebox.showinfo("Eliminado", f"La actividad '{act_a_borrar}' y sus notas fueron eliminadas.")

        ttk.Button(top, text="Sí, Eliminar Actividad", command=confirmar_eliminacion, style="Danger.TButton").pack(pady=10)

    def _on_deshacer_cambios(self):
        if messagebox.askyesno("Deshacer Cambios", "¿Desea descartar todas las modificaciones y volver al estado inicial de la planilla?"):
            self.lista_actividades = copy.deepcopy(self.lista_actividades_inicial)
            self.estudiantes_data = copy.deepcopy(self.estudiantes_data_inicial)
            self._construir_planilla_interactiva()
            messagebox.showinfo("Restaurado", "Se han deshecho los cambios correctamente.")

    def _on_exportar_planilla_blanca(self):
        messagebox.showinfo(
            "Planilla en Blanco",
            f"Exportando formato vacío para:\nAño: {self.combo_anio.get()}\nSección: {self.combo_seccion.get()}\nMateria: {self.combo_materia.get()}\n\n[Plantilla lista para impresión física o digital]"
        )

    def _on_exportar_planilla_notas(self):
        messagebox.showinfo(
            "Planilla con Notas",
            f"Generando reporte oficial de calificaciones con notas actuales para:\n{self.combo_materia.get()} ({self.combo_anio.get()} Sección '{self.combo_seccion.get()}')\n\n[Documento generado con éxito]"
        )

    def _on_guardar_en_bd(self):
        datos_a_guardar = []
        
        for indice_fila, (cedula, nombre, _) in enumerate(self.estudiantes_data, start=1):
            controles = self.entries_celdas.get(indice_fila)
            if controles:
                notas_actuales = [var.get().strip() for var in controles["vars"]]
                datos_a_guardar.append({
                    "cedula": cedula,
                    "estudiante": nombre,
                    "periodo": "2026-2027",
                    "anio": self.combo_anio.get(),
                    "seccion": self.combo_seccion.get(),
                    "materia": self.combo_materia.get(),
                    "actividades": self.lista_actividades,
                    "calificaciones": notas_actuales,
                    "promedio": controles["lbl_prom"]["text"]
                })

        if self.controlador:
            self.controlador.guardar_notas_bd(datos_a_guardar)
            messagebox.showinfo("Base de Datos", "Calificaciones enviadas al controlador con éxito.")
        else:
            print("--- DATOS EMPAQUETADOS PARA LA BD ---")
            for item in datos_a_guardar:
                print(item)
            messagebox.showinfo(
                "BD Simulada", 
                f"Se han procesado con éxito las notas de {len(datos_a_guardar)} estudiantes.\nEstructura lista para conectar con el backend."
            )

if __name__ == "__main__":
    root = tk.Tk()  
    root.title("Gestión Académica 2026 - Asignación de Notas")
    root.geometry("1220x720")
    
    app = VistaAsignacionNotas(parent=root, controlador=None)
    app.pack(fill="both", expand=True)
        
    root.mainloop()