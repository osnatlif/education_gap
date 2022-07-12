import timeit
import numpy as np
import math
from libc.math cimport exp as cexp

cpdef test():
    arr_size = 100000
    arr = np.random.random(arr_size)

    start_time = timeit.default_timer()
    [np.exp(v) for v in arr]
    print("numpy results (usec): ", 1000000*(timeit.default_timer() - start_time)/arr_size)

    start_time = timeit.default_timer()
    [math.exp(v) for v in arr]
    print("math results (usec): ", 1000000*(timeit.default_timer() - start_time)/arr_size)

    start_time = timeit.default_timer()
    [cexp(v) for v in arr]
    print("c results (usec): ", 1000000*(timeit.default_timer() - start_time)/arr_size)
