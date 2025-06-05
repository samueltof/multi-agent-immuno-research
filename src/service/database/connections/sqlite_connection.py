import pandas as pd
import threading
from typing import List, Any, Tuple
from pathlib import Path
from src.config.logger import logger
from src.config.database import DatabaseSettings
from src.service.database.database_connection import DatabaseConnection


class SQLiteConnection(DatabaseConnection):
    def __init__(self, settings: DatabaseSettings):
        logger.info("⎄ Initializing SQLite connection")
        self.settings = settings
        # Use thread-local storage for the connection object
        self.thread_local = threading.local()
        # Ensure conn attribute doesn't exist directly on the instance initially
        # The connection will be stored under self.thread_local.conn
        self.db_path = self._resolve_db_path()

    def _resolve_db_path(self) -> str:
        # Get project root from current file location
        # Go up 5 levels from src/service/database/connections/sqlite_connection.py
        project_root = Path(__file__).parent.parent.parent.parent.parent
        
        db_path_str = "<path not specified or found>"

        if self.settings.sqlite_path:
            # Handle both absolute and relative paths
            if Path(self.settings.sqlite_path).is_absolute():
                db_path = Path(self.settings.sqlite_path)
            else:
                # Use relative path from project root
                db_path = project_root / self.settings.sqlite_path

            logger.info(f"Attempting database path: {db_path}")
            if db_path.exists():
                return str(db_path)
            else:
                # Keep track of the path tried for the error message
                db_path_str = str(db_path)

        raise FileNotFoundError(f"SQLite database not specified or not found at the checked path: {db_path_str}")

    def connect(self):
        logger.info(f"⎄ Connecting to SQLite database at {self.db_path}")
        try:
            import sqlite3
            
            # Check if connection already exists for this thread
            if not hasattr(self.thread_local, 'conn') or self.thread_local.conn is None:
                # SQLite connections should be per-thread
                self.thread_local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
                logger.info("⎄ Successfully connected to SQLite")
            
            return self.thread_local.conn
        except Exception as e:
            logger.error(f"Failed to connect to SQLite: {str(e)}")
            raise

    def execute_query(self, query: str) -> tuple[list[str], list[Any]]:
        try:
            # Get thread-local connection
            if not hasattr(self.thread_local, 'conn') or self.thread_local.conn is None:
                self.connect()
                
            cursor = self.thread_local.conn.cursor()
            cursor.execute(query)
            
            # Get column names and data
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            data = cursor.fetchall()
            return columns, data
        except Exception as e:
            logger.error(f"Failed to execute SQLite query: {str(e)}")
            raise

    def execute_query_df(self, query: str) -> pd.DataFrame:
        try:
            # Get thread-local connection
            if not hasattr(self.thread_local, 'conn') or self.thread_local.conn is None:
                self.connect()
                
            return pd.read_sql_query(query, self.thread_local.conn)
        except Exception as e:
            logger.error(f"Failed to execute SQLite query to DataFrame: {str(e)}")
            raise

    def close(self):
        """Close the database connection."""
        if hasattr(self.thread_local, 'conn') and self.thread_local.conn:
            self.thread_local.conn.close()
            self.thread_local.conn = None
            logger.info("⎄ SQLite connection closed")

    def __del__(self):
        """Cleanup on destruction."""
        try:
            self.close()
        except:
            # Ignore errors during cleanup
            pass
