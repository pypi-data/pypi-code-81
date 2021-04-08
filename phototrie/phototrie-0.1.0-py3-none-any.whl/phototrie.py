import os
import shutil
from tempfile import mkdtemp
from tkinter import *
from typing import List, Tuple, Optional

from PIL import Image, ImageTk

NAMES = {"b": "bad", "g": "good", "p": "pristine"}


def prepare_processable(search_in: str):
    tmp_dir = mkdtemp("")
    to_process = []
    extension = "." + sys.argv[1]
    for file in sorted(os.listdir(search_in)):
        if file.endswith(extension):
            full_path = search_in + "/" + file
            thumb_path = tmp_dir + "/" + file + ".jpg"
            image = Image.open(file)
            image.thumbnail((512, 512))
            image.save(thumb_path)

            # also search for raw CR2
            unextended = os.path.splitext(file)[0]
            found_raw = None
            if os.path.exists(unextended + ".CR2"):
                found_raw = unextended + ".CR2"
            else:
                unextended_basename = os.path.basename(unextended)
                try_next = os.path.dirname(file) + "/CR2/" + unextended_basename
                if os.path.exists(try_next):
                    found_raw = try_next

            to_process.append((full_path, thumb_path, found_raw))

    return to_process, tmp_dir


class App:
    def __init__(
        self, to_process: List[Tuple[str, str, Optional[str]]], sort_dest: str
    ):
        self.sort_dest = sort_dest
        self.top = Tk()
        self.processing_now = None
        self.to_process = to_process

        image = self.load_next_image()
        self.display = Label(self.top, image=image)
        self.display.image = image  # prevents GC
        self.display.grid()

        self.top.bind("<b>", self.callback)
        self.top.bind("<g>", self.callback)
        self.top.bind("<p>", self.callback)

    def callback(self, e):
        name = NAMES[e.char]
        print(self.processing_now[0], name)
        shutil.move(self.processing_now[0], self.sort_dest + "/" + name)
        if self.processing_now[2] is not None:
            # also move the raw
            shutil.move(self.processing_now[2], self.sort_dest + "/" + name)
        os.remove(self.processing_now[1])

        try:
            next_img = self.load_next_image()
        except IndexError:
            self.top.quit()
            return
        self.display.configure(image=next_img)
        self.display.image = next_img  # prevents GC

    def load_next_image(self):
        next = self.to_process.pop(0)
        self.processing_now = next

        _full_path, thumb_path, _raw_path = next
        img = Image.open(thumb_path)
        photo_img = ImageTk.PhotoImage(img)
        return photo_img


def cli():
    print("<phototrie.py> [file extension to process e.g. CR2 or jpg.")
    print("keybinds: B 'bad', 'G' good, 'P' pristine")

    to_process, tmp_dir = prepare_processable(".")

    dirs = "./bad", "./good", "./pristine"

    for directory in dirs:
        if not os.path.isdir(directory):
            os.mkdir(directory)

    app = App(to_process, ".")

    app.top.mainloop()
    os.rmdir(tmp_dir)


if __name__ == "__main__":
    cli()
