import numpy
from numpy.core.fromnumeric import size
from scipy import sparse

###from PDMApp.Util_module.Utils import Util
from cm2utils.Utils import Util

def __getLoadAndFixIndx(gc):
    load_indx = []
    fix_indx = []
    
    yCoords = []
    for i in range(0, len(gc.getNodesCoordinates())):
        yCoords.append(gc.getNodesCoordinates()[i][1])
        
    yCoords_max = max(yCoords)
    yCoords_min = min(yCoords)
    
    for i in range(0, len(yCoords)):
        if (yCoords[i] == yCoords_max):
            load_indx.append(i)
        elif (yCoords[i] == yCoords_min):
            fix_indx.append(i)

    return load_indx, fix_indx
        
def Test_3D_sclr(Diff_Ops, gc, nodeTagsMinusOne4K, Normals, dim, fout=None, usingSparseMat=True):
    print("Test_3D_sclr")

    # peter comment: Applied Loads
    Applied_BC = [100,0]

    # peter comment: Material Parameters
    k = 1

    n_node = len(nodeTagsMinusOne4K)

    fld_dim = 1
    # peter comment: Assign BCs, Assign type indentifier
    # type
    var_type = numpy.zeros((n_node, 3), dtype=int)
    
    # load_indx, fix_indx: node number - 1
    load_indx, fix_indx = __getLoadAndFixIndx(gc)

    fout.write("\n%s:\n %s\n" % ("load_indx", load_indx))
    fout.write("\n%s:\n %s\n" % ("fix_indx", fix_indx))

    nodesInSurfaces = []
    for i_node in gc.getPhysicalGroups():
        nodesInSurfaces += gc.getConnectionBetweenPhysicalGroupAndNodes(physicalGroupName=i_node, sort=True)
        #fout.write("\n%s:\n %s\n" % ("**************************", i))
    
    
    # Remove duplicates as well as calculate differences.
    nodesInSurfaces = set(nodesInSurfaces)
    nodesOnBoundaries = set(gc.getNodesOnBoundaries())
    nodesInSurfaces = list(nodesInSurfaces - nodesOnBoundaries)
    # nodesInSurfaces: node number - 1
    nodesInSurfaces = [int(i-1) for i in nodesInSurfaces]

    fout.write("\n%s:\n %s\n" % ("nodesInSurfaces", nodesInSurfaces))

    # peter comment: Assign type
    for i_node in nodesInSurfaces: var_type[i_node] = 2
    for i_node in load_indx: var_type[i_node] = 1
    for i_node in fix_indx: var_type[i_node] = 1

    fout.write("\n%s:\n %s\n" % ("var_type", var_type))

    # peter comment: Assign loads
    app_load = numpy.zeros((fld_dim*n_node, 1))
    app_load[load_indx] = Applied_BC[0]
    app_load[fix_indx] = Applied_BC[1]

    fout.write("\n%s:\n %s\n" % ("app_load", app_load))

    # peter comment: Construct System of equations
    #<kr> ⬇︎ sparse matrix로 만들어서 값을 넣을까도 생각했지만, 
    #<kr> 0으로만 이루어진 sparse matrix는 아무런 데이터가 없는 상태이고, 
    #<kr> 그러면 값을 넣기 위해 필요한 위치를 불러올 수가 없다.
    #<kr> -1이나 뭐 그런걸로 default sparse matrix를 만들수는 있겠지만, 그러면 의미가 없으므로, 
    #<kr> 결국 numpy array로 매트릭스 만들고, 필요하면 sparse matrix로 변환하는 것으로.
    K_glb = numpy.zeros((fld_dim*n_node, fld_dim*n_node))
    Appld = numpy.zeros((fld_dim*n_node, 1))
    C = numpy.zeros(K_glb.shape)
    # c, dx, dy, dz, d2x, dxdy, dxdz, d2y, dydz, d2z = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    c, dx, dy, dz, d2x, dxdy, dxdz, d2y, dydz, d2z = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    zero_row = numpy.zeros((1, n_node))
    
    #MATLAB -> PYTHON: (matlab) Diff_Ops{i_node}(d2x,:) == (python) Diff_Ops[i_node][d2x-1,:] == (python) Diff_Ops[i_node][d2x-1]
    # parfor i_node = 1:n_node
    # usingSparseMat = True
    for i_node in range(0,n_node):
        if var_type[i_node][0] == 0:
            #K_glb(i_node,:) = 
            #      Diff_Ops{i_node}(d2x,:) + Diff_Ops{i_node}(d2y,:) + Diff_Ops{i_node}(d2z,:);
            if (usingSparseMat):  # using sparse matrix
                temp = Diff_Ops[i_node][d2x-1,:] + Diff_Ops[i_node][d2y-1,:] + Diff_Ops[i_node][d2z-1,:]
                for i,j in zip(temp.indices, temp.data):
                    K_glb[i_node,i] = j
            else:  # using matrix
                K_glb[i_node,:] =  (Diff_Ops[i_node][d2x-1,:] + Diff_Ops[i_node][d2y-1,:] + Diff_Ops[i_node][d2z-1,:]).todense()
        elif var_type[i_node][0] == 1:
            #K_glb(i_node,:) = Diff_Ops{i_node}(c,:);
            if (usingSparseMat):  # using sparse matrix
                temp = Diff_Ops[i_node][c-1,:]
                for i,j in zip(temp.indices, temp.data):
                    K_glb[i_node,i] = j
            else:  # using matrix
                K_glb[i_node,:] = (Diff_Ops[i_node][c-1,:]).todense()
        elif var_type[i_node][0] == 2:
            #K_glb(i_node,:) = 
            #      Diff_Ops{i_node}(dx,:)*nx + Diff_Ops{i_node}(dy,:)*ny + Diff_Ops{i_node}(dz,:)*nz;
            if (usingSparseMat):  # using sparse matrix
                temp = Diff_Ops[i_node][dx-1,:]*Normals[i_node][0] + Diff_Ops[i_node][dy-1,:]*Normals[i_node][1] + Diff_Ops[i_node][dz-1,:]*Normals[i_node][2]
                for i,j in zip(temp.indices, temp.data):
                        K_glb[i_node,i] = j
            else:
                K_glb[i_node,:] = (Diff_Ops[i_node][dx-1,:]*Normals[i_node][0] + Diff_Ops[i_node][dy-1,:]*Normals[i_node][1] + Diff_Ops[i_node][dz-1,:]*Normals[i_node][2]).todense()
    
    #fout.write("\n%s\n %s\n" % ("K_glb", K_glb.tolist()))
    fout.write("\n%s\n %s\n" % ("K_glb", K_glb))
    # K_glb = sparse.csr_matrix(K_glb)
    # fout.write("\n%s\n %s\n" % ("K_glb (sparse matrix)", K_glb))

    #SOLN = K_glb\app_load;
    SOLN = Util().mldivide(K_glb, app_load)
    # fout.write("\n%s\n %s\n" % ("SOLN", SOLN))
    return SOLN
            

def Test_3D_sclr_vectorized_implementation(Diff_OpsV, gc, nodeTagsMinusOne4K, Normals, dim, fout=None, usingSparseMat=True):
    print("Test_3D_sclr_vectorized_implementation")

    Applied_BC = [100,0]
    k = 1

    # peter comment
    # %Extract need lists for the problem. For this problem we might need to
    # %referce the nodes of each surface, the nodes intersecting between
    # %surfaces, and the interior nodes
    # surf_node_lists   = nodelists.surf_node_list;
    # intrsct_node_list = nodelists.intrsct_node_list;
    # int_node_list     = nodelists.int_node_list;
    
     



    

    

