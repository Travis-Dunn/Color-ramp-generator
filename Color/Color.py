import tkinter as tk
from tkinter import ttk
import colorsys


def convert_to_hex(h, s, v):
    s = s/100
    v = v/100
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = int(h60)
    hi = int(h60f % 6)
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0:
        r, g, b = v, t, p
    elif hi == 1:
        r, g, b = q, v, p
    elif hi == 2:
        r, g, b = p, v, t
    elif hi == 3:
        r, g, b = p, q, v
    elif hi == 4:
        r, g, b = t, p, v
    elif hi == 5:
        r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def display_color():
    h = float(hue_entry.get())
    s = float(saturation_entry.get())
    v = float(value_entry.get())

    hex_code = convert_to_hex(h, s, v)
    hex_label.config(text=hex_code)
    canvas.create_oval(10, 10, 90, 90, fill=hex_code)

def convert_to_hsv(hex_code):
    r = int(hex_code[1:3], 16) / 255.0
    g = int(hex_code[3:5], 16) / 255.0
    b = int(hex_code[5:7], 16) / 255.0
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h = int(h * 360)
    s = int(s * 100)
    v = int(v * 100)
    return (h, s, v)

root = tk.Tk()
root.title("Color Converter")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

hue_entry = ttk.Entry(mainframe)
saturation_entry = ttk.Entry(mainframe)
value_entry = ttk.Entry(mainframe)
hex_entry = ttk.Entry(mainframe)

hue_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))
saturation_entry.grid(column=2, row=2, sticky=(tk.W, tk.E))
value_entry.grid(column=2, row=3, sticky=(tk.W, tk.E))
hex_entry.grid(column=2, row=4, sticky=(tk.W, tk.E))

ttk.Label(mainframe, text="Hue:").grid(column=1, row=1, sticky=tk.W)
ttk.Label(mainframe, text="Saturation:").grid(column=1, row=2, sticky=tk.W)
ttk.Label(mainframe, text="Value:").grid(column=1, row=3, sticky=tk.W)
ttk.Label(mainframe, text="Hex:").grid(column=1, row=4, sticky=tk.W)

hex_label = ttk.Label(mainframe, text="")
hex_label.grid(column=2, row=4, sticky=tk.W)

canvas = tk.Canvas(mainframe, bg='white', width=110, height=110)
canvas.grid(column=3, row=1, rowspan=4, sticky=(tk.W, tk.E))

ttk.Button(mainframe, text="Display Color", command=display_color).grid(column=2, row=5, sticky=tk.W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

hue_entry.focus()
root.bind('<Return>', display_color)

root.mainloop()
