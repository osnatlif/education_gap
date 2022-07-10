# marriage market parameters
cdef double omega3       # probability of meeting a husband if above 18 not in school
cdef double omega4_w     # women's age
cdef double omega5_w     # women's age*age
cdef double omega4_h     # men's age
cdef double omega5_h     # men's age*age
cdef double omega6_w     # women's probability of meeting a  CG - CONSTANT
cdef double omega7_w     # women's women's probability of meeting a  CG if she SC
cdef double omega8_w     # women's probability of meeting a  CG if she HS
cdef double omega9_w     # women's probability of meeting a  SC - CONSTANT
cdef double omega10_w    # women's probability of meeting a  SC if she HS
cdef double omega6_h     # men's probability of meeting a  CG - CONSTANT
cdef double omega7_h     # men's probability of meeting a  CG if he SC
cdef double omega8_h     # men's probability of meeting a  CG if he HS
cdef double omega9_h     # men's probability of meeting a  SC - CONSTANT
cdef double omega10_h    # men's probability of meeting a  SC if he HS
# wage parameters wife
cdef double beta11_w 	   # experience HSD
cdef double beta12_w 	   # experience HSG
cdef double beta13_w 	   # experience SC
cdef double beta14_w 	   # experience CG
cdef double beta15_w 	   # experience PC
cdef double beta21_w 	   # exp^2 HSD
cdef double beta22_w 	   # exp^2 HSG
cdef double beta23_w 	   # exp^2 SC
cdef double beta24_w 	   # exp^2 CG
cdef double beta25_w 	   # exp^2 PC
cdef double beta31_w 	   # HSD
cdef double beta32_w 	   # HSG
cdef double beta33_w 	   # SC
cdef double beta34_w 	   # CG
cdef double beta35_w 	   # PC
# wage parameters husband
cdef double beta11_h 	   # experience HSD
cdef double beta12_h 	   # experience HSG
cdef double beta13_h 	   # experience SC
cdef double beta14_h 	   # experience CG
cdef double beta15_h 	   # experience PC
cdef double beta21_h 	   # exp^2 HSD
cdef double beta22_h 	   # exp^2 HSG
cdef double beta23_h 	   # exp^2 SC
cdef double beta24_h 	   # exp^2 CG
cdef double beta25_h 	   # exp^2 PC
cdef double beta31_h 	   # hsd
cdef double beta32_h     # hsg
cdef double beta33_h 	   # sc
cdef double beta34_h 	   # cg
cdef double beta35_h 	   # pc
# job offer parameters - full time
cdef double lambda0_w_ft 	  # job offer parameters - wife - full time	constant
cdef double lambda1_w_ft 	  # job offer parameters - wife	experience
cdef double lambda21_w_ft	  # job offer parameters - wife	HSG
cdef double lambda22_w_ft	  # job offer parameters - wife	SC
cdef double lambda23_w_ft	  # job offer parameters - wife	CG
cdef double lambda24_w_ft 	# job offer parameters - wife	PC
cdef double lambda0_h_ft 	  # job offer parameters - husband - full Time	constant
cdef double lambda1_h_ft 	  # job offer parameters - husband	experience
cdef double lambda21_h_ft 	# job offer parameters - husband	education
cdef double lambda22_h_ft 	# job offer parameters - husband	education
cdef double lambda23_h_ft 	# job offer parameters - husband	education
cdef double lambda24_h_ft 	# job offer parameters - husband	education
# job offer parameters - part-time
cdef double lambda0_w_pt 	  # job offer parameters - wife - part-time	constant
cdef double lambda1_w_pt 	  # job offer parameters - wife	experience
cdef double lambda21_w_pt	  # job offer parameters - wife	education
cdef double lambda22_w_pt 	# job offer parameters - wife	education
cdef double lambda23_w_pt 	# job offer parameters - wife	education
cdef double lambda24_w_pt 	# job offer parameters - wife	education

cdef double lambda0_h_pt 	  # job offer parameters - husband  - part-time	constant
cdef double lambda1_h_pt 	  # job offer parameters - husband	experience
cdef double lambda21_h_pt 	# job offer parameters - husband	education
cdef double lambda22_h_pt 	# job offer parameters - husband	education
cdef double lambda23_h_pt 	# job offer parameters - husband	education
cdef double lambda24_h_pt 	# job offer parameters - husband	education
# get fired
cdef double lambda0_w_f 	  # job offer parameters - wife - fired  ( PT FT)	constant
cdef double lambda1_w_f 	  # job offer parameters - wife	experience
cdef double lambda21_w_f 	  # job offer parameters - wife	education
cdef double lambda22_w_f 	  # job offer parameters - wife	education
cdef double lambda23_w_f 	  # job offer parameters - wife	education
cdef double lambda24_w_f 	  # job offer parameters - wife	education

