

def calculate_intrest(principal_amount, interest_rate):
    intrest = (principal_amount*1*interest_rate)/100
    return intrest


def percentage_npl_amountlent(npl_amount, amount_lent):
    npl_percentage = (npl_amount/amount_lent)*100

    return round(npl_percentage, 2)

def pl(amount_borrowed, amount_paid):
    if amount_borrowed==amount_paid:
        pl = 0.0
        return pl
    else:
        if amount_paid > amount_borrowed:
            pl = amount_paid - amount_borrowed
            return pl
        else:
            pl = amount_paid - amount_borrowed
            return pl

def percentage_pl_amountlent(pl, amount_lent):
    pl_percentage = (pl/amount_lent)*100

    return round(pl_percentage)
    