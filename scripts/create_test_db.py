import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import urllib.parse as urlparse


def create_test_database():
    # Fetch the test database URL from environment variables
    TEST_DATABASE_URL = os.getenv(
        "TEST_DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/data_db_test",
    )

    # Parse the URL to extract connection parameters
    url = urlparse.urlparse(TEST_DATABASE_URL)
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

    try:
        # Connect to the default 'postgres' database to create the test database
        conn = psycopg2.connect(
            dbname="postgres", user=user, password=password, host=host, port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Check if the test database already exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{dbname}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE DATABASE {dbname};")
            print(f"Test database '{dbname}' created successfully.")
        else:
            print(f"Test database '{dbname}' already exists.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating test database: {e}")
        exit(1)


if __name__ == "__main__":
    create_test_database()
