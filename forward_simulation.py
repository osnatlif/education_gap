import numpy as np
from parameters import p
import constant_parameters as c
import draw_husband
import draw_wife
import calculate_wage
import calculate_utility_married
import calculate_utility_single_man
import calculate_utility_single_women
from update_wife_husband_objects import update_wife_single
from update_wife_husband_objects import update_married

# from marriage_emp_decision import marriage_emp_decision, wife_emp_decision
from moments import Moments, calculate_moments


def forward_simulation(w_emax, h_emax, w_s_emax, h_s_emax, verbose, display_moments):
  m = Moments()
  # get specific cohort data
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

  for draw_f in range(0, c.DRAW_F):   # start the forward loop
      wife = draw_wife.Wife()           # declare wife structure
      temp = np.random.randint(0, 100)         # draw wife's parents information + relevant child benefit
      if temp < mother[0]:
        wife.mother_educ = 0
        wife.mother_marital = 0
      elif temp < mother[1]:
        wife.mother_educ = 0
        wife.mother_marital = 1
      elif temp < mother[2]:
        wife.mother_educ = 1
        wife.mother_marital = 0
      else:
        wife.mother_educ = 1
        wife.mother_marital = 1
      # update ability by mother education and marital status
      temp_high_ability = p.ab_high1 + p.ab_high2 * wife.mother_educ + p.ab_high3 * wife.mother_marital
      temp_medium_ability = p.ab_medium1 + p.ab_medium2 * wife.mother_educ + p.ab_medium3 * wife.mother_marital
      prob_high_ability = temp_high_ability/(1 + temp_high_ability + temp_medium_ability)
      prob_medium_ability = temp_medium_ability/(1+temp_high_ability + temp_medium_ability)
      temp = np.random.normal()
      if temp < prob_high_ability:
        wife.ability_i = 2
        wife.ability_value = c.normal_vector[2] * p.sigma_ability_w
      elif temp < prob_medium_ability + prob_high_ability:
        wife.ability_i = 1
        wife.ability_value = c.normal_vector[1] * p.sigma_ability_w
      else:
        wife.ability_i = 0
        wife.ability_value = c.normal_vector[0] * p.sigma_ability_w

      # make choices for all periods
      if verbose:
        print("=========")
        print("new women")
        print("=========")
        print(wife)
      choose_partner = 0
      for t in range(0, c.max_period):
        if verbose:
          print("========= ", wife.age, " =========")
        [wage_w_full, wage_w_part] = calculate_wage.calculate_wage_w(wife)
        if verbose:
          print("women's wage full and part")
          print(wage_w_full)
          print(wage_w_part)
        [single_women_value, single_women_index, single_women_ar] = calculate_utility_single_women.calculate_utility_single_women(w_s_emax, wage_w_part, wage_w_full, wife, t)
        if verbose:
          print("utility of single women - value and index")
          print(single_women_value)
          print(single_women_index)
        married_index = -99
        if wife.married == 0:    #  if not married - draw potential husband
          if wife.age < 20:
            prob_meet_potential_partner = np.exp(p.omega_1)/(1.0+np.exp(p.omega_1))
          else:
            temp = p.omega3 + p.omega4_w * wife.age + p.omega5_w * wife.age * wife.age
            prob_meet_potential_partner = np.exp(temp)/(1.0+np.exp(temp))
          if np.random.normal() < prob_meet_potential_partner:
            choose_partner = 1
            husband = draw_husband.draw_husband_forward(wife, mother)
            if verbose:
              print("=========")
              print("new potential husband")
              print("=========")
              print(husband)

        if wife.married == 1 or choose_partner == 1:
          [wage_h_full, wage_h_part] = calculate_wage.calculate_wage_h(husband)
          if verbose:
            print("men's wage full and part")
            print(wage_h_full)
            print(wage_h_part)
          [u_husband, u_wife, home_time_h, home_time_w, home_time_h_preg, home_time_w_preg] = calculate_utility_married.calculate_utility_married(w_emax, h_emax, wage_h_part, wage_h_full, wage_w_part, wage_w_full, wife, husband, t)
          [single_man_value, single_man_index] = calculate_utility_single_man.calculate_utility_single_man(h_s_emax, wage_h_part, wage_h_full, husband, t)
          if verbose:
            print("utility of single men - value and index")
            print(single_man_value)
            print(single_man_index)
            print("utility of married men")
            print(u_husband)
            print("utility of married women")
            print(u_wife)
          weighted_utility = float('-inf')
          for i in range(0,18):
            if u_wife[i] > single_women_value and u_husband[i] > single_man_value:
              if c.bp * u_wife[i] + (1-c.bp) * u_husband[i] > weighted_utility:
                weighted_utility = c.bp * u_wife[i] + (1-c.bp) * u_husband[i]
                married_index = i
          #####################################################################################
          # update objects and moments = married
          #####################################################################################
          if married_index > -99:
            # the function update_married - updates wife and husband objects if they choose to get married
            update_married(husband, wife, married_index, home_time_h, home_time_w, home_time_h_preg, home_time_w_preg)
            # the function update moments - update
            m.assortative_moments[wife.schooling, husband.schooling] += 1
            m.assortative_counter += 1
            m.fertility_moments_married[t, wife.kids] += 1
            if wife.capacity == 0:
              temp = 0
            elif wife.capacity == 0.5:
              temp = 1
            elif wife.capacity == 1:
              temp = 2
            m.emp_moments_wife_married[t, temp] += 1  # 0 - unemployed, 1 - part time, 2 - full time
            if husband.capacity == 0:
              temp = 0
            elif husband.capacity == 0.5:
              temp = 1
            elif husband.capacity == 1:
              temp = 2
            m.emp_moments_husband_married[t, temp] += 1  # 0 - unemployed, 1 - part time, 2 - full time
            if married_index > 5 and married_index < 12:    # wife work full time
              m.wage_moments_wife_married[t] += wage_w_full
              m.wage_counter_wife_married[t] += 1
            if married_index > 11:    # wife work part-time
              m.wage_moments_wife_married[t] += (wage_w_part * 2)
              m.wage_counter_wife_married[t] += 1
            if married_index in c.men_full_index_array:  # husband work full time
              m.wage_moments_husband_married[t] += wage_h_full
              m.wage_counter_husband_married[t] += 1
            if married_index in c.men_part_index_array:  # wife work part time
              m.wage_moments_husband_married[t] += (wage_h_part * 2)
              m.wage_counter_husband_married[t] += 1
        if married_index == -99:  # not getting married
          update_wife_single(wife, single_women_index, single_women_ar)
          m.fertility_moments_single[t, wife.kids] += 1
          if wife.capacity == 0:
            temp = 0
          elif wife.capacity == 0.5:
            temp = 1
          elif wife.capacity == 1:
            temp = 2
          m.emp_moments_wife_single[t, temp] += 1  # 0 - unemployed, 1 - part time, 2 - full time
          if single_women_index == 2 or single_women_index == 3:  # choose full time employment
            m.wage_moments_wife_single[t] += wage_w_full
            m.wage_counter_wife_single[t] += 1
          elif single_women_index == 4 or single_women_index == 5:  # choose part-time employment
            m.wage_moments_wife_single[t] += (wage_w_part * 2)
            m.wage_counter_wife_single[t] += 1
        if wife.age < 31:
          m.school_moments_wife[t, wife.schooling] += 1
        m.marriage_moments[t] += wife.married
        m.divorce_moments[t] += wife.divorce

  estimated_moments = calculate_moments(m, display_moments)
  return 0.0