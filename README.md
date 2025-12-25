# LBO Mini Model
This project builds a simplified but realistic **Leveraged Buyout (LBO) model** in Python. It simulates a private equity acquisition using debt financing, projects operating performance, models debt paydown through free cash flow, and calculates equity returns via a carried interest waterfall.

The intent is to show the ability to translate financial modeling concepts into code — not just spreadsheets.

# What This Project Simulates 
This project models the core mechanics of an LBO, including:

**Transaction Funding & Structure**
- Equity + debt-funded acquisition
- Term Loan + Revolver capital stack
- Mandatory amortization + cash sweep paydown

**Financial Operations**
- Revenue → EBITDA projections over 5 years
- Taxes, CapEx, and Working Capital affecting cash flow
- Levered Free Cash Flow after interest

**Return Mechanics**
- EBITDA exit valuation
- Net equity proceeds to sponsor
- IRR calculation over the holding period

**Carried Interest & Waterfall**
- Tiered promote structure:
  | IRR Band | GP Carry |
  |----------|-----------|
  | 0% – 12% | 0%        |
  | 12% – 18% | 10%       |
  | >18%     | 20%       |
- Carry is based on **IRR hurdles**, not retroactive profit share

# Key Findings / Takeaways
| Metric | Result |
|--------|--------|
| Sponsor IRR | **~18.4%** |
| Exit Enterprise Value | **$646M** |
| Net Equity to Sponsor | **~$465M** |
| LP Distribution | **~$386M** |
| GP Promote / Carry | **~$79.6M** |
| Promote Triggered? | **YES (above 18%)** |

# Interpretation 
- IRR clears typical PE hurdle rates (15–20%)
- No revolver draw → base case generates sufficient cash flow
- The waterfall only rewards the GP *after* outperformance is achieved
- Small changes in exit multiple strongly influence IRR (leverage effect)

# What This Demonstrates (Skills)
- Understanding of capital structure & leveraged returns
- Debt paydown mechanics and interest impact
- Cash flow behavior under leverage
- IRR-based waterfall decision logic
- Ability to replicate financial models *programmatically*
  
## Run Model
```bash
python3 lbo_model.py

