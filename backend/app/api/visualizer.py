from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from app.schemas.snapshot import SnapshotRead

router = APIRouter()


@router.get("/multiverse-tree", response_model=Dict[str, Any])
async def get_multiverse_tree():
    """
    실무 과제 1 (4D Visualizer):
    Three.js나 WebGL 기반 프론트엔드가 3차원 우주 트리 구조를
    렌더링할 수 있도록 다중 우주 분기(Multiverse Branching) 데이터를 스트리밍함.
    """
    # 더미 4D 그래프 데이터 반환
    return {
        "root_snapshot": "ss-origin",
        "nodes": [
            {
                "id": "ss-branch-1",
                "parent": "ss-origin",
                "intent": "evacuate",
                "score": 90.0,
                "status": "golden_path",
            },
            {
                "id": "ss-branch-2",
                "parent": "ss-origin",
                "intent": "ignore",
                "score": -20.0,
                "status": "collapsed",
            },
            {
                "id": "ss-branch-3",
                "parent": "ss-origin",
                "intent": "wait",
                "score": 40.0,
                "status": "active",
            },
        ],
        "edges": [
            {"source": "ss-origin", "target": "ss-branch-1"},
            {"source": "ss-origin", "target": "ss-branch-2"},
            {"source": "ss-origin", "target": "ss-branch-3"},
        ],
    }
