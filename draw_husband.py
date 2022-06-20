from parameters import p
import constant_parameters as c
from draw_wife import Wife
import numpy as np

#cdef double[:,:] husbands2 = np.loadtxt("husbands_all_new.out")
# husbands2 = np.loadtxt("husbands_all_new.out")
# husbands3 = np.loadtxt("husbands_all_new.out")
# husbands4 = np.loadtxt("husbands_all_new.out")
# husbands5 = np.loadtxt("husbands_all_new.out")

class Husband:
  def __init__(self):
    self.hsd = 0
    self.hsg = 0
    self.sc = 0
    self.cg = 0
    self.pc = 0
    self.schooling = 0   # husband schooling, can get values of 0-4
    self.years_of_schooling = 11
    self.exp = 0   # husband experience
    self.emp = 0
    self.capacity = 0
    self.married = 0
    self.age = 0
    self.kids = 0   # always zero unless single. if married - all kids at women structure
    self.health = 0
    self.home_time_ar = 1
    self.ability_value = 0.0
    self.ability_i = 0
    self.mother_educ = 0
    self.mother_marital = 0
    self.mother_immig = 0

  def __str__(self):
    return "Husband\n\tSchooling: " + str(self.schooling) + "\n\tSchooling Map: " + str(self.hsd)+","+str(self.hsg)+","+str(self.sc)+","+str(self.cg)+","+str(self.pc) + \
                                     "\n\tExperience: " + str(self.exp) + "\n\tAbility: " + str(self.ability_i)+","+str(self.ability_value) + \
                                     "\n\tAge: " + str(self.age)  + "\n\tEmployment status: " + str(self.emp)


def update_school_and_age_backwords(school_group,  t,husband):   # used only for calculating the EMAX of single men - Backward
  husband.age = c.AGE_VALUES[school_group] + t
  if husband.age >= c.AGE_VALUES[husband.schooling]:
    husband.exp = husband.age - c.AGE_VALUES[husband.schooling]
  else:
    husband.exp = 0  # if husband is still at school, experience would be zero
  update_school(husband)




def update_school(husband):         # this function update education in Husnabds structures
  if husband.schooling == 0:
    husband.hsd = 1
    husband.hsg = 0
    husband.sc = 0
    husband.cg = 0
    husband.pc = 0
  elif husband.schooling == 1:
    husband.hsg = 1
    husband.hsd = 0
    husband.sc = 0
    husband.cg = 0
    husband.pc = 0
  elif husband.schooling == 2:
    husband.sc = 1
    husband.hsg = 0
    husband.hsd = 0
    husband.cg = 0
    husband.pc = 0
  elif husband.schooling == 3:
    husband.cg = 1
    husband.hsg = 0
    husband.hsd = 0
    husband.sc = 0
    husband.pc = 0
  elif husband.schooling == 4:
    husband.pc = 1
    husband.hsg = 0
    husband.hsd = 0
    husband.sc = 0
    husband.cg = 0
  else:
    assert False


def draw_husband_forward(wife, mother):
 result = Husband()
 temp = np.random.randint(0, 100)  # draw wife's parents information
 if temp < mother[0]:
   result.mother_educ = 0
   result.mother_marital = 0
 elif temp < mother[1]:
   result.mother_educ = 0
   result.mother_marital = 1
 elif temp < mother[2]:
   result.mother_educ = 1
   result.mother_marital = 0
 else:
   result.mother_educ = 1
   result.mother_marital = 1
 # update ability by mother education and marital status
 temp_high_ability = p.ab_high1 + p.ab_high2 * result.mother_educ + p.ab_high3 * result.mother_marital
 temp_medium_ability = p.ab_medium1 + p.ab_medium2 * result.mother_educ + p.ab_medium3 * result.mother_marital
 prob_high_ability = temp_high_ability / (1 + temp_high_ability + temp_medium_ability)
 prob_medium_ability = temp_medium_ability / (1 + temp_high_ability + temp_medium_ability)
 temp = np.random.uniform(0, 1)
 if temp < prob_high_ability:
   result.ability_i = 2
   result.ability_value = c.normal_vector[2] * p.sigma_ability_h
 elif temp < prob_medium_ability + prob_high_ability:
   result.ability_i = 1
   result.ability_value = c.normal_vector[1] * p.sigma_ability_h
 else:
   result.ability_i = 0
   result.ability_value = c.normal_vector[0] * p.sigma_ability_h

 if wife.age < 18:
   result.schooling = 0   # husband hsd
 elif wife.age < 20:
   result.schooling = 1   # husband hsg
 else:
   if wife.schooling < 2:  # wife is HSD or HSG
     match_cg = np.exp(p.omega4_w + p.omega6_w) / (
           1.0 + np.exp(p.omega4_w + p.omega6_w) + np.exp(p.omega7_w + p.omega8_w))  # probability of meeting cg if hs
     match_sc = np.exp(p.omega7_w + p.omega8_w) / (
           1.0 + np.exp(p.omega4_w + p.omega6_w) + np.exp(p.omega7_w + p.omega8_w))  # probability of meeting sc if hs
     # match_hsg = 1.0 / (1.0 + np.exp(p.omega4_w + p.omega6_w) + np.exp(p.omega7_w + p.omega8_w))  # probability of meeting hs if hs
   elif wife.schooling == 2:
     match_cg = np.exp(p.omega4_w + p.omega5_w) / (
           1.0 + np.exp(p.omega4_w + p.omega5_w) + np.exp(p.omega7_w))  # probability of meeting cg if sc
     match_sc = np.exp(p.omega7_w) / (
           1.0 + np.exp(p.omega4_w + p.omega5_w) + np.exp(p.omega7_w))  # probability of meeting sc if sc
     # match_hsg = 1.0 / (1.0 + np.exp(p.omega4_w + p.omega5_w) + np.exp(p.omega7_w))  # probability of meeting hs if sc
   elif wife.schooling > 2:
     match_cg = np.exp(p.omega4_w) / (1.0 + np.exp(p.omega4_w) + np.exp(p.omega7_w))  # probability of meeting cg if cg
     match_sc = np.exp(p.omega7_w) / (1.0 + np.exp(p.omega4_w) + np.exp(p.omega7_w))  # probability of meeting sc if cg
     # match_hsg = 1.0 / (1.0 + np.exp(p.omega4_w) + np.exp(p.omega7_w))  # probability of meeting hs if cg
    # draw husband schooling
   temp = np.random.uniform(0, 1)
   if temp < match_cg:
     temp1 = np.random.uniform(0, 1)
     if temp1 < 0.9:  # fix to right number
       result.schooling = 3  # cg
     else:
       result.schooling = 4  # pc
   if temp < match_cg + match_sc:
     result.schooling = 2  # sc
   else:
     temp1 = np.random.uniform(0, 1)
     if temp1 < 0.8:  # fix to right number
       result.schooling = 1  # hsg
     else:
       result.schooling = 0  # hsd

 result.age = wife.age
 if result.age >= c.AGE_VALUES[result.schooling]:
  result.exp = result.age - c.AGE_VALUES[result.schooling]
 else:
  result.exp = 0  # if husband is still at school, experience would be zero
 update_school(result)

 return result
