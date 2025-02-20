import sys
import os
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import pyperclip  # For clipboard functionality

def midi_to_lua_table(midi_file_path):
    # Check if the file exists
    if not os.path.isfile(midi_file_path):
        return f"Error: File '{midi_file_path}' not found."
    
    with open(midi_file_path, 'rb') as f:
        data = f.read()
    
    # Convert binary data to a Lua string format
    lua_string = []
    
    for byte in data:
        if 32 <= byte <= 126:  # Printable ASCII characters
            lua_string.append(chr(byte))
        else:
            lua_string.append(f"\\{byte}")
    
    # Create Lua code
    lua_code = ''.join(lua_string)
    return lua_code, len(data)

def on_drop(event):
    file_path = event.data.strip('{}')  # Remove curly braces from the file path
    if not file_path.lower().endswith('.mid'):
        status_label.config(text="Error: Please drop a valid MIDI file (.mid).")
        return
    
    try:
        lua_code, total_bytes = midi_to_lua_table(file_path)
        status_label.config(text=f"File: {os.path.basename(file_path)}\nTotal bytes: {total_bytes}")
        
        # Copy to clipboard automatically
        pyperclip.copy(lua_code)
        status_label.config(text=status_label.cget("text") + "\nCopied to clipboard!")
    except Exception as e:
        status_label.config(text=f"Error: {e}")

# GUI Setup
root = TkinterDnD.Tk()
root.title("MIDI to Lua Table Converter")
root.geometry("400x200")
root.configure(bg="#2E3440")
root.attributes('-topmost', True)

# Drag-and-Drop Area
drop_frame = tk.Frame(root, bg="#3B4252", bd=2, relief=tk.RAISED)
drop_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

drop_label = tk.Label(drop_frame, text="Drag and Drop MIDI File Here", bg="#3B4252", fg="#ECEFF4", font=("Arial", 12))
drop_label.pack(pady=50)

# Status Label
status_label = tk.Label(root, text="", bg="#2E3440", fg="#ECEFF4", font=("Arial", 10))
status_label.pack(pady=10)

# Enable Drag-and-Drop
drop_frame.drop_target_register(DND_FILES)
drop_frame.dnd_bind('<<Drop>>', on_drop)

# Run the GUI
root.mainloop()