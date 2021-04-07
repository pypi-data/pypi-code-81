import sys
import gmsh
import numpy
from numpy.core.defchararray import not_equal

class GeometryController:
    #region doc. string
    """Class to control geometric information of the Gmsh model.
    """
    #endregion doc. string
    def __init__(self, fileName=None, dim=3):
        
        
        if not fileName is None:
            # initialize gmsh
            gmsh.initialize(sys.argv)
            gmsh.open(fileName)
            print("File name: " + fileName)
            print("Model name: " + gmsh.model.getCurrent())
            # generate n-dimensional meshes
            gmsh.model.mesh.generate(dim)
        
        #region entire object - attributes
        self.__nodeTags = None
        self.__nodesCoordinates = None
        self.__nodesOnBoundaries = None
        self.__meshTags = None
        self.__boundaryTags = None
        self.__physicalGroups = None
        self.__physicalGroups1D = None
        

        self.__connection_nodeAndCoords = None
        self.__connection_boundaryAndNodes = None
        self.__connection_meshAndNodes = None
        #endregion entire object - attributes

        #region object by physical group - attributes
        self.__connection_physicalGroup1dAndNodes = None
        self.__connection_physicalGroupAndNodes = None
        self.__connection_physicalGroupAndNormals = None
        #endregion object by physical group - attributes
        self.__connection_nodesAndIntegratedNormals = None

        self.__isGeometricInfo = False

        self.__genGeometricInfo()
        if not fileName is None: gmsh.finalize()

    def __genGeometricInfo(self):
        #region doc. string
        """Function to get all of the geometry-related information.
        
        Returns
            - void
        """
        #endregion doc. string

        #region entire object - method
        nodeTags, nodeCoords, _ = gmsh.model.mesh.getNodes()
        
        nodeAndCoord = {}
        for i in range(0, len(nodeTags)):
            coordTuple = tuple(nodeCoords[i*3:i*3+3])
            if not nodeTags[i] in nodeAndCoord:
                nodeAndCoord[nodeTags[i]] = coordTuple
            else:
                nodeAndCoord[nodeTags[i]].append(coordTuple)

        # get connection between boundary and nodes
        boundaryTags, boundaryMesh_nodes = gmsh.model.mesh.getElementsByType(1)
        connection_boundaryAndNodes, nodesOnBoundaries = self.__getConnection(2, boundaryMesh_nodes, boundaryTags)

        # get connection between mesh and node
        meshTags, triMesh_nodes = gmsh.model.mesh.getElementsByType(2)
        connection_meshAndNodes, nodesOnMeshes = self.__getConnection(3, triMesh_nodes, meshTags)
        
        self.__nodeTags = nodeTags
        #self._nodeCoordinates = Coords(nodeCoords.reshape((-1,3)))
        self.__nodesCoordinates = nodeCoords.reshape((-1,3))
        self.__connection_nodeAndCoords = nodeAndCoord

        self.__boundaryTags = boundaryTags
        self.__connection_boundaryAndNodes = connection_boundaryAndNodes
        self.__nodesOnBoundaries = nodesOnBoundaries

        self.__meshTags = meshTags
        self.__connection_meshAndNodes = connection_meshAndNodes

        #endregion entire object - method

        #region object by physical group - method

        # 1D
        physicalGroups1D = []
        connection_physicalGroup1dAndNodes = {}
        gt1 = gmsh.model.getPhysicalGroups(1)
        for tag in gt1:
            physicalGroupName = gmsh.model.getPhysicalName(tag[0], tag[1])
            physicalGroups1D.append(physicalGroupName)
            nodes4PhysicalGroup, _ = gmsh.model.mesh.getNodesForPhysicalGroup(tag[0], tag[1])
            connection_physicalGroup1dAndNodes[physicalGroupName] = nodes4PhysicalGroup
        
        self.__physicalGroups1D = physicalGroups1D
        self.__connection_physicalGroup1dAndNodes = connection_physicalGroup1dAndNodes

        # 2D and 3D
        physicalGroups = []
        connection_physicalGroupAndNodes = {}
        connection_physicalGroupAndNormals = {}
        
        
        gt2 = gmsh.model.getPhysicalGroups(2)
        # print(gt2)
        # print(gmsh.model.getEntities(2))
        

        for tag in gt2:
            # surfX = tag[1] #tag[0] = dimension, tag[1] = object tag
            # physicalGroupName = gmsh.model.getPhysicalName(2, surfX)
            # physicalGroups.append(physicalGroupName)
            # nodes4PhysicalGroup, _ = gmsh.model.mesh.getNodesForPhysicalGroup(2, surfX)
            # connection_physicalGroupAndNodes[physicalGroupName] = nodes4PhysicalGroup
            physicalGroupName = gmsh.model.getPhysicalName(tag[0], tag[1])
            physicalGroups.append(physicalGroupName)
            nodes4PhysicalGroup, _ = gmsh.model.mesh.getNodesForPhysicalGroup(tag[0], tag[1])
            connection_physicalGroupAndNodes[physicalGroupName] = nodes4PhysicalGroup


        
        # IMPORTANT: We have to use 'parametric coord' to get the normal vector 
        # of the collocation points according to the surface. 
        # We can get it using the 'gmsh.model.mesh.getNodes' method. 
        # But sometimes, this method returns the wrong physical group name. 
        # In the 2D surface model case, it seems that name returns correctly, 
        # but the 3D volume case returns the wrong name. 
        # I think I don't understand this method of the Gmsh API properly, or it might be a bug. 
        # So I reassigned the physical group name using the below process. 
        # However, this is a temporary step, so that it may contain some errors.
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # ➡︎ *It seems that I fix it.*
        # for tag in gt2:
            # surf = tag[1] #tag[0] = dimension, tag[1] = object tag
            #<kr> physical group에서 가져오는 tag와 entity tag는 다름. 즉, ⬆︎의 surf는 physical group에서 가져온 tag고, ⬇︎ surf는 entity tag임.
            #<kr> 그림을 포함한 좀 더 자세한 설명은 obsidian://open?vault=Primary&file=CodeTips%2Fgmsh%20entity%20tag
            surf = (gmsh.model.getEntitiesForPhysicalGroup(tag[0], tag[1]))[0]
            nTags, _, paramCoord = gmsh.model.mesh.getNodes(2, surf, True)
            # realPhysicalGroupName = ""
            # for k, v in connection_physicalGroupAndNodes.items():
            #     if sorted(nTags) == sorted(v):
            #         realPhysicalGroupName = k
            #         break

            connection_nodeAndNormals = {}
            
            normals = gmsh.model.getNormal(surf, paramCoord)
            tagIndex = 0
            #for i in nodes4PhysicalGroup:
            for i in nTags:
                temp = [normals[tagIndex], normals[tagIndex+1], normals[tagIndex+2]]
                connection_nodeAndNormals[i] = temp
                tagIndex += 3
                
            connection_physicalGroupAndNormals[physicalGroupName] = connection_nodeAndNormals
            #connection_physicalGroupAndNormals[realPhysicalGroupName] = connection_nodeAndNormals
            
        gt3 = gmsh.model.getPhysicalGroups(3)
        for tag in gt3:
            # physicalGroupName = gmsh.model.getPhysicalName(3, tag[1])
            physicalGroupName = gmsh.model.getPhysicalName(tag[0], tag[1])
            #⬇︎ There are not normal vector of the 3D physical group
            #physicalGroups.append(physicalGroupName)
            # nodes4PhysicalGroup, coord4PhysicalGroup = gmsh.model.mesh.getNodesForPhysicalGroup(3, tag[1])
            nodes4PhysicalGroup, coord4PhysicalGroup = gmsh.model.mesh.getNodesForPhysicalGroup(tag[0], tag[1])
            connection_physicalGroupAndNodes[physicalGroupName] = nodes4PhysicalGroup
        
        self.__physicalGroups = physicalGroups
        self.__connection_physicalGroupAndNodes = connection_physicalGroupAndNodes
        self.__connection_physicalGroupAndNormals = connection_physicalGroupAndNormals
        
        #endregion object by physical group - method

        #region - integrated normal vector
        nodesAndIntegratedNormals = {}
        for i in self.__physicalGroups:
            dicPandB = self.__connection_physicalGroupAndNormals[i]
            for p, b in dicPandB.items():
                if p in nodesAndIntegratedNormals:
                    temp = numpy.array(b) + numpy.array(nodesAndIntegratedNormals[p])
                    nodesAndIntegratedNormals[p] = (temp / numpy.linalg.norm(temp)).tolist()
                else:
                    nodesAndIntegratedNormals[p] = b
        self.__connection_nodesAndIntegratedNormals = nodesAndIntegratedNormals
            
        #endregion - integrated normal vector


        self.__isGeometricInfo = True
        

    def getNodeTags(self, sort=False):
        #region doc. string
        """Function to get all node tags of meshes.

        Parameters
            - sort - :class:`bool`. Sorting tags.
        
        Returns
            - node tags - :class:`numpy.ndarray<int>`. If sort == False.
            - node tags - :class:`list<int>`. If sort == True.
        """
        #endregion doc. string
        if (sort):
            return sorted(self.__nodeTags)
        
        return self.__nodeTags
        
    def getNodesCoordinates(self):
        #region doc. string
        """Function to get all coordinates of the nodes.
        
        Returns
            - node coordinates - :class:`numpy.ndarray<numpy.ndarray<double>>`. sorted.
        """
        #endregion doc. string
        return self.__nodesCoordinates

    def getConnectionBetweenNodeAndCoords(self, nodeTag=None):
        #region doc. string
        """Function to generate the connection between nodes and coordinates.

        Parameters
            - nodeTag - :class:`int`. Tag of a node.
        
        Returns
            - connection - :class:`dict{numpy.uint64, tuple<double>}`. sorted. If nodeTag == None. 
            - coordinates - :class:`tuple<double>`. If nodeTag != None
        """
        #endregion doc. string
        if (nodeTag==None):
            return self.__connection_nodeAndCoords
        else:
            return self.__connection_nodeAndCoords[nodeTag]
    

    def getBoundaryTags(self, sort=False):
        #region doc. string
        """Function to get 1D element tags on the boundaries.

        Parameters
            - sort - :class:`bool`. sort option.
        
        Returns
            - boundary tags - :class:`numpy.ndarray<int>`. If sort == False.
            - boundary tags - :class:`list<int>`. If sort == True.
        """
        #endregion doc. string
        if (sort):
            return sorted(self.__boundaryTags)
        return self.__boundaryTags

    def getNodesOnBoundaries(self):
        #region doc. string
        """Function to get all collocation point tags of boundaries.
        
        Returns
            - 1D element tags on boundaries - :class:`list<int>`.
        """
        #endregion doc. string
        return self.__nodesOnBoundaries


    def getMeshTags(self, sort=False):
        #region doc. string
        """Function to get all mesh tags.

        Parameters
            - sort - :class:`bool`. sort option.
        
        Returns
            - mesh tags - :class:`numpy.ndarray<int>`. If sort == True.
            - mesh tags - :class:`list<int>`. If sort == False.
        """
        #endregion doc. string
        if (sort):
            return sorted(self.__meshTags)
        return self.__meshTags
    
    def getConnectionBetweenMeshAndNodes(self, meshTag=None):
        #region doc. string
        """Function to generate a connection between mesh and nodes.

        Parameters
            - meshTag - :class:`int`. Tag of a mesh.
        
        Returns
            - connection - :class:`dict{Int, tuple<int>}`. If nodeTag == None.
            - node tags - :class:`tuple<int>`. If nodeTag != None.
        """
        #endregion doc. string
        if (meshTag==None):
            return self.__connection_meshAndNodes
        return self.__connection_meshAndNodes[meshTag]

    
    def getConnectionBetweenPhysicalGroup1dAndNodes(self, physicalGroupName=None, sort=False):
        #region doc. string
        """TODO: 리스트의 처음 두개의 값을 시작점과 끝점으로 간주. 체크해보니 일단은 맞는데, 앞으로 어떨지는 모르겠음.

        - [Description]
        - [Description]

        Parameters
            - [param1] - :class:`[type]`. [Description].
            - [param2] - :class:`[type]`. [Description].
        
        Returns
            - R1 ([value]) - :class:`[type]`. [Description]
            - R2 ([value]) - :class:`[type]`. [Description]
        """
        #endregion doc. string
        if (physicalGroupName==None):
            return self.__connection_physicalGroup1dAndNodes
        else:
            if (physicalGroupName in self.__connection_physicalGroup1dAndNodes):
                if (sort):
                    return sorted(self.__connection_physicalGroup1dAndNodes[physicalGroupName])
                return self.__connection_physicalGroup1dAndNodes[physicalGroupName]
            print("************* error *************\n" + "There's no physical name '" + physicalGroupName + "' in the model.\n" + "*********************************\n")

    def getConnectionBetweenPhysicalGroupAndNodes(self, physicalGroupName=None, sort=False):
        #region doc. string
        """Function to get a connection between physical group (2-, 3-dimension) and node tags.

        - If you want to get all physical group names, use `dict.keys().`

        Parameters
            - physicalGroupName - :class:`String`.
            - sort - :class:`bool`.
        
        Returns
            - connections - :class:`dict{String, numpy.ndarray<int>}`. If physicalGroupName == None.
            - nodes - :class:`numpy.ndarray<int>`.  If physicalGroupName != None, and sort == False.
            - nodes - :class:`list<int>`.  If physicalGroupName != None, and sort == True.
        """
        #endregion doc. string
        if (physicalGroupName==None):
            return self.__connection_physicalGroupAndNodes
        else:
            if (physicalGroupName in self.__connection_physicalGroupAndNodes):
                if (sort):
                    return sorted(self.__connection_physicalGroupAndNodes[physicalGroupName])
                return self.__connection_physicalGroupAndNodes[physicalGroupName]
            print("************* error *************\n" + "There's no physical name '" + physicalGroupName + "' in the model.\n" + "*********************************\n")


    def getConnectionBetweenPhysicalGroupAndNormals(self, physicalGroupName=None, integration=False, nodeTag=-1):
        #region doc. string
        """Function to get a connection between physical group (2-dimension) and the normal vector.

        Parameters
            - physicalGroupName - :class:`String`.
            - nodeTag - :class:`int`.
        
        Returns
            - connections - :class:`dict{String, list<double>}`. If physicalGroupName == None.
            - normal vector - :class:`list<int>`.  If physicalGroupName != None, and node tag is valid.
        """
        #endregion doc. string
        if (physicalGroupName==None):
            if (not integration):
                    return self.__connection_physicalGroupAndNormals
            else:
                if (nodeTag in self.__nodeTags):
                    return self.__connection_nodesAndIntegratedNormals[nodeTag]
                return self.__connection_nodesAndIntegratedNormals
        else:
            if (physicalGroupName in self.__connection_physicalGroupAndNodes):
                if (nodeTag in self.__connection_physicalGroupAndNodes[physicalGroupName]):
                    return self.__connection_physicalGroupAndNormals[physicalGroupName][nodeTag]
                print("************* error *************\n" + "There's no node No. '" + str(nodeTag) + "' in '" + physicalGroupName + "' in the model.\n" + "*********************************\n")
                return self.__connection_physicalGroupAndNodes[physicalGroupName]
            print("************* error *************\n" + "There's no physical name '" + physicalGroupName + "' in the model.\n" + "*********************************\n")
    
    def getPhysicalGroups1D(self):
        #region doc. string
        return self.__physicalGroups1D

    def getPhysicalGroups(self):
        #region doc. string
        """Function to get the names of the 2D physical groups.

        Parameters
            - void.
        
        Returns
            - physicalGroupName - :class:`str`.
        """
        #endregion doc. string
        return self.__physicalGroups
    

    def __getConnection(self, connectedNodeDim:int, nodes, meshes):
        #region doc. string
        """Connections between boundary or triangular mesh and nodes.

        - EX) Connection between Boundary edge tag and Node tags - {82: (1, 13), 83: (13, 14),...}
        - EX) Connection between Triangular element tag and Node tags - {7: (6, 21, 38), 8: (34, 40, 51), 9: (17, 40, 51),...}

        Parameters
            - connectedNodeDim - :class:`int`. The number of vertices of the object to generate connections. boundary = 2, triangle = 3.
            - nodes - :class:`list<int>`. [Description].
            - meshes - :class:`list<int>`. The tag list of objects for generating connections.
        
        Returns
            - connections - :class:`Dict{Int, List<Int>}`. [Description]
            - nodes on objects - :class:`List`. [Description]
        """
        #endregion doc. string
        connections = {}
        objects = []
        nodesOnObjects = []
        for i in range(0, len(nodes), connectedNodeDim):
            nodesOnObjects.extend(nodes[i:i+connectedNodeDim])
            nodesOnObjects = list(set(nodesOnObjects))
            nodeTuple = tuple(sorted(nodes[i:i+connectedNodeDim]))
            objects.append(nodeTuple)
            elementTag = meshes[int(i/connectedNodeDim)]
            
            if not elementTag in connections:
                connections[elementTag] = nodeTuple
            else:
                connections[elementTag].append(nodeTuple)

        return connections, nodesOnObjects



    def gmshClose(self):
        gmsh.finalize()

