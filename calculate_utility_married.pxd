from draw_husband cimport Husband
from draw_wife cimport Wife


cpdef tuple calculate_utility_married(double[:, :, :, :, :, :, :, :, :, :, :, :, :, :, :, :] w_emax,
    double[:, :, :, :, :, :, :, :, :, :, :, :, :, :, :, :] h_emax,
    double wage_h_part, double wage_h_full, double wage_w_part, double wage_w_full,Wife wife, Husband husband, int t)
