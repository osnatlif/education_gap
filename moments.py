import numpy as np
import constant_parameters as c
from tabulate import tabulate


class ActualMoments:
  actual_married_moments = np.loadtxt("married1970white.txt")
  actual_unmarried_moments = np.loadtxt("unmarried1970white.txt")
  actual_marr_divorce_moments = np.loadtxt("marr_divorce1970white.txt")
  actual_school_moments = np.loadtxt("school1970white.txt")
  actual_assortative_moments = np.loadtxt("assortative1970white.txt")


class Moments:
  fertility_moments_single = np.zeros((c.max_period, c.kids_size))
  fertility_moments_married = np.zeros((c.max_period, c.kids_size))
  school_moments_wife = np.zeros((c.max_school, c.school_size))
  emp_moments_wife_single = np.zeros((c.max_period, 3))  # 0 - unemployed, 1 - part time, 2 - full time
  emp_moments_wife_married = np.zeros((c.max_period, 3))  # 0 - unemployed, 1 - part time, 2 - full time
  emp_moments_husband_married = np.zeros((c.max_period, 3))  # 0 - unemployed, 1 - part time, 2 - full time
  wage_moments_wife_single = np.zeros((c.max_period))
  wage_counter_wife_single = np.zeros((c.max_period))
  wage_moments_wife_married = np.zeros((c.max_period))
  wage_counter_wife_married = np.zeros((c.max_period))
  wage_moments_husband_married = np.zeros((c.max_period))
  wage_counter_husband_married = np.zeros((c.max_period))
  marriage_moments = np.zeros((c.max_period))
  divorce_moments = np.zeros((c.max_period))
  assortative_moments = np.zeros((c.school_size, c.school_size))
  assortative_counter = np.zeros(1)


def calculate_moments(m, display_moments):
  # calculate employment moments
  #estimated_married_moments_w = np.zeros((c.max_period, 8))
  #age_arr = np.arange(17, 17+c.max_period).reshape((1, c.max_period))
  #print(age_arr)
  age_arr = np.arange(17, 17+c.max_period)

  estimated_married_moments_w = np.c_[age_arr, (m.fertility_moments_married.T/m.marriage_moments).T,
                                      m.wage_moments_wife_married/m.wage_counter_wife_married,
                                      (m.emp_moments_wife_married.T/m.marriage_moments).T]

  headers = ["Age", "No Kids", "1 Kid", "2 Kids", "3+ Kids", "Wage", "unemployment", "full", "part"]
  table = tabulate(estimated_married_moments_w, headers, floatfmt=".2f", tablefmt="simple")
  print(" married women moments")
  print(table)
  ##################################################################################################
  estimated_single_moments_w = np.c_[age_arr, (m.fertility_moments_single.T /(c.DRAW_F - m.marriage_moments)).T,
                                      m.wage_moments_wife_single / m.wage_counter_wife_single,
                                      (m.emp_moments_wife_single.T / (c.DRAW_F - m.marriage_moments)).T]

  table = tabulate(estimated_single_moments_w, headers, floatfmt=".2f", tablefmt="simple")
  print(" single women moments")
  print(table)
  ##################################################################################################
  age_arr_1970 = np.arange(17, 17+c.max_1970)
  estimated_marr_divorce_moments = np.c_[age_arr_1970, (m.marriage_moments.T[0:36] / c.DRAW_F),
                                         (m.divorce_moments.T[0:36] / c.DRAW_F), ActualMoments.actual_marr_divorce_moments[36:72,3:5]]

  headers = ["Age", "marriage", "divorce", "married", "divorce" ]
  table = tabulate(estimated_marr_divorce_moments, headers, floatfmt=".2f", tablefmt="simple")
  print("           Fitted         ", "            Actual    ")
  print(table)
  ###################################################################################################
  school_age_arr = np.arange(17, 17+c.max_school)
  estimated_school_moments = np.c_[school_age_arr, (m.school_moments_wife / c.DRAW_F), ActualMoments.actual_school_moments[14:29, 3:8] ]

  headers = ["Age", "HSD", "HSG", "SC", "CG", "PC", "HSD", "HSG", "SC", "CG", "PC"]
  print("           Fitted         ", "            Actual    ")
  table = tabulate(estimated_school_moments, headers, floatfmt=".2f", tablefmt="simple")
  print(table)
  ###################################################################################################
  estimated_assortative_moments = np.c_[ (m.assortative_moments / m.assortative_counter), ActualMoments.actual_assortative_moments ]

  print("assortative mating:", "       Fitted         ", "            Actual    ")
  headers = [ "HSD", "HSG", "SC", "CG", "PC", " ", "HSD", "HSG", "SC", "CG", "PC"]
  print("row:wife, column:husband")
  table = tabulate(estimated_assortative_moments, headers, floatfmt=".2f", tablefmt="simple")
  print(table)
  ###################################################################################################
  return estimated_married_moments_w