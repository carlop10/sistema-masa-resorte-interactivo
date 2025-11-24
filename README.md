# 🎯 Sistema Masa-Resorte Interactivo

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)](https://github.com/tu-usuario/mass-spring-simulator)

Un simulador educativo interactivo para explorar conceptos de física como resonancia, amortiguamiento y oscilaciones.

![Demo del Simulador](docs/demo.gif)

## ✨ Características Principales

### 🎮 Interfaz Intuitiva
- **Controles en tiempo real** para todos los parámetros físicos
- **Animación fluida** del sistema masa-resorte
- **Gráficas dinámicas** de posición vs tiempo
- **Detección automática** de resonancia con cambios de color
- **Sistema de consejos educativos**

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
git clone https://github.com/carlop10/sistema-masa-resorte-interactivo.git
cd sistema-masa-resorte-interactivo
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Ejecutar el simulador**:
```bash
python main.py
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
sistema-masa-resorte-interactivo/
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias
├── src/                   # Código fuente
│   ├── config.py          # Configuraciones
│   ├── physics_engine.py  # Motor físico
│   ├── animation_manager.py # Gestor de animaciones
│   ├── ui_components.py   # Componentes de UI
│   ├── welcome_screen.py  # Pantalla de bienvenida
│   └── mass_spring_app.py # Aplicación principal
└── README.md
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


## 🔍 Guía

- **📚 Mas sobre la app**: [Guía Completa](https://github.com/carlop10/sistema-masa-resorte-interactivo/blob/main/guia.html)

## 🤖 Créditos

- ** Esta aplicación se desarrolló mayormente con DeepSeek
