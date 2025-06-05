import pandas as pd
from typing import List, Any, Tuple
from src.config.logger import logger
from src.config.database import DatabaseSettings
from src.service.database.database_connection import DatabaseConnection

# Import pyathena with optional handling
try:
    from pyathena import connect
    PYATHENA_AVAILABLE = True
except ImportError:
    PYATHENA_AVAILABLE = False
    connect = None


class AthenaConnection(DatabaseConnection):
    def __init__(self, settings: DatabaseSettings):
        logger.info("⎄ Initializing Athena connection")
        self.settings = settings
        self.conn = None
        
        if not PYATHENA_AVAILABLE:
            logger.warning("⎄ pyathena not available - Athena connections will not work")

    def connect(self):
        if not PYATHENA_AVAILABLE:
            raise ImportError("pyathena is required for Athena connections. Install with: pip install pyathena")
            
        logger.info(f"⎄ Connecting to Athena in region {self.settings.region_name}")
        try:
            self.conn = connect(
                s3_staging_dir=self.settings.s3_staging_dir,
                region_name=self.settings.region_name,
                schema_name=self.settings.database_name,
            )
            logger.info("⎄ Successfully connected to Athena")
            return self.conn
        except Exception as e:
            logger.error(f"Failed to connect to Athena: {str(e)}")
            raise

    def execute_query(self, query: str) -> Tuple[List[str], List[Any]]:
        if not PYATHENA_AVAILABLE:
            raise ImportError("pyathena is required for Athena connections")
            
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            # Get column names and data
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            return columns, data
        except Exception as e:
            logger.error(f"Failed to execute Athena query: {str(e)}")
            raise

    def execute_query_df(self, query: str) -> pd.DataFrame:
        if not PYATHENA_AVAILABLE:
            raise ImportError("pyathena is required for Athena connections")
            
        try:
            return pd.read_sql_query(query, self.conn)
        except Exception as e:
            logger.error(f"Failed to execute Athena query to DataFrame: {str(e)}")
            raise
