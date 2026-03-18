# 🚀 Hyper-Realism Phase 1: Live Data Injection 진행 내역

본 문서는 HermesForge의 초현실주의(Hyper-Realism) 진화를 위한 1단계 업데이트 작업의 진행 및 구현 내역을 기록합니다.

## 📅 작업 개요
* **목표**: 고정된 단서(Evidence) 및 정적 계산 구조를 넘어, 외부 API의 실시간 데이터와 시계열 개념을 엔진에 주입.
* **주요 과제**: 
  1. `Evidence` 모델 확장 (`source_api`, `ttl` 추가)
  2. `Snapshot` 모델 확장 (`duration` 추가)
  3. `LiveWeatherPlugin` 신규 구현 (외부 환경 변수 모사)
  4. 데이터베이스 스키마(SQLite) 마이그레이션

## ✅ 진행 상태

### 1. 도메인 모델(Entity) 업데이트 
- `backend/app/domain/entities.py`
  - `Evidence` 데이터 클래스에 외부 소스를 명시하는 `source_api` 및 데이터 유효시간 `ttl`(초) 필드 추가.
  - `Snapshot` 데이터 클래스에 해당 시나리오 스냅샷이 유지되는 기간을 나타내는 `duration` 필드 추가.
- `backend/app/schemas/` 
  - FastAPI 및 Pydantic의 데이터 송수신을 위한 Request/Response 스키마에 동일한 필드 지원 추가.

### 2. 저장소(Repository) 스키마 마이그레이션
- `backend/app/repositories/sqlite.py`
  - `evidences` 테이블: `source_api` (TEXT), `ttl` (INTEGER) 컬럼 추가.
  - `snapshots` 테이블: `duration` (INTEGER) 컬럼 추가.
  - CRUD (`save`, `get`) 쿼리문 업데이트를 통해 신규 필드 영속화 확보.

### 3. LiveWeatherPlugin 도입
- `backend/app/plugins/live_weather.py`
  - 엔진이 실시간 외부 데이터를 어떻게 다룰지 테스트하기 위한 모의(mock) 플러그인 작성.
  - `BasePlugin` 인터페이스 상속 및 `registry.py`를 통한 시스템 자동 로딩 구현.
  - 폭풍우(Storm) 등 날씨 상황에 따른 확률 변동을 모사하는 `LambdaPatch` 발급 로직 구축.

### 4. 무결성 검증 (Tests & LSP)
- 기존 pytest 테스트 케이스 수정 (`backend/app/tests/`).
- 전체 시스템 빌드 및 검증 통과 여부 확인.

---
> 💡 *현재 1단계(Live Data Injection) 구현 및 테스트가 모두 **완료(Completed)**되었습니다.*