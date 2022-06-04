import numpy as np
import constant_parameters as c


ded_and_ex = np.loadtxt("deductions_exemptions.out")
tax_brackets = np.loadtxt("tax_brackets.out")


class NetIncome:
  def __init__(self):
    self.net_income_s_h = 0
    self.net_income_s_w = 0
    self.net_income_m = 0
    self.net_income_m_unemp = 0

  def __str__(self):
    return "Net Income:\n\tSingle Husband: " + str(self.net_income_s_h) + \
           "\n\tSingle Wife: " + str(self.net_income_s_w) + \
           "\n\tMarried: " + str(self.net_income_m) + \
           "\n\tMarried Unemployed: " + str(self.net_income_m_unemp)


# tax matrix
# -----+--------------------------------------------------------------------------------------------------------------------------------------------------+---------
#      | single                                                                                                                                           | married
# -----+-----------------------------------------+--------------------------------------------------------------------------------------------------------+---------
# year | br1 | br2 | br3 | br4 | br5 | br6 | br7 | br8 | br9 | br10 | br11 | %br1 | %br2 | %br3 | %br4 | %br5 | %br6 | %br7 | %br8 | %br9 | %br10 | %br11 | ...
# ---+--------------------------------------------------------------------------------------------------------------------------------------------------+---------

TAX_PERCENT_OFFSET = 11

# deduction matrix
# -----+-------------------------------------------------------------+--------------------------------------------+--------------------------------------------+--------
#      |                                                             | 0 kids                                     | 1 kid                                      | 2 kids
# -----+-------------------------------------------------------------+--------------------------------------------+--------------------------------------------+--------
# year | ded married | ded single | ex married | ex single | ex kids | int1% | int1 | int2% | int3% | int2 | int3 | int1% | int1 | int2% | int3% | int2 | int3 | ...
# -----+-------------------------------------------------------------+--------------------------------------------+--------------------------------------------+--------

DED_OFFSET = 6
DED_KIDS_OFFSET = 6
DED_INTERVAL1_OFFSET = DED_OFFSET + 1
DED_INTERVAL2_OFFSET = DED_OFFSET + 4
DED_INTERVAL3_OFFSET = DED_OFFSET + 5


def calculate_tax(reduced_income, row_number):
  tax = 0.0
  if reduced_income > 0:
    for i in range(2, 12):
      lower_bracket = tax_brackets[row_number][i-1]
      upper_bracket = tax_brackets[row_number][i]
      percent = tax_brackets[row_number][i-1+TAX_PERCENT_OFFSET]
      if reduced_income <= upper_bracket:
        tax += (reduced_income - lower_bracket)*percent
        break
      tax += (upper_bracket - lower_bracket)*percent
  return tax


def calculate_eict(wage, year_row, kids):
  EICT = 0.0
  kids_offset = DED_KIDS_OFFSET*kids
  offset1 = DED_INTERVAL1_OFFSET+kids_offset
  offset2 = DED_INTERVAL2_OFFSET+kids_offset
  offset3 = DED_INTERVAL3_OFFSET+kids_offset
  if wage < ded_and_ex[year_row][offset1]:
    # first interval  credit rate
    EICT = wage*ded_and_ex[year_row][offset1-1]
  elif wage < ded_and_ex[year_row][offset2]:
    # second (flat) interval - max EICT
    EICT = ded_and_ex[year_row][offset2-1]
  elif wage < ded_and_ex[year_row][offset3]:
    EICT = wage*ded_and_ex[year_row][offset3-2]

  return EICT


# similar handling for husband and wife in case of singles
def gross_to_net_single( year_row,  kids,  wage,  exemptions,  deductions):
  tax = 0.0
  if wage > 0.0:
    reduced_income = wage - deductions - exemptions
    EICT = calculate_eict(wage, year_row, kids)
    if EICT == 0.0:
      tax = calculate_tax(reduced_income, year_row)
    return wage - tax + EICT
  return 0.0


def gross_to_net_married( year_row,  kids,  wage_h,  wage_w,  exemptions,  deductions):
  tax = 0.0
  if wage_h > 0.0:
    reduced_income = wage_h + wage_w - deductions - exemptions
    tot_income = wage_h + wage_w
    EICT = calculate_eict(tot_income, year_row, kids)
    if EICT == 0.0:
      tax = calculate_tax(reduced_income, year_row)
    return tot_income - tax + EICT
  return 0.0


def gross_to_net(kids, wage_w, wage_h, year_row):
  # the tax brackets and the deductions and exemptions starts at 1950 and ends at 2050.
  # 1960 cohort - turns 16 at 1976 row 27, 1970 cohort row 37, 1980 cohort row 47
  deductions_m = ded_and_ex[year_row][1]
  deductions_s = ded_and_ex[year_row][2]
  exemptions_m = ded_and_ex[year_row][3] + ded_and_ex[year_row][5] * kids
  exemptions_s_w = ded_and_ex[year_row][4] + ded_and_ex[year_row][5] * kids
  exemptions_s_h = ded_and_ex[year_row][4]
  result = NetIncome()
  # CALCULATE NET INCOME FOR SINGLE WOMEN
  result.net_income_s_w = gross_to_net_single(year_row, kids, wage_w, exemptions_s_w, deductions_s)
  # CALCULATE NET INCOME FOR SINGLE MEN
  result.net_income_s_h = gross_to_net_single(year_row, c.NO_KIDS, wage_h, exemptions_s_h, deductions_s)
  # CALCULATE NET INCOME FOR MARRIED COUPLE
  result.net_income_m = gross_to_net_married(year_row, kids, wage_h, wage_w, exemptions_m, deductions_m)
  result.net_income_m_unemp = gross_to_net_married(year_row, kids, wage_h, 0, exemptions_m, deductions_m)

  return result
