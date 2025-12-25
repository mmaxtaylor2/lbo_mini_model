# ==========================================================
# ADVANCED LBO MODEL (SIMPLE STACK VERSION)
# Term Loan + Revolver + Tiered Waterfall + Cash Sweep
# Taxes | CapEx | Working Capital | IRR Sensitivity
# ==========================================================

# ----------------- DEAL INPUTS -----------------
purchase_price     = 500_000_000     # Purchase Price
debt_pct           = 0.60             # % Debt
equity_pct         = 0.40             # % Equity

# ----------------- OPERATING MODEL -----------------
starting_revenue   = 200_000_000
revenue_growth     = 0.08
ebitda_margin      = 0.22

# ----------------- CASH FLOW DRIVERS -----------------
tax_rate           = 0.25             # tax on EBIT
capex_pct          = 0.03             # % of revenue
wc_pct             = 0.02             # % of revenue growth to WC
d_and_a_pct        = 0.02             # % of revenue (simple proxy)

# ----------------- DEBT STRUCTURE -----------------
interest_rate      = 0.08             # Term Loan rate
amort_rate         = 0.05             # mandatory annual amortization
cash_sweep_pct     = 0.75             # % of FCF after interest for paydown

revolver_limit     = 20_000_000
revolver_rate      = 0.06

# ----------------- EXIT -----------------
exit_multiple      = 10
holding_period     = 5

# ----------------- WATERFALL -----------------
# Tiered promote structure (tranching)
hurdle_1 = 0.12      # 12% IRR
hurdle_2 = 0.18      # 18% IRR
promote_1 = 0.10     # 10% carry in 12-18% band
promote_2 = 0.20     # 20% carry above 18%

# ----------------- MENU INPUTS -----------------
def get_inputs():
    mode = input("\nRun Base Case or Custom? (b/c): ").lower()

    if mode == "c":
        global purchase_price, debt_pct, exit_multiple, revenue_growth
        purchase_price = float(input("Purchase Price ($): "))
        debt_pct       = float(input("Debt % (0.0-1.0): "))
        exit_multiple  = float(input("Exit Multiple: "))
        revenue_growth = float(input("Revenue Growth % (0.0-1.0): "))
        print("\nCustom assumptions loaded.\n")
    else:
        print("\nRunning Base Case...\n")
# ==========================================================
#  REVENUE → EBITDA → FCF → DEBT SCHEDULE ENGINE
# ==========================================================

def project_financials():
    revenues = []
    ebitdas = []
    revenue = starting_revenue

    for _ in range(holding_period):
        revenue *= (1 + revenue_growth)
        ebitda = revenue * ebitda_margin
        revenues.append(revenue)
        ebitdas.append(ebitda)

    return revenues, ebitdas


def build_cashflows_and_debt(revenues, ebitdas):
    # initial balances
    term_loan = purchase_price * debt_pct
    revolver = 0
    
    schedule = []
    prev_rev = revenues[0] / (1 + revenue_growth)

    for year in range(1, holding_period + 1):
        revenue = revenues[year-1]
        ebitda  = ebitdas[year-1]

        # Real operational cash flow items
        d_and_a   = revenue * d_and_a_pct
        ebit      = ebitda - d_and_a
        taxes     = max(ebit, 0) * tax_rate
        capex     = revenue * capex_pct
        wc_change = (revenue - prev_rev) * wc_pct
        prev_rev  = revenue

        # Levered Free Cash Flow (pre-debt-service)
        interest_exp = term_loan * interest_rate
        levered_fcf  = ebitda - taxes - capex - wc_change - interest_exp

        # Mandatory amortization + sweep
        mandatory_pay = term_loan * amort_rate
        sweep_pay     = max(levered_fcf * cash_sweep_pct, 0)
        total_paydown = mandatory_pay + sweep_pay

        # Revolver if needed
        if levered_fcf < 0:
            revolver_draw = min(abs(levered_fcf), revolver_limit - revolver)
            revolver += revolver_draw
        else:
            revolver_draw = 0

        term_loan = max(term_loan - total_paydown, 0)

        schedule.append({
            "Year": year,
            "Revenue": revenue,
            "EBITDA": ebitda,
            "Taxes": taxes,
            "CapEx": capex,
            "WC_Change": wc_change,
            "Interest": interest_exp,
            "Mandatory": mandatory_pay,
            "Sweep": sweep_pay,
            "Revolver_Draw": revolver_draw,
            "End_TermLoan": term_loan,
            "Revolver_Balance": revolver
        })

    return schedule, term_loan, revolver
