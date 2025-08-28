#%%writefile loyalty_app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Loyalty Profit Calculator", layout="wide")

# ------------------------ Tier Logic (Auto Platform + Perf. Fee) ------------------------
TIERS = [
    {"name": "Starter",    "aov_min": 0,   "aov_max": 100,         "platform_fee": 199,  "perf_fee_pct": 0.02},   # < ₹100
    {"name": "Growth",     "aov_min": 100, "aov_max": 250,         "platform_fee": 399,  "perf_fee_pct": 0.025},  # ₹100–₹250
    {"name": "Pro",        "aov_min": 250, "aov_max": 500,         "platform_fee": 699,  "perf_fee_pct": 0.03},   # ₹250–₹500
    # For ₹500+, choose Elite by default; bump to Enterprise for large scale (>= 3000 cust/mo).
    {"name": "Elite",      "aov_min": 500, "aov_max": float("inf"),"platform_fee": 999,  "perf_fee_pct": 0.04},
    {"name": "Enterprise", "aov_min": 500, "aov_max": float("inf"),"platform_fee": 1499, "perf_fee_pct": 0.04},
]

def pick_tier(aov: float, customers_per_month: int):
    if aov < 100:
        return TIERS[0]
    if 100 <= aov < 250:
        return TIERS[1]
    if 250 <= aov < 500:
        return TIERS[2]
    # aov >= 500 → Elite by default; Enterprise for larger scale
    return TIERS[4] if customers_per_month >= 3000 else TIERS[3]

# ------------------------ Language Selection ------------------------
language = st.selectbox(
    "🌐 Choose your language / अपनी भाषा चुनें / ನಿಮ್ಮ ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ",
    ["English", "Hindi", "Kannada"]
)

# Explainer in Selected Language
if language == "English":
    st.title("🧮 Loyalty Program Profit Calculator")
    
    # Enhanced welcome section with better visual hierarchy
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 👋 Welcome to Your Profit Calculator!
        
        **What this tool does:** Shows you exactly how much more money you can make by giving small rewards to bring customers back.
        
        **How it works:** 
        - You give ₹50 reward after every 10 visits
        - Customers visit more often to earn rewards
        - More visits = more orders = more profit for you!
        
        **Our fees:** We only charge if you make more money. If visits don't increase, fees are waived.
        """)
    
    with col2:
        st.info("""
        **💡 Quick Tip:**
        Start with your current numbers on the left, then increase "Orders per Customer (With Loyalty)" to see the magic!
        """)

elif language == "Hindi":
    st.title("🧮 लॉयल्टी प्रोग्राम लाभ कैलकुलेटर")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### आपके लाभ कैलकुलेटर में स्वागत है!
        
        **यह टूल क्या करता है:** छोटे इनाम देकर ग्राहकों को वापस लाने से आप कितना ज्यादा पैसा कमा सकते हैं, यह दिखाता है।
        
        **कैसे काम करता है:**
        - हर 10 विजिट के बाद ₹50 का इनाम दें
        - ग्राहक इनाम पाने के लिए ज्यादा बार आते हैं
        - ज्यादा विजिट = ज्यादा ऑर्डर = आपका ज्यादा लाभ!
        
        **हमारा शुल्क:** सिर्फ तभी लेते हैं जब आप ज्यादा कमाते हैं। अगर विजिट नहीं बढ़तीं तो शुल्क माफ।
        """)
    
    with col2:
        st.info("""
        **💡 त्वरित सुझाव:**
        बाईं तरफ अपने वर्तमान आंकड़े डालें, फिर "लॉयल्टी के साथ ग्राहक प्रति ऑर्डर" बढ़ाकर जादू देखें!
        """)

