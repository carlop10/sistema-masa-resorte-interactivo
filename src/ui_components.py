"""
Componentes reutilizables de la interfaz de usuario
"""

import tkinter as tk
from tkinter import messagebox

class ControlPanel:
    """Panel de control con botones +/- para ajustar parámetros"""
    
    def __init__(self, parent, title, min_val, max_val, step, current_val, 
                 param_name, info_text, callback):
        self.parent = parent
        self.title = title
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.current_val = current_val
        self.param_name = param_name
        self.info_text = info_text
        self.callback = callback
        
        self.create_widgets()
    
    def create_widgets(self):
        """Crear los widgets del panel de control"""
        self.frame = tk.Frame(self.parent, bg='#16213E', relief='groove', bd=1, padx=8, pady=1)
        self.frame.pack(fill=tk.BOTH, expand=True, pady=1)
        
        # Título y valor actual
        title_frame = tk.Frame(self.frame, bg='#16213E')
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(title_frame, text=self.title, bg='#16213E', 
                              fg='#00D4FF', font=('Arial', 9, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # Botón de información
        info_btn = tk.Button(title_frame, text="i", bg="#2181FF", fg='white', 
                            font=('Arial', 7), width=2, height=1,
                            command=self.show_info)
        info_btn.pack(side=tk.RIGHT, padx=5)
        
        self.value_label = tk.Label(title_frame, text=f"{self.current_val:.1f}", 
                                  bg='#16213E', fg='#FFD166', font=('Arial', 10, 'bold'))
        self.value_label.pack(side=tk.RIGHT)
        
        # Botones de control
        btn_frame = tk.Frame(self.frame, bg='#16213E')
        btn_frame.pack(fill=tk.X, pady=2)
        
        minus_btn = tk.Button(btn_frame, text="➖", bg='#FF2E63', fg='white', 
                            font=('Arial', 6, 'bold'), width=4,
                            command=lambda: self.adjust_value(-self.step))
        minus_btn.pack(side=tk.LEFT, padx=2)
        
        plus_btn = tk.Button(btn_frame, text="➕", bg='#00D4FF', fg='black', 
                           font=('Arial', 6, 'bold'), width=4,
                           command=lambda: self.adjust_value(self.step))
        plus_btn.pack(side=tk.LEFT, padx=2)
    
    def adjust_value(self, delta):
        """Ajustar valor del parámetro"""
        new_val = self.current_val + delta
        new_val = max(self.min_val, min(self.max_val, new_val))
        self.current_val = new_val
        self.value_label.config(text=f"{new_val:.1f}")
        self.callback(self.param_name, new_val)
    
    def show_info(self):
        """Mostrar información del parámetro"""
        messagebox.showinfo(f"Info: {self.title}", self.info_text)
    
    def update_value(self, new_val):
        """Actualizar valor mostrado"""
        self.current_val = new_val
        self.value_label.config(text=f"{new_val:.1f}")

class InfoPanel:
    """Panel de información del sistema"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()
    
    def create_widgets(self):
        """Crear widgets del panel de información"""
        self.frame = tk.Frame(self.parent, bg="#16213E", relief="ridge", bd=2, padx=10, pady=4)
        self.frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        title = tk.Label(self.frame, text="🎓 TABLERO INFORMATIVO", bg="#16213E",
                        fg="#00D4FF", font=("Arial", 12, "bold"))
        title.pack(pady=5)
        
        # Estado del sistema
        self.create_system_info()
        
        # Consejos
        self.create_tips_section()
    
    def create_system_info(self):
        """Crear sección de información del sistema"""
        system_frame = tk.Frame(self.frame, bg="#0F3460", relief="groove", bd=1, padx=8, pady=2)
        system_frame.pack(fill=tk.X, pady=2)
        
        system_title = tk.Label(system_frame, text="📊 ESTADO DEL SISTEMA", bg="#0F3460",
                               fg="#64FFDA", font=("Arial", 10, "bold"))
        system_title.pack(anchor=tk.W)
        
        self.system_text = tk.Text(system_frame, height=4, width=30, bg="#0F3460", fg="white",
                                  font=("Arial", 9), wrap=tk.WORD, relief="flat")
        self.system_text.pack(fill=tk.BOTH, expand=True, pady=2)
        self.system_text.config(state=tk.DISABLED)
    
    def create_tips_section(self):
        """Crear sección de consejos"""
        tips_frame = tk.Frame(self.frame, bg="#0F3460", relief="groove", bd=1, padx=8, pady=2)
        tips_frame.pack(fill=tk.BOTH, expand=True, pady=2)
        
        tips_title = tk.Label(tips_frame, text="💡 CONSEJOS", bg="#0F3460",
                             fg="#FF2E63", font=("Arial", 10, "bold"))
        tips_title.pack(anchor=tk.W)
        
        self.tips_text = tk.Text(tips_frame, height=3, width=30, bg="#0F3460", fg="#64FFDA",
                                font=("Arial", 14), wrap=tk.WORD, relief="flat")
        self.tips_text.pack(fill=tk.BOTH, expand=True, pady=2)
        self.tips_text.config(state=tk.DISABLED)
    
    def update_system_info(self, info_text):
        """Actualizar información del sistema"""
        self.system_text.config(state=tk.NORMAL)
        self.system_text.delete(1.0, tk.END)
        self.system_text.insert(tk.END, info_text)
        self.system_text.config(state=tk.DISABLED)
    
    def update_tips(self, tip_text):
        """Actualizar consejos"""
        self.tips_text.config(state=tk.NORMAL)
        self.tips_text.delete(1.0, tk.END)
        self.tips_text.insert(tk.END, tip_text)
        self.tips_text.config(state=tk.DISABLED)