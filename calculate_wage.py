import numpy as np
from parameters import p
from draw_husband import Husband
from draw_wife import Wife
import constant_parameters as c


def calculate_wage_w(wife):
  # this function calculates wives actual wage
  wage_full = 0
  wage_part = 0
  if wife.emp == c.UNEMP:   # didn't worked in previous period
    # draw job offer
    prob_full_tmp = p.lambda0_w_ft + p.lambda1_w_ft*wife.exp + p.lambda21_w_ft*wife.hsg + p.lambda22_w_ft*wife.sc + p.lambda23_w_ft*wife.cg + p.lambda24_w_ft*wife.pc
    prob_part_tmp = p.lambda0_w_pt + p.lambda1_w_pt*wife.exp + p.lambda21_w_pt*wife.hsg + p.lambda22_w_pt*wife.sc + p.lambda23_w_pt*wife.cg + p.lambda24_w_pt*wife.pc
    prob_full_w = np.exp(prob_full_tmp)/(1+np.exp(prob_full_tmp))
    prob_part_w = np.exp(prob_part_tmp)/(1+np.exp(prob_part_tmp))
    if np.random.uniform(0, 1) < prob_full_w:   # got full time job offer - draw wage for full time
      tmp1 = wife.ability_value + p.beta11_w * wife.exp * wife.hsd + p.beta12_w * wife.exp * wife.hsg + p.beta13_w * wife.exp * wife.sc + p.beta14_w * wife.exp * wife.cg + p.beta15_w * wife.exp * wife.pc \
        + p.beta21_w * (wife.exp * wife.hsd) ** 2+ p.beta22_w * (wife.exp * wife.hsg) ** 2 + p.beta23_w * (wife.exp * wife.sc) ** 2 + p.beta24_w * (wife.exp * wife.cg) ** 2 + p.beta25_w * (wife.exp * wife.pc) ** 2 \
        + p.beta31_w * wife.hsd + p.beta32_w * wife.hsg + p.beta33_w * wife.sc + p.beta34_w * wife.cg + p.beta35_w * wife.pc
      tmp2 = np.random.normal() * p.sigma_w_wage
      wage_full = np.exp(tmp1 + tmp2)
    if np.random.uniform(0, 1) < prob_part_w:
      # draw wage for full time - will be multiply by 0.5 if part time job
      tmp1 = wife.ability_value + p.beta11_w * wife.exp * wife.hsd + p.beta12_w * wife.exp * wife.hsg + p.beta13_w * wife.exp * wife.sc + p.beta14_w * wife.exp * wife.cg + p.beta15_w * wife.exp * wife.pc \
             + p.beta21_w * (wife.exp * wife.hsd) ** 2 + p.beta22_w * (wife.exp * wife.hsg) ** 2 + p.beta23_w * (wife.exp * wife.sc) ** 2 + p.beta24_w * (wife.exp * wife.cg) ** 2 + p.beta25_w * (wife.exp * wife.pc) ** 2 \
             + p.beta31_w * wife.hsd + p.beta32_w * wife.hsg + p.beta33_w * wife.sc + p.beta34_w * wife.cg + p.beta35_w * wife.pc
      tmp2 = np.random.normal() * p.sigma_w_wage
      wage_part = 0.5 * np.exp(tmp1 + tmp2)
  else:   #    wife.emp == 1 - worked in previous period
    prob_not_laid_off_tmp = p.lambda0_w_f + p.lambda1_w_f*wife.exp + p.lambda21_w_f*wife.hsg + p.lambda22_w_f*wife.sc + p.lambda23_w_f*wife.cg + p.lambda24_w_f*wife.pc
    prob_not_laid_off_w = np.exp(prob_not_laid_off_tmp)/(1+ np.exp(prob_not_laid_off_tmp))
    if np.random.uniform(0, 1) < prob_not_laid_off_w:
      tmp1 = wife.ability_value + p.beta11_w * wife.exp * wife.hsd + p.beta12_w * wife.exp * wife.hsg + p.beta13_w * wife.exp * wife.sc + p.beta14_w * wife.exp * wife.cg + p.beta15_w * wife.exp * wife.pc \
             + p.beta21_w * (wife.exp * wife.hsd) ** 2 + p.beta22_w * (wife.exp * wife.hsg) ** 2 + p.beta23_w * (wife.exp * wife.sc) ** 2 + p.beta24_w * (wife.exp * wife.cg) ** 2 + p.beta25_w * (wife.exp * wife.pc) ** 2 \
             + p.beta31_w * wife.hsd + p.beta32_w * wife.hsg + p.beta33_w * wife.sc + p.beta34_w * wife.cg + p.beta35_w * wife.pc
      tmp2 = np.random.normal() * p.sigma_w_wage
      if wife.capacity == 1:  # worked in previous period full time
        wage_full = np.exp(tmp1 + tmp2)
      else:
        assert(wife.capacity == 0.5)
        wage_part = 0.5 * np.exp(tmp1 + tmp2)
  return wage_full, wage_part

