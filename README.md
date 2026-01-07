## LBO Mini Model

A Python-based leveraged buyout (LBO) model that simulates a private equity acquisition using debt financing, operating projections, debt paydown mechanics, and an IRR-based carried interest waterfall. The project demonstrates the ability to translate traditional LBO financial modeling concepts into programmatic logic rather than spreadsheet-only implementations.

## Problem Context

LBO models are typically built in spreadsheets, which can obscure the underlying mechanics of leverage, cash flow allocation, and return attribution. This project was built to explicitly model those mechanics in code, allowing capital structure behavior, debt paydown, and equity returns to be traced transparently through a simulated private equity transaction.

## What This Project Simulates

The model captures the core mechanics of a simplified but realistic LBO transaction.

### Transaction Structure
- Debt- and equity-funded acquisition
- Term loan and revolver capital stack
- Mandatory amortization and excess cash sweep

### Operating Performance
- Five-year revenue and EBITDA projections
- Taxes, capital expenditures, and working capital impacts
- Levered free cash flow after interest expense

### Returns and Exit
- Exit valuation based on EBITDA multiple
- Net equity proceeds to sponsor
- Internal rate of return (IRR) over the holding period

### Carried Interest & Waterfall
- Tiered promote structure based on IRR hurdles  

| IRR Band | GP Carry |
|--------|----------|
| 0% – 12% | 0% |
| 12% – 18% | 10% |
| >18% | 20% |

- Carry is calculated on an IRR hurdle basis rather than retroactive profit sharing

## Key Outputs (Base Case)

| Metric | Result |
|------|--------|
| Sponsor IRR | ~18.4% |
| Exit Enterprise Value | ~$646M |
| Net Equity to Sponsor | ~$465M |
| LP Distribution | ~$386M |
| GP Promote / Carry | ~$79.6M |
| Promote Triggered | Yes (>18%) |

## Interpretation

- Sponsor IRR clears common private equity hurdle rates (15–20%)
- No revolver draw in the base case indicates sufficient operating cash flow
- The carry structure rewards the GP only after meaningful outperformance
- Exit multiple assumptions materially drive equity returns due to leverage amplification

## What This Demonstrates

- Understanding of leveraged capital structures and return dynamics
- Debt amortization, interest expense, and cash sweep mechanics
- Free cash flow behavior under leverage
- IRR-based waterfall and promote logic
- Ability to replicate spreadsheet-style financial models programmatically

## Run the Model

Execute the LBO simulation:

```bash
python3 lbo_model.py

