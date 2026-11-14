import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ================================
# 1. LANDING PAGE CONFIGURATION
# ================================
st.set_page_config(
  page_title="Customer Churn Investigation Dashboard",
  page_icon="📊",
  layout="wide",
  initial_sidebar_state="expanded"
)

# Style the scoreboarsd with custom CSS
st.markdown("""
<style>
  div[data-testid="metricsContainer"]{
    background-color: #f0f2f6;
    border: 1px solid #d3d6db;
    padding: 10px;
    border-radius: 5px;
  }
</style>
""", unsafe_allow_html=True)

# ================================
# 2. LOAD & FEATURE ENGINEERING
# ================================
@st.cache_data
def load_data():
  # Load the cleaned and merged dataset
  df = pd.read_csv('dashboard\customer_churn_dataset-EDA.csv')

  # Feature Engineering: Create a new column for churn status
  df['Churn Status'] = np.where(df['Churn'] == 1, 'Churned', 'Retained')

  return df

df_raw = load_data()

# ================================
# 3. SIDEBAR: GLOBAL FILTERS
# ================================
st.sidebar.header("🔍Global Filters")
st.sidebar.caption("Use these filters to refine the data displayed in the dashboard.")

sub_types = st.sidebar.multiselect(
  "Subscription Type",
  options=df_raw['Subscription Type'].unique(),
  default=df_raw['Subscription Type'].unique()
)

contract_durations = st.sidebar.multiselect(
  "Contract Length",
  options=df_raw['Contract Length'].unique(),
  default=df_raw['Contract Length'].unique()
)

genders = st.sidebar.multiselect(
  "Gender",
  options=df_raw['Gender'].unique(),
  default=df_raw['Gender'].unique()
)

age_min, age_max = int(df_raw['Age'].min()), int(df_raw['Age'].max())
age_range = st.sidebar.slider(
  "Age Range",
  min_value=age_min,
  max_value=age_max,
  value=(age_min, age_max)
)

# Apply the filters to the dataset
df = df_raw[
  (df_raw['Subscription Type'].isin(sub_types)) &
  (df_raw['Contract Length'].isin(contract_durations)) &
  (df_raw['Gender'].isin(genders)) &
  (df_raw['Age'] >= age_range[0]) & (df_raw['Age'] <= age_range[1])
]

if df.empty:
  st.warning("No data available for the selected filters. Please adjust your filter selections.")
  st.stop()
  
# ================================
# 4. HEADER & ZONE 1: KPI SCOREBOARD
# ================================
st.title("📊 Customer Churn Investigation & Retention Dashboard")
st.markdown("This dashboard provides insights into customer churn patterns and retention strategies.")

cust_total = len(df)
churn_rate = df['Churn'].mean() * 100
rev_lost = df.loc[df['Churn'] == 1, 'Total Spend'].sum()
avg_calls_churn = df.loc[df['Churn'] == 1, 'Support Calls'].mean()
avg_calls_ret = df.loc[df['Churn'] == 0, 'Support Calls'].mean()

# Active customers at high risk
high_risk_active = len(df[(df['Churn'] == 0) & ((df['Support Calls'] >= 5) | (df['Payment Delay'] > 20))])

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Total Customers", f"{cust_total:,}")
kpi2.metric("Overall Churn Rate", f"{churn_rate:.2f}%", delta="Crirical (>50%)" if churn_rate > 50 else "Contolled", delta_color="inverse")
kpi3.metric("Revenue Lost (Churned)", f"${rev_lost:,.0f}")
kpi4.metric("Average Support Calls (Churn)", f"{avg_calls_churn:.2f}", delta=f"vs {avg_calls_ret:.2f} (Retained)", delta_color='inverse')
kpi5.metric("High-Risk Active Users", f"{high_risk_active:,}", help="Active customers with Support Calls >5 or Payment Delay > 20 days")

st.divider()

# ================================
# 5. NAV TABS (ZONE 2, ZONE 3, ZONE 4)
# ================================

tab1, tab2, tab3 = st.tabs([
  "📉 Zone 2: Churn Drivers Analysis",
  "🧩 Zone 3: Segmentation & Demography",
  "🎯 Zone 4: Retention Action Watchlist"
])

COLOR_SAFE = "#2E86AB"
COLOR_RISK = "#E63946"
COLOR_NEUTRAL = "#457B9D"

