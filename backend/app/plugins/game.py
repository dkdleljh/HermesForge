from typing import Dict, List

from app.plugins.base import DomainPlugin


class GamePlugin(DomainPlugin):
    name = "game"

    def sample_evidence(self) -> List[Dict]:
        return [
            {
                "source": "game.world",
                "payload": {
                    "category": "game",
                    "weather": "storm",
                    "resources": "low",
                    "player_state": "wounded",
                    "suggested_outcome": "npc_support_event",
                    "message": "폭풍 상태: NPC 지원 이벤트 분기",
                },
                "trust_score": 0.73,
                "timestamp": "2026-03-08T00:03:00Z",
            },
            {
                "source": "game.ai_director",
                "payload": {
                    "category": "game",
                    "weather": "clear",
                    "resources": "rich",
                    "player_state": "healthy",
                    "suggested_outcome": "rare_loot_branch",
                    "message": "고급 루트 탐사 이벤트",
                },
                "trust_score": 0.69,
                "timestamp": "2026-03-08T00:04:00Z",
            },
        ]

    def context_hint(self) -> Dict:
        return {
            "user_role": "player",
            "environment": "field",
            "scenario_profile": "game",
            "intent": "explore",
        }
