import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from tkinter import ttk
from ttkthemes import ThemedStyle
import subprocess
import time
import json
from tkinter import messagebox
import requests
import os
import shlex

LIBRARIES = {
    "Windows": {
        "PyInstaller": {
            "command": "pyinstaller",
            "options": "--onefile",
            "tooltip": "Freezes Python scripts into stand-alone executables",
        },
        "cx_Freeze": {
            "command": "cxfreeze",
            "options": "",
            "tooltip": "Creates executables from Python scripts",
        },
        "py2exe": {
            "command": "py2exe",
            "options": "",
            "tooltip": "Converts Python scripts into executable Windows programs",
        },
    },
    "Mac": {
        "cx_Freeze": {
            "command": "cxfreeze",
            "options": "",
            "tooltip": "Creates executables from Python scripts",
        },
        "py2app": {
            "command": "py2app",
            "options": "",
            "tooltip": "Converts Python scripts into macOS applications",
        },
    },
    "Linux": {
        "PyInstaller": {
            "command": "pyinstaller",
            "options": "--onefile",
            "tooltip": "Freezes Python scripts into stand-alone executables",
        },
        "PyInstaller2": {
            "command": "pyinstaller2",
            "options": "--onefile",
            "tooltip": "Freezes Python scripts into stand-alone executables (alternative)",
        },
        "cx_Freeze": {
            "command": "cxfreeze",
            "options": "",
            "tooltip": "Creates executables from Python scripts",
        },
    },
}

BUILD_OPTIONS = {
    "Windows": {
        "extension": "exe",
        "tooltip": "Builds a Windows executable",
    },
    "Mac": {
        "extension": "dmg",
        "tooltip": "Builds a macOS executable",
    },
    "Linux": {
        "extension": "sh",
        "tooltip": "Builds a Linux executable",
    },
}


class PythonToExecutableApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Python to Executable")
        self.window.geometry("800x500")

        self.style = ThemedStyle(self.window)
        self.style.set_theme("equilux")

        self.file_path = tk.StringVar()
        self.selected_platform = tk.StringVar()
        self.selected_library = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.output_filename = tk.StringVar()
        self.selected_file_label_text = tk.StringVar()

        self.create_main_frame()
        self.create_content_frame()
        self.create_home_section()
        self.create_build_section()
        self.create_settings_section()
        self.create_help_section()
        self.create_status_bar()
        self.load_settings()
        self.update_clock()

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.window)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def create_content_frame(self):
        self.content_frame = ttk.Notebook(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

    def clear_status(self):
        self.status_label.config(text="Ready")
        self.window.update()

    def create_home_section(self):
        home_frame = ttk.Frame(self.content_frame)
        self.content_frame.add(home_frame, text="Home")

        home_label = ttk.Label(
            home_frame,
            text="Welcome to Python to Executable!",
            font=("Helvetica", 20),
            padding=(0, 20),
        )
        home_label.pack()

        description_label = ttk.Label(
            home_frame,
            text="This tool allows you to convert your Python scripts into standalone executables.",
            font=("Helvetica", 12),
            wraplength=600,
            padding=(0, 10),
        )
        description_label.pack()

        # File selection
        file_frame = ttk.Frame(home_frame)
        file_frame.pack(pady=20)

        file_label = ttk.Label(file_frame, text="Python File:")
        file_label.grid(row=0, column=0, sticky=tk.W)

        file_entry = ttk.Entry(file_frame, textvariable=self.file_path, width=50)
        file_entry.grid(row=0, column=1, padx=10)

        file_button = ttk.Button(
            file_frame, text="Select File", command=self.select_file
        )
        file_button.grid(row=0, column=2, padx=10)

        # Output directory selection
        output_dir_frame = ttk.Frame(home_frame)
        output_dir_frame.pack(pady=20)

        output_dir_label = ttk.Label(output_dir_frame, text="Output Directory:")
        output_dir_label.grid(row=0, column=0, sticky=tk.W)

        output_dir_entry = ttk.Entry(
            output_dir_frame, textvariable=self.output_dir, width=50
        )
        output_dir_entry.grid(row=0, column=1, padx=10)

        output_dir_button = ttk.Button(
            output_dir_frame, text="Select Folder", command=self.select_output_dir
        )
        output_dir_button.grid(row=0, column=2, padx=10)

        # Output filename
        output_filename_frame = ttk.Frame(home_frame)
        output_filename_frame.pack(pady=20)

        output_filename_label = ttk.Label(
            output_filename_frame, text="Output Filename:"
        )
        output_filename_label.grid(row=0, column=0, sticky=tk.W)

        output_filename_entry = ttk.Entry(
            output_filename_frame, textvariable=self.output_filename, width=50
        )
        output_filename_entry.grid(row=0, column=1, padx=10)

        # Autopopulate output filename when file is loaded
        self.selected_file_label = ttk.Label(
            output_filename_frame, textvariable=self.selected_file_label_text
        )
        self.selected_file_label.grid(row=1, column=0, columnspan=2, sticky=tk.W)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=(("Python Files", "*.py"), ("All Files", "*.*"))
        )
        self.file_path.set(file_path)
        self.output_filename.set(os.path.basename(file_path))
        self.selected_file_label_text.set("Selected File: " + file_path)

    def select_output_dir(self):
        output_dir = filedialog.askdirectory()
        self.output_dir.set(output_dir)

    def create_build_section(self):
        build_frame = ttk.Frame(self.content_frame)
        self.content_frame.add(build_frame, text="Build")

        platform_frame = ttk.Frame(build_frame)
        platform_frame.pack(pady=20)

        platform_label = ttk.Label(platform_frame, text="Platform:")
        platform_label.grid(row=0, column=0, sticky=tk.W)

        platform_combobox = ttk.Combobox(
            platform_frame,
            values=list(LIBRARIES.keys()),
            textvariable=self.selected_platform,
            state="readonly",
        )
        platform_combobox.grid(row=0, column=1, padx=10)

        platform_combobox.bind("<<ComboboxSelected>>", self.populate_libraries)

        library_frame = ttk.Frame(build_frame)
        library_frame.pack(pady=20)

        library_label = ttk.Label(library_frame, text="Library:")
        library_label.grid(row=0, column=0, sticky=tk.W)

        library_combobox = ttk.Combobox(
            library_frame,
            values=[],
            textvariable=self.selected_library,
            state="readonly",
        )
        library_combobox.grid(row=0, column=1, padx=10)

        build_button = ttk.Button(build_frame, text="Build", command=self.build)
        build_button.pack(pady=20)

    def populate_libraries(self, event):
        platform = self.selected_platform.get()
        libraries = LIBRARIES.get(platform, {})
        library_combobox = (
            self.content_frame.winfo_children()[1]
            .winfo_children()[1]
            .winfo_children()[1]
        )
        library_combobox["values"] = list(libraries.keys())
        library_combobox.current(0)

    def create_settings_section(self):
        settings_frame = ttk.Frame(self.content_frame)
        self.content_frame.add(settings_frame, text="Settings")

        settings_label = ttk.Label(
            settings_frame,
            text="Coming soon!",
            font=("Helvetica", 20),
            padding=(0, 20),
        )
        settings_label.pack()

    def create_help_section(self):
        help_frame = ttk.Frame(self.content_frame)
        self.content_frame.add(help_frame, text="Help")

        help_label = ttk.Label(
            help_frame,
            text="Need help?",
            font=("Helvetica", 20),
            padding=(0, 20),
        )
        help_label.pack()

        help_text = """
        This tool helps you convert Python scripts into standalone executables. 

        1. Select the Python script you want to convert by clicking the 'Select File' button. The output filename field will be automatically populated with the selected file's name.

        2. Choose the platform you want to build the executable for using the 'Platform' dropdown. Available options are Windows, Mac, and Linux.

        3. Choose the library you want to use for building the executable using the 'Library' dropdown. The available options depend on the selected platform.

        4. Select the output directory where you want the executable to be saved by clicking the 'Select Folder' button.

        5. Click the 'Build' button to start the conversion process. The status bar at the bottom will show the progress.

        Note: This tool requires the selected library to be installed on your system.

        For more information and detailed usage instructions, refer to the documentation.
        """
        help_text_label = ttk.Label(
            help_frame, text=help_text, justify=tk.LEFT, wraplength=600
        )
        help_text_label.pack()

    def create_status_bar(self):
        self.status_label = ttk.Label(
            self.window,
            text="Ready",
            anchor=tk.W,
            font=("Helvetica", 12),
            relief=tk.SUNKEN,
            padding=(5, 2),
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def build(self):
        file_path = self.file_path.get()
        platform = self.selected_platform.get()
        library = self.selected_library.get()
        output_dir = self.output_dir.get()
        output_filename = self.output_filename.get()

        if not file_path:
            messagebox.showwarning("Error", "Please select a Python file.")
            return

        if not platform:
            messagebox.showwarning("Error", "Please select a platform.")
            return

        if not library:
            messagebox.showwarning("Error", "Please select a library.")
            return

        if not output_dir:
            messagebox.showwarning("Error", "Please select an output directory.")
            return

        if not output_filename:
            messagebox.showwarning("Error", "Please enter an output filename.")
            return

        library_info = LIBRARIES.get(platform, {}).get(library)
        if not library_info:
            messagebox.showwarning("Error", "Invalid library selection.")
            return

        build_command = library_info["command"]
        build_options = library_info["options"]
        build_extension = BUILD_OPTIONS.get(platform, {}).get("extension", "")

        output_path = os.path.join(output_dir, f"{output_filename}.{build_extension}")

        self.status_label.config(text="Building...")
        self.window.update()

        # Example using PyInstaller
        pyinstaller_command = [
            "pyinstaller",
            "--onefile",
            "--name",
            output_filename,
            "--distpath",
            output_dir,
            *build_options,
            file_path,  # Remove the use of shlex.quote()
        ]
        try:
            subprocess.run(pyinstaller_command, check=True)
        except subprocess.CalledProcessError:
            self.status_label.config(text="Build failed!")
            messagebox.showerror("Build Failed", "An error occurred during the build process.")
            return

        self.status_label.config(text="Build completed!")
        messagebox.showinfo("Build Completed", "The executable was successfully created.")

        file_path = self.file_path.get()
        platform = self.selected_platform.get()
        library = self.selected_library.get()
        output_dir = self.output_dir.get()
        output_filename = self.output_filename.get()

        if not file_path:
            messagebox.showwarning("Error", "Please select a Python file.")
            return

        if not platform:
            messagebox.showwarning("Error", "Please select a platform.")
            return

        if not library:
            messagebox.showwarning("Error", "Please select a library.")
            return

        if not output_dir:
            messagebox.showwarning("Error", "Please select an output directory.")
            return

        if not output_filename:
            messagebox.showwarning("Error", "Please enter an output filename.")
            return

        library_info = LIBRARIES.get(platform, {}).get(library)
        if not library_info:
            messagebox.showwarning("Error", "Invalid library selection.")
            return

        build_command = library_info["command"]
        build_options = library_info["options"]
        build_extension = BUILD_OPTIONS.get(platform, {}).get("extension", "")

        output_path = os.path.join(output_dir, f"{output_filename}.{build_extension}")

        self.status_label.config(text="Building...")
        self.window.update()

        # Example using PyInstaller
        pyinstaller_command = [
            "pyinstaller",
            "--onefile",
            "--name",
            output_filename,
            "--distpath",
            output_dir,
            *build_options,
            file_path,  # Remove the shlex.quote() function call
        ]
        try:
            subprocess.run(pyinstaller_command, check=True)
        except subprocess.CalledProcessError:
            self.status_label.config(text="Build failed!")
            messagebox.showerror("Build Failed", "An error occurred during the build process.")
            return

        self.status_label.config(text="Build completed!")
        messagebox.showinfo("Build Completed", "The executable was successfully created.")

        file_path = self.file_path.get()
        platform = self.selected_platform.get()
        library = self.selected_library.get()
        output_dir = self.output_dir.get()
        output_filename = self.output_filename.get()

        if not file_path:
            messagebox.showwarning("Error", "Please select a Python file.")
            return

        if not platform:
            messagebox.showwarning("Error", "Please select a platform.")
            return

        if not library:
            messagebox.showwarning("Error", "Please select a library.")
            return

        if not output_dir:
            messagebox.showwarning("Error", "Please select an output directory.")
            return

        if not output_filename:
            messagebox.showwarning("Error", "Please enter an output filename.")
            return

        library_info = LIBRARIES.get(platform, {}).get(library)
        if not library_info:
            messagebox.showwarning("Error", "Invalid library selection.")
            return

        build_command = library_info["command"]
        build_options = library_info["options"]
        build_extension = BUILD_OPTIONS.get(platform, {}).get("extension", "")

        output_path = os.path.join(output_dir, f"{output_filename}.{build_extension}")

        self.status_label.config(text="Building...")
        self.window.update()

        # Example using PyInstaller
        pyinstaller_command = [
            "pyinstaller",
            "--onefile",
            "--name",
            output_filename,
            "--distpath",
            output_dir,
            *build_options,
            shlex.quote(file_path),  # Quote the file path to handle special characters
        ]
        
        print("PyInstaller Command:", " ".join(pyinstaller_command))  # Print the generated command

        try:
            subprocess.run(pyinstaller_command, check=True)
        except subprocess.CalledProcessError:
            self.status_label.config(text="Build failed!")
            messagebox.showerror("Build Failed", "An error occurred during the build process.")
            return

        self.status_label.config(text="Build completed!")
        messagebox.showinfo("Build Completed", "The executable was successfully created.")

        file_path = self.file_path.get()
        platform = self.selected_platform.get()
        library = self.selected_library.get()
        output_dir = self.output_dir.get()
        output_filename = self.output_filename.get()

        if not file_path:
            messagebox.showwarning("Error", "Please select a Python file.")
            return

        if not platform:
            messagebox.showwarning("Error", "Please select a platform.")
            return

        if not library:
            messagebox.showwarning("Error", "Please select a library.")
            return

        if not output_dir:
            messagebox.showwarning("Error", "Please select an output directory.")
            return

        if not output_filename:
            messagebox.showwarning("Error", "Please enter an output filename.")
            return

        library_info = LIBRARIES.get(platform, {}).get(library)
        if not library_info:
            messagebox.showwarning("Error", "Invalid library selection.")
            return

        build_command = library_info["command"]
        build_options = library_info["options"]
        build_extension = BUILD_OPTIONS.get(platform, {}).get("extension", "")

        output_path = os.path.join(output_dir, f"{output_filename}.{build_extension}")

        self.status_label.config(text="Building...")
        self.window.update()

        # Example using PyInstaller
        pyinstaller_command = [
            "pyinstaller",
            "--onefile",
            "--name",
            output_filename,
            "--distpath",
            output_dir,
            *build_options,
            shlex.quote(file_path),  # Quote the file path to handle special characters
        ]
        try:
            subprocess.run(pyinstaller_command, check=True)
        except subprocess.CalledProcessError:
            self.status_label.config(text="Build failed!")
            messagebox.showerror("Build Failed", "An error occurred during the build process.")
            return

        self.status_label.config(text="Build completed!")
        messagebox.showinfo("Build Completed", "The executable was successfully created.")

        file_path = self.file_path.get()
        platform = self.selected_platform.get()
        library = self.selected_library.get()
        output_dir = self.output_dir.get()
        output_filename = self.output_filename.get()

        if not file_path:
            messagebox.showwarning("Error", "Please select a Python file.")
            return

        if not platform:
            messagebox.showwarning("Error", "Please select a platform.")
            return

        if not library:
            messagebox.showwarning("Error", "Please select a library.")
            return

        if not output_dir:
            messagebox.showwarning("Error", "Please select an output directory.")
            return

        if not output_filename:
            messagebox.showwarning("Error", "Please enter an output filename.")
            return

        library_info = LIBRARIES.get(platform, {}).get(library)
        if not library_info:
            messagebox.showwarning("Error", "Invalid library selection.")
            return

        build_command = library_info["command"]
        build_options = library_info["options"]
        build_extension = BUILD_OPTIONS.get(platform, {}).get("extension", "")

        output_path = os.path.join(output_dir, f"{output_filename}.{build_extension}")

        self.status_label.config(text="Building...")
        self.window.update()

        # Example using PyInstaller
        pyinstaller_command = [
            "pyinstaller",
            "--onefile",
            "--name",
            output_filename,
            "--distpath",
            output_dir,
            *build_options,
            file_path,
        ]
        try:
            subprocess.run(pyinstaller_command, check=True)
        except subprocess.CalledProcessError:
            self.status_label.config(text="Build failed!")
            messagebox.showerror("Build Failed", "An error occurred during the build process.")
            return

        self.status_label.config(text="Build completed!")
        messagebox.showinfo("Build Completed", "The executable was successfully created.")

        file_path = self.file_path.get()
        platform = self.selected_platform.get()
        library = self.selected_library.get()
        output_dir = self.output_dir.get()
        output_filename = self.output_filename.get()

        if not file_path:
            messagebox.showwarning("Error", "Please select a Python file.")
            return

        if not platform:
            messagebox.showwarning("Error", "Please select a platform.")
            return

        if not library:
            messagebox.showwarning("Error", "Please select a library.")
            return

        if not output_dir:
            messagebox.showwarning("Error", "Please select an output directory.")
            return

        if not output_filename:
            messagebox.showwarning("Error", "Please enter an output filename.")
            return

        library_info = LIBRARIES.get(platform, {}).get(library)
        if not library_info:
            messagebox.showwarning("Error", "Invalid library selection.")
            return

        build_command = library_info["command"]
        build_options = library_info["options"]
        build_extension = BUILD_OPTIONS.get(platform, {}).get("extension", "")

        output_path = os.path.join(output_dir, f"{output_filename}.{build_extension}")

        self.status_label.config(text="Building...")
        self.window.update()

        # Example using PyInstaller
        pyinstaller_command = [
            "pyinstaller",
            file_path,
            "--onefile",
            "--name",
            output_filename,
            "--distpath",
            output_dir,
            *build_options,
        ]
        try:
            subprocess.run(pyinstaller_command, check=True)
        except subprocess.CalledProcessError:
            self.status_label.config(text="Build failed!")
            messagebox.showerror(
                "Build Failed", "An error occurred during the build process."
            )
            return

        self.status_label.config(text="Build completed!")
        messagebox.showinfo(
            "Build Completed", "The executable was successfully created."
        )

    def update_clock(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.status_label.config(text=f"Ready | {current_time}")
        self.window.after(1000, self.update_clock)

    def save_settings(self):
        settings = {
            "output_dir": self.output_dir.get(),
        }
        with open("settings.json", "w") as file:
            json.dump(settings, file)

    def load_settings(self):
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as file:
                settings = json.load(file)
                self.output_dir.set(settings.get("output_dir", ""))

    def on_closing(self):
        self.save_settings()
        self.window.destroy()

    def run(self):
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()


if __name__ == "__main__":
    app = PythonToExecutableApp()
    app.run()
