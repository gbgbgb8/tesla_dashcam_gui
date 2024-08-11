import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import sys
import platform
import os
import shutil
from tooltip_data import TOOLTIPS

def print_debug_info():
    print(f"Python version: {sys.version}")
    print(f"Tkinter version: {tk.TkVersion}")
    print(f"Tcl version: {tk.TclVersion}")
    print(f"Operating System: {platform.system()} {platform.version()}")
    print(f"Tkinter library path: {tk.__file__}")

print_debug_info()

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, 
                         background="#FFFFDD",  # Light yellow background
                         foreground="#000000",  # Black text
                         relief="solid", 
                         borderwidth=1,
                         padx=5,
                         pady=5)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class TeslaDashcamGUI:
    def __init__(self, master):
        self.master = master
        master.title("Tesla Dashcam Video Creator")
        master.minsize(800, 600)
        master.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.create_main_tab()
        self.create_layout_tab()
        self.create_timestamp_tab()
        self.create_advanced_tab()
        self.create_output_tab()

        ttk.Button(self.master, text="Create Video", command=self.run_script).pack(pady=10)

    def create_main_tab(self):
        main_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(main_frame, text="Main")

        ttk.Label(main_frame, text="Source Folder:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.source_entry = ttk.Entry(main_frame, width=50)
        self.source_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_source).grid(row=0, column=2, padx=5, pady=5)
        ToolTip(self.source_entry, TOOLTIPS["source_entry"])

        ttk.Label(main_frame, text="Output Folder:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.output_entry = ttk.Entry(main_frame, width=50)
        self.output_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output).grid(row=1, column=2, padx=5, pady=5)
        ToolTip(self.output_entry, TOOLTIPS["output_entry"])

        self.skip_existing_var = tk.BooleanVar(value=False)
        skip_existing_cb = ttk.Checkbutton(main_frame, text="Skip existing files", variable=self.skip_existing_var)
        skip_existing_cb.grid(row=2, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        ToolTip(skip_existing_cb, TOOLTIPS["skip_existing_cb"])

        self.delete_source_var = tk.BooleanVar(value=False)
        delete_source_cb = ttk.Checkbutton(main_frame, text="Delete source files after processing", variable=self.delete_source_var)
        delete_source_cb.grid(row=3, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        ToolTip(delete_source_cb, TOOLTIPS["delete_source_cb"])

        self.exclude_subdirs_var = tk.BooleanVar(value=False)
        exclude_subdirs_cb = ttk.Checkbutton(main_frame, text="Exclude subdirectories", variable=self.exclude_subdirs_var)
        exclude_subdirs_cb.grid(row=4, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        ToolTip(exclude_subdirs_cb, TOOLTIPS["exclude_subdirs_cb"])

    def create_layout_tab(self):
        layout_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(layout_frame, text="Layout")

        ttk.Label(layout_frame, text="Layout:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.layout_var = tk.StringVar(value="FULLSCREEN")
        layout_options = ["WIDESCREEN", "FULLSCREEN", "PERSPECTIVE", "CROSS", "DIAMOND"]
        layout_combo = ttk.Combobox(layout_frame, textvariable=self.layout_var, values=layout_options, state="readonly")
        layout_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ToolTip(layout_combo, TOOLTIPS["layout_combo"])

        ttk.Label(layout_frame, text="Scale:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.scale_entry = ttk.Entry(layout_frame, width=10)
        self.scale_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        ToolTip(self.scale_entry, TOOLTIPS["scale_entry"])

        self.perspective_var = tk.BooleanVar(value=False)
        perspective_cb = ttk.Checkbutton(layout_frame, text="Show side cameras in perspective", variable=self.perspective_var)
        perspective_cb.grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        ToolTip(perspective_cb, TOOLTIPS["perspective_cb"])

        ttk.Label(layout_frame, text="Background Color:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.background_entry = ttk.Entry(layout_frame, width=20)
        self.background_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        self.background_entry.insert(0, "black")
        ToolTip(self.background_entry, TOOLTIPS["background_entry"])

    def create_timestamp_tab(self):
        timestamp_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(timestamp_frame, text="Timestamp")

        self.show_timestamp_var = tk.BooleanVar(value=True)
        show_timestamp_cb = ttk.Checkbutton(timestamp_frame, text="Show timestamp", variable=self.show_timestamp_var)
        show_timestamp_cb.grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        ToolTip(show_timestamp_cb, TOOLTIPS["show_timestamp_cb"])

        ttk.Label(timestamp_frame, text="Horizontal Alignment:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.halign_var = tk.StringVar(value="CENTER")
        halign_options = ["LEFT", "CENTER", "RIGHT"]
        halign_combo = ttk.Combobox(timestamp_frame, textvariable=self.halign_var, values=halign_options, state="readonly")
        halign_combo.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        ToolTip(halign_combo, TOOLTIPS["halign_combo"])

        ttk.Label(timestamp_frame, text="Vertical Alignment:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.valign_var = tk.StringVar(value="BOTTOM")
        valign_options = ["TOP", "MIDDLE", "BOTTOM"]
        valign_combo = ttk.Combobox(timestamp_frame, textvariable=self.valign_var, values=valign_options, state="readonly")
        valign_combo.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        ToolTip(valign_combo, TOOLTIPS["valign_combo"])

        ttk.Label(timestamp_frame, text="Font:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.font_entry = ttk.Entry(timestamp_frame, width=50)
        self.font_entry.grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(timestamp_frame, text="Browse", command=self.browse_font).grid(row=3, column=2, padx=5, pady=5)
        ToolTip(self.font_entry, TOOLTIPS["font_entry"])

        ttk.Label(timestamp_frame, text="Font Size:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.fontsize_entry = ttk.Entry(timestamp_frame, width=10)
        self.fontsize_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        ToolTip(self.fontsize_entry, TOOLTIPS["fontsize_entry"])

        ttk.Label(timestamp_frame, text="Font Color:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.fontcolor_entry = ttk.Entry(timestamp_frame, width=20)
        self.fontcolor_entry.grid(row=5, column=1, sticky="w", padx=5, pady=5)
        self.fontcolor_entry.insert(0, "white")
        ToolTip(self.fontcolor_entry, TOOLTIPS["fontcolor_entry"])

    def create_advanced_tab(self):
        advanced_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(advanced_frame, text="Advanced")

        ttk.Label(advanced_frame, text="Quality:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.quality_var = tk.StringVar(value="LOWER")
        quality_options = ["LOWEST", "LOWER", "LOW", "MEDIUM", "HIGH"]
        quality_combo = ttk.Combobox(advanced_frame, textvariable=self.quality_var, values=quality_options, state="readonly")
        quality_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ToolTip(quality_combo, TOOLTIPS["quality_combo"])

        ttk.Label(advanced_frame, text="Compression:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.compression_var = tk.StringVar(value="medium")
        compression_options = ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"]
        compression_combo = ttk.Combobox(advanced_frame, textvariable=self.compression_var, values=compression_options, state="readonly")
        compression_combo.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        ToolTip(compression_combo, TOOLTIPS["compression_combo"])

        ttk.Label(advanced_frame, text="FPS:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.fps_entry = ttk.Entry(advanced_frame, width=10)
        self.fps_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.fps_entry.insert(0, "24")
        ToolTip(self.fps_entry, TOOLTIPS["fps_entry"])

        ttk.Label(advanced_frame, text="Encoding:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.encoding_var = tk.StringVar(value="x264")
        encoding_options = ["x264", "x265"]
        encoding_combo = ttk.Combobox(advanced_frame, textvariable=self.encoding_var, values=encoding_options, state="readonly")
        encoding_combo.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        ToolTip(encoding_combo, TOOLTIPS["encoding_combo"])

        self.gpu_var = tk.BooleanVar(value=True)
        gpu_cb = ttk.Checkbutton(advanced_frame, text="Use GPU Acceleration", variable=self.gpu_var)
        gpu_cb.grid(row=4, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        ToolTip(gpu_cb, TOOLTIPS["gpu_cb"])

        self.motion_only_var = tk.BooleanVar(value=False)
        motion_only_cb = ttk.Checkbutton(advanced_frame, text="Motion only (fast-forward when no motion)", variable=self.motion_only_var)
        motion_only_cb.grid(row=5, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        ToolTip(motion_only_cb, TOOLTIPS["motion_only_cb"])

    def create_output_tab(self):
        output_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(output_frame, text="Output Options")

        self.merge_var = tk.BooleanVar(value=False)
        merge_cb = ttk.Checkbutton(output_frame, text="Merge video files", variable=self.merge_var)
        merge_cb.grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        ToolTip(merge_cb, TOOLTIPS["merge_cb"])

        ttk.Label(output_frame, text="Merge Group Template:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.merge_template_entry = ttk.Entry(output_frame, width=50)
        self.merge_template_entry.grid(row=1, column=1, padx=5, pady=5)
        ToolTip(self.merge_template_entry, TOOLTIPS["merge_template_entry"])

        ttk.Label(output_frame, text="Merge Timestamp Format:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.merge_timestamp_format_entry = ttk.Entry(output_frame, width=20)
        self.merge_timestamp_format_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.merge_timestamp_format_entry.insert(0, "%Y-%m-%d_%H_%M")
        ToolTip(self.merge_timestamp_format_entry, TOOLTIPS["merge_timestamp_format_entry"])

        self.keep_intermediate_var = tk.BooleanVar(value=False)
        keep_intermediate_cb = ttk.Checkbutton(output_frame, text="Keep intermediate files", variable=self.keep_intermediate_var)
        keep_intermediate_cb.grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        ToolTip(keep_intermediate_cb, TOOLTIPS["keep_intermediate_cb"])

        self.keep_events_var = tk.BooleanVar(value=False)
        keep_events_cb = ttk.Checkbutton(output_frame, text="Keep event files", variable=self.keep_events_var)
        keep_events_cb.grid(row=4, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        ToolTip(keep_events_cb, TOOLTIPS["keep_events_cb"])

        ttk.Label(output_frame, text="Set Movie File Timestamp:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.set_moviefile_timestamp_var = tk.StringVar(value="START")
        moviefile_timestamp_options = ["START", "STOP", "SENTRY", "RENDER"]
        moviefile_timestamp_combo = ttk.Combobox(output_frame, textvariable=self.set_moviefile_timestamp_var, values=moviefile_timestamp_options, state="readonly")
        moviefile_timestamp_combo.grid(row=5, column=1, sticky="ew", padx=5, pady=5)
        ToolTip(moviefile_timestamp_combo, TOOLTIPS["moviefile_timestamp_combo"])

        ttk.Label(output_frame, text="Slow Down:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.slowdown_entry = ttk.Entry(output_frame, width=10)
        self.slowdown_entry.grid(row=6, column=1, sticky="w", padx=5, pady=5)
        ToolTip(self.slowdown_entry, TOOLTIPS["slowdown_entry"])

        ttk.Label(output_frame, text="Speed Up:").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.speedup_entry = ttk.Entry(output_frame, width=10)
        self.speedup_entry.grid(row=7, column=1, sticky="w", padx=5, pady=5)
        ToolTip(self.speedup_entry, TOOLTIPS["speedup_entry"])

        ttk.Label(output_frame, text="Chapter Offset:").grid(row=8, column=0, sticky="w", padx=5, pady=5)
        self.chapter_offset_entry = ttk.Entry(output_frame, width=10)
        self.chapter_offset_entry.grid(row=8, column=1, sticky="w", padx=5, pady=5)
        self.chapter_offset_entry.insert(0, "0")
        ToolTip(self.chapter_offset_entry, TOOLTIPS["chapter_offset_entry"])

    def browse_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, folder)

    def browse_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder)

    def browse_font(self):
        font_file = filedialog.askopenfilename(filetypes=[("TrueType Font", "*.ttf")])
        if font_file:
            self.font_entry.delete(0, tk.END)
            self.font_entry.insert(0, font_file)

    def run_script(self):
        tesla_dashcam_path = "/Applications/tesla_dashcam"

        if not os.path.exists(tesla_dashcam_path):
            messagebox.showerror("Error", f"Cannot find tesla_dashcam at {tesla_dashcam_path}. Please ensure it's installed correctly.")
            return

        command = [tesla_dashcam_path]
        
        # Add source directory as a positional argument
        source_dir = self.source_entry.get()
        if source_dir:
            command.append(source_dir)
        else:
            messagebox.showerror("Error", "Please specify a source directory.")
            return

        # Check for Apple Silicon ffmpeg in path
        ffmpeg_path = shutil.which('ffmpeg')
        if ffmpeg_path:
            # Run ffmpeg to check its version
            try:
                result = subprocess.run([ffmpeg_path, "-version"], capture_output=True, text=True, check=True)
                if "arm64" in result.stdout.lower():
                    print(f"Using Apple Silicon ffmpeg found at: {ffmpeg_path}")
                    command.extend(["--ffmpeg", ffmpeg_path])
                else:
                    print(f"Found ffmpeg, but it's not Apple Silicon version: {ffmpeg_path}")
            except subprocess.CalledProcessError:
                print(f"Error checking ffmpeg version at: {ffmpeg_path}")
        else:
            print("No ffmpeg found in system path. Will use internal version.")

        # Add other options to the command
        command.extend(["--output", self.output_entry.get()])
        command.extend(["--layout", self.layout_var.get()])
        
        if self.skip_existing_var.get():
            command.append("--skip_existing")
        
        if self.delete_source_var.get():
            command.append("--delete_source")
        
        if self.exclude_subdirs_var.get():
            command.append("--exclude_subdirs")
        
        if self.scale_entry.get():
            command.extend(["--scale", self.scale_entry.get()])
        
        if self.perspective_var.get():
            command.append("--perspective")
        
        if self.background_entry.get():
            command.extend(["--background", self.background_entry.get()])
        
        if not self.show_timestamp_var.get():
            command.append("--no-timestamp")
        else:
            command.extend(["--halign", self.halign_var.get()])
            command.extend(["--valign", self.valign_var.get()])
        
        if self.font_entry.get():
            command.extend(["--font", self.font_entry.get()])
        
        if self.fontsize_entry.get():
            command.extend(["--fontsize", self.fontsize_entry.get()])
        
        if self.fontcolor_entry.get():
            command.extend(["--fontcolor", self.fontcolor_entry.get()])
        
        command.extend(["--quality", self.quality_var.get()])
        command.extend(["--compression", self.compression_var.get()])
        command.extend(["--fps", self.fps_entry.get()])
        command.extend(["--encoding", self.encoding_var.get()])
        
        if self.gpu_var.get():
            command.append("--gpu")
        else:
            command.append("--no-gpu")
        
        if self.motion_only_var.get():
            command.append("--motion_only")

        if self.merge_var.get():
            command.append("--merge")
            if self.merge_template_entry.get():
                command.extend([self.merge_template_entry.get()])
            command.extend(["--merge_timestamp_format", self.merge_timestamp_format_entry.get()])

        if self.keep_intermediate_var.get():
            command.append("--keep-intermediate")

        if self.keep_events_var.get():
            command.append("--keep-events")

        command.extend(["--set_moviefile_timestamp", self.set_moviefile_timestamp_var.get()])

        if self.slowdown_entry.get():
            command.extend(["--slowdown", self.slowdown_entry.get()])

        if self.speedup_entry.get():
            command.extend(["--speedup", self.speedup_entry.get()])

        if self.chapter_offset_entry.get():
            command.extend(["--chapter_offset", self.chapter_offset_entry.get()])

        try:
            print(f"Executing command: {' '.join(command)}")
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"Command output:\n{result.stdout}")
            messagebox.showinfo("Success", "Video creation completed successfully!")
        except subprocess.CalledProcessError as e:
            error_message = f"An error occurred while running tesla_dashcam:\n\n{e.stderr}"
            print(error_message)
            messagebox.showerror("Error", error_message)
        except Exception as e:
            error_message = f"An unexpected error occurred:\n\n{str(e)}"
            print(error_message)
            messagebox.showerror("Error", error_message)

def main():
    root = tk.Tk()
    app = TeslaDashcamGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()