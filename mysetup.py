import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
"packages": ["os","matplotlib.backends.backend_tkagg", "tkinter", "tkinter.filedialog"]
}

#
executables = [
Executable("UI.py", base=base, targetName="tradeStrategy.exe", compress=True)
]

setup( name = "setup",
version = "0.1",
description = "trade strategy for new three board",
options = {"build_exe": build_exe_options},
executables = executables,
)