# --- TAB 1: CHURN DRIVERS ---
with tab1:
  col1, col2 = st.columns(2)
  
  with col1:
    # Q1: Revenue at Risk
    q1 = df.groupby(['Subscription Type', 'Churn'], as_index=False).agg(total_revenue=('Total Spend','sum'))
    q1['Status'] = q1['Churn'].map({0: 'Retained', 1: 'Churned'})
    fig_q1 = px.bar(
        q1, x='Subscription Type', y='total_revenue', color='Status',
        barmode='group', text_auto='.3s',
        color_discrete_map={'Retained': COLOR_SAFE, 'Churned': COLOR_RISK},
        title='Question 1: Retained vs Churned Revenue ($)'
    )
    st.plotly_chart(fig_q1, use_container_width=True)
    
    # Q3: Support Calls Threshold
    q3 = df.groupby('Support Calls', as_index=False).agg(churn_rate=('Churn','mean'))
    q3['churn_pct'] = q3['churn_rate'] * 100
    fig_q3 = px.line(
        q3, x='Support Calls', y='churn_pct', markers=True,
        title='Question 3: Spike in Churn Rate Based on Support Call Frequency'
    )
    fig_q3.update_traces(line_color='#1D3557', line_width=3, marker_size=8)
    # Vertical line tipping point at 5 calls
    fig_q3.add_vline(x=5, line_dash="dash", line_color=COLOR_RISK, annotation_text="Critical Threshold (5 Calls)")
    fig_q3.update_layout(yaxis_title='Churn Rate (%)', yaxis_range=[0, 105])
    st.plotly_chart(fig_q3, use_container_width=True)
    
  with col2:
    # Q2: Contract Length
    q2 = df.groupby('Contract Length', as_index=False).agg(churn_rate=('Churn', 'mean')).sort_values('churn_rate')
    q2['churn_pct'] = q2['churn_rate'] * 100
    fig_q2 = px.bar(
        q2, x='churn_pct', y='Contract Length', orientation='h',
        text=q2['churn_pct'].apply(lambda x: f'{x:.1f}%'),
        color='Contract Length',
        color_discrete_map={'Monthly': COLOR_RISK, 'Annual': COLOR_SAFE, 'Quarterly': COLOR_NEUTRAL},
        title='Question 2: Churn Rate by Contract Duration (%)'
    )
    fig_q2.update_layout(xaxis_title='Churn Rate (%)', showlegend=False, xaxis_range=[0, 105])
    st.plotly_chart(fig_q2, use_container_width=True)
    
    # Q4: Payment Delay
    q4 = df.groupby('Payment Delay (weeks)', observed=False, as_index=False).agg(churn_rate=('Churn', 'mean'))
    q4['churn_pct'] = q4['churn_rate'] * 100
    fig_q4 = px.bar(
        q4, x='Payment Delay (weeks)', y='churn_pct',
        text=q4['churn_pct'].apply(lambda x: f'{x:.1f}%'),
        color='churn_pct', color_continuous_scale='YlOrRd',
        title='Question 4: Escalation of Churn Risk Based on Payment Delays'
    )
    fig_q4.update_layout(yaxis_title='Churn Rate (%)', coloraxis_showscale=False, yaxis_range=[0, 105])
    st.plotly_chart(fig_q4, use_container_width=True)

