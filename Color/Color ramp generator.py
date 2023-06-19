import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
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

# Relative luminance using ITU BT. 709 spectral weights and accounting for gamma correction
def contrast_ratio(color1, color2):
    if color1[0] == "#":
        color1 = color1[1:]
    if color2[0] == "#":
        color2 = color2[1:]     

    def get_relative_luminance(hex_color):
        # Convert hex color to RGB values
        rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Convert RGB values to sRGB values
        srgb_color = []
        for c in rgb_color:
            srgb_c = c / 255
            if srgb_c <= 0.03928:
                srgb_c = srgb_c / 12.92
            else:
                srgb_c = ((srgb_c + 0.055) / 1.055) ** 2.4
            srgb_color.append(srgb_c)
        
        # Calculate relative luminance
        r, g, b = srgb_color
        relative_luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
        
        return relative_luminance
    
    l1 = get_relative_luminance(color1)
    l2 = get_relative_luminance(color2)
    if l1 > l2:
        return (l1 + 0.05) / (l2 + 0.05)
    else:
        return (l2 + 0.05) / (l1 + 0.05)

# Relative luminance using ITU BT. 601 spectral weights and accounting for gamma correction
def contrast_ratio1(color1, color2):
    if color1[0] == "#":
        color1 = color1[1:]
    if color2[0] == "#":
        color2 = color2[1:]    

    def get_relative_luminance(hex_color):
        # Convert hex color to RGB values
        rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Convert RGB values to sRGB values
        srgb_color = []
        for c in rgb_color:
            srgb_c = c / 255
            if srgb_c <= 0.03928:
                srgb_c = srgb_c / 12.92
            else:
                srgb_c = ((srgb_c + 0.055) / 1.055) ** 2.4
            srgb_color.append(srgb_c)
        
        # Calculate relative luminance
        r, g, b = srgb_color
        relative_luminance = 0.299 * r + 0.587 * g + 0.114 * b
        
        return relative_luminance
    
    l1 = get_relative_luminance(color1)
    l2 = get_relative_luminance(color2)
    if l1 > l2:
        return (l1 + 0.05) / (l2 + 0.05)
    else:
        return (l2 + 0.05) / (l1 + 0.05)

def increment_color(hue, saturation, value, dHue, dSaturation, dValue):
    scalar = 1
    new_hue = hue + dHue * scalar
    new_saturation = saturation + dSaturation * scalar
    new_value = value + dValue * scalar

    while True:
        if int(abs(hue - new_hue)) > 1 or int(abs(saturation - new_saturation)) > 1 or int(abs(value - new_value)) > 1:
            scalar *= 0.5
            new_hue = hue + dHue * scalar
            new_saturation = saturation + dSaturation * scalar
            new_value = value + dValue * scalar
        elif int(abs(hue - new_hue)) < 1 and int(abs(saturation - new_saturation)) < 1 and int(abs(value - new_value)) < 1:
            scalar *= 1.5
            new_hue = hue + dHue * scalar
            new_saturation = saturation + dSaturation * scalar
            new_value = value + dValue * scalar
        else:
            if new_hue > 360:
                new_hue = new_hue - 360
            if new_hue < 0:
                new_hue = new_hue + 360
            if new_saturation > 100:
                new_saturation = 100
            if new_saturation < 0:
                new_saturation = 0
            if new_value > 100:
                new_value = 100
            if new_value < 0:
                new_value = 0
            return new_hue, new_saturation, new_value
            
   
        
def convert_to_hsv(hex_code):
    r = int(hex_code[1:3], 16) / 255.0
    g = int(hex_code[3:5], 16) / 255.0
    b = int(hex_code[5:7], 16) / 255.0
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h = int(h * 360)
    s = int(s * 100)
    v = int(v * 100)
    return (h, s, v)

