import numpy as np
import parameters1 as p
import constant_parameters as c


wives = np.loadtxt("wives.out")


class Wife:
  def __init__(self):
    # following are indicators for the wife's schooling they have values of 0/1 and only one of them could be 1
    self.hsd = 0
    self.hsg = 0
    self.sc = 0
    self.cg = 0
    self.pc = 0
    self.schooling = 0    # wife schooling, can get values of 0-4
    self.years_of_schooling = 11
    self.exp = 0    # wife experience
    self.emp = 0  # wife employment state
    self.married = 0
    self.ability_value = 0
    self.ability_i = 0
    self.match = 0.0
    self.match_i = 0
    self.age = 0
    self.kids = 0      # wife's kids
    self.health = 0
    self.preg = 0
    self.mother_educ = 0
    self.mother_marital = 0
    self.mother_immig = 0
    self.home_time_ar = 0
  def __str__(self):
    return "Wife\n\tSchooling: " + str(self.schooling) + "\n\tSchooling Map: " + str(self.hsd) + "," + str(self.hsg) + \
           "," + str(self.sc) + "," + str(self.cg) + "," + str(self.pc) + \
           "\n\tExperience: " + str(self.exp) + "\n\tAbility: " + str(self.ability_i) + "," + str(self.ability_value) + \
           "\n\tMatch Quality: " + str(self.match_i) + ", " + str(self.match) + \
           "\n\tAge: " + str(self.age)  + "\n\tKids: " + str(self.kids)+ "\n\tHealth: " + str(self.health)+ \
           "\n\tPregnant: " + str(self.preg) +"\n\tmother education: " + str(self.mother_educ) +"\n\tmother marital: " + str(self.marital)


def update_wife_schooling(school_group,  t, wife):
  # T_END is used together with the t index which get values 0-26
  wife.schooling = school_group
  wife.age = c.AGE_VALUES[wife.schooling] + t
  if wife.schooling == 1:
    wife.hsg = 1
    wife.sc = 0
    wife.cg = 0
    wife.pc = 0
  elif wife.schooling == 2:
    wife.sc = 1
    wife.hsg = 0
    wife.cg = 0
    wife.pc = 0
  elif wife.schooling == 3:
    wife.cg = 1
    wife.hsg = 0
    wife.sc = 0
    wife.pc = 0
  elif wife.schooling == 4:
    wife.pc = 1
    wife.hsg = 0
    wife.sc = 0
    wife.cg = 0
  else:
    assert False




def update_ability(ability, wife):
  wife.ability_i = ability
  wife.ability_value = c.normal_vector[ability]*p.sigma_ability_w

def draw_wife(t, age_index, HS):
  result = Wife()
  result.match_i = np.random.randint(0, 2)
  result.match = c.normal_vector[result.match_i]*p.sigma_q
  result.ability_wi = np.random.randint(0, 2)
  result.ability_w_value = c.normal_vector[result.ability_wi] * p.sigma_ability_w
  wives_arr = wives[t+age_index]
  prob = np.random.uniform(0, 1)
  w_index = 0
  for value in wives_arr:
    if value >= prob:
      break
    w_index +=1
  assert(w_index < 40)   # index will be in the range: 0-39
  result.schooling = int(w_index/10) + 1
  assert result.schooling in range(1, 5)  # wife schooling is in the range: 1-4

  result.exp = c.exp_vector[w_index % 5]        # [0,4]->0, [5,9]->1, [10,14]->0, [15-19]->1, etc.
  result.emp_state = int(w_index/5) % 2
  assert(result.emp_state == 1 or result.emp_state == 0)

  return result
