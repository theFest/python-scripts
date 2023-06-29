import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Menu
import os
import subprocess
import json
from datetime import datetime
from tkinter.scrolledtext import ScrolledText
from ttkthemes import ThemedTk


LIBRARIES = {
    "Windows": {
        "PyInstaller": {
            "command": "pyinstaller",
            "options": "-w",
        },
        "cx_Freeze": {
            "command": "cxfreeze",
            "options": "--target-dir",
        },
        "py2exe": {
            "command": "py -m py2exe",
            "options": "",
        },
    },
    "macOS": {
        "PyInstaller": {
            "command": "pyinstaller",
            "options": "-w",
        },
        "py2app": {
            "command": "python setup.py py2app",
            "options": "",
        },
    },
    "Linux": {
        "PyInstaller": {
            "command": "pyinstaller",
            "options": "-w",
        },
        "cx_Freeze": {
            "command": "cxfreeze",
            "options": "--target-dir",
        },
    },
}


class PythonToExecutableApp(ThemedTk):
    def __init__(self):
        super().__init__(theme="equilux")
        self.title("Python to Executable")
        self.geometry("800x500")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.bind("<Escape>", self.on_exit)

        self.selected_platform = tk.StringVar()
        self.selected_library = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.file_paths = []

        self.create_menu()
        self.create_content_frame()
        self.create_build_section()
        self.create_settings_section()
        self.create_help_section()
        self.create_status_bar()
        self.create_output_window()

        self.load_settings()
        self.update_clock()

    def create_menu(self):
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.on_exit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

    def create_content_frame(self):
        self.content_frame = ttk.Notebook(self)
        self.content_frame.pack(expand=True, fill="both")

    def create_build_section(self):
        build_frame = ttk.Frame(self.content_frame)
        self.content_frame.add(build_frame, text="Build")

        platform_label = ttk.Label(
            build_frame,
            text="Platform:",
            font=("Arial", 14, "bold"),
        )
        platform_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        platform_combobox = ttk.Combobox(
            build_frame,
            textvariable=self.selected_platform,
            state="readonly",
        )
        platform_combobox["values"] = list(LIBRARIES.keys())
        platform_combobox.bind("<<ComboboxSelected>>", self.update_library_combobox)
        platform_combobox.grid(row=0, column=1, padx=10, pady=10)

        library_label = ttk.Label(
            build_frame,
            text="Library:",
            font=("Arial", 14, "bold"),
        )
        library_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.library_combobox = ttk.Combobox(
            build_frame,
            textvariable=self.selected_library,
            state="readonly",
        )
        self.library_combobox.grid(row=1, column=1, padx=10, pady=10)

        select_button = ttk.Button(
            build_frame,
            text="Select File(s)",
            command=self.select_files,
        )
        select_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)

        self.file_listbox = tk.Listbox(
            build_frame,
            width=80,
            height=10,
            selectmode=tk.MULTIPLE,
        )
        self.file_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        build_button = ttk.Button(
            build_frame,
            text="Build",
            command=self.build_executable,
        )
        build_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def create_settings_section(self):
        settings_frame = ttk.Frame(self.content_frame)
        self.content_frame.add(settings_frame, text="Settings")

        output_dir_label = ttk.Label(
            settings_frame,
            text="Output Directory:",
            font=("Arial", 14, "bold"),
        )
        output_dir_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        output_dir_entry = ttk.Entry(
            settings_frame,
            textvariable=self.output_dir,
            width=70,
        )
        output_dir_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        output_dir_button = ttk.Button(
            settings_frame,
            text="Browse",
            command=self.browse_output_dir,
        )
        output_dir_button.grid(row=0, column=2, padx=10, pady=10, sticky=tk.W)

        save_button = ttk.Button(
            settings_frame,
            text="Save Settings",
            command=self.save_settings,
        )
        save_button.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    def create_help_section(self):
        help_frame = ttk.Frame(self.content_frame)
        self.content_frame.add(help_frame, text="Help")

        help_text = (
            "Instructions:\n\n"
            "1. Select the platform and library.\n"
            "2. Click 'Select File(s)' to choose one or more Python files.\n"
            "3. Click 'Build' to generate the executable.\n\n"
            "Note: The selected library must be installed in your system.\n\n"
            "For more information, refer to the documentation."
        )

        help_label = ttk.Label(
            help_frame,
            text=help_text,
            font=("Arial", 12),
        )
        help_label.pack(padx=10, pady=10)

    def create_status_bar(self):
        self.status_bar = ttk.Label(
            self,
            text="",
            relief=tk.SUNKEN,
            anchor=tk.W,
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_output_window(self):
        self.output_window = ScrolledText(self, state=tk.DISABLED)
        self.output_window.pack(expand=True, fill="both")

    def select_files(self):
        file_paths = filedialog.askopenfilenames(
            filetypes=[("Python Files", "*.py")],
        )
        self.file_paths = list(file_paths)
        self.update_file_listbox()

    def update_file_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for file_path in self.file_paths:
            file_name = os.path.basename(file_path)
            self.file_listbox.insert(tk.END, file_name)

    def update_library_combobox(self, event=None):
        platform = self.selected_platform.get()
        libraries = LIBRARIES.get(platform, {})
        library_values = list(libraries.keys())
        self.library_combobox["values"] = library_values

        if library_values:
            self.library_combobox.current(0)

    def build_executable(self):
        if not os.path.exists(self.output_dir.get()):
            messagebox.showerror("Error", "Output directory does not exist.")
            return

        if not self.file_paths:
            messagebox.showerror("Error", "No file(s) selected.")
            return

        platform = self.selected_platform.get()
        library = self.selected_library.get()
        library_info = LIBRARIES.get(platform, {}).get(library)

        if not library_info:
            messagebox.showerror("Error", "Library not supported for the selected platform.")
            return

        self.clear_output_window()

        try:
            for file_path in self.file_paths:
                self.build_single_executable(file_path, library_info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def build_single_executable(self, file_path, library_info):
        command = library_info["command"]
        options = library_info.get("options", "")

        file_name = os.path.basename(file_path)
        output_dir = self.output_dir.get()
        output_name = f"{os.path.splitext(file_name)[0]}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        self.append_output(f"Building executable for: {file_name}\n")
        self.append_output(f"Output directory: {output_dir}\n\n")

        process = subprocess.Popen(
            [command, file_path, options, output_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            shell=True,
        )


        while process.poll() is None:
            output = process.stdout.readline().strip()
            if output:
                self.append_output(output + "\n")

        if process.returncode != 0:
            error_output = process.stderr.read().strip()
            self.append_output(f"\nError: {error_output}\n")
        else:
            self.append_output("\nExecutable built successfully.\n")

    def append_output(self, text):
        self.output_window.configure(state=tk.NORMAL)
        self.output_window.insert(tk.END, text)
        self.output_window.configure(state=tk.DISABLED)
        self.output_window.see(tk.END)

    def clear_output_window(self):
        self.output_window.configure(state=tk.NORMAL)
        self.output_window.delete(1.0, tk.END)
        self.output_window.configure(state=tk.DISABLED)

    def browse_output_dir(self):
        output_dir = filedialog.askdirectory()
        self.output_dir.set(output_dir)

    def save_settings(self):
        settings = {
            "output_dir": self.output_dir.get(),
        }
        with open("settings.json", "w") as file:
            json.dump(settings, file)
        messagebox.showinfo("Settings Saved", "Settings saved successfully.")

    def load_settings(self):
        try:
            with open("settings.json", "r") as file:
                settings = json.load(file)
            self.output_dir.set(settings.get("output_dir", ""))
        except FileNotFoundError:
            pass

    def show_about(self):
        messagebox.showinfo(
            "About",
            "Python to Executable\n\n"
            "Version: 1.0\n"
            "Author: Your Name\n"
            "Year: 2023",
        )

    def update_clock(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_bar.config(text=current_time)
        self.after(1000, self.update_clock)

    def on_exit(self, event=None):
        if messagebox.askokcancel("Exit", "Do you want to exit?"):
            self.destroy()


if __name__ == "__main__":
    app = PythonToExecutableApp()
    app.mainloop()
