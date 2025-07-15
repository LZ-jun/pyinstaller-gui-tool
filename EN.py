import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
import shutil
from PIL import Image
import tempfile

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    os.environ['TCL_LIBRARY'] = os.path.join(base_path, '_tk_data', 'tcl8.6')
    os.environ['TK_LIBRARY'] = os.path.join(base_path, '_tk_data', 'tk8.6')

class PyInstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Executable Builder")
        self.root.geometry("790x820")
        self.root.minsize(800, 820)
        
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Microsoft YaHei UI", 10))
        self.style.configure("TButton", font=("Microsoft YaHei UI", 10))
        self.style.configure("TCheckbutton", font=("Microsoft YaHei UI", 10))
        
        self.main_frame = ttk.Frame(root, padding="20 20 20 20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.main_frame, text="Python File (.py):").grid(row=0, column=0, sticky=tk.W, pady=10)
        self.script_path_var = tk.StringVar()
        self.script_entry = ttk.Entry(self.main_frame, textvariable=self.script_path_var, width=50)
        self.script_entry.grid(row=0, column=1, pady=10, padx=5, sticky=tk.W)
        ttk.Button(self.main_frame, text="Browse...", command=self.browse_script).grid(row=0, column=2, pady=10, padx=5)
        
        self.use_icon_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.main_frame, text="Icon File (.ico/.png/.jpg/.svg):", variable=self.use_icon_var,
                       command=self.toggle_icon).grid(row=1, column=0, sticky=tk.W, pady=10)
        
        self.icon_path_var = tk.StringVar()
        self.icon_entry = ttk.Entry(self.main_frame, textvariable=self.icon_path_var, width=50)
        self.icon_entry.grid(row=1, column=1, pady=10, padx=5, sticky=tk.W)
        self.icon_button = ttk.Button(self.main_frame, text="Browse...", command=self.browse_icon)
        self.icon_button.grid(row=1, column=2, pady=10, padx=5)
        
        self.include_images_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.main_frame, text="Include Images Folder", variable=self.include_images_var,
                       command=self.toggle_images_folder).grid(row=2, column=0, sticky=tk.W, pady=10)
        
        self.images_path_var = tk.StringVar()
        self.images_entry = ttk.Entry(self.main_frame, textvariable=self.images_path_var, width=50)
        self.images_entry.grid(row=2, column=1, pady=10, padx=5, sticky=tk.W)
        self.images_button = ttk.Button(self.main_frame, text="Browse...", command=self.browse_images)
        self.images_button.grid(row=2, column=2, pady=10, padx=5)
        
        ttk.Label(self.main_frame, text="Output Filename:").grid(row=3, column=0, sticky=tk.W, pady=10)
        self.output_name_var = tk.StringVar(value="myapp")
        ttk.Entry(self.main_frame, textvariable=self.output_name_var, width=35).grid(row=3, column=1, sticky=tk.W, pady=10, padx=5)
        
        ttk.Label(self.main_frame, text="Output Path:").grid(row=4, column=0, sticky=tk.W, pady=10)
        self.output_path_var = tk.StringVar()
        self.output_entry = ttk.Entry(self.main_frame, textvariable=self.output_path_var, width=50)
        self.output_entry.grid(row=4, column=1, pady=10, padx=5, sticky=tk.W)
        self.output_button = ttk.Button(self.main_frame, text="Browse...", command=self.browse_output)
        self.output_button.grid(row=4, column=2, pady=10, padx=5)
        
        options_frame = ttk.LabelFrame(self.main_frame, text="Packaging Options", padding="10 10 10 10")
        options_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10, padx=0)
        
        self.onefile_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="One File Package", variable=self.onefile_var).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        
        self.windowed_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Windowed Mode (No Console)", variable=self.windowed_var).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        self.clean_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Clean Temporary Files", variable=self.clean_var).grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
        
        self.advanced_options_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.main_frame, text="Show Advanced Options", variable=self.advanced_options_var,
                       command=self.toggle_advanced_options).grid(row=6, column=0, sticky=tk.W, pady=5)
        
        self.advanced_frame = ttk.Frame(self.main_frame)
        self.advanced_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.hidden_imports_var = tk.StringVar()
        ttk.Label(self.advanced_frame, text="Hidden Imports (comma-separated):").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.advanced_frame, textvariable=self.hidden_imports_var, width=70).grid(row=0, column=1, pady=5, padx=5)
        
        self.excludes_var = tk.StringVar()
        ttk.Label(self.advanced_frame, text="Excluded Modules (comma-separated):").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.advanced_frame, textvariable=self.excludes_var, width=70).grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(self.main_frame, text="Build Log:").grid(row=8, column=0, sticky=tk.W, pady=10)
        self.log_text = tk.Text(self.main_frame, height=12, width=80, wrap=tk.WORD)
        self.log_text.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=9, column=3, sticky=(tk.N, tk.S))
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        copyright_frame = ttk.Frame(self.main_frame, padding="10 10 10 10")
        copyright_frame.grid(row=10, column=0, columnspan=3, pady=5, sticky=tk.W)
        
        ttk.Label(copyright_frame, text="@2025 BY lzjun | ").pack(side=tk.LEFT)
        
        self.github_link = tk.Label(copyright_frame, text="https://github.com/LZ-jun", fg="blue", cursor="hand2", font=("Microsoft YaHei UI", 10, "underline"))
        self.github_link.pack(side=tk.LEFT)
        self.github_link.bind("<Button-1>", lambda e: self.copy_github())
        
        ttk.Label(copyright_frame, text=" | Click to copy").pack(side=tk.LEFT, padx=5)
        
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=11, column=0, columnspan=3, pady=15)
        
        start_btn = ttk.Button(button_frame, text="Start Building", command=self.start_building)
        start_btn.pack(side=tk.LEFT, padx=20)
        exit_btn = ttk.Button(button_frame, text="Exit", command=root.destroy)
        exit_btn.pack(side=tk.LEFT, padx=20)
        
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)
        
        self.toggle_images_folder()
        self.toggle_advanced_options()
        self.toggle_icon()
        
        self.temp_ico_path = None
        self.temp_dir = None
        
        self.update_default_output_path()
        self.output_name_var.trace_add("write", self.update_default_output_path)
    
    def toggle_icon(self):
        state = tk.NORMAL if self.use_icon_var.get() else tk.DISABLED
        self.icon_entry.configure(state=state)
        self.icon_button.configure(state=state)
        if not self.use_icon_var.get():
            self.icon_path_var.set("")
    
    def browse_script(self):
        file_path = filedialog.askopenfilename(
            title="Select Python Script",
            filetypes=[("Python files", "*.py")]
        )
        if file_path:
            self.script_path_var.set(file_path)
            script_name = os.path.basename(file_path)
            self.output_name_var.set(os.path.splitext(script_name)[0])
    
    def browse_icon(self):
        file_path = filedialog.askopenfilename(
            title="Select Icon File",
            filetypes=[
                ("All Supported Formats", "*.ico;*.jpg;*.jpeg;*.png;*.svg"),
                ("ICO Files", "*.ico"),
                ("JPG Files", "*.jpg;*.jpeg"),
                ("PNG Files", "*.png"),
                ("SVG Files", "*.svg")
            ]
        )
        if file_path:
            self.icon_path_var.set(file_path)
    
    def browse_images(self):
        folder_path = filedialog.askdirectory(title="Select Images Folder")
        if folder_path:
            self.images_path_var.set(folder_path)
    
    def browse_output(self):
        folder_path = filedialog.askdirectory(title="Select Output Folder")
        if folder_path:
            output_name = self.output_name_var.get()
            self.output_path_var.set(os.path.join(folder_path, output_name))
    
    def toggle_images_folder(self):
        state = tk.NORMAL if self.include_images_var.get() else tk.DISABLED
        self.images_path_var.set("")
        self.images_entry.configure(state=state)
        self.images_button.configure(state=state)
    
    def toggle_advanced_options(self):
        if self.advanced_options_var.get():
            self.advanced_frame.grid()
        else:
            self.advanced_frame.grid_remove()
    
    def update_default_output_path(self, *args):
        output_name = self.output_name_var.get()
        if output_name:
            default_path = os.path.join(os.getcwd(), output_name)
            self.output_path_var.set(default_path)
    
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def convert_image_to_ico(self, image_path, size=(256, 256)):
        try:
            if not os.path.exists(image_path):
                self.log(f"Error: Icon file not found: {image_path}")
                return None
                
            ext = os.path.splitext(image_path)[1].lower()
            
            if ext == ".svg":
                self.log("Warning: SVG conversion has limited support. Consider using PNG/JPG format instead.")
                try:
                    with Image.open(image_path) as img:
                        img = img.convert("RGBA")
                        img = img.resize(size, Image.LANCZOS)
                except Exception as e:
                    self.log(f"Error: Failed to process SVG file: {str(e)}")
                    self.log("Hint: Convert SVG to PNG/JPG before using.")
                    return None
            else:
                try:
                    with Image.open(image_path) as img:
                        if img.mode != "RGBA":
                            img = img.convert("RGBA")
                        img = img.resize(size, Image.LANCZOS)
                except Exception as e:
                    self.log(f"Error: Failed to open image file: {str(e)}")
                    return None
            
            self.temp_dir = tempfile.mkdtemp(prefix="pyinstaller_icon_")
            
            base_name = os.path.basename(image_path)
            file_name, _ = os.path.splitext(base_name)
            ico_path = os.path.join(self.temp_dir, f"{file_name}.ico")
            
            img.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
            
            self.log(f"Successfully converted {image_path} to ICO format")
            return ico_path
        except Exception as e:
            self.log(f"Error: Icon conversion failed: {str(e)}")
            return None
    
    def copy_github(self):
        self.root.clipboard_clear()
        self.root.clipboard_append("https://github.com/LZ-jun")
        messagebox.showinfo("Copy Success", "GitHub URL copied to clipboard")
    
    def start_building(self):
        script_path = self.script_path_var.get()
        if not script_path:
            messagebox.showerror("Error", "Please select a Python script")
            return
        
        if not os.path.exists(script_path):
            messagebox.showerror("Error", f"Script file not found: {script_path}")
            return
        
        output_path = self.output_path_var.get()
        
        if not os.path.exists(output_path):
            try:
                os.makedirs(output_path)
                self.log(f"Created output directory: {output_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create output directory: {str(e)}")
                return
        
        self.log_text.delete(1.0, tk.END)
        
        icon_path = self.icon_path_var.get() if self.use_icon_var.get() else ""
        self.temp_ico_path = None
        
        if icon_path and os.path.exists(icon_path):
            ext = os.path.splitext(icon_path)[1].lower()
            
            if ext != ".ico":
                self.log(f"Non-ICO icon file detected ({ext}), converting...")
                self.temp_ico_path = self.convert_image_to_ico(icon_path)
                if self.temp_ico_path:
                    self.log(f"Using converted ICO file: {self.temp_ico_path}")
                else:
                    messagebox.showerror("Error", "Icon conversion failed. Please ensure the image format is correct or try using .ico format.")
                    return
            else:
                self.temp_ico_path = icon_path
                self.log(f"Using original ICO icon: {icon_path}")
        else:
            self.log("No icon specified, using default icon")
        
        build_thread = threading.Thread(target=self.build_application, args=(output_path,))
        build_thread.daemon = True
        build_thread.start()
    
    def build_application(self, output_dir):
        try:
            self.status_var.set("Building...")
            
            script_path = self.script_path_var.get()
            output_name = self.output_name_var.get()
            
            dist_dir = os.path.join(output_dir, "dist")
            build_dir = os.path.join(output_dir, "build")
            
            cmd = ["pyinstaller"]
            python_exe = os.environ.get('PYTHON_EXECUTABLE')
            is_frozen = getattr(sys, 'frozen', False)
            if is_frozen and not python_exe:
                result = messagebox.askyesno(
                    "Configure Python Path",
                    "Recursive packaging environment detected! You need to select the **original Python interpreter** (not the packaged tool).\n"
                    "(Typical path: C:\\Python39\\python.exe or the python.exe in your Anaconda environment)"
                )
                if result:
                    python_exe = filedialog.askopenfilename(
                        title="Select Original Python Interpreter",
                        filetypes=[("Python Executable", "python.exe")]
                    )
                    if not python_exe:
                        messagebox.showerror("Error", "Python interpreter not selected. Packaging failed!")
                        return
                    os.environ['PYTHON_EXECUTABLE'] = python_exe
                else:
                    messagebox.showerror("Error", "Original Python path not configured. Recursive packaging will fail!")
                    return
            if not python_exe:
                python_exe = sys.executable
            python_dir = os.path.dirname(python_exe)
            tcl_dir = os.path.join(python_dir, "tcl", "tcl8.6")
            tk_dir = os.path.join(python_dir, "tcl", "tk8.6")

            if not os.path.exists(tcl_dir) or not os.path.exists(tk_dir):
                messagebox.showerror(
                    "Dependency Missing",
                    f"The selected Python interpreter is missing Tcl/Tk runtime files!\n"
                    f"Expected paths:\n{tcl_dir}\n{tk_dir}\n"
                    f"Please install a complete Python or select the correct interpreter."
                )
                return
        
            cmd.extend([
                f"--add-data={tcl_dir};_tk_data/tcl8.6",
                f"--add-data={tk_dir};_tk_data/tk8.6"
            ])
            self.log(f"Bound original Tcl/Tk paths:\n{tcl_dir}\n{tk_dir}")
        

            
            if self.onefile_var.get():
                cmd.append("--onefile")
            
            if self.windowed_var.get():
                cmd.append("--windowed")
            
            if self.clean_var.get():
                cmd.append("--clean")
            
            if self.temp_ico_path:
                cmd.extend(["--icon", self.temp_ico_path])
            
            if self.include_images_var.get():
                images_path = self.images_path_var.get()
                if images_path and os.path.exists(images_path):
                    cmd.extend(["--add-data", f"{images_path}\\*;images"])
            
            hidden_imports = self.hidden_imports_var.get().strip()
            if hidden_imports:
                for module in hidden_imports.split(','):
                    cmd.extend(["--hidden-import", module.strip()])
            
            excludes = self.excludes_var.get().strip()
            if excludes:
                for module in excludes.split(','):
                    cmd.extend(["--exclude-module", module.strip()])
            
            cmd.extend([
                "--name", output_name,
                "--distpath", dist_dir,
                "--workpath", build_dir,
                "--specpath", output_dir,
                "--log-level", "INFO",
                script_path
            ])
            
            self.log("Executing command: " + " ".join(cmd))
            self.log(f"All outputs will be saved to: {output_dir}")
            self.log("Starting build process...")
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            for line in iter(process.stdout.readline, ''):
                self.log(line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                self.log(f"Build successful! Executable located at: {os.path.join(dist_dir, output_name)}.exe")
                self.status_var.set("Build Complete")
                messagebox.showinfo("Success", f"Build completed!\nExecutable located at:\n{os.path.join(dist_dir, output_name)}.exe")
            else:
                self.log(f"Build failed with return code: {process.returncode}")
                self.status_var.set("Build Failed")
                messagebox.showerror("Error", f"Build failed with return code: {process.returncode}\nCheck the log for details")
                
        except Exception as e:
            self.log(f"An error occurred: {str(e)}")
            self.status_var.set("Error")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            if self.temp_dir and os.path.exists(self.temp_dir):
                try:
                    shutil.rmtree(self.temp_dir)
                    self.log("Temporary files cleaned up")
                except Exception as e:
                    self.log(f"Warning: Failed to clean up temporary files: {str(e)}")
            
            self.status_var.set("Ready")

if __name__ == "__main__":
    try:
        import PIL
        pillow_available = True
    except ImportError:
        pillow_available = False
        print("Warning: Pillow library not installed. Icon conversion will be disabled. Please install with `pip install pillow`.")
    
    root = tk.Tk()
    app = PyInstallerGUI(root)
    
    if not pillow_available:
        messagebox.showwarning("Dependency Missing", "Pillow library not installed. Icon conversion functionality will be disabled.\nPlease install with `pip install pillow` and try again.")
        app.icon_button.configure(state=tk.DISABLED)
    
    root.mainloop()