# number of draws
DRAW_B = 1
DRAW_F = 100
cohort = 1980
max_period = 43  # retirement
men_full_index_array = [2, 3, 8, 9, 14, 15]
men_part_index_array = [4, 5, 10, 11, 16, 17]
men_unemployed_index_array = [0, 1, 6, 7, 12, 13]
pregnancy_index_array = [1, 3, 5, 7, 9, 11, 13, 15, 17]
single_women_pregnancy_index_array = [1, 3, 5, 8, 10, 12]
single_women_full_time_index_array = [2, 3, 9, 10]
single_women_part_time_index_array = [4, 5, 11, 12]
single_women_welfare_index_array = [7, 8, 9, 10, 11, 12]
single_women_unemployed_index_array = [0, 1, 7, 8]
max_school = 14  # 30 - 17
max_1970 = 36
NO_KIDS = 0
beta0 = 0.983  # discount rate
MINIMUM_UTILITY = float('-inf')
AGE_VALUES = [18, 18, 20, 22, 25]
exp_vector = [0, 2, 4, 8, 16]  # experience - 5 point grid
home_time_vector = [0.5, 1, 1.5]
ub_h = 1000  # UNEMPLOYMENT BENEFIT HUSBAND
ub_w = 1000  # UNEMPLOYMENT BENEFIT WIFE
# work status: (unemp, emp)
UNEMP = 0
EMP = 1
# ability wife/husband: (low, medium, high)) + match quality: (high, medium, low)
normal_vector = [-1.150, 0.0, 1.150]
# marital status: (unmarried, married)
UNMARRIED = 0
MARRIED = 1
# school groups
school_size = 5
exp_size = 5
kids_size = 4    # number of children: (0, 1, 2, 3+)
ability_size = 3
home_time_size = 3
mother_size = 2
health_size = 2
# maximum fertility age
MAX_FERTILITY_AGE = 40
eta1 = 0.194   # fraction from parents net income  that one kid get
eta2 = 0.293   # fraction from parents net income that 2 kids get
eta3 = 0.367   # fraction from parents net  income that 3 kids get
eta4 = 0.423   # fraction from parents net income  that 4 kids get
scale = 0.707  # fraction of public consumption
bp = 0.5       # bargaining power
GRID = 3
AGE = 17          # initial age
GOOD = 0 # health status
POOR = 1
HK1 = 1 # 0 - 2 years of experience
HK2 = 4 # 3 - 5 years of experience
HK3 = 8 # 6 - 10 years of experience
HK4 = 12 # 11 + years of experience

mother_hispanic_newcommer_60 = 0.1      # probability mother was an immigrant
mother_hispanic_newcommer_70 = 0.1      # probability mother was an immigrant
mother_hispanic_newcommer_80 = 0.1      # probability mother was an immigrant
mother_hispanic_newcommer_90 = 0.1      # probability mother was an immigrant
#                  M=0,C=0	 M=1,C=0	M=0,C=1	 M=1,C=1
mother_1960_white    = [6.06,	88.71,	89.16]
mother_1960_black    = [30.40,	94.30,	94.3]
mother_1960_hispanic = [13.62,	94.37,	95.31]
mother_1970_white	   = [11.28,	82.16,	83.48]
mother_1970_black    = [45.26,	87.75,	90.52]
mother_1970_hispanic = [21.76,	95.30,	96.3]
mother_1980_white    = [16.24,	81.74,	83.12]
mother_1980_black	   = [57.42,	92.58,	95.31]
mother_1980_hispanic = [24.22,	93.06,	93.77]
mother_1990_white    = [19.72,	74.51,	76.81]
mother_1990_black	   = [56.66,	87.67,	92.24]
mother_1990_hispanic = [25.16,	90.99,	91.93]

constant_welfare = 4000   # before 97
by_kids_welfare = 1000    # before 97
by_income_welfare = -0.1  # before 97

cb_const_60 = 4317.681 # child benefit for single mom + 1 kid - annualy
cb_per_child_60 = 1517.235
cb_const_70 = 4749.394 # child benefit for single mom + 1 kid - annualy
cb_per_child_70 = 1179.676
cb_const_80 = 4530.784 # child benefit for single mom + 1 kid - annualy
cb_per_child_80 = 975.3533
num_cohort = 3

home_p = 0