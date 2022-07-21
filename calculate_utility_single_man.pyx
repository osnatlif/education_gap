import numpy as np
from parameters import p
from value_to_index cimport exp_to_index
from value_to_index cimport schooly_to_index
from value_to_index cimport home_time_to_index
from value_to_index cimport ability_to_index
cimport libc.math as cmath
cdef extern from "randn.c":
    double randn(double mu, double sigma)
cimport gross_to_net as tax
cimport constant_parameters as c
from draw_husband cimport Husband

cpdef tuple calculate_utility_single_man(double[:,:,:,:,:,:,:,:,:] h_s_emax, double wage_h_part, double wage_h_full,Husband husband,int t):
    ###################################################################################################
    #      calculate utility for single man
    ###################################################################################################

    cdef double net_income_single_h_ue = 0
    cdef double net_income_single_h_ef = 0
    cdef double net_income_single_h_ep = 0
    cdef double etah = 0
    cdef double budget_c_single_h_ue = 0
    cdef double budget_c_single_h_ef = 0
    cdef double budget_c_single_h_ep = 0
    cdef double kids_utility_single_h_ue = 0
    cdef double kids_utility_single_h_ef = 0
    cdef double kids_utility_single_h_ep = 0
    cdef double school_utility_h = 0
    cdef double home_time_h = 0
    cdef double divorce_cost_h = 0
    cdef double[7] u_husband_single = np.empty(7)
    cdef double[7] u_husband = np.empty(7)
    cdef int wife_exp_index = 0
    cdef int kids_index = 0
    cdef int husband_home_time_index = 0
    cdef int husband_home_time_index_preg = 0
    cdef int school_index = 0
    cdef double single_value = 0
    cdef int single_index = 0
    cdef double ar = 0
    cdef int husband_mother_educ_index = 0
    cdef int husband_mother_marital_index = 0

    net_income_single_h_ue = c.ub_h
    if wage_h_full >0:
        net_income_single_h_ef = tax.gross_to_net_single(husband.kids, wage_h_full, t)
    if wage_h_part > 0:
        net_income_single_h_ep = tax.gross_to_net_single(husband.kids, wage_h_part, t)

    if husband.kids == 0:  # calculate value of husband if there is husband
        etah = 0
    elif husband.kids == 1:
        etah = c.eta1  # this is the fraction of parent's income that one child gets
    elif husband.kids == 2:
        etah = c.eta2
    elif husband.kids == 3:
        etah = c.eta3
    else:
        assert (0)
    budget_c_single_h_ue = (1 - etah) * net_income_single_h_ue
    if wage_h_full > 0:
        budget_c_single_h_ef = (1 - etah) * net_income_single_h_ef
    if wage_h_part > 0:
        budget_c_single_h_ep = (1 - etah) * net_income_single_h_ep
    # utility from quality and quality of children: #row0 - CES  parameter row1 - women leisure row2 - husband leisure row3 -income
    if husband.kids > 0:
        kids_utility_single_h_ue = cmath.pow((p.row1_h * cmath.pow((c.leisure-c.home_p), p.row0) + p.row2 * cmath.pow((c.eta1 * net_income_single_h_ue), p.row0) +
                                        (1.0 - p.row1_h - p.row2) * cmath.pow((husband.kids), p.row0)),(1.0 / p.row0))
        if wage_h_full > 0:
            kids_utility_single_h_ef = cmath.pow((                                           p.row2 * cmath.pow((c.eta1 * net_income_single_h_ef), p.row0) +
                                                                                       (1.0 - p.row1_h - p.row2) * cmath.pow((husband.kids), p.row0)), (1.0 / p.row0))
        if wage_h_part > 0:
            kids_utility_single_h_ep = cmath.pow((p.row1_h * cmath.pow((c.leisure_part-c.home_p), p.row0) + p.row2 * cmath.pow((c.eta1 * net_income_single_h_ep), p.row0) +
                                            (1.0 - p.row1_h - p.row2) * cmath.pow((husband.kids), p.row0)), (1.0 / p.row0))
    elif husband.kids == 0:
        kids_utility_single_h_ue = 0
        kids_utility_single_h_ef = 0
        kids_utility_single_h_ep = 0
    else:
        assert (0)

    school_utility_h = 0
    if husband.schooling == 1:
        school_utility_h = p.s1_h + p.s2_h * husband.mother_educ + p.s3_h * husband.ability_value # utility from high school
    elif husband.schooling > 1:
        school_utility_h = p.s1_h + p.s2_h * husband.mother_educ + p.s3_h * husband.ability_value + p.s4_w  # utility from post high school
    # home time equation - random walk - tau0_w -pregnancy in previous period, tau1_w - drift term - should be negative
    # if husband is not married his home time is not influence by a newborn, the wife is influenced of course, so home time for her is not function of M
    if husband.home_time_ar == 0:
        print("i'm here")
    home_time_h = cmath.exp((p.tau1_h * cmath.log(husband.home_time_ar)) + p.tau0_h + randn(0, p.sigma_hp_h))
    # home_time_h_m =(home_time_h_m_minus_1.^ tau1_h ) * exp(tau0_h+ tau2_h * P_minus_1 + epsilon_f(draw_f, t, 4) * sigma(4, 4));
    # home_time_h_um=(home_time_h_um_minus_1.^ tau1_h) * exp(tau0_h+                    epsilon_f(draw_f, t, 4) * sigma(4, 4));

    # decision making - choose from up to 13 options, according to CHOOSE_HUSBAND, CHOOSE_WORK, AGE  values
    # utility from each option:
    # single options:
    #            1-singe + unemployed + non-pregnant
    #            3-singe + employed full  + non-pregnant
    #            5-singe + employed part + non-pregnant
    #            7-schooling: single + unemployed + non-pregnant + no children
    # wife current utility from each option:
    divorce_cost_h = p.dc_h + p.dc_h_kids * husband.kids
    ##########################################################################################################
    u_husband_single[1] = float('-inf')    # single husband can't get pregnant
    u_husband_single[3] = float('-inf')    # single husband can't get pregnant
    u_husband_single[5] = float('-inf')    # single husband can't get pregnant
    # husband (potential husband) current utility from each option:
    u_husband_single[0] = (1 / p.alpha0) * cmath.pow(budget_c_single_h_ue, p.alpha0) + \
                          ((              p.alpha12_h * husband.schooling + p.alpha13_w * husband.health) / p.alpha2) * cmath.pow((c.leisure-c.home_p),p.alpha2) + p.alpha3_h_s * kids_utility_single_h_ue + home_time_h + divorce_cost_h * husband.married
    #print ("period")
    #print(t)
    #print(u_husband_single[0])
    #temp = (1 / p.alpha0) * cmath.pow(budget_c_single_h_ue, p.alpha0)
    #print(temp)
    #temp = ((              p.alpha12_h * husband.schooling + p.alpha13_w * husband.health) / p.alpha2)* cmath.pow((c.leisure-c.home_p),p.alpha2)
    #print(temp)
    #temp = p.alpha3_h_s * kids_utility_single_h_ue
    #print(temp)
    #print(home_time_h)
    #print(husband.married)

    if wage_h_full > 0:  # to avoid division by zero
        u_husband_single[2] = (1 / p.alpha0) * cmath.pow(budget_c_single_h_ef, p.alpha0) + \
                              p.alpha3_h_s * kids_utility_single_h_ef + divorce_cost_h * husband.married
    else:
        u_husband_single[2] = float('-inf')
    if wage_h_part > 0:  # capacity_w=0.5
        u_husband_single[4] = (1 / p.alpha0) * cmath.pow(budget_c_single_h_ep, p.alpha0) + \
                              ((              p.alpha12_w * husband.schooling + p.alpha13_w * husband.health) / p.alpha2) * cmath.pow((c.leisure_part-c.home_p), p.alpha2) + p.alpha3_h_s * kids_utility_single_h_ep + \
                              home_time_h * (1 - 0.5 - c.home_p) + divorce_cost_h * husband.married
    else:
        u_husband_single[4] = float('-inf')
    u_husband_single[6] = school_utility_h  # in school-no leisure, no income, but utility from schooling+increase future value
    # calculate expected utility = current utility + emax value if t<T. = current utility + terminal value if t==T

    if t == c.max_period -1:
        u_husband[0]= u_husband_single[0] + p.t6_h*husband.hsg+p.t7_h*husband.sc+p.t8_h*husband.cg+p.t9_h*husband.pc+p.t10_h*husband.exp
        u_husband[1]= float('-inf') # can't get pregnant at 60
        if wage_h_full > 0:  # to avoid division by zero
            u_husband[2]= u_husband_single[2] + p.t6_h*husband.hsg+p.t7_h*husband.sc+p.t8_h*husband.cg+p.t9_h*husband.pc+p.t10_h*(husband.exp+1) #one more year of experience
        else:
            u_husband[2] = float('-inf')
        u_husband[3]= float('-inf') # can't get pregnant at 60
        if wage_h_part > 0:
            u_husband[4]= u_husband_single[4] + p.t6_h*husband.hsg+p.t7_h*husband.sc+p.t8_h*husband.cg+p.t9_h*husband.pc+p.t10_h*(husband.exp+0.5) #one more year of experience
        else:
            u_husband[4] = float('-inf')
        u_husband[5] = float('-inf') # can't get pregnant at 60
        u_husband[6]= float('-inf') # can't go to school at 60
    #####################################################################   ADD EMAX    ########################
    # t - time 17-65
    # schooling - 5 levels grid
    # experience - 5 level grid
    # number of children - 4 level grid
    # health - 2 level grid
    # home time ar process - 3 level grid
    # ability_index - 3 level grid
    # parents education - 2 levels grid
    # parents marital status - 2 levels
    # EMAX_M_UM(t,husband.schooling, husband.exp_index,husband.kids, husband.health, husband.home_time_index,husband.ability_i, husband.mother_educ, husband.mother_marital)
    # need to take care of experience and number of children when calling the EMAX:
    # if women is pregnant, add 1 to the number of children unless the number is already 4
    elif t < c.max_period - 1:
        husband_exp_index = exp_to_index(husband.exp)
        husband_home_time_index = home_time_to_index(home_time_h)
        husband_ability_index = ability_to_index(husband.ability_i)
        husband_mother_educ_index = c.mother_educ
        husband_mother_marital_index = c.mother_marital
        u_husband[0] = u_husband_single[0] + c.beta0 * h_s_emax[t+1, husband.schooling, husband_exp_index, husband.kids, husband.health, husband_home_time_index, husband_ability_index, husband_mother_educ_index, husband_mother_marital_index]
        u_husband[1] = float('-inf') # can't get pregnant after 40
        if wage_h_full > 0:
            husband_exp_index = exp_to_index(husband.exp+1)
            u_husband[2] = u_husband_single[2] + c.beta0 * h_s_emax[t+1, husband.schooling, husband_exp_index, husband.kids, husband.health, husband_home_time_index, husband_ability_index, husband_mother_educ_index, husband_mother_marital_index]
        else:
            u_husband[2] = float('-inf')
        u_husband[3] = float('-inf')
        if wage_h_part > 0:
            husband_exp_index = exp_to_index(husband.exp+0.5)
            u_husband[4] = u_husband_single[4] + c.beta0 * h_s_emax[t+1, husband.schooling, husband_exp_index,husband.kids, husband.health, husband_home_time_index,husband_ability_index, husband_mother_educ_index, husband_mother_marital_index]
        else:
            u_husband[4] = float('-inf')
        u_husband[5] = float('-inf')
        if husband.age < 31 and husband.schooling < 4:
            school_index = min(husband.schooling+1,4)
            u_husband[6] = u_husband_single[6] + c.beta0 * h_s_emax[t+1, school_index, husband_exp_index, husband.kids, husband.health, husband_home_time_index,husband_ability_index, husband_mother_educ_index, husband_mother_marital_index]
        else:
            u_husband[6] = float('-inf')
    else:
        assert()
    ###################################################################################
    single_value = max(u_husband)
    single_index = np.argmax(u_husband)

    return single_value, single_index
