from sklearn.neighbors import KDTree

class NearestNeighbors:
    """Class to create KDTree and query the Nearest Neighbor (NN) nodes

    """
    def __init__(self, nodeCoordArray, leafSize):
        self.tree = KDTree(nodeCoordArray, leaf_size=leafSize)

    def getSKnode(self, tree, nodeCoordArray, kx, nodeNumber):
        """K-based NN query for the specific collocation point. #<kr> K-based 특정 노드에 대한 NN 쿼리.

        Parameters
            - tree - :class:`sklearn.neighbors._kd_tree.KDTree`. Sci-kit learn-based KDTree for fast generalized N-point problems.
            - nodeCoordArray - :class:`numpy.ndarray`. node coordinate. #<kr> nodeCoordArray는 좌표값이 순서대로 들어간 것이다. gmsh에서는 node가 1부터 순서대로 생성되기 때문에. nodeCoordArray의 index에 1을 더하면 gmsh의 node tag와 같은 값이 된다.
            - kx - :class:`int`. The number of nearest neighbors to return.
            - nodeNumber - :class:`int`. Tag number.
        
        Returns
            - R1 (distance) - :class:`numpy.ndarray`. #<kr> 하나의 점을 기준으로, K기반 연결점(들)(nearest neighbors)간의 거리.
            - R2 (nodeTagMinusOne) - :class:`numpy.ndarray`. #<kr> 하나의 점을 기준으로, 이들과 연결된 점(들)(nearest neighbors) id. 이 점들의 id는 gmsh에서 나타나는 node tag1 보다 1이 작다.
        """
        distance, nodeTagMinusOne = tree.query(nodeCoordArray[nodeNumber-1:nodeNumber], k=kx, dualtree=True)
        return distance, nodeTagMinusOne


    def getSRNode(self, tree, nodeCoordArray, radius, nodeNumber):
        #region doc. string
        """R-based NN query for the specific collocation point. #<kr> Radius-based 특정 노드에 대한 NN 쿼리.

        Parameters
            - tree - :class:`sklearn.neighbors._kd_tree.KDTree`. Sci-kit learn-based KDTree for fast generalized N-point problems.
            - nodeCoordArray - :class:`numpy.ndarray`. node coordinate. #<kr> nodeCoordArray는 좌표값이 순서대로 들어간 것이다. gmsh에서는 node가 1부터 순서대로 생성되기 때문에. nodeCoordArray의 index에 1을 더하면 gmsh의 node tag와 같은 값이 된다.
            - radius - :class:`float`. Distance within which neighbors are returned.
            - nodeNumber - :class:`int`. Tag number.
        
        Returns
            - R1 (distance) - :class:`numpy.ndarray`. #<kr> 하나의 점을 기준으로, R기반 연결점(들)(nearest neighbors)간의 거리.
            - R2 (nodeTagMinusOne) - :class:`numpy.ndarray`. #<kr> 하나의 점을 기준으로, 이들과 연결된 점(들)(nearest neighbors) id. 이 점들의 id는 gmsh에서 나타나는 node tag1 보다 1이 작다.
        """
        #endregion doc. string
        nodeTagMinusOne, distance = tree.query_radius(nodeCoordArray[nodeNumber-1:nodeNumber], r=radius, return_distance=True, sort_results=True)
        return distance, nodeTagMinusOne

    
    #<kr> Python은 일반적인 다른 랭귀지에서의 method overload가 안됨. 변수를 가변적으로 받을 수 있어서 그런듯.
    def getNodes(self, tree, nodeCoordArray, var):
        #region doc. string
        """Get the nearest neighbor (NN) nodes.

        - If var is an integer type, K-based NNs are returned.
        - If var is a float type, radius-based NNs are returned.

        Parameters
            - tree - :class:`sklearn.neighbors._kd_tree.KDTree`. Sci-kit learn-based KDTree for fast generalized N-point problems.
            - nodeCoordArray - :class:`numpy.ndarray`. node coordinate. #<kr> nodeCoordArray는 좌표값이 순서대로 들어간 것이다. gmsh에서는 node가 1부터 순서대로 생성되기 때문에. nodeCoordArray의 index에 1을 더하면 gmsh의 node tag와 같은 값이 된다.
            - var - :class:`int` or :class:`float`. Query parameter of the KD tree. 
        
        Returns
            - R1 (distance) - :class:`numpy.ndarray`.
            - R2 (nodeTagMinusOne) - :class:`numpy.ndarray`. #<kr> 하나의 점을 기준으로, 이들과 연결된 점(들)(nearest neighbors) id. 이 점들의 id는 gmsh에서 나타나는 node tag1 보다 1이 작다.
        """
        #endregion doc. string

        if type(var) is int:
            distance, nodeTagMinusOne = self.__getNodes_int(tree, nodeCoordArray, var) # var = k
            return distance, nodeTagMinusOne
        elif type(var) is float:
            distance, nodeTagMinusOne = self.__getNodes_flot(tree, nodeCoordArray, var) # var = radius
            return distance, nodeTagMinusOne

        else:
            print("neither")

    # private function
    def __getNodes_int(self, tree, nodeCoordArray, var): # var = k
        #region doc. string
        """Get the K-based nearest neighbor (NN) nodes.

        Parameters
            - tree - :class:`sklearn.neighbors._kd_tree.KDTree`. Sci-kit learn-based KDTree for fast generalized N-point problems.
            - nodeCoordArray - :class:`numpy.ndarray`. node coordinate. nodeCoordArray는 좌표값이 순서대로 들어간 것이다. gmsh에서는 node가 1부터 순서대로 생성되기 때문에. nodeCoordArray의 index에 1을 더하면 gmsh의 node tag와 같은 값이 된다.
            - var - :class:`int`. The number of nearest neighbors to return. 
        
        Returns
            - R1 (distance) - :class:`numpy.ndarray`.
            - R2 (nodeTagMinusOne) - :class:`numpy.ndarray`. #<kr> 하나의 점을 기준으로, 이들과 연결된 점(들)(nearest neighbors) id. 이 점들의 id는 gmsh에서 나타나는 node tag1 보다 1이 작다.
        """
        #endregion doc. string

        #<kr> nodeCoordArray는 좌표값이 순서대로 들어간 것이다. gmsh에서는 node가 1부터 순서대로 생성되기 때문에
        #<kr> 일단은 nodeCoordArray의 index에 1을 더하면 gmsh의 node tag와 같은 값이 된다.
        #<kr> nodeTagMinusOne은 gmsh의 node tag와 비교해서 1이 작다는 것을 알리기 위해서 이름을 이렇게 지은것.
        distance, nodeTagMinusOne = tree.query(nodeCoordArray[:], k=var, dualtree=True)
        
        return distance, nodeTagMinusOne

        
    def __getNodes_flot(self, tree, nodeCoordArray, var): # var = radius
        #region doc. string
        """Get the radius-based nearest neighbor (NN) nodes.

        Parameters
            - tree - :class:`sklearn.neighbors._kd_tree.KDTree`. Sci-kit learn-based KDTree for fast generalized N-point problems.
            - nodeCoordArray - :class:`numpy.ndarray`. node coordinate. #<kr> nodeCoordArray는 좌표값이 순서대로 들어간 것이다. gmsh에서는 node가 1부터 순서대로 생성되기 때문에. nodeCoordArray의 index에 1을 더하면 gmsh의 node tag와 같은 값이 된다.
            - var - :class:`float`. Distance within which neighbors are returned. 
        
        Returns
            - R1 (distance) - :class:`numpy.ndarray`.
            - R2 (nodeTagMinusOne) - :class:`numpy.ndarray`. #<kr> 하나의 점을 기준으로, 이들과 연결된 점(들)(nearest neighbors) id. 이 점들의 id는 gmsh에서 나타나는 node tag1 보다 1이 작다.
        """
        #endregion doc. string
        nodeTagMinusOne, distance = tree.query_radius(nodeCoordArray[:], r=var, return_distance=True, sort_results=True)

        return distance, nodeTagMinusOne

        
        
        
        
        
