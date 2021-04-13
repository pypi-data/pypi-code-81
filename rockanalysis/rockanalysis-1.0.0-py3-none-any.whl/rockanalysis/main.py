import matplotlib.pyplot as plt
import pandas as pd
import wx

app=wx.App()

frame=wx.Frame(None, -1, "Save")


class Analyze():
    def __init__(self, filename):
        self.file = open(filename, "r")
        self.time = []
        self.force = []
        self.displacement = []
        self.run = False
        self.title = ""

    def decode(self):
        if self.run == True:
            print("Data already Decoded")
            return

        self.run=True

        # split into list that contains time, force and displacemnt (rstrip removes trailing characters)
        for line in self.file:
            line = line.rstrip().split("\t")
            try:
                #convert each element in the list to float, then create new list
                line = list(map(float, line))
               
            except ValueError:
                continue

            self.time.append(line[0])
            self.force.append(line[1])
            self.displacement.append(line[2])


    def plot(self, x, y):
        plt.plot(x, y)
        plt.show()
        
    def plotforcevtime(self):
        if self.run == False:
            self.decode()
        
        plt.plot(self.time, self.force)
        plt.ylabel("Force (N)")
        plt.xlabel("Time (s)")
        plt.title(self.title + " Force vs. Time")
        plt.show()        

    def plotdisplacementvtime(self):
        if self.run == False:
            self.decode()
        
        plt.plot(self.time, self.displacement)
        plt.ylabel("Displacement (mm)")
        plt.xlabel("Time (s)")
        plt.title(self.title + " Displacement vs. Time")
        plt.show()        

    def plotforcevdisplacement(self):
        if self.run == False:
            self.decode()
        
        g = plt.figure(1)
        plt.plot(self.displacement, self.force)
        plt.ylabel("Force (N)")
        plt.xlabel("Displacement (mm)")
        plt.title(self.title + " Force vs. Displacement")
        plt.show()        

    def saveexcel(self):
        df = pd.DataFrame({"Force (N)":self.force, "Displacement (mm)":self.displacement}, index = self.time)
        df.index.name = "Time (s)"
        with wx.FileDialog(frame, "Save Excel file", wildcard="XLSX files (*.xlsx)|*.xlsx",
                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

        # save the current contents in the file
            pathname = fileDialog.GetPath()

            try:
                with pd.ExcelWriter(pathname, mode = 'wb') as writer:
                        df.to_excel(writer,index=True, header=True)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)                        
   

#if __name__ == "__main__":
#    data = Analyze("pilot3.dat")
#    data.decode()
#    data.plot(data.time, data.force)
#    data.saveexcel()       
