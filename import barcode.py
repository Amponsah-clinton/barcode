import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import barcode
from barcode.writer import ImageWriter
import qrcode
from PIL import Image, ImageTk

def generate_barcode(number, save_path):
    ean = barcode.get_barcode_class('ean13')
    ean_barcode = ean(str(number).zfill(12), writer=ImageWriter()) 
    barcode_path = f"{save_path}/barcode_image.png"
    ean_barcode.save(barcode_path)
    return barcode_path

def generate_qrcode(number, save_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(str(number))
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    qr_path = f"{save_path}/qrcode_image.png"
    img.save(qr_path)
    return qr_path

def display_image(image_path, canvas, x, y):
    image = Image.open(image_path)
    image = image.resize((150, 150), Image.ANTIALIAS)  
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(x, y, image=photo)
    canvas.image = photo  

def on_generate():
    number = entry.get()
    if not number.isdigit():
        messagebox.showerror("Invalid input", "Please enter a valid number.")
        return
    
    save_path = filedialog.askdirectory(title="Select Folder to Save Images")
    if not save_path:
        return
    
    barcode_path = generate_barcode(number, save_path)
    qr_code_path = generate_qrcode(number, save_path)

    display_image(barcode_path, canvas, 100, 100)
    display_image(qr_code_path, canvas, 300, 100)

    messagebox.showinfo("Success", "Barcode and QR code generated and saved.")

root = tk.Tk()
root.title("Barcode and QR Code Generator")

label = tk.Label(root, text="Enter a Number:")
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=5)

generate_button = tk.Button(root, text="Generate", command=on_generate)
generate_button.pack(pady=10)

canvas = tk.Canvas(root, width=400, height=200)
canvas.pack(pady=20)

root.mainloop()
