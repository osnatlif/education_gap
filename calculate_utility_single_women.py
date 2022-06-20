 # from libc.math import pow
import numpy as np
from parameters import p
import value_to_index
import gross_to_net as tax
import constant_parameters as c
from draw_wife import Wife


def calculate_utility_single_women(w_s_emax, wage_w_part, wage_w_full, wife, t):
    # get specific cohort data
    if c.cohort == 1960:
        cb_const = c.cb_const_60
        cb_per_child = c.cb_per_child_60
    elif c.cohort == 1970:
        cb_const = c.cb_const_70
        cb_per_child = c.cb_per_child_70
    elif c.cohort == 1980:
        cb_const = c.cb_const_80
        cb_per_child = c.cb_per_child_80
    elif c.cohort == 1990:
        cb_const = c.cb_const_90
        cb_per_child = c.cb_per_child_90
    else:
        assert ()
    #####################################################################################################
    ###################################################################################################
    #      calculate utility for single women
    ###################################################################################################
    if wife.kids == 0:
        net_income_single_w_ue = c.ub_w  # if single and unemployed with no kids - only unemployment benefit
    else:
        net_income_single_w_ue = c.ub_w + cb_const + cb_per_child*(wife.kids-1)   # unemployment benefit + child benefit (minus 1 since the constant include 1 child
    if wage_w_full > 0:
        net_income_single_w_ef = tax.gross_to_net_single(wife.kids, wage_w_full, t)
    if wage_w_part > 0:
        net_income_single_w_ep = tax.gross_to_net_single(wife.kids, wage_w_part, t)

    if wife.kids == 0:   # calculate values for wife in all cases
        etaw = 0
    elif wife.kids == 1:
        etaw = c.eta1            #this is the fraction of parent's income that one child gets
    elif wife.kids == 2:
        etaw = c.eta2
    elif wife.kids == 3:
        etaw = c.eta3
    else:
        assert()

    budget_c_single_w_ue = (1-etaw)*net_income_single_w_ue
    if wage_w_full > 0:
        budget_c_single_w_ef = (1-etaw)*net_income_single_w_ef
    if wage_w_part > 0:
        budget_c_single_w_ep = (1-etaw)*net_income_single_w_ep
    #  utility from quality and quality of children: #row0 - CES  parameter row1 - women leisure row2 - husband leisure row3 -income
    if wife.kids > 0:
        kids_utility_single_w_ue = np.power((p.row1_w*np.power((1.0-c.home_p),p.row0) +    p.row2*np.power((c.eta1*net_income_single_w_ue),p.row0)+(1.0-p.row1_w-p.row2)*np.power((wife.kids),p.row0)),(1.0/p.row0))
        if wage_w_full > 0:
            kids_utility_single_w_ef = np.power((                                     p.row2*np.power((c.eta1*net_income_single_w_ef),p.row0)+(1.0-p.row1_w-p.row2)*np.power((wife.kids),p.row0)),(1.0/p.row0))
        if wage_w_part > 0:
            kids_utility_single_w_ep = np.power((p.row1_w*np.power((1.0-0.5-c.home_p),p.row0)+ p.row2*np.power((c.eta1*net_income_single_w_ep),p.row0)+(1.0-p.row1_w-p.row2)*np.power((wife.kids),p.row0)),(1.0/p.row0))
    elif wife.kids == 0:
        kids_utility_single_w_ue = 0
        kids_utility_single_w_ef = 0
        kids_utility_single_w_ep = 0
    else:
        assert(0)

    preg_utility_um = p.preg_health * wife.health + p.preg_kids * wife.kids + p.preg_t_minus1 * wife.preg + np.random.normal(0, 1)*p.sigma_p
    school_utility_w = 0
    if wife.schooling == 0:   # if hsd - don't pat tuition
        school_utility_w = p.s1_w + p.s2_w * wife.mother_educ + p.s3_w * wife.ability_value  # utility from high school
    elif wife.schooling > 0:  # if hsg or higher - need to pay tuition
        school_utility_w = p.s1_w + p.s2_w * wife.mother_educ + p.s3_w * wife.ability_value + p.s4_w  # utility rom post high  school
    # Home time equation - random walk: tau0_w - pregnancy in previous period, tau1_w - drift term - should be negative
    home_time_w =      np.exp((p.tau1_w * np.log(wife.home_time_ar)) + p.tau0_w            + np.random.normal(0,1) * p.sigma_hp_w)
    home_time_w_preg = np.exp((p.tau1_w * np.log(wife.home_time_ar)) + p.tau0_w + p.tau2_w + np.random.normal(0,1) * p.sigma_hp_w)
    # home_time_w = exp((home_time_w_minus_1. ^ tau1_w) * exp( tau0_w + tau2_w * P_minus_1 + np.random.normal(0, 1) * sigma(3, 3));
    # decision making - choose from up to 13 options, according to CHOOSE_HUSBAND, CHOOSE_WORK, AGE  values
    # utility from each option:
    # single options:
    #            0-singe + unemployed + non-pregnant
    #		         1-singe + unemployed + pregnant - zero for men
    #            2-singe + employed full  + non-pregnant
    #            3-singe + employed full  + pregnant   - zero for men
    #            4-singe + employed part + non-pregnant
    #            5-singe + employed part + pregnant   - zero for men
    #            6-schooling: single + unemployed + non-pregnant + no children
    # wife current utility from each option:
    divorce_cost_w = p.dc_w + p.dc_w_kids * wife.kids
    u_wife_single = np.empty(7)
    u_wife_single[0] = (1 / p.alpha0) * np.power(budget_c_single_w_ue, p.alpha0) + \
        ((              p.alpha12_w * wife.schooling + p.alpha13_w * wife.health) / p.alpha2) * np.power((1),p.alpha2) + p.alpha3_w_s * kids_utility_single_w_ue + home_time_w + divorce_cost_w * wife.married
    u_wife_single[1] = (1 / p.alpha0) * np.power(budget_c_single_w_ue, p.alpha0) +   \
        ((p.alpha11_w + p.alpha12_w * wife.schooling + p.alpha13_w * wife.health) / p.alpha2) * np.power((1),p.alpha2) + p.alpha3_w_s * kids_utility_single_w_ue + home_time_w_preg + preg_utility_um + divorce_cost_w * wife.married
    if wage_w_full > 0:  # to avoid division by zero
        u_wife_single[2] = (1 / p.alpha0) * np.power(budget_c_single_w_ef, p.alpha0) + \
             p.alpha3_w_s * kids_utility_single_w_ef + divorce_cost_w * wife.married
        u_wife_single[3] = (1 / p.alpha0) * np.power(budget_c_single_w_ef, p.alpha0) + \
             p.alpha3_w_s * kids_utility_single_w_ef + preg_utility_um + divorce_cost_w * wife.married
    else:
        u_wife_single[2] = float('-inf')
        u_wife_single[3] = float('-inf')
    if wage_w_part > 0:  # capacity_w=0.5
        u_wife_single[4] = (1 / p.alpha0) * np.power(budget_c_single_w_ep, p.alpha0) + \
            ((              p.alpha12_w * wife.schooling + p.alpha13_w * wife.health) / p.alpha2) * np.power((1 - 0.5 - c.home_p), p.alpha2) + p.alpha3_w_s * kids_utility_single_w_ep + \
            home_time_w * (1 - 0.5 - c.home_p) + divorce_cost_w * wife.married
        u_wife_single[5] = (1 / p.alpha0) * np.power(budget_c_single_w_ep, p.alpha0) +   \
            ((p.alpha11_w + p.alpha12_w * wife.schooling + p.alpha13_w * wife.health) / p.alpha2) * np.power((1 - 0.5 - c.home_p),p.alpha2) + p.alpha3_w_s * kids_utility_single_w_ep + \
            home_time_w_preg * (1 - 0.5 - c.home_p) + preg_utility_um + divorce_cost_w * wife.married
    else:
        u_wife_single[4] = float('-inf')
        u_wife_single[5] = float('-inf')
    u_wife_single[6] = school_utility_w  # in school-no leisure, no income, but utility from schooling+increase future value
    # calculate expected utility = current utility + emax value if t<T. = current utility + terminal value if t==T
    u_wife = np.empty(7)
    if t == c.max_period:
        u_wife[0]= u_wife_single[0] + p.t1_w*wife.hsg+p.t2_w*wife.sc+p.t3_w*wife.cg+p.t4_w*wife.pc+p.t5_w*wife.exp+p.t13_w*wife.kids
        u_wife[1]= float('-inf') # can't get pregnant at 60
        if wage_w_full > 0:  # to avoid division by zero
            u_wife[2]= u_wife_single[2] + p.t1_w*wife.hsg+p.t2_w*wife.sc+p.t3_w*wife.cg+p.t4_w*wife.pc+p.t5_w*(wife.exp+1)+p.t13_w*wife.kids+p.t16_w #one more year of experience
        else:
            u_wife[2] = float('-inf')
        u_wife[3]= float('-inf') # can't get pregnant at 60
        if wage_w_part > 0:
            u_wife[4]= u_wife_single[4] + p.t1_w*wife.hsg+p.t2_w*wife.sc+p.t3_w*wife.cg+p.t4_w*wife.pc+p.t5_w*(wife.exp+0.5)+p.t13_w*wife.kids+p.t16_w #one more year of experience
        else:
            u_wife[4] = float('-inf')
        u_wife[5] = float('-inf') # can't get pregnant at 60
        u_wife[6] = float('-inf') # can't go to school at 60
    #####################################################################   ADD EMAX    ########################
    # t - time 17-65
    # schooling - 5 levels grid
    # experience - 5 level grid
    # number of children - 4 level grid - 0, 1, 2 , 3+
    # health - 2 level grid
    # home time ar process - 3 level grid
    # ability_index - 3 level grid
    # parents education - 2 levels grid
    # parents marital status - 2 levels
    # EMAX_M_UM(t,wife.schooling, wife_exp_index,wife.kids, wife.health, wife_home_time_index,wife_ability_i, wife.mother_educ, wife.mother_marital)
    # need to take care of experience and number of children when calling the EMAX:
    # if women is pregnant, add 1 to the number of children unless the number is already 4
    elif t < c.max_period:
        wife_exp_index = value_to_index.exp_to_index(wife.exp)
        wife_home_time_index = value_to_index.home_time_to_index(home_time_w)
        wife_home_time_index_preg = value_to_index.home_time_to_index(home_time_w_preg)

        u_wife[0] = u_wife_single[0] + c.beta0 * w_s_emax[t, wife.schooling, wife_exp_index, wife.kids, wife.health, wife_home_time_index, wife.ability_i, wife.mother_educ, wife.mother_marital]
        if wife.age < 40:
            kids_index = min( wife.kids+1, 3)
            u_wife[1] = u_wife_single[1] + c.beta0 * w_s_emax[t,wife.schooling, wife_exp_index, kids_index, wife.health, wife_home_time_index_preg,wife.ability_i, wife.mother_educ, wife.mother_marital]
        else:
            u_wife[1] = float('-inf') # can't get pregnant after 40
        if wage_w_full > 0:
            wife_exp_index = value_to_index.exp_to_index(wife.exp+1)
            u_wife[2] = u_wife_single[2] + c.beta0 * w_s_emax[t,wife.schooling, wife_exp_index,wife.kids, wife.health, wife_home_time_index,wife.ability_i, wife.mother_educ, wife.mother_marital]
        else:
            u_wife[2] = float('-inf')
        if wage_w_full > 0 & wife.age < 40:
            kids_index = min( wife.kids+1, 3)
            u_wife[3] = u_wife_single[3] + c.beta0 * w_s_emax[t,wife.schooling, wife_exp_index,kids_index, wife.health, wife_home_time_index_preg,wife.ability_i, wife.mother_educ, wife.mother_marital]
        else:
            u_wife[3] = float('-inf')
        if wage_w_part > 0:
            wife_exp_index = value_to_index.exp_to_index(wife.exp+0.5)
            u_wife[4] = u_wife_single[4] + c.beta0 * w_s_emax[t,wife.schooling, wife_exp_index,wife.kids, wife.health, wife_home_time_index,wife.ability_i, wife.mother_educ, wife.mother_marital]
        else:
            u_wife[4] = float('-inf')
        if wage_w_part > 0 & wife.age < 40:
            kids_index = min( wife.kids+1, 3)
            u_wife[5] = u_wife_single[5] + c.beta0 * w_s_emax[t,wife.schooling, wife_exp_index, kids_index, wife.health, wife_home_time_index_preg,wife.ability_i, wife.mother_educ, wife.mother_marital]
        else:
            u_wife[5] = float('-inf')
        if wife.age < 31:
            school_index = value_to_index.schooly_to_index(wife.years_of_schooling+1)
            u_wife[6] = u_wife_single[6] + c.beta0 * w_s_emax[t,school_index, wife_exp_index,wife.kids, wife.health, wife_home_time_index,wife.ability_i, wife.mother_educ, wife.mother_marital]
        else:
            u_wife[6] = float('-inf')
    else:
        assert()
    ###################################################################################
    single_value = max(u_wife)
    single_index = np.argmax(u_wife)
    # print("value and index of max")
    # print(single_max_option)
    # print(single_max_option_index)
    # print(u_wife)
    if single_index == 1 or single_index == 3 or single_index == 5:
        ar = home_time_w_preg
    else:
        ar = home_time_w

    return single_value, single_index, ar


