from os import error
import sys, os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
parent_dir2 = os.path.abspath(os.path.join(parent_dir, os.path.pardir))
sys.path.append(parent_dir2)

import re
# from Utils import Util

class OutputFileParams:
    #region doc. string
    """Class to save outputCtrl file to input variables.

    - #<kr> left안에 있는 변수들 이름과 attributes의 이름이 완전히 같아야 함. 순서는 상관없음.

    Parameters
        - lefts - :class:`tuple`. Input parameter tuple.
        - title - :class:`string`. The title of the file.
        - geo_file - :class:`string`.
        - file_type - :class:`string`. ex) vtk
        - initial_discretization - :class:`bool`.
        - physical_group - :class:`bool`. Whether to apply the physical group.
    
    """
    #endregion doc. string
    lefts = ("title", "geo_file", "file_type", "initial_discretization", "physical_group")
    title = None
    geo_file = None
    file_type = None
    initial_discretization = None
    physical_group = None

    def __init__(self, outputCtrlFile):
        #region doc. string
        """Constructor of the OutputFileParams class.

        Parameters
            - outputCtrlFile - :class:`string`. output control file name.
        
        Returns
            - void
        """
        #endregion doc. string
        #self.__extractParamsFromFile(ctrlFile)
        FileController().extractParamsFromFile(OutputFileParams, outputCtrlFile)

class NeighborParams:
    #region doc. string
    """Class to save neighborCtrl file to input variables.

    - #<kr> class OutputFileParams 과 같은 기능을 함.

    Parameters
        - lefts - :class:`tuple`. Input parameter tuple.
        - nearest_neighbor - :class:`bool`. Whether to apply the nearest neigbors.
        - leaf_size - :class:`int`. 
        - NN_number - :class:`int`. 
        - NN_radius - :class:`float`. 
        - Order_of_Polynomial - :class:`int`. = m. 1 <= m <= 6.
        - Problem_Dimension - :class:`int`. = n. 1 <= n <= 3.
        - Safety_Factor_for_K - :class:`float`. = s_k. 1.0 <= s_k <= 3.0.
        - Safety_Factor_for_R - :class:`float`. = s_r. 1.0 <= s_k <= 3.0.
    
    """
    #endregion doc. string
    lefts = ("nearest_neighbor", "leaf_size", "NN_number", "NN_radius", 
        "Order_of_Polynomial", "Problem_Dimension", "Safety_Factor_for_K", "Safety_Factor_for_R", "Top_op")
    nearest_neighbor = None
    leaf_size = None
    NN_number = None
    NN_radius = None
    Order_of_Polynomial = None
    Problem_Dimension = None
    Safety_Factor_for_K = None
    Safety_Factor_for_R = None
    Top_op = None

    def __init__(self, neighborCtrlFile):
        #region doc. string
        """Constructor of the OutputFileParams class.

        Parameters
            - neighborCtrlFile - :class:`string`. neighbor control file name.
        
        Returns
            - void
        """
        #endregion doc. string
        FileController().extractParamsFromFile(NeighborParams, neighborCtrlFile)

class FileController:
    #region doc. string
    """file controller
    
    """
    #endregion doc. string
    def __init__(self):
        pass
    def extractParamsFromFile(self, className, ctrlFile):
        #region doc. string
        """To extract parameters from the output control file.

        Parameters
            - className - :class:`string`. Class name, including the defined attributes.
            - ctrlFile - :class:`string`. output control file name.
        
        Returns
            - void
        """
        #endregion doc. string

        # ctrler = open(Util().address_file("inp", ctrlFile), 'r')
        ctrler = open(ctrlFile, 'r')
        
        pVal = {} # dict. that contains lefts (keys) and rights (values) of the output ctrl file.
        for x in ctrler:
            x = x.strip()
            #<kr> ⬇︎ output control file의 주석 처리.
            #<kr> '#'을 검색해서, 처음 시작이면 그 줄을 건너뛰고, 줄의 중간에 있으면 그 뒷부분 다 삭제.
            co = re.search(r'(#)', x)
            if co is not None:
                x = x[:co.start()].strip()

            if x != "":
                di = re.search(r'(=)', x)
                if di is not None:
                    leftE = x[:di.start()].strip()
                    rightE = x[di.start()+1:].strip()
                    pVal[leftE] = rightE
                else:
                    print("WARNING: Check the input string")
        #if sorted(tuple(pVal.keys())) == sorted(OutputFileParams.lefts):
        if sorted(tuple(pVal.keys())) == sorted(className.lefts):
            #for i in OutputFileParams.lefts:
            for i in className.lefts:
                if self.__typeChecker(pVal[i]):
                    #print("OutputFileParams."+i + "=" + pVal[i])
                    print(className.__name__+ "."+i + "=" + pVal[i])
                    #exec("OutputFileParams."+i + "=" + pVal[i])
                    exec(className.__name__ + "."+i + "=" + pVal[i])
                else:
                    #print("OutputFileParams."+i + "=" + "\"" + str(pVal[i]) + "\"")
                    print(className.__name__ + "."+i + "=" + "\"" + str(pVal[i]) + "\"")
                    #exec("OutputFileParams."+i + "=" + "\"" + str(pVal[i]) + "\"")
                    exec(className.__name__ + "."+i + "=" + "\"" + str(pVal[i]) + "\"")

        else:
            print("ERROR: Wrong parameter name")
            #print(self.__diffx(InputParams.lefts, tuple(pVal.keys())))
            raise error
            
        ctrler.close()

    def __typeChecker(self, val):
        if (val == "True") or (val == "False") or (val == "None"):
            return True
        elif re.match(r'(list\(range\()', val):
            return True
        elif re.match(r'(numpy\.linspace\()', val):
            return True
        try:
            int(val)
            return True
        except ValueError:
            try:
                float(val)
                return True
            except ValueError:
                return False
        return False
    
    def __diffx(self, l1, l2):
        li_dif = [i for i in l1 if i in l1 and i not in l2]
        return li_dif