elif language == "Kannada":
    st.title("🧮 ಲಾಯಲ್ಟಿ ಲಾಭ ಕ್ಯಾಲ್ಕುಲೇಟರ್")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### ನಿಮ್ಮ ಲಾಭ ಕ್ಯಾಲ್ಕುಲೇಟರ್‌ಗೆ ಸ್ವಾಗತ!
        
        **ಈ ಟೂಲ್ ಏನು ಮಾಡುತ್ತದೆ:** ಚಿಕ್ಕ ಬಹುಮಾನಗಳನ್ನು ನೀಡಿ ಗ್ರಾಹಕರನ್ನು ಹಿಂದೆ ತರುವ ಮೂಲಕ ನೀವು ಎಷ್ಟು ಹೆಚ್ಚು ಹಣ ಸಂಪಾದಿಸಬಹುದು ಎಂದು ತೋರಿಸುತ್ತದೆ.
        
        **ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ:**
        - ಪ್ರತಿ 10 ಭೇಟಿಗಳ ನಂತರ ₹50 ಬಹುಮಾನ ನೀಡಿ
        - ಗ್ರಾಹಕರು ಬಹುಮಾನಗಳನ್ನು ಪಡೆಯಲು ಹೆಚ್ಚು ಬಾರಿ ಬರುತ್ತಾರೆ
        - ಹೆಚ್ಚು ಭೇಟಿಗಳು = ಹೆಚ್ಚು ಆರ್ಡರ್‌ಗಳು = ನಿಮ್ಮ ಹೆಚ್ಚು ಲಾಭ!
        
        **ನಮ್ಮ ಶುಲ್ಕ:** ನೀವು ಹೆಚ್ಚು ಹಣ ಸಂಪಾದಿಸಿದಾಗ ಮಾತ್ರ ವಿಧಿಸುತ್ತೇವೆ. ಭೇಟಿಗಳು ಹೆಚ್ಚದಿದ್ದರೆ ಶುಲ್ಕವಿಲ್ಲ.
        """)
    
    with col2:
        st.info("""
        **💡 ತ್ವರಿತ ಸಲಹೆ:**
        ಎಡಭಾಗದಲ್ಲಿ ನಿಮ್ಮ ಪ್ರಸ್ತುತ ಸಂಖ್ಯೆಗಳನ್ನು ಹಾಕಿ, ನಂತರ "ಲಾಯಲ್ಟಿಯೊಂದಿಗೆ ಗ್ರಾಹಕರಿಗೆ ಒಂದು ಆರ್ಡರ್" ಹೆಚ್ಚಿಸಿ ಮ್ಯಾಜಿಕ್ ನೋಡಿ!
        """)

# ------------------------ Core Calculator ------------------------

# Enhanced Sidebar with better organization
st.sidebar.header("🏪 Your Shop Details")
st.sidebar.markdown("**📊 Basic Business Info**")

# Group related inputs with better labels and help text
aov = st.sidebar.number_input(
    "💰 Average Order Value (₹)", 
    min_value=0, 
    value=200,
    help="How much does a typical customer spend per order?"
)

profit_margin_percent = st.sidebar.number_input(
    "📈 Profit Margin (%)", 
    min_value=0.0, 
    max_value=100.0, 
    value=10.0,
    help="What percentage of revenue is your profit?"
)

customers_per_month = st.sidebar.number_input(
    "👥 Customers per Month", 
    min_value=0, 
    value=50,
    help="How many unique customers visit your shop monthly?"
)

st.sidebar.markdown("**🎯 Loyalty Program Settings**")

orders_before = st.sidebar.number_input(
    "📉 Orders per Customer (Before Loyalty)", 
    min_value=0, 
    value=2,
    help="How many times does a customer order before you start the loyalty program?"
)

orders_after = st.sidebar.number_input(
    "📈 Orders per Customer (With Loyalty)", 
    min_value=0, 
    value=4,
    help="How many times do you expect customers to order after starting the loyalty program?"
)

st.sidebar.markdown("**🎁 Reward Settings**")

reward_frequency = st.sidebar.number_input(
    " Reward Frequency (Every N visits)", 
    min_value=1, 
    value=10,
    help="Give reward after how many visits? (e.g., every 5th visit)"
)

reward_value = st.sidebar.number_input(
    " Reward Value (₹)", 
    min_value=0, 
    value=int(aov / 4),
    help="How much reward to give? (Recommended: 10-25% of order value)"
)

redemption_rate = st.sidebar.slider(
    "🎯 Reward Redemption Rate (%)", 
    min_value=0, 
    max_value=100, 
    value=100,
    help="What percentage of customers will actually use their rewards?"
)

# Performance Fee Toggle with better explanation
st.sidebar.markdown("**⚙️ Fee Settings**")
include_performance_fee = st.sidebar.toggle(
    "Include Performance Fee", 
    value=True,
    help="Performance fee is % of your extra profit. Turn off to see platform fee only."
)

st.divider()

# Enhanced Real-world Example with better formatting
st.markdown("### 📋 Your Business Scenario")
col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"""
    ** Current Situation:**
    - {customers_per_month} customers
    - {orders_before} visits each
    - {customers_per_month * orders_before} total orders
    """)

with col2:
    st.success(f"""
    **🎯 With Loyalty Program:**
    - Same {customers_per_month} customers
    - {orders_after} visits each
    - {customers_per_month * orders_after} total orders
    """)

with col3:
    st.warning(f"""
    **🎁 Reward Strategy:**
    - Give ₹{reward_value} after every {reward_frequency} visits
    - Expected {customers_per_month * (orders_after // reward_frequency)} rewards given
    """)

# Auto-select Tier → Platform Fee + Performance % (from AOV range; Enterprise if large scale)
tier = pick_tier(aov, customers_per_month)
tier_name = tier["name"]
platform_fee_auto = tier["platform_fee"]
perf_fee_pct = tier["perf_fee_pct"]  # e.g., 0.02 = 2%

# Enhanced tier display
st.markdown("### ️ Your Pricing Tier")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Tier", tier_name, help=f"Based on ₹{aov} AOV and {customers_per_month} customers")

with col2:
    st.metric("Platform Fee", f"₹{platform_fee_auto}/month", help="Fixed monthly fee")

with col3:
    if include_performance_fee:
        st.metric("Performance Fee", f"{perf_fee_pct*100:.1f}%", help="% of your extra profit")
    else:
        st.metric("Performance Fee", "Disabled", help="No performance fee charged")

# ------------------------ Calculations ------------------------
# Without loyalty
orders_without = customers_per_month * orders_before
revenue_without = orders_without * aov
profit_without = revenue_without * (profit_margin_percent / 100)

# With loyalty (before any fees)
orders_with = customers_per_month * orders_after
revenue_with = orders_with * aov
gross_profit_with = revenue_with * (profit_margin_percent / 100)

# Reward cost (keep your original working approach)
rewards_per_customer = orders_after // reward_frequency
potential_rewards = customers_per_month * rewards_per_customer
redeemed_rewards = potential_rewards * (redemption_rate / 100)
total_reward_cost = redeemed_rewards * reward_value

# Profit with loyalty BEFORE fees
profit_with_before_fees = gross_profit_with - total_reward_cost

# Incremental profit base (for Perf. Fee). Only positive uplift pays.
incremental_profit_base = max(0, profit_with_before_fees - profit_without)

# Fees
loyalty_improvement = orders_after > orders_before
performance_fee = (perf_fee_pct * incremental_profit_base) if (loyalty_improvement and include_performance_fee) else 0
platform_fee_display = platform_fee_auto if loyalty_improvement else 0
total_fee = platform_fee_display + performance_fee

# Final net profit with loyalty AFTER fees
net_profit_with = profit_with_before_fees - total_fee
delta = net_profit_with - profit_without
percent_delta = (delta / profit_without * 100) if profit_without > 0 else 0

# ------------------------ Enhanced Comparison Metrics ------------------------
st.markdown("### 📊 Profit Comparison")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader(" Without Loyalty")
    st.metric("Monthly Orders", f"{orders_without:,}")
    st.metric("Revenue", f"₹{revenue_without:,.0f}")
    st.metric("Net Profit", f"₹{profit_without:,.0f}")

with col2:
    st.subheader(" With Loyalty")
    st.metric("Monthly Orders", f"{orders_with:,}")
    st.metric("Revenue", f"₹{revenue_with:,.0f}")
    st.metric("Gross Profit", f"₹{gross_profit_with:,.0f}")
    st.metric("Rewards Redeemed", f"{redeemed_rewards:.0f} of {potential_rewards}")
    st.metric("Reward Cost", f"₹{total_reward_cost:,.0f}")
    st.metric("Profit (pre-fees)", f"₹{profit_with_before_fees:,.0f}")
    st.metric("Platform Fee", f"₹{platform_fee_display:,.0f}")
    
    # Conditionally show Performance Fee
    if include_performance_fee:
        st.metric("Perf. Fee (on Incremental Profit)", f"₹{performance_fee:,.0f}")
    else:
        st.metric("Perf. Fee (on Incremental Profit)", "₹0 (Disabled)")
    
    st.metric("Total Fee", f"₹{total_fee:,.0f}")
    st.metric("Net Profit (after fees)", f"₹{net_profit_with:,.0f}", delta=f"₹{delta:,.0f} ({percent_delta:.1f}%)")

with col3:
    st.subheader(" Uplift & ROI")
    st.metric("Incremental Profit (pre-fee)", f"₹{incremental_profit_base:,.0f}")
    # Fixed ROI calculation
    roi = (incremental_profit_base / total_fee) if total_fee > 0 else 0
    st.metric("ROI (Profit ÷ Fee)", f"{roi:.1f}×" if total_fee > 0 else "N/A")
    
    # Add helpful ROI interpretation
    if total_fee > 0:
        if roi > 2:
            st.success(" Excellent ROI! You're making great returns.")
        elif roi > 1:
            st.info("✅ Good ROI! You're making more than you're paying.")
        elif roi > 0.5:
            st.warning("⚠️ Low ROI. Consider adjusting reward strategy.")
        else:
            st.error("❌ Poor ROI. This may not be profitable.")

if not loyalty_improvement:
    st.warning("⚠️ Loyalty is not improving visits. Platform & Performance fees are waived (no uplift).")

# Enhanced Verdict with better styling
st.divider()
st.markdown("### 🎯 Final Verdict")

if delta > 0:
    st.success(f"""
    ✅ **Loyalty Program is PROFITABLE!**
    
    You'll make **₹{delta:,.0f} extra profit** per month ({percent_delta:.1f}% increase).
    For every ₹1 you pay in fees, you get ₹{roi:.1f} in extra profit.
    """)
elif delta == 0:
    st.info("ℹ️ **Loyalty Program breaks even.** Consider adjusting your reward strategy.")
else:
    st.error(f"""
    ❌ **Loyalty Program may reduce profit.**
    
    You could lose ₹{abs(delta):,.0f} per month. Try:
    - Reducing reward value
    - Increasing visit frequency requirement
    - Improving customer engagement
    """)

# ------------------------ Enhanced Profit Forecast Table ------------------------
st.divider()
st.markdown("### 📈 Profit Forecast for Different Customer Volumes")

# Add explanation
st.info("""
 **How to read this table:** See how your profit changes as your business grows. 
The loyalty program becomes more profitable with scale!
""")

projection_data = []
for cust in [50, 100, 200, 300, 400, 500, 1000, 2000, 3000, 5000]:
    t = pick_tier(aov, cust)
    pf_fixed = t["platform_fee"]
    pf_pct = t["perf_fee_pct"]

    orders_no_loyalty = cust * orders_before
    revenue_no_loyalty = orders_no_loyalty * aov
    profit_no_loyalty = revenue_no_loyalty * (profit_margin_percent / 100)

    orders_loyalty = cust * orders_after
    revenue_loyalty = orders_loyalty * aov
    gross_profit_loyalty = revenue_loyalty * (profit_margin_percent / 100)

    rewards_proj = cust * (orders_after // reward_frequency) * (redemption_rate / 100)
    reward_cost_proj = rewards_proj * reward_value

    profit_with_before_fees_proj = gross_profit_loyalty - reward_cost_proj
    incr_profit_base_proj = max(0, profit_with_before_fees_proj - profit_no_loyalty)

    # Apply performance fee toggle to forecast calculations
    perf_fee_proj = (pf_pct * incr_profit_base_proj) if (orders_after > orders_before and include_performance_fee) else 0
    platform_fee_proj = pf_fixed if orders_after > orders_before else 0
    total_fee_proj = platform_fee_proj + perf_fee_proj

    profit_loyalty_after_fees = profit_with_before_fees_proj - total_fee_proj
    gain_pct = ((profit_loyalty_after_fees - profit_no_loyalty) / profit_no_loyalty * 100) if profit_no_loyalty else 0
    incr_profit_after_fees = max(0, profit_loyalty_after_fees - profit_no_loyalty)
    roi_proj = (incr_profit_after_fees / total_fee_proj) if total_fee_proj > 0 else 0

    projection_data.append({
        "Customers": cust,
        "Tier": t["name"],
        "Net Profit (No Loyalty) ₹": round(profit_no_loyalty),
        "Profit w/ Loyalty (pre-fees) ₹": round(profit_with_before_fees_proj),
        "Incremental Profit (pre-fee) ₹": round(incr_profit_base_proj),
        "Perf. Fee ₹": round(perf_fee_proj),
        "Total Fee ₹": round(total_fee_proj),
        "Net Profit (after fees) ₹": round(profit_loyalty_after_fees),
        "Incremental Profit (after fees) ₹": round(incr_profit_after_fees),
        "ROI (×)": f"{roi_proj:.1f}×" if total_fee_proj > 0 else "N/A",
        "Incremental Gain (%)": f"{gain_pct:.1f}%" if profit_no_loyalty > 0 else "N/A",
    })

# Enhanced dataframe display
df = pd.DataFrame(projection_data)
st.dataframe(df, use_container_width=True)

# Enhanced caption
if include_performance_fee:
    st.caption("📋 *Platform fee and performance fee are auto-selected by tier. Performance fee is charged on incremental profit (pre-fees).*")
else:
    st.caption("📋 *Platform fee is auto-selected by tier. Performance fee is disabled.*")

# Add final call-to-action
st.divider()
st.markdown("### 🚀 Ready to Start Your Loyalty Program?")

col1, col2 = st.columns(2)
with col1:
    st.info("""
    **Next Steps:**
    1. Review your numbers above
    2. Adjust reward strategy if needed
    3. Contact us to get started!
    """)

with col2:
    st.success("""
    **Benefits:**
    - Increase customer visits
    - Boost monthly revenue
    - Build customer loyalty
    - Only pay fees when profitable
    """)
