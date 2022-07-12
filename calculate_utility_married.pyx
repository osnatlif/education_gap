import numpy as np
cimport libc.math as cmath
from parameters import p
from value_to_index cimport exp_to_index
from value_to_index cimport home_time_to_index
from value_to_index cimport ability_to_index

cimport gross_to_net as tax
from draw_husband cimport Husband
from draw_wife cimport Wife
cimport constant_parameters as c


cpdef tuple calculate_utility_married(double[:, :, :, :, :, :, :, :, :, :, :, :, :, :, :, :] w_emax,
    double[:, :, :, :, :, :, :, :, :, :, :, :, :, :, :, :] h_emax,
    double wage_h_part, double wage_h_full, double wage_w_part, double wage_w_full, Wife wife, Husband husband, int t):
    #####################################################################################################
    ##### declare variables anf initilize
    #####################################################################################################
    cdef int kids_temp = 0
    cdef double net_income_married_Wue_Hue = 0
    cdef double net_income_married_Wue_Hef = 0
    cdef double net_income_married_Wue_Hep = 0
    cdef double net_income_married_Wef_Hue = 0
    cdef double net_income_married_Wef_Hef = 0
    cdef double net_income_married_Wef_Hep = 0
    cdef double net_income_married_Wep_Hue = 0
    cdef double net_income_married_Wep_Hef = 0
    cdef double net_income_married_Wep_Hep = 0
    cdef double eta = 0
    cdef double budget_c_married_Wue_Hue = 0
    cdef double budget_c_married_Wue_Hef = 0
    cdef double budget_c_married_Wue_Hep = 0
    cdef double budget_c_married_Wef_Hue = 0
    cdef double budget_c_married_Wef_Hef = 0
    cdef double budget_c_married_Wef_Hep = 0
    cdef double budget_c_married_Wep_Hue = 0
    cdef double budget_c_married_Wep_Hef = 0
    cdef double budget_c_married_Wep_Hep = 0
    cdef double kids_utility_married_Wue_Hue = 0
    cdef double kids_utility_married_Wue_Hef = 0
    cdef double kids_utility_married_Wue_Hep = 0
    cdef double kids_utility_married_Wef_Hue = 0
    cdef double kids_utility_married_Wef_Hef = 0
    cdef double kids_utility_married_Wef_Hep = 0
    cdef double kids_utility_married_Wep_Hue = 0
    cdef double kids_utility_married_Wep_Hef = 0
    cdef double kids_utility_married_Wep_Hep = 0
    cdef double preg_utility = float('-inf')
    cdef double home_time_h = 0
    cdef double home_time_w = 0
    cdef double home_time_h_preg = 0
    cdef double home_time_w_preg = 0
    cdef double marriage_utility = 0
    cdef double marriage_cost_h = 0
    cdef double marriage_cost_w = 0
    cdef double[:] uc_wife = np.empty(18)
    cdef double[:] uc_husband = np.empty(18)
    cdef double[:] u_wife = np.empty(18)
    cdef double[:] u_husband = np.empty(18)
    cdef int h_exp_index = 0
    cdef int h_exp_index_f = 0
    cdef int h_exp_index_p = 0
    cdef int h_home_time_index = 0
    cdef int h_home_time_index_preg = 0
    cdef int w_exp_index = 0
    cdef int w_exp_index_f = 0
    cdef int w_exp_index_p = 0
    cdef int w_home_time_index = 0
    cdef int w_home_time_index_preg = 0
    cdef int mother_educ_index = 0
    cdef int mother_marital_index = 0
    cdef double temp
    # in variables' names: first index wife, second husband
    kids_temp = wife.kids + husband.kids   # if married, kids only at wife object.if consider getting married, add both kids
    net_income_married_Wue_Hue  = c.ub_w + c.ub_h
    net_income_married_Wue_Hef  = c.ub_w + tax.gross_to_net_married(kids_temp,   0   , wage_h_full, t)
    net_income_married_Wue_Hep  = c.ub_w + tax.gross_to_net_married(kids_temp,   0   , wage_h_part, t)
    ###############
    net_income_married_Wef_Hue  = c.ub_h + tax.gross_to_net_married(kids_temp, wage_w_full,  0         , t)
    net_income_married_Wef_Hef  =          tax.gross_to_net_married(kids_temp, wage_w_full, wage_h_full , t)
    net_income_married_Wef_Hep  =          tax.gross_to_net_married(kids_temp, wage_w_full, wage_h_part , t)
    ###################
    net_income_married_Wep_Hue = c.ub_h + tax.gross_to_net_married(kids_temp, wage_w_part,    0       , t)
    net_income_married_Wep_Hef =          tax.gross_to_net_married(kids_temp, wage_w_part, wage_h_full, t)
    net_income_married_Wep_Hep =          tax.gross_to_net_married(kids_temp, wage_w_part, wage_h_part, t)
    # budget constraint
    if kids_temp == 0:
        eta = 0
    elif kids_temp == 1:
        eta = c.eta1            # this is the fraction of parent's income that one child gets
    elif kids_temp == 2:
        eta = c.eta2
    elif kids_temp == 3:
        eta = c.eta3
    else:
        assert()

    # first index wife, second husband
    budget_c_married_Wue_Hue  = (1-eta)*net_income_married_Wue_Hue
    if wage_h_full > 0:
        budget_c_married_Wue_Hef  = (1-eta)*net_income_married_Wue_Hef
    if wage_h_part > 0:
        budget_c_married_Wue_Hep  = (1-eta)*net_income_married_Wue_Hep
    ############
    if wage_w_full > 0:
        budget_c_married_Wef_Hue  = (1-eta)*net_income_married_Wef_Hue
        if wage_h_full > 0:
            budget_c_married_Wef_Hef  = (1-eta)*net_income_married_Wef_Hef
        if wage_h_part > 0:
            budget_c_married_Wef_Hep  = (1-eta)*net_income_married_Wef_Hep
    ###########
    if wage_w_part > 0:
        budget_c_married_Wep_Hue  = (1-eta)*net_income_married_Wep_Hue
        if wage_h_full > 0:
            budget_c_married_Wep_Hef  = (1-eta)*net_income_married_Wep_Hef
        if wage_h_part > 0:
            budget_c_married_Wep_Hep  = (1-eta)*net_income_married_Wep_Hep

    # I assume that each kid get 20% (eta1). if the family has 2 kids, each gets 20%, yet the total is 32% (eta2) since part is common
    if kids_temp > 0:
        # first index wife, second husband
        kids_utility_married_Wue_Hue = (p.row1_w*cmath.pow(1.0-c.home_p, p.row0) +
                                       p.row1_h*cmath.pow(1.0-c.home_p, p.row0) +
                                       p.row2*cmath.pow(c.eta1*net_income_married_Wue_Hue, p.row0) +
                                       (1-p.row1_w-p.row1_h-p.row2)*cmath.pow(cmath.pow(kids_temp, p.row0), 1.0/p.row0))
        if wage_h_full > 0:
            kids_utility_married_Wue_Hef = (p.row1_w*cmath.pow(1.0-c.home_p, p.row0) +
                                            p.row2*cmath.pow(c.eta1*net_income_married_Wue_Hef, p.row0) +
                                            (1-p.row1_w-p.row1_h-p.row2)*cmath.pow(cmath.pow(kids_temp, p.row0), 1.0/p.row0))
        if wage_h_part > 0:
            kids_utility_married_Wue_Hep = (p.row1_w*cmath.pow(1.0-c.home_p, p.row0) +
                                            p.row1_h*cmath.pow(1.0-0.5-c.home_p, p.row0) +
                                            p.row2*cmath.pow(c.eta1*net_income_married_Wue_Hep, p.row0) +
                                            (1-p.row1_w-p.row1_h-p.row2)*cmath.pow(cmath.pow(kids_temp, p.row0), 1.0/p.row0))
        #########################
        if wage_w_full > 0:
            kids_utility_married_Wef_Hue = (p.row1_h*cmath.pow(1.0-c.home_p, p.row0) +
                                            p.row2*cmath.pow(c.eta1*net_income_married_Wef_Hue, p.row0) +
                                            (1-p.row1_w-p.row1_h-p.row2)*cmath.pow(cmath.pow(kids_temp, p.row0), 1.0/p.row0))
            if wage_h_full > 0:
                kids_utility_married_Wef_Hef = (p.row2*cmath.pow(c.eta1*net_income_married_Wef_Hef, p.row0) +
                                                (1-p.row1_w-p.row1_h-p.row2)*cmath.pow(cmath.pow(kids_temp, p.row0), 1.0/p.row0))
            if wage_h_part > 0:
                kids_utility_married_Wef_Hep = (p.row1_h*cmath.pow(1.0-0.5-c.home_p, p.row0) +
                                                p.row2*cmath.pow(c.eta1*net_income_married_Wef_Hep, p.row0) +
                                                (1-p.row1_w-p.row1_h-p.row2)*cmath.pow(cmath.pow(kids_temp, p.row0), 1.0/p.row0))
        #####################
        if wage_w_part > 0:
            kids_utility_married_Wep_Hue = (p.row1_w*cmath.pow(1.0-0.5-c.home_p, p.row0) +
                                            p.row1_h*cmath.pow(1.0-c.home_p, p.row0) +
                                            p.row2*cmath.pow(c.eta1*net_income_married_Wep_Hue, p.row0) +
                                            (1-p.row1_w-p.row1_h-p.row2)*cmath.pow(cmath.pow(kids_temp, p.row0), 1.0/p.row0))
            if wage_h_full > 0:
                kids_utility_married_Wep_Hef = (p.row1_w*cmath.pow(1.0-0.5-c.home_p, p.row0) +
                                                p.row2*cmath.pow(c.eta1*net_income_married_Wep_Hef, p.row0) +
                                                (1-p.row1_w-p.row1_h-p.row2)*cmath.pow(cmath.pow(kids_temp, p.row0), 1.0/p.row0))
            if wage_h_part > 0:
                kids_utility_married_Wep_Hep = (p.row1_w*cmath.pow(1.0-0.5-c.home_p, p.row0) +
                                                p.row1_h*cmath.pow(1.0-0.5-c.home_p, p.row0) +
                                                p.row2*cmath.pow(c.eta1*net_income_married_Wep_Hep, p.row0) +
                                                (1-p.row1_w-p.row1_h-p.row2)*cmath.pow(cmath.pow(kids_temp, p.row0), 1.0/p.row0))
    elif kids_temp == 0:
        kids_utility_married_Wue_Hue = 0
        kids_utility_married_Wue_Hef = 0
        kids_utility_married_Wue_Hep = 0
        kids_utility_married_Wef_Hue = 0
        kids_utility_married_Wef_Hef = 0
        kids_utility_married_Wef_Hep = 0
        kids_utility_married_Wep_Hue = 0
        kids_utility_married_Wep_Hef = 0
        kids_utility_married_Wep_Hep = 0
    # utility from pregnancy when married / utility from pregnancy when SINGLE
    if wife.age < 40:
        preg_utility = p.preg_health * wife.health + p.preg_kids * kids_temp + p.preg_t_minus1 * wife.preg + np.random.normal(0, 1) * p.sigma_p
    else:
        preg_utility = float('-inf')
        # if husband is not married his home time is not influence by a newborn, the wife is influenced of course, so home time for her is not function of M
    home_time_h = cmath.exp(p.tau1_h * cmath.log(husband.home_time_ar) + p.tau0_h  + np.random.normal(0, 1) * p.sigma_hp_h)
    home_time_w = cmath.exp(p.tau1_h * cmath.log(wife.home_time_ar)    + p.tau0_w  + np.random.normal(0, 1) * p.sigma_hp_w)
    if wife.age < 40:
        home_time_h_preg = cmath.exp(p.tau1_h * cmath.log(husband.home_time_ar) + p.tau0_h + p.tau2_h + np.random.normal(0, 1) * p.sigma_hp_h)
        home_time_w_preg = cmath.exp(p.tau1_h * cmath.log(wife.home_time_ar) + p.tau0_w + p.tau2_w + np.random.normal(0, 1) * p.sigma_hp_w)
    else:
        home_time_h_preg = float('-inf')
        home_time_w_preg = float('-inf')
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    if wife.schooling == husband. schooling:
        marriage_utility = p.taste_c + p.taste_health * cmath.pow(wife.health - husband.health, 2) +                np.random.normal(0, 1) * p.sigma_q  # utility from marriage
    elif wife.schooling < husband. schooling:
        marriage_utility = p.taste_c + p.taste_health * cmath.pow(wife.health - husband.health, 2) + p.taste_w_up + np.random.normal(0, 1) * p.sigma_q  # utility from marriage
    else:
        marriage_utility = p.taste_c + p.taste_health * cmath.pow(wife.health - husband.health, 2) + p.taste_w_down + np.random.normal(0, 1) * p.sigma_q  # utility from marriage
    marriage_cost_h = p.mc + p.mc_by_parents * husband.mother_marital
    marriage_cost_w = p.mc + p.mc_by_parents * wife.mother_marital
    # marriage options:# first index wife, second husband
    #            0-married + women unemployed  +man unemployed     +non-pregnant
    #                        1-married + women unemployed  +man unemployed     +pregnant
    #                        2-married + women unemployed  +man employed full  +non-pregnant
    #                        3-married + women unemployed  +man employed full  +pregnant
    #                        4-married + women unemployed  +man employed part  +non-pregnant
    #                        5-married + women unemployed  +man employed part  +pregnant
    #            6-married + women employed full   +man unemployed     +non-pregnant
    #                        7-married + women employed full   +man unemployed     +pregnant
    #                        8-married + women employed full   +man employed full  +non-pregnant
    #                        9-married + women employed full +man employed full  +pregnant
    #                        10-married + women employed full +man employed part  +non-pregnant
    #                        11-married + women employed full +man employed part  +pregnant
    #            12-married + women employed part  +man unemployed     +non-pregnant
    #                        13-married + women employed part +man unemployed     +pregnant
    #                        14-married + women employed part +man employed full  +non-pregnant
    #                        15-married + women employed part +man employed full  +pregnant
    #                        16-married + women employed part +man employed part  +non-pregnant
    #                        17-married + women employed part  +man employed part  +pregnant
    # marriage options:# first index wife, second husband
    uc_wife[0] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wue_Hue, p.alpha0) + marriage_cost_w * (1-wife.married) + \
                 ((              p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2)*cmath.pow(1, p.alpha2) + p.alpha3_w_m * kids_utility_married_Wue_Hue + home_time_w
    uc_wife[1] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wue_Hue, p.alpha0) + marriage_cost_w * (1-wife.married) + \
                 ((p.alpha11_w + p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2)*cmath.pow(1, p.alpha2) + p.alpha3_w_m * kids_utility_married_Wue_Hue + home_time_w_preg + preg_utility
    uc_husband[0] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wue_Hue, p.alpha0) + marriage_cost_h * (1 - husband.married) + \
                    ((             p.alpha12_h * husband.schooling + p.alpha13_h * husband.health) / p.alpha2) * cmath.pow(1, p.alpha2) + p.alpha3_h_m * kids_utility_married_Wue_Hue + home_time_h
    uc_husband[1] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wue_Hue, p.alpha0) + marriage_cost_h * (1 - husband.married) + \
                    ((             p.alpha12_h * husband.schooling + p.alpha13_h * husband.health) / p.alpha2) * cmath.pow(1, p.alpha2) + p.alpha3_h_m * kids_utility_married_Wue_Hue + home_time_h_preg + preg_utility

    if wage_h_full > 0:
        uc_wife[2] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wue_Hef, p.alpha0) + marriage_cost_w * (1-wife.married) + \
                     ((              p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2)*cmath.pow(1, p.alpha2) + p.alpha3_w_m * kids_utility_married_Wue_Hef + home_time_w
        uc_wife[3] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wue_Hef, p.alpha0) + marriage_cost_w * (1-wife.married) + \
                     ((p.alpha11_w + p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2)*cmath.pow(1, p.alpha2) + p.alpha3_w_m * kids_utility_married_Wue_Hef + home_time_w_preg + preg_utility
        uc_husband[2] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wue_Hef, p.alpha0) + marriage_cost_h * (1 - husband.married) + \
                        p.alpha3_h_m * kids_utility_married_Wue_Hef
        uc_husband[3] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wue_Hef, p.alpha0) + marriage_cost_h * (1 - husband.married) + \
                        p.alpha3_h_m * kids_utility_married_Wue_Hef + preg_utility
    else:
        uc_wife[2] = float('-inf')
        uc_wife[3] = float('-inf')
        uc_husband[2] = float('-inf')
        uc_husband[3] = float('-inf')

    if wage_h_part > 0:
        uc_wife[4] = marriage_utility + (1 / p.alpha0) * cmath.pow(budget_c_married_Wue_Hep, p.alpha0) + marriage_cost_w * (1-wife.married) + \
                     ((              p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2)*cmath.pow(1, p.alpha2) + p.alpha3_w_m * kids_utility_married_Wue_Hep + home_time_w
        uc_wife[5] = marriage_utility + (1 / p.alpha0) * cmath.pow(budget_c_married_Wue_Hep, p.alpha0) + marriage_cost_w * (1-wife.married)  + \
                     ((p.alpha11_w + p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2)*cmath.pow(1, p.alpha2) + p.alpha3_w_m * kids_utility_married_Wue_Hep + home_time_w_preg + preg_utility
        uc_husband[4] = marriage_utility + (1 / p.alpha0) * cmath.pow(budget_c_married_Wue_Hep, p.alpha0) + marriage_cost_h * (1 - husband.married) + \
                        ((         p.alpha12_h * husband.schooling + p.alpha13_h * husband.health) / p.alpha2) * cmath.pow(1 - 0.5 - c.home_p, p.alpha2) + p.alpha3_h_m * kids_utility_married_Wue_Hep + home_time_h * (1 - 0.5 - c.home_p)
        uc_husband[5] = marriage_utility + (1 / p.alpha0) * cmath.pow(budget_c_married_Wue_Hep, p.alpha0) + marriage_cost_h * (1 - husband.married) + \
                        ((         p.alpha12_h * husband.schooling + p.alpha13_h * husband.health) / p.alpha2) * cmath.pow(1 - 0.5 - c.home_p, p.alpha2) + p.alpha3_h_m * kids_utility_married_Wue_Hep + home_time_h_preg * (1 - 0.5 - c.home_p) + preg_utility
    else:
        uc_wife[4] = float('-inf')
        uc_wife[5] = float('-inf')
        uc_husband[4] = float('-inf')
        uc_husband[5] = float('-inf')

    if wage_w_full > 0:    # capacity_w=0.5
        uc_wife[6]= marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wef_Hue, p.alpha0) + p.alpha3_w_m * kids_utility_married_Wef_Hue + marriage_cost_w * (1-wife.married)
        uc_wife[7]= marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wef_Hue, p.alpha0) + p.alpha3_w_m * kids_utility_married_Wef_Hue + marriage_cost_w * (1-wife.married) + preg_utility
        uc_husband[6] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wef_Hue, p.alpha0) + p.alpha3_h_m * kids_utility_married_Wef_Hue + marriage_cost_h * (1 - husband.married) + \
                        ((              p.alpha12_h * husband.schooling + p.alpha13_h * husband.health) / p.alpha2) * cmath.pow(1, p.alpha2) + home_time_h
        uc_husband[7] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wef_Hue, p.alpha0) + p.alpha3_h_m * kids_utility_married_Wef_Hue + marriage_cost_w * (1 - husband.married) + preg_utility + \
                        ((              p.alpha12_h * husband.schooling + p.alpha13_h * husband.health) / p.alpha2) * cmath.pow(1, p.alpha2) + home_time_h_preg
        if wage_h_full > 0:             # both employed full
            uc_wife[8] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wef_Hef, p.alpha0) +  p.alpha3_w_m * kids_utility_married_Wef_Hef + marriage_cost_w * (1-wife.married)
            uc_wife[9] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wef_Hef, p.alpha0) + p.alpha3_w_m * kids_utility_married_Wef_Hef +  marriage_cost_w * (1-wife.married) +preg_utility
            uc_husband[8] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wef_Hef, p.alpha0) +  p.alpha3_h_m * kids_utility_married_Wef_Hef + marriage_cost_h * (1-husband.married)
            uc_husband[9] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wef_Hef, p.alpha0) + p.alpha3_h_m * kids_utility_married_Wef_Hef +  marriage_cost_h * (1-husband.married) +preg_utility
        else:
            uc_wife[8] = float('-inf')
            uc_wife[9] = float('-inf')
            uc_husband[8] = float('-inf')
            uc_husband[9] = float('-inf')
        if wage_h_part > 0:
            uc_wife[10] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wef_Hep, p.alpha0) + p.alpha3_w_m * kids_utility_married_Wef_Hep + marriage_cost_w * (1-wife.married)
            uc_wife[11] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wef_Hep, p.alpha0) + p.alpha3_w_m * kids_utility_married_Wef_Hep + marriage_cost_w * (1-wife.married) + preg_utility
            uc_husband[10] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wef_Hep, p.alpha0) + p.alpha3_h_m * kids_utility_married_Wef_Hep + marriage_cost_h * (1 - husband.married)
            ((              p.alpha12_h * husband.schooling + p.alpha13_h * husband.health) / p.alpha2) * cmath.pow(1 - 0.5 - c.home_p, p.alpha2)  + home_time_h * (1 - 0.5 - c.home_p)
            uc_husband[11] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wef_Hep, p.alpha0) + p.alpha3_h_m * kids_utility_married_Wef_Hep + marriage_cost_h * (1 - husband.married) + preg_utility
            ((              p.alpha12_h * husband.schooling + p.alpha13_h * husband.health) / p.alpha2) * cmath.pow(1 - 0.5 - c.home_p, p.alpha2) + home_time_h_preg * (1 - 0.5 - c.home_p) + preg_utility
        else:
            uc_wife[10] = float('-inf')
            uc_wife[11] = float('-inf')
            uc_husband[10] = float('-inf')
            uc_husband[11] = float('-inf')
    else:
        uc_wife[6] = float('-inf')
        uc_wife[7] = float('-inf')
        uc_wife[8] = float('-inf')
        uc_wife[9] = float('-inf')
        uc_wife[10] = float('-inf')
        uc_wife[11] = float('-inf')
        uc_husband[6] = float('-inf')
        uc_husband[7] = float('-inf')
        uc_husband[8] = float('-inf')
        uc_husband[9] = float('-inf')
        uc_husband[10] = float('-inf')
        uc_husband[11] = float('-inf')
    ##################################################################################################################
    if wage_w_part > 0:  # if wife got part-time job offer
        uc_wife[12] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wep_Hue, p.alpha0) + p.alpha3_w_m * kids_utility_married_Wep_Hue + marriage_cost_w * (1-wife.married) \
                      + ((p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2) * cmath.pow(1-0.5-c.home_p, p.alpha2) + home_time_w*(1-0.5-c.home_p)
        uc_wife[13] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wep_Hue, p.alpha0) + p.alpha3_w_m * kids_utility_married_Wep_Hue + marriage_cost_w * (1-wife.married) \
                      + ((p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2) * cmath.pow(1-0.5-c.home_p, p.alpha2) + home_time_w_preg*(1-0.5-c.home_p) + preg_utility
        uc_husband[12] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wep_Hue, p.alpha0) + p.alpha3_h_m * kids_utility_married_Wep_Hue + marriage_cost_h * (1 - husband.married) \
                         + ((p.alpha12_h * husband.schooling + p.alpha13_h * husband.health) / p.alpha2) * cmath.pow(1 - c.home_p, p.alpha2) + home_time_h
        uc_husband[13] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wep_Hue, p.alpha0) + p.alpha3_h_m * kids_utility_married_Wep_Hue + marriage_cost_h * (1 - husband.married) \
                         + ((p.alpha12_h * husband.schooling + p.alpha13_h * husband.health) / p.alpha2) * cmath.pow(1 - c.home_p, p.alpha2) + home_time_h_preg + preg_utility
        if wage_h_full > 0:
            uc_wife[14] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wep_Hef, p.alpha0) + p.alpha3_w_m * kids_utility_married_Wep_Hef + marriage_cost_w * (1-wife.married) \
                          + ((p.alpha11_w + p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2) * cmath.pow(1-0.5-c.home_p, p.alpha2) + home_time_w*(1-0.5-c.home_p)
            uc_wife[15] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wep_Hef, p.alpha0) + p.alpha3_w_m * kids_utility_married_Wep_Hef + marriage_cost_w * (1-wife.married) \
                          + ((p.alpha11_w + p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2) * cmath.pow(1-0.5-c.home_p,p.alpha2) + home_time_w_preg*(1-0.5-c.home_p) + preg_utility
            uc_husband[14] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wep_Hef, p.alpha0) + p.alpha3_h_m * kids_utility_married_Wep_Hef + marriage_cost_h * (1-husband.married)
            uc_husband[15] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wep_Hef, p.alpha0) + p.alpha3_h_m * kids_utility_married_Wep_Hef + marriage_cost_h * (1-husband.married) + preg_utility
        else:
            uc_wife[14] = float('-inf')
            uc_wife[15] = float('-inf')
            uc_husband[14] = float('-inf')
            uc_husband[15] = float('-inf')
        if wage_h_part > 0:
            uc_wife[16] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wep_Hep, p.alpha0) + p.alpha3_w_m * kids_utility_married_Wep_Hep + marriage_cost_w * (1-wife.married) \
                          + ((               p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2) * cmath.pow(1 - 0.5 - c.home_p, p.alpha2) + home_time_w*(1 - 0.5 - c.home_p)
            uc_wife[17] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wep_Hep, p.alpha0) + p.alpha3_w_m * kids_utility_married_Wep_Hep + marriage_cost_w * (1-wife.married) \
                          + ((p.alpha11_w + p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2) * cmath.pow(1 - 0.5 - c.home_p, p.alpha2) + home_time_w_preg*(1 - 0.5 - c.home_p) + preg_utility
            uc_husband[16] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wep_Hep, p.alpha0) + p.alpha3_h_m * kids_utility_married_Wep_Hep + marriage_cost_h * (1-husband.married) \
                             + ((              p.alpha12_h * husband.schooling + p.alpha13_h * husband.health)/p.alpha2) * cmath.pow(1 - 0.5 - c.home_p, p.alpha2) + home_time_h*(1 - 0.5 - c.home_p)
            uc_husband[17] = marriage_utility + (1/p.alpha0) * cmath.pow(budget_c_married_Wep_Hep, p.alpha0) + p.alpha3_h_m * kids_utility_married_Wep_Hep + marriage_cost_h * (1-husband.married) \
                             + ((              p.alpha12_h * husband.schooling + p.alpha13_h * husband.health)/p.alpha2) * cmath.pow(1 - 0.5 - c.home_p, p.alpha2) + home_time_h_preg*(1 - 0.5 - c.home_p) + preg_utility
        else:
            uc_wife[16] = float('-inf')
            uc_wife[17] = float('-inf')
            uc_husband[16] = float('-inf')
            uc_husband[17] = float('-inf')
    else:
        uc_wife[12] = float('-inf')
        uc_wife[13] = float('-inf')
        uc_wife[14] = float('-inf')
        uc_wife[15] = float('-inf')
        uc_wife[16] = float('-inf')
        uc_wife[17] = float('-inf')
        uc_husband[12] = float('-inf')
        uc_husband[13] = float('-inf')
        uc_husband[14] = float('-inf')
        uc_husband[15] = float('-inf')
        uc_husband[16] = float('-inf')
        uc_husband[17] = float('-inf')
    ##################################################################################################
    ##################################################################################################
    ########               add emax or terminal value                                         ########
    ##################################################################################################
    ##################################################################################################
    if t == c.max_period - 1:
        u_wife[0] = uc_wife[0] + p.t1_w*wife.hsg + p.t2_w*wife.sc + p.t3_w*wife.cg + p.t4_w*wife.pc + p.t5_w*wife.exp + p.t6_w*husband.hsg + p.t7_w*husband.sc + p.t8_w*husband.cg + p.t9_w*husband.pc + p.t10_w*husband.exp + p.t11_w * marriage_utility
        u_wife[1] = float('-inf')
        u_husband[0] = uc_husband[0] + p.t1_h * wife.hsg + p.t2_h * wife.sc + p.t3_h * wife.cg + p.t4_h * wife.pc + p.t5_h * wife.exp + p.t6_h * husband.hsg + p.t7_h * husband.sc + p.t8_h * husband.cg + p.t9_h * husband.pc + p.t10_h * husband.exp + p.t11_h * marriage_utility
        u_husband[1] = float('-inf')
        if wage_h_full > 0:
            u_wife[2] =    uc_wife[2]    + p.t1_w * wife.hsg + p.t2_w * wife.sc + p.t3_w * wife.cg + p.t4_w * wife.pc + p.t5_w * wife.exp + p.t6_w * husband.hsg + p.t7_w * husband.sc + p.t8_w * husband.cg + p.t9_w * husband.pc + p.t10_w * (husband.exp+1) + p.t11_w * marriage_utility
            u_husband[2] = uc_husband[2] + p.t1_h * wife.hsg + p.t2_h * wife.sc + p.t3_h * wife.cg + p.t4_h * wife.pc + p.t5_h * wife.exp + p.t6_h * husband.hsg + p.t7_h * husband.sc + p.t8_h * husband.cg + p.t9_h * husband.pc + p.t10_h * (husband.exp+1) + p.t11_h * marriage_utility
        else:
            u_wife[2] = float('-inf')
            u_husband[2] = float('-inf')
        u_wife[3] = float('-inf')
        u_husband[3]= float('-inf')
        if wage_h_part > 0:
            u_wife[4] =       uc_wife[4] + p.t1_w * wife.hsg + p.t2_w * wife.sc + p.t3_w * wife.cg + p.t4_w * wife.pc + p.t5_w * wife.exp + p.t6_w * husband.hsg + p.t7_w * husband.sc + p.t8_w * husband.cg + p.t9_w * husband.pc + p.t10_w * (husband.exp+0.5) + p.t11_w * marriage_utility
            u_husband[4] = uc_husband[4] + p.t1_h * wife.hsg + p.t2_h * wife.sc + p.t3_h * wife.cg + p.t4_h * wife.pc + p.t5_h * wife.exp + p.t6_h * husband.hsg + p.t7_h * husband.sc + p.t8_h * husband.cg + p.t9_h * husband.pc + p.t10_h * (husband.exp+0.5) + p.t11_h * marriage_utility
        else:
            u_wife[4] = float('-inf')
            u_husband[4] = float('-inf')
        u_wife[5] = float('-inf')
        u_husband[5] = float('-inf')
        if wage_w_full > 0:
            u_wife[6] = uc_wife[6] + p.t1_w * wife.hsg + p.t2_w * wife.sc + p.t3_w * wife.cg + p.t4_w * wife.pc + p.t5_w * (wife.exp+1) + p.t6_w * husband.hsg + p.t7_w * husband.sc + p.t8_w * husband.cg + p.t9_w * husband.pc + p.t10_w * husband.exp + p.t11_w * marriage_utility
            u_husband[6] = uc_husband[6] + p.t1_h * wife.hsg + p.t2_h * wife.sc + p.t3_h * wife.cg + p.t4_h * wife.pc + p.t5_h * (wife.exp+1) + p.t6_h * husband.hsg + p.t7_h * husband.sc + p.t8_h * husband.cg + p.t9_h * husband.pc + p.t10_h * husband.exp + p.t11_h * marriage_utility
        else:
            u_wife[6] = float('-inf')
            u_husband[6] = float('-inf')
        u_wife[7] = float('-inf')
        u_husband[7] = float('-inf')
        if wage_h_full > 0 and wage_w_full > 0:
            u_wife[8] = uc_wife[8] + p.t1_w * wife.hsg + p.t2_w * wife.sc + p.t3_w * wife.cg + p.t4_w * wife.pc + p.t5_w * (wife.exp+1) + p.t6_w * husband.hsg + p.t7_w * husband.sc + p.t8_w * husband.cg + p.t9_w * husband.pc + p.t10_w * (husband.exp+1) + p.t11_w * marriage_utility
            u_husband[8] = uc_husband[8] + p.t1_h * wife.hsg + p.t2_h * wife.sc + p.t3_h * wife.cg + p.t4_h * wife.pc + p.t5_h * (wife.exp+1) + p.t6_h * husband.hsg + p.t7_h * husband.sc + p.t8_h * husband.cg + p.t9_h * husband.pc + p.t10_h * (husband.exp+1) + p.t11_h * marriage_utility
        else:
            u_wife[8] = float('-inf')
            u_husband[8] = float('-inf')
        u_wife[9] = float('-inf')
        u_husband[9] = float('-inf')
        if wage_h_part > 0 and wage_w_full > 0:
            u_wife[10] = uc_wife[10] + p.t1_w * wife.hsg + p.t2_w * wife.sc + p.t3_w * wife.cg + p.t4_w * wife.pc + p.t5_w * (wife.exp+1) + p.t6_w * husband.hsg + p.t7_w * husband.sc + p.t8_w * husband.cg + p.t9_w * husband.pc + p.t10_w * (husband.exp+0.5) + p.t11_w * marriage_utility
            u_husband[10] = uc_husband[10] + p.t1_h * wife.hsg + p.t2_h * wife.sc + p.t3_h * wife.cg + p.t4_h * wife.pc + p.t5_h * (wife.exp+1) + p.t6_h * husband.hsg + p.t7_h * husband.sc + p.t8_h * husband.cg + p.t9_h * husband.pc + p.t10_h * (husband.exp+0.5) + p.t11_h * marriage_utility
        else:
            u_wife[10] = float('-inf')
            u_husband[10] = float('-inf')
        u_wife[11]= float('-inf')
        u_husband[11] = float('-inf')
        if wage_w_part > 0:
            u_wife[12] = uc_wife[12] + p.t1_w * wife.hsg + p.t2_w * wife.sc + p.t3_w * wife.cg + p.t4_w * wife.pc + p.t5_w * (wife.exp+0.5) + p.t6_w * husband.hsg + p.t7_w * husband.sc + p.t8_w * husband.cg + p.t9_w * husband.pc + p.t10_w * husband.exp + p.t11_w * marriage_utility
            u_husband[12] = uc_husband[12] + p.t1_h * wife.hsg + p.t2_h * wife.sc + p.t3_h * wife.cg + p.t4_h * wife.pc + p.t5_h * (wife.exp+0.5) + p.t6_h * husband.hsg + p.t7_h * husband.sc + p.t8_h * husband.cg + p.t9_h * husband.pc + p.t10_h * husband.exp + p.t11_h * marriage_utility
        else:
            u_wife[12] = float('-inf')
            u_husband[12] = float('-inf')
        u_wife[13]= float('-inf')
        u_husband[13] = float('-inf')
        if wage_h_full > 0 and wage_w_part > 0:
            u_wife[14] = uc_wife[14] + p.t1_w * wife.hsg + p.t2_w * wife.sc + p.t3_w * wife.cg + p.t4_w * wife.pc + p.t5_w * (wife.exp+0.5) + p.t6_w * husband.hsg + p.t7_w * husband.sc + p.t8_w * husband.cg + p.t9_w * husband.pc + p.t10_w * (husband.exp+1) + p.t11_w * marriage_utility
            u_husband[14] = uc_husband[14] + p.t1_h * wife.hsg + p.t2_h * wife.sc + p.t3_h * wife.cg + p.t4_h * wife.pc + p.t5_h * (wife.exp+0.5) + p.t6_h * husband.hsg + p.t7_h * husband.sc + p.t8_h * husband.cg + p.t9_h * husband.pc + p.t10_h * (husband.exp+1) + p.t11_h * marriage_utility
        else:
            u_wife[14] = float('-inf')
            u_husband[14] = float('-inf')
        u_wife[15]= float('-inf')
        u_husband[15] = float('-inf')
        if wage_h_part > 0 and wage_w_part > 0:
            u_wife[16] = uc_wife[16] + p.t1_w * wife.hsg + p.t2_w * wife.sc + p.t3_w * wife.cg + p.t4_w * wife.pc + p.t5_w * (wife.exp+0.5) + p.t6_w * husband.hsg + p.t7_w * husband.sc + p.t8_w * husband.cg + p.t9_w * husband.pc + p.t10_w * (husband.exp+0.5) + p.t11_w * marriage_utility
            u_husband[16] = uc_husband[16] + p.t1_h * wife.hsg + p.t2_h * wife.sc + p.t3_h * wife.cg + p.t4_h * wife.pc + p.t5_h * (wife.exp+0.5) + p.t6_h * husband.hsg + p.t7_h * husband.sc + p.t8_h * husband.cg + p.t9_h * husband.pc + p.t10_h * (husband.exp+0.5) + p.t11_h * marriage_utility
        else:
            u_wife[16] = float('-inf')
            u_husband[16] = float('-inf')
        u_wife[17] = float('-inf')
        u_husband[17] = float('-inf')
    elif t < c.max_period - 1:
        # t is not the terminal period so add emax
        # t - time 17-65
        # HS,wife.schooling - schooling - 5 levels grid
        # HK, WK - experience - 5 level grid
        # C_N, H_N , W_N - number of kids - 4 level grid
        # H_HEALTH,wife.health - health - 3 level grid
        # H_L, W_L - taste for leisure - 3 level grid
        # ability_h_index,ability_w_index - 3 level grid
        # prev_state_h,prev_state_w - work at t-1 - 3 level grid
        # PE_H, PE_W - parents education - 2 levels grid
        # p_minus_1 - pregnancy at t-1, always zero for single men

        #######################################
        # add emax to men and women's utility
        #######################################
        h_exp_index = exp_to_index(husband.exp)                        # get experience index
        h_exp_index_f = exp_to_index(husband.exp+1)                    # increase experience by 1 if full time job
        h_exp_index_p = exp_to_index(husband.exp+0.5)                  # increase experience by 0.5 if part-time job
        h_home_time_index = home_time_to_index(home_time_h)            # index of home time AR(1) if not pregnant
        h_home_time_index_preg = home_time_to_index(home_time_h_preg)  # index of home time AR(1) if pregnant
        w_exp_index = exp_to_index(wife.exp)                           # get experience index
        w_exp_index_f = exp_to_index(wife.exp+1)                       # increase experience by 1 if full time job
        w_exp_index_p = exp_to_index(wife.exp+0.5)                     # increase experience by 0.5 if part-time job
        w_home_time_index = home_time_to_index(home_time_w)            # index of home time AR(1) if not pregnant
        w_home_time_index_preg = home_time_to_index(home_time_w_preg)  # index of home time AR(1) if pregnant
        wife_ability_index = ability_to_index(wife.ability_i)
        husband_ability_index = ability_to_index(husband.ability_i)
        wife_mother_educ_index = c.mother_educ
        wife_mother_marital_index = c.mother_marital
        husband_mother_educ_index = c.mother_educ
        husband_mother_marital_index = c.mother_marital
        if kids_temp < 3:
            kids_temp_preg = kids_temp + 1   # if pregnant - add another kid to emax, but only up to 3 kids
        else:
            kids_temp_preg = 3
        u_wife[0]     = uc_wife[0]     + c.beta0 * w_emax[t+1, wife.schooling, husband.schooling, w_exp_index, h_exp_index   ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
        u_husband[0]  = uc_husband[0]  + c.beta0 * h_emax[t+1, wife.schooling, husband.schooling, w_exp_index, h_exp_index   ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
        u_wife[1]     = uc_wife[1]     + c.beta0 * w_emax[t+1, wife.schooling, husband.schooling, w_exp_index, h_exp_index ,kids_temp_preg, wife.health, husband.health, w_home_time_index_preg, h_home_time_index_preg, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
        u_husband[1]  = uc_husband[1]  + c.beta0 * h_emax[t+1, wife.schooling, husband.schooling, w_exp_index, h_exp_index ,kids_temp_preg, wife.health, husband.health, w_home_time_index_preg, h_home_time_index_preg, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
        if wage_h_full > 0:
            u_wife[2]     = uc_wife[2]     + c.beta0 * w_emax[t+1, wife.schooling, husband.schooling, w_exp_index, h_exp_index_f ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_husband[2]  = uc_husband[2]  + c.beta0 * h_emax[t+1, wife.schooling, husband.schooling, w_exp_index, h_exp_index_f ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_wife[3]     = uc_wife[3]     + c.beta0 * w_emax[t+1, wife.schooling, husband.schooling, w_exp_index, h_exp_index_f ,kids_temp_preg, wife.health, husband.health, w_home_time_index_preg, h_home_time_index_preg, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_husband[3]  = uc_husband[3]  + c.beta0 * h_emax[t+1, wife.schooling, husband.schooling, w_exp_index, h_exp_index_f ,kids_temp_preg, wife.health, husband.health, w_home_time_index_preg, h_home_time_index_preg, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
        else:
            u_wife[2] = float('-inf')
            u_wife[3] = float('-inf')
            u_husband[2] = float('-inf')
            u_husband[3] = float('-inf')
        if wage_h_full > 0:
            u_wife[4]     = uc_wife[4]     + c.beta0 * w_emax[t+1, wife.schooling, husband.schooling, w_exp_index, h_exp_index_p ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_husband[4]  = uc_husband[4]  + c.beta0 * h_emax[t+1, wife.schooling, husband.schooling, w_exp_index, h_exp_index_p ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_wife[5]     = uc_wife[5]     + c.beta0 * w_emax[t+1, wife.schooling, husband.schooling, w_exp_index, h_exp_index_p ,kids_temp_preg, wife.health, husband.health, w_home_time_index_preg, h_home_time_index_preg, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_husband[5]  = uc_husband[5]  + c.beta0 * h_emax[t+1, wife.schooling, husband.schooling, w_exp_index, h_exp_index_p ,kids_temp_preg, wife.health, husband.health, w_home_time_index_preg, h_home_time_index_preg, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
        else:
            u_wife[4] = float('-inf')
            u_wife[5] = float('-inf')
            u_husband[4] = float('-inf')
            u_husband[5] = float('-inf')
        if wage_w_full > 0:
            u_wife[6]     = uc_wife[6]     + c.beta0 * w_emax[t+1, wife.schooling, husband.schooling, w_exp_index_f, h_exp_index ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_husband[6]  = uc_husband[6]  + c.beta0 * h_emax[t+1, wife.schooling, husband.schooling, w_exp_index_f, h_exp_index ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_wife[7]     = uc_wife[7]     + c.beta0 * w_emax[t+1, wife.schooling, husband.schooling, w_exp_index_f, h_exp_index ,kids_temp_preg, wife.health, husband.health, w_home_time_index_preg, h_home_time_index_preg, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_husband[7]  = uc_husband[7]  + c.beta0 * h_emax[t+1, wife.schooling, husband.schooling, w_exp_index_f, h_exp_index ,kids_temp_preg, wife.health, husband.health, w_home_time_index_preg, h_home_time_index_preg, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
        else:
            u_wife[6] = float('-inf')
            u_wife[7] = float('-inf')
            u_husband[7] = float('-inf')
            u_husband[7] = float('-inf')
        if wage_h_full > 0 and wage_w_full > 0:
            u_wife[8]     = uc_wife[8]     + c.beta0 * w_emax[t+1, wife.schooling, husband.schooling, w_exp_index_f, h_exp_index_f ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_husband[8]  = uc_husband[8]  + c.beta0 * h_emax[t+1, wife.schooling, husband.schooling, w_exp_index_f, h_exp_index_f ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_wife[9]    = uc_wife[9]    + c.beta0 * w_emax[t+1, wife.schooling, husband.schooling, w_exp_index_f, h_exp_index_f ,kids_temp_preg, wife.health, husband.health, w_home_time_index_preg, h_home_time_index_preg, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_husband[9] = uc_husband[9] + c.beta0 * h_emax[t+1, wife.schooling, husband.schooling, w_exp_index_f, h_exp_index_f ,kids_temp_preg, wife.health, husband.health, w_home_time_index_preg, h_home_time_index_preg, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
        else:
            u_wife[8] = float('-inf')
            u_wife[9] = float('-inf')
            u_husband[8] = float('-inf')
            u_husband[9] = float('-inf')
        if wage_h_part > 0 and wage_w_full > 0:
            u_wife[10]    = uc_wife[10]    + c.beta0 * w_emax[t+1, wife.schooling, husband.schooling, w_exp_index_f, h_exp_index_p ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_husband[10] = uc_husband[10] + c.beta0 * h_emax[t+1, wife.schooling, husband.schooling, w_exp_index_f, h_exp_index_p ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_wife[11]    = uc_wife[11]    + c.beta0 * w_emax[t+1, wife.schooling, husband.schooling, w_exp_index_f, h_exp_index_p ,kids_temp_preg, wife.health, husband.health, w_home_time_index_preg, h_home_time_index_preg, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_husband[11] = uc_husband[11] + c.beta0 * h_emax[t+1, wife.schooling, husband.schooling, w_exp_index_f, h_exp_index_p ,kids_temp_preg, wife.health, husband.health, w_home_time_index_preg, h_home_time_index_preg, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
        else:
            u_wife[10] = float('-inf')
            u_wife[11] = float('-inf')
            u_husband[10] = float('-inf')
            u_husband[11] = float('-inf')
        if wage_w_part > 0:
            u_wife[12]    = uc_wife[12]    + c.beta0 * w_emax[t+1, wife.schooling, husband.schooling, w_exp_index_f, h_exp_index ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_husband[12] = uc_husband[12] + c.beta0 * h_emax[t+1, wife.schooling, husband.schooling, w_exp_index_f, h_exp_index ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_wife[13]    = uc_wife[13]    + c.beta0 * w_emax[t+1, wife.schooling, husband.schooling, w_exp_index_f, h_exp_index ,kids_temp_preg, wife.health, husband.health, w_home_time_index_preg, h_home_time_index_preg, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_husband[13] = uc_husband[13] + c.beta0 * h_emax[t+1, wife.schooling, husband.schooling, w_exp_index_f, h_exp_index ,kids_temp_preg, wife.health, husband.health, w_home_time_index_preg, h_home_time_index_preg, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
        else:
            u_wife[12] = float('-inf')
            u_wife[13] = float('-inf')
            u_husband[12] = float('-inf')
            u_husband[13] = float('-inf')
        if wage_h_full > 0 and wage_w_part > 0:
            u_wife[14]    = uc_wife[14]    + c.beta0 * w_emax[t+1, wife.schooling, husband.schooling, w_exp_index_p, h_exp_index_f ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_husband[14] = uc_husband[14] + c.beta0 * h_emax[t+1, wife.schooling, husband.schooling, w_exp_index_p, h_exp_index_f ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_wife[15]    = uc_wife[15]    + c.beta0 * w_emax[t+1, wife.schooling, husband.schooling, w_exp_index_p, h_exp_index_f ,kids_temp_preg, wife.health, husband.health, w_home_time_index_preg, h_home_time_index_preg, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_husband[15] = uc_husband[15] + c.beta0 * h_emax[t+1, wife.schooling, husband.schooling, w_exp_index_p, h_exp_index_f ,kids_temp_preg, wife.health, husband.health, w_home_time_index_preg, h_home_time_index_preg, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
        else:
            u_wife[14] = float('-inf')
            u_wife[15] = float('-inf')
            u_husband[14] = float('-inf')
            u_husband[15] = float('-inf')
        if wage_h_part > 0 and wage_w_part > 0:
            u_wife[16]    = uc_wife[16]    + c.beta0 * w_emax[t+1, wife.schooling, husband.schooling, w_exp_index_p, h_exp_index_p ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_husband[16] = uc_husband[16] + c.beta0 * h_emax[t+1, wife.schooling, husband.schooling, w_exp_index_p, h_exp_index_p ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_wife[17]    = uc_wife[17]    + c.beta0 * w_emax[t+1, wife.schooling, husband.schooling, w_exp_index_p, h_exp_index_p ,kids_temp_preg, wife.health, husband.health, w_home_time_index_preg, h_home_time_index_preg, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            u_husband[17] = uc_husband[17] + c.beta0 * h_emax[t+1, wife.schooling, husband.schooling, w_exp_index_p, h_exp_index_p ,kids_temp_preg, wife.health, husband.health, w_home_time_index_preg, h_home_time_index_preg, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            temp = h_emax[t+1, wife.schooling, husband.schooling, w_exp_index_p, h_exp_index_p ,kids_temp_preg, wife.health, husband.health, w_home_time_index_preg, h_home_time_index_preg, wife_ability_index, husband_ability_index, wife_mother_educ_index, husband_mother_educ_index, wife_mother_marital_index ,husband_mother_marital_index]
            #print(temp)
            #print("total utility")
            #print(np.asarray(u_wife))
            #print("current utility")
            #print(np.asarray(uc_wife))
        else:
            u_wife[16] = float('-inf')
            u_wife[17] = float('-inf')
            u_husband[16] = float('-inf')
            u_husband[17] = float('-inf')
    # return the utility arrays of husband and wife + utility from home time for the AR process
    #print("total utility")
    #print(np.asarray(u_wife))
    #print("current utility")
    #print(np.asarray(uc_wife))
    return u_husband,  u_wife, home_time_h, home_time_w, home_time_h_preg, home_time_w_preg
