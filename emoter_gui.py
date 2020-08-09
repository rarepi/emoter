from tkinter import *
from PIL import Image
from PIL import ImageTk
from PIL import ImageDraw
from emoter import make_emotes

root = Tk()
root.title('Emoter')

########################
# temporarily hardcoded
########################
emote_size = 96
sprite_size = 256

img = Image.open("Jeanne_DArc_Alter_Berserker.png")
img_tk = ImageTk.PhotoImage(image=img)

h = 800
w = h
frame = Frame(root,width=w,height=h)
frame.pack(expand=True, fill=BOTH)
canvas = Canvas(frame, width=img_tk.width(), height=h, bg="white", scrollregion=(0,0,img_tk.width(),img_tk.height()))
vbar = Scrollbar(frame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)
canvas.config(width=img_tk.width(),height=300)
canvas.config(yscrollcommand=vbar.set)
canvas.pack(side=LEFT,expand=True,fill=BOTH)
canvas.pack(pady=10)

img_canvas = canvas.create_image(0, 0, anchor=NW, image=img_tk)

col_count = int(img.width/sprite_size)
row_count = int(img.height/sprite_size)
print(col_count)
print(row_count)

root.geometry(str(img.width) + "x" + str(h))
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
