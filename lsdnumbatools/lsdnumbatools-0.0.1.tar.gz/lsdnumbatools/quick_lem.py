import numba as nb
import numpy as np
import math as m
import lsdnumbatools as lsdnb

@nb.jit(nopython = True, cache = True)
def SPIL_Srec(erosion, elevation, stack, receivers, dist2receivers,
         area, k, m, n, dt, tolerance, nnodes):
  for inode in range(nnodes):
    istack = stack[inode]
    irec = receivers[istack]
    # print(inode)

    if irec == istack:
      # no erosion at basin outlets
      erosion[istack] = 0.
      continue

    factor = k[istack] * dt * area[istack]**m / dist2receivers[istack]**n

    ielevation = elevation[istack]
    irec_elevation = elevation[irec] - erosion[irec]

    # iterate: lower elevation until convergence
    elevation_k = ielevation
    elevation_prev = np.inf

    while abs(elevation_k - elevation_prev) > tolerance:
      elevation_prev = elevation_k
      slope = elevation_k - irec_elevation
      diff = ((elevation_k - ielevation + factor * (slope)**n) /
          (1. + factor * n * slope**(n - 1)))
      elevation_k -= diff

    erosion[istack] = ielevation - elevation_k

    # if(erosion[istack] > 2):
    #   print()
  # print("GURG")


@nb.jit(nopython = True, cache = True)
def SPIL_Srec_explicit(erosion, elevation, stack, receivers, dist2receivers,
         area, k, m, n, dt, tolerance, nnodes):
  for inode in range(nnodes):
    istack = stack[inode]
    irec = receivers[istack]
    # print(inode)

    if irec == istack:
      # no erosion at basin outlets
      erosion[istack] = 0.
      continue

    erosion[istack] = abs((elevation[istack] - elevation[irec])/dist2receivers[istack])**n * area[istack]**m * k[istack] * dt

    if(elevation[istack] - erosion[istack]) < 0:
      print(abs((elevation[irec] - elevation[istack])/dist2receivers[istack]), "||", area[istack])

  # print("GURG")


