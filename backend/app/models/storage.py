"""SQLite 저장 스키마 초기화 SQL."""

DDL_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS evidence (
        id TEXT PRIMARY KEY,
        source TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        trust_score REAL NOT NULL,
        timestamp TEXT NOT NULL,
        hash TEXT NOT NULL,
        source_api TEXT,
        ttl INTEGER
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS lambda_patches (
        id TEXT PRIMARY KEY,
        conditions_json TEXT NOT NULL,
        outcome_json TEXT NOT NULL,
        probability_mass REAL NOT NULL,
        confidence REAL NOT NULL,
        constraint_proof TEXT NOT NULL,
        witness_refs_json TEXT NOT NULL,
        anchor_weight REAL NOT NULL,
        labels_json TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS snapshots (
        snapshot_id TEXT PRIMARY KEY,
        parent_snapshot_id TEXT,
        patches_json TEXT NOT NULL,
        policy_root TEXT NOT NULL,
        witness_root TEXT NOT NULL,
        entropy_budget REAL NOT NULL,
        created_at TEXT NOT NULL,
        version TEXT NOT NULL,
        duration INTEGER
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS rendered_events (
        render_id TEXT PRIMARY KEY,
        snapshot_id TEXT NOT NULL,
        context_hash TEXT NOT NULL,
        rendered_event_json TEXT NOT NULL,
        confidence REAL NOT NULL,
        policy_hash TEXT NOT NULL,
        provenance_json TEXT NOT NULL,
        label TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
    """,
]
