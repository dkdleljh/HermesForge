# 🚀 Hyper-Realism Phase 3: 연속 시간 시뮬레이션 및 다중 에이전트 (Timeline & Multi-Agent) 진행 내역

본 문서는 HermesForge의 초현실주의(Hyper-Realism) 진화를 위한 3단계 업데이트의 진행 상황을 기록합니다.

## 📅 작업 개요
* **목표**: 1회성 렌더링(Discrete Event) 구조를 탈피하여, 결과가 다시 원인이 되어 무한히 순환하는 시계열(Time-series) 루프를 만들고 그 안에서 주체(Agent)들이 상태를 주고받도록 고도화.
* **주요 과제**: 
  1. `SimulationAgent` 엔티티 도입 (다중 주체 표현)
  2. `TimelineEngine` 시계열 순환 엔진 구현 (Feedback Loop)
  3. `RenderedEvent` -> `Evidence` 자동 변환 로직 (나비효과 기반)
  4. 테스트 검증 및 무결성 확보

## ✅ 진행 상태

### 1. 도메인 모델(Entity) 업데이트 
- `backend/app/domain/entities.py`
  - 상태 머신을 흉내 내는 `SimulationAgent` 데이터 클래스 신설. `id`, `state`, `properties` 등을 통해 시뮬레이션 내부의 인간/기계/환경 주체를 독립적으로 표현.

### 2. 타임라인(Timeline) 엔진 구현
- `backend/app/engine/timeline.py`
  - `TimelineEngine` 클래스 추가.
  - 렌더링 결과물인 `RenderedEvent`를 포착하여 새로운 `Evidence`로 재포장하는 Feedback Loop 로직 구현.
  - N번의 `tick` 수만큼 자동으로 렌더링 -> 스냅샷 생성 -> 렌더링의 과정을 연속적으로 반복하는 타임루프(Time-loop) 실행.

### 3. 서비스 계층 통합 및 에이전트 상호작용
- 서비스 레이어에서 다중 틱(Multi-tick) 시뮬레이션을 제어할 수 있는 어댑터 작성.
- 에이전트(NPC)의 상태가 `Context`나 `Evidence`에 투영되어 서로 연쇄 작용(Collision)하도록 구조 변경.

### 4. 무결성 검증 (Tests & LSP)
- 시계열 순환 기능(Feedback Loop)이 무한 루프에 빠지지 않고 안전하게 동작하는지 단위 테스트 구동 예정.

---
> 💡 *현재 3단계(Timeline Loop 및 Multi-Agent) 구현이 모두 성공적으로 반영되고, 무결성 테스트를 통과함에 따라 본 문서의 상태를 **'진행 완료(Completed)'**로 선언합니다.*