cdef double lambda0_h_f 	  # job offer parameters - husband - fired (PT FT)	constant
cdef double lambda1_h_f 	  # job offer parameters - husband	experience
cdef double lambda21_h_f 	  # job offer parameters - husband	education
cdef double lambda22_h_f 	  # job offer parameters - husband	education
cdef double lambda23_h_f 	  # job offer parameters - husband	education
cdef double lambda24_h_f 	  # job offer parameters - husband	education
##############################################################################
# fixed parameters
##############################################################################
cdef double omega_1 	        # probability of meeting a husband if below 18
cdef double omega_2 	        # probability of meeting a husband if above 18 but in school
cdef double taste_c 	        # taste for marriage	constant
cdef double taste_w_up   	    # taste for marriage	schooling gap - men more educated
cdef double taste_w_down 	    # taste for marriage	schooling gap - women more educated
cdef double taste_health      # taste for marriage	health gap
cdef double preg_health       # utility from pregnancy - health
cdef double preg_unmarried 	  # utility from pregnancy -	married
cdef double preg_t_minus1     # utility from pregnancy - pregnancy in t-1
cdef double preg_kids         # utility from pregnancy - number of kide
# utility from quality and quantity of children
cdef double row0 	            # utility from quality and quantity of children	CES function's parameter
cdef double row1_w 	          # utility from quality and quantity of children	wife leisure
cdef double row1_h 	          # utility from quality and quantity of children	husband leisure
cdef double row2  	          # utility from quality and quantity of children	spending per child
# welfare parameters
cdef double stigma 	          # disutility from welfare
cdef double stigma96 	        # disutility from welfare after 1996
cdef double p_alimony	        # prob of having alimony for single mothers)
cdef double alimony 	        # mean of alimony	exp of draw from normal distribution
# utility parameters
cdef double alpha0 	        # utility parameters 	CRRA consumption parameter
cdef double alpha11_w 	    # utility parameters - wife	leisure when pregnant
cdef double alpha12_w 	    # utility parameters - wife	leisure by  education
cdef double alpha13_w 	    # utility parameters - wife	leisure by health
cdef double alpha12_h       # utility parameters -husband	leisure by  education
cdef double alpha13_h 	    # utility parameters -husband	leisure by health
cdef double alpha2 	        # utility parameters 	utility from leisure CRRA parameter
cdef double alpha3_w_m 	    # utility parameters - wife	utility from kids when married
cdef double alpha3_w_s 	    # utility parameters - wife	utility from kids when single
cdef double alpha3_h_m 	    # utility parameters - husband	utility from kids when married
cdef double alpha3_h_s 	    # utility parameters - husband	utility from kids when single
# marriage and divorce cost
cdef double mc 	             # fixed cost of getting married
cdef double mc_by_parents 	 # cost of marriage by parents marital status
cdef double dc_w 	           # fixed cost of divorce wife	alpha4
cdef double dc_h 	           # fixed cost of divorce husband	alpha4
cdef double dc_w_kids 	     # fixed cost of divorce child wife	alpha4
cdef double dc_h_kids 	     # fixed cost of divorce child husband	alpha4
cdef double tau0_w 	         # Home Time Equation - wife	constant
cdef double tau1_w 	         # home time equation - wife	ar coefficient
cdef double tau2_w 	         # home time equation - wife	pregnancy in previous period
cdef double tau0_h 	         # home time equation - husband	constant
cdef double tau1_h 	         # home time equation - husband	ar coefficient
cdef double tau2_h 	         # home time equation - husband	pregnancy in previous period
#  ability parameters
cdef double ab_high1 	     # ability parameters - high	ability constant
cdef double ab_high2 	     # ability parameters - high	ability parents education
cdef double ab_high3 	     # ability parameters - high	ability parents married
cdef double ab_medium1 	   # ability parameters - medium	ability constant
cdef double ab_medium2 	   # ability parameters - medium	ability parents education
cdef double ab_medium3 	   # ability parameters - medium	ability parents married
# error terms variance
cdef double sigma_ability_w 	 # random shock variance matrix	variance wife ability
cdef double sigma_ability_h 	 # random shock variance matrix	variance husband ability
cdef double sigma_hp_w  	     # random shock variance matrix	variance home time wife
cdef double sigma_hp_h 	       # random shock variance matrix	variance home time husband
cdef double sigma_w_wage  	   # random shock variance matrix	wife's wage error variance
cdef double sigma_h_wage  	   # random shock variance matrix	husband's wage error variance
cdef double sigma_q 	         # random shock variance matrix	match quality variance
cdef double sigma_p 	         # random shock variance matrix	pregnancy
# utility from schooling parameters
cdef double s1_w 	   # utility from schooling - wife	s1_w constant
cdef double s2_w 	   # utility from schooling - wife	s2_w mother is CG
cdef double s3_w 	   # utility from schooling - wife	s3_w return for ability
cdef double s4_w 	   # utility from schooling - wife+husband	s4_w post high school tuition
cdef double s1_h 	   # utility from schooling - husband	s1_h constant
cdef double s2_h 	   # utility from schooling - husband	s2_h mother is  CG
cdef double s3_h 	   # utility from schooling - husband	s3_h return for ability
# terminal value parameters
cdef double t1_w 	   # terminal value - wife:	wife Education - HSG
cdef double t2_w 	   # terminal value - wife:	wife Education - SC
cdef double t3_w 	   # terminal value - wife:	wife Education - CG
cdef double t4_w 	   # terminal value - wife:	wife Education - PC
cdef double t5_w 	   # terminal value - wife:	wife experience
cdef double t6_w  	 # terminal value - wife: husband education - HSG
cdef double t7_w 	   # terminal value - wife:	husband education - SC
cdef double t8_w 	   # terminal value - wife:	husband education - CG
cdef double t9_w 	   # terminal value - wife:	husband education - PC
cdef double t10_w	   # terminal value - wife:	husband experience
cdef double t11_w	   # terminal value - wife:	marriage utility
cdef double t1_h 	   # terminal value - husband: wife Education - HSG
cdef double t2_h 	   # terminal value - husband: wife Education - SC
cdef double t3_h 	   # terminal value - husband: wife Education - CG
cdef double t4_h 	   # terminal value - husband: wife Education - PC
cdef double t5_h     # terminal value - husband: wife	experience
cdef double t6_h 	   # terminal value - husband: husband education - HSG
cdef double t7_h 	   # terminal value - husband: husband education - SC
cdef double t8_h 	   # terminal value - husband: husband education - CG
cdef double t9_h 	   # terminal value - husband: husband education - PC
cdef double t10_h 	 # terminal value - husband: husband experience
cdef double t11_h    # terminal value - husband: marriage utility
