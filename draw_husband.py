import parameters1 as p
import constant_parameters as c
from draw_wife import Wife
import numpy as np

#cdef double[:,:] husbands2 = np.loadtxt("husbands_all_new.out")
husbands2 = np.loadtxt("husbands_all_new.out")
husbands3 = np.loadtxt("husbands_all_new.out")
husbands4 = np.loadtxt("husbands_all_new.out")
husbands5 = np.loadtxt("husbands_all_new.out")

class Husband:
  def get_school(self):
    return self.schooling
  def get_(self):
    return self.HE
  def get_age(self):
    return self.age
  def increase_age(self):
    self.age += 1
  def __init__(self):
    self.hsd = 0
    self.hsg = 0
    self.sc = 0
    self.cg = 0
    self.pc = 0
    self.schooling = 0   # husband schooling, can get values of 0-4
    self.exp = 0   # husband experience
    self.married = 0
    self.ability_value = 0.0
    self.ability_i = 0
    self.age = 0
    self.emp_state = 0
    self.kids = 0   # always zero unless single. if married - all kids at women structure
    self.health = 0
    self.mother_educ = 0
    self.mother_marital = 0
    self.mother_immig = 0
    self.home_time_ar = 0
  def __str__(self):
    return "Husband\n\tSchooling: " + str(self.schooling) + "\n\tSchooling Map: " + str(self.hsd)+","+str(self.hsg)+","+str(self.sc)+","+str(self.cg)+","+str(self.pc) + \
                                     "\n\tExperience: " + str(self.exp) + "\n\tAbility: " + str(self.ability_i)+","+str(self.ability_value) + \
                                     "\n\tAge: " + str(self.age)  + "\n\tEmployment status: " + str(self.emp_state)


def update_school_and_age(school_group,  t,husband):   # used only for calculating the EMAX of single men - Backward
  husband.age = c.AGE_VALUES[school_group] + t
  if husband.age >= c.AGE_VALUES[husband.schooling]:
    husband.exp = husband.age - c.AGE_VALUES[husband.schooling]
  else:
    husband.exp = 0  # if husband is still at school, experience would be zero
  update_school(husband)



def update_school_and_age_f(wife, husband):     # used only for forward solution - when wife draw a partner
  husband.age = wife.age
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


def draw_husband(t,  wife, forward):
 result = Husband()
 result.ability_i = np.random.randint(0, 2)                                           # draw ability index
 result.ability_value = c.normal_vector[result.ability_i] * p.sigma_ability_h   # calculate ability value
 if wife.schooling == 1:
  tmp_husbands = husbands2
 elif wife.schooling == 2:
  tmp_husbands = husbands3
 elif wife.schooling == 3:
  tmp_husbands = husbands4
 else:
  tmp_husbands = husbands5

  husband_arr = tmp_husbands[t+wife.age_index]      # t+wife.age_index = wife's age which is identical to husband's age
  prob = np.random.uniform(0, 1)
  # find the first index in the husband array that is not less than the probability
  # note: first column of the husband matrix is skipped since it is just an index, hence the: [1:]
  h_index = 0
  for value in husband_arr[1:]:
    if value >= prob:
      break
    h_index +=1
  # husband schooling is in the range: 0-4
  result.exp = int(h_index)
  #print(result.exp)
  assert(result.exp in range(0, 5))
  if forward:
    update_school_and_age_f(wife, result)
  else:
    update_school_and_age(result.schooling, t, result)

  return result
