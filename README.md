# 📊 Customer Churn Investigation & Retention Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]([MASUKKAN_LINK_STREAMLIT_APP_KAMU])
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)

An end-to-end exploratory data analysis (EDA) and interactive business intelligence dashboard built to investigate subscription churn drivers, segment customer risk profiles, and generate actionable retention strategies across **505,206 customer records**.

🔗 **Live Interactive Dashboard:** [Launch Streamlit App]([MASUKKAN_LINK_STREAMLIT_APP_KAMU])

---

## 📌 Project Overview

High customer churn directly erodes recurring revenue and increases customer acquisition pressure. Using a subscription dataset sourced from [Kaggle - Customer Churn Dataset](https://www.kaggle.com/datasets/muhammadshahidazeem/customer-churn-dataset), this project answers **8 core business questions** structured from highest financial impact to demographic insights, culminating in an operational **Retention Action Watchlist** for Customer Success and Billing teams.

### Core Objectives
1. **Identify Churn Drivers:** Pinpoint exact behavioral thresholds (support calls, payment delays, contract types) where churn probability spikes.
2. **Segment Customers:** Classify customers by monetary value (`Total Spend`), product engagement (`Usage Frequency`), and recency (`Last Interaction`).
3. **Propose Retention Actions:** Translate analytical findings into rule-based intervention triggers for active at-risk customers (`Churn = 0`).

---

## 🗂️ Dataset & Preprocessing Workflow

The raw dataset consists of two separate splits (`training-master` and `testing-master`), which were audited, cleaned, and merged in `EDA.ipynb`:

* **Data Merging & Cleaning:** Combined `440,833` training rows (dropped 1 completely null row at index `199295`) and `64,374` testing rows into a unified dataset of **`505,206` records** across **12 features** with zero duplicates.
* **Type Standardization:** Standardized `float64` columns in the training set to `int64` for schema consistency.
* **Feature Engineering (Binning):** Created business-oriented cohorts (`Payment Delay (weeks)`, `Spend Tier`, `Usage Tier`, `Interaction Recency`, `Tenure Phase`, and `Age Group`) exported to `dashboard/customer_churn_dataset-EDA.csv`.

---

## 🔍 Key Business Questions & Analytical Findings

| # | Business Question | Key Data Findings |
| :- | :--- | :--- |
| **1** | **Revenue at Risk:** How much total revenue is lost due to churn, and which plan loses the most? | Overall churn stands at **55.52%** (`280,492` churned customers), resulting in **$151.13M in lost spend** vs. $162.01M retained. Losses are evenly distributed across **Standard ($50.52M)**, **Basic ($50.45M)**, and **Premium ($50.16M)**, with churned users spending **$539 on average** vs. **$721** for retained users. |
| **2** | **Contract Length Impact:** How significant is the churn gap across Monthly, Quarterly, and Annual plans? | **Monthly contracts suffer a massive 90.20% churn rate** (`98,525` of `109,234` users), nearly double the churn rate of **Annual (46.09%)** and **Quarterly (45.82%)** contracts. |
| **3** | **Support Calls Threshold:** At what complaint frequency do customers abandon the service? | Churn stays steady at **~29.9%–31.0%** for `0–2` calls, rises to **55.4%** at `4` calls, and hits a **critical tipping point at $\ge 5$ calls**, surging to **87.5%–91.7%**. |
| **4** | **Payment Delay Signal:** When does late payment shift from oversight to a clear churn indicator? | Churn remains around **42.8%–48.3%** up to 20 days late, then jumps sharply to **94.17%** once delays exceed **20 days (`>3 weeks`)**. |
| **5** | **Spend vs. Usage Segmentation:** How do customer segments differ in churn risk? | **Low Spend + Low Usage** shows the highest churn (**71.1%**), followed by **Low Spend + High Usage (67.9%)**. **High Spend** customers are significantly more resilient (**43.3%** for Low Usage; **39.4%** for High Usage). |
| **6** | **Silent Churn Detection:** Do low usage and long inactivity detect churn early? | Yes. Regardless of usage tier, churn climbs steadily as `Last Interaction` ages—from **47.2%–50.8%** (`Active: 1–10 days`) to **62.0%–65.5%** (`Inactive: >20 days`). |
| **7** | **Tenure Vulnerability:** Which subscription phase experiences the highest cancellation rate? | **Basic plan** users churn heavily during onboarding (**63.8%** in `0–12 months`), while all tiers experience a secondary spike at **`13–24 months` (~59.3%)** before stabilizing at ~54.5% thereafter. |
| **8** | **Demographic Patterns:** Do specific age groups or genders churn disproportionately? | Customers aged **51–60** and **>60 years** experience extreme churn (**89.2%–91.3%**). Across ages `18–50`, **Female** customers consistently exhibit higher churn rates than Male customers (e.g., **63.4% vs. 45.6%** in ages `18–30`). |

---

## 🎯 Actionable Retention Recommendations

1. **Monthly-to-Annual Migration Campaign:** Offer targeted discounts (e.g., 15% off or 2 months free) to high-spending `Monthly` subscribers before their renewal cycle to lock in lower churn tiers.
2. **Support Escalation Trigger (`>= 4 Calls`):** Automatically flag any active customer reaching their 4th support call for priority intervention by a Dedicated Account Manager before they hit the 5-call tipping point.
3. **Automated Billing Grace & Installment Reminders (`Day 15–20`):** Trigger proactive billing alerts and flexible payment options between days 15 and 20 of payment delay to prevent accounts from crossing the 20-day churn cliff.
4. **Senior & Onboarding UX Support:** Provide guided onboarding tutorials and proactive check-ins for customers aged `>50` and new `Basic` plan subscribers (`0–12 months`).

---

## 🖥️ Dashboard Architecture (Streamlit)

The interactive web application (`dashboard/app.py`) is structured into four operational zones:

* **Global Filters (Sidebar):** Filter the entire dashboard dynamically by `Subscription Type`, `Contract Length`, `Gender`, and `Age` range.
* **Zone 1 — Executive KPI Scorecard:** Real-time metrics tracking *Total Customers*, *Overall Churn Rate*, *Revenue Lost*, *Avg. Support Calls*, and *High-Risk Active Users*.
* **Zone 2 — Churn Drivers (Q1–Q4):** Interactive Plotly bar and threshold line charts highlighting financial losses, contract duration gaps, support call tipping points, and payment delay escalations.
* **Zone 3 — Segmentation & Demography (Q5–Q8):** 2x2 risk matrix heatmap, silent churn grouped bars, tenure lifecycle trends, and demographic breakdowns.
* **Zone 4 — Retention Action Watchlist:** Operational drill-down table filtering active users (`Churn = 0`) by custom risk thresholds, complete with automated **Recommended Action** tags and one-click **CSV Export**.

---

## 📁 Repository Structure

```text
customer-churn-investigation/
├── dashboard/
│   ├── app.py                                   # Main Streamlit dashboard application
│   └── customer_churn_dataset-EDA.csv           # Processed dataset with engineered cohort columns
├── data/
│   ├── customer_churn_dataset-training-master.csv
│   ├── customer_churn_dataset-testing-master.csv
│   └── customer_churn_dataset-cleaned.csv
├── EDA.ipynb                                    # Data cleaning, business question aggregations & Plotly EDA
├── requirements.txt                             # Python dependencies for local & cloud deployment
└── README.md                                    # Project documentation
```

# 🚀 How to Run Locally
## 1. Clone the repository:
```Bash
git clone [https://github.com/](https://github.com/)[USERNAME_GITHUB_KAMU]/customer-churn-investigation.git
cd customer-churn-investigation
```

## 2. Create and activate a virtual environment (optional but recommended):
```Bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

## 3. Install required dependencies:
```Bash
pip install -r requirements.txt
```
## 4. Run the Streamlit dashboard:
```Bash
streamlit run dashboard/app.py
```
