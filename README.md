Creating a `README.md` file is a great way to provide documentation for your project. Here's a template for the `README.md` that you can customize based on your project details:

---

# ELT Summary Airflow Project

## Overview

This project is an **Airflow-based ETL/ELT pipeline** that processes user session data. It leverages Snowflake for data storage and transformations. The pipeline includes tasks such as creating temporary tables, performing primary key checks, checking for duplicate rows, and swapping tables for production-ready datasets.

### Key Features
- Extract data from Snowflake.
- Perform **Create Table As Select (CTAS)** for user session data.
- Run **primary key uniqueness checks** and ensure there are no duplicates.
- Swap the temporary table with the main table.

---

## Requirements

1. **Airflow** (configured with Docker)
2. **Snowflake** (with necessary credentials)
3. **Python** (for custom operations and hooks)
4. **GitHub** (for version control)

---

## Installation

### Prerequisites

- You need to have **Docker** and **Airflow** installed and running in your development environment.
- A **Snowflake account** with appropriate credentials (user, password, warehouse, database, schema).

### Steps to Set Up the Project

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Nak1106/Assignment_6.git
   cd your-repository-name
   ```

2. **Install required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Snowflake connection in Airflow:**
   Ensure that you have configured the Snowflake connection (`snowflake_conn`) in Airflow's UI or `connections` configuration file.

4. **Run Airflow:**
   If you are using Docker, ensure Airflow is running:
   ```bash
   docker-compose up -d
   ```

---

## How It Works

1. **CTAS (Create Table As Select)**: 
   - The `run_ctas` task creates a temporary table in Snowflake by selecting data from two tables (`user_session_channel` and `session_timestamp`).
   - The SQL is customizable and can be edited for different data sources.

2. **Primary Key Check**: 
   - The pipeline ensures that the `sessionId` field is unique in the generated table. If duplicates are found, the pipeline will raise an error.

3. **Duplicate Check**: 
   - After creating the temporary table, the pipeline checks for any duplicate rows by comparing the total row count with the distinct row count.

4. **Table Swap**:
   - Once the temporary table is validated, it is swapped with the existing main table, making the new data available for use.

---

## Example DAG

```python
from airflow.decorators import task
from airflow import DAG
from datetime import datetime

@task
def run_ctas(database, schema, table, select_sql, primary_key=None):
    # Function implementation goes here
    pass

with DAG(
    dag_id='ELT_Summary',
    start_date=datetime(2024, 10, 3),
    schedule='45 3 * * *'
) as dag:

    database = "dev"
    schema = "analytics"
    table = "session_summary"
    select_sql = """SELECT u.*, s.ts
    FROM dev.raw.user_session_channel u
    JOIN dev.raw.session_timestamp s ON u.sessionId=s.sessionId
    """
    run_ctas(database, schema, table, select_sql, primary_key='sessionId')
```  
