from enum import Enum
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings
import os
from typing import Optional

# Load environment variables
env_path = find_dotenv()
load_dotenv(dotenv_path=env_path)

class DatabaseType(Enum):
    POSTGRES = "postgres"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    ATHENA = "athena"
    BIGQUERY = "bigquery"
    MSSQL = "mssql"

class DatabaseSettings(BaseSettings):
    # Common settings
    database_type: DatabaseType = DatabaseType(os.getenv("DATABASE_TYPE", "sqlite"))
    database_name: Optional[str] = os.getenv("DATABASE_NAME")
    
    # Schema information
    database_schema_path: Optional[str] = os.getenv("DATABASE_SCHEMA_PATH")
    
    # AWS Athena specific
    s3_staging_dir: Optional[str] = os.getenv("S3_STAGING_DIR") 
    region_name: Optional[str] = os.getenv("AWS_REGION") 
    
    # SQL database specific
    host: Optional[str] = os.getenv("DB_HOST")
    port: Optional[int] = int(os.getenv("DB_PORT")) if os.getenv("DB_PORT") else None 
    username: Optional[str] = os.getenv("DB_USERNAME") 
    password: Optional[str] = os.getenv("DB_PASSWORD")
    local: bool = False
    
    # SQLite specific
    sqlite_path: Optional[str] = os.getenv("SQLITE_PATH", "data/database.db")
    
    # Vector database paths
    vector_db_path: str = os.getenv("VECTOR_DB_PATH", "data/lancedb") 
    query_examples_path: Optional[str] = os.getenv("QUERY_EXAMPLES_PATH")
    vector_table_name: str = os.getenv("VECTOR_TABLE_NAME", "sql_query_pairs")
    
    model_config = {
        "validate_assignment": True,
        "env_file": None,  # We handle .env loading manually above
        "extra": "ignore"
    } 