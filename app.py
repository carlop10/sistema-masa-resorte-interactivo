import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk, messagebox
from scipy.integrate import solve_ivp
import matplotlib.animation as animation
import time


class WelcomeScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Bienvenido al Laboratorio Virtual")
        self.root.geometry("800x600")
        self.root.configure(bg="#1A1A2E")

        # Configurar estilo moderno
        self.setup_styles()
        self.setup_welcome_screen()
        
        

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Colores modernos
        style.configure("Modern.TFrame", background="#1A1A2E")
        style.configure(
            "Title.TLabel",
            background="#1A1A2E",
            foreground="#00D4FF",
            font=("Arial", 28, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background="#1A1A2E",
            foreground="#64FFDA",
            font=("Arial", 16),
        )
        style.configure(
            "Accent.TButton",
            background="#00D4FF",
            foreground="black",
            font=("Arial", 12, "bold"),
        )
        style.configure(
            "Exit.TButton",
            background="#FF2E63",
            foreground="white",
            font=("Arial", 12, "bold"),
        )

    def setup_welcome_screen(self):
        # Frame principal con gradiente
        main_frame = ttk.Frame(self.root, style="Modern.TFrame", padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Logo/Icono
        emoji_label = ttk.Label(
            main_frame, text="🔬", font=("Arial", 60), background="#1A1A2E"
        )
        emoji_label.pack(pady=2)

        # Título principal
        title_label = ttk.Label(
            main_frame, text="LABORATORIO VIRTUAL", style="Title.TLabel"
        )
        title_label.pack(pady=2)

        subtitle_label = ttk.Label(
            main_frame, text="Sistema Masa-Resorte Interactivo", style="Subtitle.TLabel"
        )
        subtitle_label.pack(pady=2)

        # Frame de información con tarjetas
        info_frame = ttk.Frame(main_frame, style="Modern.TFrame")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=2)

        # Conceptos básicos en tarjeta
        concepts_card = tk.Frame(
            info_frame, bg="#16213E", relief="raised", bd=2, padx=20, pady=2
        )
        concepts_card.pack(fill=tk.BOTH, expand=True, pady=2)

        concepts_title = tk.Label(
            concepts_card,
            text="🎓 CONCEPTOS BÁSICOS",
            bg="#16213E",
            fg="#00D4FF",
            font=("Arial", 14, "bold"),
        )
        concepts_title.pack(pady=2)

        concepts_text = """
• ⚖️ MASA: Inercia del sistema... Más masa = Movimiento más lento
• 🧊 RIGIDEZ: Fuerza del resorte... Más rigidez = Oscilaciones más rápidas  
• 🎯 FUERZA: Energía externa aplicada al sistema
• ⚡ RESONANCIA: Cuando frecuencia externa = frecuencia natural
• 🛑 AMORTIGUAMIENTO: Fricción que disipa energía
        """

        concepts_label = tk.Label(
            concepts_card,
            text=concepts_text,
            bg="#16213E",
            fg="white",
            font=("Arial", 11),
            justify=tk.LEFT,
        )
        concepts_label.pack(pady=1)

        # Instrucciones en tarjeta
        instructions_card = tk.Frame(
            info_frame, bg="#0F3460", relief="raised", bd=2, padx=20, pady=2
        )
        instructions_card.pack(fill=tk.BOTH, expand=True, pady=2)

        instructions_title = tk.Label(
            instructions_card,
            text="🎮 INSTRUCCIONES",
            bg="#0F3460",
            fg="#64FFDA",
            font=("Arial", 14, "bold"),
        )
        instructions_title.pack(pady=2)

        instructions_text = """
1. Usa los botones + y - para ajustar parámetros
2. Prueba los experimentos predefinidos  
3. Observa la animación en tiempo real
4. ¡Busca la RESONANCIA!
5. Experimenta y aprende física divertida
        """

        instructions_label = tk.Label(
            instructions_card,
            text=instructions_text,
            bg="#0F3460",
            fg="white",
            font=("Arial", 11, "bold"),
            justify=tk.LEFT,
        )
        instructions_label.pack(pady=1)

        # Botones con estilo moderno
        button_frame = ttk.Frame(main_frame, style="Modern.TFrame")
        button_frame.pack(pady=4)

        ttk.Button(
            button_frame,
            text="🚀 INICIAR EXPERIMENTO",
            command=self.start_lab,
            style="Accent.TButton",
        ).pack(side=tk.LEFT, padx=15)

        ttk.Button(
            button_frame, text="❌ SALIR", command=self.root.quit, style="Exit.TButton"
        ).pack(side=tk.LEFT, padx=15)

    def start_lab(self):
        self.root.destroy()
        root = tk.Tk()
        app = MassSpringApp(root)
        root.mainloop()


class MassSpringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔬 LABORATORIO VIRTUAL - Sistema Masa-Resorte")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1A1A2E")

        # Parámetros del sistema
        self.m = 1.0
        self.k = 4.0
        self.c = 0.1
        self.F0 = 2.0
        self.omega = 2.0
        self.force_type = "cos"
        self.achievements = set()

        # Configurar estilos modernos
        self.setup_styles()
        # Configurar el layout principal
        self.setup_gui()

        # Inicializar simulación
        self.solution_t, self.solution_y = self.solve_system()
        self.setup_animation()
        
        # Sistema de consejos automáticos
        self.tips = [
            "🔬 **CONSEJO**: La frecuencia natural se calcula como √(k/m). ¡Ajusta masa y rigidez para cambiarla!",
            "⚡ **FENÓMENO**: La resonancia ocurre cuando la frecuencia externa iguala a la natural del sistema",
            "🎯 **EXPERIMENTO**: Prueba el preset 'Resonancia' para ver oscilaciones dramáticas",
            "🔄 **OBSERVA**: El amortiguamiento disipa energía y reduce gradualmente las oscilaciones",
            "📊 **ANÁLISIS**: La gráfica muestra cómo el desplazamiento varía con el tiempo",
            "⚖️ **FÍSICA**: Más masa = más inercia = oscilaciones más lentas",
            "🧊 **PROPIEDAD**: Resortes más rígidos oscilan más rápido",
            "🌊 **PATRÓN**: Diferentes tipos de fuerza crean distintos patrones de movimiento",
            "🔍 **CURIOSIDAD**: Los edificios altos usan amortiguadores para resistir terremotos",
            "🎵 **APLICACIÓN**: Los instrumentos musicales usan resonancia para producir sonidos",
            "🏗️ **INGENIERÍA**: Los puentes deben diseñarse para evitar resonancia con el viento",
            "🚗 **EJEMPLO**: Los amortiguadores de autos protegen contra vibraciones en caminos",
            "⏰ **DATOS**: El período de oscilación es 2π/ω, donde ω es la frecuencia natural",
            "💡 **CONSEJO**: Para resonancia pura, ajusta frecuencia externa = √(k/m)",
            "📈 **VISUAL**: Amplitud máxima en resonancia = F0/(m*ω²) para sistemas no amortiguados",
            "🛡️ **SEGURIDAD**: Demasiada resonancia puede dañar estructuras mecánicas",
            "🎮 **EXPLORA**: Experimenta con combinaciones extremas para entender límites del sistema",
            "🔧 **CONTROL**: Usa amortiguamiento para estabilizar sistemas resonantes",
            "📚 **HISTORIA**: El puente de Tacoma Narrows colapsó por resonancia con el viento en 1940",
            "🌟 **LOGRO**: ¡Has descubierto la resonancia! Es uno de los fenómenos más importantes en física"
        ]
        self.current_tip_index = 0
        self.setup_automatic_tips()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Colores modernos y vibrantes
        colors = {
            "primary": "#1A1A2E",
            "secondary": "#16213E",
            "accent1": "#00D4FF",
            "accent2": "#64FFDA",
            "accent3": "#FF2E63",
            "accent4": "#FFD166",
            "text": "#FFFFFF",
        }

        # Configurar estilos
        style.configure("Main.TFrame", background=colors["primary"])
        style.configure("Card.TFrame", background=colors["secondary"])
        style.configure(
            "Title.TLabel",
            background=colors["primary"],
            foreground=colors["accent1"],
            font=("Arial", 12, "bold"),
        )
        style.configure(
            "Value.TLabel",
            background=colors["secondary"],
            foreground=colors["accent4"],
            font=("Arial", 11, "bold"),
        )

        # Botones de control
        style.configure(
            "Control.TButton", background=colors["accent1"], foreground="black"
        )
        style.configure(
            "Info.TButton", background=colors["accent2"], foreground="black"
        )
        style.configure(
            "Danger.TButton", background=colors["accent3"], foreground="white"
        )

    def setup_gui(self):
        """Configurar la interfaz gráfica"""
        main_frame = ttk.Frame(self.root, style="Main.TFrame", padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Dividir en 2 filas principales
        # Fila 1: Gráficos
        graph_frame = ttk.Frame(main_frame, style="Main.TFrame")
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=1)

        # Fila 2: Controles e información
        control_frame = ttk.Frame(main_frame, style="Main.TFrame")
        control_frame.pack(fill=tk.BOTH, expand=True, pady=1)

        # Configurar gráficos
        self.setup_graphs(graph_frame)

        # Configurar controles e información
        self.setup_controls(control_frame)

    def setup_graphs(self, parent):
        """Configurar área de gráficos"""
        graph_container = ttk.Frame(parent, style="Main.TFrame")
        graph_container.pack(fill=tk.BOTH, expand=True)

        # Gráfico de animación
        anim_frame = tk.Frame(
            graph_container, bg="#16213E", relief="ridge", bd=2, padx=10, pady=1
        )
        anim_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)

        anim_title = tk.Label(
            anim_frame,
            text="🎬 ANIMACIÓN EN TIEMPO REAL",
            bg="#16213E",
            fg="#00D4FF",
            font=("Arial", 11, "bold"),
        )
        anim_title.pack(pady=1)

        self.fig_anim = Figure(figsize=(4.5, 3), facecolor="#16213E")
        self.ax_anim = self.fig_anim.add_subplot(111)
        self.setup_animation_plot()

        self.canvas_anim = FigureCanvasTkAgg(self.fig_anim, anim_frame)
        self.canvas_anim.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Gráfico de desplazamiento
        graph_frame = tk.Frame(
            graph_container, bg="#16213E", relief="ridge", bd=2, padx=10, pady=1
        )
        graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=2)

        graph_title = tk.Label(
            graph_frame,
            text="📊 DESPLAZAMIENTO vs TIEMPO",
            bg="#16213E",
            fg="#64FFDA",
            font=("Arial", 11, "bold"),
        )
        graph_title.pack(pady=1)

        self.fig_graph = Figure(figsize=(4.5, 3), facecolor="#16213E")
        self.ax_graph = self.fig_graph.add_subplot(111)
        self.setup_graph_plot()

        self.canvas_graph = FigureCanvasTkAgg(self.fig_graph, graph_frame)
        self.canvas_graph.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def setup_animation_plot(self):
        """Configurar gráfico de animación"""
        self.ax_anim.clear()
        self.ax_anim.set_xlim(-4, 6)
        self.ax_anim.set_ylim(-1.5, 1.5)
        self.ax_anim.set_aspect("equal")
        self.ax_anim.set_facecolor("#0F3460")
        self.ax_anim.set_title(
            "Sistema Masa-Resorte", color="#00D4FF", fontweight="bold", fontsize=10
        )
        self.ax_anim.grid(True, alpha=0.3, color="#00D4FF")

        # Pared
        self.ax_anim.axvline(x=-3, color="#FF2E63", linewidth=8, alpha=0.8)

        # Resorte y masa
        (self.spring_line,) = self.ax_anim.plot([], [], "#00D4FF", linewidth=3)
        self.mass = plt.Circle((0, 0), 0.2, fc="#FF2E63", ec="#FFD166", linewidth=2)
        self.ax_anim.add_patch(self.mass)

        # Texto de resonancia
        self.res_text = self.ax_anim.text(
            0, 1.3, "", fontsize=10, ha="center", fontweight="bold", color="#FFD166"
        )

        # Configurar colores
        self.ax_anim.tick_params(colors="white", labelsize=8)
        for spine in self.ax_anim.spines.values():
            spine.set_color("#00D4FF")

    def setup_graph_plot(self):
        """Configurar gráfico de desplazamiento"""
        self.ax_graph.clear()
        self.ax_graph.set_xlim(0, 20)
        self.ax_graph.set_ylim(-3, 3)
        self.ax_graph.set_facecolor("#0F3460")
        
        self.ax_graph.set_xlabel("Tiempo (s)", color="white", fontsize=9)
        self.ax_graph.set_ylabel("Desplazamiento (m)", color="white", fontsize=9)
        self.ax_graph.grid(True, alpha=0.3, color="#64FFDA")
        self.ax_graph.tick_params(colors="white", labelsize=8)

        (self.graph_line,) = self.ax_graph.plot([], [], "#64FFDA", linewidth=2)
        self.time_line = self.ax_graph.axvline(
            x=0, color="#FF2E63", linestyle="--", alpha=0.7
        )

        for spine in self.ax_graph.spines.values():
            spine.set_color("#64FFDA")

    def create_control_panel(self, parent, title, min_val, max_val, step, current_val, param_name, info_text):
        """Crear panel de control con botones + y -"""
        frame = tk.Frame(parent, bg='#16213E', relief='groove', bd=1, padx=8, pady=1)
        frame.pack(fill=tk.BOTH, expand=True, pady=1)
        
        # Título y valor actual
        title_frame = tk.Frame(frame, bg='#16213E')
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(title_frame, text=title, bg='#16213E', fg='#00D4FF', 
                            font=('Arial', 9, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # Botón de información
        info_btn = tk.Button(title_frame, text="i", bg="#2181FF", fg='white', 
                            font=('Arial', 7), width=2, height=1,
                            command=lambda: messagebox.showinfo(f"Info: {title}", info_text))
        info_btn.pack(side=tk.RIGHT, padx=5)
        
        value_label = tk.Label(title_frame, text=f"{current_val:.1f}", 
                            bg='#16213E', fg='#FFD166', font=('Arial', 10, 'bold'))
        value_label.pack(side=tk.RIGHT)
        
        # Botones de control
        btn_frame = tk.Frame(frame, bg='#16213E')
        btn_frame.pack(fill=tk.X, pady=2)
        
        def adjust_value(delta):
            current = getattr(self, param_name)
            new_val = current + delta
            new_val = max(min_val, min(max_val, new_val))
            setattr(self, param_name, new_val)
            value_label.config(text=f"{new_val:.1f}")
            self.on_parameter_change()
        
        minus_btn = tk.Button(btn_frame, text="➖", bg='#FF2E63', fg='white', 
                            font=('Arial', 6, 'bold'), width=4,
                            command=lambda: adjust_value(-step))
        minus_btn.pack(side=tk.LEFT, padx=2)
        
        plus_btn = tk.Button(btn_frame, text="➕", bg='#00D4FF', fg='black', 
                            font=('Arial', 6, 'bold'), width=4,
                            command=lambda: adjust_value(step))
        plus_btn.pack(side=tk.LEFT, padx=2)
        
        return value_label

    def adjust_value(self, new_val, min_val, max_val, callback, value_label):
        """Ajustar valor dentro de los límites"""
        new_val = max(min_val, min(max_val, new_val))
        value_label.config(text=f"{new_val:.1f}")
        callback(new_val)

    def setup_controls(self, parent):
        """Configurar área de controles e información"""
        controls_container = ttk.Frame(parent, style="Main.TFrame")
        controls_container.pack(fill=tk.BOTH, expand=True)

        # Panel de controles
        self.setup_control_panel(controls_container)

        # Panel de información
        self.setup_info_panel(controls_container)

    def setup_control_panel(self, parent):
        """Panel de controles interactivos"""
        control_frame = tk.Frame(
            parent, bg="#16213E", relief="ridge", bd=2, padx=6, pady=2
        )
        control_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        title = tk.Label(
            control_frame,
            text="🎛️ PANEL DE CONTROL",
            bg="#16213E",
            fg="#00D4FF",
            font=("Arial", 12, "bold"),
        )
        title.pack(pady=2)

        # Controles de parámetros en grid 2x2
        params_frame = tk.Frame(control_frame, bg="#16213E")
        params_frame.pack(fill=tk.BOTH, expand=True, pady=1)

        # Fila 1 - Masa y Rigidez
        row1_frame = tk.Frame(params_frame, bg="#16213E")
        row1_frame.pack(fill=tk.X, pady=1)

        # Masa (columna 1)
        mass_frame = tk.Frame(row1_frame, bg="#16213E")
        mass_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        self.mass_label = self.create_control_panel(
            mass_frame,
            "⚖️ MASA (kg)",
            0.1,
            5.0,
            0.1,
            self.m,
            'm',
            "Controla la inercia del sistema\n• 0.1-1 kg: Oscilaciones rápidas\n• 1-3 kg: Balanceado\n• 3-5 kg: Movimiento lento",
        )

        # Rigidez (columna 2)
        stiffness_frame = tk.Frame(row1_frame, bg="#16213E")
        stiffness_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=2)
        self.k_label = self.create_control_panel(
            stiffness_frame,
            "🧊 RIGIDEZ (N/m)",
            0.5,
            15.0,
            0.5,
            self.k,
            'k',
            "Fuerza del resorte\n• 0.5-3 N/m: Resorte suave\n• 3-8 N/m: Normal\n• 8-15 N/m: Resorte rígido",
        )

        # Fila 2 - Fuerza y Frecuencia
        row2_frame = tk.Frame(params_frame, bg="#16213E")
        row2_frame.pack(fill=tk.X, pady=1)

        # Fuerza (columna 1)
        force_frame = tk.Frame(row2_frame, bg="#16213E")
        force_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        self.F0_label = self.create_control_panel(
            force_frame,
            "🎯 FUERZA (N)",
            0.0,
            10.0,
            0.5,
            self.F0,
            'F0',
            "Intensidad de fuerza externa\n• 0 N: Movimiento libre\n• 0.1-3 N: Vibración suave\n• 3-10 N: Oscilaciones intensas",
        )

        # Frecuencia (columna 2)
        freq_frame = tk.Frame(row2_frame, bg="#16213E")
        freq_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=2)
        self.omega_label = self.create_control_panel(
            freq_frame,
            "📡 FRECUENCIA (rad/s)",
            0.1,
            8.0,
            0.1,
            self.omega,
            'omega',
            "Velocidad de la fuerza\n• 0.1-1 rad/s: Suave\n• 1-3 rad/s: Normal\n• 3-8 rad/s: Rápido\n⚡ RESONANCIA cuando coincide con frecuencia natural",
        )

        # Selectores compactos
        selector_frame = tk.Frame(control_frame, bg="#16213E")
        selector_frame.pack(fill=tk.X, pady=4)

        # Tipo de fuerza
        force_frame = tk.Frame(selector_frame, bg="#16213E")
        force_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)

        force_title = tk.Label(
            force_frame,
            text="🌊 TIPO DE FUERZA",
            bg="#16213E",
            fg="#64FFDA",
            font=("Arial", 9, "bold"),
        )
        force_title.pack()

        self.force_var = tk.StringVar(value="Coseno")
        forces = ["Coseno", "Seno", "Pulso", "Escalón"]
        for force in forces:
            tk.Radiobutton(
                force_frame,
                text=force,
                variable=self.force_var,
                value=force,
                command=self.on_force_type_change,
                bg="#16213E",
                fg="white",
                selectcolor="#00D4FF",
            ).pack(anchor=tk.W)

        # Botón info para tipo de fuerza
        tk.Button(
            force_frame,
            text="ℹ️ Info",
            bg="#64FFDA",
            fg="black",
            font=("Arial", 7),
            command=lambda: messagebox.showinfo(
                "Tipos de Fuerza",
                "• COSENO: Oscilación suave y continua\n• SENO: Similar a coseno pero desplazada\n• PULSO: Fuerza intermitente\n• ESCALÓN: Fuerza constante después de 2s",
            ),
        ).pack(pady=2)

        # Experimentos
        preset_frame = tk.Frame(selector_frame, bg="#16213E")
        preset_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        preset_title = tk.Label(
            preset_frame,
            text="🧪 EXPERIMENTOS",
            bg="#16213E",
            fg="#FFD166",
            font=("Arial", 9, "bold"),
        )
        preset_title.pack()

        self.preset_var = tk.StringVar(value="Normal")
        presets = ["Normal", "Resonancia", "Amortiguado", "Libre"]
        for preset in presets:
            tk.Radiobutton(
                preset_frame,
                text=preset,
                variable=self.preset_var,
                value=preset,
                command=self.on_preset_change,
                bg="#16213E",
                fg="white",
                selectcolor="#FF2E63",
            ).pack(anchor=tk.W)

        # Botón info para experimentos
        tk.Button(
            preset_frame,
            text="ℹ️ Info",
            bg="#FFD166",
            fg="black",
            font=("Arial", 7),
            command=lambda: messagebox.showinfo(
                "Experimentos Predefinidos",
                "• NORMAL: Configuración balanceada\n• RESONANCIA: Frecuencias coinciden (¡efecto dramático!)\n• AMORTIGUADO: Alta fricción\n• LIBRE: Sin fuerza externa",
            ),
        ).pack(pady=2)

        # Botones de acción
        action_frame = tk.Frame(control_frame, bg="#16213E")
        action_frame.pack(fill=tk.X, pady=4)

        tk.Button(
            action_frame,
            text="🔄 Reiniciar",
            bg="#00D4FF",
            fg="black",
            font=("Arial", 9, "bold"),
            command=self.on_reset,
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            action_frame,
            text="🚪 Salir",
            bg="#FF2E63",
            fg="white",
            font=("Arial", 9, "bold"),
            command=self.root.quit,
        ).pack(side=tk.LEFT, padx=2)

    def setup_info_panel(self, parent):
        """Panel de información y logros"""
        info_frame = tk.Frame(
            parent, bg="#16213E", relief="ridge", bd=2, padx=10, pady=4
        )
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        title = tk.Label(
            info_frame,
            text="🎓 TABLERO INFORMATIVO",
            bg="#16213E",
            fg="#00D4FF",
            font=("Arial", 12, "bold"),
        )
        title.pack(pady=5)

        # Estado del sistema
        system_frame = tk.Frame(
            info_frame, bg="#0F3460", relief="groove", bd=1, padx=8, pady=2
        )
        system_frame.pack(fill=tk.X, pady=2)

        system_title = tk.Label(
            system_frame,
            text="📊 ESTADO DEL SISTEMA",
            bg="#0F3460",
            fg="#64FFDA",
            font=("Arial", 10, "bold"),
        )
        system_title.pack(anchor=tk.W)

        self.system_text = tk.Text(
            system_frame,
            height=3,
            width=30,
            bg="#0F3460",
            fg="white",
            font=("Arial", 9),
            wrap=tk.WORD,
            relief="flat",
        )
        self.system_text.pack(fill=tk.BOTH, expand=True, pady=2)
        self.system_text.insert(
            tk.END, "Frecuencia Natural: 2.00 rad/s\nRazón: 1.00\nEstado: Normal"
        )
        self.system_text.config(state=tk.DISABLED)

        # Logros
        achievements_frame = tk.Frame(
            info_frame, bg="#0F3460", relief="groove", bd=1, padx=8, pady=2
        )
        achievements_frame.pack(fill=tk.X, pady=2)

        achievements_title = tk.Label(
            achievements_frame,
            text="🏆 LOGROS",
            bg="#0F3460",
            fg="#FFD166",
            font=("Arial", 10, "bold"),
        )
        achievements_title.pack(anchor=tk.W)

        self.achievements_text = tk.Text(
            achievements_frame,
            height=2,
            width=30,
            bg="#0F3460",
            fg="#FFD166",
            font=("Arial", 9),
            wrap=tk.WORD,
            relief="flat",
        )
        self.achievements_text.pack(fill=tk.BOTH, expand=True, pady=2)
        self.achievements_text.insert(tk.END, "• Ninguno aún")
        self.achievements_text.config(state=tk.DISABLED)

        # Consejos
        tips_frame = tk.Frame(
            info_frame, bg="#0F3460", relief="groove", bd=1, padx=8, pady=2
        )
        tips_frame.pack(fill=tk.BOTH, expand=True, pady=2)

        tips_title = tk.Label(
            tips_frame,
            text="💡 CONSEJOS",
            bg="#0F3460",
            fg="#FF2E63",
            font=("Arial", 10, "bold"),
        )
        tips_title.pack(anchor=tk.W)

        self.tips_text = tk.Text(
            tips_frame,
            height=3,
            width=30,
            bg="#0F3460",
            fg="#64FFDA",
            font=("Arial", 9),
            wrap=tk.WORD,
            relief="flat",
        )
        self.tips_text.pack(fill=tk.BOTH, expand=True, pady=2)
        self.tips_text.insert(
            tk.END,
            "¡Prueba el experimento 'Resonancia' para ver oscilaciones dramáticas! 🔥",
        )
        self.tips_text.config(state=tk.DISABLED)

    def external_force(self, t):
        force_type_map = {
            "Coseno": "cos",
            "Seno": "sin",
            "Pulso": "pulse",
            "Escalón": "step",
        }
        actual_type = force_type_map.get(self.force_var.get(), "cos")

        if actual_type == "cos":
            return self.F0 * np.cos(self.omega * t)
        elif actual_type == "sin":
            return self.F0 * np.sin(self.omega * t)
        elif actual_type == "pulse":
            return self.F0 * (0.5 + 0.5 * np.sign(np.sin(self.omega * t)))
        elif actual_type == "step":
            return self.F0 * (t > 2.0)
        return 0.0

    def equation(self, t, Y):
        y, yp = Y
        force = self.external_force(t)
        dydt = yp
        dypdt = (-self.k * y - self.c * yp + force) / self.m
        return [dydt, dypdt]

    def solve_system(self):
        t_eval = np.linspace(0, 20, 800)
        sol = solve_ivp(self.equation, [0, 20], [0, 0], t_eval=t_eval, method="RK45")
        return sol.t, sol.y[0]

    def create_spring_coords(self, y_pos):
        spring_end_x = -3 + y_pos + 3
        x_vals = np.linspace(-3, spring_end_x, 80)
        n_coils = 10
        y_vals = 0.2 * np.sin(n_coils * np.pi * np.linspace(0, 1, 80))
        return x_vals, y_vals

    def setup_animation(self):
        """Configurar la animación"""
        self.ani = animation.FuncAnimation(
            self.fig_anim,
            self.update_animation,
            frames=len(self.solution_t),
            interval=25,
            blit=True,
            repeat=True,
            cache_frame_data=False,
        )

    def update_animation(self, frame):
        if frame >= len(self.solution_t):
            return (
                self.spring_line,
                self.mass,
                self.graph_line,
                self.res_text,
                self.time_line,
            )

        t, y = self.solution_t, self.solution_y
        current_y = y[frame]
        current_t = t[frame]

        # Actualizar animación
        spring_x, spring_y = self.create_spring_coords(current_y)
        self.spring_line.set_data(spring_x, spring_y)
        self.mass.center = (-3 + current_y + 3, 0)

        # Actualizar gráfico
        self.graph_line.set_data(t[: frame + 1], y[: frame + 1])
        self.time_line.set_xdata([current_t, current_t])

        # Ajustar límites dinámicos
        if frame > 10:
            y_max = max(1, np.max(np.abs(y[: frame + 1])) * 1.2)
            self.ax_graph.set_ylim(-y_max, y_max)
            self.ax_graph.set_xlim(0, max(20, current_t + 1))

        # Verificar resonancia
        natural_freq = np.sqrt(self.k / self.m)
        if abs(self.omega - natural_freq) < 0.2 and self.F0 > 0:
            self.res_text.set_text("⚡ ¡RESONANCIA!")
            self.mass.set_facecolor("#FFD166")
            self.spring_line.set_color("#FF2E63")
        else:
            self.res_text.set_text("")
            self.mass.set_facecolor("#FF2E63")
            self.spring_line.set_color("#00D4FF")

        # Actualizar panel de información
        self.update_info_panel(natural_freq)

        return (
            self.spring_line,
            self.mass,
            self.graph_line,
            self.res_text,
            self.time_line,
        )

    def update_info_panel(self, natural_freq):
        """Actualizar el panel de información"""
        # Calcular si hay resonancia
        is_resonance = abs(self.omega - natural_freq) < 0.2 and self.F0 > 0
        
        # Estado del sistema
        system_info = f"Frecuencia Natural: {natural_freq:.2f} rad/s\n"
        system_info += f"Frecuencia Externa: {self.omega:.2f} rad/s\n"
        system_info += f"Razón: {self.omega/natural_freq:.2f}\n"
        
        # Determinar estado basado en parámetros actuales
        if is_resonance:
            system_info += "Estado: ⚡ RESONANCIA"
        elif self.F0 == 0:
            system_info += "Estado: 🌀 MOVIMIENTO LIBRE"
        elif self.c > 1.0:
            system_info += "Estado: 🛑 AMORTIGUADO FUERTE"
        else:
            system_info += "Estado: ✅ NORMAL"
        
        self.system_text.config(state=tk.NORMAL)
        self.system_text.delete(1.0, tk.END)
        self.system_text.insert(tk.END, system_info)
        self.system_text.config(state=tk.DISABLED)

    def on_parameter_change(self, event=None):
        """Cuando cambia cualquier parámetro"""
        # Actualizar etiquetas de valores
        self.mass_label.config(text=f"{self.m:.1f}")
        self.k_label.config(text=f"{self.k:.1f}")
        self.F0_label.config(text=f"{self.F0:.1f}")
        self.omega_label.config(text=f"{self.omega:.1f}")

        self.solution_t, self.solution_y = self.solve_system()
        self.canvas_anim.draw()
        self.canvas_graph.draw()

    def on_force_type_change(self):
        """Cuando cambia el tipo de fuerza"""
        self.tips_text.config(state=tk.NORMAL)
        self.tips_text.delete(1.0, tk.END)
        self.tips_text.insert(
            tk.END,
            f"Fuerza cambiada a: {self.force_var.get()}\nObserva el nuevo patrón de movimiento",
        )
        self.tips_text.config(state=tk.DISABLED)

        self.solution_t, self.solution_y = self.solve_system()

    def on_preset_change(self):
        """Cuando se selecciona un experimento predefinido"""
        presets = {
            "Normal": {"m": 1.0, "k": 4.0, "F0": 2.0, "omega": 2.0, "c": 0.1},
            "Resonancia": {"m": 1.0, "k": 4.0, "F0": 3.0, "omega": 2.0, "c": 0.05},
            "Amortiguado": {"m": 2.0, "k": 4.0, "F0": 1.0, "omega": 1.0, "c": 1.5},
            "Libre": {"m": 1.0, "k": 4.0, "F0": 0.0, "omega": 2.0, "c": 0.0},
        }

        preset = presets[self.preset_var.get()]
        self.m = preset["m"]
        self.k = preset["k"]
        self.F0 = preset["F0"]
        self.omega = preset["omega"]
        self.c = preset["c"]

        # Actualizar controles visuales
        self.mass_label.config(text=f"{self.m:.1f}")
        self.k_label.config(text=f"{self.k:.1f}")
        self.F0_label.config(text=f"{self.F0:.1f}")
        self.omega_label.config(text=f"{self.omega:.1f}")

        self.tips_text.config(state=tk.NORMAL)
        self.tips_text.delete(1.0, tk.END)
        self.tips_text.insert(
            tk.END,
            f"Experimento: {self.preset_var.get()}\n¡Observa el comportamiento del sistema!",
        )
        self.tips_text.config(state=tk.DISABLED)

        self.solution_t, self.solution_y = self.solve_system()

    def on_reset(self):
        """Reiniciar el sistema"""
        self.achievements.clear()
        self.m = 1.0
        self.k = 4.0
        self.F0 = 2.0
        self.omega = 2.0
        self.force_var.set("Coseno")
        self.preset_var.set("Normal")
        self.c = 0.1

        # Actualizar controles visuales
        self.mass_label.config(text=f"{self.m:.1f}")
        self.k_label.config(text=f"{self.k:.1f}")
        self.F0_label.config(text=f"{self.F0:.1f}")
        self.omega_label.config(text=f"{self.omega:.1f}")

        self.achievements_text.config(state=tk.NORMAL)
        self.achievements_text.delete(1.0, tk.END)
        self.achievements_text.insert(tk.END, "• Ninguno aún")
        self.achievements_text.config(state=tk.DISABLED)

        self.tips_text.config(state=tk.NORMAL)
        self.tips_text.delete(1.0, tk.END)
        self.tips_text.insert(tk.END, "¡Sistema reiniciado! Comienza a experimentar 🎯")
        self.tips_text.config(state=tk.DISABLED)

        self.solution_t, self.solution_y = self.solve_system()

    def show_random_tip(self):
        """Mostrar un consejo aleatorio"""
        tips = [
            "🔍 ¿Sabías? La resonancia puede hacer que puentes se colapsen si no se diseña bien",
            "🎯 Prueba ajustar masa y rigidez para cambiar la frecuencia natural",
            "⚡ La resonancia ocurre cuando frecuencia externa = frecuencia natural",
            "🔄 El amortiguamiento hace que las oscilaciones desaparezcan gradualmente",
            "🎮 ¡Experimenta con diferentes combinaciones para descubrir patrones!",
            "📚 Usa los botones ℹ️ para aprender sobre cada parámetro del sistema",
            "🔥 En resonancia, pequeñas fuerzas pueden crear oscilaciones muy grandes",
        ]
        import random

        self.tips_text.config(state=tk.NORMAL)
        self.tips_text.delete(1.0, tk.END)
        self.tips_text.insert(tk.END, f"💡 {random.choice(tips)}")
        self.tips_text.config(state=tk.DISABLED)


# Ejecutar la aplicación
if __name__ == "__main__":
    # Primero mostrar pantalla de bienvenida
    welcome_root = tk.Tk()
    welcome_app = WelcomeScreen(welcome_root)
    welcome_root.mainloop()
