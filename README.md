# 📊 Customer Segmentation using RFM Analysis

> **Transforming raw transaction data into actionable business insights**  
> Built with Python • Pandas • SQLite • Excel

---

## 📌 Project Overview

Understanding customer behaviour is the foundation of smart business decisions. In this project, I applied **RFM Analysis** — a proven method to categorise customers based on their purchasing habits — to identify who the most valuable customers are, who needs attention, and who may be at risk of leaving.

This end-to-end solution covers **data loading → calculation → scoring → segmentation → database storage → advanced querying**.

---

## 🧠 What is RFM Analysis?

| Metric | Full Name | Meaning |
|---|---|---|
| **R** — Recency | Days since last purchase | More recent = higher value |
| **F** — Frequency | Total number of purchases | More purchases = higher value |
| **M** — Monetary | Total amount spent | Higher spend = higher value |

Each customer receives a score from **1 to 5** (5 = best), which is then combined to assign them to a meaningful segment.

---

## 🏷️ Customer Segments

| Segment | Description |
|---|---|
| 🏆 **Champions** | Highest scores across all metrics — most valuable, active, and spending well |
| 💎 **Loyal Customers** | Regular buyers who have purchased recently |
| 💰 **High Spenders** | Purchase frequently and contribute significant revenue |
| ✅ **Active** | Engaged customers with steady purchasing behaviour |
| ⚠️ **At Risk** | Previously active customers who haven't purchased recently |
| ❌ **Lost** | Customers who haven't purchased in a long time — opportunity to re-engage |
| 🆕 **New** | Recently onboarded or less-engaged customers to nurture |

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|---|---|
| **Python 3** | Core programming language |
| **Pandas** | Data manipulation, grouping, and transformation |
| **SQLite** | Relational database storage, table joins, and aggregation |
| **Excel (.xlsx)** | Data input and deliverable output files |
| **Methodology** | RFM modelling, quantile ranking, custom business logic |

---

---

## 🔄 Workflow

### Step 1 — Load & Prepare Data
- Read Excel file and inspect columns
- Convert `InvoiceDate` to datetime format
- Identify the most recent transaction date

### Step 2 — Calculate RFM Metrics
- Group records by `Customer ID`
- **Recency**: Days since last purchase
- **Frequency**: Count of unique invoices
- **Monetary**: Sum of total spend

### Step 3 — Assign Scores
- Rank customers using `pd.qcut` into 5 equal groups
- Recency: fewer days = higher score
- Frequency & Monetary: higher values = higher score

### Step 4 — Segment Customers
- Apply custom business rules via a Python function
- Assign each customer to one of 7 segments
- Generate summary counts per segment

### Step 5 — Export Results
- Save segmented data to Excel for business use

### Step 6 — Build SQL Database
- Create **two linked tables**:
  - `rfm_data` → RFM metrics + segment labels
  - `customers` → Customer ID + Country information
- Establish relationship using `CustomerID`

### Step 7 — Run Advanced Queries
- **INNER JOIN** → Combine customer details with RFM data
- **GROUP BY** → Count customers by country and segment
- **Filter & Sort** → Identify top-spending active customers

---

## 📊 Key Results

*(Update with your actual numbers after running the code!)*

| Segment | Number of Customers |
|---|---:|
| 🏆 Champions | — |
| 💎 Loyal Customers | — |
| 💰 High Spenders | — |
| ✅ Active | — |
| ⚠️ At Risk | — |
| ❌ Lost | — |
| 🆕 New | — |
| **Total** | **—** |

---
## 📁 Project Structure
Customer-Segmentation-using-RFM-Analysis/
│
├── rfm_analysis.py                      # Complete RFM analysis code
│
├── customer_rfm_data.xlsx               # Calculated RFM metrics
├── customer_segments_final.xlsx         # Final segmented customer results
├── customer_database.db                 # SQLite database
│
├── Data Loading.png                     # Screenshot: Data loaded successfully
├── RFM Calculation.png                  # Screenshot: RFM metrics table
├── Segment Summary.png                  # Screenshot: Count per segment
├── Segment + Country Summary.png         # Screenshot: Country & segment breakdown
├── SQL Join result table.png            # Screenshot: INNER JOIN query output
├── Tables in Database.png                # Screenshot: Database tables list
├── Customer_database.png                 # Screenshot: Database saved confirmation
│
├── README.md                             # Project documentation & explanation
└── LICENSE                               # MIT License

## 🎥 Walkthrough Video

Watch the full step-by-step explanation and code run-through on LinkedIn:
👉 **[Paste your video link here]**

---

## 📬 Connect With Me

- **LinkedIn**: [linkedin.com/in/your-profile](https://linkedin.com/in/your-profile)
- **GitHub**: [github.com/your-username](https://github.com/your-username)
- **Email**: your.email@example.com

---

*Built by **Shumaila Liaqat** — Data Analyst • Python • SQL • Power BI*  
*Turning data into insights, one project at a time.* 🚀
