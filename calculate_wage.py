from libc.math import exp as cexp
import parameters1 as p
from draw_husband import Husband
from draw_wife import Wife
import constant_parameters as c

def calculate_wage_w(wife, w_draw, epsilon):
  # this function calculates wives actual wage
  if wife.emp_state == c.UNEMP:   #didn't worked in previous period
    # draw job offer
    prob_full_tmp = p.lambda0_w_ft + p.lambda1_w_ft*wife.exp + p.lambda21_w_ft*wife.hsg + p.lambda22_w_ft*wife.sc + p.lambda23_w_ft*wife.cg + p.lambda24_w_ft*wife.pc
    prob_part_tmp = p.lambda0_w_pt + p.lambda1_w_pt*wife.exp + p.lambda21_w_pt*wife.hsg + p.lambda22_w_pt*wife.sc + p.lambda23_w_pt*wife.cg + p.lambda24_w_fp*wife.pc
    prob_full_w = cexp(prob_full_tmp)/(1+cexp(prob_full_tmp))
    prob_part_w = cexp(prob_part_tmp)/(1+cexp(prob_part_tmp))
    if w_draw < prob_full_w:   #w_draws = rand(DRAW_F,T,2)  1 - health,2 -job offer,
      # draw wage for full time
      tmp1 = wife.ability_value + p.beta11_w * wife.exp * wife.hsg + p.beta12_w * wife.exp * wife.sc + p.beta13_w * wife.exp * wife.cg + p.beta14_w * wife.exp * wife.pc \
             + p.beta21_w * (wife.exp * wife.hsg) ** 2 + p.beta22_w * (wife.exp * wife.sc) ** 2 + p.beta23_w * (
                     wife.exp * wife.cg) ** 2 + p.beta24_w * (wife.exp * wife.pc) ** 2 \
             + p.beta31_w * wife.hsg + p.beta32_w * wife.sc + p.beta33_w * wife.cg + p.beta34_w * wife.pc
      tmp2 = epsilon * p.sigma_w_wage
      wage_full = cexp(tmp1 + tmp2)
    else:
      wage_full = 0
    if w_draw < prob_part_w:
      # draw wage for full time - will be multiply by 0.5 if part time job
      tmp1 = wife.ability_value + p.beta11_w * wife.exp * wife.hsg + p.beta12_w * wife.exp * wife.sc + p.beta13_w * wife.exp * wife.cg + p.beta14_w * wife.exp * wife.pc \
             + p.beta21_w * (wife.exp * wife.hsg) ** 2 + p.beta22_w * (wife.exp * wife.sc) ** 2 + p.beta23_w * (
                 wife.exp * wife.cg) ** 2 + p.beta24_w * (wife.exp * wife.pc) ** 2 \
             + p.beta31_w * wife.hsg + p.beta32_w * wife.sc + p.beta33_w * wife.cg + p.beta34_w * wife.pc
      tmp2 = epsilon * p.sigma_w_wage
      wage_part = cexp(0.5*tmp1 + tmp2)
    else:
      wage_part = 0
  else:   #    wife.emp == 1 - worked in previous period
    prob_not_laid_off_tmp = p.lambda0_w_f + p.lambda1_w_f*wife.exp + p.lambda21_w_f*wife.hsg + p.lambda22_w_f*wife.sc + p.lambda23_w_f*wife.cg + p.lambda24_w_f*wife.pc
    prob_not_laid_off_w = cexp(prob_not_laid_off_tmp)/(1+cexp(prob_not_laid_off_tmp))
    if w_draw < prob_not_laid_off_w:
      wife.emp = 1
      tmp1 = wife.ability_value + p.beta11_w * wife.exp * wife.hsg + p.beta12_w * wife.exp * wife.sc + p.beta13_w * wife.exp * wife.cg + p.beta14_w * wife.exp * wife.pc \
               + p.beta21_w * (wife.exp * wife.hsg) ** 2 + p.beta22_w * (wife.exp * wife.sc) ** 2 + p.beta23_w * (
                   wife.exp * wife.cg) ** 2 + p.beta24_w * (wife.exp * wife.pc) ** 2 \
               + p.beta31_w * wife.hsg + p.beta32_w * wife.sc + p.beta33_w * wife.cg + p.beta34_w * wife.pc
      tmp2 = epsilon * p.sigma_w_wage
      if wife.capacity == 1:  # worked in previous period full time
        wage_full = cexp(tmp1 + tmp2)
      else:
        assert(wife.capacity == 0.5)
        wage_part = cexp(0.5*tmp1 + tmp2)
    else:    # got fired
      wage_full = 0
      wage_part = 0
      wife.EMP = 0
      wife.capacity = 0
  return wage_full , wage_part

