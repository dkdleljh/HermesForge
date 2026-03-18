from typing import Dict, List

from app.plugins.base import DomainPlugin
from app.plugins.education import EducationPlugin
from app.plugins.game import GamePlugin
from app.plugins.training import TrainingPlugin
from app.plugins.live_weather import LiveWeatherPlugin


class PluginRegistry:
    """도메인 플러그인을 동적으로 등록/조회한다."""

    def __init__(self) -> None:
        self._plugins: Dict[str, DomainPlugin] = {}

    def register(self, plugin: DomainPlugin) -> None:
        self._plugins[plugin.name] = plugin

    def get(self, name: str) -> DomainPlugin:
        return self._plugins[name]

    def list_names(self) -> List[str]:
        return list(self._plugins.keys())


def build_default_registry() -> PluginRegistry:
    registry = PluginRegistry()
    registry.register(EducationPlugin())
    registry.register(GamePlugin())
    registry.register(TrainingPlugin())
    registry.register(LiveWeatherPlugin())
    return registry
