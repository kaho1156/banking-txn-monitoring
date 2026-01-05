import pandas as pd
import sqlite3
import random
import matplotlib.pyplot as plt
import seaborn as sns
from faker import Faker
from datetime import datetime, timedelta

"""
AML Transaction Monitoring & Surveillance System (PoC)
Author: Moses Wong
Description: An end-to-end pipeline simulating banking data ingestion, 
             ETL processing, and SQL-based rule monitoring for AML compliance.
"""

class AMLSystem:
    def __init__(self, num_customers=300):
        self.fake = Faker()
        self.num_customers = num_customers
        self.exchange_rates = {"AUD": 1.0, "USD": 1.5, "HKD": 0.2}
        self.conn = sqlite3.connect(":memory:") # Using in-memory DB for demonstration

    def generate_data(self):
        """Phase 1: Data Ingestion - Synthesizing Customer and Transaction Data"""
        # Generate Static Customer Data
        cust_list = []
        start_date = datetime.now() - timedelta(days=365*5)
        for i in range(1, self.num_customers + 1):
            cust_list.append({
                "CIN": f"C{i:04d}",
                "Cust_Name": self.fake.name(),
                "Cust_Tier": random.choice(["GOLD", "SILVER", "VIP"]),
                "Cust_Sin_Dt": (start_date + timedelta(days=random.randint(0, 365*5))).date()
            })
        df_cust = pd.DataFrame(cust_list)

        # Generate Dynamic Transaction Data
        txn_list = []
        txn_types = ["CASH", "WIRE", "ONLINE", "CARD", "ATM", "NON FACE TO FACE"]
        for cin in df_cust['CIN']:
            for _ in range(random.randint(5, 50)):
                cur = random.choice(["HKD", "USD", "AUD"])
                amt = round(random.uniform(10, 20000), 2)
                if random.random() < 0.05: amt *= 10 # Simulate Outliers
                
                txn_list.append({
                    "Txn_Date": (datetime.now() - timedelta(days=random.randint(0, 730))).strftime("%d/%m/%Y %H:%M:%S"),
                    "CIN": cin,
                    "Txn_Cur": cur,
                    "Txn_Amt": amt,
                    "Txn_Type": random.choice(txn_types),
                    "Nf2f": random.choice(["Y", "N"])
                })
        df_txn = pd.DataFrame(txn_list)
        return df_cust, df_txn

    def process_data(self, df_cust, df_txn):
        """Phase 2: ETL & Data Transformation"""
        df_txn = df_txn.copy()
        # Standardize Timeframes
        df_txn['Txn_Date'] = pd.to_datetime(df_txn['Txn_Date'], dayfirst=True)
        df_cust['Cust_Sin_Dt'] = pd.to_datetime(df_cust['Cust_Sin_Dt'])
        
        # Currency Conversion to Base (AUD)
        df_txn['Txn_Amt_AUD'] = df_txn.apply(
            lambda x: round(x['Txn_Amt'] * self.exchange_rates[x['Txn_Cur']], 2), axis=1
        )
        
        # Load into SQLite for Monitoring
        df_cust.to_sql("cust_data", self.conn, index=False, if_exists="replace")
        df_txn.to_sql("txn_data", self.conn, index=False, if_exists="replace")

    def run_scenarios(self):
        """Phase 3: Surveillance Scenarios (SQL-based Monitoring)"""
        scenarios = {
            "New Customer High-Risk Activity": """
                SELECT T.*, C.Cust_Sin_Dt 
                FROM txn_data T 
                JOIN cust_data C ON T.CIN = C.CIN
                WHERE T.Txn_Date >= C.Cust_Sin_Dt 
                  AND julianday(T.Txn_Date) - julianday(C.Cust_Sin_Dt) <= 30
                  AND T.Txn_Amt_AUD > 10000;
            """,
            "Potential Structuring (Smurfing)": """
                SELECT CIN, COUNT(*) as cnt, SUM(Txn_Amt_AUD) as total_vol
                FROM txn_data
                WHERE Txn_Type = 'CASH'
                GROUP BY CIN, date(Txn_Date)
                HAVING cnt >= 3 AND total_vol BETWEEN 8000 AND 10000;
            """,
            "Cash Volume Summary by Tier": """
                SELECT C.Cust_Tier, COUNT(T.Txn_Cur) as Txn_Count, SUM(T.Txn_Amt_AUD) as Total_AUD 
                FROM txn_data T 
                JOIN cust_data C ON T.CIN = C.CIN 
                WHERE T.Txn_Type = 'CASH' 
                GROUP BY C.Cust_Tier;
            """
        }
        
        results = {}
        for name, query in scenarios.items():
            results[name] = pd.read_sql(query, self.conn)
        return results

    def visualize(self, summary_df):
        """Phase 4: Data Visualization for Stakeholders"""
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x='Cust_Tier', y='Total_AUD', data=summary_df, palette='magma')
        plt.title('Total Cash Risk Exposure by Customer Tier', fontsize=15)
        plt.ylabel('Total Amount (AUD)')
        plt.savefig("aml_risk_summary.png")
        plt.show()

# --- Execution ---
if __name__ == "__main__":
    sys = AMLSystem()
    print("Step 1: Ingesting Data...")
    raw_cust, raw_txn = sys.generate_data()
    
    print("Step 2: Processing ETL...")
    sys.process_data(raw_cust, raw_txn)
    
    print("Step 3: Running Monitoring Scenarios...")
    alerts = sys.run_scenarios()
    
    for alert_name, df in alerts.items():
        print(f"\n[ALERT] {alert_name} (Total: {len(df)})")
        print(df.head())

    print("\nStep 4: Generating Visualization...")
    sys.visualize(alerts["Cash Volume Summary by Tier"])
