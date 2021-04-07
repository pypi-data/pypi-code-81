import numpy
from scipy import sparse

def get_Diff_Op_mat_vec(Diff_Ops: list, fout=None):
    # [Lp, n_node] = size(Diff_Ops{1});
    Lp, n_node = Diff_Ops[0].get_shape()
    # print(Lp)
    # print(n_node)
    # Operator = cell(Lp,1);
    # temp_mat = zeros(n_node,n_node);
    # Operator(:) = {temp_mat};
    Operator = []
    temp_mat = numpy.zeros((int(n_node),int(n_node)))
    Operator = [temp_mat for i in range(Lp)]
    
    # for poly_order = 1:Lp
    #     for i_node = 1:n_node
    #         Operator{poly_order}(i_node, :) = Diff_Ops{i_node}(poly_order,:);
    #     end
    #     Operator{poly_order} = sparse(Operator{poly_order});
    # end
    for poly_order in range(0, Lp): # 10
        for i_node in range(0, n_node): # 45
            Operator[poly_order][i_node, :] = (Diff_Ops[i_node][poly_order, :]).todense()
        Operator[poly_order] = sparse.csr_matrix(Operator[poly_order])
    
    fout.write("%s\n %s\n" % ("Operator", Operator))