def display_color():     
    if hue_entry.get() != "":
        h = float(hue_entry.get())
        s = float(saturation_entry.get())
        v = float(value_entry.get())
        dh = float(delta_hue.get())
        ds = float(delta_saturation.get())
        dv = float(delta_value.get())
        tcr = float(target_contrast.get())
        if h >= 0 and h <= 360 and s > 0 and s <= 100 and v > 0 and v <= 100:
            #0
            hex_code = convert_to_hex(h, s, v)
            hex_label.config(text=hex_code)                  
            canvas.create_rectangle(0, 0, 110, 110, fill=hex_code, outline="")  
            formatted_string = f"{h} | {s} | {v}"
            HSV_label_0.config(text=formatted_string)
            #0 second row
            hex_label8.config(text=hex_code)                  
            canvas8.create_rectangle(0, 0, 110, 110, fill=hex_code, outline="")
            HSV_label_8.config(text=formatted_string)
            
            #1
            
            hex1_h, hex1_s, hex1_v = increment_color(h, s, v, dh, ds, dv)
            hex1 = convert_to_hex(hex1_h, hex1_s, hex1_v)
            contrast = contrast_ratio(hex_code, hex1)
            counter = 0
            while contrast < tcr:                
                hex1_h, hex1_s, hex1_v = increment_color(hex1_h, hex1_s, hex1_v, dh, ds, dv)
                hex1 = convert_to_hex(hex1_h, hex1_s, hex1_v)
                contrast = contrast_ratio(hex_code, hex1)                
                counter += 1
                if counter > 1000:
                    hex1 = "#FFFFFF"
                    hex_label1.config(text=hex1)
                    canvas1.create_rectangle(0, 0, 110, 110, fill=hex1, outline="")
                    formatted_string = f"{hex1_h} | {hex1_s} | {hex1_v}"
                    HSV_label_1.config(text=formatted_string)
                    contrast = 21 

            hex_label1.config(text=hex1)
            canvas1.create_rectangle(0, 0, 110, 110, fill=hex1, outline="")
            formatted_string = f"{hex1_h} | {hex1_s} | {hex1_v}"
            HSV_label_1.config(text=formatted_string)
            
            #1 second row
            
            hex1a_h, hex1a_s, hex1a_v = increment_color(h, s, v, dh, ds, dv)
            hex1a = convert_to_hex(hex1a_h, hex1a_s, hex1a_v)
            contrast = contrast_ratio1(hex_code, hex1a)
            counter = 0
            while contrast < tcr:                
                hex1a_h, hex1a_s, hex1a_v = increment_color(hex1a_h, hex1a_s, hex1a_v, dh, ds, dv)
                hex1a = convert_to_hex(hex1a_h, hex1a_s, hex1a_v)
                contrast = contrast_ratio1(hex_code, hex1a)                
                counter += 1
                if counter > 1000:
                    hex1a = "#FFFFFF"
                    hex_label9.config(text=hex1a)
                    canvas9.create_rectangle(0, 0, 110, 110, fill=hex1a, outline="")
                    formatted_string = f"{hex1a_h} | {hex1a_s} | {hex1a_v}"
                    HSV_label_9.config(text=formatted_string)
                    contrast = 21

            hex_label9.config(text=hex1a)
            canvas9.create_rectangle(0, 0, 110, 110, fill=hex1a, outline="")
            formatted_string = f"{hex1a_h} | {hex1a_s} | {hex1a_v}"
            HSV_label_9.config(text=formatted_string)
            #2

            hex2_h, hex2_s, hex2_v = increment_color(hex1_h, hex1_s, hex1_v, dh, ds, dv)
            hex2 = convert_to_hex(hex2_h, hex2_s, hex2_v)
            contrast = contrast_ratio(hex1, hex2)
            counter = 0
            while contrast < tcr:
                hex2_h, hex2_s, hex2_v = increment_color(hex2_h, hex2_s, hex2_v, dh, ds, dv)
                hex2 = convert_to_hex(hex2_h, hex2_s, hex2_v)
                contrast = contrast_ratio(hex1, hex2)
                counter += 1
                if counter > 1000:
                    hex2 = "#FFFFFF"
                    hex_label2.config(text=hex2)
                    canvas2.create_rectangle(0, 0, 110, 110, fill=hex2, outline="")
                    formatted_string = f"{hex2_h} | {hex2_s} | {hex2_v}"
                    HSV_label_2.config(text=formatted_string)
                    contrast = 21
            hex_label2.config(text=hex2)
            canvas2.create_rectangle(0, 0, 110, 110, fill=hex2, outline="")
            formatted_string = f"{hex2_h} | {hex2_s} | {hex2_v}"
            HSV_label_2.config(text=formatted_string)
            
            #2 second row

            hex2a_h, hex2a_s, hex2a_v = increment_color(hex1a_h, hex1a_s, hex1_v, dh, ds, dv)
            hex2a = convert_to_hex(hex2a_h, hex2a_s, hex2a_v)
            contrast = contrast_ratio1(hex1a, hex2a)
            counter = 0
            while contrast < tcr:
                hex2a_h, hex2a_s, hex2a_v = increment_color(hex2a_h, hex2a_s, hex2a_v, dh, ds, dv)
                hex2a = convert_to_hex(hex2a_h, hex2a_s, hex2a_v)
                contrast = contrast_ratio1(hex1a, hex2a)
                counter += 1
                if counter > 1000:
                    hex2a = "#FFFFFF"
                    hex_label10.config(text=hex2a)
                    canvas10.create_rectangle(0, 0, 110, 110, fill=hex2a, outline="")
                    formatted_string = f"{hex2a_h} | {hex2a_s} | {hex2a_v}"
                    HSV_label_10.config(text=formatted_string)
                    contrast = 21
            hex_label10.config(text=hex2a)
            canvas10.create_rectangle(0, 0, 110, 110, fill=hex2a, outline="")
            formatted_string = f"{hex2a_h} | {hex2a_s} | {hex2a_v}"
            HSV_label_10.config(text=formatted_string)
            #3

            hex3_h, hex3_s, hex3_v = increment_color(hex2_h, hex2_s, hex2_v, dh, ds, dv)
            hex3 = convert_to_hex(hex3_h, hex3_s, hex3_v)
            contrast = contrast_ratio(hex2, hex3)
            counter = 0
            while contrast < tcr:
                hex3_h, hex3_s, hex3_v = increment_color(hex3_h, hex3_s, hex3_v, dh, ds, dv)
                hex3 = convert_to_hex(hex3_h, hex3_s, hex3_v)
                contrast = contrast_ratio(hex2, hex3)
                counter += 1
                if counter > 1000:
                    hex3 = "#FFFFFF"
                    hex_label3.config(text=hex3)
                    canvas3.create_rectangle(0, 0, 110, 110, fill=hex3, outline="")
                    formatted_string = f"{hex3_h} | {hex3_s} | {hex3_v}"
                    HSV_label_3.config(text=formatted_string)
                    contrast = 21
            hex_label3.config(text=hex3)
            canvas3.create_rectangle(0, 0, 110, 110, fill=hex3, outline="")
            formatted_string = f"{hex3_h} | {hex3_s} | {hex3_v}"
            HSV_label_3.config(text=formatted_string)
            
            #3 second row

            hex3a_h, hex3a_s, hex3a_v = increment_color(hex2a_h, hex2a_s, hex2a_v, dh, ds, dv)
            hex3a = convert_to_hex(hex3a_h, hex3a_s, hex3a_v)
            contrast = contrast_ratio1(hex2a, hex3a)
            counter = 0
            while contrast < tcr:
                hex3_ha, hex3a_s, hex3a_v = increment_color(hex3a_h, hex3a_s, hex3_v, dh, ds, dv)
                hex3a = convert_to_hex(hex3a_h, hex3a_s, hex3a_v)
                contrast = contrast_ratio1(hex2a, hex3a)
                counter += 1
                if counter > 1000:
                    hex3a = "#FFFFFF"
                    hex_label11.config(text=hex3a)
                    canvas11.create_rectangle(0, 0, 110, 110, fill=hex3a, outline="")
                    formatted_string = f"{hex3a_h} | {hex3a_s} | {hex3a_v}"
                    HSV_label_11.config(text=formatted_string)
                    contrast = 21
            hex_label11.config(text=hex3a)
            canvas11.create_rectangle(0, 0, 110, 110, fill=hex3a, outline="")
            formatted_string = f"{hex3a_h} | {hex3a_s} | {hex3a_v}"
            HSV_label_11.config(text=formatted_string)
            #4

            hex4_h, hex4_s, hex4_v = increment_color(hex3_h, hex3_s, hex3_v, dh, ds, dv)
            hex4 = convert_to_hex(hex4_h, hex4_s, hex4_v)
            contrast = contrast_ratio(hex3, hex4)
            counter = 0
            while contrast < tcr:
                hex4_h, hex4_s, hex4_v = increment_color(hex4_h, hex4_s, hex4_v, dh, ds, dv)
                hex4 = convert_to_hex(hex4_h, hex4_s, hex4_v)
                contrast = contrast_ratio(hex3, hex4)
                counter += 1
                if counter > 1000:
                    hex4 = "#FFFFFF"
                    hex_label4.config(text=hex4)
                    canvas4.create_rectangle(0, 0, 110, 110, fill=hex4, outline="")
                    formatted_string = f"{hex4_h} | {hex4_s} | {hex4_v}"
                    HSV_label_4.config(text=formatted_string)
                    contrast = 21
            hex_label4.config(text=hex4)
            canvas4.create_rectangle(0, 0, 110, 110, fill=hex4, outline="")
            formatted_string = f"{hex4_h} | {hex4_s} | {hex4_v}"
            HSV_label_4.config(text=formatted_string)
            
            #4 second row

            hex4a_h, hex4a_s, hex4a_v = increment_color(hex3a_h, hex3a_s, hex3a_v, dh, ds, dv)
            hex4a = convert_to_hex(hex4a_h, hex4a_s, hex4a_v)
            contrast = contrast_ratio1(hex3a, hex4a)
            counter = 0
            while contrast < tcr:
                hex4a_h, hex4a_s, hex4a_v = increment_color(hex4a_h, hex4a_s, hex4a_v, dh, ds, dv)
                hex4a = convert_to_hex(hex4a_h, hex4a_s, hex4a_v)
                contrast = contrast_ratio1(hex3a, hex4a)
                counter += 1
                if counter > 1000:
                    hex4a = "#FFFFFF"
                    hex_label12.config(text=hex4a)
                    canvas12.create_rectangle(0, 0, 110, 110, fill=hex4a, outline="")
                    formatted_string = f"{hex4a_h} | {hex4a_s} | {hex4a_v}"
                    HSV_label_12.config(text=formatted_string)
                    contrast = 21
            hex_label12.config(text=hex4a)
            canvas12.create_rectangle(0, 0, 110, 110, fill=hex4a, outline="")
            formatted_string = f"{hex4a_h} | {hex4a_s} | {hex4a_v}"
            HSV_label_12.config(text=formatted_string)

            #5

            hex5_h, hex5_s, hex5_v = increment_color(hex4_h, hex4_s, hex4_v, dh, ds, dv)
            hex5 = convert_to_hex(hex5_h, hex5_s, hex5_v)
            contrast = contrast_ratio(hex4, hex5)
            counter = 0
            while contrast < tcr:
                hex5_h, hex5_s, hex5_v = increment_color(hex5_h, hex5_s, hex5_v, dh, ds, dv)
                hex5 = convert_to_hex(hex5_h, hex5_s, hex5_v)
                contrast = contrast_ratio(hex4, hex5)
                counter += 1
                if counter > 1000:
                    hex5 = "#FFFFFF"
                    hex_label5.config(text=hex5)
                    canvas5.create_rectangle(0, 0, 110, 110, fill=hex5, outline="")
                    formatted_string = f"{hex5_h} | {hex5_s} | {hex5_v}"
                    HSV_label_5.config(text=formatted_string)
                    contrast = 21
            hex_label5.config(text=hex5)
            canvas5.create_rectangle(0, 0, 110, 110, fill=hex5, outline="") 
            formatted_string = f"{hex5_h} | {hex5_s} | {hex5_v}"
            HSV_label_5.config(text=formatted_string)
            
            #5 second row

            hex5a_h, hex5a_s, hex5a_v = increment_color(hex4a_h, hex4a_s, hex4a_v, dh, ds, dv)
            hex5a = convert_to_hex(hex5a_h, hex5a_s, hex5a_v)
            contrast = contrast_ratio1(hex4a, hex5a)
            counter = 0
            while contrast < tcr:
                hex5a_h, hex5a_s, hex5a_v = increment_color(hex5a_h, hex5a_s, hex5a_v, dh, ds, dv)
                hex5a = convert_to_hex(hex5a_h, hex5a_s, hex5a_v)
                contrast = contrast_ratio1(hex4a, hex5a)
                counter += 1
                if counter > 1000:
                    hex5a = "#FFFFFF"
                    hex_label13.config(text=hex5a)
                    canvas13.create_rectangle(0, 0, 110, 110, fill=hex5a, outline="")
                    formatted_string = f"{hex5a_h} | {hex5a_s} | {hex5a_v}"
                    HSV_label_13.config(text=formatted_string)
                    contrast = 21
            hex_label13.config(text=hex5a)
            canvas13.create_rectangle(0, 0, 110, 110, fill=hex5a, outline="")
            formatted_string = f"{hex5a_h} | {hex5a_s} | {hex5a_v}"
            HSV_label_13.config(text=formatted_string)

            #6

            hex6_h, hex6_s, hex6_v = increment_color(hex5_h, hex5_s, hex5_v, dh, ds, dv)
            hex6 = convert_to_hex(hex6_h, hex6_s, hex6_v)
            contrast = contrast_ratio(hex5, hex6)
            counter = 0
            while contrast < tcr:
                hex6_h, hex6_s, hex6_v = increment_color(hex6_h, hex6_s, hex6_v, dh, ds, dv)
                hex6 = convert_to_hex(hex6_h, hex6_s, hex6_v)
                contrast = contrast_ratio(hex5, hex6)
                counter += 1
                if counter > 1000:
                    hex6 = "#FFFFFF"
                    hex_label6.config(text=hex6)
                    canvas6.create_rectangle(0, 0, 110, 110, fill=hex6, outline="")
                    formatted_string = f"{hex6_h} | {hex6_s} | {hex6_v}"
                    HSV_label_6.config(text=formatted_string)
                    contrast = 21
            hex_label6.config(text=hex6)                           
            canvas6.create_rectangle(0, 0, 110, 110, fill=hex6, outline="")
            formatted_string = f"{hex6_h} | {hex6_s} | {hex6_v}"
            HSV_label_6.config(text=formatted_string)

            #6 second row

            hex6a_h, hex6a_s, hex6a_v = increment_color(hex5a_h, hex5a_s, hex5a_v, dh, ds, dv)
            hex6a = convert_to_hex(hex6a_h, hex6a_s, hex6a_v)
            contrast = contrast_ratio1(hex5a, hex6a)
            counter = 0
            while contrast < tcr:
                hex6a_h, hex6a_s, hex6a_v = increment_color(hex6a_h, hex6a_s, hex6a_v, dh, ds, dv)
                hex6a = convert_to_hex(hex6a_h, hex6a_s, hex6a_v)
                contrast = contrast_ratio1(hex5a, hex6a)
                counter += 1
                if counter > 1000:
                    hex6a = "#FFFFFF"
                    hex_label14.config(text=hex6a)
                    canvas14.create_rectangle(0, 0, 110, 110, fill=hex6a, outline="")
                    formatted_string = f"{hex6a_h} | {hex6a_s} | {hex6a_v}"
                    HSV_label_14.config(text=formatted_string)
                    contrast = 21
            hex_label14.config(text=hex6a)                           
            canvas14.create_rectangle(0, 0, 110, 110, fill=hex6a, outline="")
            formatted_string = f"{hex6a_h} | {hex6a_s} | {hex6a_v}"
            HSV_label_14.config(text=formatted_string)
            

            #7

            hex7_h, hex7_s, hex7_v = increment_color(hex6_h, hex6_s, hex6_v, dh, ds, dv)
            hex7 = convert_to_hex(hex7_h, hex7_s, hex7_v)
            contrast = contrast_ratio(hex6, hex7)
            counter = 0
            while contrast < tcr:
                hex7_h, hex7_s, hex7_v = increment_color(hex7_h, hex7_s, hex7_v, dh, ds, dv)
                hex7 = convert_to_hex(hex7_h, hex7_s, hex7_v)
                contrast = contrast_ratio(hex6, hex7)
                counter += 1
                if counter > 1000:
                    hex7 = "#FFFFFF"
                    hex_label7.config(text=hex7)
                    canvas7.create_rectangle(0, 0, 110, 110, fill=hex7, outline="")
                    formatted_string = f"{hex7_h} | {hex7_s} | {hex7_v}"
                    HSV_label_7.config(text=formatted_string)
                    contrast = 21
            hex_label7.config(text=hex7)
            canvas7.create_rectangle(0, 0, 110, 110, fill=hex7, outline="")  
            formatted_string = f"{hex7_h} | {hex7_s} | {hex7_v}"
            HSV_label_7.config(text=formatted_string)
            
            #7 second row

            hex7a_h, hex7a_s, hex7a_v = increment_color(hex6a_h, hex6a_s, hex6a_v, dh, ds, dv)
            hex7a = convert_to_hex(hex7a_h, hex7a_s, hex7a_v)
            contrast = contrast_ratio1(hex6a, hex7a)
            counter = 0
            while contrast < tcr:
                hex7_ha, hex7a_s, hex7a_v = increment_color(hex7a_h, hex7a_s, hex7a_v, dh, ds, dv)
                hex7a = convert_to_hex(hex7a_h, hex7a_s, hex7a_v)
                contrast = contrast_ratio1(hex6a, hex7a)
                counter += 1
                if counter > 1000:
                    hex7a = "#FFFFFF"
                    hex_label15.config(text=hex7a)
                    canvas15.create_rectangle(0, 0, 110, 110, fill=hex7a, outline="")
                    formatted_string = f"{hex7a_h} | {hex7a_s} | {hex7a_v}"
                    HSV_label_15.config(text=formatted_string)
                    contrast = 21
            hex_label15.config(text=hex7a)
            canvas15.create_rectangle(0, 0, 110, 110, fill=hex7a, outline="")
            formatted_string = f"{hex7a_h} | {hex7a_s} | {hex7a_v}"
            HSV_label_15.config(text=formatted_string)

