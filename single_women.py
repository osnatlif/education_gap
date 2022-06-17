import numpy as np
import parameters as p
import constant_parameters as c
import draw_husband
import draw_wife
import calculate_wage
from calculate_utility_single_women import calculate_utility_single_women
from calculate_utility_married import calculate_utility_married
from calculate_utility_single_man import calculate_utility_single_man


def single_women(t, w_emax, h_emax, w_s_emax, h_s_emax,  verbose):
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
    wife = draw_wife.Wife()
    iter_count = 0
    wife.age = 17 + t
    # c.max_period, c.school_size, c.exp_size, c.kids_size, c.health_size, c.home_time_size, c.ability_size, c.mother_size, c.mother_size])
    for school in range(0, c.school_size):   # loop over school
        wife.schooling = school
        draw_wife.update_wife_schooling(wife)
        for exp in range(0, c.exp_size):           # loop over experience
            wife.exp = c.exp_vector[exp]
            for kids in range(0, 4):                # for each number of kids: 0, 1, 2,  - open loop of kids
                wife.kids = kids
                for home_time in range(0, 3):       # home time loop - three options
                    wife.home_time_ar = c.home_time_vector[home_time]
                    for ability in range(0, 3):     # for each ability level: low, medium, high - open loop of ability
                        wife.ability_i = ability
                        wife.ability_value = c.normal_vector[ability] * p.sigma_ability_w  # wife ability - low, medium, high
                        for mother_educ in range(0,2):
                            wife.mother_educ = mother_educ
                            for mother_marital in range(0, 2):
                                wife.mother_marital = mother_marital
                                sum = 0
                                if verbose:
                                   print(wife)
                                for draw in range(0, c.DRAW_B):
                                    married_index = -99
                                    choose_partner = 0
                                    wage_w_full, wage_w_part = calculate_wage.calculate_wage_w(wife)
                                    single_women_value, _, _ = calculate_utility_single_women(w_s_emax, wage_w_part, wage_w_full, wife, t)
                                    if wife.age < 20:
                                        prob_meet_potential_partner = np.exp(p.omega_1) / (1.0 + np.exp(p.omega_1))
                                    else:
                                        temp = p.omega3 + p.omega4_w * wife.age + p.omega5_w * wife.age * wife.age
                                        prob_meet_potential_partner = np.exp(temp) / (1.0 + np.exp(temp))
                                    if np.random.normal() < prob_meet_potential_partner:
                                        choose_partner = 1
                                        husband = draw_husband.draw_husband_forward(wife, mother)
                                    if choose_partner == 1:
                                        wage_h_full, wage_h_part = calculate_wage.calculate_wage_h(husband)
                                        u_husband, u_wife, _, _, _, _ = calculate_utility_married(w_emax, h_emax, wage_h_part, wage_h_full, wage_w_part, wage_w_full, wife, husband, t)
                                        single_man_value, single_man_index = calculate_utility_single_man(h_s_emax, wage_h_part, wage_h_full, husband, t)
                                        weighted_utility = float('-inf')
                                        for i in range(0, 18):
                                            if u_wife[i] > single_women_value and u_husband[i] > single_man_value:
                                                if c.bp * u_wife[i] + (1 - c.bp) * u_husband[i] > weighted_utility:
                                                    weighted_utility = c.bp * u_wife[i] + (1 - c.bp) * u_husband[i]
                                                    married_index = i
                                    if married_index > -99:
                                         sum += u_wife[married_index]
                                    else:
                                        sum += single_women_value
                                    print("====================== new draw ======================")
    # end draw backward loop
    w_s_emax[t][school][exp][kids][wife.health][home_time][ability][mother_educ][mother_marital] = sum / c.DRAW_B
    if verbose:
        print("emax(", t, ", ", school, ", ", exp,", ", kids, ",", ability, ")=", sum / c.DRAW_B)
        print("======================================================")
    iter_count = iter_count + 1
    return iter_count
