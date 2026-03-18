from typing import List, Tuple, Optional
from app.domain.entities import RenderedEvent

class QuantumMerger:
    def _evaluate_timeline_score(self, timeline_history: List[RenderedEvent]) -> float:
        score = 100.0
        for event in timeline_history:
            category = event.rendered_event.get("category", "")
            action = event.rendered_event.get("action", "")
            if category == "disaster":
                score -= 30.0
            if category == "risk":
                score -= 10.0
            if action in ["priority_evacuation", "secure_area", "resolve"]:
                score += 20.0
            score += event.confidence * 5.0
        return score

    def find_golden_path(self, multiverses: List[List[RenderedEvent]]) -> Tuple[List[RenderedEvent], float]:
        if not multiverses:
            raise ValueError("병합할 타임라인 결과가 없습니다.")
        best_timeline: Optional[List[RenderedEvent]] = None
        best_score = float('-inf')
        for timeline in multiverses:
            current_score = self._evaluate_timeline_score(timeline)
            if current_score > best_score:
                best_score = current_score
                best_timeline = timeline
        return best_timeline or [], best_score
