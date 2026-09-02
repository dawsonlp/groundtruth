"""SQLite Single-File Persistence Adapter for GroundTruth Catalog."""

import json
from pathlib import Path
import sqlite3
from typing import Any, Dict, List, Optional

from groundtruth.adapters.base import DataRepository
from groundtruth.conceptual.models import BusinessTerm, PropertyConcept
from groundtruth.logical.entities import LogicalEntity


class SQLiteDataAdapter(DataRepository):
    """Stores GroundTruth conceptual and logical models in a single SQLite file."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS terms (
                    slug TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    definition TEXT NOT NULL,
                    data_json TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS entities (
                    uri TEXT PRIMARY KEY,
                    domain TEXT NOT NULL,
                    name TEXT NOT NULL,
                    conceptual_term_ref TEXT,
                    data_json TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_entities_domain ON entities(domain);
            """)

    def save_term(self, term: BusinessTerm) -> None:
        with self._get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO terms (slug, name, domain, definition, data_json) VALUES (?, ?, ?, ?, ?)",
                (term.slug, term.name, term.domain, term.definition, json.dumps(term.to_dict())),
            )

    def get_term(self, slug: str) -> Optional[BusinessTerm]:
        with self._get_connection() as conn:
            row = conn.execute("SELECT data_json FROM terms WHERE slug = ?", (slug,)).fetchone()
            if row:
                return BusinessTerm.from_dict(json.loads(row["data_json"]))
        return None

    def save_entity(self, entity: LogicalEntity) -> None:
        with self._get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO entities (uri, domain, name, conceptual_term_ref, data_json) VALUES (?, ?, ?, ?, ?)",
                (entity.uri, entity.domain, entity.name, entity.conceptual_term_ref, json.dumps(entity.to_dict())),
            )

    def get_entity(self, uri: str) -> Optional[LogicalEntity]:
        with self._get_connection() as conn:
            row = conn.execute("SELECT data_json FROM entities WHERE uri = ?", (uri,)).fetchone()
            if row:
                return LogicalEntity.from_dict(json.loads(row["data_json"]))
        return None

    def list_entities(self, domain: Optional[str] = None) -> List[LogicalEntity]:
        with self._get_connection() as conn:
            if domain:
                cursor = conn.execute("SELECT data_json FROM entities WHERE domain = ?", (domain,))
            else:
                cursor = conn.execute("SELECT data_json FROM entities")
            return [LogicalEntity.from_dict(json.loads(row["data_json"])) for row in cursor.fetchall()]

