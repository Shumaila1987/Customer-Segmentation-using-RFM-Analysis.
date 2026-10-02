import pandas as pd
from datetime import datetime

# File is in the SAME folder — simple name only!
df = pd.read_excel("online_retail_ready.xlsx")

print("✅ File loaded successfully!")
print("\n--- Column Names ---")
print(df.columns.tolist())

# Convert date
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
latest_date = df['InvoiceDate'].max()
print(f"\nLatest date in data: {latest_date}")

# Calculate RFM
rfm = df.groupby('Customer ID').agg({
    'InvoiceDate': lambda x: (latest_date - x.max()).days,  # Recency
    'Invoice': 'nunique',                                      # Frequency
    'SpendPerRow': 'sum'                                       # Monetary
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

print("\n--- RFM Results ---")
print(rfm.head())

# Save
rfm.to_excel("customer_rfm_data.xlsx", index=False)
print("\n✅ Saved: customer_rfm_data.xlsx")
# --- CUSTOMER SEGMENTATION ---
# Assign scores: 5 = best, 1 = needs attention
rfm['R_Score'] = pd.qcut(rfm['Recency'].rank(method='first'), 5, labels=['5','4','3','2','1'])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=['1','2','3','4','5'])
rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), 5, labels=['1','2','3','4','5'])

