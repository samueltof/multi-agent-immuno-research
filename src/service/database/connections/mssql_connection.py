import pandas as pd
from typing import List, Any, Tuple
from src.config.logger import logger
from src.config.database import DatabaseSettings
from src.service.database.database_connection import DatabaseConnection

# Import pyodbc at the module level for easier testing
try:
    import pyodbc
    PYODBC_AVAILABLE = True
except ImportError:
    PYODBC_AVAILABLE = False
    pyodbc = None


class MSSQLConnection(DatabaseConnection):
    # Constants for connection settings
    ENCRYPT = "yes"  # Changed from "Mandatory" to "yes" which is a valid value
    TRUST_SERVER_CERTIFICATE = "yes"  # Changed from "True" to "yes" which is a valid value
    CONNECTION_TIMEOUT = 15
    APPLICATION_INTENT = "ReadOnly"  # Changed from ReadWrite to ReadOnly

    def __init__(self, settings: DatabaseSettings):
        logger.info("⎄ Initializing MSSQL connection")
        self.settings = settings
        self.conn = None
        
        if not PYODBC_AVAILABLE:
            logger.warning("⎄ pyodbc not available - MSSQL connections will not work")

    def connect(self):
        if not PYODBC_AVAILABLE:
            raise ImportError("pyodbc is required for MSSQL connections")
            
        logger.info(
            f"⎄ Connecting to MSSQL at {self.settings.host}:{self.settings.port}"
        )
        try:
            # Build connection string with encryption settings
            connection_string = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.settings.host};"
                f"DATABASE={self.settings.database_name};"
                f"UID={self.settings.username};"
                f"PWD={self.settings.password};"
                f"Connection Timeout={self.CONNECTION_TIMEOUT};"
                f"Encrypt={self.ENCRYPT};"
                f"TrustServerCertificate={self.TRUST_SERVER_CERTIFICATE};"
                f"ApplicationIntent={self.APPLICATION_INTENT};"
            )
            
            self.conn = pyodbc.connect(connection_string)
            logger.info("⎄ Successfully connected to MSSQL")
            return self.conn
        except Exception as e:
            logger.error(f"Failed to connect to MSSQL: {str(e)}")
            raise

    def execute_query(self, query: str) -> Tuple[List[str], List[Any]]:
        if not PYODBC_AVAILABLE:
            raise ImportError("pyodbc is required for MSSQL connections")
            
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            # Get column names and data
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            return columns, data
        except Exception as e:
            logger.error(f"Failed to execute MSSQL query: {str(e)}")
            raise

    def execute_query_df(self, query: str) -> pd.DataFrame:
        if not PYODBC_AVAILABLE:
            raise ImportError("pyodbc is required for MSSQL connections")
            
        try:
            return pd.read_sql_query(query, self.conn)
        except Exception as e:
            logger.error(f"Failed to execute MSSQL query to DataFrame: {str(e)}")
            raise
