from cx_Freeze import setup, Executable
import sys
import os

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["asyncio", "websockets", "cryptography", "win32service", "win32event", "servicemanager"],
    "excludes": ["tkinter", "unittest"],
    "include_files": [
        ("../shared/", "shared/"),
        ("service.py", "service.py"),
        ("main.py", "main.py")
    ]
}

# GUI applications require a different base on Windows
base = None
if sys.platform == "win32":
    base = "Win32Service"

setup(
    name="Universal Clipboard",
    version="1.0",
    description="Universal Clipboard Service",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "service.py",
            base=base,
            target_name="UniversalClipboard.exe",
            icon="icon.ico"  # You'll need to add an icon file
        )
    ]
) 