#!/usr/bin/env python3
#
# Trilobite AppHub:
# author: Michael Gene Brockus (Dreamer)
# Gmail: <mail: michaelbrockus@gmail.com>
#
from .program import MesonBuildGUI
import tkinter as tk

def main_prog():
    root = tk.Tk()
    app = MesonBuildGUI(root)
    app.start_progress_thread()
    root.mainloop()
