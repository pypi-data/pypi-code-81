import cupy.cuda.curand as curand
from spins import functions

class curandRNG:
    def __init__(self, seed=0):
        rnu = curand.createGenerator(curand.CURAND_RNG_PSEUDO_PHILOX4_32_10)
        curand.setPseudoRandomGeneratorSeed(rnu, seed)
        self._rnu = rnu
    def Uniform(self, arr):
        ptr = arr.__cuda_array_interface__['data'][0]
        curand.generateUniform(self._rnu, ptr, arr.size)
    def Uniformint(self, arr):
        self.Uniform(arr)
        arr[:] = functions.int(arr)
