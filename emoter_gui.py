from tkinter import *
from PIL import Image
from PIL import ImageTk
from PIL import ImageDraw

root = Tk()
root.title('Emoter')
# root.iconbitmap('path/to/file.ico')
root.geometry("800x600")





w = 600
h = 400
canvas = Canvas(root, width=w, height=h, bg="white")
canvas.pack(pady=20)

img = Image.open("Jeanne_DArc_Alter_Berserker.png")
# img.thumbnail((1000, 1000), Image.ANTIALIAS)
img_tk = ImageTk.PhotoImage(image=img)
img_canvas = canvas.create_image(0, 0, anchor=NW, image=img_tk)

########################
# temporarily hardcoded
########################
sprite_size = 256
emote_size = 96



col_count = int(img.width/sprite_size)
row_count = int(img.height/sprite_size)
print(col_count)
print(row_count)

root.geometry(str(img.width) + "x" + str(img.height))
canvas.config(width=img.width, height=img.height)


alpha = Image.new("RGBA", (96, 96), (255, 255, 255, 0))
draw = ImageDraw.Draw(alpha)
draw.rectangle([0,0,emote_size,emote_size], fill=(255, 127, 0, 100), outline=(255, 127, 0, 255), width=1)
rect = ImageTk.PhotoImage(image=alpha)

for i in range(0, col_count+1):
    for j in range(0, row_count+1):
        img_canvas_rect = canvas.create_image(i*sprite_size, j*sprite_size, anchor=NW, image=rect, tags="rect" + str(i) + "-" + str(j))




#label = Label(root)
#label.pack(pady=20)


def left(event):
    x = -10
    y = 0
    canvas.move(img_canvas_rect, x, y)

def right(event):
    x = 10
    y = 0
    canvas.move(img_canvas_rect, x, y)

def up(event):
    x = 0
    y = -10
    canvas.move(img_canvas_rect, x, y)

def down(event):
    x = 0
    y = 10
    canvas.move(img_canvas_rect, x, y)

def move(event):
    x = event.x % sprite_size
    y = event.y % sprite_size

    if x + emote_size > sprite_size:
        x = sprite_size - emote_size
    if y + emote_size > sprite_size:
        y = sprite_size - emote_size

    # label.config(text=str(event.x) + " / " + str(event.y))
    for i in range(0, col_count + 1):
        for j in range(0, row_count + 1):
            canvas.coords("rect" + str(i) + "-" + str(j), x+i*sprite_size, y+j*sprite_size)


canvas.bind("<B1-Motion>", move)
root.bind("<Left>", left)
root.bind("<Right>", right)
root.bind("<Up>", up)
root.bind("<Down>", down)

root.mainloop()
