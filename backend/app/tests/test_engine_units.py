from app.domain.entities import Context, LambdaPatch, Snapshot
from app.engine.materializer import BayesianNetworkMaterializer
from app.engine.merger import PolicyAwareMerger
from app.policies.safety_kernel import SafetyKernel


def _patch(pid: str, category: str, action: str, confidence: float):
    return LambdaPatch(
        id=pid,
        conditions={"x": 1},
        outcome={"category": category, "action": action, "message": action},
        probability_mass=0.7,
        confidence=confidence,
        constraint_proof="test",
        witness_refs=["ev-1"],
        anchor_weight=1.0,
        labels=[category],
    )


def test_materialize_deterministic_prefers_best_score():
    materializer = BayesianNetworkMaterializer()
    snapshot = Snapshot("ss-1", None, ["a", "b"], "p", "w", 1.0, "now", "0.1.0")
    context = Context("trainer", "high_risk", ["render"], {}, "training", "evacuate")
    selected = materializer.materialize(
        snapshot,
        context,
        [_patch("a", "training", "priority_evacuation", 0.8), _patch("b", "game", "loot", 0.6)],
        "deterministic",
    )
    assert selected.id == "a"


def test_merge_blocks_forbidden_categories():
    merger = PolicyAwareMerger()
    left = Snapshot("l", None, [], "p", "w", 1.0, "now", "0.1.0")
    right = Snapshot("r", None, [], "p", "w", 1.0, "now", "0.1.0")
    merged = merger.merge(left, right, [_patch("a", "harmful", "x", 0.6)], [_patch("b", "game", "y", 0.8)])
    assert [m.id for m in merged] == ["b"]


def test_safety_policy_enforces_watermark_and_label():
    from app.domain.entities import RenderedEvent

    event = RenderedEvent(
        render_id="re-1",
        snapshot_id="ss-1",
        context_hash="ctx",
        rendered_event={"category": "education", "action": "review"},
        confidence=0.8,
        policy_hash="",
        provenance={},
        label="",
        timestamp="now",
    )
    safe = SafetyKernel().apply(event)
    assert safe.label == "POSSIBILITY_RENDER"
    assert safe.provenance["watermark"] == "NOT_FACT"
