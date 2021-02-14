from tkinter import *
from tkinter import filedialog
import win32gui
from PIL import ImageGrab, Image
import numpy as np
from PIL import ImageFilter


from keras.models import load_model
model = load_model('model/model.h5')


root = Tk()
root.title("Hand Writtten Digit Recognication")
root.geometry("300x300")
root.iconbitmap(r'D.ico') 



def Canvas_window_for_draw_digit():
    draw = Toplevel(root)
    global canvas
    draw.attributes('-fullscreen', True)
    canvas = Canvas(draw, width=300, height=300, bg = "white", cursor="cross")
    canvas.grid(row=0, column=0, pady=2, sticky=W, columnspan = 3)
    canvas.bind("<B1-Motion>",draw_lines)

    button_clear = Button(draw, text = "Clear", command =clear_all)
    button_clear.grid(row=1, column=0, pady=5)

    predict_btn = Button(draw, text = "Recognise", command = make_img_of_canvas) 
    predict_btn.grid(row=1, column=2, pady=5)

    # digit_output.destroy()
    exit_btn = Button(draw, text = "Exit", command = draw.destroy)
    exit_btn.grid(row=2, column= 1)

def clear_all():
    canvas.delete("all")
def draw_lines(event):
    x = event.x
    y = event.y
    r=8
    canvas.create_oval(x-r, y-r, x + r, y + r, fill='black')



# upload file
def UploadAction(event=None):
    global filename
    filename = filedialog.askopenfilename()
    # print('Selected:', filename)
    # if(".png" not in filename and ".jpg" not in filename):
    #     error_window_jpg = Toplevel(root)
    #     error_window_jpg.geometry("200x200")
    #     error_window_jpg.title("Error!")
    #     Error_message = Label(error_window_jpg,text = "Please upload .jpg or .png file only")
    #     Error_message.place(relx=0.5, rely=0.5, anchor=CENTER)
    #     return
    error_window_jpg = Toplevel(root)
    error_window_jpg.geometry("200x200")
    error_window_jpg.title("Error!")
    Error_message = Label(error_window_jpg,text = "Under Working Process")
    Error_message.place(relx=0.5, rely=0.5, anchor=CENTER)

def make_img_of_canvas():
    HWND = canvas.winfo_id() # get the handle of the canvas
    rect = win32gui.GetWindowRect(HWND) # get the coordinate of the canvas
    im = ImageGrab.grab(rect)

    digit= predict_digit(im)
    # digit, acc = predict_digit(im)


    global digit_output
    digit_output = Toplevel(root)
    digit_output.geometry("300x300")
    digit_output_label = Label(digit_output,text = "", font=("Helvetica", 48))
    digit_output_label.place(relx=0.5, rely=0.5, anchor=CENTER)
    # digit_output_label.configure(text= str(digit)+', '+ str(int(acc*100))+'%')
    digit_output_label.configure(text = str(digit))

def predict_digit(image):
    # image = image.resize((28,28))
    # image = image.convert('L')
    # image = np.array(image)
    # image = image.reshape(1,28,28,1)
    # image = image/255.0

    image = convert(image)

    result = model.predict(image)
    digit = np.argmax(result)
    probability = max(result)
    return digit
    # return 1,0.75

def imageprepare(im):
    im = im.convert('L')
    width = float(im.size[0])
    height = float(im.size[1])
    newImage = Image.new('L', (28, 28), (255))
    if width > height:
        nheight = int(round((20.0 / width * height), 0)) 
        if (nheight == 0):  
            nheight = 1
        img = im.resize((20, nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wtop = int(round(((28 - nheight) / 2), 0)) 
        newImage.paste(img, (4, wtop))
    else:
        nwidth = int(round((20.0 / height * width), 0))
        if (nwidth == 0):  
            nwidth = 1
        img = im.resize((nwidth, 20), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wleft = int(round(((28 - nwidth) / 2), 0))
        newImage.paste(img, (wleft, 4))
    tv = list(newImage.getdata())
    tva = [(255 - x) * 1.0 / 255.0 for x in tv]
    return tva

import matplotlib.pyplot as plt

def convert(image):
    x=[imageprepare(image)]
    print(len(x))
    newArr=[[0 for d in range(28)] for y in range(28)]
    k = 0
    for i in range(28):
        for j in range(28):
            newArr[i][j]=x[0][k]
            k=k+1

    img = np.array(newArr).reshape(-1,28,28,1)
    return img

##################################################################### Root window

# Name label in root window
Name = Label(root,text = "Created by Dhananjay!")
Name.grid(row =0,column = 0)
# button1 for drawing here
button1 = Button(root,text = "Draw Digit", command = Canvas_window_for_draw_digit)
button1.place(relx=0.5, rely=0.25,anchor=CENTER)

# button2 for uploading files  
button = Button(root, text='Upload file', command=UploadAction)
button.place(relx=0.5, rely=0.75, anchor=CENTER)


root.resizable(0,0)
root.mainloop()