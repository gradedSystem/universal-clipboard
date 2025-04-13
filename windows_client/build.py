import PyInstaller.__main__
import os
import sys

def build_executable():
    # Get the absolute path to the main script
    main_script = os.path.abspath(os.path.join(os.path.dirname(__file__), 'main.py'))
    
    # Define the PyInstaller arguments
    args = [
        main_script,
        '--name=UniversalClipboard',
        '--onefile',
        '--windowed',
        '--icon=NONE',
        '--add-data=../shared;shared',
        '--hidden-import=websockets',
        '--hidden-import=cryptography',
        '--hidden-import=PIL',
        '--hidden-import=win32clipboard',
        '--hidden-import=win32con',
        '--clean',
        '--noconfirm',
    ]
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)

if __name__ == '__main__':
    build_executable() 