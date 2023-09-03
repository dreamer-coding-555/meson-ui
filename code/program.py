#!/usr/bin/env python3
#
# Trilobite AppHub:
# author: Michael Gene Brockus (Dreamer)
# Gmail: <mail: michaelbrockus@gmail.com>
#
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
import subprocess
import threading
import queue
import os


class MesonBuildGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Meson-UI")
        self.root.configure(bg="gray30")

        # Set the fixed window size (width x height)
        self.root.geometry("750x500")
        self.root.resizable(False, False)

        # Get the current working directory
        self.default_path = os.getcwd()

        # Initialize flag for showing/hiding init view
        self.show_init_view = False

        # Create a Canvas for the modern Meson Build-style logo
        self.canvas = tk.Canvas(
            root, width=120, height=80, bg="gray30", highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        # Draw a simplified representation of the modern Meson Build logo
        self.canvas.create_text(60, 20, text="Meson-UI",
                                fill="green", font=("Arial", 20, "bold"))

        # Project Path Entry
        self.path_label = tk.Label(
            root, text="Project Path:", bg="gray30", fg="gray80", font=("Arial", 10, "bold"))
        self.path_label.grid(row=0, column=0, padx=5, pady=5, sticky="sew")
        self.path_entry = tk.Entry(root, width=80)
        self.path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="sew")
        # Auto-fill with current working directory
        self.path_entry.insert(0, self.default_path)

        # Button Frame
        self.button_frame = tk.Frame(root, bg="gray40")
        self.button_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Browse Button for folder selection
        button_style = {'padx': 25, 'pady': 5, 'bg': 'gray40', 'fg': 'gray80'}
        self.browse_button = tk.Button(
            self.root, text="Browse", command=self.open_folder_dialog, **button_style)
        self.browse_button.grid(row=0, column=1, sticky="e")

        # Buttons (arranged using grid)
        self.setup_button = tk.Button(
            self.button_frame, text="Setup Project", command=self.setup_project, **button_style)
        self.setup_button.grid(row=0, column=0, sticky="we")

        # Buttons for compiling, initializing, running tests, and cleaning
        self.compile_button = tk.Button(
            self.button_frame, text="Compile Project", command=self.compile_project, **button_style)
        self.compile_button.grid(row=0, column=1, sticky="we")

        self.init_button = tk.Button(
            self.button_frame, text="Init Project", command=self.initialize_project, **button_style)
        self.init_button.grid(row=0, column=2, sticky="we")

        self.run_tests_button = tk.Button(
            self.button_frame, text="Run Tests", command=self.run_tests, **button_style)
        self.run_tests_button.grid(row=0, column=3, sticky="we")

        self.clean_button = tk.Button(
            self.button_frame, text="Clean Project", command=self.clean_project, **button_style)
        self.clean_button.grid(row=0, column=4, sticky="we")

        # Inside the __init__ method of MesonBuildGUI
        self.introspect_button = tk.Button(
            self.button_frame, text="Introspect", command=self.introspect_project, **button_style)
        self.introspect_button.grid(row=0, column=5, sticky="we")

        # Output Console
        self.console = tk.Text(root, wrap="none", bg="black", fg="white")
        self.console.grid(row=2, column=0, columnspan=2,
                          padx=5, pady=5, sticky="nsew")
        self.console.tag_configure("stdout", foreground="green")
        self.console.tag_configure("stderr", foreground="red")

        # Command Queue
        self.command_queue = queue.Queue()

        # Add a progress bar
        self.progress_bar = ttk.Progressbar(root, mode='indeterminate')
        self.progress_bar.grid(row=2, column=0, columnspan=2,
                               padx=5, pady=5, sticky="nsew")
        self.progress_bar.grid_remove()  # Initially, hide the progress bar

    def update_console(self, text, tag=None):
        self.console.insert(tk.END, text, tag)
        self.console.see(tk.END)

    def run_command(self, command):
        try:
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
            for line in process.stdout:
                self.command_queue.put(("stdout", line))
            for line in process.stderr:
                self.command_queue.put(("stderr", line))
            process.wait()
        except Exception as e:
            self.command_queue.put(("stderr", f"Error: {e}\n"))

    def execute_command(self, command):
        self.command_queue.put(("stdout", f"Running command: {command}\n"))
        self.run_command(command)
        self.command_queue.put(("stdout", "Command finished.\n"))

    def open_folder_dialog(self):
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, selected_folder)

    def setup_project(self):
        project_path = self.path_entry.get()
        command = f"meson setup {project_path}/builddir"
        self.execute_command(command)

    def compile_project(self):
        project_path = self.path_entry.get()
        command = f"ninja -C {project_path}/builddir"
        self.execute_command(command)

    # Update the progress bar
    def update_progress(self):
        while True:
            try:
                tag, line = self.command_queue.get(timeout=0.1)
                self.update_console(line, tag)
                self.root.update()
            except queue.Empty:
                if not threading.active_count() > 1:
                    break

    def start_progress_thread(self):
        progress_thread = threading.Thread(target=self.update_progress)
        progress_thread.daemon = True
        progress_thread.start()

    def initialize_project(self):
        project_path = self.path_entry.get()
        command = f"meson init {project_path}"
        self.execute_command(command)

    def run_tests(self):
        project_path = self.path_entry.get()
        command = f"meson test -C {project_path}/builddir"
        self.execute_command(command)

    def clean_project(self):
        project_path = self.path_entry.get()
        command = f"ninja -C {project_path}/builddir clean"
        self.execute_command(command)

    def introspect_project(self):
        project_path = self.path_entry.get()
        command = f"meson introspect {project_path}/builddir"
        self.execute_command(command)

    def update_progress(self):
        while True:
            try:
                tag, line = self.command_queue.get(timeout=0.1)
                self.update_console(line, tag)
                self.root.update()
            except queue.Empty:
                if not threading.active_count() > 1:
                    break

    def start_progress_thread(self):
        progress_thread = threading.Thread(target=self.update_progress)
        progress_thread.daemon = True
        progress_thread.start()

def greet():
    return "Hello, Python Developer"
# end of func
