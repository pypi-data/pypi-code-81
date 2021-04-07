if __name__ == "__main__":
    import sys, os
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
    parent_dir2 = os.path.abspath(os.path.join(parent_dir, os.path.pardir))
    sys.path.append(parent_dir2)

import numpy
from scipy import sparse

###from PDMApp.Util_module.Utils import Util
from cm2utils.Utils import Util
###from PDMApp.DiffOp_module.Taylor import taylor_poly_vec_P
from cm2diffop.Taylor import taylor_poly_vec_P

class Calc_diff_ops:
    def __init__(self):
        pass
    def calc_diff_ops_1d(self):
        pass
    def calc_diff_ops_2d(self):
        pass
    #   calc_diff_ops_gen(   coord, dilp, top_op, nblist,            poly_order,      TEST)
    def calc_diff_ops_3d(self, gc, dilp, top_op, nodeTagsMinusOne4K, poly_order, dim, TEST, fout=None):
        #region doc. string
        """description

        - Ver. 0.1의 calc_diff_ops_3d.m
        - Ver. 0.2의 calc_diff_ops_gen.m

        Parameters
            - [param1] - :class:`[type]`. [Description].
            - [param2] - :class:`[type]`. [Description].
        
        Returns
            - R1 ([value]) - :class:`[type]`. [Description]
            - R2 ([value]) - :class:`[type]`. [Description]
        """
        #endregion doc. string
        #                          dilp, nblist,             poly_order,      TEST
        print("calc_diff_ops_3d")

        Diff_Op = []
        
        n_node = len(nodeTagsMinusOne4K)

        # peter comment: polynomial terms for given order and dimension
        Lp = Util().factorial(poly_order+dim) / ( Util().factorial(poly_order) * Util().factorial(dim))
        fout.write("%s %s\n" % ("poly_order: ", poly_order))
        fout.write("%s %s\n" % ("Lp: ", Lp))
        #Lt = factorial(top_op+dim)/(factorial(top_op)*factorial(dim));
        Lt = Util().factorial(top_op+dim) / ( Util().factorial(top_op) * Util().factorial(dim) )
        fout.write("%s %s\n" % ("top_op: ", top_op))
        fout.write("%s %s\n" % ("Lt: ", Lt))

        #node_analyze = zeros(4,n_node);
        node_analyze = numpy.zeros((4, n_node))

        for NN in nodeTagsMinusOne4K:
            node_p = NN[0]+1  #<kr> NN[0]: 기준 점 tag - 1.
            coord_p = gc.getConnectionBetweenNodeAndCoords(node_p)
            dilp_p = dilp[NN[0]]

            # peter comment: Pre-alllocate memory to calculate diff ops at point, p
            M_p = numpy.zeros((int(Lp), int(Lp)))
            b_p = numpy.zeros((int(Lp), n_node))
            b_p = numpy.asmatrix(b_p)


            for tag in NN:
                node_q = tag+1
                coord_q = gc.getConnectionBetweenNodeAndCoords(node_q)
                # peter comment:
                # The normalized distance from point, p to point, q. 
                # Notes, the normalize distance will always <= 1 
                # when we calcaulate the dialation parameter based on a specified number of neighbors, 
                q2p_norm_dist = numpy.linalg.norm(numpy.array(coord_p) - numpy.array(coord_q)) / dilp_p

                # preter comment: The weight function 
                wgt_p2q =(1.0 - q2p_norm_dist)**4

                # peter comment: Aquire the polynomial coeffiecnets (these are scaled by dilp)
                P_coeff_trans = taylor_poly_vec_P(coord_p, coord_q, dilp_p, poly_order, Lp, dim)
                P_coeff = numpy.reshape(P_coeff_trans, (len(P_coeff_trans),1))

                # peter comment: Update the "moment" matrix
                M_p = M_p + P_coeff * wgt_p2q * P_coeff_trans

                # peter comment: Update the b matrix 
                b_p[:,tag] = P_coeff * wgt_p2q

                # fout.write("="*30+"\n")
                # fout.write("%s: %s\n" % ("node_p", node_p))
                # fout.write("%s: %s\n" % ("node_q", node_q))
                # fout.write("%s: %s\n" % ("dilp_p", dilp_p))
                # fout.write("%s: %s\n" % ("numpy.array(coord_p)", numpy.array(coord_p)))
                # fout.write("%s: %s\n" % ("numpy.array(coord_q)", numpy.array(coord_q)))
                # fout.write("%s: %s\n" % ("numpy.array(coord_p) - numpy.array(coord_q)", numpy.array(coord_p) - numpy.array(coord_q)))
                # fout.write("%s: %s\n" % ("numpy.linalg.norm(numpy.array(coord_p) - numpy.array(coord_q)", numpy.linalg.norm(numpy.array(coord_p) - numpy.array(coord_q))))
                # fout.write("%s: %s\n" % ("q2p_norm_dist", q2p_norm_dist))
                # fout.write("%s: %s\n" % ("wgt_p2q", wgt_p2q))
                # fout.write("%s: %s\n" % ("P_coeff", P_coeff_trans))
                # fout.write("%s:\n %s\n" % ("M_p", M_p))
                # fout.write("%s:\n %s\n" % ("b_p", b_p))
                # fout.write("%s\n" % ("*"*30))
            
            # peter comment: Invert and solve
            # TODO: We MUST check the below code.
            #Diff_Op_p = Util.mldivide(M_p,b_p)
            Diff_Op_p = numpy.linalg.lstsq(M_p, b_p)[0]
            # fout.write("\n%s\n%s\n" % ("Diff_Op_p 1", Diff_Op_p))

            #Diff_Op_p = Diff_Op_p(1:Lt,:);
            # Diff_Op_p = Diff_Op_p[0:(int(Lt)+1),:]
            Diff_Op_p = Diff_Op_p[0:(int(Lt)),:]
            # fout.write("\n%s\n%s\n" % ("Diff_Op_p 2", Diff_Op_p))


            if dim == 3:
                # peter comment: Re-scale
                #Diff_Op_p(2, 1:n_node) = (1.0/dilp_p)*Diff_Op_p(2,1:n_node) #peter comment: dx [1,0,0] 1            
                Diff_Op_p[1, 0:n_node] = (1.0 / dilp_p) * Diff_Op_p[1, 0:n_node] #peter comment: dx [1,0,0] 1
                #Diff_Op_p(3,1:n_node) = (1.0/dilp_p)*Diff_Op_p(3,1:n_node) #peter comment: dy [0,1,0] 1
                Diff_Op_p[2,0:n_node] = (1.0 / dilp_p) * Diff_Op_p[2,0:n_node] #peter comment: dy [0,1,0] 1
                #Diff_Op_p(4,1:n_node) = (1.0/dilp_p)*Diff_Op_p(4,1:n_node) #peter comment: dz [0,0,1] 1
                Diff_Op_p[3,0:n_node] = (1.0 / dilp_p) * Diff_Op_p[3,0:n_node] #peter comment: dz [0,0,1] 1

                # if poly_order > 1:
                if top_op > 1:
                    #Diff_Op_p(5,1:n_node) = (2.0/dilp_p^2)*Diff_Op_p(5,1:n_node)  #peter comment: d2x [2,0,0] 2
                    Diff_Op_p[4,0:n_node] = (2.0 / dilp_p**2) * Diff_Op_p[4,0:n_node]  #peter comment: d2x [2,0,0] 2
                    #Diff_Op_p(6,1:n_node) = (1.0/dilp_p^2)*Diff_Op_p(6,1:n_node)  #peter comment: dxdy[1,1,0] 2
                    Diff_Op_p[5,0:n_node] = (1.0 / dilp_p**2) * Diff_Op_p[5,0:n_node]  #peter comment: dxdy[1,1,0] 2
                    #Diff_Op_p(7,1:n_node) = (1.0/dilp_p^2)*Diff_Op_p(7,1:n_node)  #peter comment: dxdz[1,0,1] 2
                    Diff_Op_p[6,0:n_node] = (1.0 / dilp_p**2) * Diff_Op_p[6,0:n_node]  #peter comment: dxdz[1,0,1] 2
                    #Diff_Op_p(8,1:n_node) = (2.0/dilp_p^2)*Diff_Op_p(8,1:n_node)  #peter comment: d2y [0,2,0] 2
                    Diff_Op_p[7,0:n_node] = (2.0 / dilp_p**2) * Diff_Op_p[7,0:n_node]  #peter comment: d2y [0,2,0] 2
                    #Diff_Op_p(9,1:n_node) = (1.0/dilp_p^2)*Diff_Op_p(9,1:n_node)  #peter comment: dydz[0,1,1] 2
                    Diff_Op_p[8,0:n_node] = (1.0 / dilp_p**2) * Diff_Op_p[8,0:n_node]  #peter comment: dydz[0,1,1] 2
                    #Diff_Op_p(10,1:n_node) = (2.0/dilp_p^2)*Diff_Op_p(10,1:n_node)  #peter comment: d2z[0,0,2] 2
                    Diff_Op_p[9,0:n_node] = (2.0 / dilp_p**2) * Diff_Op_p[9,0:n_node]  #peter comment: d2z[0,0,2] 2

                # if poly_order > 2:
                if top_op > 2:
                    # Diff_Op_p(11,1:n_node) = (6.0/dilp_p^2)*Diff_Op_p(11,1:n_node);         %d3x
                    Diff_Op_p[10, 0:n_node] = (6.0 / dilp_p**2) * Diff_Op_p[10, 0:n_node] #peter comment: d3x
                    # Diff_Op_p(12,1:n_node) = (2.0/dilp_p^2)*Diff_Op_p(12,1:n_node);         %d2xdy
                    Diff_Op_p[11, 0:n_node] = (2.0 / dilp_p**2) * Diff_Op_p[11, 0:n_node] #peter comment: d2xdy
                    # Diff_Op_p(13,1:n_node) = (2.0/dilp_p^2)*Diff_Op_p(13,1:n_node);         %d2xdz  
                    Diff_Op_p[12, 0:n_node] = (2.0 / dilp_p**2) * Diff_Op_p[12, 0:n_node] #peter comment: d2xdz  
                    # Diff_Op_p(14,1:n_node) = (2.0/dilp_p^2)*Diff_Op_p(14,1:n_node);         %dxd2y 
                    Diff_Op_p[13, 0:n_node] = (2.0 / dilp_p**2) * Diff_Op_p[13, 0:n_node] #peter comment: dxd2y 
                    # Diff_Op_p(15,1:n_node) = (2.0/dilp_p^2)*Diff_Op_p(15,1:n_node);         %dxdydz   
                    Diff_Op_p[14, 0:n_node] = (2.0 / dilp_p**2) * Diff_Op_p[14, 0:n_node] #peter comment: dxdydz   
                    # Diff_Op_p(16,1:n_node) = (2.0/dilp_p^2)*Diff_Op_p(16,1:n_node);         %dxd2z  
                    Diff_Op_p[15, 0:n_node] = (2.0 / dilp_p**2) * Diff_Op_p[15, 0:n_node] #peter comment: dxd2z  
                    # Diff_Op_p(17,1:n_node) = (6.0/dilp_p^2)*Diff_Op_p(17,1:n_node);         %d3y
                    Diff_Op_p[16, 0:n_node] = (6.0 / dilp_p**2) * Diff_Op_p[16, 0:n_node] #peter comment: d3y
                    # Diff_Op_p(18,1:n_node) = (2.0/dilp_p^2)*Diff_Op_p(18,1:n_node);         %d2ydz  
                    Diff_Op_p[17, 0:n_node] = (2.0 / dilp_p**2) * Diff_Op_p[17, 0:n_node] #peter comment: d2ydz  
                    # Diff_Op_p(19,1:n_node) = (2.0/dilp_p^2)*Diff_Op_p(19,1:n_node);         %dyd2z     
                    Diff_Op_p[18, 0:n_node] = (2.0 / dilp_p**2) * Diff_Op_p[18, 0:n_node] #peter comment: dyd2z     
                    # Diff_Op_p(20,1:n_node) = (6.0/dilp_p^2)*Diff_Op_p(20,1:n_node);         %d3z
                    Diff_Op_p[19, 0:n_node] = (6.0 / dilp_p**2) * Diff_Op_p[19, 0:n_node] #peter comment: d3z 
            
            elif dim == 2:
                # Diff_Op_p(2,1:n_node) = (1.0/dilp_p)*Diff_Op_p(2,1:n_node);             %dx [1,0] 1
                Diff_Op_p[1, 0:n_node] = (1.0 / dilp_p) * Diff_Op_p[1, 0:n_node]
                # Diff_Op_p(3,1:n_node) = (1.0/dilp_p)*Diff_Op_p(3,1:n_node);             %dy [0,1] 1
                Diff_Op_p[2, 0:n_node] = (1.0 / dilp_p) * Diff_Op_p[2, 0:n_node]
                # Diff_Op_p(4,1:n_node) = (2.0/dilp_p^2)*Diff_Op_p(4,1:n_node);           %d2x [2,0] 2
                Diff_Op_p[3, 0:n_node] = (2.0 / dilp_p**2) * Diff_Op_p[3, 0:n_node]
                # Diff_Op_p(5,1:n_node) = (1.0/dilp_p^2)*Diff_Op_p(5,1:n_node);           %dxdy [1,1] 2
                Diff_Op_p[4, 0:n_node] = (1.0 / dilp_p**2) * Diff_Op_p[4, 0:n_node]
                # Diff_Op_p(6,1:n_node) = (2.0/dilp_p^2)*Diff_Op_p(6,1:n_node);           %d2y[0,2]   2
                Diff_Op_p[5, 0:n_node] = (2.0 / dilp_p**2) * Diff_Op_p[5, 0:n_node]

                # if top_op > 2
                if top_op > 2:
                    # Diff_Op_p(7,1:n_node) = (6.0/dilp_p^3)*Diff_Op_p(7,1:n_node);           %d3x [3,0] 3
                    Diff_Op_p[6, 0:n_node] = (6.0 / dilp_p**3) * Diff_Op_p[6, 0:n_node]
                    # Diff_Op_p(8,1:n_node) = (2.0/dilp_p^3)*Diff_Op_p(8,1:n_node);           %d2xdy [2,1] 3
                    Diff_Op_p[7, 0:n_node] = (2.0 / dilp_p**3) * Diff_Op_p[7, 0:n_node]
                    # Diff_Op_p(9,1:n_node) = (2.0/dilp_p^3)*Diff_Op_p(9,1:n_node);            %dxd2y
                    Diff_Op_p[8, 0:n_node] = (2.0 / dilp_p**3) * Diff_Op_p[8, 0:n_node]
                    # Diff_Op_p(10,1:n_node) = (6.0/dilp_p^3)*Diff_Op_p(10,1:n_node);     	%d3y
                    Diff_Op_p[9, 0:n_node] = (6.0 / dilp_p**3) * Diff_Op_p[9, 0:n_node]
                # end

                # if top_op > 3        
                if top_op > 3:
                    # Diff_Op_p(11,1:n_node) = (24.0/dilp^4)*Diff_Op_p(11,1:n_node);          %d4x
                    Diff_Op_p[10, 0:n_node] = (24.0 / dilp_p**4) * Diff_Op_p[10, 0:n_node]
                    # Diff_Op_p(12,1:n_node) = (6.0/dilp^4)*Diff_Op_p(12,1:n_node);           %d3xdy
                    Diff_Op_p[11, 0:n_node] = (6.0 / dilp_p**4) * Diff_Op_p[11, 0:n_node]
                    # Diff_Op_p(13,1:n_node) = (4.0/dilp^4)*Diff_Op_p(13,1:n_node);           %d2xd2y
                    Diff_Op_p[12, 0:n_node] = (4.0 / dilp_p**4) * Diff_Op_p[12, 0:n_node]
                    # Diff_Op_p(14,1:n_node) = (6.0/dilp^4)*Diff_Op_p(14,1:n_node);           %dxd3y
                    Diff_Op_p[13, 0:n_node] = (6.0 / dilp_p**4) * Diff_Op_p[13, 0:n_node]
                    # Diff_Op_p(15,1:n_node) = (24.0/dilp^4)*Diff_Op_p(15,1:n_node);          %d4y
                    Diff_Op_p[14, 0:n_node] = (24.0 / dilp_p**4) * Diff_Op_p[14, 0:n_node]
                # end

            elif dim == 1:
                # Diff_Op_p(2,1:n_node) = (1.0/dilp_p)*Diff_Op_p(2,1:n_node);              %dx [1] 1
                Diff_Op_p[1, 0:n_node] = (1.0 / dilp_p) * Diff_Op_p[1, 0:n_node]
                # Diff_Op_p(3,1:n_node) = (2.0/dilp_p^2)*Diff_Op_p(3,1:n_node);           %d2x [2] 2
                Diff_Op_p[2, 0:n_node] = (2.0 / dilp_p**2) * Diff_Op_p[2, 0:n_node]

                if top_op > 2:
                    # Diff_Op_p(4,1:n_node) = (6.0/dilp_p^3)*Diff_Op_p(4,1:n_node);           %d3x [3] 3
                    Diff_Op_p[3, 0:n_node] = (6.0 / dilp_p**3) * Diff_Op_p[3, 0:n_node]
                # end
    
                if top_op > 3:
                    # Diff_Op_p(5,1:n_node) = (24.0/dilp^4)*Diff_Op_p(5,1:n_node);            %d4x [4] 4
                    Diff_Op_p[4, 0:n_node] = (24.0 / dilp_p**4) * Diff_Op_p[4, 0:n_node]
                # end

            
            Diff_Op_p_sparse = sparse.csr_matrix(Diff_Op_p)
            Diff_Op.append(Diff_Op_p_sparse)

            # fout.write("%s\n" % ("/"*30))
            # fout.write("%s:\n %s\n" % ("Diff_Op_p", Diff_Op_p))
            # fout.write("%s:\n %s\n" % ("Diff_Op_p_sparse", Diff_Op_p_sparse))
            # fout.write("%s\n" % ("/"*30))

        # fout.write("%s\n" % ("="*50))
        # fout.write("%s:\n %s\n" % ("Diff_Op", Diff_Op))
        # fout.write("%s:\n %s\n" % ("Diff_Op[0]", Diff_Op[0]))
        # fout.write("%s\n" % ("="*50))

        return Diff_Op