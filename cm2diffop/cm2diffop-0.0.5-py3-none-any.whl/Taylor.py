import numpy

def taylor_poly_vec_P(coord_p, coord_q, dilp_p, poly_order:int, Lp, dim):
    scld_dist = (numpy.array(coord_q) - numpy.array(coord_p)) / dilp_p
    
    # peter comment: Initialize
    P_coeff = numpy.zeros(int(Lp))
    cnt = 0

    if dim == 1:
        pass
    elif dim == 2:
        pass
    elif dim == 3:
        # for p = 0:poly_order
        for p in range(0, poly_order+1):
            # for q = 0:p
            for q in range(0, p+1):
                # for r = 0:q
                for r in range(0, q+1):
                    # P_coeff(cnt) = scld_dist(1)^(p-q)*scld_dist(2)^(q-r)*scld_dist(3)^(r);
                    # cnt = cnt + 1;
                    P_coeff[cnt] = (scld_dist[0]**(p-q)) * (scld_dist[1]**(q-r)) * (scld_dist[2]**(r))
                    cnt = cnt + 1
    return P_coeff