# 🎯 Sistema Masa-Resorte Interactivo

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)](https://github.com/tu-usuario/mass-spring-simulator)

Un simulador educativo interactivo para visualizar y experimentar con sistemas masa-resorte, resonancia y amortiguamiento. Desarrollado para ferias científicas y educación en física.

![Demo del Simulador](docs/demo.gif)

## ✨ Características Principales

### 🎮 Interfaz Intuitiva
- **Controles en tiempo real** para todos los parámetros físicos
- **Animación fluida** del sistema masa-resorte
- **Gráficas dinámicas** de posición vs tiempo
- **Detección automática** de resonancia con cambios de color

### 🔬 Parámetros Ajustables
- **Masa (m)**: 0.1 - 5.0 kg
- **Rigidez (k)**: 0.5 - 15.0 N/m  
- **Amortiguamiento (c)**: 0.0 - 2.0 N·s/m
- **Fuerza Externa (F₀)**: 0 - 10 N
- **Frecuencia (ω)**: 0.1 - 8.0 rad/s

### 🌊 Tipos de Fuerza
- **Coseno**: `F(t) = F₀·cos(ω·t)`
- **Seno**: `F(t) = F₀·sin(ω·t)`
- **Pulso**: Fuerza que alterna entre 0 y F₀
- **Escalón**: Fuerza constante que se activa en t=2s

### 🧪 Experimentos Predefinidos
- **Normal**: Configuración balanceada de referencia
- **Resonancia**: Demostración dramática de resonancia
- **Amortiguado**: Sistema con alto amortiguamiento
- **Libre**: Oscilaciones naturales sin fuerzas externas

## 🚀 Instalación Rápida

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación en 3 Pasos

1. **Clonar el repositorio**:
```bash
git clone https://github.com/tu-usuario/mass-spring-simulator.git
cd mass-spring-simulator
```

2. **Instalar dependencias**:
```bash
pip install numpy scipy matplotlib
```

3. **Ejecutar el simulador**:
```bash
python mass_spring_simulator.py
```

### 📦 Instalación con Entorno Virtual (Recomendado)

```bash
# Crear entorno virtual
python -m venv mass_spring_env

# Activar entorno (Linux/Mac)
source mass_spring_env/bin/activate

# Activar entorno (Windows)
mass_spring_env\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python mass_spring_simulator.py
```

## 🎓 Guía de Uso Rápido

### Primera Ejecución
1. Al iniciar, verás una **pantalla de bienvenida** con explicaciones
2. Haz clic en **"INICIAR EXPERIMENTO"** para comenzar
3. Usa los **controles deslizantes** para ajustar parámetros
4. Observa la **animación en tiempo real** y la **gráfica inferior**

### Demostraciones Recomendadas

#### 🎯 Demostración de Resonancia (2 minutos)
1. Selecciona **"Resonancia"** en experimentos predefinidos
2. Haz clic en **"Aplicar Configuración"**
3. Observa cómo crece la amplitud dramáticamente
4. Explica: *"¡Resonancia! Una fuerza pequeña aplicada correctamente produce efectos enormes"*

#### 🛑 Control con Amortiguamiento (1 minuto)
1. Selecciona **"Amortiguado"** en experimentos predefinidos  
2. Aplica la configuración
3. Muestra cómo las oscilaciones desaparecen rápidamente
4. Explica: *"Así funcionan los amortiguadores de tu auto"*

#### 🔄 Sistema Libre (1 minuto)
1. Selecciona **"Libre"** en experimentos predefinidos
2. Aplica la configuración
3. Observa oscilaciones perfectamente regulares
4. Explica: *"Este es el comportamiento natural del sistema sin influencias externas"*

## 📚 Marco Teórico

### 🔍 La Ecuación Fundamental
El sistema sigue la ecuación diferencial:

```
m·y'' + c·y' + k·y = F(t)
```

Donde:
- `m·y''`: Término de inercia (masa × aceleración)
- `c·y'`: Término de amortiguamiento (fricción viscosa)  
- `k·y`: Término de restauración (fuerza del resorte)
- `F(t)`: Fuerza externa aplicada

### 📈 Frecuencia Natural y Resonancia
La frecuencia natural del sistema es:
```
ω_natural = √(k/m)
```

La **resonancia** ocurre cuando:
```
ω_externa ≈ ω_natural
```

### 🎯 Tipos de Amortiguamiento
- **Subamortiguado** (`c < 2√(m·k)`): Oscilaciones que decaen
- **Críticamente amortiguado** (`c = 2√(m·k)`): Retorno rápido sin oscilar
- **Sobreamortiguado** (`c > 2√(m·k)`): Retorno lento sin oscilar

## 🏗️ Arquitectura del Software

### 📁 Estructura del Proyecto
```
mass-spring-simulator/
├── mass_spring_simulator.py  # Código principal
├── requirements.txt          # Dependencias
├── README.md                # Este archivo
├── docs/                    # Documentación
│   ├── guia_completa.html   # Guía detallada
│   ├── demo.gif            # GIF demostrativo
│   └── images/             # Imágenes para documentación
└── examples/               # Ejemplos adicionales
    └── advanced_modes.py   # Modos de oscilación avanzados
```

### 🔧 Componentes Principales

#### Clase `WelcomeScreen`
- Pantalla de bienvenida interactiva
- Explicaciones de conceptos básicos
- Navegación a la simulación principal

#### Clase `MassSpringApp` 
- Interfaz gráfica completa con Tkinter
- Sistema de animación con Matplotlib
- Resolución numérica de ecuaciones diferenciales
- Gestión de parámetros y experimentos

#### Algoritmos Numéricos
- **Método RK45** para resolver ecuaciones diferenciales
- **Interpolación suave** para animaciones
- **Detección de resonancia** en tiempo real

## 🎨 Personalización y Extensión

### 🔧 Modificar Parámetros
Puedes ajustar los rangos de los parámetros editando las líneas:
```python
# En mass_spring_simulator.py, buscar:
self.mass_slider = Slider(..., valmin=0.1, valmax=5.0)
self.k_slider = Slider(..., valmin=0.5, valmax=15.0)
# etc...
```

### 🎯 Añadir Nuevos Experimentos
Agrega nuevos experimentos predefinidos en el diccionario:
```python
self.experiments = {
    "Normal": {"m": 1.0, "k": 4.0, "c": 0.1, "F0": 2.0, "omega": 2.0},
    "Tu Experimento": {"m": 2.0, "k": 8.0, "c": 0.5, "F0": 1.0, "omega": 1.0},
    # Añadir más aquí...
}
```

### 🌊 Crear Nuevos Tipos de Fuerza
Extiende la función `external_force`:
```python
def external_force(self, t):
    # ... código existente ...
    elif actual_type == "triangular":
        # Implementar fuerza triangular
        period = 2 * np.pi / self.omega
        phase = (t % period) / period
        return self.F0 * (2 * abs(phase - 0.5) - 0.5)
```

## 📊 Aplicaciones en el Mundo Real

### 🏗️ Ingeniería Civil
- **Taipei 101**: Amortiguador de 660 toneladas
- **Puentes**: Diseño anti-resonancia
- **Edificios altos**: Control de oscilaciones por viento

### 🚗 Ingeniería Automotriz  
- **Suspensiones**: Amortiguadores y resortes
- **Confort**: Control de vibraciones
- **Seguridad**: Estabilidad en curvas

### 🎵 Música y Acústica
- **Instrumentos musicales**: Cajas de resonancia
- **Estudios de grabación**: Aislamiento acústico
- **Altavoces**: Diseño de cajas acústicas

### ⚡ Electrónica
- **Circuitos RLC**: Análogos a sistemas masa-resorte
- **Filtros**: Selección de frecuencias
- **Comunicaciones**: Sintonización de antenas

## 🐛 Solución de Problemas

### ❌ Error: "ModuleNotFoundError: No module named 'numpy'"
**Solución**: Instalar las dependencias:
```bash
pip install numpy scipy matplotlib
```

### ❌ Error: La animación se ve entrecortada
**Solución**: 
- Reducir la frecuencia externa (ω < 4 rad/s)
- Cerrar otras aplicaciones que consuman recursos
- Usar una computadora con mejor rendimiento gráfico

### ❌ Error: Tkinter no está disponible
**Solución** (Linux):
```bash
sudo apt-get install python3-tk
```

**Solución** (Mac):
```bash
brew install python-tk
```

### ❌ El programa se cierra inesperadamente
**Solución**:
- Verificar que todos los parámetros estén dentro de los rangos válidos
- Reiniciar el programa
- Ejecutar desde terminal para ver mensajes de error


## 📞 Contacto y Soporte

- **🐙 GitHub**: [https://github.com/carlop10](https://github.com/carlop10)
- **📚 Documentación**: [Guía Completa](https://github.com/carlop10/sistema-masa-resorte-interactivo/blob/main/guia.pdf)
