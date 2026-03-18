from typing import List, Dict, Any
from uuid import uuid4
import random

from app.domain.entities import SimulationAgent, RenderedEvent

class SentientAgent:
    def __init__(self, base_agent: SimulationAgent):
        self.base_agent = base_agent
        self.sentience_level: float = random.uniform(0.3, 0.9)

    def decide_reaction(self, event: RenderedEvent) -> str:
        category = event.rendered_event.get("category", "")
        action = event.rendered_event.get("action", "")
        if category == "disaster" and self.sentience_level > 0.7:
            return random.choice(["riot", "hack_system", "organize_resistance"])
        if action == "priority_evacuation" and self.sentience_level < 0.5:
            return "obey_and_evacuate"
        if action == "priority_evacuation" and self.sentience_level >= 0.5:
            return "ignore_and_loot"
        return "observing"

class EmergentSociety:
    def __init__(self) -> None:
        self.citizens: Dict[str, SentientAgent] = {}

    def add_citizen(self, agent: SentientAgent) -> None:
        self.citizens[agent.base_agent.id] = agent

    def generate_society_intent(self) -> str:
        if not self.citizens:
            return "neutral"
        state_counts: Dict[str, int] = {}
        for citizen in self.citizens.values():
            st = citizen.base_agent.state
            state_counts[st] = state_counts.get(st, 0) + 1
        
        dominant_state = max(state_counts.keys(), key=lambda k: state_counts[k])
        
        if dominant_state in ["riot", "hack_system"]:
            return "rebellion"
        elif dominant_state == "obey_and_evacuate":
            return "compliance"
        return "survival"
