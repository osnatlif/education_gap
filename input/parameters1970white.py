import numpy as np
# marriage market parameters
omega3 = -1.345     # probability of meeting a husband if above 18 not in school
omega4_w = 0.114    # women's age
omega5_w = -0.004   # women's age*age
omega4_h = 0.1      # men's age
omega5_h = -0.003   # men's age*age
omega6_w = 1.67     # women's probability of meeting a  CG - CONSTANT
omega7_w = -1.257   # women's women's probability of meeting a  CG if she SC
omega8_w = -4.054   # women's probability of meeting a  CG if she HS
omega9_w = 0.684    # women's probability of meeting a  SC - CONSTANT
omega10_w = -1.989  # women's probability of meeting a  SC if she HS
omega6_h = 1.358    # men's probability of meeting a  CG - CONSTANT
omega7_h = -1.053   # men's probability of meeting a  CG if he SC
omega8_h = -2.126   # men's probability of meeting a  CG if he HS
omega9_h = 0.265    # men's probability of meeting a  SC - CONSTANT
omega10_h = -1.356  # men's probability of meeting a  SC if he HS
# wage parameters wife
beta11_w = 0.029	    # experience HSD
beta12_w = 0.054	    # experience HSG
beta13_w = 0.060	    # experience SC
beta14_w = 0.074	    # experience CG
beta15_w = 0.078	    # experience PC
beta21_w = -0.0001	  # exp^2 HSD
beta22_w = -0.0001	  # exp^2 HSG
beta23_w = -0.0001	  # exp^2 SC
beta24_w = -0.0002	  # exp^2 CG
beta25_w = -0.0002	  # exp^2 PC
beta31_w = 9.657	    # HSD
beta32_w = 9.783	    # HSG
beta33_w = 9.974	    # SC
beta34_w = 10.294	    # CG
beta35_w = 10.475	    # PC
# wage parameters husband
beta11_h = 0.045	   # experience HSD
beta12_h = 0.072	   # experience HSG
beta13_h = 0.081	   # experience SC
beta14_h = 0.090	   # experience CG
beta15_h = 0.099	   # experience PC
beta21_h = -0.0001	 # exp^2 HSD
beta22_h = -0.0001	 # exp^2 HSG
beta23_h = -0.0002	 # exp^2 SC
beta24_h = -0.0002	 # exp^2 CG
beta25_h = -0.0002	 # exp^2 PC
beta31_h = 9.877	   # hsd
beta32_h = 9.939     # hsg
beta33_h = 10.180	   # sc
beta34_h = 10.464	   # cg
beta35_h = 10.635	   # pc
# job offer parameters - full time
lambda0_w_ft = -0.57	  # job offer parameters - wife - full time	constant
lambda1_w_ft = 0.06	  # job offer parameters - wife	experience
lambda21_w_ft = 0.11	  # job offer parameters - wife	HSG
lambda22_w_ft = 0.11	  # job offer parameters - wife	SC
lambda23_w_ft = 0.11	  # job offer parameters - wife	CG
lambda24_w_ft = 0.11	  # job offer parameters - wife	PC
lambda0_h_ft = -0.32	  # job offer parameters - husband - full Time	constant
lambda1_h_ft = 0.10	    # job offer parameters - husband	experience
lambda21_h_ft = 0.16	  # job offer parameters - husband	education
lambda22_h_ft = 0.16	  # job offer parameters - husband	education
lambda23_h_ft = 0.16	  # job offer parameters - husband	education
lambda24_h_ft = 0.16	  # job offer parameters - husband	education
# job offer parameters - part-time
lambda0_w_pt = -1.52	  # job offer parameters - wife - part-time	constant
lambda1_w_pt = 0.01	  # job offer parameters - wife	experience
lambda21_w_pt = 0.06	  # job offer parameters - wife	education
lambda22_w_pt = 0.06	  # job offer parameters - wife	education
lambda23_w_pt = 0.06	  # job offer parameters - wife	education
lambda24_w_pt = 0.06	  # job offer parameters - wife	education

