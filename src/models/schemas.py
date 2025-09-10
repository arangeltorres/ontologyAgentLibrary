"""Pydantic schemas for the database agent system."""

from __future__ import annotations
from typing import Optional, Literal, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

# ---------- Common Types ----------
DBType = Literal["snowflake", "postgres", "mysql", "databricks"]

class Conn(BaseModel):
    """Database connection model."""
    model_config = ConfigDict(extra='forbid', json_schema_extra={'additionalProperties': False})
    
    type: DBType
    # Snowflake
    account: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    warehouse: Optional[str] = None
    database: Optional[str] = None
    schema_name: Optional[str] = Field(None, alias='schema')
    role: Optional[str] = None
    # Postgres
    host: Optional[str] = None
    port: Optional[int] = 5432
    dbname: Optional[str] = None
    sslmode: Optional[str] = "prefer"
    # MySQL
    # Databricks
    databricks_server_hostname: Optional[str] = None
    databricks_http_path: Optional[str] = None
    databricks_token: Optional[str] = None

class SchemaArgs(BaseModel):
    """Arguments for schema operations."""
    model_config = ConfigDict(extra='forbid', json_schema_extra={'additionalProperties': False})
    
    conn: Conn
    database: Optional[str] = None
    schema_name: Optional[str] = Field(None, alias='schema')
    table: Optional[str] = None

class MetadataArgs(BaseModel):
    """Arguments for metadata operations."""
    model_config = ConfigDict(extra='forbid', json_schema_extra={'additionalProperties': False})
    
    conn: Conn
    level: Literal["table", "column"]
    database: Optional[str] = None
    schema_name: str = Field(alias='schema')
    table: str
    column: Optional[str] = None
    comment: Optional[str] = None
    tags: Optional[Dict[str, str]] = None  # Snowflake

class QueryArgs(BaseModel):
    """Arguments for SQL query execution."""
    model_config = ConfigDict(extra='forbid', json_schema_extra={'additionalProperties': False})
    
    conn: Conn
    sql: str
