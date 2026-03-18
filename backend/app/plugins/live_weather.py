from typing import Dict, List

from app.plugins.base import DomainPlugin

class LiveWeatherPlugin(DomainPlugin):
    name: str = "live_weather"

    def sample_evidence(self) -> List[Dict]:
        return [
            {
                "id": "ev-weather-storm-01",
                "source": "openweathermap_live",
                "payload": {"category": "environment", "condition": "storm", "wind_speed": 120, "message": "강력한 폭풍우 발생 중"},
                "trust_score": 0.98,
                "timestamp": "2026-03-08T15:00:00Z",
                "hash": "mock_live_hash",
                "source_api": "openweathermap_api",
                "ttl": 3600
            }
        ]

    def context_hint(self) -> Dict:
        return {
            "environment": "high_risk",
            "scenario_profile": "weather",
            "intent": "analyze_disaster_impact"
        }
