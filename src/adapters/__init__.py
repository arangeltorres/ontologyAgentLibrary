"""Adaptadores de base de datos."""

from .base import DBAdapter
from .factory import get_adapter

__all__ = ["DBAdapter", "get_adapter"]