def copy_to_clipboard(hex):
    root.clipboard_clear()
    root.clipboard_append(hex)

def show_about():
    messagebox.showinfo("About", "This program is freeware, use as permitted in GNU GPL v3.0.\n\nLeave bug reports or whatever at https://github.com/Travis-Dunn/Color-ramp-generator/ \n\nMade by Travis Dunn 2023")

while True:
    root = tk.Tk()
    root.title("Color ramp generator 1.01")
    
    mainframe = ttk.Frame(root, padding="0 0 0 0")
    mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
    root.columnconfigure(0, weight=1)    
    root.rowconfigure(0, weight=1)        
    
    hue_entry = ttk.Entry(mainframe)
    saturation_entry = ttk.Entry(mainframe)
    value_entry = ttk.Entry(mainframe)
    target_contrast = ttk.Entry(mainframe)
    delta_hue = ttk.Entry(mainframe)
    delta_saturation = ttk.Entry(mainframe)
    delta_value = ttk.Entry(mainframe)    
    
    hue_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))
    saturation_entry.grid(column=2, row=2, sticky=(tk.W, tk.E))
    value_entry.grid(column=2, row=3, sticky=(tk.W, tk.E))    
    target_contrast.grid(column=2, row=4, sticky=(tk.W, tk.E))
    delta_hue.grid(column=2, row=5, sticky=(tk.W, tk.E))
    delta_saturation.grid(column=2, row=6, sticky=(tk.W, tk.E))
    delta_value.grid(column=2, row=7, sticky=(tk.W, tk.E))
    
    ttk.Label(mainframe, text="Hue:").grid(column=1, row=1, sticky=tk.W)
    ttk.Label(mainframe, text="Saturation:").grid(column=1, row=2, sticky=tk.W)
    ttk.Label(mainframe, text="Value:").grid(column=1, row=3, sticky=tk.W)    
    ttk.Label(mainframe, text="Target contrast:").grid(column=1, row=4, sticky=tk.W)
    ttk.Label(mainframe, text="Delta hue:").grid(column=1, row=5, sticky=tk.W)
    ttk.Label(mainframe, text="Delta saturation:").grid(column=1, row=6, sticky=tk.W)
    ttk.Label(mainframe, text="Delta value:").grid(column=1, row=7, sticky=tk.W)
    ttk.Label(mainframe, text="Relative luminance using ITU BT. 709 spectral weights and accounting for gamma correction").grid(column=3, row=1, columnspan=7, sticky="w")
    ttk.Label(mainframe, text="Relative luminance using ITU BT. 601 spectral weights and accounting for gamma correction").grid(column=3, row=8, columnspan=7, sticky="w")
    
    hex_label = ttk.Label(mainframe, text="")    
    hex_label1 = ttk.Label(mainframe, text="") 
    hex_label2 = ttk.Label(mainframe, text="") 
    hex_label3 = ttk.Label(mainframe, text="") 
    hex_label4 = ttk.Label(mainframe, text="") 
    hex_label5 = ttk.Label(mainframe, text="") 
    hex_label6 = ttk.Label(mainframe, text="") 
    hex_label7 = ttk.Label(mainframe, text="")    
    hex_label8 = ttk.Label(mainframe, text="") 
    hex_label9 = ttk.Label(mainframe, text="") 
    hex_label10 = ttk.Label(mainframe, text="")
    hex_label11 = ttk.Label(mainframe, text="")
    hex_label12 = ttk.Label(mainframe, text="")
    hex_label13 = ttk.Label(mainframe, text="")
    hex_label14 = ttk.Label(mainframe, text="")
    hex_label15 = ttk.Label(mainframe, text="")   

    # new stuff
    HSV_label_0  = ttk.Label(mainframe, text="null")
    HSV_label_1  = ttk.Label(mainframe, text="null")
    HSV_label_2  = ttk.Label(mainframe, text="null")
    HSV_label_3  = ttk.Label(mainframe, text="null")
    HSV_label_4  = ttk.Label(mainframe, text="null")
    HSV_label_5  = ttk.Label(mainframe, text="null")
    HSV_label_6  = ttk.Label(mainframe, text="null")
    HSV_label_7  = ttk.Label(mainframe, text="null")
    HSV_label_8  = ttk.Label(mainframe, text="null")
    HSV_label_9  = ttk.Label(mainframe, text="null")
    HSV_label_10 = ttk.Label(mainframe, text="null")
    HSV_label_11 = ttk.Label(mainframe, text="null")
    HSV_label_12 = ttk.Label(mainframe, text="null")
    HSV_label_13 = ttk.Label(mainframe, text="null")
    HSV_label_14 = ttk.Label(mainframe, text="null")
    HSV_label_15 = ttk.Label(mainframe, text="null")

    HSV_label_0 .grid(column=3 , row=6 , sticky=tk.W)
    HSV_label_1 .grid(column=4 , row=6 , sticky=tk.W)
    HSV_label_2 .grid(column=5 , row=6 , sticky=tk.W)
    HSV_label_3 .grid(column=6 , row=6 , sticky=tk.W)
    HSV_label_4 .grid(column=7 , row=6 , sticky=tk.W)
    HSV_label_5 .grid(column=8 , row=6 , sticky=tk.W)
    HSV_label_6 .grid(column=9 , row=6 , sticky=tk.W)
    HSV_label_7 .grid(column=10, row=6 , sticky=tk.W)
    HSV_label_8 .grid(column=3 , row=13, sticky=tk.W)
    HSV_label_9 .grid(column=4 , row=13, sticky=tk.W)
    HSV_label_10.grid(column=5 , row=13, sticky=tk.W)
    HSV_label_11.grid(column=6 , row=13, sticky=tk.W)
    HSV_label_12.grid(column=7 , row=13, sticky=tk.W)
    HSV_label_13.grid(column=8 , row=13, sticky=tk.W)
    HSV_label_14.grid(column=9 , row=13, sticky=tk.W)
    HSV_label_15.grid(column=10, row=13, sticky=tk.W)
    # end new stuff

    hex_label.  grid(column=3,  row=5, sticky=tk.W)
    hex_label1. grid(column=4,  row=5, sticky=tk.W)
    hex_label2. grid(column=5,  row=5, sticky=tk.W)
    hex_label3. grid(column=6,  row=5, sticky=tk.W)
    hex_label4. grid(column=7,  row=5, sticky=tk.W)
    hex_label5. grid(column=8,  row=5, sticky=tk.W)
    hex_label6. grid(column=9,  row=5, sticky=tk.W)
    hex_label7. grid(column=10, row=5, sticky=tk.W)  
    hex_label8. grid(column=3,  row=11,sticky=tk.W)
    hex_label9. grid(column=4,  row=11,sticky=tk.W)
    hex_label10.grid(column=5,  row=11,sticky=tk.W)
    hex_label11.grid(column=6,  row=11,sticky=tk.W)
    hex_label12.grid(column=7,  row=11,sticky=tk.W)
    hex_label13.grid(column=8,  row=11,sticky=tk.W)
    hex_label14.grid(column=9,  row=11,sticky=tk.W)
    hex_label15.grid(column=10, row=11,sticky=tk.W) 
    
    canvas = tk.Canvas(mainframe, bg='white', width=110, height=110, bd=-2, highlightthickness = 0)  
    canvas1 = tk.Canvas(mainframe, bg='white', width=110, height=110, bd=-2, highlightthickness = 0) 
    canvas2 = tk.Canvas(mainframe, bg='white', width=110, height=110, bd=-2, highlightthickness = 0) 
    canvas3 = tk.Canvas(mainframe, bg='white', width=110, height=110, bd=-2, highlightthickness = 0) 
    canvas4 = tk.Canvas(mainframe, bg='white', width=110, height=110, bd=-2, highlightthickness = 0) 
    canvas5 = tk.Canvas(mainframe, bg='white', width=110, height=110, bd=-2, highlightthickness = 0) 
    canvas6 = tk.Canvas(mainframe, bg='white', width=110, height=110, bd=-2, highlightthickness = 0) 
    canvas7 = tk.Canvas(mainframe, bg='white', width=110, height=110, bd=-2, highlightthickness = 0)     
    canvas8  = tk.Canvas(mainframe, bg='white', width=110, height=110, bd=-2, highlightthickness = 0)
    canvas9  = tk.Canvas(mainframe, bg='white', width=110, height=110, bd=-2, highlightthickness = 0)
    canvas10 = tk.Canvas(mainframe, bg='white', width=110, height=110, bd=-2, highlightthickness = 0)
    canvas11 = tk.Canvas(mainframe, bg='white', width=110, height=110, bd=-2, highlightthickness = 0)
    canvas12 = tk.Canvas(mainframe, bg='white', width=110, height=110, bd=-2, highlightthickness = 0)
    canvas13 = tk.Canvas(mainframe, bg='white', width=110, height=110, bd=-2, highlightthickness = 0)
    canvas14 = tk.Canvas(mainframe, bg='white', width=110, height=110, bd=-2, highlightthickness = 0)
    canvas15 = tk.Canvas(mainframe, bg='white', width=110, height=110, bd=-2, highlightthickness = 0)

    canvas.  grid(column=3, row=2, rowspan=4, sticky=(tk.W, tk.E))
    canvas1. grid(column=4, row=2, rowspan=4, sticky=(tk.W, tk.E))
    canvas2. grid(column=5, row=2, rowspan=4, sticky=(tk.W, tk.E))
    canvas3. grid(column=6, row=2, rowspan=4, sticky=(tk.W, tk.E))
    canvas4. grid(column=7, row=2, rowspan=4, sticky=(tk.W, tk.E))
    canvas5. grid(column=8, row=2, rowspan=4, sticky=(tk.W, tk.E))
    canvas6. grid(column=9, row=2, rowspan=4, sticky=(tk.W, tk.E))
    canvas7. grid(column=10,row=2, rowspan=4, sticky=(tk.W, tk.E))
    canvas8. grid(column=3, row=9, rowspan=4, sticky=(tk.W, tk.E))
    canvas9. grid(column=4, row=9, rowspan=4, sticky=(tk.W, tk.E))
    canvas10.grid(column=5, row=9, rowspan=4, sticky=(tk.W, tk.E))
    canvas11.grid(column=6, row=9, rowspan=4, sticky=(tk.W, tk.E))
    canvas12.grid(column=7, row=9, rowspan=4, sticky=(tk.W, tk.E))
    canvas13.grid(column=8, row=9, rowspan=4, sticky=(tk.W, tk.E))
    canvas14.grid(column=9, row=9, rowspan=4, sticky=(tk.W, tk.E))
    canvas15.grid(column=10,row=9, rowspan=4, sticky=(tk.W, tk.E))
            
    ttk.Button(mainframe, text="Generate", command=display_color).grid(column=2, row=9, sticky=tk.W)
    ttk.Button(mainframe, text="about", command=show_about).grid(column=2, row=10, sticky=tk.W)
    
    ttk.Button(mainframe, text="Copy hex", command=lambda: copy_to_clipboard(hex_label .cget("text"))).grid(column= 3, row=7, sticky=tk.S)
    ttk.Button(mainframe, text="Copy hex", command=lambda: copy_to_clipboard(hex_label1.cget("text"))).grid(column= 4, row=7, sticky=tk.S)
    ttk.Button(mainframe, text="Copy hex", command=lambda: copy_to_clipboard(hex_label2.cget("text"))).grid(column= 5, row=7, sticky=tk.S)
    ttk.Button(mainframe, text="Copy hex", command=lambda: copy_to_clipboard(hex_label3.cget("text"))).grid(column= 6, row=7, sticky=tk.S)
    ttk.Button(mainframe, text="Copy hex", command=lambda: copy_to_clipboard(hex_label4.cget("text"))).grid(column= 7, row=7, sticky=tk.S)
    ttk.Button(mainframe, text="Copy hex", command=lambda: copy_to_clipboard(hex_label5.cget("text"))).grid(column= 8, row=7, sticky=tk.S)
    ttk.Button(mainframe, text="Copy hex", command=lambda: copy_to_clipboard(hex_label6.cget("text"))).grid(column= 9, row=7, sticky=tk.S)
    ttk.Button(mainframe, text="Copy hex", command=lambda: copy_to_clipboard(hex_label7.cget("text"))).grid(column=10, row=7, sticky=tk.S)    
    ttk.Button(mainframe, text="Copy hex", command=lambda: copy_to_clipboard(hex_label8.cget("text"))).grid(column=3,   row=14, sticky=tk.S)
    ttk.Button(mainframe, text="Copy hex", command=lambda: copy_to_clipboard(hex_label9.cget("text"))).grid(column=4,   row=14, sticky=tk.S)
    ttk.Button(mainframe, text="Copy hex", command=lambda: copy_to_clipboard(hex_label10.cget("text"))).grid(column=5,  row=14, sticky=tk.S)
    ttk.Button(mainframe, text="Copy hex", command=lambda: copy_to_clipboard(hex_label11.cget("text"))).grid(column=6,  row=14, sticky=tk.S)
    ttk.Button(mainframe, text="Copy hex", command=lambda: copy_to_clipboard(hex_label12.cget("text"))).grid(column=7,  row=14, sticky=tk.S)
    ttk.Button(mainframe, text="Copy hex", command=lambda: copy_to_clipboard(hex_label13.cget("text"))).grid(column=8,  row=14, sticky=tk.S)
    ttk.Button(mainframe, text="Copy hex", command=lambda: copy_to_clipboard(hex_label14.cget("text"))).grid(column=9,  row=14, sticky=tk.S)
    ttk.Button(mainframe, text="Copy hex", command=lambda: copy_to_clipboard(hex_label15.cget("text"))).grid(column=10, row=14, sticky=tk.S)
    
    for child in mainframe.winfo_children(): child.grid_configure(padx=0, pady=5)
    
    hue_entry.focus()
    root.bind('<Return>', display_color)
        
    root.mainloop()