# Combine scores into one code
rfm['RFM_Code'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

# Name each customer group
def label_segment(row):
    r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
    if r == '5' and f == '5' and m == '5':
        return '🏆 Champions'
    elif r in ['4','5'] and f in ['4','5']:
        return '💎 Loyal Customers'
    elif r == '5' and m in ['4','5']:
        return '💰 High Spenders'
    elif r in ['3','4','5']:
        return '✅ Active'
    elif r in ['1','2'] and f in ['4','5']:
        return '⚠️ At Risk'
    elif r in ['1','2']:
        return '❌ Lost'
    else:
        return '🆕 New'
rfm['Segment'] = rfm.apply(label_segment, axis=1)
# Show results
print("\n" + "="*50)
print("📊 FINAL CUSTOMER SEGMENTATION")
print("="*50)
print(rfm[['CustomerID','Recency','Frequency','Monetary','Segment']].head(10))

# Count how many in each group
print("\n" + "="*50)
print("📈 SEGMENT SUMMARY")
print("="*50)
print(rfm['Segment'].value_counts())

# Save final file
rfm.to_excel("customer_segments_final.xlsx", index=False)
print("\n✅ Final file saved: customer_segments_final.xlsx")
import sqlite3

# Create database connection
conn = sqlite3.connect('customer_database.db')

# Save RFM data as SQL table
rfm.to_sql('rfm_data', conn, if_exists='replace', index=False)

# Also save original customer info as separate table
df[['Customer ID', 'Country']].drop_duplicates().to_sql('customers', conn, if_exists='replace', index=False)

# JOIN both tables — show customer + their RFM + country
query = """
SELECT 
    c."Customer ID",
    c.Country,
    r.Recency,
    r.Frequency,
    r.Monetary,
    r.Segment
FROM customers c
INNER JOIN rfm_data r 
    ON c."Customer ID" = r.CustomerID
LIMIT 10
"""

print("\n" + "="*60)
print("🔍 SQL JOIN RESULT — Customer + Country + RFM + Segment")
print("="*60)
sql_result = pd.read_sql(query, conn)
print(sql_result)

conn.close()
print("\n✅ SQL database created: customer_database.db")
# === SQL DATABASE & JOINS ===
import sqlite3

# Connect to/create database
conn = sqlite3.connect('customer_database.db')

# 1. Save RFM data as SQL table
rfm.to_sql('rfm_data', conn, if_exists='replace', index=False)

# 2. Create separate Customers table (Customer ID + Country)
customers_table = df[['Customer ID', 'Country']].drop_duplicates()
customers_table.to_sql('customers', conn, if_exists='replace', index=False)

# 3. INNER JOIN — Combine both tables
sql_query = """
SELECT 
    c."Customer ID",
    c.Country,
    r.Recency,
    r.Frequency,
    r.Monetary,
    r.Segment
FROM customers c
INNER JOIN rfm_data r 
    ON c."Customer ID" = r.CustomerID
LIMIT 15
"""

print("\n" + "="*70)
print("🔍 SQL INNER JOIN — Customers + RFM + Segments")
print("="*70)
joined_result = pd.read_sql(sql_query, conn)
print(joined_result)

# Also show how many per country + segment
summary_query = """
SELECT 
    Country,
    Segment,
    COUNT(*) AS Total_Customers
FROM customers c
JOIN rfm_data r ON c."Customer ID" = r.CustomerID
GROUP BY Country, Segment
ORDER BY Country, Total_Customers DESC
LIMIT 10
"""
print("\n" + "="*70)
print("📊 Country + Segment Summary")
print("="*70)
summary_result = pd.read_sql(summary_query, conn)
print(summary_result)
# ==============================================
# 📊 YOUR SQL QUERIES
# ==============================================

# Query 1: View all customers with their country
print("\n--- ALL CUSTOMERS ---")
query1 = """
SELECT "Customer ID", Country
FROM customers
LIMIT 10
"""
result1 = pd.read_sql(query1, conn)
print(result1)

# Query 2: View full RFM data with segments
print("\n--- FULL RFM DATA ---")
query2 = """
SELECT CustomerID, Recency, Frequency, Monetary, Segment
FROM rfm_data
LIMIT 15
"""
result2 = pd.read_sql(query2, conn)
print(result2)

# Query 3: JOIN both tables — Customer + Country + RFM + Segment
print("\n--- CUSTOMER FULL PROFILE ---")
query3 = """
SELECT 
    c."Customer ID",
    c.Country,
    r.Recency,
    r.Frequency,
    r.Monetary,
    r.Segment
FROM customers c
INNER JOIN rfm_data r 
    ON c."Customer ID" = r.CustomerID
LIMIT 10
"""
result3 = pd.read_sql(query3, conn)
print(result3)

# Query 4: Count customers in each segment
print("\n--- CUSTOMERS PER SEGMENT ---")
query4 = """
SELECT 
    Segment,
    COUNT(*) AS Total_Customers,
    ROUND(AVG(Monetary), 2) AS Avg_Spending
FROM rfm_data
GROUP BY Segment
ORDER BY Total_Customers DESC
"""
result4 = pd.read_sql(query4, conn)
print(result4)

# Query 5: Champions only — your best customers
print("\n--- 🏆 CHAMPIONS ---")
query5 = """
SELECT *
FROM rfm_data
WHERE Segment = '🏆 Champions'
ORDER BY Monetary DESC
LIMIT 10
"""
result5 = pd.read_sql(query5, conn)
print(result5)

# Query 6: At Risk / Lost customers who need attention
print("\n--- ⚠️ AT RISK & LOST ---")
query6 = """
SELECT 
    c."Customer ID",
    c.Country,
    r.Recency,
    r.Monetary,
    r.Segment
FROM customers c
JOIN rfm_data r ON c."Customer ID" = r.CustomerID
WHERE r.Segment IN ('⚠️ At Risk', '❌ Lost')
ORDER BY r.Recency DESC
LIMIT 15
"""
result6 = pd.read_sql(query6, conn)
print(result6)

# Query 7: Total revenue by segment
print("\n--- 💰 TOTAL REVENUE BY SEGMENT ---")
query7 = """
SELECT 
    Segment,
    COUNT(*) AS Number_of_Customers,
    SUM(Monetary) AS Total_Revenue
FROM rfm_data
GROUP BY Segment
ORDER BY Total_Revenue DESC
"""
result7 = pd.read_sql(query7, conn)
print(result7)

conn.close()
print("\n✅ Done! Database saved: customer_database.db")
# === PURE SQL QUERIES — View directly in SQL ===
