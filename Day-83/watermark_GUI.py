from tkinter import Tk,filedialog,Button,Label
from PIL import Image,ImageTk,ImageDraw,ImageFont

window = Tk()

window.title("Watermarks App")
window.config(padx=50,pady=50)

def upload_image():
    global image
    global photo
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    image = Image.open(filepath)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(size=50)
    draw.text((image.width-200,image.height-50),font=font,text="Maneesh",fill="white")
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    save_path = filedialog.asksaveasfilename(
    defaultextension=".jpg",
    filetypes=[
        ("JPEG", "*.jpg"),
        ("PNG", "*.png")])

    image.save(save_path)
upload_button = Button(window,
    text="Upload Image",
    command=upload_image
)
upload_button.pack()

image_label = Label(window)
image_label.pack()


window.mainloop()