# number of draws
cdef int DRAW_B = 1
DRAW_F = 100
cdef int cohort = 1970
cdef int max_period = 43  # retirement
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
cdef int NO_KIDS = 0
cdef double beta0 = 0.983  # discount rate
cdef double MINIMUM_UTILITY = float('-inf')
cdef int[:] AGE_VALUES = [18, 18, 20, 22, 25]
cdef int[:] exp_vector = [0, 2, 4, 8, 16]  # experience - 5 point grid
#cdef double[:] home_time_vector = [0.5, 1, 1.5]
cdef double[:] home_time_vector = [0.5, 1.5]
cdef int ub_h = 1000  # UNEMPLOYMENT BENEFIT HUSBAND
cdef int ub_w = 1000  # UNEMPLOYMENT BENEFIT WIFE
# work status: (unemp, emp)
cdef int UNEMP = 0
cdef int EMP = 1
# ability wife/husband: (low, medium, high)) + match quality: (high, medium, low)
# cdef double[:] normal_vector = [-1.150, 0.0, 1.150]
cdef double[:] normal_vector = [-1.150,  1.150]

# marital status: (unmarried, married)
cdef int UNMARRIED = 0
cdef int MARRIED = 1
# school groups
cdef int school_size = 5
cdef int exp_size = 5
cdef int kids_size = 4    # number of children: (0, 1, 2, 3+)
cdef int ability_size = 2 #3
cdef int home_time_size = 2 #3
cdef int mother_size = 1 #2
cdef int health_size = 1 # 2
cdef int mother_educ = 0
cdef int mother_marital = 0
# maximum fertility age
cdef int MAX_FERTILITY_AGE = 40
cdef double eta1 = 0.194   # fraction from parents net income  that one kid get
cdef double eta2 = 0.293   # fraction from parents net income that 2 kids get
cdef double eta3 = 0.367   # fraction from parents net  income that 3 kids get
cdef double eta4 = 0.423   # fraction from parents net income  that 4 kids get
cdef double scale = 0.707  # fraction of public consumption
cdef double bp = 0.5       # bargaining power
cdef int GRID = 3
cdef int AGE = 17          # initial age
cdef int GOOD = 0 # health status
cdef int POOR = 1
cdef int HK1 = 1 # 0 - 2 years of experience
cdef int HK2 = 4 # 3 - 5 years of experience
cdef int HK3 = 8 # 6 - 10 years of experience
cdef int HK4 = 12 # 11 + years of experience

cdef double mother_hispanic_newcommer_60 = 0.1      # probability mother was an immigrant
cdef double mother_hispanic_newcommer_70 = 0.1      # probability mother was an immigrant
cdef double mother_hispanic_newcommer_80 = 0.1      # probability mother was an immigrant
cdef double mother_hispanic_newcommer_90 = 0.1      # probability mother was an immigrant
#                  M=0,C=0       M=1,C=0        M=0,C=1  M=1,C=1
cdef double[:] mother_1960_white    = [6.06,    88.71,  89.16]
cdef double[:] mother_1960_black    = [30.40,   94.30,  94.3]
cdef double[:] mother_1960_hispanic = [13.62,   94.37,  95.31]
cdef double[:] mother_1970_white           = [11.28,    82.16,  83.48]
cdef double[:] mother_1970_black    = [45.26,   87.75,  90.52]
cdef double[:] mother_1970_hispanic = [21.76,   95.30,  96.3]
cdef double[:] mother_1980_white    = [16.24,   81.74,  83.12]
cdef double[:] mother_1980_black    = [57.42,    92.58,  95.31]
cdef double[:] mother_1980_hispanic = [24.22,   93.06,  93.77]
cdef double[:] mother_1990_white    = [19.72,   74.51,  76.81]
cdef double[:] mother_1990_black    = [56.66,    87.67,  92.24]
cdef double[:] mother_1990_hispanic = [25.16,   90.99,  91.93]

cdef int constant_welfare = 4000   # before 97
cdef int by_kids_welfare = 1000    # before 97
cdef double by_income_welfare = -0.1  # before 97

cdef double cb_const_60 = 4317.681 # child benefit for single mom + 1 kid - annually
cdef double cb_per_child_60 = 1517.235
cdef double cb_const_70 = 4749.394 # child benefit for single mom + 1 kid - annually
cdef double cb_per_child_70 = 1179.676
cdef double cb_const_80 = 4530.784 # child benefit for single mom + 1 kid - annually
cdef double cb_per_child_80 = 975.3533
cdef double cb_const_90 = 4530.784 # child benefit for single mom + 1 kid - annually
cdef double cb_per_child_90 = 975.3533
cdef int num_cohort = 3
cdef double home_p = 0

max_period_f = max_period
kids_size_f = kids_size
school_size_f = school_size
max_school_f = max_school
cohort_f = cohort
mother_1960_white_f    = mother_1960_white
mother_1960_black_f    = mother_1960_black
mother_1960_hispanic_f = mother_1960_hispanic
mother_1970_white_f    = mother_1970_white
mother_1970_black_f    = mother_1970_black
mother_1970_hispanic_f = mother_1970_hispanic
mother_1980_white_f    = mother_1980_white
mother_1980_black_f    = mother_1980_black
mother_1980_hispanic_f = mother_1980_hispanic
mother_1990_white_f    = mother_1990_white
mother_1990_black_f    = mother_1990_black
mother_1990_hispanic_f = mother_1990_hispanic
bp_f = bp