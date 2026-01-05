# 🛡️ Automated AML Transaction Monitoring System (PoC)

## 📌 Project Overview
This project is an **End-to-End (E2E) Compliance Surveillance Engine** built with Python and SQL. It simulates a core banking environment to detect suspicious financial activities, bridging the gap between traditional regulatory compliance and automated data engineering.

## 💼 Business Context
[cite_start]Drawing from my **6+ years of experience** as a Compliance Manager at **HSBC** and **Bank of China**, I designed this system to automate the detection of "Red Flags" that typically require intensive manual review. This solution focuses on **scalability** and **detection accuracy**.

## 🚀 Key Features
- **Data Ingestion:** Synthesizes high-volume transaction data and customer profiles using `Faker`.
- **ETL Pipeline:** Standardizes timeframes and converts multiple currencies (USD, HKD) to a base currency (AUD) for unified monitoring.
- **Surveillance Scenarios:** Implements industry-standard SQL rules:
  - **Structuring (Smurfing):** Detects multiple cash deposits just below the AUSTRAC $10,000 threshold.
  - **New Customer Monitoring:** Flags high-value transactions occurring within the first 30 days of account opening.
- **Reporting & Viz:** Generates a stakeholder dashboard showing risk exposure across customer tiers (VIP, GOLD, SILVER).

## 🛠️ Technical Stack
- **Languages:** Python 3.x, SQL (SQLite)
- **Libraries:** Pandas (Data Processing), Matplotlib/Seaborn (Visualization), Faker (Data Generation).
- **Architecture:** Class-based Modular Design.

## 📈 Impact
[cite_start]In my previous role, similar strategic process redesigns successfully **reduced case response time by 20%**. This project demonstrates the technical implementation of that efficiency gain.
