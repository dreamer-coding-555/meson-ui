#!/usr/bin/env python3
#
# Trilobite AppHub:
# author: Michael Gene Brockus (Dreamer)
# Gmail: <mail: michaelbrockus@gmail.com>
#
import tkinter as tk
import subprocess
import threading
import queue

class MesonBuildGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Meson Build GUI")

        # Project Path Entry
        self.path_label = tk.Label(root, text="Project Path:")
        self.path_label.pack()
        self.path_entry = tk.Entry(root, width=40)
        self.path_entry.pack()

        # Buttons
        self.setup_button = tk.Button(root, text="Setup", command=self.setup_project)
        self.setup_button.pack()
        self.compile_button = tk.Button(root, text="Compile", command=self.compile_project)
        self.compile_button.pack()
        self.test_button = tk.Button(root, text="Test", command=self.test_project)
        self.test_button.pack()
        self.init_button = tk.Button(root, text="Init Project", command=self.init_project)
        self.init_button.pack()

        # Progress Bar
        self.progress_bar = tk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack()

        # Output Console
        self.console = tk.Text(root, wrap="none")
        self.console.pack()

        # Command Queue
        self.command_queue = queue.Queue()

    def update_console(self, text):
        self.console.insert(tk.END, text)
        self.console.see(tk.END)

    def run_command(self, command):
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
            for line in process.stdout:
                self.command_queue.put(line)
            for line in process.stderr:
                self.command_queue.put(line)
            process.wait()
        except Exception as e:
            self.command_queue.put(f"Error: {e}\n")

    def execute_command(self, command):
        self.command_queue.put(f"Running command: {command}\n")
        self.run_command(command)
        self.command_queue.put("Command finished.\n")

    def setup_project(self):
        project_path = self.path_entry.get()
        command = f"meson setup {project_path}/build"
        self.execute_command(command)

    def compile_project(self):
        project_path = self.path_entry.get()
        command = f"ninja -C {project_path}/build"
        self.execute_command(command)

    def test_project(self):
        project_path = self.path_entry.get()
        command = f"ninja -C {project_path}/build test"
        self.execute_command(command)

    def init_project(self):
        project_path = self.path_entry.get()
        command = f"meson init {project_path}"
        self.execute_command(command)

    def update_progress(self):
        while True:
            try:
                line = self.command_queue.get(timeout=0.1)
                self.update_console(line)
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
