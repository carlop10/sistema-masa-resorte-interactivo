#!/usr/bin/env python3
"""
Punto de entrada principal del Laboratorio Virtual Masa-Resorte
"""

import tkinter as tk
from src.welcome_screen import WelcomeScreen

def main():
    """Función principal de la aplicación"""
    try:
        root = tk.Tk()
        app = WelcomeScreen(root)
        root.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()