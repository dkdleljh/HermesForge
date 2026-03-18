from app.schemas.evidence import EvidenceCreate
from app.schemas.snapshot import SnapshotGenerateRequest
from app.services.evidence_service import EvidenceService
from app.services.snapshot_service import SnapshotService
from app.plugins.registry import PluginRegistry


class DemoService:
    def __init__(self, evidence_service: EvidenceService, snapshot_service: SnapshotService, plugin_registry: PluginRegistry):
        self.evidence_service = evidence_service
        self.snapshot_service = snapshot_service
        self.plugin_registry = plugin_registry

    def bootstrap(self):
        evidence_count = 0
        for name in self.plugin_registry.list_names():
            plugin = self.plugin_registry.get(name)
            for item in plugin.sample_evidence():
                self.evidence_service.create(EvidenceCreate(**item))
                evidence_count += 1

        snapshot = self.snapshot_service.generate(SnapshotGenerateRequest())
        patch_count = len(snapshot.patches)
        return {
            "message": "demo bootstrap 완료",
            "evidence_count": evidence_count,
            "patch_count": patch_count,
            "snapshot_count": 1,
        }