##############################################################################333
def calculate_wage_h(husband):
  # this function calculates wives actual wage
  wage_full = 0
  wage_part = 0
  if husband.emp == c.UNEMP:  # didn't work in previous period
    # draw job offer
    prob_full_tmp = p.lambda0_h_ft + p.lambda1_h_ft *  husband.exp + p.lambda21_h_ft *  husband.hsg + p.lambda22_h_ft * husband.sc + p.lambda23_h_ft * husband.cg + p.lambda24_h_ft * husband.pc
    prob_part_tmp = p.lambda0_h_pt + p.lambda1_h_pt *  husband.exp + p.lambda21_h_pt *  husband.hsg + p.lambda22_h_pt * husband.sc + p.lambda23_h_pt * husband.cg + p.lambda24_h_pt * husband.pc
    prob_full_h = np.exp(prob_full_tmp) / (1 + np.exp(prob_full_tmp))
    prob_part_h = np.exp(prob_part_tmp) / (1 + np.exp(prob_part_tmp))
    if np.random.uniform(0, 1) < prob_full_h:  # w_draws = rand(DRAW_F,T,2)  1 - health,2 -job offer,
      # draw wage for full time
      tmp1 =  husband.ability_value + p.beta11_h *  husband.exp *  husband.hsd + p.beta12_h *  husband.exp *  husband.hsg + p.beta13_h *  husband.exp * husband.sc + p.beta14_h * husband.exp * husband.cg + p.beta15_h * husband.exp * husband.pc \
        + p.beta21_h * ( husband.exp *  husband.hsd) ** 2+ p.beta22_h * ( husband.exp *  husband.hsg) ** 2 + p.beta23_h * ( husband.exp *  husband.sc) ** 2 + p.beta24_h * (husband.exp * husband.cg) ** 2 + p.beta25_h * (husband.exp * husband.pc) ** 2 \
        + p.beta31_h *  husband.hsd + p.beta32_h *  husband.hsg + p.beta33_h *  husband.sc + p.beta34_h *  husband.cg + p.beta35_h *  husband.pc
      tmp2 = np.random.normal() * p.sigma_h_wage
      wage_full = np.exp(tmp1 + tmp2)
    if np.random.uniform(0, 1) < prob_part_h:
      # draw wage for full time - will be multiply by 0.5 if part time job
      tmp1 = husband.ability_value + p.beta11_h * husband.exp * husband.hsd + p.beta12_h * husband.exp * husband.hsg + p.beta13_h * husband.exp * husband.sc + p.beta14_h * husband.exp * husband.cg + p.beta15_h * husband.exp * husband.pc \
             + p.beta21_h * (husband.exp * husband.hsd) ** 2 + p.beta22_h * (husband.exp * husband.hsg) ** 2 + p.beta23_h * (husband.exp * husband.sc) ** 2 + p.beta24_h * (husband.exp * husband.cg) ** 2 + p.beta25_h * (husband.exp * husband.pc) ** 2 \
             + p.beta31_h * husband.hsd + p.beta32_h * husband.hsg + p.beta33_h * husband.sc + p.beta34_h * husband.cg + p.beta35_h * husband.pc
      tmp2 = np.random.normal() * p.sigma_h_wage
      wage_part = 0.5 * np.exp(tmp1 + tmp2)
  else:  #  husband.emp == 1 - worked in previous period
    prob_not_laid_off_tmp = p.lambda0_h_f + p.lambda1_h_f * husband.exp + p.lambda21_h_f *  husband.hsg + p.lambda22_h_f *  husband.sc + p.lambda23_h_f *  husband.cg + p.lambda24_h_f *  husband.pc
    prob_not_laid_off_h = np.exp(prob_not_laid_off_tmp) / (1 + np.exp(prob_not_laid_off_tmp))
    if np.random.uniform(0, 1) < prob_not_laid_off_h:
      tmp1 = husband.ability_value + p.beta11_h * husband.exp * husband.hsd + p.beta12_h * husband.exp * husband.hsg + p.beta13_h * husband.exp * husband.sc + p.beta14_h * husband.exp * husband.cg + p.beta15_h * husband.exp * husband.pc \
             + p.beta21_h * (husband.exp * husband.hsd) ** 2 + p.beta22_h * (                   husband.exp * husband.hsg) ** 2 + p.beta23_h * (husband.exp * husband.sc) ** 2 + p.beta24_h * (husband.exp * husband.cg) ** 2 + p.beta25_h * (husband.exp * husband.pc) ** 2 \
             + p.beta31_h * husband.hsd + p.beta32_h * husband.hsg + p.beta33_h * husband.sc + p.beta34_h * husband.cg + p.beta35_h * husband.pc
      tmp2 = np.random.normal() * p.sigma_h_wage
      if husband.capacity == 1:  # worked in previous period full time
        wage_full = np.exp(tmp1 + tmp2)
      else:
        assert(husband.capacity == 0.5)
        wage_part = 0.5 * np.exp(tmp1 + tmp2)
  return wage_full, wage_part

