import os
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
import subprocess
import winrm
import threading
import time
import requests
from PIL import Image, ImageTk
from io import BytesIO


class RemoteWindowsChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Remote Windows Checker")
        self.root.configure(bg="#1e1e1e")
        self.root.option_add("*Font", "Arial 12")
        self.root.geometry("1920x1080")

        self.set_dark_theme()

        icon_url = "https://www.pngall.com/wp-content/uploads/2/Windows-Logo-PNG-Transparent-HD-Photo.png"
        response = requests.get(icon_url)
        if response.status_code == 200:
            icon_image = Image.open(BytesIO(response.content))
            self.root.iconphoto(True, ImageTk.PhotoImage(icon_image))

        self.navbar_frame = tk.Frame(self.root, bg="#2f2f2f")
        self.navbar_frame.pack(side=tk.TOP, fill=tk.X)

        self.title_label = tk.Label(
            self.navbar_frame,
            text="Remote Windows Checker",
            fg="white",
            bg="#2f2f2f",
            font=("Arial", 24, "bold"),
            padx=10,
            pady=10,
        )
        self.title_label.pack(side=tk.LEFT)

        self.remote_mode = False
        self.remote_button = tk.Button(
            self.navbar_frame,
            text="Remote",
            command=self.toggle_remote_mode,
            bg="#2f2f2f",
            fg="#FFFFFF",
            font=("Arial", 12),
            relief=tk.FLAT,
            activebackground="#555555",
            activeforeground="#FFFFFF",
        )
        self.remote_button.pack(side=tk.LEFT, padx=10)

        self.mode_label = tk.Label(
            self.navbar_frame,
            text="Local Mode",
            bg="#2f2f2f",
            fg="#FFFFFF",
            font=("Arial", 12),
        )
        self.mode_label.pack(side=tk.LEFT)

        self.status_bar = tk.Label(
            self.navbar_frame,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 12),
            bg="#2f2f2f",
            fg="#FFFFFF",
        )
        self.status_bar.pack(side=tk.RIGHT, padx=10)

        self.clock_label = tk.Label(
            self.navbar_frame,
            bg="#2f2f2f",
            fg="#FFFFFF",
            font=("Arial", 12),
        )
        self.clock_label.pack(side=tk.RIGHT)

        self.remote_frame = tk.Frame(self.root, bg="#1e1e1e")

        self.panel_label = tk.Label(
            self.remote_frame,
            text="Panel SN:",
            font=("Arial", 12),
            bg="#1e1e1e",
            fg="#FFFFFF",
        )
        self.panel_label.grid(row=0, column=0, padx=5, pady=5)

        self.panel_entry = tk.Entry(self.remote_frame, font=("Arial", 12))
        self.panel_entry.grid(row=0, column=1, padx=5, pady=5)

        self.username_label = tk.Label(
            self.remote_frame,
            text="Username:",
            font=("Arial", 12),
            bg="#1e1e1e",
            fg="#FFFFFF",
        )
        self.username_label.grid(row=1, column=0, padx=5, pady=5)

        self.username_entry = tk.Entry(self.remote_frame, font=("Arial", 12))
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        self.password_label = tk.Label(
            self.remote_frame,
            text="Password:",
            font=("Arial", 12),
            bg="#1e1e1e",
            fg="#FFFFFF",
        )
        self.password_label.grid(row=2, column=0, padx=5, pady=5)

        self.password_entry = tk.Entry(self.remote_frame, show="*", font=("Arial", 12))
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        self.auth_label = tk.Label(
            self.remote_frame,
            text="Authentication:",
            font=("Arial", 12),
            bg="#1e1e1e",
            fg="#FFFFFF",
        )
        self.auth_label.grid(row=3, column=0, padx=5, pady=5)

        authentication_options = ["NTLM", "Kerberos", "Default"]
        self.auth_var = tk.StringVar()
        self.auth_dropdown = ttk.Combobox(
            self.remote_frame,
            values=authentication_options,
            state="readonly",
            font=("Arial", 12),
            textvariable=self.auth_var,
        )
        self.auth_dropdown.grid(row=3, column=1, padx=5, pady=5)
        self.auth_dropdown.current(0)

        self.check_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.check_frame.pack(pady=10)

        check_button_texts = [
            "Check OS Version",
            "Check Firewall Status",
            "Check Antivirus Status",
            "Check Windows Updates",
            "Check Password Policy",
            "Check Startup Entries",
            "Check Open Ports",
            "Check Disk Space",
            "Check Event Logs",
        ]
        self.check_var = tk.StringVar()
        self.check_var.set(check_button_texts[0])
        self.check_dropdown = ttk.Combobox(
            self.check_frame,
            values=check_button_texts,
            state="readonly",
            font=("Arial", 12),
            textvariable=self.check_var,
        )
        self.check_dropdown.grid(row=0, column=0, padx=5, pady=5)

        self.run_check_button = tk.Button(
            self.check_frame,
            text="Run Check",
            command=self.run_security_check,
            width=15,
        )
        self.run_check_button.grid(row=0, column=1, padx=5, pady=5)

        self.clear_button = tk.Button(
            self.navbar_frame, text="Clear", command=self.clear_text, width=20
        )
        self.clear_button.pack(side=tk.RIGHT, padx=10)

        self.console_frame = tk.Frame(self.root, bg="#000000")
        self.console_frame.pack(pady=5, fill=tk.BOTH, expand=True)

        self.console_text = scrolledtext.ScrolledText(
            self.console_frame,
            height=10,
            width=100,
            font=("Courier New", 10),
            bg="#000000",
            fg="#FFFFFF",
            wrap=tk.WORD,
        )
        self.console_text.pack(fill=tk.BOTH, expand=True)

        self.create_menu()

        self.current_operation = ""
        self.update_clock_and_status()

    def set_dark_theme(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TLabel", background="#1e1e1e", foreground="#FFFFFF", font=("Arial", 12)
        )
        style.configure("TButton", relief=tk.RAISED, font=("Arial", 12))
        style.map(
            "TButton",
            background=[("active", "#555555")],
            foreground=[("active", "#FFFFFF")],
        )
        style.configure(
            "Horizontal.TProgressbar",
            troughcolor="#1e1e1e",
            background="#FFFFFF",
            bordercolor="#1e1e1e",
            lightcolor="#1e1e1e",
            darkcolor="#1e1e1e",
        )

    def toggle_remote_mode(self):
        self.remote_mode = not self.remote_mode
        current_mode = "Remote Mode" if self.remote_mode else "Local Mode"
        self.mode_label.config(text=current_mode)
        if self.remote_mode:
            self.remote_frame.pack(side=tk.LEFT, padx=10, pady=10)
            self.remote_button.config(relief=tk.SUNKEN)
        else:
            self.remote_frame.pack_forget()
            self.remote_button.config(relief=tk.FLAT)

    def save_to_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text Files", "*.txt")]
        )
        if not file_path:
            return
        with open(file_path, "w") as file:
            file.write(self.console_text.get("1.0", tk.END))

    def show_about_info(self):
        about_info = "Windows Security Checker\nVersion 1.0\n\nCreated by YourName"
        tk.messagebox.showinfo("About", about_info)

    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Save Output", command=self.save_to_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Clear Output", command=self.clear_output)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_command(
            label="Toggle Remote Mode", command=self.toggle_remote_mode
        )
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)

        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about_info)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.root.config(menu=self.menu_bar)

    def run_security_check(self):
        self.console_text.delete(1.0, tk.END)
        check_type = self.check_var.get()
        threading.Thread(
            target=self.run_security_check_thread, args=(check_type,)
        ).start()

    def run_security_check_thread(self, check_type):
        self.current_operation = check_type
        result = self.run_check(check_type)
        self.update_result_text(result)
        self.current_operation = ""

    def run_check(self, check_type):
        if self.remote_mode:
            result = self.run_check_remote(check_type)
        else:
            result = self.run_check_local(check_type)
        return result.strip()

    def run_check_local(self, check_type):
        try:
            if check_type == "Check OS Version":
                result = subprocess.check_output(["systeminfo"]).decode("utf-8")
            elif check_type == "Check Firewall Status":
                result = subprocess.check_output(
                    ["netsh", "advfirewall", "show", "allprofiles"]
                ).decode("utf-8")
            elif check_type == "Check Antivirus Status":
                result = subprocess.check_output(
                    ["powershell", "Get-MpComputerStatus"]
                ).decode("utf-8")
            elif check_type == "Check Windows Updates":
                result = subprocess.check_output(
                    ["powershell", "Get-WUHistory"]
                ).decode("utf-8")
            elif check_type == "Check Password Policy":
                result = subprocess.check_output(["net", "accounts"]).decode("utf-8")
            elif check_type == "Check Startup Entries":
                result = subprocess.check_output(
                    ["wmic", "startup", "list", "full"]
                ).decode("utf-8")
            elif check_type == "Check Open Ports":
                result = subprocess.check_output(["netstat", "-ano"]).decode("utf-8")
            elif check_type == "Check Disk Space":
                result = subprocess.check_output(
                    ["wmic", "logicaldisk", "get", "freespace,caption"]
                ).decode("utf-8")
            elif check_type == "Check Event Logs":
                result = subprocess.check_output(
                    [
                        "powershell",
                        "Get-EventLog",
                        "-LogName",
                        "Application",
                        "-Newest",
                        "10",
                    ]
                ).decode("utf-8")
        except subprocess.CalledProcessError as e:
            result = f"Error: {e.output.decode('utf-8')}"
        return result.strip()

    def run_check_remote(self, check_type):
        result = ""
        try:
            host = self.panel_entry.get().strip()
            username = self.username_entry.get().strip()
            password = self.password_entry.get().strip()
            auth_type = self.auth_var.get()
            session = winrm.Session(
                host,
                auth=(username, password),
                transport="ntlm" if auth_type == "NTLM" else "kerberos",
                server_cert_validation="ignore",
            )
            if check_type == "Check OS Version":
                result = session.run_ps("systeminfo").std_out.decode("utf-8")
            elif check_type == "Check Firewall Status":
                result = session.run_ps(
                    "netsh advfirewall show allprofiles"
                ).std_out.decode("utf-8")
            elif check_type == "Check Antivirus Status":
                result = session.run_ps("Get-MpComputerStatus").std_out.decode("utf-8")
            elif check_type == "Check Windows Updates":
                powershell_script = """
                    $hotFixes = Get-HotFix
                    $updates = $hotFixes | Where-Object { $_.Description -eq "Update" }
                    $result = $updates | ForEach-Object { $_.HotFixID }
                    $result -join "`n"
                """
                result = session.run_ps(powershell_script).std_out.decode("utf-8")
            elif check_type == "Check Password Policy":
                result = session.run_ps("net accounts").std_out.decode("utf-8")
            elif check_type == "Check Startup Entries":
                result = session.run_ps("wmic startup list full").std_out.decode(
                    "utf-8"
                )
            elif check_type == "Check Open Ports":
                result = session.run_ps("netstat -ano").std_out.decode("utf-8")
            elif check_type == "Check Event Logs":
                result = session.run_ps(
                    "Get-EventLog -LogName Application -Newest 100"
                ).std_out.decode("utf-8")
            elif check_type == "Check Disk Space":
                result = session.run_ps(
                    "wmic logicaldisk get freespace,caption"
                ).std_out.decode("utf-8")
        except Exception as e:
            result = f"Error: {str(e)}"
        return result.strip()

    def update_result_text(self, result):
        self.console_text.insert(tk.END, result)
        self.status_bar.config(text=f"{self.current_operation} completed.")

    def update_clock_and_status(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.config(text=current_time)
        if self.current_operation:
            self.status_bar.config(text=f"{self.current_operation} in progress...")
        else:
            self.status_bar.config(text="Ready")
        self.status_bar.after(1000, self.update_clock_and_status)

    def clear_text(self):
        self.console_text.delete("1.0", tk.END)

    def clear_output(self):
        self.console_text.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    gui = RemoteWindowsChecker(root)
    root.mainloop()
