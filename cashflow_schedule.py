from assumptions import purchase_price, debt_percentage, interest_rate, amortization_rate

def debt_schedule():
    opening_debt = purchase_price * debt_percentage
    schedule = []

    for year in range(1, 6):
        interest = opening_debt * interest_rate
        principal_payment = opening_debt * amortization_rate
        ending_debt = opening_debt - principal_payment

        schedule.append({
            "year": year,
            "opening_debt": round(opening_debt, 2),
            "interest": round(interest, 2),
            "principal_payment": round(principal_payment, 2),
            "ending_debt": round(ending_debt, 2),
        })

        opening_debt = ending_debt

    return schedule