# ==========================================================
#  IRR, EXIT VALUE & TIERED WATERFALL DISTRIBUTIONS
# ==========================================================

def calculate_returns(schedule, ebitdas, revolver_balance, term_loan_end):
    initial_equity = purchase_price * equity_pct

    # Exit valuation
    exit_ebitda  = ebitdas[-1]
    exit_value   = exit_ebitda * exit_multiple

    # Net equity proceeds after debt & revolver
    net_equity_value = exit_value - term_loan_end - revolver_balance

    # IRR Calculation
    irr = ((net_equity_value / initial_equity) ** (1/holding_period) - 1) * 100

    # --------- TIERED WATERFALL (IRR-BASED) ---------
    profit = net_equity_value - initial_equity
    gp_promote = 0

    if irr <= hurdle_1 * 100:                           # Under 12%
        lp_take = net_equity_value
        gp_take = 0
    
    elif irr <= hurdle_2 * 100:                         # 12% to 18%
        promote_band = profit * promote_1               # 10% of profits in band
        gp_promote += promote_band
        lp_take = net_equity_value - gp_promote
        gp_take = gp_promote

    else:                                                # Above 18%
        # First band: 12% to 18%
        promote_band_1 = profit * promote_1              # 10% on mid band
        # Second band: above 18%
        promote_band_2 = profit * promote_2              # 20% on upper band
        gp_promote = promote_band_1 + promote_band_2
        lp_take = net_equity_value - gp_promote
        gp_take = gp_promote

    return net_equity_value, irr, lp_take, gp_take, exit_value


# Pretty printed output
def print_results(revenues, ebitdas, schedule, net_equity, irr, lp_take, gp_take, exit_value):
    print("\n==================== FINAL LBO RESULTS ====================")
    for i, (rev, ebitda) in enumerate(zip(revenues, ebitdas), start=1):
        print(f"Year {i}: Revenue ${rev:,.0f} | EBITDA ${ebitda:,.0f}")

    print("\n--- Debt & Cash Flow Movement ---")
    for row in schedule:
        print(f"Year {row['Year']}: Debt ↓ to ${row['End_TermLoan']:,.0f} | Revolver ${row['Revolver_Balance']:,.0f}")

    print("\n--- Exit & Sponsor Returns ---")
    print(f"Enterprise Value @ Exit:   ${exit_value:,.0f}")
    print(f"Net Equity to Sponsor:     ${net_equity:,.0f}")
    print(f"IRR to Sponsor:            {irr:.2f}%")

    print("\n--- Tiered Carry Waterfall (GP / LP) ---")
    print(f"LP Distribution:           ${lp_take:,.0f}")
    print(f"GP Promote / Carry:        ${gp_take:,.0f}")
    print(f"Promote Triggered?:        {'YES' if gp_take>0 else 'NO'}")
    print("===========================================================\n")
# ==========================================================
#  EXIT MULTIPLE SENSITIVITY (8x → 12x)
# ==========================================================

def sensitivity_table(revenues, ebitdas, schedule):
    print("=========== EXIT MULTIPLE SENSITIVITY (IRR %) ===========")
    for m in [8, 9, 10, 11, 12]:
        global exit_multiple
        exit_multiple = m
        # re-run core engine for each exit case
        _, _, t_end, rev_bal = schedule[-1]['End_TermLoan'], schedule[-1]['Revolver_Balance'], None, None
        net_equity, irr, _, _, _ = calculate_returns(schedule, ebitdas, schedule[-1]['Revolver_Balance'], schedule[-1]['End_TermLoan'])
        print(f"{m}x → IRR: {irr:.2f}%")
    print("=========================================================\n")


# ==========================================================
#  MAIN EXECUTION PIPELINE
# ==========================================================

if __name__ == "__main__":
    get_inputs()

    revenues, ebitdas = project_financials()
    schedule, term_loan_end, revolver_balance = build_cashflows_and_debt(revenues, ebitdas)
    net_equity, irr, lp_take, gp_take, exit_value = calculate_returns(schedule, ebitdas, revolver_balance, term_loan_end)

    print_results(revenues, ebitdas, schedule, net_equity, irr, lp_take, gp_take, exit_value)
    sensitivity_table(revenues, ebitdas, schedule)

