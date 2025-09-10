"""Factory para crear adaptadores de base de datos."""

from .base import DBAdapter
from .snowflake import SnowflakeAdapter
from .postgres import PostgresAdapter
from ..models.schemas import Conn

def get_adapter(conn: Conn) -> DBAdapter:
    """Crea un adaptador de base de datos basado en el tipo de conexión."""
    if conn.type == "snowflake":
        return SnowflakeAdapter(conn)
    if conn.type == "postgres":
        return PostgresAdapter(conn)
    # TODO: mysql, databricks
    raise ValueError(f"DB no soportada aún: {conn.type}")
