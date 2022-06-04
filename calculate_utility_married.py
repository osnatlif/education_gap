#from libc.math import pow
import numpy as np
import parameters1 as p
from value_to_index import exp_to_index
from gross_to_net import gross_to_net
import constant_parameters as c
from draw_husband import Husband
from draw_wife import Wife

def calculate_utility(w_emax, h_emax, wage_h_part, wage_h_full, wage_w_part, wage_w_full, wife, husband, t):
    #####################################################################################################
   # net income - first observation for taxes is 1950. so age 17 of the 1960 cohort - will be line 27
    if c.cohort == 1960:
        year_row = 27 + t
    elif c.cohort == 1970:
        year_row = 37 + t
    elif c.cohort == 1980:
        year_row = 47 + t
    elif c.cohort==1990:
        year_row = 57 + t
    else:
        assert()
    # in variables' names: first index wife, second husband
    kids_temp = wife.kids + husband.kids   # if married, HN=0, KIDS AT WIFE! if consider geting married, # of kids is WN+HN
    net_income_married_Wue_Hue  = c.UB_W + c.UB_H
    net_income_married_Wue_Hef  = c.UB_W + gross_to_net(kids_temp,   0   , wage_h_full, t)
    net_income_married_Wue_Hep  = c.UB_W + gross_to_net(kids_temp,   0   , wage_h_part, t)
    ###############
    net_income_married_Wef_Hue  = c.UB_H + gross_to_net(kids_temp,wage_w_full ,  0         , t)
    net_income_married_Wef_Hef  =          gross_to_net(kids_temp,wage_w_full ,wage_h_full , t)
    net_income_married_Wef_Hep  =          gross_to_net(kids_temp,wage_w_full ,wage_h_part , t)
    ###################
    net_income_married_Wep_Hue = c.UB_H + gross_to_net(kids_temp, wage_w_part,    0       , t)
    net_income_married_Wep_Hef =          gross_to_net(kids_temp, wage_w_part, wage_h_full, t)
    net_income_married_Wep_Hep =          gross_to_net(kids_temp, wage_w_part, wage_h_part, t)
    # budget constraint
    if kids_temp == 0:
       eta = 0
    elif kids_temp == 1:
       eta = c.eta1            #this is the fraction of parent's income that one child gets
    elif kids_temp == 2:
       eta = c.eta2
    elif kids_temp == 3:
       eta = c.eta3
    else:
       assert(0)

    # first index wife, second husband
    budget_c_married_Wue_Hue  = (1-eta)*(net_income_married_Wue_Hue)
    budget_c_married_Wue_Hef  = (1-eta)*(net_income_married_Wue_Hef)
    budget_c_married_Wue_Hep  = (1-eta)*(net_income_married_Wue_Hep)
    ############
    budget_c_married_Wef_Hue  = (1-eta)*(net_income_married_Wef_Hue)
    budget_c_married_Wef_Hef  = (1-eta)*(net_income_married_Wef_Hef)
    budget_c_married_Wef_Hep  = (1-eta)*(net_income_married_Wef_Hep)
    ###########
    budget_c_married_Wep_Hue  = (1-eta)*(net_income_married_Wep_Hue)
    budget_c_married_Wep_Hef  = (1-eta)*(net_income_married_Wep_Hef)
    budget_c_married_Wep_Hep  = (1-eta)*(net_income_married_Wep_Hep)

    # I assume that each kid get 20% (eta1). if the family has 2 kids, each gets 20%, yet the total is 32% (eta2) since part is common
    if kids_temp > 0:
        # first index wife, second husband
        kids_utility_married_ue_ue = pow((p.row1_w*pow((1.0-c.home_p),p.row0)  + p.row1_h*pow((1.0-c.home_p),p.row0)     + p.row2*pow((c.eta1*net_income_married_Wue_Hue),p.row0)+(1-p.row1_w-p.row1_h-p.row2)*pow((kids_temp),p.row0)),(1.0/p.row0))
        kids_utility_married_ue_ef = pow((p.row1_w*pow((1.0-c.home_p),p.row0)  +                                       p.row2*pow((c.eta1*net_income_married_Wue_Hef),p.row0)+(1-p.row1_w-p.row1_h-p.row2)*pow((kids_temp),p.row0)),(1.0/p.row0))
        kids_utility_married_ue_ep = pow((p.row1_w*pow((1.0-c.home_p),p.row0)  + p.row1_h*pow((1.0-0.5-c.home_p),p.row0) + p.row2*pow((c.eta1*net_income_married_Wue_Hep),p.row0)+(1-p.row1_w-p.row1_h-p.row2)*pow((kids_temp),p.row0)),(1.0/p.row0))
        #########################
        kids_utility_married_ef_ue = pow((                                  p.row1_h*pow((1.0-c.home_p),p.row0)      + p.row2*pow((c.eta1*net_income_married_Wef_Hue),p.row0)+(1-p.row1_w-p.row1_h-p.row2)*pow((kids_temp),p.row0)),(1.0/p.row0))
        kids_utility_married_ef_ef = pow((                                                                       + p.row2*pow((c.eta1*net_income_married_Wep_Hue),p.row0)+(1-p.row1_w-p.row1_h-p.row2)*pow((kids_temp),p.row0)),(1.0/p.row0))
        kids_utility_married_ef_ep = pow((                                  p.row1_h*pow((1.0-0.5-c.home_p),p.row0)  + p.row2*pow((c.eta1*net_income_married_Wef_Hef),p.row0)+(1-p.row1_w-p.row1_h-p.row2)*pow((kids_temp),p.row0)),(1.0/p.row0))
        #####################
        kids_utility_married_ep_ue = pow((p.row1_w*pow((1.0-0.5-c.home_p),p.row0) + p.row1_h*pow((1.0-c.home_p),p.row0)    + p.row2*pow((c.eta1*net_income_married_Wue_Hue),p.row0)+(1-p.row1_w-p.row1_h-p.row2)*pow((kids_temp),p.row0)),(1.0/p.row0))
        kids_utility_married_ep_ep = pow((p.row1_w*pow((1.0-0.5-c.home_p),p.row0) +                                    + p.row2*pow((c.eta1*net_income_married_Wue_Hue),p.row0)+(1-p.row1_w-p.row1_h-p.row2)*pow((kids_temp),p.row0)),(1.0/p.row0))
        kids_utility_married_ep_ef = pow((p.row1_w*pow((1.0-0.5-c.home_p),p.row0) + p.row1_h*pow((1.0-0.5-c.home_p),p.row0)+ p.row2*pow((c.eta1*net_income_married_Wue_Hue),p.row0)+(1-p.row1_w-p.row1_h-p.row2)*pow((kids_temp),p.row0)),(1.0/p.row0))
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
    preg_utility = p.preg_health * wife.health + p.preg_kids * kids_temp + p.preg_t_minus1 * wife.preg + np.random.normal(0, 1) * p.sigma_p
    # home time equation - random walk - tau0_w -pregnancy in previous period, tau1_w - drift term - should be negative
    # if husband is not married his home time is not influence by a newborn, the wife is influenced of course, so home time for her is not function of M
    home_time_h = np.exp(p.tau1_h * np.log(husband.home_time_ar) + p.tau0_h + p.tau2_h * wife.preg + np.random.normal(0, 1) * p.sigma_hp_h)
    home_time_w = np.exp(p.tau1_h * np.log(wife.home_time_ar)    + p.tau0_w + p.tau2_h * wife.preg + np.random.normal(0, 1) * p.sigma_hp_w)
    # home_time_h_m =(home_time_h_m_minus_1.^ tau1_h ) * exp(tau0_h+ tau2_h * P_minus_1 + epsilon_f(draw_f, t, 4) * sigma(4, 4));
    # home_time_h_um=(home_time_h_um_minus_1.^ tau1_h) * exp(tau0_h+                    epsilon_f(draw_f, t, 4) * sigma(4, 4));
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # DRAW AND CALCULATE MARRIAGE AND PREGNENCY TRANSITORY UTILITY #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    if wife.schooling == husband. schooling:
        marriage_utility = p.taste_c + p.taste_health * pow((wife.health-husband.health), 2) +                np.random.normal(0, 1) * p.sigma_q # utility from marriage
    elif wife.schooling < husband. schooling:
        marriage_utility = p.taste_c + p.taste_health * pow((wife.health-husband.health), 2) + p.taste_w_up + np.random.normal(0, 1) * p.sigma_q # utility from marriage
    else:
        marriage_utility = p.taste_c + p.taste_health * pow((wife.health-husband.health), 2) + p.taste_w_down + np.random.normal(0, 1) * p.sigma_q # utility from marriage
    marriage_cost_h = p.mc + p.mc_by_parents * husband.mother_marital
    marriage_cost_w = p.mc + p.mc_by_parents * wife.mother_marital
    # marriage options:# first index wife, second husband
    #            1-married + women unemployed  +man unemployed     +non-pregnant
    #   		     2-married + women unemployed  +man unemployed     +pregnant
    #   		     3-married + women unemployed  +man employed full  +non-pregnant
    #   		     4-married + women unemployed  +man employed full  +pregnant
    #   		     5-married + women unemployed  +man employed part  +non-pregnant
    #   		     6-married + women unemployed  +man employed part  +pregnant
    #            1-married + women employed full   +man unemployed     +non-pregnant
    #   		     2-married + women employed full   +man unemployed     +pregnant
    #   		     3-married + women employed full   +man employed full  +non-pregnant
    #   		     4-married + women employed full +man employed full  +pregnant
    #   		     5-married + women employed full +man employed part  +non-pregnant
    #   		     6-married + women employed full +man employed part  +pregnant
    #            1-married + women employed part  +man unemployed     +non-pregnant
    #   		     2-married + women employed part +man unemployed     +pregnant
    #   		     3-married + women employed part +man employed full  +non-pregnant
    #   		     4-married + women employed part +man employed full  +pregnant
    #   		     5-married + women employed part +man employed part  +non-pregnant
    #   		     6-married + women employed part  +man employed part  +pregnant
    # marriage options:# first index wife, second husband
    uc_wife = np.empty(18)
    uc_husband = np.empty(18)
    #!!!!!!update home time if pregnant!!!!!!
    uc_wife[1] = marriage_utility + (1/p.alpha0)*pow((budget_c_married_Wue_Hue),p.alpha0) + marriage_cost_w * (1-wife.married) + \
        ((              p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2)*pow((1),p.alpha2) + p.alpha3_w_m * kids_utility_married_Wue_Hue + home_time_w
    uc_wife[2] = marriage_utility + (1/p.alpha0)*pow((budget_c_married_Wue_Hue),p.alpha0) + marriage_cost_w * (1-wife.married) + \
        ((p.alpha11_w + p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2)*pow((1),p.alpha2) + p.alpha3_w_m * kids_utility_married_Wue_Hue + home_time_w + preg_utility
    uc_husband[1] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wue_Hue), p.alpha0) + marriage_cost_h * (1 - husband.married) + \
        ((             p.alpha12_h * husband.schooling + p.alpha13_h * husband.health) / p.alpha2) * pow((1),p.alpha2) + p.alpha3_h_m * kids_utility_married_Wue_Hue + home_time_h
    uc_husband[2] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wue_Hue), p.alpha0) + marriage_cost_h * (1 - husband.married) + \
        ((             p.alpha12_h * husband.schooling + p.alpha13_h * husband.health) / p.alpha2) * pow((1),p.alpha2) + p.alpha3_h_m * kids_utility_married_Wue_Hue + home_time_h + preg_utility

    if wage_h_full > 0:
        uc_wife[3] = marriage_utility + (1/p.alpha0)*pow((budget_c_married_Wue_Hef),p.alpha0) + marriage_cost_w * (1-wife.married) + \
            ((              p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2)*pow((1),p.alpha2) + p.alpha3_w_m * kids_utility_married_Wue_Hef + home_time_w
        uc_wife[4] = marriage_utility + (1/p.alpha0)*pow((budget_c_married_Wue_Hef),p.alpha0) + marriage_cost_w * (1-wife.married) + \
            ((p.alpha11_w + p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2)*pow((1),p.alpha2) + p.alpha3_w_m * kids_utility_married_Wue_Hef + home_time_w + preg_utility
        uc_husband[3] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wue_Hef), p.alpha0) + marriage_cost_h * (1 - husband.married) + \
            p.alpha3_h_m * kids_utility_married_Wue_Hef
        uc_husband[4] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wue_Hef), p.alpha0) + marriage_cost_h * (1 - husband.married) + \
            p.alpha3_h_m * kids_utility_married_Wue_Hef + preg_utility
    else:
        uc_wife[3] = 0
        uc_wife[4] = 0
        uc_husband[3] = 0
        uc_husband[4] = 0

    if wage_h_part > 0:
        uc_wife[5] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wue_Hep), p.alpha0) + marriage_cost_w * (1-wife.married) + \
            ((              p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2)*pow((1),p.alpha2) + p.alpha3_w_m * kids_utility_married_Wue_Hep + home_time_w
        uc_wife[6] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wue_Hep), p.alpha0) + marriage_cost_w * (1-wife.married)  + \
            ((p.alpha11_w + p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2)*pow((1),p.alpha2) + p.alpha3_w_m * kids_utility_married_Wue_Hep + home_time_w + preg_utility
        uc_husband[5] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wue_Hep), p.alpha0) + marriage_cost_h * (1 - husband.married) + \
                 ((p.alpha12_h * husband.schooling + p.alpha13_h * husband.health) / p.alpha2) * pow((1 - 0.5 - c.home_p),p.alpha2) + p.alpha3_h_m * kids_utility_married_Wue_Hep + home_time_h * (1 - 0.5 - c.home_p)
        uc_husband[6] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wue_Hep), p.alpha0) + marriage_cost_h * (1 - husband.married) + \
                 ((p.alpha11_h + p.alpha12_h * husband.schooling + p.alpha13_h * husband.health) / p.alpha2) * pow((1 - 0.5 - c.home_p),p.alpha2) + p.alpha3_h_m * kids_utility_married_Wue_Hep + home_time_h * (1 - 0.5 - c.home_p) + preg_utility
    else:
        uc_wife[5] = float('-inf')
        uc_wife[6] = float('-inf')
        uc_husband[5] = float('-inf')
        uc_husband[6] = float('-inf')

    if wage_w_full > 0:    #capacity_w=0.5
        uc_wife[7]= marriage_utility + (1/p.alpha0)*pow((budget_c_married_Wef_Hue),p.alpha0)+ p.alpha3_w_m * kids_utility_married_Wef_Hue + marriage_cost_w * (1-wife.married)
        uc_wife[8]= marriage_utility + (1/p.alpha0)*pow((budget_c_married_Wef_Hue),p.alpha0)+ p.alpha3_w_m * kids_utility_married_Wef_Hue + marriage_cost_w * (1-wife.married) + preg_utility
        uc_husband[7] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wef_Hue),p.alpha0) + p.alpha3_h_m * kids_utility_married_Wef_Hue + marriage_cost_h * (1 - husband.married) + \
            ((              p.alpha12_h * husband.schooling + p.alpha13_h * husband.health) / p.alpha2) * pow((1), p.alpha2)  + home_time_h
        uc_husband[8] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wef_Hue),p.alpha0) + p.alpha3_h_m * kids_utility_married_Wef_Hue + marriage_cost_w * (1 - husband.married) + preg_utility + \
            ((              p.alpha12_h * husband.schooling + p.alpha13_h * husband.health) / p.alpha2) * pow((1), p.alpha2) + home_time_h
        if wage_h_full > 0:             # both employed full
            uc_wife[9] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wef_Hef), p.alpha0) +  p.alpha3_w_m * kids_utility_married_Wef_Hef + marriage_cost_w * (1-wife.married)
            uc_wife[10] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wef_Hef), p.alpha0) + p.alpha3_w_m * kids_utility_married_Wef_Hef +  marriage_cost_w * (1-wife.married) +preg_utility
            uc_husband[9] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wef_Hef), p.alpha0) +  p.alpha3_h_m * kids_utility_married_Wef_Hef + marriage_cost_h * (1-husband.married)
            uc_husband[10] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wef_Hef), p.alpha0) + p.alpha3_h_m * kids_utility_married_Wef_Hef +  marriage_cost_h * (1-husband.married) +preg_utility

        else:
            uc_wife[9] = float('-inf')
            uc_wife[10] = float('-inf')
            uc_husband[9] = float('-inf')
            uc_husband[10] = float('-inf')
        if wage_h_part > 0:
            uc_wife[11] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wef_Hep), p.alpha0) + p.alpha3_w_m * kids_utility_married_Wef_Hep + marriage_cost_w * (1-wife.married)
            uc_wife[12] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wef_Hep), p.alpha0) + p.alpha3_w_m * kids_utility_married_Wef_Hep + marriage_cost_w * (1-wife.married) + preg_utility
            uc_husband[11] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wef_Hep), p.alpha0) + p.alpha3_h_m * kids_utility_married_Wef_Hep + marriage_cost_h * (1 - husband.married)
            ((              p.alpha12_h * husband.schooling + p.alpha13_h * husband.health) / p.alpha2) * pow((1 - 0.5 - c.home_p), p.alpha2)  + home_time_h * (1 - 0.5 - c.home_p)
            uc_husband[12] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wef_Hep), p.alpha0) + p.alpha3_h_m * kids_utility_married_Wef_Hep + marriage_cost_h * (1 - husband.married) + preg_utility
            ((              p.alpha12_h * husband.schooling + p.alpha13_h * husband.health) / p.alpha2) * pow((1 - 0.5 - c.home_p), p.alpha2) + home_time_h * (1 - 0.5 - c.home_p) + preg_utility
        else:
            uc_wife[11] = float('-inf')
            uc_wife[12] = float('-inf')
            uc_husband[11] = float('-inf')
            uc_husband[12] = float('-inf')
    else:
        uc_wife[7] = float('-inf')
        uc_wife[8] = float('-inf')
        uc_wife[9] = float('-inf')
        uc_wife[10] = float('-inf')
        uc_wife[11] = float('-inf')
        uc_wife[12] = float('-inf')
        uc_husband[7] = float('-inf')
        uc_husband[8] = float('-inf')
        uc_husband[9] = float('-inf')
        uc_husband[10] = float('-inf')
        uc_husband[11] = float('-inf')
        uc_husband[12] = float('-inf')
