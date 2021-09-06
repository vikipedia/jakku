def tax(taxable_income):
    if taxable_income <= 250000:
        return 0
    elif taxable_income <= 500000:
        return (taxable_income - 250000)*0.05
    elif taxable_income <= 1000000:
        return 12500 + (taxable_income - 500000)*0.2
    else:
        return 112500 + (taxable_income - 1000000)*0.3


def my_deductions():
    return 168999


def house_rent_and_interest_less_deductions():
    return 150000


def my_business_head():
    return 540000 + 270000


def salary():
    return 300000


def my_taxble_income():
    return my_business_head()/2 + house_rent_and_interest_less_deductions() - my_deductions()
