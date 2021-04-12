from direct.directbase.DirectStart import base
from panda3d.core import*


class Window:
    def __init__(self):
        self.base = base
        self.window = WindowProperties()
        self.window.setTitle("New Galaxy")
        self.window.setSize(1600, 1000)
        self.base.win.requestProperties(self.window)
        self.planets = []
        self.position = [(0, 0, 0), (600, 0, 0), (-900, 0, 0),
                         (1200, 0, 0), (1600, 0, 0), (200, 150, 0)]
        self.LoadPlanet()
        self.LoadSky()

    def LoadPlanet(self):
        for i in range(1, 7):
            planet = loader.loadModel(f"images_galaxy/planet{i}")
            planet.reparentTo(render)
            planet.setPos(self.position[i - 1][0],
                          self.position[i - 1][1],
                          self.position[i - 1][2])
            self.planets.append(planet)
            planet.hprInterval(9 - i, (360, 0, 0)).loop()

        for i in range(2, 6):
            virtual = render.attachNewNode(f"planet_{i}")
            planets[i - 1].reparentTo(virtual)
            virtual.hprInterval(9 - i, (360, 0, 0)).loop()

        virtual_6 = planets[3].attachNewNode("planet_6")
        planets[5].reparentTo(virtual_6)

    def LoadSky(self):
        self.sky = loader.loadModel("images_galaxy/space_sky")
        self.sky.reparentTo(render)


if __name__ == "__main__":
    window = Window()
    window.base.run()
