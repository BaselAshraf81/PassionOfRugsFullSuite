#!/usr/bin/env python3
"""
Passion Of Rugs Advanced Dialer v4.1 - Launcher
Choose between Bulk Processing Mode or Professional Dialer Mode
"""

import tkinter as tk
from tkinter import messagebox
import sys


class LauncherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Passion Of Rugs Advanced Dialer v4.1")
        self.root.geometry("600x600")
        self.root.resizable(True, True)
        
        # Colors
        self.colors = {
            'bg': '#F5F7FA',
            'primary': '#2C3E50',
            'secondary': '#3498DB',
            'success': '#27AE60',
            'white': '#FFFFFF'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Center window
        self.center_window()
        
        # Create UI
        self.create_ui()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_ui(self):
        """Create the launcher UI"""
        # Main container
        main = tk.Frame(self.root, bg=self.colors['bg'])
        main.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Title
        title = tk.Label(
            main,
            text="Passion Of Rugs Advanced Dialer v4.1",
            font=('Arial', 24, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        )
        title.pack(pady=(0, 10))
        
        # Subtitle
        subtitle = tk.Label(
            main,
            text="Professional Lead Processing System",
            font=('Arial', 12),
            bg=self.colors['bg'],
            fg=self.colors['secondary']
        )
        subtitle.pack(pady=(0, 40))
        
        # Mode selection label
        mode_label = tk.Label(
            main,
            text="Select Processing Mode:",
            font=('Arial', 14, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        )
        mode_label.pack(pady=(0, 20))
        
        # Mode 1 button
        mode1_frame = tk.Frame(main, bg=self.colors['white'], relief=tk.RAISED, bd=2)
        mode1_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            mode1_frame,
            text="MODE 1: Bulk Processing",
            font=('Arial', 14, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary']
        ).pack(pady=(15, 5))
        
        tk.Label(
            mode1_frame,
            text="Process Excel datasets with progress tracking\nIdeal for batch processing large datasets",
            font=('Arial', 10),
            bg=self.colors['white'],
            fg='gray',
            justify=tk.CENTER
        ).pack(pady=(0, 10))
        
        tk.Button(
            mode1_frame,
            text="Start Bulk Processing",
            command=self.start_mode1,
            font=('Arial', 12, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            padx=30,
            pady=10,
            cursor='hand2'
        ).pack(pady=(0, 15))
        
        # Mode 2 button
        mode2_frame = tk.Frame(main, bg=self.colors['white'], relief=tk.RAISED, bd=2)
        mode2_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            mode2_frame,
            text="Professional Dialer Mode",
            font=('Arial', 14, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary']
        ).pack(pady=(15, 5))
        
        tk.Label(
            mode2_frame,
            text="CloudTalk-integrated call center interface\nIdeal for active calling and lead review",
            font=('Arial', 10),
            bg=self.colors['white'],
            fg='gray',
            justify=tk.CENTER
        ).pack(pady=(0, 10))
        
        tk.Button(
            mode2_frame,
            text="Start Dialer",
            command=self.start_mode2,
            font=('Arial', 12, 'bold'),
            bg=self.colors['success'],
            fg='white',
            padx=30,
            pady=10,
            cursor='hand2'
        ).pack(pady=(0, 15))
        
        # Version info
        version = tk.Label(
            main,
            text="Version 3.0 | Excel Caching Enabled",
            font=('Arial', 9),
            bg=self.colors['bg'],
            fg='gray'
        )
        version.pack(side=tk.BOTTOM, pady=(20, 0))
    
    def start_mode1(self):
        """Start Bulk Processing Mode"""
        self.root.destroy()
        from bulk_processor_gui import main
        main()
    
    def start_mode2(self):
        """Start Professional Dialer Mode"""
        self.root.destroy()
        from dialer_gui import main
        main()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = LauncherGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
