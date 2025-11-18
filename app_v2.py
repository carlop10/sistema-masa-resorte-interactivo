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
        self.root.configure(bg='#2C3E50')
        
        self.setup_welcome_screen()
    
    def setup_welcome_screen(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título principal
        title_label = ttk.Label(main_frame, text="🔬 LABORATORIO VIRTUAL", 
                               font=('Arial', 24, 'bold'), foreground='white', background='#2C3E50')
        title_label.pack(pady=20)
        
        subtitle_label = ttk.Label(main_frame, text="Sistema Masa-Resorte", 
                                  font=('Arial', 18), foreground='#BDC3C7', background='#2C3E50')
        subtitle_label.pack(pady=10)
        
        # Frame de información
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=4)
        
        # Conceptos básicos
        concepts_text = """
📚 CONCEPTOS BÁSICOS:

⚖️ MASA: Representa la inercia del sistema. 
   Más masa = Movimiento más lento

🧊 RIGIDEZ: Qué tan fuerte es el resorte.
   Más rigidez = Oscilaciones más rápidas

🎯 FUERZA EXTERNA: Energía que impulsa el sistema.
   Puede ser constante o oscilante

⚡ RESONANCIA: Fenómeno que ocurre cuando la frecuencia 
   externa coincide con la natural del sistema

🛑 AMORTIGUAMIENTO: Fricción que disipa energía.
   Reduce gradualmente las oscilaciones
        """
        
        concepts_label = tk.Text(info_frame, height=15, width=60, bg='#34495E', fg='white',
                                font=('Arial', 8), wrap=tk.WORD, relief='flat', padx=10, pady=10)
        concepts_label.insert(tk.END, concepts_text)
        concepts_label.config(state=tk.DISABLED)
        concepts_label.pack(pady=10)
        
        # Instrucciones
        instructions_text = """
🎮 INSTRUCCIONES:

1. Usa los sliders para ajustar los parámetros del sistema
2. Prueba los experimentos predefinidos
3. Observa la animación y las gráficas en tiempo real
4. Busca el fenómeno de RESONANCIA
5. ¡Aprende jugando!
        """
        
        instructions_label = tk.Text(info_frame, height=8, width=60, bg='#34495E', fg='#F39C12',
                                    font=('Arial', 10, 'bold'), wrap=tk.WORD, relief='flat', padx=10, pady=10)
        instructions_label.insert(tk.END, instructions_text)
        instructions_label.config(state=tk.DISABLED)
        instructions_label.pack(pady=10)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=30)
        
        ttk.Button(button_frame, text="🚀 Iniciar Laboratorio", 
                  command=self.start_lab, style='Accent.TButton').pack(side=tk.LEFT, padx=10)
        
        ttk.Button(button_frame, text="❌ Salir", 
                  command=self.root.quit).pack(side=tk.LEFT, padx=10)
        
        # Configurar estilo para botón destacado
        style = ttk.Style()
        style.configure('Accent.TButton', foreground='white', background='#27AE60')
    
    def start_lab(self):
        self.root.destroy()  # Cerrar ventana de bienvenida
        root = tk.Tk()
        app = MassSpringApp(root)
        root.mainloop()

class MassSpringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔬 LABORATORIO VIRTUAL - Sistema Masa-Resorte")
        self.root.geometry("1200x800")  # Tamaño más manejable
        self.root.configure(bg='#2C3E50')
        
        # Parámetros del sistema
        self.m = 1.0
        self.k = 4.0
        self.c = 0.1
        self.F0 = 2.0
        self.omega = 2.0
        self.force_type = 'cos'
        self.achievements = set()
        
        # Configurar el layout principal con scroll
        self.setup_gui()
        
        # Inicializar simulación
        self.solution_t, self.solution_y = self.solve_system()
        self.setup_animation()
        
    def setup_gui(self):
        """Configurar la interfaz gráfica con Tkinter"""
        # Frame principal con scroll
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear un canvas y scrollbar para hacer scrollable
        self.canvas = tk.Canvas(main_frame, bg='#2C3E50')
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to scroll
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Dividir en 2 áreas principales
        # Fila 1: Gráficos
        graph_frame = ttk.Frame(self.scrollable_frame)
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Fila 2: Controles e información
        control_frame = ttk.Frame(self.scrollable_frame)
        control_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Configurar gráficos
        self.setup_graphs(graph_frame)
        
        # Configurar controles e información
        self.setup_controls(control_frame)
        
        # Botón de salir en la parte inferior
        exit_frame = ttk.Frame(self.scrollable_frame)
        exit_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(exit_frame, text="🚪 Salir del Laboratorio", 
                  command=self.root.quit, style='Danger.TButton').pack(pady=5)
        
        # Configurar estilos
        style = ttk.Style()
        style.configure('Danger.TButton', foreground='white', background='#E74C3C')
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def setup_graphs(self, parent):
        """Configurar área de gráficos"""
        # Frame para gráficos
        graph_container = ttk.Frame(parent)
        graph_container.pack(fill=tk.BOTH, expand=True)
        
        # Gráfico de animación (izquierda)
        anim_frame = ttk.LabelFrame(graph_container, text="🎬 ANIMACIÓN DEL SISTEMA", padding=10)
        anim_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.fig_anim = Figure(figsize=(5, 3.5), facecolor='#2C3E50')  # Tamaño reducido
        self.ax_anim = self.fig_anim.add_subplot(111)
        self.setup_animation_plot()
        
        self.canvas_anim = FigureCanvasTkAgg(self.fig_anim, anim_frame)
        self.canvas_anim.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Gráfico de desplazamiento (derecha)
        graph_frame = ttk.LabelFrame(graph_container, text="📊 DESPLAZAMIENTO vs TIEMPO", padding=10)
        graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.fig_graph = Figure(figsize=(5, 3.5), facecolor='#2C3E50')  # Tamaño reducido
        self.ax_graph = self.fig_graph.add_subplot(111)
        self.setup_graph_plot()
        
        self.canvas_graph = FigureCanvasTkAgg(self.fig_graph, graph_frame)
        self.canvas_graph.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def setup_animation_plot(self):
        """Configurar gráfico de animación"""
        self.ax_anim.clear()
        self.ax_anim.set_xlim(-4, 6)
        self.ax_anim.set_ylim(-1.5, 1.5)
        self.ax_anim.set_aspect('equal')
        self.ax_anim.set_facecolor('#34495E')
        self.ax_anim.set_title('Sistema Masa-Resorte', color='white', fontweight='bold', fontsize=10)
        self.ax_anim.grid(True, alpha=0.3, color='gray')
        
        # Pared
        self.ax_anim.axvline(x=-3, color='#E74C3C', linewidth=8, alpha=0.8)
        
        # Resorte y masa
        self.spring_line, = self.ax_anim.plot([], [], '#3498DB', linewidth=3)
        self.mass = plt.Circle((0, 0), 0.2, fc='#E74C3C', ec='#F39C12', linewidth=2)
        self.ax_anim.add_patch(self.mass)
        
        # Texto de resonancia
        self.res_text = self.ax_anim.text(0, 1.3, '', fontsize=10, 
                                         ha='center', fontweight='bold', 
                                         color='#F39C12')
        
        # Configurar colores
        self.ax_anim.tick_params(colors='white', labelsize=8)
        for spine in self.ax_anim.spines.values():
            spine.set_color('white')
    
    def setup_graph_plot(self):
        """Configurar gráfico de desplazamiento"""
        self.ax_graph.clear()
        self.ax_graph.set_xlim(0, 20)
        self.ax_graph.set_ylim(-3, 3)
        self.ax_graph.set_facecolor('#34495E')
        self.ax_graph.set_title('Desplazamiento vs Tiempo', color='white', fontweight='bold', fontsize=10)
        self.ax_graph.set_xlabel('Tiempo (s)', color='white', fontsize=9)
        self.ax_graph.set_ylabel('Desplazamiento (m)', color='white', fontsize=9)
        self.ax_graph.grid(True, alpha=0.3, color='gray')
        self.ax_graph.tick_params(colors='white', labelsize=8)
        
        self.graph_line, = self.ax_graph.plot([], [], '#2ECC71', linewidth=2)
        self.time_line = self.ax_graph.axvline(x=0, color='#E74C3C', linestyle='--', alpha=0.7)
        
        for spine in self.ax_graph.spines.values():
            spine.set_color('white')
    
    def setup_controls(self, parent):
        """Configurar área de controles e información"""
        # Frame para controles (izquierda) e información (derecha)
        controls_container = ttk.Frame(parent)
        controls_container.pack(fill=tk.BOTH, expand=True)
        
        # Panel de controles
        self.setup_control_panel(controls_container)
        
        # Panel de información
        self.setup_info_panel(controls_container)
    
    def create_info_button(self, parent, tooltip_text):
        """Crear botón de información con tooltip"""
        def show_tooltip():
            messagebox.showinfo("Información", tooltip_text)
        
        info_btn = ttk.Button(parent, text="ℹ️", width=3, command=show_tooltip)
        return info_btn
    
    def setup_control_panel(self, parent):
        """Panel de controles interactivos"""
        control_frame = ttk.LabelFrame(parent, text="🎛️ CONTROLES DEL SISTEMA", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Sliders con estilo moderno
        sliders_frame = ttk.Frame(control_frame)
        sliders_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Masa
        mass_frame = ttk.Frame(sliders_frame)
        mass_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(mass_frame, text="Masa (kg):", foreground="white", background="#2C3E50").pack(side=tk.LEFT)
        self.create_info_button(mass_frame, 
            "⚖️ MASA: Controla la inercia del sistema\n\n"
            "• Masa PEQUEÑA (0.1-1 kg): Oscilaciones rápidas\n"
            "• Masa MEDIA (1-3 kg): Comportamiento balanceado\n" 
            "• Masa GRANDE (3-5 kg): Movimiento lento y pesado").pack(side=tk.LEFT, padx=5)
        
        self.mass_var = tk.DoubleVar(value=self.m)
        mass_scale = ttk.Scale(sliders_frame, from_=0.1, to=5.0, variable=self.mass_var, 
                              orient=tk.HORIZONTAL, command=self.on_parameter_change)
        mass_scale.pack(fill=tk.X, pady=2)
        
        # Rigidez
        stiffness_frame = ttk.Frame(sliders_frame)
        stiffness_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(stiffness_frame, text="Rigidez (N/m):", foreground="white", background="#2C3E50").pack(side=tk.LEFT)
        self.create_info_button(stiffness_frame, 
            "🧊 RIGIDEZ: Qué tan fuerte es el resorte\n\n"
            "• Resorte SUAVE (0.5-3 N/m): Oscilaciones lentas\n"
            "• Rigidez MEDIA (3-8 N/m): Comportamiento normal\n"
            "• Resorte RÍGIDO (8-15 N/m): Vibraciones rápidas").pack(side=tk.LEFT, padx=5)
        
        self.k_var = tk.DoubleVar(value=self.k)
        k_scale = ttk.Scale(sliders_frame, from_=0.5, to=15.0, variable=self.k_var, 
                           orient=tk.HORIZONTAL, command=self.on_parameter_change)
        k_scale.pack(fill=tk.X, pady=2)
        
        # Fuerza
        force_frame = ttk.Frame(sliders_frame)
        force_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(force_frame, text="Fuerza (N):", foreground="white", background="#2C3E50").pack(side=tk.LEFT)
        self.create_info_button(force_frame, 
            "🎯 FUERZA EXTERNA: Intensidad de la fuerza aplicada\n\n"
            "• Sin fuerza (0 N): Movimiento libre\n"
            "• Fuerza PEQUEÑA (0.1-3 N): Vibración suave\n"
            "• Fuerza GRANDE (3-10 N): Oscilaciones intensas").pack(side=tk.LEFT, padx=5)
        
        self.F0_var = tk.DoubleVar(value=self.F0)
        force_scale = ttk.Scale(sliders_frame, from_=0.0, to=10.0, variable=self.F0_var, 
                               orient=tk.HORIZONTAL, command=self.on_parameter_change)
        force_scale.pack(fill=tk.X, pady=2)
        
        # Frecuencia
        freq_frame = ttk.Frame(sliders_frame)
        freq_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(freq_frame, text="Frecuencia (rad/s):", foreground="white", background="#2C3E50").pack(side=tk.LEFT)
        self.create_info_button(freq_frame, 
            "📡 FRECUENCIA: Velocidad de la fuerza oscilante\n\n"
            "• Frecuencia BAJA (0.1-1 rad/s): Oscilaciones suaves\n"
            "• Frecuencia MEDIA (1-3 rad/s): Comportamiento normal\n"
            "• Frecuencia ALTA (3-8 rad/s): Vibraciones rápidas\n\n"
            "⚡ RESONANCIA: Ocurre cuando coincide con la frecuencia natural").pack(side=tk.LEFT, padx=5)
        
        self.omega_var = tk.DoubleVar(value=self.omega)
        freq_scale = ttk.Scale(sliders_frame, from_=0.1, to=8.0, variable=self.omega_var, 
                              orient=tk.HORIZONTAL, command=self.on_parameter_change)
        freq_scale.pack(fill=tk.X, pady=2)
        
        # Selectores en fila
        selector_frame = ttk.Frame(control_frame)
        selector_frame.pack(fill=tk.X, pady=10)
        
        # Tipo de fuerza
        force_type_frame = ttk.LabelFrame(selector_frame, text="Tipo de Fuerza", padding=5)
        force_type_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.force_var = tk.StringVar(value="Coseno")
        forces = ["Coseno", "Seno", "Pulso", "Escalón"]
        for force in forces:
            ttk.Radiobutton(force_type_frame, text=force, variable=self.force_var, 
                           value=force, command=self.on_force_type_change).pack(anchor=tk.W)
        
        # Experimentos predefinidos
        preset_frame = ttk.LabelFrame(selector_frame, text="Experimentos", padding=5)
        preset_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.preset_var = tk.StringVar(value="Normal")
        presets = ["Normal", "Resonancia", "Amortiguado", "Libre"]
        for preset in presets:
            ttk.Radiobutton(preset_frame, text=preset, variable=self.preset_var, 
                           value=preset, command=self.on_preset_change).pack(anchor=tk.W)
        
        # Botones de acción
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="🔄 Reiniciar", command=self.on_reset).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="💡 Consejo Aleatorio", command=self.show_random_tip).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📚 Ayuda", command=self.show_help).pack(side=tk.LEFT, padx=5)
    
    def setup_info_panel(self, parent):
        """Panel de información y logros"""
        info_frame = ttk.LabelFrame(parent, text="🎓 ZONA DE APRENDIZAJE", padding=10)
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Información del sistema
        system_frame = ttk.LabelFrame(info_frame, text="📊 ESTADO DEL SISTEMA", padding=8)
        system_frame.pack(fill=tk.X, pady=5)
        
        self.system_text = tk.Text(system_frame, height=4, width=35, bg='#34495E', fg='white',
                                  font=('Arial', 9), wrap=tk.WORD, relief='flat')
        self.system_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.system_text.insert(tk.END, "Frecuencia Natural: 2.00 rad/s\nRazón: 1.00\nEstado: Normal")
        self.system_text.config(state=tk.DISABLED)
        
        # Logros
        achievements_frame = ttk.LabelFrame(info_frame, text="🏆 LOGROS", padding=8)
        achievements_frame.pack(fill=tk.X, pady=5)
        
        self.achievements_text = tk.Text(achievements_frame, height=3, width=35, bg='#34495E', fg='#2ECC71',
                                        font=('Arial', 9), wrap=tk.WORD, relief='flat')
        self.achievements_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.achievements_text.insert(tk.END, "• Ninguno aún")
        self.achievements_text.config(state=tk.DISABLED)
        
        # Consejos
        tips_frame = ttk.LabelFrame(info_frame, text="💡 CONSEJOS", padding=8)
        tips_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.tips_text = tk.Text(tips_frame, height=4, width=35, bg='#34495E', fg='#3498DB',
                                font=('Arial', 9), wrap=tk.WORD, relief='flat')
        self.tips_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tips_text.insert(tk.END, "Prueba el experimento 'Resonancia' para ver el efecto más dramático")
        self.tips_text.config(state=tk.DISABLED)

    # ... (el resto de los métodos se mantiene igual que antes)
    def external_force(self, t):
        force_type_map = {
            'Coseno': 'cos',
            'Seno': 'sin', 
            'Pulso': 'pulse',
            'Escalón': 'step'
        }
        actual_type = force_type_map.get(self.force_var.get(), 'cos')
        
        if actual_type == 'cos':
            return self.F0 * np.cos(self.omega * t)
        elif actual_type == 'sin':
            return self.F0 * np.sin(self.omega * t)
        elif actual_type == 'pulse':
            return self.F0 * (0.5 + 0.5 * np.sign(np.sin(self.omega * t)))
        elif actual_type == 'step':
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
        sol = solve_ivp(self.equation, [0, 20], [0, 0], t_eval=t_eval, method='RK45')
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
            self.fig_anim, self.update_animation, 
            frames=len(self.solution_t),
            interval=25, 
            blit=True, 
            repeat=True,
            cache_frame_data=False
        )
    
    def update_animation(self, frame):
        if frame >= len(self.solution_t):
            return self.spring_line, self.mass, self.graph_line, self.res_text, self.time_line
            
        t, y = self.solution_t, self.solution_y
        current_y = y[frame]
        current_t = t[frame]
        
        # Actualizar animación
        spring_x, spring_y = self.create_spring_coords(current_y)
        self.spring_line.set_data(spring_x, spring_y)
        self.mass.center = (-3 + current_y + 3, 0)
        
        # Actualizar gráfico
        self.graph_line.set_data(t[:frame+1], y[:frame+1])
        self.time_line.set_xdata([current_t, current_t])
        
        # Ajustar límites dinámicos
        if frame > 10:
            y_max = max(1, np.max(np.abs(y[:frame+1])) * 1.2)
            self.ax_graph.set_ylim(-y_max, y_max)
            self.ax_graph.set_xlim(0, max(20, current_t + 1))
        
        # Verificar resonancia
        natural_freq = np.sqrt(self.k / self.m)
        if abs(self.omega - natural_freq) < 0.2 and self.F0 > 0:
            self.res_text.set_text('⚡ ¡RESONANCIA!')
            self.mass.set_facecolor('#F39C12')
            self.spring_line.set_color('#E74C3C')
        else:
            self.res_text.set_text('')
            self.mass.set_facecolor('#E74C3C')
            self.spring_line.set_color('#3498DB')
        
        # Actualizar panel de información
        self.update_info_panel(natural_freq)
        
        return self.spring_line, self.mass, self.graph_line, self.res_text, self.time_line
    
    def update_info_panel(self, natural_freq):
        """Actualizar el panel de información"""
        # Estado del sistema
        system_info = f"Frecuencia Natural: {natural_freq:.2f} rad/s\n"
        system_info += f"Razón: {self.omega/natural_freq:.2f}\n"
        system_info += "Estado: ⚡ Resonancia" if abs(self.omega - natural_freq) < 0.2 else "Estado: ✅ Normal"
        
        self.system_text.config(state=tk.NORMAL)
        self.system_text.delete(1.0, tk.END)
        self.system_text.insert(tk.END, system_info)
        self.system_text.config(state=tk.DISABLED)
    
    def on_parameter_change(self, event=None):
        """Cuando cambia cualquier parámetro"""
        self.m = self.mass_var.get()
        self.k = self.k_var.get()
        self.F0 = self.F0_var.get()
        self.omega = self.omega_var.get()
        
        self.solution_t, self.solution_y = self.solve_system()
        self.canvas_anim.draw()
        self.canvas_graph.draw()
    
    def on_force_type_change(self):
        """Cuando cambia el tipo de fuerza"""
        self.tips_text.config(state=tk.NORMAL)
        self.tips_text.delete(1.0, tk.END)
        self.tips_text.insert(tk.END, f"Fuerza cambiada a: {self.force_var.get()}\nObserva el nuevo patrón")
        self.tips_text.config(state=tk.DISABLED)
        
        self.solution_t, self.solution_y = self.solve_system()
    
    def on_preset_change(self):
        """Cuando se selecciona un experimento predefinido"""
        presets = {
            'Normal': {'m': 1.0, 'k': 4.0, 'F0': 2.0, 'omega': 2.0, 'c': 0.1},
            'Resonancia': {'m': 1.0, 'k': 4.0, 'F0': 3.0, 'omega': 2.0, 'c': 0.05},
            'Amortiguado': {'m': 2.0, 'k': 4.0, 'F0': 1.0, 'omega': 1.0, 'c': 1.5},
            'Libre': {'m': 1.0, 'k': 4.0, 'F0': 0.0, 'omega': 2.0, 'c': 0.0}
        }
        
        preset = presets[self.preset_var.get()]
        self.mass_var.set(preset['m'])
        self.k_var.set(preset['k'])
        self.F0_var.set(preset['F0'])
        self.omega_var.set(preset['omega'])
        self.c = preset['c']
        
        self.tips_text.config(state=tk.NORMAL)
        self.tips_text.delete(1.0, tk.END)
        self.tips_text.insert(tk.END, f"Experimento: {self.preset_var.get()}\n¡Observa el comportamiento!")
        self.tips_text.config(state=tk.DISABLED)
        
        self.on_parameter_change()
    
    def on_reset(self):
        """Reiniciar el sistema"""
        self.achievements.clear()
        self.mass_var.set(1.0)
        self.k_var.set(4.0)
        self.F0_var.set(2.0)
        self.omega_var.set(2.0)
        self.force_var.set("Coseno")
        self.preset_var.set("Normal")
        self.c = 0.1
        
        self.achievements_text.config(state=tk.NORMAL)
        self.achievements_text.delete(1.0, tk.END)
        self.achievements_text.insert(tk.END, "• Ninguno aún")
        self.achievements_text.config(state=tk.DISABLED)
        
        self.on_parameter_change()
    
    def show_help(self):
        """Mostrar ayuda"""
        help_text = """
        🔍 CÓMO USAR EL LABORATORIO:
        
        1. Ajusta los sliders para cambiar parámetros
        2. Prueba los Experimentos predefinidos
        3. Observa cómo cambia la animación
        4. ¡Desbloquea logros aprendiendo!
        
        ⚡ RESONANCIA: Ocurre cuando la frecuencia externa 
        coincide con la frecuencia natural del sistema
        
        💡 Usa los botones ℹ️ para aprender sobre cada parámetro
        """
        messagebox.showinfo("Ayuda del Laboratorio", help_text)
    
    def show_random_tip(self):
        """Mostrar un consejo aleatorio"""
        tips = [
            "🔍 ¿Sabías? La resonancia puede hacer que puentes se colapsen",
            "🎯 Prueba diferentes combinaciones para descubrir patrones",
            "⚡ La frecuencia natural depende de la masa y la rigidez",
            "🔄 El amortiguamiento hace que las oscilaciones desaparezcan",
            "🎮 ¡Desbloquea todos los logros experimentando!",
            "📚 Haz clic en ℹ️ para aprender sobre cada parámetro"
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