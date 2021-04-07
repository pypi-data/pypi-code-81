import os, errno
import numpy
from scipy.linalg import qr
import math
import matplotlib.pyplot as plt

class Util:
    def __init__(self):
        pass
    def address_file(self, subDir, fileName):
        #region doc. string
        """Function to get the current file location.

        - If you change the location of the "Utils.py" file, you should revise this function.

        Parameters
            - subDir - :class:`String`. sub-directory.
            - fileName - :class:`String`. file name.
        
        Returns
            - R - :class:`String`. current path + subDir + fileName.
        """
        #endregion doc. string
        
        current_dir = os.path.dirname(__file__) #<kr> 파일이 있는 곳의 폴더.
        parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
        #parent_dir = Path(current_dir).parent
        rel_path = subDir + "/" + fileName
        abs_path = os.path.join(parent_dir, rel_path)
        
        # ⬇︎ make directory if the directory does not exist.
        if not os.path.exists(os.path.dirname(abs_path)):
            try:
                os.makedirs(os.path.dirname(abs_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        return abs_path

    def factorial(self, n):
        #region doc. string
        """factorial calculation

        Parameters
            - n - :class:`int`.
        
        Returns
            - R - :class:`int`.
        """
        #endregion doc. string
        if n == 0:
            return 1
        else:
            return n * self.factorial(n-1)


    def inducedK(self, m, n, s_k):
        #region doc. string
        """Calculating the K value for KD tree for Meshfree analysis

        Parameters
            - m - :class:`int`. Polynomial Order
            - n - :class:`int`. Problem Dimension
            - s_k - :class:`float`. Safe factor for K
        
        Returns
            - R - :class:`int`. Induced K value for KD tree
        """
        #endregion doc. string
        return int(s_k * self.factorial(m+n) / (self.factorial(m) * self.factorial(n)))


    def mldivide(self, A, b):
        #region doc. string
        """mldivide function (\ operator) of Matlab. (solving simultaneous equations (연립방정식) A*x = B)

        - ref site: https://pythonquestion.com/post/how-can-i-obtain-the-same-special-solutions-to-underdetermined-linear-systems-that-matlab-s-a-b-mldivide-operator-returns-using-numpy-scipy/
        - ref site: https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html#numpy.linalg.lstsq

        Parameters
            - [param1] - :class:`[type]`. [Description].
            - [param2] - :class:`[type]`. [Description].
        
        Returns
            - R1 ([value]) - :class:`[type]`. [Description]
            - R2 ([value]) - :class:`[type]`. [Description]
        """
        #endregion doc. string
        x1, res, rnk, s = numpy.linalg.lstsq(A, b)
        if rnk == A.shape[1]:
            return x1   # nothing more to do if A is full-rank
        Q, R, P = qr(A.T, mode='full', pivoting=True)
        Z = Q[:, rnk:].conj()
        C = numpy.linalg.solve(Z[rnk:], -x1[rnk:])
        return x1 + Z.dot(C)


    def getKeyFromValue(self, dicData, val):
        for key, value in dicData.items():
            if val == value: 
                return key 
  
        return "key doesn't exist"


    def intersectionPtBtwLineAndPt2D(self, startP, endP, exP):
        #region doc. string
        """A, B는 하나의 선분, 선분위에 있지 않는 점 P가 선분 AB에 수선의 발을 내렸을때의 교점 H 찾기. 그냥 연립방정식 푼것.
                        * B
                    -   -
              H *       -
            -       * P -
        A *--------------

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
        denominator = startP[0] - endP[0]
        numerator = startP[1] - endP[1]
        if denominator == 0 or numerator == 0:
            return "ccccccccheck"
        else:
            alpha = abs(  (startP[1] - endP[1]  ) /  ( startP[0] - endP[0] ) )
            Hx = ( -startP[1] + exP[1] + alpha * startP[0] + (1 / alpha) * exP[0] ) / (  alpha + (1 / alpha)  )
            Hy = alpha * ( Hx - startP[0] ) + startP[1]
            return (Hx, Hy, 0)

    def euclideanDistance2D(self, startP, endP):
        v = (startP[0] - endP[0])**2 + (startP[1] - endP[1])**2
        return math.sqrt(v)

    def show3dPlots(self, data:list[list[numpy.array]]):
        #region doc. string
        """[summary]

        - [Description]
        - [Description]

        Parameters
            - data - :class:`list[list[numpy.array]]`. numpy.array (x), numpy.array (y), numpy.array (z)의 리스트의 리스트.
        
        Returns
            - R1 ([value]) - :class:`[type]`. [Description]
            - R2 ([value]) - :class:`[type]`. [Description]
        """
        #endregion doc. string
        fig = plt.figure(figsize=(16,8))

        idx = 1
        for i in data:
            ax = fig.add_subplot(1,len(data),idx, projection='3d')
            ax.plot_surface(i[0], i[1], i[2], rstride=1, cstride=1, cmap='seismic', alpha=0.8)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            idx += 1

        plt.show()


    def transformFor2dLine(self, startP:list, endP:list, point:list, toXAxis=True):
        #region doc. string
        """[summary]

        - toXAxis = True이면, X 축으로 이동, False면, 원래 좌표로 이동.
        - [Description]

        Parameters
            - [param1] - :class:`[type]`. [Description].
            - [param2] - :class:`[type]`. [Description].
        
        Returns
            - R1 ([value]) - :class:`[type]`. [Description]
            - R2 ([value]) - :class:`[type]`. [Description]
        """
        #endregion doc. string
        
        deltaX = endP[0] - startP[0]
        deltaY = endP[1] - startP[1]
        centerP = [ (endP[0] + startP[0]) / 2,  (endP[1] + startP[1]) / 2]
        theta = 0
        if deltaX == 0:
            theta =  -(numpy.pi/2)
        elif deltaY == 0:
            theta = 0
        else:
            tangentTheta = deltaY / deltaX
            if tangentTheta > 0:
                temp = numpy.arctan(tangentTheta)
                theta = -1*temp
            else:
                temp = numpy.arctan(tangentTheta)
                theta = -1 * (temp + numpy.pi)

        tR = numpy.array( [[numpy.cos(theta), -numpy.sin(theta)],  [numpy.sin(theta), numpy.cos(theta)]] )
        tT = numpy.array( [[-centerP[0]],  [-centerP[1]]] )
        p = numpy.array( [ [point[0]], [point[1]]  ] )
        if (toXAxis):
            return numpy.dot(tR, (p + tT) ) 
        return numpy.dot( numpy.linalg.inv(tR), p ) - tT

