from tkinter import *
from PIL import Image
from PIL import ImageTk
from PIL import ImageDraw
from emoter import make_emotes


class emoter_gui:
    def __init__(self):
        super().__init__()
        self.sprite_size = 0
        self.emote_size = 96
        self.img = None
        self.sprite_rows = 0
        self.sprite_cols = 0
        self.rect = None
        self.x = 0
        self.y = 0

    def initUI(self):

        root = Tk()
        root.title('Emoter')

        self.img = "Jeanne_DArc_Alter_Berserker.png"
        img = Image.open(self.img)
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
        canvas.pack(side=LEFT,expand=True,fill=Y)
        canvas.pack(pady=10)
        img_canvas = canvas.create_image(0, 0, anchor=NW, image=img_tk)


        def confirm():
            make_emotes(self.img, self.sprite_size, self.x, self.y, self.emote_size)

        config_canvas = Canvas(frame, width=50, height=h)
        config_canvas.pack(side=RIGHT,expand=True,fill=BOTH)

        sv_sprite_size = IntVar(config_canvas, value=256)
        self.sprite_size = sv_sprite_size.get()
        entry_sprite_size = Entry(config_canvas, textvariable=sv_sprite_size)
        entry_sprite_size.pack()

        self.sprite_cols = int(img.width/self.sprite_size)
        self.sprite_rows = int(img.height/self.sprite_size)

        def update_sprite_size(event):
            print(str(event))
            self.sprite_size = sv_sprite_size.get()

        entry_sprite_size.bind("<Return>", update_sprite_size)
        entry_sprite_size.bind("<FocusOut>", update_sprite_size)



        sv_emote_size = IntVar(config_canvas, value=96)
        self.emote_size = sv_emote_size.get()
        entry_emote_size = Entry(config_canvas, textvariable=sv_emote_size)
        entry_emote_size.pack()

        def update_emote_size(event):
            print(str(event))
            self.emote_size = sv_emote_size.get()
            render_rectangles()

        entry_emote_size.bind("<Return>", update_emote_size)
        entry_emote_size.bind("<FocusOut>", update_emote_size)



        b = Button(config_canvas, text="OK", command=confirm)
        b.pack()

        root.geometry(str(img.width+50) + "x" + str(h))
        canvas.config(width=img.width, height=img.height)

        def render_rectangles():
            alpha = Image.new("RGBA", (self.emote_size, self.emote_size), (255, 255, 255, 0))
            draw = ImageDraw.Draw(alpha)
            draw.rectangle([0, 0, self.emote_size, self.emote_size],
                           fill=(255, 127, 0, 100),
                           outline=(255, 127, 0, 255),
                           width=1)
            self.rect = ImageTk.PhotoImage(image=alpha)
            canvas.itemconfig("rect", image=self.rect)

        for i in range(0, self.sprite_cols+1):
            for j in range(0, self.sprite_rows+1):
                canvas.create_image(i*self.sprite_size, j*self.sprite_size, anchor=NW, tags=("rect", "rect" + str(i) + "-" + str(j)))
        render_rectangles()


        def move(event):
            self.x = event.x % self.sprite_size
            self.y = event.y % self.sprite_size

            if self.x + self.emote_size > self.sprite_size:
                self.x = self.sprite_size - self.emote_size
            if self.y + self.emote_size > self.sprite_size:
                self.y = self.sprite_size - self.emote_size

            # label.config(text=str(event.x) + " / " + str(event.y))
            for i in range(0, self.sprite_cols + 1):
                for j in range(0, self.sprite_rows + 1):
                    canvas.coords("rect" + str(i) + "-" + str(j), self.x+i*self.sprite_size, self.y+j*self.sprite_size)
        canvas.bind("<B1-Motion>", move)



        root.mainloop()


def main():
    app = emoter_gui()
    app.initUI()
    pass


if __name__ == "__main__":
    main()