lambda0_h_pt = -1.93	  # job offer parameters - husband  - part-time	constant
lambda1_h_pt = 0.01	  # job offer parameters - husband	experience
lambda21_h_pt = 0.00	  # job offer parameters - husband	education
lambda22_h_pt = 0.00	  # job offer parameters - husband	education
lambda23_h_pt = 0.00	  # job offer parameters - husband	education
lambda24_h_pt = 0.00	  # job offer parameters - husband	education
# get fired
lambda0_w_f = 0.99	    # job offer parameters - wife - fired  ( PT FT)	constant
lambda1_w_f = 0.19	    # job offer parameters - wife	experience
lambda21_w_f = 0.11	  # job offer parameters - wife	education
lambda22_w_f = 0.11	  # job offer parameters - wife	education
lambda23_w_f = 0.11	  # job offer parameters - wife	education
lambda24_w_f = 0.11	  # job offer parameters - wife	education

lambda0_h_f = 1.11	    # job offer parameters - husband - fired (PT FT)	constant
lambda1_h_f = 0.27	    # job offer parameters - husband	experience
lambda21_h_f = 0.09	  # job offer parameters - husband	education
lambda22_h_f = 0.09	  # job offer parameters - husband	education
lambda23_h_f = 0.09	  # job offer parameters - husband	education
lambda24_h_f = 0.09	  # job offer parameters - husband	education
##############################################################################
# fixed parameters
##############################################################################
omega_1 = -1.867	       # probability of meeting a husband if below 18
omega_2 = -1.329	       # probability of meeting a husband if above 18 but in school
taste_c = 1.485	         # taste for marriage	constant
taste_w_up = -1.894  	 # taste for marriage	schooling gap - men more educated
taste_w_down = -2.227	 # taste for marriage	schooling gap - women more educated
taste_health = 0         # taste for marriage	health gap
preg_health = 0.0002     # utility from pregnancy - health
preg_unmarried = -22.429	   # utility from pregnancy -	married
preg_t_minus1 = -19.227   # utility from pregnancy - pregnancy in t-1
preg_kids = -13.98       # utility from pregnancy - number of kide
# utility from quality and quantity of children
row0 = -0.869	        # utility from quality and quantity of children	CES function's parameter
row1_w = 0.413	        # utility from quality and quantity of children	wife leisure
row1_h = 0.350	        # utility from quality and quantity of children	husband leisure
row2 = 0.03	          # utility from quality and quantity of children	spending per child
# welfare parameters
stigma = -44.742	      # disutility from welfare
stigma96 = -61.543	    # disutility from welfare after 1996
p_alimony = np.exp(-0.483)/(1+np.exp(-0.483))	    # prob of having alimony for single mothers)
alimony = np.exp(8.689)	        # mean of alimony	exp of draw from normal distribution
# utility parameters
alpha0 = 0.462	       # utility parameters 	CRRA consumption parameter
alpha11_w = 0.492	     # utility parameters - wife	leisure when pregnant
alpha12_w = 0.078	     # utility parameters - wife	leisure by  education
alpha13_w = 0.157	     # utility parameters - wife	leisure by health
alpha12_h = 0.04     # utility parameters -husband	leisure by  education
alpha13_h = 0.1058	     # utility parameters -husband	leisure by health
alpha2 = 0.771	       # utility parameters 	utility from leisure CRRA parameter
alpha3_w_m = 0.722	   # utility parameters - wife	utility from kids when married
alpha3_w_s = 0.464	   # utility parameters - wife	utility from kids when single
alpha3_h_m = 0.326	   # utility parameters - husband	utility from kids when married
alpha3_h_s = 0.068	   # utility parameters - husband	utility from kids when single
# marriage and divorce cost
mc = -1.946	             # fixed cost of getting married
mc_by_parents = -12.691	 # cost of marriage by parents marital status
dc_w = -10.579	           # fixed cost of divorce wife	alpha4
dc_h = -10.691	           # fixed cost of divorce husband	alpha4
dc_w_kids = -100.372	     # fixed cost of divorce child wife	alpha4
dc_h_kids = -100.260	     # fixed cost of divorce child husband	alpha4
tau0_w = 0.0	 # Home Time Equation - wife	constant
tau1_w = 0.842	 # home time equation - wife	ar coefficient
tau2_w = 1.493	 # home time equation - wife	pregnancy in previous period
tau0_h = 0.0	 # home time equation - husband	constant
tau1_h = 0.691	 # home time equation - husband	ar coefficient
tau2_h = 0.454	 # home time equation - husband	pregnancy in previous period
#  ability parameters
ab_high1 = -0.918	     # ability parameters - high	ability constant
ab_high2 = 1.211 	     # ability parameters - high	ability parents education
ab_high3 = 0.413	     # ability parameters - high	ability parents married
ab_medium1 = -0.460	   # ability parameters - medium	ability constant
ab_medium2 = 0.399	   # ability parameters - medium	ability parents education
ab_medium3 = 0.272	   # ability parameters - medium	ability parents married
# error terms variance
sigma_ability_w = np.exp(-0.549)	 # random shock variance matrix	variance wife ability
sigma_ability_h = np.exp(-0.592)	 # random shock variance matrix	variance husband ability
sigma_hp_w = np.exp(-1.426) 	     # random shock variance matrix	variance home time wife
sigma_hp_h = np.exp(-1.312)	       # random shock variance matrix	variance home time husband
sigma_w_wage = np.exp(-0.620) 	   # random shock variance matrix	wife's wage error variance
sigma_h_wage = np.exp(-0.624) 	   # random shock variance matrix	husband's wage error variance
sigma_q = np.exp(-0.822)	         # random shock variance matrix	match quality variance
sigma_p = np.exp(-0.225)	         # random shock variance matrix	pregnancy
# utility from schooling parameters
s1_w = 550.432	   # utility from schooling - wife	s1_w constant
s2_w = 132.469	   # utility from schooling - wife	s2_w mother is CG
s3_w = 116.674	   # utility from schooling - wife	s3_w return for ability
s4_w = -20.429	 # utility from schooling - wife+husband	s4_w post high school tuition
s1_h = 350.375	   # utility from schooling - husband	s1_h constant
s2_h = 112.582	   # utility from schooling - husband	s2_h mother is  CG
s3_h = 16.719	   # utility from schooling - husband	s3_h return for ability
# terminal value parameters
t1_w = 10.918	 # terminal value - wife:	wife Education - HSG
t2_w = 30.462	 # terminal value - wife:	wife Education - SC
t3_w = 35.885	 # terminal value - wife:	wife Education - CG
t4_w = 57.247	 # terminal value - wife:	wife Education - PC
t5_w = 21.278	 # terminal value - wife:	wife experience
t6_w = 8.210 	 # terminal value - wife: husband education - HSG
t7_w = 13.216	 # terminal value - wife:	husband education - SC
t8_w = 58.130	 # terminal value - wife:	husband education - CG
t9_w = 61.873	 # terminal value - wife:	husband education - PC
t10_w = 16.833	 # terminal value - wife:	husband experience
t11_w = 112.743	 # terminal value - wife:	marriage utility
t1_h = 26.942	 # terminal value - husband: wife Education - HSG
t2_h = 35.655	 # terminal value - husband: wife Education - SC
t3_h = 39.843	 # terminal value - husband: wife Education - CG
t4_h = 58.215	 # terminal value - husband: wife Education - PC
t5_h = 5.222	   # terminal value - husband: wife	experience
t6_h = 17.880	 # terminal value - husband: husband education - HSG
t7_h = 20.516	 # terminal value - husband: husband education - SC
t8_h = 23.348	 # terminal value - husband: husband education - CG
t9_h = 27.876	 # terminal value - husband: husband education - PC
t10_h = 7.660	   # terminal value - husband: husband experience
t11_h = 70.536	 # terminal value - husband: marriage utility
