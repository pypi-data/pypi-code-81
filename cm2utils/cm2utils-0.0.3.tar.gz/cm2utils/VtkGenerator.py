import sys, os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
sys.path.append(current_dir)
sys.path.append(parent_dir)

# from GmshCP2VTK.lib.GeometryController import GeometryController

class VtkGenerator:
    def __init__(self) -> None:
        pass
    def header(self, title, vtkWriter, version=3.0, dt=1.0, fileDataTypeNum=0, dataSetNum=2):
        #region doc. string
        """To write header information.

        Parameters
            - title - :class:`string`. title of vtk file.
            - fout - :class:`io.TextIOWrapper`. Text IO wrapper. .vtk file.
            - version - :class:`float`. version of vtk file.
            - dt - :class:`float`. time step. default = 1.0
            - fileDataTypeNum - :class:`int`. file data type. 0: ASCII, 1: BINARY. default=0.
            - dataSetNum - :class:`int`. data set type. 0: STRUCTURED_POINTS, 1: STRUCTURED_GRID, 2: UNSTRUCTURED_GRID, 3: POLYDATA, 4: RECTILINEAR_GRID, 5: FIELD. default=2.
        
        Returns
            - void.
        """
        #endregion doc. string
        
        headStr = "%s %0.1f\n" % ("# vtk DataFile Version", version)
        titleStr = title + ": t=" + str(dt) + "\n"
        fileDataTypes = ("ASCII\n", "BINARY\n")
        dataSets = ("STRUCTURED_POINTS\n", "STRUCTURED_GRID\n", "UNSTRUCTURED_GRID\n", "POLYDATA\n", "RECTILINEAR_GRID\n", "FIELD\n")
        dataSetStr = "DATASET " +  dataSets[dataSetNum]
        vtkWriter.write(headStr + titleStr + fileDataTypes[fileDataTypeNum] + dataSetStr + "\n")


    def pointsData(self, dataType, vtkWriter, data=None, physicalGroupName=None):
        #region doc. string
        """To write point data

        Parameters
            - dataType - :class:`string`. data type.
            - fout - :class:`io.TextIOWrapper`. Text IO wrapper. .vtk file.
            - physicalGroupName - :class:`string`. physical group name of the gmsh model.
        
        Returns
            - void
        """
        #endregion doc. string
        head = "POINTS"
        if data is None:
            if physicalGroupName == None:
                connection = self.gc.getConnectionBetweenNodeAndCoords()
                #print (str(connection))
                n = len(connection)
                headstr = head + " " + str(n) + " " + dataType+"\n"
                vtkWriter.write(headstr)
                for _, v in connection.items():
                    for i in v:
                        vtkWriter.write(str(i) + " ")
                    vtkWriter.write("\n")
                vtkWriter.write("\nPOINT_DATA " + str(n) + "\n")
            else:
                #getConnectionBetweenNodeAndCoords()
                nodeTags = self.gc.getConnectionBetweenPhysicalGroupAndNodes(physicalGroupName=physicalGroupName, sort=True)
                n = len(nodeTags)
                headstr = head + " " + str(n) + " " + dataType+"\n"
                vtkWriter.write(headstr)

                for i in nodeTags:
                    coord = self.gc.getConnectionBetweenNodeAndCoords(nodeTag=i)
                    vtkWriter.write("%s %s %s\n" % (coord[0], coord[1], coord[2]))
                vtkWriter.write("\nPOINT_DATA " + str(n) + "\n")
        else: # apply data
            n = len(data)
            headstr = head + " " + str(n) + " " + dataType+"\n"
            vtkWriter.write(headstr)
            for i in data:
                #fout.write(str(i) + "\n")
                vtkWriter.write("%s %s %s\n" % (i[0], i[1], i[2]))
            vtkWriter.write("\nPOINT_DATA " + str(n) + "\n")

    def vectorsData(self, dataName, dataType, data, vtkWriter):
        #region doc. string
        """To write vector data

        Parameters
            - dataName - :class:`string`. data name.
            - dataType - :class:`string`. data type. ex) float
            - data - :class:`list`.
            - fout - :class:`io.TextIOWrapper`. Text IO wrapper. .vtk file.
        
        Returns
            - void
        """
        #endregion doc. string
        head = "\nVECTORS"
        headStr = head + " " + dataName + " " + dataType + "\n"
        vtkWriter.write(headStr)
        
        for i in range(len(data)):
            vtkWriter.write(str(data[i][0]) + " " + str(data[i][1]) + " " + str(data[i][2]) + "\n")
    
                