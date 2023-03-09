import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageOps, ImageTk, ImageFilter
import math

root = tk.Tk()
root.geometry("800x800")
root.title("Image Editor Tool")
root.attributes('-zoomed', True)
root.config(bg="white")

photo_width = 354
photo_height = 472
choise_photo_format = tk.IntVar()
choise_photo_format.set(0)

tmp_image = Image.open("./default_img.jpg")
tmp_processed_image = tmp_image
final_image = tmp_image

top_cropping = 0
left_cropping = 0
right_cropping = photo_width
bottom_cropping =  photo_height

def searchImage():
    global file_path, tmp_image, tmp_processed_image, photo_height, photo_width
    file_path = filedialog.askopenfilename(initialdir="/home/gilson/Pictures")
    original_image = Image.open(file_path)
    new_width, new_height = int(original_image.width / 2), int(original_image.height / 2)
    tmp_image = original_image.resize((new_width, new_height), Image.LANCZOS)
    tmp_processed_image = tmp_image
    updateComponents()
    restoreComponents()
    min_scale_h = photo_height / tmp_processed_image.height * 100
    min_scale_w = photo_width / tmp_processed_image.width * 100
    if(min_scale_h > min_scale_w):
        scale_resize_btn.config(from_= math.ceil(min_scale_h))
    else:
        scale_resize_btn.config(from_= math.ceil(min_scale_w))
    renderImage(tmp_image)
    
def updateComponents():
    horizontal_cropping_btn.config(to=tmp_processed_image.width - photo_width)
    vertical_cropping_btn.config(to=tmp_processed_image.height - photo_height)

def restoreComponents():
    scale_resize_btn.set(100)
    horizontal_cropping_btn.set(1)
    vertical_cropping_btn.set(1)

def renderImage(image):
    converted_image = ImageTk.PhotoImage(image)
    img_canvas.image = converted_image
    img_canvas.create_image(0, 0, image=converted_image, anchor="nw")

def selectFormat():
    global photo_width, photo_height
    index = choise_photo_format.get()
    if(index == 0):
        photo_width = 354
        photo_height = 472
    elif(index == 1):
        photo_width = 591
        photo_height = 827
    img_canvas.config(width=photo_width, height=photo_height)
    restoreComponents()
    updateComponents()

def scaleImage(value):
    global tmp_image, tmp_processed_image
    scale_factor = int(value) / 100
    tmp_processed_image = tmp_image.resize((round(tmp_image.width * scale_factor), round(tmp_image.height * scale_factor)))
    verticalCropping(vertical_cropping_btn.get())
    horizontalCropping(horizontal_cropping_btn.get())
    updateComponents()
    renderImage(tmp_processed_image)

def verticalCropping(value):
    global final_image, tmp_processed_image, top_cropping, left_cropping, right_cropping, bottom_cropping
    cropping_factor = int(value)
    top_cropping = cropping_factor
    bottom_cropping = top_cropping + photo_height
    final_image = tmp_processed_image.crop((left_cropping, top_cropping, right_cropping, bottom_cropping))
    renderImage(final_image)

def horizontalCropping(value):
    global final_image, tmp_processed_image, top_cropping, left_cropping, right_cropping, bottom_cropping,horizontal_cropping_btn
    cropping_factor = int(value)
    left_cropping = cropping_factor
    right_cropping = left_cropping + photo_width
    final_image = tmp_processed_image.crop((left_cropping, top_cropping, right_cropping, bottom_cropping))
    renderImage(final_image)

def saveImage():
    generatePhoto().save("output.jpg")

def generatePhoto():
    global tmp_complete_photo
    tmp_complete_photo = Image.new( "RGB", (1800, 1200), (255, 255, 255))
    if(choise_photo_format.get() == 0):
        margin_top = 85
        margin_left = 185
        total_margin = 0
        for x in range(3):
            tmp_complete_photo.paste(final_image, (total_margin + margin_left, margin_top))
            tmp_complete_photo.paste(final_image, (total_margin + margin_left, 2 * margin_top + photo_height))
            total_margin = total_margin + margin_left + photo_width
    else:
        margin_top = 4
        margin_left = 48
        total_margin = 0
        final_rotated = final_image.rotate(90, expand=True)
        for x in range(2):
            tmp_complete_photo.paste(final_rotated, (total_margin + margin_left, margin_top))
            tmp_complete_photo.paste(final_rotated, (total_margin + margin_left, 2 * margin_top + photo_width))
            total_margin = total_margin + margin_left + photo_height
    return(tmp_complete_photo)

def showPhoto():
    generatePhoto().show()

# Barra de tarefa lateral
left_frame = tk.Frame(root, width=400, height=500, bg="grey")
left_frame.pack(side="left", fill="y")

# Botão de selecionar imagem
search_btn = tk.Button(left_frame, text="Selecionar Imagem", bg="white", command=searchImage)
search_btn.pack(pady=15, padx=20)

# Botão formato da foto
format_1_btn = tk.Radiobutton(left_frame, text="3x4", variable=choise_photo_format, value=0, command=selectFormat)
format_1_btn.pack()

format_2_btn = tk.Radiobutton(left_frame, text="5x7", variable=choise_photo_format, value=1, command=selectFormat)
format_2_btn.pack()

# Botões deslizantes redimencionar imagem
tk.Label(left_frame, text="Zoom/Escala").pack(pady=(30, 0))
scale_resize_btn = tk.Scale(left_frame, from_=1, to=100, orient="horizontal", command=scaleImage)
scale_resize_btn.set(100)
scale_resize_btn.pack(pady=(0, 10))

tk.Label(left_frame, text="Movimento Vertical").pack(pady=(30, 0))
vertical_cropping_btn = tk.Scale(left_frame, from_=1, to=100, command=verticalCropping)
vertical_cropping_btn.pack(pady=(0, 10))

tk.Label(left_frame, text="Movimento Horizontal").pack(pady=(30, 0))
horizontal_cropping_btn = tk.Scale(left_frame, from_=1, to=100, orient="horizontal", command=horizontalCropping)
horizontal_cropping_btn.pack(pady=(0, 10))

# Botão de selecionar imagem
save_btn = tk.Button(left_frame, text="Salvar Imagem", bg="white", command=saveImage)
save_btn.pack(pady=15, padx=20, side="bottom")

# Botão de exibir pre-impressão
save_btn = tk.Button(left_frame, text="Exibir Foto", bg="white", command=showPhoto)
save_btn.pack(pady=15, padx=20, side="bottom")

# Canvas com a imagem
img_canvas = tk.Canvas(root, width=photo_width, height=photo_height, bg="white", bd="1", highlightthickness=1, highlightbackground = 'grey')
img_canvas.pack(expand=1)

root.mainloop()