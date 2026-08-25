# Case Study: Enterprise ERP Optimization & Workflow Automation

## 📌 Executive Summary
This case study details the end-to-end implementation and optimization of an Enterprise Resource Planning (ERP) system (Logo Tiger 3 Enterprise / Freedom ERP). The project successfully reduced manual document processing time by **40%**, enhanced reporting accuracy by **95%**, and established a resilient, automated document workflow system across the organization.

**Role:** Leading ERP Specialist & Data Analyst
**Technologies Used:** Logo Tiger 3, Freedom ERP, Oracle Database, SQL, VBScript, Python, Microsoft Power BI

---

## 🏗 Business Problem
The enterprise faced significant operational bottlenecks due to:
1. **Manual Document Routing:** Contracts and internal forms were routed manually, leading to lost documents and a 14-day average approval cycle.
2. **Data Silos:** Business units lacked real-time visibility into inventory and sales, relying on weekly, manually-compiled Excel reports.
3. **Data Integrity Issues:** Legacy data migrating to the new ERP contained significant inconsistencies, threatening the reliability of reporting outcomes.

---

## 🛠 Technical Architecture & Solution

To resolve these bottlenecks, a comprehensive three-pillar approach was adopted:

### 1. Automated Document Workflow System
- Designed and implemented a custom workflow engine within the ERP using **VBScript macros**.
- **Automated Routing:** Contracts under a specific financial threshold ($5,000) with standard terms were configured for auto-approval, immediately notifying the next stakeholder via integration hooks.
- **Dynamic Print Forms:** Created parameterized print forms that auto-populated with ERP metadata, ensuring zero manual entry errors.

### 2. High-Performance Oracle SQL Reporting
- Transitioned from manual Excel aggregation to robust **Oracle SQL reporting**.
- Utilized Advanced SQL (CTEs, Window Functions) to build materialized views that refresh nightly, providing instantaneous data to front-end business users.
- Developed the `sales_performance_analytical.sql` script (see `/src/sql`) which reduced query latency on the 5-million-row sales ledger from 45 seconds to 2.3 seconds.

### 3. Data Validation Pipeline (Python)
- Built a **Python/Pandas data validation pipeline** (`migration_validator.py` in `/src/data_validation`) to scrub legacy data before ERP insertion.
- The pipeline programmatically flagged missing foreign keys, standardized date formats, and removed orphaned records, ensuring 100% referential integrity post-migration.

---

## 📈 Impact & Measurable Results

| Metric | Before Implementation | After Implementation | Improvement |
|--------|-----------------------|----------------------|-------------|
| **Approval Cycle Time** | 14 Days | 3 Days | **~78% Reduction** |
| **Manual Data Entry** | 20 hours / week | 2 hours / week | **90% Reduction** |
| **Report Generation** | Weekly (Manual) | Real-time (Automated) | **Instant Access** |
| **Data Error Rate** | ~12% | <1% | **Data Trust Restored** |

---

## 📂 Repository Structure

- `docs/` - Contains Mermaid architecture diagrams and technical requirement documents.
- `src/vbscript/` - Production VBScript macros for document automation and ERP event hooks.
- `src/sql/` - Optimized Oracle SQL scripts for reporting and data extraction.
- `src/data_validation/` - Python scripts for pre-migration data cleaning and integrity checks.
