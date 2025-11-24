"""
Configuraciones y constantes de la aplicación
"""

# Colores del tema
COLORS = {
    "primary": "#1A1A2E",
    "secondary": "#16213E",
    "accent1": "#00D4FF",
    "accent2": "#64FFDA",
    "accent3": "#FF2E63",
    "accent4": "#FFD166",
    "text": "#FFFFFF",
}

# Parámetros físicos por defecto
DEFAULT_PARAMETERS = {
    "mass": 1.0,
    "stiffness": 4.0,
    "damping": 0.1,
    "force_amplitude": 2.0,
    "frequency": 2.0,
    "force_type": "Coseno"
}

# Límites de los parámetros
PARAMETER_LIMITS = {
    "mass": {"min": 0.1, "max": 5.0, "step": 0.1},
    "stiffness": {"min": 0.5, "max": 15.0, "step": 0.5},
    "damping": {"min": 0.0, "max": 2.0, "step": 0.1},
    "force_amplitude": {"min": 0.0, "max": 10.0, "step": 0.5},
    "frequency": {"min": 0.1, "max": 8.0, "step": 0.1},
}

# Experimentos predefinidos
PRESETS = {
    "Normal": {
        "mass": 1.0,
        "stiffness": 4.0,
        "force_amplitude": 2.0,
        "frequency": 2.0,
        "damping": 0.1
    },
    "Resonancia": {
        "mass": 1.0,
        "stiffness": 4.0,
        "force_amplitude": 3.0,
        "frequency": 2.0,
        "damping": 0.05
    },
    "Amortiguado": {
        "mass": 2.0,
        "stiffness": 4.0,
        "force_amplitude": 1.0,
        "frequency": 1.0,
        "damping": 1.5
    },
    "Libre": {
        "mass": 1.0,
        "stiffness": 4.0,
        "force_amplitude": 0.0,
        "frequency": 2.0,
        "damping": 0.0
    }
}

# Configuración de animación
ANIMATION_CONFIG = {
    "interval": 25,      # ms entre frames
    "frames": 800,       # número de frames
    "simulation_time": 17,  # segundos
    "blit": True
}

# Consejos del sistema
TIPS = [
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