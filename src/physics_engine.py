"""
Motor físico para el sistema masa-resorte
"""

import numpy as np
from scipy.integrate import solve_ivp

class PhysicsEngine:
    """Motor de física para resolver el sistema masa-resorte"""
    
    def __init__(self):
        self.parameters = {}
        
    def set_parameters(self, mass, stiffness, damping, force_amplitude, frequency, force_type="Coseno"):
        """Establecer parámetros del sistema"""
        self.parameters = {
            'mass': mass,
            'stiffness': stiffness,
            'damping': damping,
            'force_amplitude': force_amplitude,
            'frequency': frequency,
            'force_type': force_type
        }
    
    def external_force(self, t):
        """Calcular fuerza externa según el tipo"""
        force_type_map = {
            "Coseno": "cos",
            "Seno": "sin",
            "Pulso": "pulse",
            "Escalón": "step",
        }
        
        actual_type = force_type_map.get(self.parameters.get('force_type', 'Coseno'), "cos")
        F0 = self.parameters['force_amplitude']
        omega = self.parameters['frequency']

        if actual_type == "cos":
            return F0 * np.cos(omega * t)
        elif actual_type == "sin":
            return F0 * np.sin(omega * t)
        elif actual_type == "pulse":
            return F0 * (0.5 + 0.5 * np.sign(np.sin(omega * t)))
        elif actual_type == "step":
            return F0 * (t > 2.0)
        return 0.0

    def equation(self, t, Y):
        """Ecuación diferencial del sistema"""
        y, yp = Y
        m = self.parameters['mass']
        k = self.parameters['stiffness']
        c = self.parameters['damping']
        
        force = self.external_force(t)
        dydt = yp
        dypdt = (-k * y - c * yp + force) / m
        
        return [dydt, dypdt]

    def solve_system(self, t_max=17, num_points=800):  # Cambiar default a 20
        """Resolver el sistema de ecuaciones diferenciales"""
        t_eval = np.linspace(0, t_max, num_points)
        sol = solve_ivp(
            self.equation, 
            [0, t_max], 
            [0, 0], 
            t_eval=t_eval, 
            method="RK45"
        )
        return sol.t, sol.y[0]
    
    def calculate_natural_frequency(self):
        """Calcular frecuencia natural del sistema"""
        m = self.parameters['mass']
        k = self.parameters['stiffness']
        return np.sqrt(k / m) if m > 0 else 0
    
    def calculate_critical_damping(self):
        """Calcular amortiguamiento crítico"""
        m = self.parameters['mass']
        k = self.parameters['stiffness']
        return 2 * np.sqrt(m * k)
    
    def is_resonance(self, threshold=0.05):
        """Verificar si el sistema está en resonancia"""
        natural_freq = self.calculate_natural_frequency()
        external_freq = self.parameters['frequency']
        force_amplitude = self.parameters['force_amplitude']
        damping = self.parameters['damping']
        
        if natural_freq == 0 or force_amplitude == 0:
            return False
            
        ratio = external_freq / natural_freq
        return (1 - threshold <= ratio <= 1 + threshold) and damping < 0.5
    
    def get_system_info(self):
        """Obtener información completa del sistema"""
        natural_freq = self.calculate_natural_frequency()
        critical_damping = self.calculate_critical_damping()
        damping_ratio = self.parameters['damping'] / critical_damping if critical_damping > 0 else 0
        
        is_resonance = self.is_resonance()
        
        system_info = f"Frecuencia Natural: {natural_freq:.2f} rad/s\n"
        system_info += f"Frecuencia Externa: {self.parameters['frequency']:.2f} rad/s\n"
        system_info += f"Razón: {self.parameters['frequency']/natural_freq:.2f}\n"
        system_info += f"Amort. Crítico: {critical_damping:.2f}\n"
        system_info += f"Razón Amort.: {damping_ratio:.2f}\n"
        
        # Determinar estado
        if is_resonance:
            system_info += "Estado: ⚡ RESONANCIA"
        elif self.parameters['force_amplitude'] == 0:
            system_info += "Estado: 🌀 MOVIMIENTO LIBRE"
        elif self.parameters['damping'] > 1.0:
            system_info += "Estado: 🛑 AMORTIGUADO FUERTE"
        else:
            system_info += "Estado: ✅ NORMAL"
        
        # Indicadores de advertencia
        if damping_ratio > 0.8:
            system_info += "\n⚠️ Sistema muy amortiguado"
        elif self.parameters['force_amplitude'] > 8 and abs(self.parameters['frequency'] - natural_freq) < 0.5:
            system_info += "\n🚨 ¡Cuidado! Fuerza alta cerca de resonancia"
        
        return system_info