import numpy
from scipy.spatial import Voronoi

class VoronoiController:
    #region doc. string
    """scipy.spatial.Voronoi-based data controller
    """
    #endregion doc. string
    def __init__(self, inputPoints:numpy.array) -> None:
        self.inputPoints = inputPoints
        print("self.input points\n", self.inputPoints)
        self.vor = Voronoi(inputPoints)
        
    def getRegionFromPoint(self, pt:list=None):
        #region doc. string
        """입력 포인트를 중심점으로 갖는 voronoi diagram 반환. voronoi diagram은 vertex index의 list 임.
        
        - [Description]

        Parameters
            - pt - :class:`list`. 2D/3D point coord.
        
        Returns
            - R1 (rValue) - :class:`dict{int, list(int)}`. If pt == None. {region idx, [vertex idx]}.
            - R2 (reg) - :class:`list(int)`. If pt != None. [vertex idx].
        """
        #endregion doc. string
        #<kr> ⬇︎ pt가 None이 아니면, 특정 포인트를 대상으로 수행.
        if (not pt is None):
            # print("*"*50)
            checker = numpy.where( (self.inputPoints == pt).all(axis=1)   )
            
            if (not len(checker[0]) is 0 ):
                print("pt: ", pt)
                for i, reg in enumerate(self.vor.regions):
                    if len(reg) == 0:
                        pass
                    elif (checker[0][0] == numpy.where(self.vor.point_region == i)[0][0]):
                        return reg
            else:
                print("Error")
        #<kr> ⬇︎ pt가 None이면 전체 center point index (vor.points)와 region index (vor.vertices) list 리턴.
        else:
            rValue = {}
            for i, reg in enumerate(self.vor.regions):
                if len(reg) == 0:
                    pass
                else:
                    rValue[numpy.where(self.vor.point_region == i)[0][0]] = reg
            return rValue
            
    def getAdjacentsFromRegion(self, region:list, order=1):
        #region doc. string
        """region (vertex 들이 있는 list)을 구성하는 vertex를 공유하는 다른 region의 index를 리턴.
        
        - input이 region. 즉, getRegionFromPoint를 사용해서 가져온 region을 입력 변수로 사용.
        - order =1: 한단계 확장, order = 2: 두단계 확장, ...

        Parameters
            - region - :class:`list`. [vertex idx].
            - order - :class:`int`. order >= 1.
        
        Returns
            - R (rValue) - :class:`list(list(int))`. 전체 값 중 제일 앞의 값 (rValue[0][0])은 입력 region의 index.
        """
        #endregion doc. string
        rValue = []
        iter = 0
        # region index 찾기.
        ipRegIdx = -1
        for i, target in enumerate(self.vor.regions):
            if (region is target):
                ipRegIdx = i
                break

        adjacent = []
        for r in region:
            for i, target in enumerate(self.vor.regions):
                 # 일단, 입력한 region은 제외 (i == ipRegIdx)
                if len(target) == 0 or i == ipRegIdx:
                    pass
                else:
                    if (r != -1 and r in target):
                        if (not i in adjacent):
                            adjacent.append(i)
        adjacent.insert(0, ipRegIdx) # 제일 앞에 입력한 region을 넣어줌.
        rValue.append(adjacent)

        iter += 1
        while order > iter:
            tempRegion = []
            for d in rValue:
                # for i in adjacent:
                for i in d:
                    regionVertexList = self.vor.regions[i] #<kr> region을 구성하는 vertex list.
                    ttemp = self.getAdjacentsFromRegion(regionVertexList)[0]
                    for j in ttemp:
                        if (self.__eleInList(j, rValue)) or (j in tempRegion):
                            continue
                        else:
                            tempRegion.append(j)
                        
            rValue.append(tempRegion)
            iter += 1

        # return adjacent
        return rValue

    def isOpenTypeRegion(self, regionIdx:int):
        #region doc. string
        """To check the given region is open type or not.

        Parameters
            - regionIdx - :class:`int`. [Description].
        
        Returns
            - R - :class:`boolean`. If the region is open type, return TRUE, or closed type, return FALSE.
        """
        #endregion doc. string
        if (-1 in self.vor.regions[regionIdx]):
            return True
        return False

    def getRegionVerticesFromRegionIdx(self, regionIdx:int):
        #region doc. string
        """To get the coordinates of the region

        Parameters
            - regionIdx - :class:`int`. [Description].
        
        Returns
            - R (rValue) - :class:`list(numpy.array)`. [Description]
        """
        #endregion doc. string
        rValue = []
        vertexList = self.vor.regions[regionIdx] # vertex list
        for i in vertexList:
            if (i == -1):
                rValue.append("Open Type")
            else:
                rValue.append(    self.vor.vertices[i]                )
        return rValue
        
    def __eleInList(self, source:int, target:list[list]):
        for i in target:
            if (source in i):
                return True
        return False