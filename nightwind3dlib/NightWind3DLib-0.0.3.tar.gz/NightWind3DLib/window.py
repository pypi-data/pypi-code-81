from direct.directbase.DirectStart import base
from panda3d.core import*


class Window:
    def __init__(self):
        self.base = base
        self.window = WindowProperties()
        self.window.setTitle("Fly to the universe")
        self.window.setSize(1200, 900)
        self.base.win.requestProperties(window)
        self.base.setBackgroundColor(0/255, 128/255, 255/255)
        self.LoadBg()

    def LoadBg(self):
        self.schoolKey = loader.loadModel("images_window/school")
        self.schoolKey.reparentTo(render)
        self.space = loader.loadModel("images_window/space")
        self.space.reparentTo(render)
        self.space.setScale(0.7)
        self.space.setPos(0, -500, 0)


if __name__ == "__main__":
    window = Window()
    window.base.run()
