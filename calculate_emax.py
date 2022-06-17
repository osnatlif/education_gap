import numpy as np
# from single_men import single_men
# from single_women import single_women
# from married_couple cimport married_couple
import constant_parameters as c
from single_men import single_men
from single_women import single_women
from married_couple_emax import married_couple_emax


def create_married_emax():
    return np.ndarray([c.max_period, c.school_size, c.school_size, c.exp_size, c.exp_size,c.kids_size, c.health_size, c.health_size,
    c.home_time_size, c.home_time_size, c.ability_size, c.ability_size, c.mother_size, c.mother_size, c.mother_size, c.mother_size])


def create_single_w_emax():
    return np.ndarray([c.max_period, c.school_size, c.exp_size, c.kids_size, c.health_size, c.home_time_size, c.ability_size, c.mother_size, c.mother_size])


def create_single_h_emax():
    return np.ndarray([c.max_period, c.school_size, c.exp_size, c.kids_size, c.health_size, c.home_time_size, c.ability_size, c.mother_size, c.mother_size])


def calculate_emax(w_emax, h_emax, w_s_emax, h_s_emax, verbose):
  iter_count = 0
  # running until the one before last period
  for t in range(c.max_period - 2, 0, -1):
    # EMAX FOR SINGLE MEN
    iter_count += single_men(t, w_emax, h_emax, w_s_emax, h_s_emax, verbose)
    # EMAX FOR SINGLE WOMEN
    iter_count += single_women(t, w_emax, h_emax, w_s_emax, h_s_emax, verbose)
    # EMAX FOR MARRIED COUPLE
    iter_count += married_couple_emax(t, w_emax, h_emax, w_s_emax, h_s_emax, verbose)

  return iter_count