##############################################################################333
def calculate_wage_h(husband, h_draw, epsilon):
  # this function calculates wives actual wage
  if  husband.emp_state == c.UNEMP:  # didn't worked in previous period
    # draw job offer
    prob_full_tmp = p.lambda0_h_ft + p.lambda1_h_ft *  husband.exp + p.lambda21_h_ft *  husband.hsg + p.lambda22_h_ft *  husband.sc + p.lambda23_h_ft *  husband.cg + p.lambda24_h_ft *  husband.pc
    prob_part_tmp = p.lambda0_h_pt + p.lambda1_h_pt *  husband.exp + p.lambda21_h_pt *  husband.hsg + p.lambda22_h_pt *  husband.sc + p.lambda23_h_pt *  husband.cg + p.lambda24_h_fp *  husband.pc
    prob_full_h = cexp(prob_full_tmp) / (1 + cexp(prob_full_tmp))
    prob_part_h = cexp(prob_part_tmp) / (1 + cexp(prob_part_tmp))
    if h_draw < prob_full_h:  # w_draws = rand(DRAW_F,T,2)  1 - health,2 -job offer,
     husband.emp = 1
     # draw wage for full time
     tmp1 =  husband.ability_h_value + p.beta11_h *  husband.exp *  husband.hsg + p.beta12_h *  husband.exp *  husband.sc + p.beta13_h *  husband.exp *  husband.cg + p.beta14_h *  husband.exp *  husband.pc \
            + p.beta21_h * ( husband.exp *  husband.hsg) ** 2 + p.beta22_h * ( husband.exp *  husband.sc) ** 2 + p.beta23_h * (
                 husband.exp *  husband.cg) ** 2 + p.beta24_h * ( husband.exp *  husband.pc) ** 2 \
            + p.beta31_h *  husband.hsg + p.beta32_h *  husband.sc + p.beta33_h *  husband.cg + p.beta34_h *  husband.pc
     tmp2 = epsilon * p.sigma_h_wage
     wage_full = cexp(tmp1 + tmp2)
     husband.capacity = 1
    else:
      wage_full = 0
    if h_draw  <  prob_part_h:
     husband.EMP = 1
     # draw wage for full time - will be multiply by 0.5 if part time job
     tmp1 = husband.ability_h_value + p.beta11_h * husband.exp * husband.hsg + p.beta12_h * husband.exp * husband.sc + p.beta13_h * husband.exp * husband.cg + p.beta14_h * husband.exp * husband.pc \
       + p.beta21_h * (husband.exp * husband.hsg) ** 2 + p.beta22_h * (husband.exp * husband.sc) ** 2 + p.beta23_h * (
           husband.exp * husband.cg) ** 2 + p.beta24_h * (husband.exp * husband.pc) ** 2 \
       + p.beta31_h * husband.hsg + p.beta32_h * husband.sc + p.beta33_h * husband.cg + p.beta34_h * husband.pc
     tmp2 = epsilon * p.sigma_h_wage
     wage_part = cexp(0.5 * tmp1 + tmp2)
     husband.capacity = 0.5
    else:
     wage_part = 0
     husband.capacity = 0
     husband.EMP = 0
  else:  #  husband.emp == 1 - worked in previous period
    prob_not_laid_off_tmp = p.lambda0_h_f + p.lambda1_h_f * husband.HE + p.lambda21_h_f *  husband.hsg + p.lambda22_h_f *  husband.sc + p.lambda23_h_f *  husband.cg + p.lambda24_h_f *  husband.pc
    prob_not_laid_off_h = cexp(prob_not_laid_off_tmp) / (1 + cexp(prob_not_laid_off_tmp))
    if h_draw < prob_not_laid_off_h:
     husband.EMP = 1
     tmp1 = husband.ability_h_value + p.beta11_h * husband.exp * husband.hsg + p.beta12_h * husband.exp * husband.sc + p.beta13_h * husband.exp * husband.cg + p.beta14_h * husband.exp * husband.pc \
       + p.beta21_h * (husband.exp * husband.hsg) ** 2 + p.beta22_h * (husband.exp * husband.sc) ** 2 + p.beta23_h * (
           husband.exp * husband.cg) ** 2 + p.beta24_h * (husband.exp * husband.pc) ** 2 \
       + p.beta31_h * husband.hsg + p.beta32_h * husband.sc + p.beta33_h * husband.cg + p.beta34_h * husband.pc
     tmp2 = epsilon * p.sigma_h_wage
     if  husband.capacity == 1:  # worked in previous period full time
      wage_full = cexp(tmp1 + tmp2)
      husband.capacity = 1
     else:
      assert ( husband.capacity == 0.5)
      wage_part = cexp(0.5 * tmp1 + tmp2)
      husband.capacity = 0.5
    else:  # got fired
      wage_full = 0
      wage_part = 0
      husband.EMP = 0
      husband.capacity = 0
  return wage_full, wage_part

