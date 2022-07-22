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


cdef int single_women(int t, double[:, :, :, :, :, :, :, :, :, :, :, :, :, :, :, :] w_emax,
    double[:, :, :, :, :, :, :, :, :, :, :, :, :, :, :, :] h_emax,
    double[:,:,:,:,:,:,:,:,:] w_s_emax,
    double[:,:,:,:,:,:,:,:,:] h_s_emax, verbose) except -1:
    cdef double[3] mother
    cdef int iter_count = 0
    cdef double sum_emax
    cdef double weighted_utility = float('-inf')
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
        print("====================== single women:  ======================")
    cdef draw_wife.Wife wife = draw_wife.Wife()
    wife.age = 17 + t
    # c.max_period, c.school_size, c.exp_size, c.kids_size, c.health_size, c.home_time_size, c.ability_size, c.mother_size, c.mother_size])
    for school in range(0, c.school_size):   # loop over school
        wife.schooling = school
        draw_wife.update_wife_schooling(wife)
        for exp in range(0, c.exp_size):           # loop over experience
            wife.exp = c.exp_vector[exp]
            for kids in range(0, 4):                # for each number of kids: 0, 1, 2,  - open loop of kids
                wife.kids = kids
                for home_time in range(0, c.home_time_size):       # home time loop - three options
                    wife.home_time_ar = c.home_time_vector[home_time]
                    for ability in range(0, c.ability_size):     # for each ability level: low, medium, high - open loop of ability
                        wife.ability_i = ability
                        wife.ability_value = c.ability_vector[ability] * p.sigma_ability_w  # wife ability - low, medium, high
                        for mother_educ in range(0,c.mother_size):
                            wife.mother_educ = mother_educ
                            for mother_marital in range(0, c.mother_size):
                                wife.mother_marital = mother_marital
                                sum_emax = 0
                                iter_count = iter_count + 1
                                if verbose:
                                    print(wife)
                                for draw in range(0, c.DRAW_B):
                                    married_index = -99
                                    choose_partner = 0
                                    wage_w_full, wage_w_part, info = calculate_wage.calculate_wage_w(wife)
                                    single_women_value, single_women_index, _, single_women_u = calculate_utility_single_women(w_s_emax, wage_w_part, wage_w_full, wife, t)

                                    if wife.age < 20:
                                        prob_meet_potential_partner = cmath.exp(p.omega_1) / (1.0 + cmath.exp(p.omega_1))
                                    else:
                                        temp = p.omega3 + p.omega4_w * wife.age + p.omega5_w * wife.age * wife.age
                                        prob_meet_potential_partner = cmath.exp(temp) / (1.0 + cmath.exp(temp))
                                    if uniform() < prob_meet_potential_partner:
                                        choose_partner = 1
                                        husband = draw_husband.draw_husband_forward(wife, mother[1], mother[2], mother[3])
                                    if choose_partner == 1:
                                        wage_h_full, wage_h_part = calculate_wage.calculate_wage_h(husband)
                                        u_husband, u_wife, _, _, _, _ = calculate_utility_married(w_emax, h_emax, wage_h_part, wage_h_full, wage_w_part, wage_w_full, wife, husband, t)
                                        single_man_value, _ = calculate_utility_single_man(h_s_emax, wage_h_part, wage_h_full, husband, t)
                                        weighted_utility = float('-inf')
                                        for i in range(0, 18):
                                            if u_wife[i] > single_women_value and u_husband[i] > single_man_value:
                                                if c.bp * u_wife[i] + (1 - c.bp) * u_husband[i] > weighted_utility:
                                                    weighted_utility = c.bp * u_wife[i] + (1 - c.bp) * u_husband[i]
                                                    married_index = i
                                    if married_index > -99:
                                        sum_emax += prob_meet_potential_partner * u_wife[married_index] +(1-prob_meet_potential_partner)*single_women_value
                                    else:
                                        sum_emax += single_women_value
                                    # print("====================== new draw ======================")
                                    school_info = {}

                                    school_info["wage_w_full"] = wage_w_full
                                    school_info["wage_w_part"] = wage_w_part
                                    school_info["single_women_value"] = single_women_value
                                    school_info["single_women_index"] = single_women_index
                                    school_info["prob_meet_potential_partner"] = prob_meet_potential_partner
                                    school_info["single_women_u"] = np.asarray(single_women_u)
                                    school_info["calculate_wage_info"] = info
                                    school_info["sum_emax"] = sum_emax
                                    school_info["wife"] = str(wife)
                                    key = str(exp) + "" + str(kids) + "" + str(home_time) + "" + str(mother_educ) + "" + str(mother_marital)
                                    #if single_women_index == 6 and school > 0:
                                    #    print("##########################################")
                                    #    print(t)
                                    #    print(key)
                                    #    print(school_info)

                                # end draw backward loop


                                w_s_emax[t][school][exp][kids][wife.health][home_time][ability][mother_educ][mother_marital] = sum_emax / c.DRAW_B
                                if verbose:
                                    print("emax(", t, ", ", school, ", ", exp,", ", kids, ",", ability, ")=", sum_emax / c.DRAW_B)
                                    print("======================================================")
    #for k in school2_arr:
        #if school3_arr[k]["sum_emax"] < school2_arr[k]["sum_emax"] and \
            #school3_arr[k]["wage_w_full"] > 0:
            #print("##########################################")
            #print(t)
            #print(k)
            #print("-----------------------")
            #print(school2_arr[k])
            #print("-----------------------")
            #print(school3_arr[k])

    return iter_count
