# convert values to indexes on their respective grids

cpdef int home_time_to_index(double home_time):
    if home_time < 0:
        return 0
    elif home_time > 0:
        return 2
    else:
        return 1

cpdef int exp_to_index(double exp):   # levels grid: 0, 1-2, 3-4, 5-10, 11+
    if exp == 0:
        return 0
    elif exp < 3:  # 1 or 2 years
        return 1
    elif exp < 6:  # 3 or 5 years
        return 2
    elif exp < 11:  # 6 to 10 years
        return 3
    else:    # above 11 years of experience
        return 4

cpdef int schooly_to_index(int years_of_schooling):   # levels grid: 0, 1-2, 3-4, 5-10, 11+
    if years_of_schooling == 12:
        return 1    #hsg
    elif years_of_schooling < 15:  # 1 or 2 years
        return 2   # sc
    elif years_of_schooling < 18:  # 3 or 5 years
        return 3   # cg
    else:
        return 4  # pc