# Database Agent System

Modular system for interacting with different databases using AI agents with a flexible query base system.

## Project Structure

```
Ontology AgentsSDK/
├── src/
│   ├── __init__.py              # Main exports
│   ├── models/                  # Pydantic models
│   │   ├── __init__.py
│   │   └── schemas.py           # Data schemas
│   ├── adapters/                # Database adapters
│   │   ├── __init__.py
│   │   ├── base.py              # Abstract base class
│   │   ├── snowflake.py         # Snowflake adapter
│   │   ├── postgres.py          # PostgreSQL adapter
│   │   └── factory.py           # Adapter factory
│   ├── tools/                   # Agent tools
│   │   └── __init__.py          # Tool functions
│   ├── utils/                   # Utilities
│   │   └── __init__.py          # Utility functions
│   └── queries/                 # Query base system
│       ├── __init__.py          # Query manager
│       ├── snowflake/           # Snowflake queries
│       │   ├── queries.json     # Standard queries
│       │   └── custom_queries.json # Custom queries
│       ├── postgres/            # PostgreSQL queries
│       │   └── queries.json
│       ├── mysql/               # MySQL queries
│       │   └── queries.json
│       └── databricks/          # Databricks queries
│           └── queries.json
├── main.py                      # Main entry point
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## Usage

### Deterministic Mode
```bash
python main.py --mode det --action list_schema --payload_json '{
  "conn": {"type":"snowflake","account":"...","user":"...","password":"...","database":"ONT_TEST","schema":"PUBLIC"},
  "schema":"PUBLIC"
}'
```

### View Current Ontology
```bash
python main.py --mode det --action view_current_ontology --payload_json '{
  "conn": {"type":"snowflake","account":"...","user":"...","password":"...","database":"ONT_TEST","schema":"PUBLIC"}
}'
```

### Available Actions
- `list_schema`: List database schema information
- `update_metadata`: Update comments and metadata
- `execute_query`: Execute SQL queries
- `get_ontology`: Return foreign key relationships
- `view_current_ontology`: Get current ontology from knowledge graph storage

## Query Base System

The system includes a flexible query management system that allows you to:

### 1. Use Predefined Queries
Queries are stored in JSON files organized by database type:
- `src/queries/snowflake/queries.json` - Standard Snowflake queries
- `src/queries/postgres/queries.json` - Standard PostgreSQL queries
- `src/queries/mysql/queries.json` - Standard MySQL queries
- `src/queries/databricks/queries.json` - Standard Databricks queries

### 2. Add Custom Queries
You can add custom queries to extend functionality:
```json
{
  "custom_query_name": {
    "sql": "SELECT * FROM custom_table WHERE condition = '{param}'",
    "description": "Custom query description",
    "category": "optional_category"
  }
}
```

### 3. Parameter Substitution
Queries support parameter substitution using `{parameter_name}` syntax:
```json
{
  "filtered_tables": {
    "sql": "SELECT * FROM information_schema.tables WHERE table_schema = '{schema}' AND table_name LIKE '{pattern}'",
    "description": "Get tables matching pattern"
  }
}
```

### 4. Query Manager Usage
```python
from src.queries import query_manager

# Load queries for a database type
queries = query_manager.load_queries("snowflake")

# Get a specific query with parameters
query = query_manager.get_query("snowflake", "list_schema", 
                               database_filter="AND table_catalog = 'MY_DB'",
                               schema_filter="AND table_schema = 'PUBLIC'")

# List available queries
available = query_manager.list_available_queries("snowflake")
```

## Supported Databases
- ✅ Snowflake
- ✅ PostgreSQL
- 🚧 MySQL (queries ready, adapter pending)
- 🚧 Databricks (queries ready, adapter pending)

## Installation

```bash
pip install -r requirements.txt
```

## Features

- **Modular Architecture**: Clean separation of concerns
- **Query Base System**: Flexible JSON-based query management
- **Multi-Database Support**: Unified interface for different databases
- **Parameter Substitution**: Dynamic query building
- **Custom Query Support**: Easy extension with custom queries
- **Type Safety**: Full Pydantic model validation
- **Agent Integration**: Ready for AI agent frameworks