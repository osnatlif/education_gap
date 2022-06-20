from parameters import p
import constant_parameters as c
import draw_husband
import draw_wife
import calculate_wage
from calculate_utility_single_women import calculate_utility_single_women
from calculate_utility_married import calculate_utility_married
from calculate_utility_single_man import calculate_utility_single_man


def married_couple_emax(t, w_emax, h_emax, w_s_emax, h_s_emax,  verbose):
    if verbose:
        print("====================== married couple:  ======================")
    wife = draw_wife.Wife()
    husband = draw_husband.Husband()
    iter_count = 0
    wife.age = 17 + t
    husband.age = wife.age
    # [c.max_period, c.school_size, c.school_size, c.exp_size, c.exp_size,c.kids_size, c.health_size, c.health_size,
    # c.home_time_size, c.home_time_size, c.ability_size, c.ability_size, c.mother_size, c.mother_size, c.mother_size,
    # c.mother_size])
    for school_w in range(0, c.school_size):   # loop over school
        wife.schooling = school_w
        draw_wife.update_wife_schooling(wife)
        for school_h in range(0, c.school_size):
            husband.schooling = school_h
            draw_husband.update_school(husband)
            for exp_w in range(0, c.exp_size):           # loop over experience
                wife.exp = c.exp_vector[exp_w]
                for exp_h in range(0, c.exp_size):
                    husband.exp = c.exp_vector[exp_h]
                    for kids in range(0, 4):                # for each number of kids: 0, 1, 2,  - open loop of kids
                        wife.kids = kids
                        for home_time_w in range(0, 3):       # home time loop - three options
                            wife.home_time_ar = c.home_time_vector[home_time_w]
                            for home_time_h in range(0, 3):
                                husband.home_time_ar = c.home_time_vector[home_time_h]
                                for ability_w in range(0, 3):     # for each ability level: low, medium, high - open loop of ability
                                    wife.ability_i = ability_w
                                    wife.ability_value = c.normal_vector[ability_w] * p.sigma_ability_w  # wife ability - low, medium, high
                                    for ability_h in range(0, 3):
                                        husband.ability_i = ability_h
                                        husband.ability_value = c.normal_vector[ability_h] * p.sigma_ability_h  # wife ability - low, medium, high
                                        for mother_educ_w in range(0, 2):
                                            wife.mother_educ = mother_educ_w
                                            for mother_educ_h in range(0, 2):
                                                husband.mother_educ = mother_educ_h
                                                for mother_marital_w in range(0, 2):
                                                    wife.mother_marital = mother_marital_w
                                                    for mother_marital_h in range(0, 2):
                                                        husband.mother_marital = mother_marital_h
                                                        w_sum = 0
                                                        h_sum = 0
                                                        if verbose:
                                                            print(wife)
                                                            print(husband)
                                                        for draw in range(0, c.DRAW_B):
                                                            married_index = -99
                                                            wage_w_full, wage_w_part = calculate_wage.calculate_wage_w(wife)
                                                            wage_h_full, wage_h_part = calculate_wage.calculate_wage_h(husband)
                                                            single_women_value, _, _ = calculate_utility_single_women(w_s_emax, wage_w_part, wage_w_full, wife, t)
                                                            single_man_value, _ = calculate_utility_single_man(h_s_emax, wage_h_part, wage_h_full, husband, t)
                                                            u_husband, u_wife, _, _, _, _ = calculate_utility_married(w_emax, h_emax, wage_h_part, wage_h_full, wage_w_part, wage_w_full, wife, husband, t)
                                                            weighted_utility = float('-inf')
                                                            for i in range(0, 18):
                                                                if u_wife[i] > single_women_value and u_husband[i] > single_man_value:
                                                                    if c.bp * u_wife[i] + (1 - c.bp) * u_husband[i] > weighted_utility:
                                                                        weighted_utility = c.bp * u_wife[i] + (1 - c.bp) * u_husband[i]
                                                                        married_index = i
                                                            if married_index > -99:
                                                                h_sum += u_husband[married_index]
                                                                w_sum += u_wife[married_index]
                                                            else:
                                                                w_sum += single_women_value
                                                                h_sum += single_man_value
                                                            print("====================== new draw ======================")
    # end draw backward loop
    w_emax[t][school_w][school_h][exp_w][exp_h][kids][wife.health][husband.health][home_time_w][home_time_h][ability_w] \
        [ability_h][mother_educ_w][mother_educ_h][mother_marital_w][mother_marital_h] = w_sum / c.DRAW_B
    h_emax[t][school_w][school_h][exp_w][exp_h][kids][wife.health][husband.health][home_time_w][home_time_h][ability_w] \
        [ability_h][mother_educ_w][mother_educ_h][mother_marital_w][mother_marital_h] = h_sum / c.DRAW_B
    if verbose:
        print("emax wife(", t, ", ", school_w, ", ", exp_w,", ", kids, ",", ability_w, ")=", w_sum / c.DRAW_B)
        print("======================================================")
    iter_count = iter_count + 1
    return iter_count
