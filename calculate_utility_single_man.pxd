from draw_husband cimport Husband

cpdef tuple calculate_utility_single_man(double[:,:,:,:,:,:,:,:,:] h_s_emax,
    double wage_h_part, double wage_h_full,Husband husband,int t)