##################################################################################################################
    if wage_w_part > 0:  #to avoid division by zero
        uc_wife[13] = marriage_utility + (1/p.alpha0) * pow((budget_c_married_Wep_Hue), p.alpha0) + p.alpha3_w_m * kids_utility_married_Wep_Hue + marriage_cost_w * (1-wife.married) \
            ((p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2) * pow((1-0.5-c.home_p),p.alpha2) + home_time_w*(1-0.5-c.home_p)
        uc_wife[14] = marriage_utility + (1/p.alpha0) * pow((budget_c_married_Wep_Hue), p.alpha0) + p.alpha3_w_m * kids_utility_married_Wep_Hue + marriage_cost_w * (1-wife.married)   \
            ((p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2) * pow((1-0.5-c.home_p),p.alpha2) + home_time_w*(1-0.5-c.home_p) + preg_utility
        uc_husband[13] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wep_Hue), p.alpha0) + p.alpha3_h_m * kids_utility_married_Wep_Hue + marriage_cost_h * (1 - husband.married) \
                          ((p.alpha12_h * husband.schooling + p.alpha13_h * husband.health) / p.alpha2) * pow((1 - c.home_p), p.alpha2) + home_time_h
        uc_husband[14] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wep_Hue),p.alpha0) + p.alpha3_h_m * kids_utility_married_Wep_Hue + marriage_cost_h * (1 - husband.married) \
                          ((p.alpha12_h * husband.schooling + p.alpha13_h * husband.health) / p.alpha2) * pow((1 - c.home_p), p.alpha2) + home_time_h  + preg_utility
        if wage_h_full > 0:
            uc_wife[15] = marriage_utility + (1/p.alpha0) * pow((budget_c_married_Wep_Hef),p.alpha0) + p.alpha3_w_m * kids_utility_married_Wep_Hef + marriage_cost_w * (1-wife.married)    \
                ((p.alpha11_w + p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2)*pow((1-0.5-c.home_p),p.alpha2) + home_time_w*(1-0.5-c.home_p)
            uc_wife[16] = marriage_utility + (1/p.alpha0) * pow((budget_c_married_Wep_Hef),p.alpha0) + p.alpha3_w_m * kids_utility_married_Wep_Hef + marriage_cost_w * (1-wife.married)    \
                ((p.alpha11_w + p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2)*pow((1-0.5-c.home_p),p.alpha2) + home_time_w*(1-0.5-c.home_p) + preg_utility
            uc_husband[15] = marriage_utility + (1/p.alpha0) * pow((budget_c_married_Wep_Hef),p.alpha0) + p.alpha3_h_m * kids_utility_married_Wep_Hef + marriage_cost_h * (1-husband.married)
            uc_husband[16] = marriage_utility + (1/p.alpha0) * pow((budget_c_married_Wep_Hef),p.alpha0) + p.alpha3_h_m * kids_utility_married_Wep_Hef + marriage_cost_h * (1-husband.married) + preg_utility
        else:
            uc_wife[15] = float('-inf')
            uc_wife[16] = float('-inf')
            uc_husband[15] = float('-inf')
            uc_husband[16] = float('-inf')
        if wage_h_part > 0:
            uc_wife[17] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wep_Hep), p.alpha0) + p.alpha3_w_m * kids_utility_married_Wep_Hep + marriage_cost_w * (1-wife.married)  \
                ((               p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2)*pow((1 - 0.5 - c.home_p),p.alpha2) + home_time_w*(1 - 0.5 - c.home_p)
            uc_wife[18] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wep_Hep), p.alpha0) + p.alpha3_w_m * kids_utility_married_Wep_Hep + marriage_cost_w * (1-wife.married)   \
                ((p.alpha11_w + p.alpha12_w * wife.schooling + p.alpha13_w * wife.health)/p.alpha2)*pow((1 - 0.5 - c.home_p),p.alpha2) + home_time_w*(1 - 0.5 - c.home_p) + preg_utility
            uc_husband[17] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wep_Hep), p.alpha0) + p.alpha3_h_m * kids_utility_married_Wep_Hep + marriage_cost_h * (1-husband.married)  \
                ((              p.alpha12_h * husband.schooling + p.alpha13_h * husband.health)/p.alpha2)*pow((1 - 0.5 - c.home_p),p.alpha2) + home_time_h*(1 - 0.5 - c.home_p)
            uc_husband[18] = marriage_utility + (1 / p.alpha0) * pow((budget_c_married_Wep_Hep), p.alpha0) + p.alpha3_h_m * kids_utility_married_Wep_Hep + marriage_cost_h * (1-husband.married)   \
                ((              p.alpha12_h * husband.schooling + p.alpha13_h * husband.health)/p.alpha2)*pow((1 - 0.5 - c.home_p),p.alpha2) + home_time_h*(1 - 0.5 - c.home_p) + preg_utility
        else:
            uc_wife[17] = float('-inf')
            uc_wife[18] = float('-inf')
            uc_husband[17] = float('-inf')
            uc_husband[18] = float('-inf')
    else:
        uc_wife[13] = float('-inf')
        uc_wife[14] = float('-inf')
        uc_wife[15] = float('-inf')
        uc_wife[16] = float('-inf')
        uc_wife[17] = float('-inf')
        uc_wife[18] = float('-inf')
        uc_husband[13] = float('-inf')
        uc_husband[14] = float('-inf')
        uc_husband[15] = float('-inf')
        uc_husband[16] = float('-inf')
        uc_husband[17] = float('-inf')
        uc_husband[18] = float('-inf')
    ##################################################################################################
    ##################################################################################################
    ########               add emax or terminal value                                         ########
    ##################################################################################################
    ##################################################################################################
    u_wife = np.empty(18)
    u_husband = np.empty(18)
    if t == c.max_period:
        u_wife[1] = uc_wife[1] + p.t1_w*wife.hsg + p.t2_w*wife.sc + p.t3_w*wife.cg + p.t4_w*wife.pc + p.t5_w*wife.exp + p.t6_w*husband.hsg + p.t7_w*husband.sc + p.t8_w*husband.cg + p.t9_w*husband.pc + p.t10_w*husband.exp + p.t11_w * marriage_utility
        u_wife[2] = float('-inf')
        u_husband[1] = uc_husband[1] + p.t1_h * wife.hsg + p.t2_h * wife.sc + p.t3_h * wife.cg + p.t4_h * wife.pc + p.t5_h * wife.exp + p.t6_h * husband.hsg + p.t7_h * husband.sc + p.t8_h * husband.cg + p.t9_h * husband.pc + p.t10_h * husband.exp + p.t11_h * marriage_utility
        u_husband[2] = float('-inf')
        if wage_h_full > 0:
            u_wife[3] =    uc_wife[3]    + p.t1_w * wife.hsg + p.t2_w * wife.sc + p.t3_w * wife.cg + p.t4_w * wife.pc + p.t5_w * wife.exp + p.t6_w * husband.hsg + p.t7_w * husband.sc + p.t8_w * husband.cg + p.t9_w * husband.pc + p.t10_w * husband.exp + p.t11_w * marriage_utility
            u_husband[3] = uc_husband[3] + p.t1_h * wife.hsg + p.t2_h * wife.sc + p.t3_h * wife.cg + p.t4_h * wife.pc + p.t5_h * wife.exp + p.t6_h * husband.hsg + p.t7_h * husband.sc + p.t8_h * husband.cg + p.t9_h * husband.pc + p.t10_h * husband.exp + p.t11_h * marriage_utility
        else:
            u_wife[3] = float('-inf')
            u_husband[3] = float('-inf')
        u_wife[4]= float('-inf')
        u_husband[4]= float('-inf')
        if wage_h_part > 0:
            u_wife[5] =       uc_wife[5] + p.t1_w * wife.hsg + p.t2_w * wife.sc + p.t3_w * wife.cg + p.t4_w * wife.pc + p.t5_w * wife.exp + p.t6_w * husband.hsg + p.t7_w * husband.sc + p.t8_w * husband.cg + p.t9_w * husband.pc + p.t10_w * husband.exp + p.t11_w * marriage_utility
            u_husband[5] = uc_husband[5] + p.t1_h * wife.hsg + p.t2_h * wife.sc + p.t3_h * wife.cg + p.t4_h * wife.pc + p.t5_h * wife.exp + p.t6_h * husband.hsg + p.t7_h * husband.sc + p.t8_h * husband.cg + p.t9_h * husband.pc + p.t10_h * husband.exp + p.t11_h * marriage_utility

        else:
            u_wife[5] = float('-inf')
            u_husband[5] = float('-inf')
        u_wife[6]= float('-inf')
        u_husband[6] = float('-inf')
        if wage_w_full > 0:
            u_wife[7] = uc_wife[7] + p.t1_w * wife.hsg + p.t2_w * wife.sc + p.t3_w * wife.cg + p.t4_w * wife.pc + p.t5_w * wife.exp + p.t6_w * husband.hsg + p.t7_w * husband.sc + p.t8_w * husband.cg + p.t9_w * husband.pc + p.t10_w * husband.exp + p.t11_w * marriage_utility
            u_husband[7] = uc_husband[7] + p.t1_h * wife.hsg + p.t2_h * wife.sc + p.t3_h * wife.cg + p.t4_h * wife.pc + p.t5_h * wife.exp + p.t6_h * husband.hsg + p.t7_h * husband.sc + p.t8_h * husband.cg + p.t9_h * husband.pc + p.t10_h * husband.exp + p.t11_h * marriage_utility
        else:
            u_wife[7] = float('-inf')
            u_husband[7] = float('-inf')
        u_wife[8] = float('-inf')
        u_husband[8] = float('-inf')
        if wage_h_full > 0 & wage_w_full > 0:
            u_wife[9] = uc_wife[9] + p.t1_w * wife.hsg + p.t2_w * wife.sc + p.t3_w * wife.cg + p.t4_w * wife.pc + p.t5_w * wife.exp + p.t6_w * husband.hsg + p.t7_w * husband.sc + p.t8_w * husband.cg + p.t9_w * husband.pc + p.t10_w * husband.exp + p.t11_w * marriage_utility
            u_husband[9] = uc_husband[9] + p.t1_h * wife.hsg + p.t2_h * wife.sc + p.t3_h * wife.cg + p.t4_h * wife.pc + p.t5_h * wife.exp + p.t6_h * husband.hsg + p.t7_h * husband.sc + p.t8_h * husband.cg + p.t9_h * husband.pc + p.t10_h * husband.exp + p.t11_h * marriage_utility
        else:
            u_wife[9] = float('-inf')
            u_husband[9] = float('-inf') 
        u_wife[10]= float('-inf')
        u_husband[10]= float('-inf')
        if wage_h_part > 0 & wage_w_full > 0:
            u_wife[11] = uc_wife[11] + p.t1_w * wife.hsg + p.t2_w * wife.sc + p.t3_w * wife.cg + p.t4_w * wife.pc + p.t5_w * wife.exp + p.t6_w * husband.hsg + p.t7_w * husband.sc + p.t8_w * husband.cg + p.t9_w * husband.pc + p.t10_w * husband.exp + p.t11_w * marriage_utility
            u_husband[11] = uc_husband[11] + p.t1_h * wife.hsg + p.t2_h * wife.sc + p.t3_h * wife.cg + p.t4_h * wife.pc + p.t5_h * wife.exp + p.t6_h * husband.hsg + p.t7_h * husband.sc + p.t8_h * husband.cg + p.t9_h * husband.pc + p.t10_h * husband.exp + p.t11_h * marriage_utility
        else:
            u_wife[11] = float('-inf')
            u_husband[11] = float('-inf') 
        u_wife[12]= float('-inf')
        u_husband[12] = float('-inf')
        if wage_w_part > 0:
            u_wife[13] = uc_wife[13] + p.t1_w * wife.hsg + p.t2_w * wife.sc + p.t3_w * wife.cg + p.t4_w * wife.pc + p.t5_w * wife.exp + p.t6_w * husband.hsg + p.t7_w * husband.sc + p.t8_w * husband.cg + p.t9_w * husband.pc + p.t10_w * husband.exp + p.t11_w * marriage_utility
            u_husband[13] = uc_husband[13] + p.t1_h * wife.hsg + p.t2_h * wife.sc + p.t3_h * wife.cg + p.t4_h * wife.pc + p.t5_h * wife.exp + p.t6_h * husband.hsg + p.t7_h * husband.sc + p.t8_h * husband.cg + p.t9_h * husband.pc + p.t10_h * husband.exp + p.t11_h * marriage_utility
        else:
            u_wife[13] = float('-inf')
            u_husband[13] = float('-inf')
        u_wife[14]= float('-inf')
        u_husband[14] = float('-inf')
        if wage_h_full > 0 & wage_w_part > 0:
            u_wife[15] = uc_wife[15] + p.t1_w * wife.hsg + p.t2_w * wife.sc + p.t3_w * wife.cg + p.t4_w * wife.pc + p.t5_w * wife.exp + p.t6_w * husband.hsg + p.t7_w * husband.sc + p.t8_w * husband.cg + p.t9_w * husband.pc + p.t10_w * husband.exp + p.t11_w * marriage_utility
            u_husband[15] = uc_husband[15] + p.t1_h * wife.hsg + p.t2_h * wife.sc + p.t3_h * wife.cg + p.t4_h * wife.pc + p.t5_h * wife.exp + p.t6_h * husband.hsg + p.t7_h * husband.sc + p.t8_h * husband.cg + p.t9_h * husband.pc + p.t10_h * husband.exp + p.t11_h * marriage_utility
        else:
            u_wife[15] = float('-inf')
            u_husband = float('-inf')          
        u_wife[16]= float('-inf')
        u_husband[16] = float('-inf')
        if wage_h_part > 0 & wage_w_part > 0:
            u_wife[17] = uc_wife[17] + p.t1_w * wife.hsg + p.t2_w * wife.sc + p.t3_w * wife.cg + p.t4_w * wife.pc + p.t5_w * wife.exp + p.t6_w * husband.hsg + p.t7_w * husband.sc + p.t8_w * husband.cg + p.t9_w * husband.pc + p.t10_w * husband.exp + p.t11_w * marriage_utility
            u_husband[17] = uc_husband[17] + p.t1_h * wife.hsg + p.t2_h * wife.sc + p.t3_h * wife.cg + p.t4_h * wife.pc + p.t5_h * wife.exp + p.t6_h * husband.hsg + p.t7_h * husband.sc + p.t8_h * husband.cg + p.t9_h * husband.pc + p.t10_h * husband.exp + p.t11_h * marriage_utility
        else:
            u_wife[17] = float('-inf')
            u_husband[17] = float('-inf')
        u_wife[18] = float('-inf')
        u_husband[18] = float('-inf')
    elif t < c.max_period:
        # t is not the terminal period so add EMAX
        # t - time 17-65
        # HS,wife.schooling - schooling - 5 levels grid
        # HK, WK - experience - 5 level grid
        # C_N, H_N , W_N - number of kids - 4 level grid
        # H_HEALTH,wife.health - health - 3 level drid
        # H_L, W_L - taste for leisure - 3 level grid
        # ability_h_index,ability_w_index - 3 level grid
        # prev_state_h,prev_state_w - work at t-1 - 3 level grid
        # PE_H, PE_W - parents education - 2 levels grid
        # p_minus_1 - pregnancy at t-1, always zero for single men
        # EMAX_M_UM(t,HS,HK,C_N,H_HEALTH,H_L,ability_h_index,prev_state_h,PE_H, p_minus_1)
        # EMAX_W_UM(t,wife.schooling,WK,C_N,wife.health,W_L,ability_w_index,prev_state_w,PE_W, p_minus_1)
        # EMAX_M_M(t,wife.schooling,WK,C_N,wife.health,W_L,ability_w_index,prev_state_w,PE_W, p_minus_1, HS,HK,H_HEALTH,H_L,ability_h_index,prev_state_h,PE_H,marriage_utility)
        # emaw_w_m(t,wife.schooling,WK,C_N,wife.health,W_L,ability_w_index,prev_state_w,PE_W, p_minus_1, HS,HK,H_HEALTH,H_L,ability_h_index,prev_state_h,PE_H,marriage_utility)
        # need to take care of experience and number of kids when calling the EMAX:
        # if women is pregnant, add 1 to the number of kids unless the number is already 4
        #######################################
        # add EMAX to men and women's utility
        #######################################
        h_exp_index = exp_to_index(husband.exp)
        h_home_time_index = exp_to_index(home_time_h)
        w_exp_index = exp_to_index(wife.exp)
        w_home_time_index = exp_to_index(home_time_w)
        u_wife[1] = uc_wife[1]   + c.beta0 * w_emax(t, wife.schooling, husband.schooling, wife.exp, husband.exp ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife.ability_i, husband.ability_i, wife.mother_educ, husband.mother_educ, wife.mother_marital ,husband.mother_marital)
        u_wife[2] = uc_wife[2]   + c.beta0 * w_emax(t, wife.schooling, husband.schooling, wife.exp, husband.exp ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife.ability_i, husband.ability_i, wife.mother_educ, husband.mother_educ, wife.mother_marital ,husband.mother_marital)
        u_wife[3] = uc_wife[3]   + c.beta0 * w_emax(t, wife.schooling, husband.schooling, wife.exp, husband.exp ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife.ability_i, husband.ability_i, wife.mother_educ, husband.mother_educ, wife.mother_marital ,husband.mother_marital)
        u_wife[4] = uc_wife[4]   + c.beta0 * w_emax(t, wife.schooling, husband.schooling, wife.exp, husband.exp ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife.ability_i, husband.ability_i, wife.mother_educ, husband.mother_educ, wife.mother_marital ,husband.mother_marital)
        u_wife[5] = uc_wife[5]   + c.beta0 * w_emax(t, wife.schooling, husband.schooling, wife.exp, husband.exp ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife.ability_i, husband.ability_i, wife.mother_educ, husband.mother_educ, wife.mother_marital ,husband.mother_marital)
        u_wife[6] = uc_wife[6]   + c.beta0 * w_emax(t, wife.schooling, husband.schooling, wife.exp, husband.exp ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife.ability_i, husband.ability_i, wife.mother_educ, husband.mother_educ, wife.mother_marital ,husband.mother_marital)
        u_wife[7] = uc_wife[7]   + c.beta0 * w_emax(t, wife.schooling, husband.schooling, wife.exp, husband.exp ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife.ability_i, husband.ability_i, wife.mother_educ, husband.mother_educ, wife.mother_marital ,husband.mother_marital)
        u_wife[8] = uc_wife[8]   + c.beta0 * w_emax(t, wife.schooling, husband.schooling, wife.exp, husband.exp ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife.ability_i, husband.ability_i, wife.mother_educ, husband.mother_educ, wife.mother_marital ,husband.mother_marital)
        u_wife[9] = uc_wife[9]   + c.beta0 * w_emax(t, wife.schooling, husband.schooling, wife.exp, husband.exp ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife.ability_i, husband.ability_i, wife.mother_educ, husband.mother_educ, wife.mother_marital ,husband.mother_marital)
        u_wife[10] = uc_wife[10] + c.beta0 * w_emax(t, wife.schooling, husband.schooling, wife.exp, husband.exp ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife.ability_i, husband.ability_i, wife.mother_educ, husband.mother_educ, wife.mother_marital ,husband.mother_marital)
        u_wife[11] = uc_wife[11] + c.beta0 * w_emax(t, wife.schooling, husband.schooling, wife.exp, husband.exp ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife.ability_i, husband.ability_i, wife.mother_educ, husband.mother_educ, wife.mother_marital ,husband.mother_marital)
        u_wife[12] = uc_wife[12] + c.beta0 * w_emax(t, wife.schooling, husband.schooling, wife.exp, husband.exp ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife.ability_i, husband.ability_i, wife.mother_educ, husband.mother_educ, wife.mother_marital ,husband.mother_marital)
        u_wife[13] = uc_wife[13] + c.beta0 * w_emax(t, wife.schooling, husband.schooling, wife.exp, husband.exp ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife.ability_i, husband.ability_i, wife.mother_educ, husband.mother_educ, wife.mother_marital ,husband.mother_marital)
        u_wife[14] = uc_wife[14] + c.beta0 * w_emax(t, wife.schooling, husband.schooling, wife.exp, husband.exp ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife.ability_i, husband.ability_i, wife.mother_educ, husband.mother_educ, wife.mother_marital ,husband.mother_marital)
        u_wife[15] = uc_wife[15] + c.beta0 * w_emax(t, wife.schooling, husband.schooling, wife.exp, husband.exp ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife.ability_i, husband.ability_i, wife.mother_educ, husband.mother_educ, wife.mother_marital ,husband.mother_marital)
        u_wife[16] = uc_wife[16] + c.beta0 * w_emax(t, wife.schooling, husband.schooling, wife.exp, husband.exp ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife.ability_i, husband.ability_i, wife.mother_educ, husband.mother_educ, wife.mother_marital ,husband.mother_marital)
        u_wife[17] = uc_wife[17] + c.beta0 * w_emax(t, wife.schooling, husband.schooling, wife.exp, husband.exp ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife.ability_i, husband.ability_i, wife.mother_educ, husband.mother_educ, wife.mother_marital ,husband.mother_marital)
        u_wife[18] = uc_wife[18] + c.beta0 * w_emax(t, wife.schooling, husband.schooling, wife.exp, husband.exp ,kids_temp, wife.health, husband.health, w_home_time_index, h_home_time_index, wife.ability_i, husband.ability_i, wife.mother_educ, husband.mother_educ, wife.mother_marital ,husband.mother_marital)

    return u_husband,  u_wife


