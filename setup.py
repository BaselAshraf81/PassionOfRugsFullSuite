#!/usr/bin/env python3
"""
Setup script for Passion Of Rugs Dialer v4.1
Helps users configure the application for first use.
"""

import os
import shutil

def setup_config():
    """Copy template config and guide user through setup."""
    
    print("🔧 Setting up Passion Of Rugs Dialer v4.1...")
    print()
    
    # Check if config.py already exists
    if os.path.exists('config.py'):
        print("✅ config.py already exists")
        return
    
    # Copy template
    if os.path.exists('config.template.py'):
        shutil.copy('config.template.py', 'config.py')
        print("✅ Created config.py from template")
        print()
        print("📝 Next steps:")
        print("1. Edit config.py and add your TrestleIQ API key")
        print("2. (Optional) Add CloudTalk credentials for dialer mode")
        print("3. Run: python launcher.py")
        print()
    else:
        print("❌ config.template.py not found")
        return False
    
    return True

if __name__ == "__main__":
    setup_config()