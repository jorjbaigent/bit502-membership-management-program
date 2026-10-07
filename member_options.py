#------------------------------------------
#BIT502 Assessment 3, Jorj Baigent, 5132617
#------------------------------------------
"""Shared membership options used by registration and search screens."""

#Membership plans
PLAN_STANDARD = "Standard"
PLAN_PREMIUM = "Premium"
PLAN_KIDS = "Kids"

#Payment types
PLAN_MONTHLY = "Monthly"
PLAN_ANNUAL = "Annual"


MEMBERSHIP_PLANS = (PLAN_STANDARD, PLAN_PREMIUM, PLAN_KIDS)
PAYMENT_PLANS = (PLAN_MONTHLY, PLAN_ANNUAL)

#Membership prices
MEMBERSHIP_PRICES = {
    PLAN_STANDARD: 10,
    PLAN_PREMIUM: 15,
    PLAN_KIDS: 5,
}

#Optional Extras names and prices
EXTRAS = {
    "Book Rental": 5,
    "Private Area Access": 15,
    "Monthly Booklet": 2,
    "Online ebook Rental": 5,
}

#Library card discount
LIBRARY_CARD_DISCOUNT = 0.10
