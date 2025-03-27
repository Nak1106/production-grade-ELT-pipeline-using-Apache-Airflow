from airflow import DAG
from airflow.decorators import task
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from datetime import datetime

def return_snowflake_conn():
    hook = SnowflakeHook(snowflake_conn_id='snowflake_conn')
    conn = hook.get_conn()
    return conn.cursor()

@task
def creating_session_channel_table():
    cur = return_snowflake_conn()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dev.raw.user_session_channel (
            userId INT NOT NULL,
            sessionId VARCHAR(32) PRIMARY KEY,
            channel VARCHAR(32) DEFAULT 'direct'
        );
    """)
    cur.connection.commit()

@task
def creating_session_timestamp_table():
    cur = return_snowflake_conn()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dev.raw.session_timestamp (
            sessionId VARCHAR(32) PRIMARY KEY,
            ts TIMESTAMP  
        );
    """)
    cur.connection.commit()

@task
def populating_tables():
    cur = return_snowflake_conn()
    # Set context
    cur.execute("USE WAREHOUSE COMPUTE_WH;") 
    cur.execute("USE DATABASE dev;")
    cur.execute("USE SCHEMA raw;")

    # Create the stage
    cur.execute("""
        CREATE OR REPLACE STAGE dev.raw.blob_stage
        URL = 's3://s3-geospatial/readonly/'
        FILE_FORMAT = (TYPE = CSV, SKIP_HEADER = 1, FIELD_OPTIONALLY_ENCLOSED_BY = '"');
    """)
    cur.connection.commit()

    # Copy data into user_session_channel
    cur.execute("""
        COPY INTO dev.raw.user_session_channel
        FROM @dev.raw.blob_stage/user_session_channel.csv
        FILE_FORMAT = (TYPE = 'CSV', SKIP_HEADER = 1, FIELD_OPTIONALLY_ENCLOSED_BY='"');
    """)

    # Copy data into session_timestamp
    cur.execute("""
        COPY INTO dev.raw.session_timestamp
        FROM @dev.raw.blob_stage/session_timestamp.csv
        FILE_FORMAT = (TYPE = 'CSV', SKIP_HEADER = 1, FIELD_OPTIONALLY_ENCLOSED_BY='"');
    """)

    cur.connection.commit()

with DAG(
    dag_id='Session_Summary_ETL',
    start_date=datetime(2025, 3, 21),
    catchup=False,
    tags=['ETL_user_activity'],
    schedule_interval='30 3 * * *'  # Runs daily at 03:30 UTC
) as dag:
    creating_session_channel_table() >> creating_session_timestamp_table() >> populating_tables()
