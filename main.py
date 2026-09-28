"""
=============================================================================
PROYECTO: Tarea 1 - Escape de la Torre
ARCHIVO: main.py
DECLARACIÓN DE AUTORÍA:
La interfaz gráfica de usuario (GUI) contenida en este archivo ha sido 
desarrollada con la asistencia de Inteligencia Artificial Generativa, 
cumpliendo con lo estipulado en las bases de la evaluación para componentes 
opcionales de visualización.
=============================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
from simulacion import SimulacionEscape

# =============================================================================
# DEFINICIÓN DE ENTORNOS DE PRUEBA
# =============================================================================

# Mapa 1 (Alta densidad / Cuello de botella)
# Pasillos muy angostos que convergen hacia una única salida.
# Tamaño: 20x11 | Agentes: 80
MAPA_1 = [
    "####################",
    "#F                S#",
    "############### ####",  
    "#                  #",
    "####### #### #######",  
    "#                 F#",
    "### #### #### #### #",  
    "#          F       #",
    "#F                 #",
    "#                  #",
    "####################"
]

# Mapa 2 (Densidad media / Laberinto corporativo)
# Múltiples salas conectadas por intersecciones y cruces ciegos.
# Tamaño: 30x15 | Agentes: 80
MAPA_2 = [
    "##############################",
    "#     #      #     F#       S#",
    "# ### # #### # #### # ###### #",
    "# #        #        #        #",
    "# # ###### ######## ######## #",
    "#   #    #   #    # #   #    #",
    "##### ## ### # ## # # # # ####",
    "#     #      #  #     #      #",
    "####### ######## ###### ######",
    "#       #      #      #      #",
    "# ##### # #### ###### ###### #",
    "# #   # #    #      # #      #",
    "# # # # #### ###### # # ######",
    "#F  #        #F              #",
    "##############################"
]

# Mapa 3 (Baja densidad / Dispersión abierta)
# Entorno semiabierto con baja concentración de muros y múltiples rutas.
# Tamaño: 40x18 | Agentes: 200
MAPA_3 = [
    "########################################",
    "#                                     S#",
    "#  ##          ##       F  ##          #",
    "#  ##          ##          ##          #",
    "#                                      #",
    "#       ####        ####        ####   #",
    "#       ####        ####        ####   #",
    "#F                                     #",
    "#                                      #",
    "#  ##          ##          ##          #",
    "#  ##          ##          ##          #",
    "#                                      #",
    "#F                                     #",
    "#       ####        ####        ####   #",
    "#       ####        ####        ####   #",
    "#                             F        #",
    "#                                      #",
    "########################################"
]

def generar_posiciones(mapa_grid, cantidad):
    """
    Selecciona posiciones transitables al azar para distribuir a los agentes en el mapa.

    Identifica todas las casillas marcadas como libres (' ') y extrae una muestra 
    aleatoria correspondiente a la cantidad de agentes.

    Args:
        mapa_grid (list of str): Matriz bidimensional que representa el entorno.
        cantidad (int): Número de agentes a posicionar.

    Returns:
        list of tuple: Coordenadas (fila, columna) iniciales para los agentes.
    """
    filas = len(mapa_grid)
    cols = len(mapa_grid[0])
    
    # Recolectar todas las casillas libres transitables
    libres = []
    for r in range(filas):
        for c in range(cols):
            if mapa_grid[r][c] == ' ':
                libres.append((r, c))

    # Tomar muestra sin reemplazo si el espacio es suficiente
    if len(libres) >= cantidad:
        return random.sample(libres, cantidad)
    else:
        # Selección con reemplazo para entornos densos (sobreocupación)
        return [random.choice(libres) for _ in range(cantidad)]

# Configuración predeterminada de parámetros por escenario:
# (Matriz del Mapa, Posiciones iniciales de agentes, Frecuencia propagación k_fuego)
MAPAS_DISPONIBLES = {
    "Mapa 1: Cuello de botella (10 agentes)": (MAPA_1, generar_posiciones(MAPA_1, 80), 3),
    "Mapa 2: Laberinto corporativo (80 agentes)": (MAPA_2, generar_posiciones(MAPA_2, 80), 3),
    "Mapa 3: Dispersión abierta (200 agentes)": (MAPA_3, generar_posiciones(MAPA_3, 200), 2)
}

# =============================================================================
# CLASE DE LA INTERFAZ GRÁFICA
# =============================================================================

class InterfazEscapeTorre:
    """
    Controlador principal de la interfaz de usuario para la simulación de evacuación.
    
    Administra los componentes de Tkinter, inicializa el motor de simulación subyacente
    y coordina la actualización del renderizado gráfico (Canvas) turno a turno.
    """

    def __init__(self, master):
        """
        Inicializa la ventana principal y los componentes de diseño.
        
        Args:
            master (tk.Tk): Ventana raíz de Tkinter.
        """
        self.master = master
        self.master.title("Simulador: Escape de la Torre - Inteligencia Artificial")
        self.master.resizable(False, False)

        # Variables de estado y configuración
        self.simulacion = None
        self.algoritmo_seleccionado = tk.StringVar(value="BFS")
        self.mapa_seleccionado = tk.StringVar(value="Mapa 1: Cuello de botella (10 agentes)")
        self.auto_ejecucion = False
        self.tam_celda = 35

        # Inicialización de paneles visuales
        self.crear_panel_controles()
        self.crear_panel_estadisticas()
        
        self.canvas = tk.Canvas(master, bg="#2b2b2b")
        self.canvas.pack(padx=15, pady=10)

        self.crear_leyenda()
        self.reiniciar_simulacion()

    def crear_panel_controles(self):
        """
        Construye la barra superior con menús desplegables y botones de ejecución.
        Permite seleccionar el entorno, el algoritmo de búsqueda y regular la velocidad.
        """
        panel = ttk.LabelFrame(self.master, text=" Controles de Simulación ", padding=10)
        panel.pack(fill="x", padx=15, pady=5)

        # Selector de Mapa
        ttk.Label(panel, text="Mapa:").grid(row=0, column=0, padx=5, sticky="w")
        cb_mapa = ttk.Combobox(panel, textvariable=self.mapa_seleccionado, 
                               values=list(MAPAS_DISPONIBLES.keys()), state="readonly", width=38)
        cb_mapa.grid(row=0, column=1, padx=5)
        cb_mapa.bind("<<ComboboxSelected>>", lambda e: self.reiniciar_simulacion())

        # Selector de Algoritmo de Búsqueda
        ttk.Label(panel, text="Algoritmo:").grid(row=0, column=2, padx=5, sticky="w")
        cb_algoritmo = ttk.Combobox(panel, textvariable=self.algoritmo_seleccionado, 
                                    values=["BFS", "DFS", "Greedy", "A*", "Genético"], state="readonly", width=10)
        cb_algoritmo.grid(row=0, column=3, padx=5)

        # Botones de control de ejecución
        self.btn_paso = ttk.Button(panel, text="Avanzar Turno", command=self.avanzar_un_turno)
        self.btn_paso.grid(row=0, column=4, padx=5)

        self.btn_auto = ttk.Button(panel, text="Iniciar Auto", command=self.alternar_auto)
        self.btn_auto.grid(row=0, column=5, padx=5)

        self.btn_reiniciar = ttk.Button(panel, text="Reiniciar", command=self.reiniciar_simulacion)
        self.btn_reiniciar.grid(row=0, column=6, padx=5)

        # Control de velocidad (delay de actualización)
        ttk.Label(panel, text="Velocidad:").grid(row=0, column=7, padx=5)
        self.slider_velocidad = ttk.Scale(panel, from_=20, to=500, orient="horizontal", value=150)
        self.slider_velocidad.grid(row=0, column=8, padx=5)

    def crear_panel_estadisticas(self):
        """
        Genera la barra de estado inferior para monitorizar métricas críticas 
        en tiempo real (turnos transcurridos, sobrevivientes y bajas).
        """
        panel = ttk.Frame(self.master, padding=5)
        panel.pack(fill="x", padx=15)

        self.lbl_turno = ttk.Label(panel, text="Turno: 0", font=("Arial", 10, "bold"))
        self.lbl_turno.pack(side="left", padx=15)

        self.lbl_vivos = ttk.Label(panel, text="En camino: 0", foreground="#1f77b4", font=("Arial", 10, "bold"))
        self.lbl_vivos.pack(side="left", padx=15)

        self.lbl_salvados = ttk.Label(panel, text="Evacuados: 0", foreground="#2ca02c", font=("Arial", 10, "bold"))
        self.lbl_salvados.pack(side="left", padx=15)

        self.lbl_muertos = ttk.Label(panel, text="Bajas: 0", foreground="#d62728", font=("Arial", 10, "bold"))
        self.lbl_muertos.pack(side="left", padx=15)

        self.lbl_estado = ttk.Label(panel, text="Estado: En curso", font=("Arial", 10, "italic"))
        self.lbl_estado.pack(side="right", padx=15)

    def crear_leyenda(self):
        """
        Dibuja los indicadores de colores (muro, salida, fuego, agentes) para facilitar
        la interpretación visual de la grilla espacial.
        """
        panel = ttk.Frame(self.master, padding=5)
        panel.pack(fill="x", padx=15, pady=5)

        elementos = [
            ("Muro (#)", "#333333"),
            ("Salida (S)", "#2ecc71"),
            ("Fuego (F)", "#e74c3c"),
            ("Agente Activo", "#3498db"),
            ("Baja", "#7f8c8d")
        ]

        for texto, color in elementos:
            box = tk.Canvas(panel, width=14, height=14, bg=color, highlightthickness=1, highlightbackground="gray")
            box.pack(side="left", padx=(10, 2))
            lbl = ttk.Label(panel, text=texto, font=("Arial", 8))
            lbl.pack(side="left", padx=(0, 10))

    def reiniciar_simulacion(self):
        """
        Restablece el estado global del sistema de simulación al turno 0.
        Escala dinámicamente la cuadrícula del Canvas dependiendo de las 
        dimensiones del mapa seleccionado.
        """
        self.detener_auto()
        mapa, agentes_pos, k_fuego = MAPAS_DISPONIBLES[self.mapa_seleccionado.get()]
        
        self.simulacion = SimulacionEscape(mapa, k_fuego, agentes_pos)
        
        # Ajuste dinámico del tamaño de las celdas según las dimensiones
        if self.simulacion.cols >= 40:
            self.tam_celda = 22
        elif self.simulacion.cols >= 30:
            self.tam_celda = 28
        else:
            self.tam_celda = 35
            
        ancho = self.simulacion.cols * self.tam_celda
        alto = self.simulacion.filas * self.tam_celda
        self.canvas.config(width=ancho, height=alto)

        self.actualizar_vista()
        self.lbl_estado.config(text="Estado: En curso", foreground="black")

    def avanzar_un_turno(self):
        """
        Invoca la lógica de progresión temporal para calcular un solo ciclo de tiempo
        (movimiento de agentes y propagación del fuego) y refleja los cambios gráficos.
        """
        if not self.simulacion.terminar():
            self.simulacion.turno(self.algoritmo_seleccionado.get())
            self.actualizar_vista()

            # Detectar condición de parada
            if self.simulacion.terminar():
                self.detener_auto()
                salvados = sum(1 for a in self.simulacion.agentes if a.evacuado)
                total = len(self.simulacion.agentes)
                self.lbl_estado.config(text=f"Terminado ({salvados}/{total} evacuados)", foreground="#2ca02c")
                
                # Desplegar alerta final con los resultados
                messagebox.showinfo("Simulación Finalizada", 
                                    f"La evacuación terminó en el turno {self.simulacion.turno_actual}.\n"
                                    f"Supervivientes: {salvados}/{total}\n"
                                    f"Tasa de supervivencia: {(salvados/total)*100:.1f}%")

    def alternar_auto(self):
        """Alterna entre el modo de ejecución paso a paso y el avance autónomo."""
        if self.auto_ejecucion:
            self.detener_auto()
        else:
            if not self.simulacion.terminar():
                self.auto_ejecucion = True
                self.btn_auto.config(text="Pausar")
                self.btn_paso.config(state="disabled")
                self.bucle_auto()

    def bucle_auto(self):
        """
        Lazo recursivo manejado por 'after' para ejecutar turnos consecutivos 
        sin bloquear el hilo principal de la interfaz gráfica.
        """
        if self.auto_ejecucion and not self.simulacion.terminar():
            self.avanzar_un_turno()
            velocidad = int(self.slider_velocidad.get())
            self.master.after(velocidad, self.bucle_auto)
        else:
            self.detener_auto()

    def detener_auto(self):
        """Interrumpe la simulación continua y habilita los controles manuales."""
        self.auto_ejecucion = False
        self.btn_auto.config(text="Iniciar Auto")
        self.btn_paso.config(state="normal")

    def actualizar_vista(self):
        """
        Renderiza la vista top-down del entorno basándose en la matriz de estado.
        Dibuja la cuadrícula, colores identificativos y superpone el contador de 
        congestión sobre las celdas densamente pobladas.
        """
        self.canvas.delete("all")
        s = self.tam_celda

        # Renderizado de celdas base
        for i in range(self.simulacion.filas):
            for j in range(self.simulacion.cols):
                x0, y0 = j * s, i * s
                x1, y1 = x0 + s, y0 + s
                tipo = self.simulacion.mapa[i][j]

                # Asignación de colores según la naturaleza del obstáculo
                color = "#ecf0f1"
                if tipo == '#':
                    color = "#2c3e50"
                elif tipo == 'S':
                    color = "#2ecc71"
                elif tipo == 'F':
                    color = "#e74c3c"

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#bdc3c7")

                # Etiquetado de celdas con alta densidad (cuellos de botella)
                congest = self.simulacion.congestion[i][j]
                if congest > 1 and tipo not in ['#', 'F', 'S']:
                    font_size = max(6, s // 4)
                    self.canvas.create_text(x1 - (s//4), y0 + (s//4), text=f"×{congest}", 
                                            fill="#e67e22", font=("Arial", font_size, "bold"))

        # Renderizado de agentes vivos o fallecidos
        for a in self.simulacion.agentes:
            if a.evacuado:
                continue

            i, j = a.posicion
            padding = s // 6
            x0 = j * s + padding
            y0 = i * s + padding
            x1 = x0 + s - (padding * 2)
            y1 = y0 + s - (padding * 2)

            color_agente = "#7f8c8d" if a.muerto else "#2980b9"
            self.canvas.create_oval(x0, y0, x1, y1, fill=color_agente, outline="white", width=1)

        # Actualización de contadores estadísticos en la UI
        vivos = sum(1 for a in self.simulacion.agentes if not a.evacuado and not a.muerto)
        salvados = sum(1 for a in self.simulacion.agentes if a.evacuado)
        muertos = sum(1 for a in self.simulacion.agentes if a.muerto)

        self.lbl_turno.config(text=f"Turno: {self.simulacion.turno_actual}")
        self.lbl_vivos.config(text=f"En camino: {vivos}")
        self.lbl_salvados.config(text=f"Evacuados: {salvados}")
        self.lbl_muertos.config(text=f"Bajas: {muertos}")


if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazEscapeTorre(ventana)
    ventana.mainloop()