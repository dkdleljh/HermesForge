def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_demo_bootstrap_and_materialize_flow(client):
    boot = client.post("/api/demo/bootstrap")
    assert boot.status_code == 200
    assert boot.json()["evidence_count"] >= 6

    snapshots = client.get("/api/snapshots")
    assert snapshots.status_code == 200
    snapshot_id = snapshots.json()[0]["snapshot_id"]

    payload = {
        "snapshot_id": snapshot_id,
        "mode": "deterministic",
        "context": {
            "user_role": "trainer",
            "environment": "high_risk",
            "permissions": ["render"],
            "state_flags": {"urgency": "high"},
            "scenario_profile": "training",
            "intent": "evacuate",
        },
    }
    rendered = client.post("/api/materialize", json=payload)
    assert rendered.status_code == 200
    body = rendered.json()
    assert body["label"] == "POSSIBILITY_RENDER"
    assert body["provenance"]["watermark"] == "NOT_FACT"


def test_context_changes_output(client):
    snapshots = client.get("/api/snapshots")
    if not snapshots.json():
        client.post("/api/demo/bootstrap")
        snapshots = client.get("/api/snapshots")

    snapshot_id = snapshots.json()[0]["snapshot_id"]

    req_a = {
        "snapshot_id": snapshot_id,
        "mode": "weighted",
        "context": {
            "user_role": "teacher",
            "environment": "classroom",
            "permissions": ["render"],
            "state_flags": {"focus": "low"},
            "scenario_profile": "education",
            "intent": "review",
        },
    }
    req_b = {
        "snapshot_id": snapshot_id,
        "mode": "weighted",
        "context": {
            "user_role": "player",
            "environment": "field",
            "permissions": ["render"],
            "state_flags": {"resource": "low"},
            "scenario_profile": "game",
            "intent": "explore",
        },
    }

    a = client.post("/api/materialize", json=req_a).json()
    b = client.post("/api/materialize", json=req_b).json()

    assert a["context_hash"] != b["context_hash"]