# --- TAB 2: SEGMENTATION & DEMOGRAPHY ---
with tab2:
  col3, col4 = st.columns(2)
  
  with col3:
    # Q5: Heatmap Matrix Spend vs Usage
    q5 = df.groupby(['Spend Tier', 'Usage Tier'], observed=False, as_index=False).agg(churn_rate=('Churn', 'mean'))
    pivot_q5 = q5.pivot(index='Spend Tier', columns='Usage Tier', values='churn_rate') * 100
    fig_q5 = px.imshow(
        pivot_q5, text_auto='.1f', color_continuous_scale='YlOrRd',
        labels=dict(x="Usage Tier", y="Spend Tier", color="Churn Rate (%)"),
        title='Question 5: Customers Segmentation Matrix — Churn Rate (%)'
    )
    st.plotly_chart(fig_q5, use_container_width=True)
    
    # Q7: Tenure Phase
    q7 = df.groupby(['Tenure Phase', 'Subscription Type'], observed=False, as_index=False).agg(churn_rate=('Churn', 'mean'))
    q7['churn_pct'] = q7['churn_rate'] * 100
    fig_q7 = px.line(
        q7, x='Tenure Phase', y='churn_pct', color='Subscription Type', markers=True,
        title='Question 7: Trend of Churn Rate Throughout Customer Tenure'
    )    
    fig_q7.update_layout(yaxis_title='Churn Rate (%)')
    st.plotly_chart(fig_q7, use_container_width=True)
    
  with col4:
    # Q6: Silent Churn
    q6 = df.groupby(['Usage Tier', 'Interaction Recency'], observed=False, as_index=False).agg(churn_rate=('Churn', 'mean'))
    q6['churn_pct'] = q6['churn_rate'] * 100
    fig_q6 = px.bar(
        q6, x='Interaction Recency', y='churn_pct', color='Usage Tier',
        barmode='group', text=q6['churn_pct'].apply(lambda x: f'{x:.1f}%'),
        color_discrete_map={'Low Usage': COLOR_RISK, 'High Usage': COLOR_SAFE},
        title='Question 6: Silent Churn Detection (Usage Frequency vs Last Interaction)'
    )
    fig_q6.update_layout(yaxis_title='Churn Rate (%)', yaxis_range=[0, 85])
    st.plotly_chart(fig_q6, use_container_width=True)
    
    # Q8: Age & Gender Demography
    q8 = df.groupby(['Age Group', 'Gender'], observed=False, as_index=False).agg(churn_rate=('Churn', 'mean'))
    q8['churn_pct'] = q8['churn_rate'] * 100
    fig_q8 = px.bar(
        q8, x='Age Group', y='churn_pct', color='Gender',
        barmode='group', text=q8['churn_pct'].apply(lambda x: f'{x:.1f}%'),
        color_discrete_map={'Female': '#E76F51', 'Male': '#2A9D8F'},
        title='Question 8: Comparison of Churn Rate by Age Group and Gender'
    )
    fig_q8.update_layout(yaxis_range=[0, 105], yaxis_title='Churn Rate (%)')
    st.plotly_chart(fig_q8, use_container_width=True)
    
# --- TAB 3: RETENTION ACTION WATCHLIST (LOCAL FILTERS) ---
with tab3:
  st.subheader("Priority List of Active High-Risk Customers (Churn = 0)")
  st.caption("Use the Local Filter below to filter the intervention targets for the Customer Success & Billing team")
  
  # Local Filters for Operational Investigation
  f1, f2, f3 = st.columns(3)
  min_calls = f1.slider("Minimal Support Calls", 0, 10, 4)
  min_delay = f2.slider("Minimal Payment Delay (Days)", 0, 30, 15)
  min_spend = f3.number_input("Minimal Total Spend ($)", min_value=0, max_value=1000, value=500, step=50)
  
  watchlist = df[
    (df['Churn'] == 0) &
    (df['Total Spend'] >= min_spend) &
    ((df['Support Calls'] >= min_calls) | (df['Payment Delay'] >= min_delay))
  ].copy()
  
  # Recommendations for automated actions based on business rules
  def assign_action(row):
    actions = []
    if row['Contract Length'] == 'Monthly':
      actions.append("Offer a 15% Discount on Annual upgrades")
    if row['Support Calls'] >= 5:
      actions.append("Dedicated Account Manager Escalation")
    if row['Payment Delay'] > 20:
      actions.append("Billing Reminder + Installment Options")
    if row['Age'] > 50 and row['Usage Frequency'] < 10:
      actions.append("Personal Customer Service Onboarding Session")
    return " | ".join(actions) if actions else "Email Re-engagement Campaign"

  watchlist['Recommended Action'] = watchlist.apply(assign_action, axis=1)
  watchlist_display = watchlist[[
    'CustomerID', 'Subscription Type', 'Contract Length', 'Total Spend',
    'Support Calls', 'Payment Delay', 'Usage Frequency', 'Recommended Action'
  ]].sort_values(by='Total Spend', ascending=False)
  
  st.info(f"**{len(watchlist_display):,} active customers** were found that satisfied risk criteria described above.")
  st.dataframe(watchlist_display.head(50), use_container_width=True, hide_index=True)
  
  # Export to CSV button for operational team
  csv_export = watchlist_display.to_csv(index=False).encode('utf-8')
  st.download_button(
    label="⬇️ Download the Retention Target List (CSV)",
    data=csv_export,
    file_name="retention_action_watchlist.csv",
    mime="text/csv"
  )
