"""
Aplicación principal del simulador masa-resorte (versión modular)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import datetime
from io import BytesIO

from .physics_engine import PhysicsEngine
from .animation_manager import AnimationManager
from .ui_components import ControlPanel, InfoPanel
from .config import COLORS, DEFAULT_PARAMETERS, PARAMETER_LIMITS, PRESETS, ANIMATION_CONFIG, TIPS

class MassSpringApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        
        # Inicializar componentes
        self.physics_engine = PhysicsEngine()
        self.animation_manager = None
        self.info_panel = None
        self.control_panels = {}
        
        # Parámetros actuales
        self.current_params = DEFAULT_PARAMETERS.copy()
        
        # Sistema de consejos
        self.tips = TIPS
        self.current_tip_index = 0
        self.tip_scheduler = None
        
        self.setup_styles()
        self.setup_gui()
        self.initialize_simulation()
        self.setup_automatic_tips()
    
    def setup_window(self):
        """Configurar ventana principal"""
        self.root.title("🔬 LABORATORIO VIRTUAL - Sistema Masa-Resorte")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg=COLORS["primary"])
        
        # Bindings de teclado
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", lambda e: self.root.attributes('-fullscreen', False))
    
    def setup_styles(self):
        """Configurar estilos de la interfaz"""
        style = ttk.Style()
        style.theme_use("clam")

        # Configurar estilos
        style.configure("Main.TFrame", background=COLORS["primary"])
        style.configure("Card.TFrame", background=COLORS["secondary"])
        style.configure(
            "Title.TLabel",
            background=COLORS["primary"],
            foreground=COLORS["accent1"],
            font=("Arial", 12, "bold"),
        )
        style.configure(
            "Value.TLabel",
            background=COLORS["secondary"],
            foreground=COLORS["accent4"],
            font=("Arial", 11, "bold"),
        )

        # Botones de control
        style.configure(
            "Control.TButton", background=COLORS["accent1"], foreground="black"
        )
        style.configure(
            "Info.TButton", background=COLORS["accent2"], foreground="black"
        )
        style.configure(
            "Danger.TButton", background=COLORS["accent3"], foreground="white"
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
            graph_container, bg=COLORS["secondary"], relief="ridge", bd=2, padx=10, pady=1
        )
        anim_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)

        anim_title = tk.Label(
            anim_frame,
            text="🎬 ANIMACIÓN EN TIEMPO REAL",
            bg=COLORS["secondary"],
            fg=COLORS["accent1"],
            font=("Arial", 11, "bold"),
        )
        anim_title.pack(pady=1)

        self.fig_anim = Figure(figsize=(4.5, 3), facecolor=COLORS["secondary"])
        self.ax_anim = self.fig_anim.add_subplot(111)

        self.canvas_anim = FigureCanvasTkAgg(self.fig_anim, anim_frame)
        self.canvas_anim.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Gráfico de desplazamiento
        graph_frame = tk.Frame(
            graph_container, bg=COLORS["secondary"], relief="ridge", bd=2, padx=10, pady=1
        )
        graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=2)

        graph_title = tk.Label(
            graph_frame,
            text="📊 DESPLAZAMIENTO vs TIEMPO",
            bg=COLORS["secondary"],
            fg=COLORS["accent2"],
            font=("Arial", 11, "bold"),
        )
        graph_title.pack(pady=1)

        self.fig_graph = Figure(figsize=(4.5, 3), facecolor=COLORS["secondary"])
        self.ax_graph = self.fig_graph.add_subplot(111)

        self.canvas_graph = FigureCanvasTkAgg(self.fig_graph, graph_frame)
        self.canvas_graph.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def setup_controls(self, parent):
        """Configurar área de controles e información"""
        controls_container = ttk.Frame(parent, style="Main.TFrame")
        controls_container.pack(fill=tk.BOTH, expand=True)

        # Panel de controles
        self.setup_control_panel(controls_container)

        # Panel de información
        self.info_panel = InfoPanel(controls_container)
    
    def setup_control_panel(self, parent):
        """Panel de controles interactivos"""
        control_frame = tk.Frame(
            parent, bg=COLORS["secondary"], relief="ridge", bd=2, padx=6, pady=2
        )
        control_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        title = tk.Label(
            control_frame,
            text="🎛️ PANEL DE CONTROL",
            bg=COLORS["secondary"],
            fg=COLORS["accent1"],
            font=("Arial", 12, "bold"),
        )
        title.pack(pady=2)

        # Controles de parámetros
        params_frame = tk.Frame(control_frame, bg=COLORS["secondary"])
        params_frame.pack(fill=tk.BOTH, expand=True, pady=1)

        # Crear paneles de control para cada parámetro
        self.create_parameter_panels(params_frame)
        
        # Selectores compactos
        self.create_selectors(control_frame)
        
        # Botones de acción
        self.create_action_buttons(control_frame)
    
    def create_parameter_panels(self, parent):
        """Crear paneles de control para cada parámetro"""
        # Fila 1 - Masa y Rigidez
        row1_frame = tk.Frame(parent, bg=COLORS["secondary"])
        row1_frame.pack(fill=tk.X, pady=1)

        # Masa
        mass_frame = tk.Frame(row1_frame, bg=COLORS["secondary"])
        mass_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        self.control_panels["mass"] = ControlPanel(
            mass_frame,
            "⚖️ MASA (kg)",
            PARAMETER_LIMITS["mass"]["min"],
            PARAMETER_LIMITS["mass"]["max"],
            PARAMETER_LIMITS["mass"]["step"],
            self.current_params["mass"],
            'mass',
            "Controla la inercia del sistema\n• 0.1-1 kg: Oscilaciones rápidas\n• 1-3 kg: Balanceado\n• 3-5 kg: Movimiento lento",
            self.on_parameter_change
        )

        # Rigidez
        stiffness_frame = tk.Frame(row1_frame, bg=COLORS["secondary"])
        stiffness_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=2)
        self.control_panels["stiffness"] = ControlPanel(
            stiffness_frame,
            "🧊 RIGIDEZ (N/m)",
            PARAMETER_LIMITS["stiffness"]["min"],
            PARAMETER_LIMITS["stiffness"]["max"],
            PARAMETER_LIMITS["stiffness"]["step"],
            self.current_params["stiffness"],
            'stiffness',
            "Fuerza del resorte\n• 0.5-3 N/m: Resorte suave\n• 3-8 N/m: Normal\n• 8-15 N/m: Resorte rígido",
            self.on_parameter_change
        )

        # Fila 2 - Fuerza y Frecuencia
        row2_frame = tk.Frame(parent, bg=COLORS["secondary"])
        row2_frame.pack(fill=tk.X, pady=1)

        # Fuerza
        force_frame = tk.Frame(row2_frame, bg=COLORS["secondary"])
        force_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        self.control_panels["force_amplitude"] = ControlPanel(
            force_frame,
            "🎯 FUERZA (N)",
            PARAMETER_LIMITS["force_amplitude"]["min"],
            PARAMETER_LIMITS["force_amplitude"]["max"],
            PARAMETER_LIMITS["force_amplitude"]["step"],
            self.current_params["force_amplitude"],
            'force_amplitude',
            "Intensidad de fuerza externa\n• 0 N: Movimiento libre\n• 0.1-3 N: Vibración suave\n• 3-10 N: Oscilaciones intensas",
            self.on_parameter_change
        )

        # Frecuencia
        freq_frame = tk.Frame(row2_frame, bg=COLORS["secondary"])
        freq_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=2)
        self.control_panels["frequency"] = ControlPanel(
            freq_frame,
            "📡 FRECUENCIA (rad/s)",
            PARAMETER_LIMITS["frequency"]["min"],
            PARAMETER_LIMITS["frequency"]["max"],
            PARAMETER_LIMITS["frequency"]["step"],
            self.current_params["frequency"],
            'frequency',
            "Velocidad de la fuerza\n• 0.1-1 rad/s: Suave\n• 1-3 rad/s: Normal\n• 3-8 rad/s: Rápido\n⚡ RESONANCIA cuando coincide con frecuencia natural",
            self.on_parameter_change
        )
        
        # Fila 3 - Amortiguamiento
        row3_frame = tk.Frame(parent, bg=COLORS["secondary"])
        row3_frame.pack(fill=tk.X, pady=1)
        
        # Amortiguamiento
        damping_frame = tk.Frame(row3_frame, bg=COLORS["secondary"])
        damping_frame.pack(fill=tk.BOTH, expand=True, padx=2)
        self.control_panels["damping"] = ControlPanel(
            damping_frame,
            "🛑 AMORTIGUAMIENTO",
            PARAMETER_LIMITS["damping"]["min"],
            PARAMETER_LIMITS["damping"]["max"],
            PARAMETER_LIMITS["damping"]["step"],
            self.current_params["damping"],
            'damping',
            "Fricción del sistema\n• 0.0: Sin fricción (ideal)\n• 0.1-0.5: Poco amortiguado\n• 0.5-1.5: Normal\n• 1.5-2.0: Muy amortiguado",
            self.on_parameter_change
        )
    
    def create_selectors(self, parent):
        """Crear selectores de tipo de fuerza y experimentos"""
        selector_frame = tk.Frame(parent, bg=COLORS["secondary"])
        selector_frame.pack(fill=tk.X, pady=4)

        # Tipo de fuerza
        force_frame = tk.Frame(selector_frame, bg=COLORS["secondary"])
        force_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)

        force_title = tk.Label(
            force_frame,
            text="🌊 TIPO DE FUERZA",
            bg=COLORS["secondary"],
            fg=COLORS["accent2"],
            font=("Arial", 9, "bold"),
        )
        force_title.pack()

        self.force_var = tk.StringVar(value=self.current_params["force_type"])
        forces = ["Coseno", "Seno", "Pulso", "Escalón"]
        for force in forces:
            tk.Radiobutton(
                force_frame,
                text=force,
                variable=self.force_var,
                value=force,
                command=self.on_force_type_change,
                bg=COLORS["secondary"],
                fg="white",
                selectcolor=COLORS["accent1"],
            ).pack(anchor=tk.W)

        # Botón info para tipo de fuerza
        tk.Button(
            force_frame,
            text="Información",
            bg=COLORS["accent2"],
            fg="black",
            font=("Arial", 7),
            command=lambda: messagebox.showinfo(
                "Tipos de Fuerza",
                "• COSENO: Oscilación suave y continua\n• SENO: Similar a coseno pero desplazada\n• PULSO: Fuerza intermitente\n• ESCALÓN: Fuerza constante después de 2s",
            ),
        ).pack(pady=2)

        # Experimentos
        preset_frame = tk.Frame(selector_frame, bg=COLORS["secondary"])
        preset_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        preset_title = tk.Label(
            preset_frame,
            text="🧪 EXPERIMENTOS",
            bg=COLORS["secondary"],
            fg=COLORS["accent4"],
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
                bg=COLORS["secondary"],
                fg="white",
                selectcolor=COLORS["accent3"],
            ).pack(anchor=tk.W)

        # Botón info para experimentos
        tk.Button(
            preset_frame,
            text="Información",
            bg=COLORS["accent4"],
            fg="black",
            font=("Arial", 7),
            command=lambda: messagebox.showinfo(
                "Experimentos Predefinidos",
                "• NORMAL: Configuración balanceada\n• RESONANCIA: Frecuencias coinciden \n• AMORTIGUADO: Alta fricción\n• LIBRE: Sin fuerza externa",
            ),
        ).pack(pady=2)
    
    def create_action_buttons(self, parent):
        """Crear botones de acción"""
        action_frame = tk.Frame(parent, bg=COLORS["secondary"])
        action_frame.pack(fill=tk.X, pady=4)
        
        # Botón Capturar
        tk.Button(
            action_frame,
            text="📸 Capturar",
            bg=COLORS["accent4"],
            fg="black",
            font=("Arial", 9, "bold"),
            command=self.take_snapshot
        ).pack(side=tk.LEFT, padx=2)

        # Botón Reiniciar
        tk.Button(
            action_frame,
            text="🔄 Reiniciar",
            bg=COLORS["accent1"],
            fg="black",
            font=("Arial", 9, "bold"),
            command=self.on_reset
        ).pack(side=tk.LEFT, padx=2)
        
        # Botón Volver al Inicio
        tk.Button(
            action_frame,
            text="🏠 Inicio",
            bg="#2181FF",
            fg="white",
            font=("Arial", 9, "bold"),
            command=self.return_to_welcome
        ).pack(side=tk.LEFT, padx=2)

        # Botón Salir
        tk.Button(
            action_frame,
            text="🚪 Salir",
            bg=COLORS["accent3"],
            fg="white",
            font=("Arial", 9, "bold"),
            command=self.quit_application
        ).pack(side=tk.LEFT, padx=2)

    def initialize_simulation(self):
        """Inicializar la simulación"""
        # Configurar motor físico
        self.physics_engine.set_parameters(**self.current_params)
        
        # Configurar gestor de animaciones
        self.animation_manager = AnimationManager(
            self.fig_anim, self.ax_anim, self.fig_graph, self.ax_graph
        )
        
        # Resolver sistema inicial - USAR simulation_time de CONFIG
        self.solution_t, self.solution_y = self.physics_engine.solve_system(
            t_max=ANIMATION_CONFIG["simulation_time"],
            num_points=ANIMATION_CONFIG["frames"]
        )
        
        # Iniciar animación - USAR interval de CONFIG
        self.animation_manager.start_animation(
            self.solution_t, self.solution_y, self.physics_engine,
            interval=ANIMATION_CONFIG["interval"]
        )
        
        # Actualizar información inicial
        self.update_info_panel()
        
        # Mostrar consejo inicial
        self.info_panel.update_tips("¡Bienvenido! Ajusta los parámetros y observa el comportamiento del sistema 🎯")
    
    def on_parameter_change(self, param_name, new_value):
        """Cuando cambia un parámetro"""
        self.current_params[param_name] = new_value
        self.update_simulation()
    
    def on_force_type_change(self):
        """Cuando cambia el tipo de fuerza"""
        self.current_params["force_type"] = self.force_var.get()
        self.info_panel.update_tips(f"Fuerza cambiada a: {self.force_var.get()}\nObserva el nuevo patrón de movimiento")
        self.update_simulation()
    
    def on_preset_change(self):
        """Cuando se selecciona un experimento predefinido"""
        preset_name = self.preset_var.get()
        preset = PRESETS[preset_name]
        
        # Actualizar parámetros
        for param, value in preset.items():
            self.current_params[param] = value
            if param in self.control_panels:
                self.control_panels[param].update_value(value)
        
        # Actualizar tipo de fuerza si está en el preset
        if "force_type" in preset:
            self.force_var.set(preset["force_type"])
        
        self.info_panel.update_tips(f"Experimento: {preset_name}\n¡Observa el comportamiento del sistema!")
        self.update_simulation()
    
    def update_simulation(self):
        """Actualizar toda la simulación"""
        # Actualizar motor físico
        self.physics_engine.set_parameters(**self.current_params)
        
        # Resolver sistema
        self.solution_t, self.solution_y = self.physics_engine.solve_system()
        
        # Reiniciar animación
        self.animation_manager.start_animation(
            self.solution_t, self.solution_y, self.physics_engine
        )
        
        # Redibujar canvas
        self.canvas_anim.draw()
        self.canvas_graph.draw()
        
        # Actualizar información
        self.update_info_panel()
    
    def update_info_panel(self):
        """Actualizar panel de información"""
        system_info = self.physics_engine.get_system_info()
        self.info_panel.update_system_info(system_info)
    
    def on_reset(self):
        """Reiniciar el sistema"""
        # Restablecer parámetros por defecto
        self.current_params = DEFAULT_PARAMETERS.copy()
        
        # Actualizar controles
        for param_name, control_panel in self.control_panels.items():
            control_panel.update_value(self.current_params[param_name])
        
        # Restablecer selectores
        self.force_var.set(self.current_params["force_type"])
        self.preset_var.set("Normal")
        
        # Actualizar simulación
        self.update_simulation()
        
        # Actualizar consejos
        self.info_panel.update_tips("¡Sistema reiniciado! Comienza a experimentar 🎯")
    
    def setup_automatic_tips(self):
        """Configurar consejos automáticos"""
        self.show_next_tip()
        self.tip_scheduler = self.root.after(5000, self.schedule_tips)
    
    def schedule_tips(self):
        """Programar próximo consejo"""
        self.show_next_tip()
        self.tip_scheduler = self.root.after(5000, self.schedule_tips)
    
    def show_next_tip(self):
        """Mostrar siguiente consejo"""
        if self.tips:
            tip = self.tips[self.current_tip_index]
            self.info_panel.update_tips(f"💡 {tip}")
            self.current_tip_index = (self.current_tip_index + 1) % len(self.tips)
    
    def take_snapshot(self):
        """Tomar captura del estado actual"""
        try:
            from PIL import ImageGrab, Image
        except ImportError:
            self.info_panel.update_tips("❌ Error: PIL no está instalado. Ejecuta: pip install pillow")
            return
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"snapshot_m{self.current_params['mass']}_k{self.current_params['stiffness']}_c{self.current_params['damping']}_{timestamp}.png"

        try:
            # Intentar capturar ventana completa
            self.root.update()
            x = self.root.winfo_rootx()
            y = self.root.winfo_rooty()
            w = self.root.winfo_width()
            h = self.root.winfo_height()

            bbox = (x, y, x + w, y + h)
            img = ImageGrab.grab(bbox)
            img.save(f"snapshot_{filename}", quality=95)
            
            self.info_panel.update_tips(f"📸 Captura guardada: snapshot_{filename}")
            
        except Exception as e:
            # Fallback: guardar solo las figuras
            try:
                buf_anim = BytesIO()
                buf_graph = BytesIO()
                self.fig_anim.savefig(buf_anim, dpi=150, facecolor=self.fig_anim.get_facecolor(), bbox_inches='tight')
                self.fig_graph.savefig(buf_graph, dpi=150, facecolor=self.fig_graph.get_facecolor(), bbox_inches='tight')

                buf_anim.seek(0)
                buf_graph.seek(0)
                img1 = Image.open(buf_anim).convert("RGBA")
                img2 = Image.open(buf_graph).convert("RGBA")

                # Combinar imágenes
                target_h = max(img1.height, img2.height)
                img1 = img1.resize((int(img1.width * target_h / img1.height), target_h), Image.LANCZOS)
                img2 = img2.resize((int(img2.width * target_h / img2.height), target_h), Image.LANCZOS)

                gap = 20
                new_img = Image.new("RGBA", (img1.width + img2.width + gap, target_h), (26, 30, 46, 255))
                new_img.paste(img1, (0, 0))
                new_img.paste(img2, (img1.width + gap, 0))

                new_img.convert("RGB").save(f"snapshot_{filename}", quality=95)
                self.info_panel.update_tips(f"📸 Captura combinada guardada: snapshot_{filename}")
                
            except Exception as e2:
                self.info_panel.update_tips(f"❌ Error al guardar captura: {str(e2)}")
    
    def toggle_fullscreen(self, event=None):
        """Alternar pantalla completa"""
        self.fullscreen = not self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', self.fullscreen)
    
    def return_to_welcome(self):
        """Volver a la pantalla de bienvenida"""
        # Detener animación y consejos
        if self.animation_manager:
            self.animation_manager.stop_animation()
        if self.tip_scheduler:
            self.root.after_cancel(self.tip_scheduler)
        
        # Cerrar ventana actual
        self.root.destroy()
        
        # Crear nueva ventana de bienvenida
        from .welcome_screen import WelcomeScreen
        welcome_root = tk.Tk()
        welcome_app = WelcomeScreen(welcome_root)
        welcome_root.mainloop()
    
    def quit_application(self):
        """Salir de la aplicación"""
        # Detener animación y consejos
        if self.animation_manager:
            self.animation_manager.stop_animation()
        if self.tip_scheduler:
            self.root.after_cancel(self.tip_scheduler)
        
        # Cerrar aplicación
        self.root.quit()
        self.root.destroy()