from typing import Dict, List

from app.plugins.base import DomainPlugin


class EducationPlugin(DomainPlugin):
    name = "education"

    def sample_evidence(self) -> List[Dict]:
        return [
            {
                "source": "edu.sensor",
                "payload": {
                    "category": "education",
                    "student_state": "fatigued",
                    "difficulty": "high",
                    "focus": 0.4,
                    "suggested_outcome": "review_session",
                    "message": "집중도 하락: 복습과 재설명 필요",
                },
                "trust_score": 0.76,
                "timestamp": "2026-03-08T00:00:00Z",
            },
            {
                "source": "edu.coach",
                "payload": {
                    "category": "education",
                    "student_state": "stable",
                    "difficulty": "medium",
                    "focus": 0.75,
                    "suggested_outcome": "advanced_practice",
                    "message": "심화 문제 풀이 추천",
                },
                "trust_score": 0.82,
                "timestamp": "2026-03-08T00:02:00Z",
            },
        ]

    def context_hint(self) -> Dict:
        return {
            "user_role": "teacher",
            "environment": "classroom",
            "scenario_profile": "education",
            "intent": "review",
        }
