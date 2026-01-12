"""
Database Configuration File
Supports MySQL and SQLite
Used for storing cleaned & processed job acceptance data
"""

# ===============================
# MYSQL CONFIGURATION
# ===============================
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_mysql_password",
    "database": "job_acceptance_db",
    "port": 3306
}

# ===============================
# SQLITE CONFIGURATION (OPTIONAL)
# ===============================
SQLITE_DB_PATH = "database/job_acceptance.db"

# ===============================
# TABLE NAME
# ===============================
TABLE_NAME = "job_acceptance"
