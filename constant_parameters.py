# number of draws
DRAW_B = 1
DRAW_F = 100
cohort = 1980

NO_KIDS = 0
beta0 = 0.983  # discount rate
MINIMUM_UTILITY = float('-inf')
AGE_VALUES = [18, 18, 20, 22, 25]
exp_vector = [0, 2, 4, 8, 16]  # experience - 5 point grid
EXP_SIZE = 5
UB_H = 1000  # UNEMPLOYMENT BENEFIT HUSBAND
UB_W = 1000  # UNEMPLOYMENT BENEFIT WIFE
KIDS_SIZE = 4 # number of children: (0, 1, 2, 3+)
# work status: (unemp, emp)
UNEMP = 0
EMP = 1
WORK_SIZE = 2
# ability wife/husband: (low, medium, high)) + match quality: (high, medium, low)
normal_vector = [-1.150, 0.0, 1.150]
ABILITY_SIZE = 3
MATCH_Q_SIZE = 3
# marital status: (unmarried, married)
UNMARRIED = 0
MARRIED = 1
# school groups
SCHOOL_SIZE = 5
# maximum fertility age
MAX_FERTILITY_AGE = 40
eta1 = 0.194 # fraction from parents net income  that one kid get
eta2 = 0.293 # fraction from parents net income that 2 kids get
eta3 = 0.367 # fraction from parents net  income that 3 kids get
eta4 = 0.423 # fraction from parents net income  that 4 kids get
scale = 0.707 # fraction of public consumption 
BP = 0.5 # FIXED BARGENING POWER
GRID = 3
AGE = 16 # initial age
max_period = 44 # retirement
GOOD = 1 # health status
POOR = 2
HK1 = 1 # 0 - 2 years of experience
HK2 = 4 # 3 - 5 years of experience
HK3 = 8 # 6 - 10 years of experience
HK4 = 12 # 11 + years of experience

m_education = 0.06 # probability of collage educated mother - married women with CG + PC at age 45 (no earlier data), cohort 1915
m_education_70 = 0.06 # probability of collage educated mother - married women with CG + PC at age 40, cohort 1925
m_education_80 = 0.11 # probability of collage educated mother - married women with CG + PC at age 40, cohort 1935
m_marital = 0.20 # probability of married mother
m_marital_70 = 0.27 # probability  of married mother
m_marital_80 = 0.29 # probability  of married mother
m_newcommer = 0.1 # probability mother was an immigrant
m_newcommer_70 = 0.1 # probability mother was an immigrant
m_newcommer_80 = 0.1 # probability mother was an immigrant

cb_const = 4317.681 # child benefit for single mom + 1 kid - annualy
cb_per_child = 1517.235
cb_const_70 = 4749.394 # child benefit for single mom + 1 kid - annualy
cb_per_child_70 = 1179.676
cb_const_80 = 4530.784 # child benefit for single mom + 1 kid - annualy
cb_per_child_80 = 975.3533
num_cohort = 3

home_p = 0