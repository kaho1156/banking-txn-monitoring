# 🏦 Banking Transaction Risk Monitoring

This project simulates banking customer and transaction data using Python and analyzes high-risk behavior patterns using SQL. It's designed as a showcase of data engineering, SQL analysis, and risk logic commonly applied in anti-fraud and compliance workflows.

## 📌 Project Objectives

- Generate realistic customer and transaction data with Python (using `Faker`)
- Store and query data using SQLite
- Identify high-risk transactions using SQL rules
- Export and visualize key findings

## 🛠️ Tools Used

- Python (Pandas, SQLite3, Faker)
- SQL
- Jupyter Notebook
- Google Colab (for exports/downloads)

## 🧾 Key Risk Rules Implemented

1. **Large Cash Transactions** — over AUD 10,000  
2. **High-Value Wire Transfers** — over AUD 50,000  
3. **Non Face-to-Face Large Transactions** — over AUD 10,000  
4. **New Customer Activity** — large transactions within first 30 days

## 📊 Sample Insights

- Distribution of transaction types
- Top customers by transaction amount
- Frequency of high-risk transaction types

> Example: `SELECT * FROM txn_data WHERE [Txn Type] = 'CASH' AND [Txn Amt in AUD] > 10000`

## 📁 Repository Structure

├── txn_analysis.ipynb # Main analysis notebook
├── README.md # Project overview
├── data/ # Optional: sample .csv datasets
├── output/ # Exported results (e.g. .csv summaries)
└── requirements.txt # List of dependencies

markdown
複製
編輯

## 🚀 How to Run

1. Clone the repo and open `txn_analysis.ipynb` in Jupyter or Colab.
2. Run each cell step-by-step.
3. Query high-risk behaviors via the built-in SQL logic.
4. Download results or extend analysis (e.g., ML clustering or Power BI dashboard).

## 💡 Future Improvements

- Add dashboards using Power BI or Tableau
- Apply clustering (KMeans) for customer segmentation
- Expand currency support and geography

---

## 👤 Author

Moses Wong — *Data Analyst / IT Graduate passionate about fraud detection and risk analytics.*