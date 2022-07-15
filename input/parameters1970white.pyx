import numpy as np
# marriage market parameters
cdef double omega3 = -1.345     # probability of meeting a husband if above 18 not in school
cdef double omega4_w = 0.114    # women's age
cdef double omega5_w = -0.004   # women's age*age
cdef double omega4_h = 0.1      # men's age
cdef double omega5_h = -0.003   # men's age*age
cdef double omega6_w = 1.67     # women's probability of meeting a  CG - CONSTANT
cdef double omega7_w = -1.257   # women's women's probability of meeting a  CG if she SC
cdef double omega8_w = -4.054   # women's probability of meeting a  CG if she HS
cdef double omega9_w = 0.684    # women's probability of meeting a  SC - CONSTANT
cdef double omega10_w = -1.989  # women's probability of meeting a  SC if she HS
cdef double omega6_h = 1.358    # men's probability of meeting a  CG - CONSTANT
cdef double omega7_h = -1.053   # men's probability of meeting a  CG if he SC
cdef double omega8_h = -2.126   # men's probability of meeting a  CG if he HS
cdef double omega9_h = 0.265    # men's probability of meeting a  SC - CONSTANT
cdef double omega10_h = -1.356  # men's probability of meeting a  SC if he HS
# wage parameters wife
cdef double beta11_w = 0.029	    # experience HSD
cdef double beta12_w = 0.054	    # experience HSG
cdef double beta13_w = 0.060	    # experience SC
cdef double beta14_w = 0.074	    # experience CG
cdef double beta15_w = 0.078	    # experience PC
cdef double beta21_w = -0.0001	  # exp^2 HSD
cdef double beta22_w = -0.0001	  # exp^2 HSG
cdef double beta23_w = -0.0001	  # exp^2 SC
cdef double beta24_w = -0.0002	  # exp^2 CG
cdef double beta25_w = -0.0002	  # exp^2 PC
cdef double beta31_w = 9.657	    # HSD
cdef double beta32_w = 9.783	    # HSG
cdef double beta33_w = 9.974	    # SC
cdef double beta34_w = 10.294	    # CG
cdef double beta35_w = 10.475	    # PC
# wage parameters husband
cdef double beta11_h = 0.045	   # experience HSD
cdef double beta12_h = 0.072	   # experience HSG
cdef double beta13_h = 0.081	   # experience SC
cdef double beta14_h = 0.090	   # experience CG
cdef double beta15_h = 0.099	   # experience PC
cdef double beta21_h = -0.0001	 # exp^2 HSD
cdef double beta22_h = -0.0001	 # exp^2 HSG
cdef double beta23_h = -0.0002	 # exp^2 SC
cdef double beta24_h = -0.0002	 # exp^2 CG
cdef double beta25_h = -0.0002	 # exp^2 PC
cdef double beta31_h = 9.877	   # hsd
cdef double beta32_h = 9.939     # hsg
cdef double beta33_h = 10.180	   # sc
cdef double beta34_h = 10.464	   # cg
cdef double beta35_h = 10.635	   # pc
# job offer parameters - full time
cdef double lambda0_w_ft = -0.57	  # job offer parameters - wife - full time	constant
cdef double lambda1_w_ft = 0.06	  # job offer parameters - wife	experience
cdef double lambda21_w_ft = 0.11	  # job offer parameters - wife	HSG
cdef double lambda22_w_ft = 0.11	  # job offer parameters - wife	SC
cdef double lambda23_w_ft = 0.11	  # job offer parameters - wife	CG
cdef double lambda24_w_ft = 0.11	  # job offer parameters - wife	PC
cdef double lambda0_h_ft = -0.32	  # job offer parameters - husband - full Time	constant
cdef double lambda1_h_ft = 0.10	    # job offer parameters - husband	experience
cdef double lambda21_h_ft = 0.16	  # job offer parameters - husband	education
cdef double lambda22_h_ft = 0.16	  # job offer parameters - husband	education
cdef double lambda23_h_ft = 0.16	  # job offer parameters - husband	education
cdef double lambda24_h_ft = 0.16	  # job offer parameters - husband	education
# job offer parameters - part-time
cdef double lambda0_w_pt = -1.52	  # job offer parameters - wife - part-time	constant
cdef double lambda1_w_pt = 0.01	  # job offer parameters - wife	experience
cdef double lambda21_w_pt = 0.06	  # job offer parameters - wife	education
cdef double lambda22_w_pt = 0.06	  # job offer parameters - wife	education
cdef double lambda23_w_pt = 0.06	  # job offer parameters - wife	education
cdef double lambda24_w_pt = 0.06	  # job offer parameters - wife	education

