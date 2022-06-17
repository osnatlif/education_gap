import constant_parameters as c
from draw_wife import Wife
from draw_husband import Husband
import draw_wife
import value_to_index
# single options:
#            0-singe + unemployed + non-pregnant
#		         1-singe + unemployed + pregnant - zero for men
#            2-singe + employed full  + non-pregnant
#            3-singe + employed full  + pregnant   - zero for men
#            4-singe + employed part + non-pregnant
#            5-singe + employed part + pregnant   - zero for men
#            6-schooling: single + unemployed + non-pregnant + no children


def update_wife_single(wife, single_women_index, single_women_ar):
    wife.age = wife.age + 1
    if wife.married == 1:
        wife.divorce = 1
    wife.married = 0
    wife.match = 0.0
    wife.match_i = 0
    wife.home_time_ar = single_women_ar
    if single_women_index == 6:   # choose to go to school
        wife.years_of_schooling = wife.years_of_schooling + 1
        school_group = value_to_index.schooly_to_index(wife.years_of_schooling)
        draw_wife.update_wife_schooling(school_group, wife)
    if single_women_index == 2 or single_women_index == 3:   # choose full time employment
        wife.exp = wife.exp + 1
        wife.emp = 1
        wife.capacity = 1
    elif single_women_index == 4 or single_women_index == 5:   # choose part-time employment
        wife.exp = wife.exp + 0.5
        wife.emp = 1
        wife.capacity = 0.5
    else:
        wife.emp = 0
        wife.capacity = 0
    if single_women_index == 1 or single_women_index == 3 or single_women_index == 5:   # choose to have another child
        wife.kids = min(wife.kids + 1, 3)      # wife's kids
        wife.preg = 1
    else:
        wife.preg = 0


# marriage options:# first index wife, second husband
#            0-married + women unemployed  +man unemployed     +non-pregnant
#   		     1-married + women unemployed  +man unemployed     +pregnant
#   		     2-married + women unemployed  +man employed full  +non-pregnant
#   		     3-married + women unemployed  +man employed full  +pregnant
#   		     4-married + women unemployed  +man employed part  +non-pregnant
#   		     5-married + women unemployed  +man employed part  +pregnant
#            6-married + women employed full   +man unemployed     +non-pregnant
#   		     7-married + women employed full   +man unemployed     +pregnant
#   		     8-married + women employed full   +man employed full  +non-pregnant
#   		     9-married + women employed full +man employed full  +pregnant
#   		     10-married + women employed full +man employed part  +non-pregnant
#   		     11-married + women employed full +man employed part  +pregnant
#            12-married + women employed part  +man unemployed     +non-pregnant
#   		     13-married + women employed part +man unemployed     +pregnant
#   		     14-married + women employed part +man employed full  +non-pregnant
#   		     15-married + women employed part +man employed full  +pregnant
#   		     16-married + women employed part +man employed part  +non-pregnant
#   		     17-married + women employed part  +man employed part  +pregnant

def update_married(husband, wife, married_index, home_time_h, home_time_w, home_time_h_preg, home_time_w_preg):
    men_full_index_array = [2, 3, 8, 9, 14, 15]
    men_part_index_array = [4, 5, 10, 11, 16, 17]
    men_unemployed_index_array = [0, 1, 6, 7, 12, 13]
    pregnancy_index_array = [1, 3, 5, 7, 9, 11, 13, 15, 17]
    wife.age = wife.age + 1
    husband.age = wife.age
    wife.married = 1
    wife.divorce = 0
    husband.married = 1
    # update employment status wife
    if married_index < 6:   # wife choose unemployment
        wife.emp = 0
        wife.capacity = 0
    elif married_index < 12: # wife choose full time job
        wife.emp = 1
        wife.capacity = 1
        wife.exp = wife.exp + 1
    elif married_index < 18:
        wife.emp = 1
        wife.capacity = 0.5
        wife.exp = wife.exp + 0.5
    else:
        assert()
    # update employment status husband
    if married_index in c.men_unemployed_index_array:    # men unemployed
        husband.emp = 0
        husband.capacity = 0
    elif married_index in c.men_full_index_array:    # men employed full-time
        husband.emp = 1
        husband.capacity = 1
        husband.exp = husband.exp + 1
    elif married_index in c.men_part_index_array:    # men employed part-time
        husband.emp = 1
        husband.capacity = 0.5
        husband.exp = husband.exp + 0.5
    else:
        assert ()
    # update kids, home time and pregnancy
    if married_index in c.pregnancy_index_array:   # choose to have another child
        if wife.kids + husband.kids < 3:
            wife.kids = wife.kids + husband.kids + 1     # number of children for married couple. if "just married" - add husband kids to wife
        else:
            wife.kids = 3
        husband.kids = 0    # keep number of children only at wife's object if married
        wife.preg = 1
        wife.home_time_ar = home_time_w_preg
        husband.home_time_ar = home_time_h_preg
    else:
        if wife.kids + husband.kids < 3:
            wife.kids = wife.kids + husband.kids  # number of children for married couple. if "just married" - add husband kids to wife
        else:
            wife.kids = 3
        husband.kid = 0
        wife.preg = 0
        wife.home_time_ar = home_time_w
        husband.home_time_ar = home_time_h