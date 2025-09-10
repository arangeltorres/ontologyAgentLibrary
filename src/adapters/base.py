"""Clase base para adaptadores de base de datos."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..models.schemas import MetadataArgs

class DBAdapter(ABC):
    """Interfaz base para adaptadores de base de datos."""
    
    @abstractmethod
    def list_schema(self, database=None, schema=None, table=None) -> List[Dict[str, Any]]:
        """Lista el esquema de la base de datos."""
        raise NotImplementedError
    
    @abstractmethod
    def update_metadata(self, args: MetadataArgs) -> str:
        """Actualiza metadatos de tabla o columna."""
        raise NotImplementedError
    
    @abstractmethod
    def run_query(self, sql: str) -> List[Dict[str, Any]]:
        """Ejecuta una consulta SQL."""
        raise NotImplementedError
    
    @abstractmethod
    def ontology(self, database=None, schema=None) -> Dict[str, Any]:
        """Devuelve la ontología (relaciones FK) de la base de datos."""
        raise NotImplementedError