cdef double lambda0_h_pt = -1.93	  # job offer parameters - husband  - part-time	constant
cdef double lambda1_h_pt = 0.01	  # job offer parameters - husband	experience
cdef double lambda21_h_pt = 0.00	  # job offer parameters - husband	education
cdef double lambda22_h_pt = 0.00	  # job offer parameters - husband	education
cdef double lambda23_h_pt = 0.00	  # job offer parameters - husband	education
cdef double lambda24_h_pt = 0.00	  # job offer parameters - husband	education
# get fired
cdef double lambda0_w_f = 0.99	    # job offer parameters - wife - fired  ( PT FT)	constant
cdef double lambda1_w_f = 0.19	    # job offer parameters - wife	experience
cdef double lambda21_w_f = 0.11	  # job offer parameters - wife	education
cdef double lambda22_w_f = 0.11	  # job offer parameters - wife	education
cdef double lambda23_w_f = 0.11	  # job offer parameters - wife	education
cdef double lambda24_w_f = 0.11	  # job offer parameters - wife	education

cdef double lambda0_h_f = 1.11	    # job offer parameters - husband - fired (PT FT)	constant
cdef double lambda1_h_f = 0.27	    # job offer parameters - husband	experience
cdef double lambda21_h_f = 0.09	  # job offer parameters - husband	education
cdef double lambda22_h_f = 0.09	  # job offer parameters - husband	education
cdef double lambda23_h_f = 0.09	  # job offer parameters - husband	education
cdef double lambda24_h_f = 0.09	  # job offer parameters - husband	education
##############################################################################
# fixed parameters
##############################################################################
cdef double omega_1 = -1.867	       # probability of meeting a husband if below 18
cdef double omega_2 = -1.329	       # probability of meeting a husband if above 18 but in school
cdef double taste_c = 1.485	         # taste for marriage	constant
cdef double taste_w_up = -1.894  	 # taste for marriage	schooling gap - men more educated
cdef double taste_w_down = -2.227	 # taste for marriage	schooling gap - women more educated
cdef double taste_health = 0         # taste for marriage	health gap
cdef double preg_health = 0.0002     # utility from pregnancy - health
cdef double preg_unmarried = -22.429	   # utility from pregnancy -	married
cdef double preg_t_minus1 = -19.227   # utility from pregnancy - pregnancy in t-1
cdef double preg_kids = -13.98       # utility from pregnancy - number of kide
# utility from quality and quantity of children
cdef double row0 = -0.869	        # utility from quality and quantity of children	CES function's parameter
cdef double row1_w = 0.413	        # utility from quality and quantity of children	wife leisure
cdef double row1_h = 0.350	        # utility from quality and quantity of children	husband leisure
cdef double row2 = 0.003	          # utility from quality and quantity of children	spending per child
# welfare parameters
cdef double stigma = -44.742	      # disutility from welfare
cdef double stigma96 = -61.543	    # disutility from welfare after 1996
cdef double p_alimony = np.exp(-0.483)/(1+np.exp(-0.483))	    # prob of having alimony for single mothers)
cdef double alimony = np.exp(8.689)	        # mean of alimony	exp of draw from normal distribution
# utility parameters
cdef double alpha0 = 0.462	       # utility parameters 	CRRA consumption parameter
cdef double alpha11_w = 0.492	     # utility parameters - wife	leisure when pregnant
cdef double alpha12_w = 0.078	     # utility parameters - wife	leisure by  education
cdef double alpha13_w = 0.157	     # utility parameters - wife	leisure by health
cdef double alpha12_h = 0.004     # utility parameters -husband	leisure by  education
cdef double alpha13_h = 0.058	     # utility parameters -husband	leisure by health
cdef double alpha2 = 0.771	       # utility parameters 	utility from leisure CRRA parameter
cdef double alpha3_w_m = 0.722	   # utility parameters - wife	utility from kids when married
cdef double alpha3_w_s = 0.464	   # utility parameters - wife	utility from kids when single
cdef double alpha3_h_m = 0.326	   # utility parameters - husband	utility from kids when married
cdef double alpha3_h_s = 0.068	   # utility parameters - husband	utility from kids when single
# marriage and divorce cost
cdef double mc = -1.946	             # fixed cost of getting married
cdef double mc_by_parents = -12.691	 # cost of marriage by parents marital status
cdef double dc_w = -10.579	           # fixed cost of divorce wife	alpha4
cdef double dc_h = -10.691	           # fixed cost of divorce husband	alpha4
cdef double dc_w_kids = -100.372	     # fixed cost of divorce child wife	alpha4
cdef double dc_h_kids = -100.260	     # fixed cost of divorce child husband	alpha4
cdef double tau0_w = 0.0	 # Home Time Equation - wife	constant
cdef double tau1_w = 0.842	 # home time equation - wife	ar coefficient
cdef double tau2_w = 1.493	 # home time equation - wife	pregnancy in previous period
cdef double tau0_h = 0.0	 # home time equation - husband	constant
cdef double tau1_h = 0.691	 # home time equation - husband	ar coefficient
cdef double tau2_h = 0.454	 # home time equation - husband	pregnancy in previous period
#  ability parameters
cdef double ab_high1 = -0.918	     # ability parameters - high	ability constant
cdef double ab_high2 = 1.211 	     # ability parameters - high	ability parents education
cdef double ab_high3 = 0.413	     # ability parameters - high	ability parents married
cdef double ab_medium1 = -0.460	   # ability parameters - medium	ability constant
cdef double ab_medium2 = 0.399	   # ability parameters - medium	ability parents education
cdef double ab_medium3 = 0.272	   # ability parameters - medium	ability parents married
# error terms variance
cdef double sigma_ability_w = np.exp(-0.549)	 # random shock variance matrix	variance wife ability
cdef double sigma_ability_h = np.exp(-0.592)	 # random shock variance matrix	variance husband ability
cdef double sigma_hp_w = np.exp(-1.426) 	     # random shock variance matrix	variance home time wife
cdef double sigma_hp_h = np.exp(-1.312)	       # random shock variance matrix	variance home time husband
cdef double sigma_w_wage = np.exp(-0.620) 	   # random shock variance matrix	wife's wage error variance
cdef double sigma_h_wage = np.exp(-0.624) 	   # random shock variance matrix	husband's wage error variance
cdef double sigma_q = np.exp(-0.822)	         # random shock variance matrix	match quality variance
cdef double sigma_p = np.exp(-0.225)	         # random shock variance matrix	pregnancy
# utility from schooling parameters
cdef double s1_w = 550.432	   # utility from schooling - wife	s1_w constant
cdef double s2_w = 132.469	   # utility from schooling - wife	s2_w mother is CG
cdef double s3_w = 116.674	   # utility from schooling - wife	s3_w return for ability
cdef double s4_w = -20.429	 # utility from schooling - wife+husband	s4_w post high school tuition
cdef double s1_h = 350.375	   # utility from schooling - husband	s1_h constant
cdef double s2_h = 112.582	   # utility from schooling - husband	s2_h mother is  CG
cdef double s3_h = 16.719	   # utility from schooling - husband	s3_h return for ability
# terminal value parameters
cdef double t1_w = 10.918	 # terminal value - wife:	wife Education - HSG
cdef double t2_w = 30.462	 # terminal value - wife:	wife Education - SC
cdef double t3_w = 35.885	 # terminal value - wife:	wife Education - CG
cdef double t4_w = 57.247	 # terminal value - wife:	wife Education - PC
cdef double t5_w = 21.278	 # terminal value - wife:	wife experience
cdef double t6_w = 8.210 	 # terminal value - wife: husband education - HSG
cdef double t7_w = 13.216	 # terminal value - wife:	husband education - SC
cdef double t8_w = 58.130	 # terminal value - wife:	husband education - CG
cdef double t9_w = 61.873	 # terminal value - wife:	husband education - PC
cdef double t10_w = 16.833	 # terminal value - wife:	husband experience
cdef double t11_w = 112.743	 # terminal value - wife:	marriage utility
cdef double t1_h = 26.942	 # terminal value - husband: wife Education - HSG
cdef double t2_h = 35.655	 # terminal value - husband: wife Education - SC
cdef double t3_h = 39.843	 # terminal value - husband: wife Education - CG
cdef double t4_h = 58.215	 # terminal value - husband: wife Education - PC
cdef double t5_h = 5.222	   # terminal value - husband: wife	experience
cdef double t6_h = 17.880	 # terminal value - husband: husband education - HSG
cdef double t7_h = 20.516	 # terminal value - husband: husband education - SC
cdef double t8_h = 23.348	 # terminal value - husband: husband education - CG
cdef double t9_h = 27.876	 # terminal value - husband: husband education - PC
cdef double t10_h = 7.660	   # terminal value - husband: husband experience
cdef double t11_h = 70.536	 # terminal value - husband: marriage utility
