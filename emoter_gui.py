from tkinter import *
from tkinter import filedialog

from PIL import Image
from PIL import ImageTk
from PIL import ImageDraw

from pathlib import Path

from emoter import make_emotes


class emoter_gui:
    def __init__(self):
        super().__init__()
        self.sprite_size = 0
        self.emote_size = 96
        self.image_file = None
        self.sprite_sheet = None
        self.sprite_rows = 0
        self.sprite_cols = 0
        self.rect = None
        self.x = 0
        self.y = 0

    def initUI(self):
        h = 512
        w = 1024
        root = Tk()
        root.title('Emoter')
        root.geometry(str(w + 50) + "x" + str(h + 50))

        ####################
        # Open File Dialog #
        ####################
        # canvas
        file_dialog_canvas = Canvas(root, width=w, height=50)
        file_dialog_canvas.pack(side=TOP, expand=True, fill=BOTH)
        # input
        svar_image_file = StringVar(file_dialog_canvas, value="")
        entry_image_file = Entry(file_dialog_canvas, textvariable=svar_image_file)

        def recalculate_emote_grid():
            self.sprite_cols = int(self.sprite_sheet.width() / self.sprite_size)
            self.sprite_rows = int(self.sprite_sheet.height() / self.sprite_size)

        # button
        def open_image_file():
            svar_image_file.set(filedialog.askopenfilename(initialdir=".", title="Select file"))
            update_image_file()
        button_open_image_file = Button(file_dialog_canvas, text="Open", command=open_image_file)
        button_open_image_file.pack(side=LEFT, padx=(10,0))
        entry_image_file.pack(expand=True, fill=BOTH, padx=10, pady=10)

        def update_image_file(event=None):
            self.image_file = svar_image_file.get()
            self.sprite_sheet = PhotoImage(file=self.image_file)
            canvas.itemconfig("sprite-sheet", image=self.sprite_sheet)
            canvas.config(scrollregion=(0, 0, self.sprite_sheet.width(), self.sprite_sheet.height()))
            recalculate_emote_grid()
            canvas.delete("rect")
            for i in range(0, self.sprite_cols + 1):
                for j in range(0, self.sprite_rows + 1):
                    canvas.create_image(i * self.sprite_size, j * self.sprite_size, anchor=NW,
                                        tags=("rect", "rect" + str(i) + "-" + str(j)))
            render_rectangles()

        entry_image_file.bind("<Return>", update_image_file)
        entry_image_file.bind("<FocusOut>", update_image_file)

        ################
        # Sheet Canvas #
        ################
        frame = Frame(root, width=w, height=h)
        frame.pack(expand=True, fill=BOTH)
        canvas = Canvas(frame, width=w, height=h, bg="white")
        canvas.create_image(0, 0, anchor=NW, tag="sprite-sheet")

        vbar = Scrollbar(frame, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=canvas.yview)
        hbar = Scrollbar(frame, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)
        hbar.config(command=canvas.xview)
        canvas.config(yscrollcommand=vbar.set, xscrollcommand=hbar.set)
        canvas.pack(side=LEFT, expand=True, fill=Y)
        canvas.pack(pady=10)

        config_canvas = Canvas(frame, width=50, height=h)
        config_canvas.pack(side=RIGHT, expand=True, fill=BOTH)

        ivar_sprite_size = IntVar(config_canvas, value=256)
        self.sprite_size = ivar_sprite_size.get()
        entry_sprite_size = Entry(config_canvas, textvariable=ivar_sprite_size)
        entry_sprite_size.pack()

        def update_sprite_size(event):
            self.sprite_size = ivar_sprite_size.get()
            update_image_file()
            # TODO reset rectangle positions here

        entry_sprite_size.bind("<Return>", update_sprite_size)
        entry_sprite_size.bind("<FocusOut>", update_sprite_size)

        ivar_emote_size = IntVar(config_canvas, value=96)
        self.emote_size = ivar_emote_size.get()
        entry_emote_size = Entry(config_canvas, textvariable=ivar_emote_size)
        entry_emote_size.pack()

        def update_emote_size(event):
            self.emote_size = ivar_emote_size.get()
            recalculate_emote_grid()
            render_rectangles()

        entry_emote_size.bind("<Return>", update_emote_size)
        entry_emote_size.bind("<FocusOut>", update_emote_size)

        def confirm():
            make_emotes(self.image_file, self.sprite_size, self.x, self.y, self.emote_size)

        b = Button(config_canvas, text="OK", command=confirm)
        b.pack()

        def render_rectangles():
            alpha = Image.new("RGBA", (self.emote_size, self.emote_size), (255, 255, 255, 0))
            draw = ImageDraw.Draw(alpha)
            draw.rectangle([0, 0, self.emote_size, self.emote_size],
                           fill=(255, 127, 0, 100),
                           outline=(255, 127, 0, 255),
                           width=1)
            self.rect = ImageTk.PhotoImage(image=alpha)
            canvas.itemconfig("rect", image=self.rect)

        def move(event):
            self.x = min(max(0, event.x), w - 1) % self.sprite_size
            self.y = min(max(0, event.y), h - 1) % self.sprite_size

            if self.x + self.emote_size > self.sprite_size:
                self.x = self.sprite_size - self.emote_size
            if self.y + self.emote_size > self.sprite_size:
                self.y = self.sprite_size - self.emote_size

            # label.config(text=str(event.x) + " / " + str(event.y))
            for i in range(0, self.sprite_cols + 1):
                for j in range(0, self.sprite_rows + 1):
                    canvas.coords("rect" + str(i) + "-" + str(j), self.x + i * self.sprite_size,
                                  self.y + j * self.sprite_size)

        canvas.bind("<B1-Motion>", move)

        root.mainloop()


def main():
    app = emoter_gui()
    app.initUI()
    pass


if __name__ == "__main__":
    main()
