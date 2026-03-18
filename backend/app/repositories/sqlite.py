import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, List, Optional

from app.domain.entities import Evidence, LambdaPatch, RenderedEvent, Snapshot
from app.models.storage import DDL_STATEMENTS
from app.repositories.base import EvidenceRepository, PatchRepository, RenderedEventRepository, SnapshotRepository


class SQLiteUnit:
    """SQLite 연결과 스키마를 관리한다."""

    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    @contextmanager
    def connection(self) -> Generator[sqlite3.Connection, None, None]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self.connection() as conn:
            cursor = conn.cursor()
            for ddl in DDL_STATEMENTS:
                cursor.execute(ddl)


class SQLiteEvidenceRepository(EvidenceRepository):
    def __init__(self, unit: SQLiteUnit):
        self.unit = unit

    def create(self, evidence: Evidence) -> Evidence:
        with self.unit.connection() as conn:
            conn.execute(
                "INSERT INTO evidence (id, source, payload_json, trust_score, timestamp, hash, source_api, ttl) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (evidence.id, evidence.source, json.dumps(evidence.payload), evidence.trust_score, evidence.timestamp, evidence.hash, evidence.source_api, evidence.ttl),
            )
        return evidence

    def list_all(self) -> List[Evidence]:
        with self.unit.connection() as conn:
            rows = conn.execute("SELECT * FROM evidence ORDER BY timestamp DESC").fetchall()
        return [
            Evidence(
                id=row["id"],
                source=row["source"],
                payload=json.loads(row["payload_json"]),
                trust_score=row["trust_score"],
                timestamp=row["timestamp"],
                hash=row["hash"],
                source_api=row["source_api"],
                ttl=row["ttl"],
            )
            for row in rows
        ]

    def get(self, evidence_id: str) -> Optional[Evidence]:
        with self.unit.connection() as conn:
            row = conn.execute("SELECT * FROM evidence WHERE id = ?", (evidence_id,)).fetchone()
        if not row:
            return None
        return Evidence(
            id=row["id"],
            source=row["source"],
            payload=json.loads(row["payload_json"]),
            trust_score=row["trust_score"],
            timestamp=row["timestamp"],
            hash=row["hash"],
            source_api=row["source_api"],
            ttl=row["ttl"],
        )


