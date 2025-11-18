import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib.animation as animation
from scipy.integrate import solve_ivp
import time

class FixedMassSpringSimulator:
    def __init__(self):
        # Parámetros iniciales
        self.m = 1.0
        self.k = 4.0
        self.c = 0.1
        self.F0 = 2.0
        self.omega = 2.0
        self.force_type = 'cos'
        
        # Configurar figura con layout fijo
        self.fig = plt.figure(figsize=(15, 8))
        self.setup_fixed_layout()
        self.setup_plots()
        
    def setup_fixed_layout(self):
        """Layout fijo sin superposiciones"""
        # Definir áreas exactas
        self.ax_anim = plt.axes([0.05, 0.5, 0.4, 0.4])      # Animación
        self.ax_graph = plt.axes([0.55, 0.5, 0.4, 0.4])     # Gráfico tiempo
        self.ax_controls = plt.axes([0.1, 0.1, 0.8, 0.3])   # Controles
        self.ax_controls.set_axis_off()
        
    def setup_plots(self):
        """Configurar las gráficas iniciales"""
        # Animación del resorte
        self.ax_anim.clear()
        self.ax_anim.set_xlim(-4, 6)
        self.ax_anim.set_ylim(-1.5, 1.5)
        self.ax_anim.set_aspect('equal')
        self.ax_anim.set_title('ANIMACIÓN MASA-RESORTE', fontweight='bold')
        self.ax_anim.grid(True, alpha=0.3)
        
        # Pared
        self.ax_anim.axvline(x=-3, color='brown', linewidth=8)
        
        # Resorte y masa (inicialmente vacíos)
        self.spring_line, = self.ax_anim.plot([], [], 'blue', linewidth=3)
        self.mass = plt.Circle((0, 0), 0.2, fc='red', ec='black')
        self.ax_anim.add_patch(self.mass)
        
        # Texto de resonancia
        self.res_text = self.ax_anim.text(0, 1.2, '', fontsize=12, 
                                         ha='center', fontweight='bold', color='red')
        
        # Gráfico de desplazamiento
        self.ax_graph.clear()
        self.ax_graph.set_xlim(0, 20)
        self.ax_graph.set_ylim(-3, 3)
        self.ax_graph.set_title('DESPLAZAMIENTO vs TIEMPO', fontweight='bold')
        self.ax_graph.set_xlabel('Tiempo (s)')
        self.ax_graph.set_ylabel('Desplazamiento (m)')
        self.ax_graph.grid(True, alpha=0.3)
        
        self.graph_line, = self.ax_graph.plot([], [], 'green', linewidth=2)
        
        # Línea de tiempo actual
        self.time_line = self.ax_graph.axvline(x=0, color='red', linestyle='--', alpha=0.7)
        
    def external_force(self, t):
        if self.force_type == 'cos':
            return self.F0 * np.cos(self.omega * t)
        elif self.force_type == 'sin':
            return self.F0 * np.sin(self.omega * t)
        elif self.force_type == 'pulse':
            return self.F0 * (0.5 + 0.5 * np.sign(np.sin(self.omega * t)))
        elif self.force_type == 'step':
            return self.F0 * (t > 2.0)
        return 0.0
    
    def equation(self, t, Y):
        y, yp = Y
        force = self.external_force(t)
        dydt = yp
        dypdt = (-self.k * y - self.c * yp + force) / self.m
        return [dydt, dypdt]
    
    def solve_system(self):
        t_eval = np.linspace(0, 20, 1000)
        sol = solve_ivp(self.equation, [0, 20], [0, 0], t_eval=t_eval, method='RK45')
        return sol.t, sol.y[0]
    
    def create_spring_coords(self, y_pos):
        """Crear coordenadas realistas del resorte"""
        # La posición y_pos es el desplazamiento desde el equilibrio
        spring_end_x = -3 + y_pos + 3  # Desde pared en x=-3 hasta masa
        x_vals = np.linspace(-3, spring_end_x, 100)
        
        # Resorte con forma de onda
        n_coils = 12
        y_vals = 0.2 * np.sin(n_coils * np.pi * np.linspace(0, 1, 100))
        
        return x_vals, y_vals
    
    def update_animation(self, frame):
        """Actualizar frame de animación"""
        if frame >= len(self.solution_t):
            return self.spring_line, self.mass, self.graph_line, self.res_text, self.time_line
            
        t, y = self.solution_t, self.solution_y
        current_y = y[frame]
        current_t = t[frame]
        
        # ACTUALIZAR ANIMACIÓN
        spring_x, spring_y = self.create_spring_coords(current_y)
        self.spring_line.set_data(spring_x, spring_y)
        
        # Mover masa
        mass_x = -3 + current_y + 3  # Posición correcta de la masa
        self.mass.center = (mass_x, 0)
        
        # ACTUALIZAR GRÁFICO con la línea que se dibuja progresivamente
        self.graph_line.set_data(t[:frame+1], y[:frame+1])
        self.time_line.set_xdata([current_t, current_t])
        
        # Ajustar límites dinámicamente
        if frame > 10:
            y_max = max(1, np.max(np.abs(y[:frame+1])) * 1.2)
            self.ax_graph.set_ylim(-y_max, y_max)
            
            x_max = max(20, current_t + 1)
            self.ax_graph.set_xlim(0, x_max)
        
        # Detectar resonancia
        natural_freq = np.sqrt(self.k / self.m)
        if abs(self.omega - natural_freq) < 0.2 and self.F0 > 0:
            self.res_text.set_text('⚡ RESONANCIA!')
            self.mass.set_facecolor('orange')
            self.spring_line.set_color('red')
        else:
            self.res_text.set_text('')
            self.mass.set_facecolor('red')
            self.spring_line.set_color('blue')
        
        return self.spring_line, self.mass, self.graph_line, self.res_text, self.time_line
    
    def create_organized_controls(self):
        """Crear controles bien organizados sin superposiciones"""
        
        # Sliders en columna ordenada
        slider_width = 0.25
        slider_height = 0.03
        start_x = 0.1
        start_y = 0.25
        
        # Slider de Masa
        ax_mass = plt.axes([start_x, start_y, slider_width, slider_height])
        self.slider_mass = Slider(ax_mass, 'Masa (kg)', 0.1, 5.0, valinit=self.m)
        
        # Slider de Rigidez
        ax_k = plt.axes([start_x, start_y - 0.05, slider_width, slider_height])
        self.slider_k = Slider(ax_k, 'Rigidez (N/m)', 0.5, 15.0, valinit=self.k)
        
        # Slider de Fuerza
        ax_force = plt.axes([start_x, start_y - 0.10, slider_width, slider_height])
        self.slider_force = Slider(ax_force, 'Fuerza (N)', 0.0, 10.0, valinit=self.F0)
        
        # Slider de Frecuencia
        ax_freq = plt.axes([start_x, start_y - 0.15, slider_width, slider_height])
        self.slider_freq = Slider(ax_freq, 'Frecuencia (rad/s)', 0.1, 8.0, valinit=self.omega)
        
        # Selector de tipo de fuerza (a la derecha de los sliders)
        ax_force_type = plt.axes([0.5, 0.25, 0.15, 0.1])
        self.force_radio = RadioButtons(ax_force_type, ['Coseno', 'Seno', 'Pulso', 'Escalón'])
        ax_force_type.set_title("Tipo de Fuerza", fontsize=10)
        
        # Botones de presets (debajo del selector de fuerza)
        ax_presets = plt.axes([0.5, 0.1, 0.15, 0.1])
        self.preset_radio = RadioButtons(ax_presets, ['Normal', 'Resonancia', 'Amortiguado', 'Libre'])
        ax_presets.set_title("Configuraciones", fontsize=10)
        
        # Conectar eventos
        self.slider_mass.on_changed(self.update_simulation)
        self.slider_k.on_changed(self.update_simulation)
        self.slider_force.on_changed(self.update_simulation)
        self.slider_freq.on_changed(self.update_simulation)
        self.force_radio.on_clicked(self.change_force_type)
        self.preset_radio.on_clicked(self.apply_preset)
    
    def change_force_type(self, label):
        force_map = {'Coseno': 'cos', 'Seno': 'sin', 'Pulso': 'pulse', 'Escalón': 'step'}
        self.force_type = force_map[label]
        self.update_simulation(None)
    
    def apply_preset(self, label):
        presets = {
            'Normal': {'m': 1.0, 'k': 4.0, 'F0': 2.0, 'omega': 2.0, 'c': 0.1},
            'Resonancia': {'m': 1.0, 'k': 4.0, 'F0': 3.0, 'omega': 2.0, 'c': 0.05},
            'Amortiguado': {'m': 2.0, 'k': 4.0, 'F0': 1.0, 'omega': 1.0, 'c': 1.5},
            'Libre': {'m': 1.0, 'k': 4.0, 'F0': 0.0, 'omega': 2.0, 'c': 0.0}
        }
        
        preset = presets[label]
        self.m = preset['m']
        self.k = preset['k']
        self.F0 = preset['F0']
        self.omega = preset['omega']
        self.c = preset['c']
        
        # Actualizar sliders
        self.slider_mass.set_val(self.m)
        self.slider_k.set_val(self.k)
        self.slider_force.set_val(self.F0)
        self.slider_freq.set_val(self.omega)
        
        self.update_simulation(None)
    
    def update_simulation(self, val):
        """Actualizar simulación cuando cambian parámetros"""
        self.m = self.slider_mass.val
        self.k = self.slider_k.val
        self.F0 = self.slider_force.val
        self.omega = self.slider_freq.val
        
        # Recalcular solución
        self.solution_t, self.solution_y = self.solve_system()
        
        # Resetear gráficos
        self.setup_plots()

# INICIALIZAR Y EJECUTAR
print("Iniciando simulador mejorado...")
sim = FixedMassSpringSimulator()
sim.create_organized_controls()

# Calcular solución inicial
start_time = time.time()
sim.solution_t, sim.solution_y = sim.solve_system()
print(f"Solución calculada en {time.time() - start_time:.2f} segundos")

# Crear animación
ani = animation.FuncAnimation(
    sim.fig, sim.update_animation, 
    frames=len(sim.solution_t),
    interval=20, 
    blit=True, 
    repeat=True,
    cache_frame_data=False
)

plt.tight_layout()
plt.show()