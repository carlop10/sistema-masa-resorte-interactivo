"""
Pantalla de bienvenida del Laboratorio Virtual
"""

import tkinter as tk
from tkinter import ttk, messagebox

from .config import COLORS
from .mass_spring_app import MassSpringApp

class WelcomeScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Bienvenido al Laboratorio Virtual")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg=COLORS["primary"])

        # Configurar estilo moderno
        self.setup_styles()
        self.setup_welcome_screen()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Colores modernos
        style.configure("Modern.TFrame", background=COLORS["primary"])
        style.configure(
            "Title.TLabel",
            background=COLORS["primary"],
            foreground=COLORS["accent1"],
            font=("Arial", 28, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=COLORS["primary"],
            foreground=COLORS["accent2"],
            font=("Arial", 16),
        )
        style.configure(
            "Accent.TButton",
            background=COLORS["accent1"],
            foreground="black",
            font=("Arial", 12, "bold"),
        )
        style.configure(
            "Exit.TButton",
            background=COLORS["accent3"],
            foreground="white",
            font=("Arial", 12, "bold"),
        )

    def setup_welcome_screen(self):
        # Frame principal con gradiente
        main_frame = ttk.Frame(self.root, style="Modern.TFrame", padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Logo/Icono
        emoji_label = ttk.Label(
            main_frame, text="🔬", font=("Arial", 60), background=COLORS["primary"]
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
            info_frame, bg=COLORS["secondary"], relief="raised", bd=2, padx=20, pady=2
        )
        concepts_card.pack(fill=tk.BOTH, expand=True, pady=2)

        concepts_title = tk.Label(
            concepts_card,
            text="🎓 CONCEPTOS BÁSICOS",
            bg=COLORS["secondary"],
            fg=COLORS["accent1"],
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
            bg=COLORS["secondary"],
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
            fg=COLORS["accent2"],
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
            text="🚀 INICIAR ",
            command=self.start_lab,
            style="Accent.TButton",
        ).pack(side=tk.LEFT, padx=15)
        
        ttk.Button(
            button_frame,
            text="ℹ️  INFO",
            command=lambda: messagebox.showinfo(
                "Información",
                "Laboratorio Virtual - Sistema Masa-Resorte\n\n\nExplora conceptos de física de manera interactiva.",
            ),
            style="Accent.TButton",
        ).pack(side=tk.LEFT, padx=15)

        ttk.Button(
            button_frame,
            text="🚪 SALIR",
            command=self.root.quit, 
            style="Exit.TButton"
        ).pack(side=tk.LEFT, padx=15)
        

    def start_lab(self):
        self.root.destroy()
        root = tk.Tk()
        app = MassSpringApp(root)
        root.mainloop()