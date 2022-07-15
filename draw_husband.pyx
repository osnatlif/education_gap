from parameters import p
cimport constant_parameters as c
cimport libc.math as cmath
from draw_wife cimport Wife
cdef extern from "randn.c":
    double uniform()
import numpy as np

#cdef double[:,:] husbands2 = np.loadtxt("husbands_all_new.out")
# husbands2 = np.loadtxt("husbands_all_new.out")
# husbands3 = np.loadtxt("husbands_all_new.out")
# husbands4 = np.loadtxt("husbands_all_new.out")
# husbands5 = np.loadtxt("husbands_all_new.out")

cdef class Husband:
    def get_capacity(self):
        return self.capacity
    def get_schooling(self):
        return self.schooling
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


cpdef update_school_and_age_backwords(int school_group, int t,Husband husband):   # used only for calculating the EMAX of single men - Backward
    husband.age = c.AGE_VALUES[school_group] + t
    if husband.age >= c.AGE_VALUES[husband.schooling]:
        husband.exp = husband.age - c.AGE_VALUES[husband.schooling]
    else:
        husband.exp = 0  # if husband is still at school, experience would be zero
    update_school(husband)


cpdef update_school(Husband husband):         # this function update education in Husnabds structures
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


cpdef Husband draw_husband_forward(Wife wife, double mother0, double mother1, double mother2):
    cdef Husband result = Husband()
    cdef double temp = uniform()*100
    # draw wife's parents information
    if temp < mother0:
        result.mother_educ = 0
        result.mother_marital = 0
    elif temp < mother1:
        result.mother_educ = 0
        result.mother_marital = 1
    elif temp < mother2:
        result.mother_educ = 1
        result.mother_marital = 0
    else:
        result.mother_educ = 1
        result.mother_marital = 1
    # update ability by mother education and marital status
    cdef double temp_high_ability = p.ab_high1 + p.ab_high2 * result.mother_educ + p.ab_high3 * result.mother_marital
    cdef double temp_medium_ability = p.ab_medium1 + p.ab_medium2 * result.mother_educ + p.ab_medium3 * result.mother_marital
    cdef double prob_high_ability = temp_high_ability / (1 + temp_high_ability + temp_medium_ability)
    cdef double prob_medium_ability = temp_medium_ability / (1 + temp_high_ability + temp_medium_ability)
    temp = uniform()
    if temp < prob_high_ability:
        result.ability_i = 2
        result.ability_value = c.normal_vector[2] * p.sigma_ability_h
    elif temp < prob_medium_ability + prob_high_ability:
        result.ability_i = 1
        result.ability_value = c.normal_vector[1] * p.sigma_ability_h
    else:
        result.ability_i = 0
        result.ability_value = c.normal_vector[0] * p.sigma_ability_h

    cdef double match_cg
    cdef double match_sc
    cdef double temp1
    if wife.age < 18:
        result.schooling = 0   # husband hsd
    elif wife.age < 20:
        result.schooling = 1   # husband hsg
    else:
        if wife.schooling < 2:  # wife is HSD or HSG
            match_cg = cmath.exp(p.omega4_w + p.omega6_w) / (
                1.0 + cmath.exp(p.omega4_w + p.omega6_w) + cmath.exp(p.omega7_w + p.omega8_w))  # probability of meeting cg if hs
            match_sc = cmath.exp(p.omega7_w + p.omega8_w) / (
                1.0 + cmath.exp(p.omega4_w + p.omega6_w) + cmath.exp(p.omega7_w + p.omega8_w))  # probability of meeting sc if hs
            # match_hsg = 1.0 / (1.0 + np.exp(p.omega4_w + p.omega6_w) + np.exp(p.omega7_w + p.omega8_w))  # probability of meeting hs if hs
        elif wife.schooling == 2:
            match_cg = cmath.exp(p.omega4_w + p.omega5_w) / (
                1.0 + cmath.exp(p.omega4_w + p.omega5_w) + cmath.exp(p.omega7_w))  # probability of meeting cg if sc
            match_sc = cmath.exp(p.omega7_w) / (
                1.0 + cmath.exp(p.omega4_w + p.omega5_w) + cmath.exp(p.omega7_w))  # probability of meeting sc if sc
            # match_hsg = 1.0 / (1.0 + np.exp(p.omega4_w + p.omega5_w) + np.exp(p.omega7_w))  # probability of meeting hs if sc
        elif wife.schooling > 2:
            match_cg = cmath.exp(p.omega4_w) / (1.0 + cmath.exp(p.omega4_w) + cmath.exp(p.omega7_w))  # probability of meeting cg if cg
            match_sc = cmath.exp(p.omega7_w) / (1.0 + cmath.exp(p.omega4_w) + cmath.exp(p.omega7_w))  # probability of meeting sc if cg
            # match_hsg = 1.0 / (1.0 + np.exp(p.omega4_w) + np.exp(p.omega7_w))  # probability of meeting hs if cg
            # draw husband schooling
        temp = uniform()
        if temp < match_cg:
            temp1 = uniform()
            if temp1 < 0.9:  # fix to right number
                result.schooling = 3  # cg
            else:
                result.schooling = 4  # pc
        if temp < match_cg + match_sc:
            result.schooling = 2  # sc
        else:
            temp1 = uniform()
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
