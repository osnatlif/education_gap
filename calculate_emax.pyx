import numpy as np
from time import perf_counter
cimport constant_parameters as c
from single_men cimport single_men
from single_women cimport single_women
from married_couple_emax cimport married_couple_emax


cpdef create_married_emax():
    return np.ndarray([c.max_period, c.school_size, c.school_size, c.exp_size, c.exp_size,c.kids_size, c.health_size, c.health_size,
                       c.home_time_size, c.home_time_size, c.ability_size, c.ability_size, c.mother_size, c.mother_size, c.mother_size, c.mother_size])


cpdef create_single_w_emax():
    return np.ndarray([c.max_period, c.school_size, c.exp_size, c.kids_size, c.health_size, c.home_time_size, c.ability_size, c.mother_size, c.mother_size])


cpdef create_single_h_emax():
    return np.ndarray([c.max_period, c.school_size, c.exp_size, c.kids_size, c.health_size, c.home_time_size, c.ability_size, c.mother_size, c.mother_size])


cpdef int calculate_emax(double[:, :, :, :, :, :, :, :, :, :, :, :, :, :, :, :] w_emax,
    double[:, :, :, :, :, :, :, :, :, :, :, :, :, :, :, :] h_emax,
    double[:,:,:,:,:,:,:,:,:] w_s_emax, double[:,:,:,:,:,:,:,:,:] h_s_emax, verbose) except -1:
    cdef int iter_count = 0
    cdef double tic
    cdef double toc
    # running until the one before last period
    for t in range(c.max_period - 2, 0, -1):
        # EMAX FOR SINGLE MEN
        tic = perf_counter()
        iter_count += single_men(t, w_emax, h_emax, w_s_emax, h_s_emax, verbose)
        toc = perf_counter()
        #print("calculate single men for t=%d took: %.4f (sec)" % (t, (toc - tic)))
        # EMAX FOR SINGLE WOMEN
        tic = perf_counter()
        iter_count += single_women(t, w_emax, h_emax, w_s_emax, h_s_emax, verbose)
        toc = perf_counter()
        #print("calculate single women for t=%d took: %.4f (sec)" % (t, (toc - tic)))
        # EMAX FOR MARRIED COUPLE
        tic = perf_counter()
        iter_count += married_couple_emax(t, w_emax, h_emax, w_s_emax, h_s_emax, verbose)
        toc = perf_counter()
        #print("calculate married couple for t=%d took: %.4f (sec)" % (t, (toc - tic)))

    return iter_count