class SQLitePatchRepository(PatchRepository):
    def __init__(self, unit: SQLiteUnit):
        self.unit = unit

    def create(self, patch: LambdaPatch) -> LambdaPatch:
        with self.unit.connection() as conn:
            conn.execute(
                """
                INSERT INTO lambda_patches
                (id, conditions_json, outcome_json, probability_mass, confidence, constraint_proof, witness_refs_json, anchor_weight, labels_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    patch.id,
                    json.dumps(patch.conditions),
                    json.dumps(patch.outcome),
                    patch.probability_mass,
                    patch.confidence,
                    patch.constraint_proof,
                    json.dumps(patch.witness_refs),
                    patch.anchor_weight,
                    json.dumps(patch.labels),
                ),
            )
        return patch

    def list_all(self) -> List[LambdaPatch]:
        with self.unit.connection() as conn:
            rows = conn.execute("SELECT * FROM lambda_patches").fetchall()
        return [
            LambdaPatch(
                id=row["id"],
                conditions=json.loads(row["conditions_json"]),
                outcome=json.loads(row["outcome_json"]),
                probability_mass=row["probability_mass"],
                confidence=row["confidence"],
                constraint_proof=row["constraint_proof"],
                witness_refs=json.loads(row["witness_refs_json"]),
                anchor_weight=row["anchor_weight"],
                labels=json.loads(row["labels_json"]),
            )
            for row in rows
        ]

    def get(self, patch_id: str) -> Optional[LambdaPatch]:
        with self.unit.connection() as conn:
            row = conn.execute("SELECT * FROM lambda_patches WHERE id = ?", (patch_id,)).fetchone()
        if not row:
            return None
        return LambdaPatch(
            id=row["id"],
            conditions=json.loads(row["conditions_json"]),
            outcome=json.loads(row["outcome_json"]),
            probability_mass=row["probability_mass"],
            confidence=row["confidence"],
            constraint_proof=row["constraint_proof"],
            witness_refs=json.loads(row["witness_refs_json"]),
            anchor_weight=row["anchor_weight"],
            labels=json.loads(row["labels_json"]),
        )


class SQLiteSnapshotRepository(SnapshotRepository):
    def __init__(self, unit: SQLiteUnit):
        self.unit = unit

    def create(self, snapshot: Snapshot) -> Snapshot:
        with self.unit.connection() as conn:
            conn.execute(
                """
                INSERT INTO snapshots
                (snapshot_id, parent_snapshot_id, patches_json, policy_root, witness_root, entropy_budget, created_at, version, duration)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    snapshot.snapshot_id,
                    snapshot.parent_snapshot_id,
                    json.dumps(snapshot.patches),
                    snapshot.policy_root,
                    snapshot.witness_root,
                    snapshot.entropy_budget,
                    snapshot.created_at,
                    snapshot.version,
                    snapshot.duration,
                ),
            )
        return snapshot

    def list_all(self) -> List[Snapshot]:
        with self.unit.connection() as conn:
            rows = conn.execute("SELECT * FROM snapshots ORDER BY created_at DESC").fetchall()
        return [
            Snapshot(
                snapshot_id=row["snapshot_id"],
                parent_snapshot_id=row["parent_snapshot_id"],
                patches=json.loads(row["patches_json"]),
                policy_root=row["policy_root"],
                witness_root=row["witness_root"],
                entropy_budget=row["entropy_budget"],
                created_at=row["created_at"],
                version=row["version"],
                duration=row["duration"],
            )
            for row in rows
        ]

    def get(self, snapshot_id: str) -> Optional[Snapshot]:
        with self.unit.connection() as conn:
            row = conn.execute("SELECT * FROM snapshots WHERE snapshot_id = ?", (snapshot_id,)).fetchone()
        if not row:
            return None
        return Snapshot(
            snapshot_id=row["snapshot_id"],
            parent_snapshot_id=row["parent_snapshot_id"],
            patches=json.loads(row["patches_json"]),
            policy_root=row["policy_root"],
            witness_root=row["witness_root"],
            entropy_budget=row["entropy_budget"],
            created_at=row["created_at"],
            version=row["version"],
            duration=row["duration"],
        )


class SQLiteRenderedEventRepository(RenderedEventRepository):
    def __init__(self, unit: SQLiteUnit):
        self.unit = unit

    def create(self, event: RenderedEvent) -> RenderedEvent:
        with self.unit.connection() as conn:
            conn.execute(
                """
                INSERT INTO rendered_events
                (render_id, snapshot_id, context_hash, rendered_event_json, confidence, policy_hash, provenance_json, label, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.render_id,
                    event.snapshot_id,
                    event.context_hash,
                    json.dumps(event.rendered_event),
                    event.confidence,
                    event.policy_hash,
                    json.dumps(event.provenance),
                    event.label,
                    event.timestamp,
                ),
            )
        return event

    def list_recent(self, limit: int = 10) -> List[RenderedEvent]:
        with self.unit.connection() as conn:
            rows = conn.execute(
                "SELECT * FROM rendered_events ORDER BY timestamp DESC LIMIT ?", (limit,)
            ).fetchall()
        return [
            RenderedEvent(
                render_id=row["render_id"],
                snapshot_id=row["snapshot_id"],
                context_hash=row["context_hash"],
                rendered_event=json.loads(row["rendered_event_json"]),
                confidence=row["confidence"],
                policy_hash=row["policy_hash"],
                provenance=json.loads(row["provenance_json"]),
                label=row["label"],
                timestamp=row["timestamp"],
            )
            for row in rows
        ]
