import pandas as pd
from typing import List, Any, Tuple
from src.config.logger import logger
from src.config.database import DatabaseSettings
from src.service.database.database_connection import DatabaseConnection

# Import mysql.connector with optional handling
try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    mysql = None


class MySQLConnection(DatabaseConnection):
    def __init__(self, settings: DatabaseSettings):
        logger.info("⎄ Initializing MySQL connection")
        self.settings = settings
        self.conn = None
        
        if not MYSQL_AVAILABLE:
            logger.warning("⎄ mysql-connector-python not available - MySQL connections will not work")

    def connect(self):
        if not MYSQL_AVAILABLE:
            raise ImportError("mysql-connector-python is required for MySQL connections. Install with: pip install mysql-connector-python")
            
        logger.info(
            f"⎄ Connecting to MySQL at {self.settings.host}:{self.settings.port}"
        )
        try:
            self.conn = mysql.connector.connect(
                database=self.settings.database_name,
                user=self.settings.username,
                password=self.settings.password,
                host=self.settings.host,
                port=self.settings.port,
            )
            logger.info("⎄ Successfully connected to MySQL")
            return self.conn
        except Exception as e:
            logger.error(f"Failed to connect to MySQL: {str(e)}")
            raise

    def execute_query(self, query: str) -> Tuple[List[str], List[Any]]:
        if not MYSQL_AVAILABLE:
            raise ImportError("mysql-connector-python is required for MySQL connections")
            
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            # Get column names and data
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            return columns, data
        except Exception as e:
            logger.error(f"Failed to execute MySQL query: {str(e)}")
            raise

    def execute_query_df(self, query: str) -> pd.DataFrame:
        if not MYSQL_AVAILABLE:
            raise ImportError("mysql-connector-python is required for MySQL connections")
            
        try:
            return pd.read_sql_query(query, self.conn)
        except Exception as e:
            logger.error(f"Failed to execute MySQL query to DataFrame: {str(e)}")
            raise
