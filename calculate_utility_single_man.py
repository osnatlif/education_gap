#from libc.math import pow
import numpy as np
import parameters as p
from value_to_index import exp_to_index
from value_to_index import schooly_to_index
import gross_to_net as tax
import constant_parameters as c
from draw_husband import Husband

def calculate_utility_single_man(h_s_emax, wage_h_part, wage_h_full, husband, t):
    #####################################################################################################
    # utility for single men - this function is only used in the Emax for single men  - calculate only in backward when "is single" flag is on
    # also used for calculate value of divorce
    ###################################################################################################
    #      calculate utility for single man
    ###################################################################################################
    net_income_single_h_ue = c.ub_h
    net_income_single_h_ef = tax.gross_to_net_single(husband.kids, wage_h_full, t)
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
    budget_c_single_h_ef = (1 - etah) * net_income_single_h_ef
    budget_c_single_h_ep = (1 - etah) * net_income_single_h_ep
    # utility from quality and quality of children: #row0 - CES  parameter row1 - women leisure row2 - husband leisure row3 -income
    if husband.kids > 0:
        kids_utility_single_h_ue = pow((p.row1_h * pow((1.0 - c.home_p), p.row0) + p.row2 * pow((c.eta1 * net_income_single_h_ue), p.row0) +
             (1.0 - p.row1_h - p.row2) * pow((husband.kids), p.row0)),(1.0 / p.row0))
        kids_utility_single_h_ef = pow((                                           p.row2 * pow((c.eta1 * net_income_single_h_ef), p.row0) +
             (1.0 - p.row1_h - p.row2) * pow((husband.kids), p.row0)), (1.0 / p.row0))
        kids_utility_single_h_ep = pow((p.row1_h * pow((1.0 - 0.5 - c.home_p), p.row0) + p.row2 * pow((c.eta1 * net_income_single_h_ep), p.row0) +
             (1.0 - p.row1_h - p.row2) * pow((husband.kids), p.row0)), (1.0 / p.row0))
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
    home_time_h = np.exp((p.tau1_h * np.log(husband.home_time_ar)) + p.tau0_h + np.random.normal(0, 1) * p.sigma_hp_h)
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

    u_husband_single = np.empty(7)
    u_husband_single[1] = float('-inf')    # single husband can't get pregnant
    u_husband_single[3] = float('-inf')    # single husband can't get pregnant
    u_husband_single[5] = float('-inf')    # single husband can't get pregnant
    # husband (potential husband) current utility from each option:
    u_husband_single[0] = (1 / p.alpha0) * pow(budget_c_single_h_ue, p.alpha0) + \
        ((              p.alpha12_h * husband.schooling + p.alpha13_w * husband.health) / p.alpha2) * pow((1),p.alpha2) + p.alpha3_h_s * kids_utility_single_h_ue + home_time_h + divorce_cost_h * husband.married
    if wage_h_full > 0:  # to avoid division by zero
        u_husband_single[2] = (1 / p.alpha0) * pow(budget_c_single_h_ef, p.alpha0) + \
             p.alpha3_h_s * kids_utility_single_h_ef + divorce_cost_h * husband.married
    else:
        u_husband_single[2] = float('-inf')
    if wage_h_part > 0:  # capacity_w=0.5
        u_husband_single[4] = (1 / p.alpha0) * pow(budget_c_single_h_ep, p.alpha0) + \
            ((              p.alpha12_w * husband.schooling + p.alpha13_w * husband.health) / p.alpha2) * pow((1 - 0.5 - c.home_p), p.alpha2) + p.alpha3_h_s * kids_utility_single_h_ep + \
            home_time_h * (1 - 0.5 - c.home_p) + divorce_cost_h * husband.married
    else:
        u_husband_single[4] = float('-inf')
    u_husband_single[6] = school_utility_h  # in school-no leisure, no income, but utility from schooling+increase future value
    # calculate expected utility = current utility + emax value if t<T. = current utility + terminal value if t==T

    u_husband = np.empty(7)
    if t == c.max_period:
        u_husband[0]= u_husband_single[0] + p.t1_w*husband.hsg+p.t2_w*husband.sc+p.t3_w*husband.cg+p.t4_w*husband.pc+p.t5_w*husband.exp+p.t13_w*husband.kids
        u_husband[1]= float('-inf') # can't get pregnant at 60
        if wage_h_full > 0:  # to avoid division by zero
            u_husband[2]= u_husband_single[2] + p.t1_w*husband.hsg+p.t2_w*husband.sc+p.t3_w*husband.cg+p.t4_w*husband.pc+p.t5_w*(husband.exp+1)+p.t13_w*husband.kids+p.t16_w #one more year of experience
        else:
            u_husband[2] = float('-inf')
        u_husband[3]= float('-inf') # can't get pregnant at 60
        if wage_h_part > 0:
            u_husband[4]= u_husband_single[4] + p.t1_w*husband.hsg+p.t2_w*husband.sc+p.t3_w*husband.cg+p.t4_w*husband.pc+p.t5_w*(husband.exp+0.5)+p.t13_w*husband.kids+p.t16_w #one more year of experience
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
    elif t < c.max_period:
        husband_exp_index = exp_to_index(husband.exp)
        husband_home_time_index = exp_to_index(home_time_h)
        u_husband[0] = u_husband_single[0] + c.beta0 * h_s_emax[t,husband.schooling, husband_exp_index,husband.kids, husband.health, husband_home_time_index,husband.ability_i, husband.mother_educ, husband.mother_marital]
        u_husband[1] = float('-inf') # can't get pregnant after 40
        if wage_h_full > 0:
            husband.exp_index = exp_to_index(husband.exp+1)
            u_husband[2] = u_husband_single[2] + c.beta0 * h_s_emax[t,husband.schooling, husband.exp_index,husband.kids, husband.health, husband_home_time_index,husband.ability_i, husband.mother_educ, husband.mother_marital]
        else:
            u_husband[2] = float('-inf')
        u_husband[3] = float('-inf')
        if wage_h_part > 0:
            husband_exp_index = exp_to_index(husband.exp+0.5)
            u_husband[4] = u_husband_single[4] + c.beta0 * h_s_emax[t,husband.schooling, husband_exp_index,husband.kids, husband.health, husband_home_time_index,husband.ability_i, husband.mother_educ, husband.mother_marital]
        else:
            u_husband[4] = float('-inf')
        u_husband[5] = float('-inf')
        if husband.age < 31:
            school_index = schooly_to_index(husband.years_of_schooling+1)
            u_husband[6] = u_husband_single[6] + c.beta0 * h_s_emax[t, school_index, husband_exp_index, husband.kids, husband.health, husband_home_time_index,husband.ability_i, husband.mother_educ, husband.mother_marital]
        else:
            u_husband[6] = float('-inf')
    else:
        assert()
    ###################################################################################
    single_value = max(u_husband)
    single_index = np.argmax(u_husband)
    # print("value and index of max")
    # print(single_max_option)
    # print(single_max_option_index)
    # print(u_wife)
    return single_value, single_index


