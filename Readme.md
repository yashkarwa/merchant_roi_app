# Loyalty Profit Calculator (Streamlit)

A simple, merchant-friendly calculator to estimate whether a visit-based loyalty program increases monthly profit. It compares Before vs With Loyalty, applies rewards, and (optionally) a performance fee on incremental profit. Includes an auto-selected platform tier fee.

## Features
- Clean, single-page Streamlit app
- Auto Tier selection from AOV and scale (Enterprise if ≥ 3000 customers/month)
- Optional Performance Fee toggle (on incremental profit)
- Clear snapshot: orders, revenue, gross profit, rewards, fees, net profit
- ROI metric with interpretation (Profit ÷ Fee)
- Profit forecast table for multiple customer volumes
- Multilingual labels: English, Hindi, Kannada

## Run locally

Prereqs: Python 3.9+ recommended

```bash
# from the project root
python -m venv .venv
.\.venv\Scripts\activate   # Windows
# source .venv/bin/activate # macOS/Linux

pip install streamlit pandas
streamlit run app.py
# If your file is named loyalty_app.py:
# streamlit run loyalty_app.py
```

## Inputs (left sidebar)
- Average Order Value (₹)
- Profit Margin (%)
- Customers per Month
- Orders per Customer (Before Loyalty)
- Orders per Customer (With Loyalty)
- Reward Frequency (Every N visits)
- Reward Value (₹)
- Reward Redemption Rate (%)
- Include Performance Fee (toggle)

## Tiers (auto-selected)
- Starter: AOV < 100 → ₹199, Perf Fee 2%
- Growth: 100 ≤ AOV < 250 → ₹399, Perf Fee 2.5%
- Pro: 250 ≤ AOV < 500 → ₹699, Perf Fee 3%
- Elite: AOV ≥ 500 → ₹999, Perf Fee 4%
- Enterprise: AOV ≥ 500 and Customers ≥ 3000 → ₹1499, Perf Fee 4%

Note: Platform fee is charged only when there is uplift (Orders with Loyalty > Orders Before). Performance fee is charged only if the toggle is ON and there is uplift.

## Calculations (formulas)

Baseline (No Loyalty)
- Orders_without = Customers × Orders_before
- Revenue_without = Orders_without × AOV
- Profit_without = Revenue_without × (PM% / 100)

With Loyalty (pre-fees)
- Orders_with = Customers × Orders_after
- Revenue_with = Orders_with × AOV
- GrossProfit_with = Revenue_with × (PM% / 100)

Rewards
- Rewards_per_customer = floor(Orders_after / N)
- Potential_rewards = Customers × Rewards_per_customer
- Redeemed_rewards = Potential_rewards × (RR% / 100)
- Total_reward_cost = Redeemed_rewards × Reward_value

Profit (pre-fees)
- Profit_with_pre_fees = GrossProfit_with − Total_reward_cost

Fees
- Incremental_profit_base = max(0, Profit_with_pre_fees − Profit_without)
- Platform_fee = tier.platform_fee if uplift else 0
- Performance_fee = perf_fee_pct × Incremental_profit_base if (uplift and toggle ON) else 0
- Total_fee = Platform_fee + Performance_fee

Net and ROI
- Net_profit_with = Profit_with_pre_fees − Total_fee
- Delta = Net_profit_with − Profit_without
- ROI = Incremental_profit_base ÷ Total_fee (shown when Total_fee > 0)

Why ROI uses pre-fee incremental profit:
- It answers “How much incremental profit do I earn for each ₹1 fee?”
- Using post-fee profit in the numerator would double-count fees.

## UI Sections
- Without Loyalty: Orders, Revenue, Net Profit
- With Loyalty: Orders, Revenue, Gross Profit, Rewards, Reward Cost, Profit (pre-fees), Fees, Net Profit
- Uplift & ROI: Incremental Profit (pre-fee), ROI (Profit ÷ Fee) with simple interpretation
- Profit Forecast Table for volumes [50, 100, 200, 300, 400, 500, 1000, 2000, 3000, 5000]

## Example sanity check
If:
- AOV=₹500, PM=20%, Customers=100, Orders_before=1, Orders_after=2
- N=5, Reward=₹50, RR=50%
- Tier=Elite (₹999), Performance Fee OFF
Then:
- Incremental_profit_base computed from pre-fee profits
- Total_fee = ₹999
- ROI = Incremental_profit_base ÷ 999

If Incremental_profit_base = ₹2,812 and Total_fee = ₹999, ROI = 2.8×

## Troubleshooting
- ROI shows “N/A”: Spend (Total Fee) is 0. Enable uplift or toggle performance fee ON.
- Values look off: Verify PM% and RR% inputs. Very high reward value or low N can make programs unprofitable.
- Port in use: `streamlit run app.py --server.port 8502`

## Tech stack
- Python, Streamlit, Pandas
- Single-file app (easy to deploy and customize)

## License
MIT (or your preferred license)