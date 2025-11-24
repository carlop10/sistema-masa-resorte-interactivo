"""
Gestor de animaciones y visualizaciones
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class AnimationManager:
    """Gestiona las animaciones y gráficas del sistema"""
    
    def __init__(self, fig_anim, ax_anim, fig_graph, ax_graph):
        self.fig_anim = fig_anim
        self.ax_anim = ax_anim
        self.fig_graph = fig_graph
        self.ax_graph = ax_graph
        
        # Elementos de la animación
        self.spring_line = None
        self.mass = None
        self.graph_line = None
        self.time_line = None
        self.res_text = None
        
        self.ani = None
        self.setup_animation_elements()
    
    def setup_animation_elements(self):
        """Configurar elementos visuales de la animación"""
        # Configurar gráfico de animación
        self.ax_anim.clear()
        self.ax_anim.set_xlim(-7, 7)
        self.ax_anim.set_ylim(-2, 2)
        self.ax_anim.set_aspect("equal")
        self.ax_anim.set_facecolor("#0F3460")
        self.ax_anim.set_title("Sistema Masa-Resorte", color="#00D4FF", 
                              fontweight="bold", fontsize=10)
        self.ax_anim.grid(True, alpha=0.3, color="#00D4FF")
        
        # Pared
        self.wall_x = -6
        self.ax_anim.axvline(x=self.wall_x, color="#FF2E63", linewidth=8, alpha=0.8)
        
        # Resorte y masa
        self.spring_line, = self.ax_anim.plot([], [], "#00D4FF", linewidth=4, alpha=0.9)
        self.equilibrium_x = 0
        self.mass = plt.Circle((self.equilibrium_x, 0), 0.2, fc="#FF2E63", 
                              ec="#FF2E63", linewidth=2)
        self.ax_anim.add_patch(self.mass)
        
        # Línea de equilibrio
        self.ax_anim.axvline(x=self.equilibrium_x, color="#64FFDA", 
                            linestyle="--", alpha=0.5, linewidth=1)
        
        # Texto de resonancia
        self.res_text = self.ax_anim.text(0, 1.3, "", fontsize=10, ha="center", 
                                         fontweight="bold", color="#FFD166")
        
        # Configurar colores
        self.ax_anim.tick_params(colors="white", labelsize=8)
        for spine in self.ax_anim.spines.values():
            spine.set_color("#00D4FF")
        
        # Configurar gráfico de desplazamiento
        self.setup_graph_plot()
    
    def setup_graph_plot(self):
        """Configurar gráfico de desplazamiento vs tiempo"""
        self.ax_graph.clear()
        self.ax_graph.set_xlim(0, 20)
        self.ax_graph.set_ylim(-3, 3)
        self.ax_graph.set_facecolor("#0F3460")
        
        self.ax_graph.set_xlabel("Tiempo (s)", color="white", fontsize=9)
        self.ax_graph.set_ylabel("Desplazamiento (m)", color="white", fontsize=9)
        self.ax_graph.grid(True, alpha=0.3, color="#64FFDA")
        self.ax_graph.tick_params(colors="white", labelsize=8)

        self.graph_line, = self.ax_graph.plot([], [], "#64FFDA", linewidth=2)
        self.time_line = self.ax_graph.axvline(x=0, color="#FF2E63", 
                                              linestyle="--", alpha=0.7)

        for spine in self.ax_graph.spines.values():
            spine.set_color("#64FFDA")
    
    def create_spring_coords(self, y_pos):
        """Crear coordenadas del resorte con ondulación realista"""
        wall_x = self.wall_x
        natural_length = abs(self.equilibrium_x - wall_x)
        mass_x = self.equilibrium_x + y_pos
        
        # Límites físicos
        min_compression = wall_x + 0.5
        max_stretch = wall_x + natural_length * 3
        
        # Aplicar límites suaves
        if mass_x < min_compression:
            mass_x = min_compression + (y_pos + (min_compression - self.equilibrium_x)) * 0.1
        elif mass_x > max_stretch:
            mass_x = max_stretch - (y_pos - (max_stretch - self.equilibrium_x)) * 0.1
        
        # Crear resorte
        spring_length = mass_x - wall_x
        num_points = 150
        x_vals = np.linspace(wall_x, mass_x, num_points)
        
        # Ondulación del resorte
        base_coils = 12
        stretch_factor = spring_length / natural_length
        n_coils = max(5, min(20, int(base_coils * stretch_factor)))
        
        t = np.linspace(0, 1, num_points)
        main_wave = 0.15 * np.sin(n_coils * 2 * np.pi * t)
        secondary_wave = 0.03 * np.sin(n_coils * 4 * np.pi * t + np.pi/4)
        tertiary_wave = 0.02 * np.sin(n_coils * 6 * np.pi * t + np.pi/2)
        
        y_vals = main_wave + secondary_wave + tertiary_wave
        
        # Suavizar extremos
        window = np.ones(num_points)
        window[:10] = np.linspace(0, 1, 10)
        window[-10:] = np.linspace(1, 0, 10)
        y_vals = y_vals * window
        
        return x_vals, y_vals
    
    def update_animation(self, frame, solution_t, solution_y, physics_engine):
        """Actualizar frame de la animación"""
        if frame >= len(solution_t):
            return self.spring_line, self.mass, self.graph_line, self.res_text, self.time_line

        current_y = solution_y[frame]
        current_t = solution_t[frame]

        # Actualizar resorte y masa
        spring_x, spring_y = self.create_spring_coords(current_y)
        self.spring_line.set_data(spring_x, spring_y)
        self.mass.center = (spring_x[-1], 0)

        # Actualizar gráfico
        self.graph_line.set_data(solution_t[:frame+1], solution_y[:frame+1])
        self.time_line.set_xdata([current_t, current_t])

        # Ajustar límites dinámicos
        if frame > 10:
            y_max = max(1, np.max(np.abs(solution_y[:frame+1]))) * 1.2
            self.ax_graph.set_ylim(-y_max, y_max)
            self.ax_graph.set_xlim(0, max(20, current_t + 1))

        # Actualizar resonancia
        if physics_engine.is_resonance():
            self.res_text.set_text("⚡ ¡RESONANCIA!")
            self.mass.set_facecolor("#FFD166")
            self.spring_line.set_color("#FFD166")
            # Efecto de parpadeo suave en resonancia
            if frame % 10 < 5:
                self.mass.set_alpha(0.9)
            else:
                self.mass.set_alpha(0.7)
        else:
            self.res_text.set_text("")
            self.mass.set_facecolor("#FF2E63")
            self.spring_line.set_color("#00D4FF")
            self.mass.set_alpha(1.0)

        return self.spring_line, self.mass, self.graph_line, self.res_text, self.time_line
    
    def start_animation(self, solution_t, solution_y, physics_engine, interval=25):
        """Iniciar la animación"""
        # Detener animación anterior si existe
        if self.ani:
            self.ani.event_source.stop()
        
        # Crear nueva animación
        self.ani = FuncAnimation(
            self.fig_anim,
            lambda frame: self.update_animation(frame, solution_t, solution_y, physics_engine),
            frames=len(solution_t),
            interval=interval,
            blit=True,
            repeat=True,
            cache_frame_data=False,
        )
        return self.ani
    
    def stop_animation(self):
        """Detener la animación"""
        if self.ani:
            self.ani.event_source.stop()