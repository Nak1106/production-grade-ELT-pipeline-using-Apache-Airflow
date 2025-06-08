# 🧾 ELT Summary with Airflow and Snowflake

This project showcases a **production-grade ELT pipeline using Apache Airflow** to process user session data. It performs SQL-based transformations on Snowflake using tasks such as table creation, primary key and duplicate validation, and safe table swapping for production deployment.

---

## 🚀 Key Features

- Automates **CTAS (Create Table As Select)** jobs  
- Performs **Primary Key uniqueness checks**  
- Detects and prevents **duplicate records**  
- Uses **Snowflake Table Swapping** to update production tables without downtime  
- Scheduled DAG runs with dependency control  

---

## ⚙️ Requirements

- Python 3.x  
- Docker & Docker Compose (for Airflow environment)  
- Apache Airflow  
- Snowflake account  
- Valid Snowflake connection in Airflow (`snowflake_conn`)  

---

## 🏗️ Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Nak1106/Assignment_6.git
cd Assignment_6
```

### 2. Install Python Requirements

```bash
pip install -r requirements.txt
```

### 3. Configure Airflow Connections

- Add `snowflake_conn` in the Airflow UI with your Snowflake credentials.  
- Alternatively, use Airflow CLI to add the connection.

### 4. Run Airflow (if using Docker)

```bash
docker-compose up -d
```

---

## 📊 Workflow Summary

### Session Data Ingestion DAG (`Session_Summary_ETL`)
- Creates base tables: `user_session_channel` and `session_timestamp`
- Stages and loads CSV files from S3 into Snowflake

### ELT Summary DAG (`ELT_Summary`)
- Creates a temporary summary table using a JOIN on session data
- Verifies:
  - **Primary Key Uniqueness** (`sessionId`)
  - **No Duplicate Records**
- If valid, swaps the temp table with the production table

---

## 🔍 Example SQL Logic

```sql
SELECT u.*, s.ts
FROM dev.raw.user_session_channel u
JOIN dev.raw.session_timestamp s ON u.sessionId = s.sessionId
```

---

## 📁 File Breakdown

| File                        | Purpose                                                                 |
|-----------------------------|-------------------------------------------------------------------------|
| `session_summary.py`        | DAG for CTAS, primary key check, deduplication, and table swapping      |
| `user_session_channel.py`   | DAG for table creation and data ingestion from S3                       |
| `requirements.txt`          | List of Python packages required for execution                          |
| `README.md`                 | This documentation file                                                 |

---

## 🧠 Learning Outcomes

- Build modular, scalable DAGs using Airflow  
- Use Snowflake’s advanced SQL capabilities (e.g., `STAGE`, `CTAS`, `SWAP`)  
- Implement data quality checks in production pipelines  
- Automate safe deployment of transformed data to production tables  

---

## 📅 DAG Scheduling

| DAG Name              | Schedule (UTC)     | Description                                     |
|-----------------------|--------------------|-------------------------------------------------|
| `Session_Summary_ETL` | Daily at 03:30 UTC | Creates raw tables and loads S3 data            |
| `ELT_Summary`         | Daily at 03:45 UTC | Runs CTAS, PK check, deduplication, table swap  |

---

## 👨‍💻 Author

**Nakshatra Desai**  
Graduate Student – MS Data Analytics @ San Jose State University  
📫 [LinkedIn](https://www.linkedin.com/in/nakshatra-desai-547a771b6/)

---

## 📌 Short Description (for GitHub Repo)

> End-to-end ELT pipeline using Airflow and Snowflake to create production-ready session summaries. Includes CTAS, primary key validation, deduplication, and safe table swaps.
