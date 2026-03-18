from typing import Dict, List

from app.plugins.base import DomainPlugin


class TrainingPlugin(DomainPlugin):
    name = "training"

    def sample_evidence(self) -> List[Dict]:
        return [
            {
                "source": "training.dispatch",
                "payload": {
                    "category": "training",
                    "emergency": "fire_alarm",
                    "equipment": "partial_failure",
                    "personnel": "reduced",
                    "suggested_outcome": "priority_evacuation",
                    "message": "대피 우선 조치 시나리오",
                },
                "trust_score": 0.88,
                "timestamp": "2026-03-08T00:05:00Z",
            },
            {
                "source": "training.supervisor",
                "payload": {
                    "category": "training",
                    "emergency": "chemical_alert",
                    "equipment": "stable",
                    "personnel": "full",
                    "suggested_outcome": "zone_isolation_check",
                    "message": "격리 구역 점검 절차",
                },
                "trust_score": 0.79,
                "timestamp": "2026-03-08T00:06:00Z",
            },
        ]

    def context_hint(self) -> Dict:
        return {
            "user_role": "trainer",
            "environment": "high_risk",
            "scenario_profile": "training",
            "intent": "evacuate",
        }
