from email.mime import image
from tkinter import *
from tkinter import colorchooser
import tkinter.filedialog as fd
from tkinter.simpledialog import askinteger, askstring
from tkinter.messagebox import showinfo
from PIL import Image, ImageDraw, ImageFont, ImageTk




def select_image():
    filepath = fd.askopenfilename(
        title='Open a file',
        initialdir='C:/Users/OLA/Pictures',
        )
    display_image(filepath)

 
def display_image(filepath):
    global img_to_display, width, height, image_to_edit, cv
    try:
        image_to_edit = Image.open(fp=filepath, mode='r', formats=None)
        width, height = image_to_edit.size
        img_to_display = PhotoImage(file=filepath)
        canvas.config(width=width, height=height)
        cv = canvas.create_image(width/2, height/2, image=img_to_display)
        canvas.grid(column=1, row=1)
        add_button = Button(text="Add Text", command=add_text, highlightthickness=0)
        add_button.grid(column=2, row=3)
        choose_image.grid(row=3, column=0)
        

    except:
        showinfo(
            title = 'Unidentified Image',
             message='Invalid Image'
             )


def add_text():
    global watermark, image_file, ct
    watermark = askstring(title="Watermark", prompt="Type your watermark")
    text_size = askinteger(title="Text Size", prompt="Set text size")
    x_axis = askinteger(title="Horizontal Placement", prompt=f"Type in the horizontal position between 0-{width}")
    y_axis = askinteger(title="VerticalPlacement",prompt=f"Type in the vertical position between 0-{height}")
    rgb_color, web_color = colorchooser.askcolor(parent=window, initialcolor="black")
    
    try:
        edit_image = ImageDraw.Draw(image_to_edit)
        #Display text on image
        ct = canvas.create_text(x_axis, y_axis, text=watermark, fill=web_color, font=('Arial', text_size, "normal"))
        # Add text to your image
        edit_image.text((x_axis, y_axis), text=watermark, font=ImageFont.truetype("arial.ttf", text_size), fill=web_color)

    except ValueError:
        showinfo(
            title = 'Unidentified Image',
             message='No Opened Image'
             )

    remove = Button(text="Remove Text", command=reset,  highlightthickness=0)
    remove.grid(column=2, row=2)
    save = Button(text="Save Image", command=save_image)
    save.grid(column=0, row=2)

def reset():
    canvas.itemconfig(ct, text='')


def save_image():
    try:
        save_loc = fd.asksaveasfile(initialfile="Untitled.jpg", defaultextension=".jpg", filetypes=[("All Files", "*.*"), ("Image","*.jpg")])
        image_to_edit.convert('RGB').save(save_loc.name)
        image_to_edit.close()
        canvas.itemconfig(ct, text='')
        default_img = PhotoImage(file='default.png')
        canvas.itemconfig(cv, image=default_img)
        canvas.create_image(width/2, height/2, image=default_img)

    except ValueError:
        showinfo(
            title = 'Unidentified Image',
             message='No Opened Image'
             )

    
window = Tk()
window.title("Image Watermarking Program")
window.config(padx=50, pady=50)

Label().grid(row=0, column=0)

choose_image = Button(text='Choose Image File', command=select_image)
choose_image.grid(row=1, column=1)

canvas = Canvas(width=600, height=400, bg="white")
window.mainloop()