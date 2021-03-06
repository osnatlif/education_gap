import numpy as np
from parameters import p
cimport constant_parameters as c
cimport draw_husband
cimport draw_wife
cimport calculate_wage
cimport libc.math as cmath
cdef extern from "randn.c":
    double uniform()
from calculate_utility_single_women cimport calculate_utility_single_women
from calculate_utility_married cimport calculate_utility_married
from calculate_utility_single_man cimport calculate_utility_single_man


cdef int single_men(int t, double[:, :, :, :, :, :, :, :, :, :, :, :, :, :, :, :] w_emax,
    double[:, :, :, :, :, :, :, :, :, :, :, :, :, :, :, :] h_emax,
    double[:,:,:,:,:,:,:,:,:] w_s_emax,
    double[:,:,:,:,:,:,:,:,:] h_s_emax, verbose) except -1:
    cdef double[:] mother
    cdef int iter_count = 0
    cdef double sum_emax = 0
    cdef int married_index = -99
    cdef int choose_partner = 0
    cdef int school
    cdef int exp
    cdef int kids
    cdef int home_time
    cdef int ability
    cdef int mother_educ
    cdef int mother_marital
    cdef int draw
    cdef double wage_w_full
    cdef double wage_w_part
    cdef double wage_h_full
    cdef double wage_h_part
    cdef double single_women_value
    cdef double single_man_value
    cdef double[:] u_wife = np.empty(18)
    cdef double[:] u_husband = np.empty(18)
    if c.cohort == 1960:
        mother = c.mother_1960_white
    elif c.cohort == 1970:
        mother = c.mother_1970_white
    elif c.cohort == 1980:
        mother = c.mother_1980_white
    elif c.cohort == 1990:
        mother = c.mother_1990_white
    else:
        assert ()

    if verbose:
        print("====================== single men:  ======================")
    cdef draw_husband.Husband husband = draw_husband.Husband()
    cdef draw_wife.Wife wife = draw_wife.Wife()
    husband.age = 17 + t
    # c.max_period, c.school_size, c.exp_size, c.kids_size, c.health_size, c.home_time_size, c.ability_size, c.mother_size, c.mother_size])
    for school in range(0, c.school_size):   # loop over school
        husband.schooling = school
        draw_husband.update_school(husband)
        for exp in range(0, c.exp_size):           # loop over experience
            husband.exp = c.exp_vector[exp]
            for kids in range(0, 2):                # for each number of kids: 0, 1,   - open loop of kids
                husband.kids = kids
                for home_time in range(0, c.home_time_size):       # home time loop - three options
                    husband.home_time_ar = c.home_time_vector[home_time]
                    for ability in range(0, c.ability_size):     # for each ability level: low, medium, high - open loop of ability
                        husband.ability_i = ability
                        husband.ability_value = c.ability_vector[ability] * p.sigma_ability_h  # husband.ability - low, medium, high
                        for mother_educ in range(0,c.mother_size):
                            husband.mother_educ = mother_educ
                            for mother_marital in range(0, c.mother_size):
                                husband.mother_marital = mother_marital
                                sum_emax = 0
                                iter_count = iter_count + 1
                                if verbose:
                                    print(husband)
                                for draw in range(0, c.DRAW_B):
                                    married_index = -99
                                    choose_partner = 0
                                    wage_h_full, wage_h_part = calculate_wage.calculate_wage_h(husband)
                                    single_men_value, _ = calculate_utility_single_man(h_s_emax, wage_h_part, wage_h_full, husband, t)
                                    if husband.age < 20:
                                        prob_meet_potential_partner = cmath.exp(p.omega_1) / (1.0 + cmath.exp(p.omega_1))
                                    else:
                                        temp = p.omega3 + p.omega4_h * husband.age + p.omega5_h * husband.age * husband.age
                                        prob_meet_potential_partner = cmath.exp(temp) / (1.0 + cmath.exp(temp))
                                    if uniform() < prob_meet_potential_partner:
                                        choose_partner = 1
                                        wife = draw_wife.draw_wife(husband, mother[0], mother[1], mother[2])
                                    if choose_partner == 1:
                                        wage_w_full, wage_w_part = calculate_wage.calculate_wage_w(wife)
                                        u_husband, u_wife, _, _, _, _ = calculate_utility_married(w_emax, h_emax, wage_h_part, wage_h_full, wage_w_part, wage_w_full, wife, husband, t)
                                        single_women_value, _, _ = calculate_utility_single_women(w_s_emax, wage_w_part, wage_w_full, wife, t)
                                        weighted_utility = float('-inf')
                                        for i in range(0, 18):
                                            if u_wife[i] > single_women_value and u_husband[i] > single_men_value:
                                                if c.bp * u_wife[i] + (1 - c.bp) * u_husband[i] > weighted_utility:
                                                    weighted_utility = c.bp * u_wife[i] + (1 - c.bp) * u_husband[i]
                                                    married_index = i
                                    if married_index > -99:
                                        sum_emax += prob_meet_potential_partner * u_husband[married_index] + (1-prob_meet_potential_partner) * single_men_value
                                    else:
                                        sum_emax += single_men_value
                                    # print("====================== new draw ======================")
                                # end draw backward loop
                                h_s_emax[t][school][exp][kids][husband.health][home_time][ability][mother_educ][mother_marital] = sum_emax / c.DRAW_B
                                if verbose:
                                    print("emax(", t, ", ", school, ", ", exp,", ", kids, ",", ability, ")=", sum_emax / c.DRAW_B)
                                    print("======================================================")

    return iter_count
