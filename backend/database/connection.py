"""Database connection manager for DuckDB."""
import duckdb
from pathlib import Path

class DatabaseConnection:
    """Manages DuckDB database connection and initialization."""
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        """Singleton pattern for database connection."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize database connection."""
        if self._connection is None:
            db_path = Path(__file__).parent / "research_copilot.db"
            self._connection = duckdb.connect(str(db_path))
            self._initialize_schema()
    
    def _initialize_schema(self):
        """Initialize database schema from schema.sql."""
        schema_path = Path(__file__).parent / "schema.sql"
        if schema_path.exists():
            with open(schema_path, 'r') as f:
                schema_sql = f.read()
                for statement in schema_sql.split(';'):
                    if statement.strip():
                        try:
                            self._connection.execute(statement)
                        except Exception:
                            pass
    
    def get_connection(self):
        """Get database connection.
        
        Returns:
            duckdb.DuckDBPyConnection: Database connection instance.
        """
        return self._connection

def get_db():
    """Get database connection instance.
    
    Returns:
        duckdb.DuckDBPyConnection: Database connection.
    """
    return DatabaseConnection().get_connection()
