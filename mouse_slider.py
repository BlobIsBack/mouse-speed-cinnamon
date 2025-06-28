#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import subprocess
import sys

class MouseSpeedController:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Speed Controller")
        self.root.geometry("350x300")
        self.root.resizable(False, False)
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title label
        title_label = ttk.Label(main_frame, text="Mouse Speed Setting", 
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Current value label
        self.value_label = ttk.Label(main_frame, text="Current: 0.0", 
                                    font=("Arial", 12))
        self.value_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # Scale (slider) with 20 notches from -1 to 1
        self.scale = tk.Scale(main_frame, from_=-1.0, to=1.0, 
                             orient=tk.HORIZONTAL, length=300,
                             resolution=0.1,
                             command=self.on_scale_change)
        self.scale.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Min/Max labels
        ttk.Label(main_frame, text="-1.0\n(Slower)").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(main_frame, text="1.0\n(Faster)").grid(row=3, column=1, sticky=tk.E)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Apply button
        self.apply_button = ttk.Button(button_frame, text="Apply Setting", 
                                      command=self.apply_setting)
        self.apply_button.grid(row=0, column=0, padx=5)
        
        # Reset button
        self.reset_button = ttk.Button(button_frame, text="Reset to 0", 
                                      command=self.reset_setting)
        self.reset_button.grid(row=0, column=1, padx=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="", foreground="green")
        self.status_label.grid(row=5, column=0, columnspan=2)
        
        # Load current setting
        self.load_current_setting()
        
    def on_scale_change(self, value):
        """Update the value label when slider moves"""
        self.value_label.config(text=f"Current: {float(value):.1f}")
        
    def load_current_setting(self):
        """Load the current gsettings value"""
        try:
            result = subprocess.run(['gsettings', 'get', 
                                   'org.cinnamon.desktop.peripherals.mouse', 'speed'],
                                  capture_output=True, text=True, check=True)
            current_value = float(result.stdout.strip())
            self.scale.set(current_value)
            self.value_label.config(text=f"Current: {current_value:.1f}")
            self.status_label.config(text="Loaded current setting", foreground="blue")
        except subprocess.CalledProcessError:
            self.status_label.config(text="Error: Could not read current setting", 
                                   foreground="red")
        except (ValueError, FileNotFoundError):
            self.status_label.config(text="Error: gsettings not found or invalid value", 
                                   foreground="red")
            
    def apply_setting(self):
        """Apply the current slider value to gsettings"""
        value = self.scale.get()
        try:
            subprocess.run(['gsettings', 'set', 
                          'org.cinnamon.desktop.peripherals.mouse', 'speed', 
                          str(value)], check=True)
            self.status_label.config(text=f"Applied: {value:.1f}", foreground="green")
        except subprocess.CalledProcessError:
            self.status_label.config(text="Error: Failed to apply setting", 
                                   foreground="red")
        except FileNotFoundError:
            self.status_label.config(text="Error: gsettings command not found", 
                                   foreground="red")
            
    def reset_setting(self):
        """Reset slider and setting to 0"""
        self.scale.set(0.0)
        self.value_label.config(text="Current: 0.0")
        self.apply_setting()

def main():
    root = tk.Tk()
    app = MouseSpeedController(root)
    root.mainloop()

if __name__ == "__main__":
    main()