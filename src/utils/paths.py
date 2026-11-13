import os
import sys

def get_project_root() -> str:
    """
    Returns the root directory of the project.
    If the application is frozen (PyInstaller), it returns the directory of the executable.
    Otherwise, it returns the directory of the project root (3 levels up from this file).
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def get_assets_dir() -> str:
    """
    Returns the assets directory.
    If frozen, it expects 'assets' to be next to the executable.
    Otherwise, it points to 'src/assets'.
    """
    if getattr(sys, 'frozen', False):
        return os.path.join(get_project_root(), "assets")
    else:
        return os.path.join(get_project_root(), "src", "assets")

