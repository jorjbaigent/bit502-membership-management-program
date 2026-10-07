#------------------------------------------
#BIT502 Assessment 3, Jorj Baigent, 5132617
#------------------------------------------

"""Shared membership pricing and payment calculations"""

#------------------------------------------
#IMPORTS
#------------------------------------------
from member_options import (
    EXTRAS,
    LIBRARY_CARD_DISCOUNT,
    MEMBERSHIP_PRICES,
    PLAN_ANNUAL
)

#------------------------------------------
#CALCULATION FUNCTIONS
#------------------------------------------

#Gets the selected membership plan cost
def get_membership_cost(selected_plan):
    return MEMBERSHIP_PRICES[selected_plan]


#Gets a list of extras selected and calculates the cost for them
def calculate_extras_cost(selected_extras):
    extras_selected = [name for name, selected in selected_extras.items() if selected]

    return sum(EXTRAS[name] for name in extras_selected), extras_selected


#Calculates and applies library discount
def calculate_library_discount(monthly_price, has_library_card):
    return monthly_price * LIBRARY_CARD_DISCOUNT if has_library_card else 0


#Calculates and applies annual discount
def calculate_annual_discount(membership_cost, has_library_card, payment_plan):
    if payment_plan != PLAN_ANNUAL:
        return 0

    discounted_membership = membership_cost

    if has_library_card:
        discounted_membership *= 1 - LIBRARY_CARD_DISCOUNT
    return discounted_membership / 12


#Calculates and returns totals
def calculate_totals(membership_cost, extras_cost, library_discount, annual_discount, payment_plan):
    monthly_cost = membership_cost + extras_cost
    total_discount = library_discount + annual_discount
    monthly_total = monthly_cost - total_discount

    if payment_plan == PLAN_ANNUAL:
        annual_total = monthly_total * 12
        return monthly_total, total_discount, annual_total, annual_total / 52, "yearly"
    return monthly_total, total_discount, monthly_total, monthly_total / 4, "monthly"