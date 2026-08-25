# Case Study: End-to-End Data Analytics & BI Platform

## 📌 Executive Summary
This case study demonstrates the architecture and implementation of a modern, automated data analytics pipeline and Business Intelligence (BI) platform. By replacing scattered, manual Excel reporting with a robust ETL pipeline (Python/Pandas), statistical modeling (R), and dynamic dashboards (Power BI / SSRS), the project empowered product development strategies with data-backed insights.

**Role:** Data Analyst / ERP Specialist
**Technologies Used:** Python, R, Microsoft Power BI, SSRS, SQL (Oracle/PostgreSQL), Docker, PyTest

---

## 🏗 Business Problem
At a leading multi-facility industrial manufacturing conglomerate, customer feedback and product defect data were scattered across siloed systems. 
- **The Issue:** Product teams had no consolidated view of customer satisfaction. Analysis was done manually in Excel, taking 3 days to compile each month.
- **The Risk:** Delayed responses to negative customer trends resulted in missed opportunities for product refinement and resource allocation.

---

## 🛠 Technical Architecture & Solution

### 1. Robust Python ETL Pipeline (`/src/python_etl`)
Instead of manual data dumps, a Python-based ETL pipeline was constructed.
- **Extraction & Cleaning:** `transform.py` loads raw CSV/SQL data, imputes missing values, and strictly validates data types.
- **Feature Engineering:** Derives new time-series dimensions and maps heuristic sentiment categories to unstructured feedback text.
- **Testing:** Implemented automated PyTest unit tests (`/tests/test_transform.py`) to guarantee pipeline reliability before pushing data to the warehouse.
- **High-Performance Export:** Outputs cleansed data to `.parquet` format for fast ingestion.

### 2. Statistical Trend Modeling in R (`/src/r_statistics`)
While dashboards show "what" happened, statistical models show "why" and "what's next".
- **Time Series Forecasting:** Used `auto.arima()` to forecast customer satisfaction trends 6 months into the future.
- **Hypothesis Testing:** Automated T-Tests to determine if month-over-month drops in ratings were statistically significant or just random noise, preventing knee-jerk business reactions.

### 3. Power BI & Advanced DAX (`/powerbi`)
- Deployed a standardized corporate aesthetic using a custom JSON theme.
- Utilized complex DAX (Data Analysis Expressions) for rolling averages, dynamic YoY comparisons, and churn-risk flagging.
- *See `DAX_Measures.md` for code examples of the business logic implemented.*

### 4. Scalable Infrastructure (`/infrastructure`)
- Provided a `docker-compose.yml` to instantly spin up Oracle (simulating the ERP) and PostgreSQL (the Data Warehouse) for local testing and CI/CD integration.

---

## 📈 Impact & Measurable Results

- **Time Savings:** Reduced reporting compilation time from **3 days to fully automated (0 hours)**.
- **Strategic Impact:** The R statistical models identified a significant drop in ratings for a flagship product, allowing management to reallocate engineering resources 2 months earlier than previous cycles.
- **Data Quality:** The PyTest-backed ETL pipeline caught and isolated 15% of bad legacy data before it ever reached the dashboard.
