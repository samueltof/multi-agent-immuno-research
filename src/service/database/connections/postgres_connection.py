import pandas as pd
from typing import List, Any, Tuple
from src.config.logger import logger
from src.config.database import DatabaseSettings
from src.service.database.database_connection import DatabaseConnection

# Import psycopg2 with optional handling
try:
    import psycopg2
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    psycopg2 = None


class PostgresConnection(DatabaseConnection):
    def __init__(self, settings: DatabaseSettings):
        logger.info("⎄ Initializing PostgreSQL connection")
        self.settings = settings
        self.conn = None
        
        if not PSYCOPG2_AVAILABLE:
            logger.warning("⎄ psycopg2 not available - PostgreSQL connections will not work")

    def connect(self):
        if not PSYCOPG2_AVAILABLE:
            raise ImportError("psycopg2 is required for PostgreSQL connections. Install with: pip install psycopg2-binary")
            
        logger.info(
            f"⎄ Connecting to PostgreSQL at {self.settings.host}:{self.settings.port}"
        )
        try:
            self.conn = psycopg2.connect(
                dbname=self.settings.database_name,
                user=self.settings.username,
                password=self.settings.password,
                host=self.settings.host,
                port=self.settings.port,
            )
            logger.info("⎄ Successfully connected to PostgreSQL")
            return self.conn
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {str(e)}")
            raise

    def execute_query(self, query: str) -> Tuple[List[str], List[Any]]:
        if not PSYCOPG2_AVAILABLE:
            raise ImportError("psycopg2 is required for PostgreSQL connections")
            
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            # Get column names and data
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            return columns, data
        except Exception as e:
            logger.error(f"Failed to execute PostgreSQL query: {str(e)}")
            raise

    def execute_query_df(self, query: str) -> pd.DataFrame:
        if not PSYCOPG2_AVAILABLE:
            raise ImportError("psycopg2 is required for PostgreSQL connections")
            
        try:
            return pd.read_sql_query(query, self.conn)
        except Exception as e:
            logger.error(f"Failed to execute PostgreSQL query to DataFrame: {str(e)}")
            raise
