#!/usr/bin/env python3
"""
Build script for Passion Of Rugs Advanced Dialer v4.1
Creates executable with PyInstaller
"""

import PyInstaller.__main__
import os
import sys

def build_executable():
    """Build the executable using PyInstaller"""
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # PyInstaller arguments
    args = [
        'launcher.py',  # Main script
        '--name=PassionOfRugs_Dialer_v4.1',  # Executable name
        '--onedir',  # Directory bundle (faster startup)
        '--windowed',  # No console window (GUI app)
        '--icon=NONE',  # No icon for now
        
        # Hidden imports (modules that PyInstaller might miss)
        '--hidden-import=pandas',
        '--hidden-import=numpy',
        '--hidden-import=openpyxl',
        '--hidden-import=requests',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.scrolledtext',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=tkinterweb',
        '--hidden-import=lead_processor_v2',
        '--hidden-import=cache_manager',
        '--hidden-import=ai_assistant',
        '--hidden-import=openai',
        '--hidden-import=dialer_gui',
        '--hidden-import=bulk_processor_gui',
        '--hidden-import=base64',
        '--hidden-import=threading',
        '--hidden-import=webbrowser',
        '--hidden-import=urllib',
        '--hidden-import=urllib.parse',
        '--hidden-import=json',
        '--hidden-import=datetime',
        '--hidden-import=time',
        '--hidden-import=re',
        '--hidden-import=os',
        '--hidden-import=sys',
        '--hidden-import=logging',
        '--hidden-import=pathlib',
        '--hidden-import=typing',
        
        # Exclude unnecessary modules to reduce size
        '--exclude-module=matplotlib',
        '--exclude-module=scipy',
        '--exclude-module=PIL',
        '--exclude-module=PyQt5',
        '--exclude-module=PyQt6',
        
        # Clean build
        '--clean',
        '--noconfirm',
        
        # Optimization
        '--optimize=2',
    ]
    
    print("=" * 70)
    print("Building Passion Of Rugs Advanced Dialer v4.1")
    print("=" * 70)
    print()
    print("This may take a few minutes...")
    print()
    
    try:
        PyInstaller.__main__.run(args)
        
        print()
        print("=" * 70)
        print("Build Complete!")
        print("=" * 70)
        print()
        
        exe_path = os.path.join(current_dir, 'dist', 'PassionOfRugs_Dialer_v4.1', 'PassionOfRugs_Dialer_v4.1.exe')
        
        print(f"Executable location: {exe_path}")
        print()
        print("NOTE: Distribute the entire 'PassionOfRugs_Dialer_v4.1' folder from 'dist'")
        print("The .exe file needs the supporting files in the same folder.")
        print()
        print("To run: Double-click PassionOfRugs_Dialer_v4.1.exe")
        print()
        
    except Exception as e:
        print(f"Error during build: {e}")
        sys.exit(1)

if __name__ == '__main__':
    build_executable()
