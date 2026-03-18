# HermesForge

HermesForge는 **사건 사실 저장소가 아니라 가능역(Possibility Field) 엔진**을 목표로 하는 확장형 MVP입니다.

## 프로젝트 소개
- 추천 프로그램명 후보
1. HermesForge (기본 프로젝트명)
2. PossibilityOS
3. GhostLight Engine
4. ScenarioFabric
5. Counterfactual Studio
- 핵심 목표: Evidence, LambdaPatch, Snapshot, Context를 통해 `가능한 결과`를 안전하게 렌더

## 왜 필요한가
- 교육/게임/훈련/정책 실험은 “정답”보다 “가능성 탐색”이 중요합니다.
- 사실과 시뮬레이션을 분리하지 않으면 오해/오용 위험이 커집니다.
- HermesForge는 `NOT_FACT` 워터마크와 Safety Kernel로 오해를 줄입니다.

## 핵심 개념
- Evidence: 입력 단서
- LambdaPatch(Λ-patch): 조건-결과 가능역 규칙
- Snapshot: 특정 시점의 patch 집합
- Context: 사용자/환경/의도 조건
- RenderedEvent: 가능역 렌더 결과(항상 POSSIBILITY_RENDER)

## 주요 기능
- Evidence 수집/조회
- LambdaPatch 생성/조회
- Snapshot 생성/조회/병합
- Context 기반 Materialize(deterministic, weighted)
- Safety Policy 검사 및 NOT_FACT 워터마크 강제
- 교육/게임/훈련 샘플 플러그인
- REST API + OpenAPI
- React 대시보드

## 설치 방법
```bash
cd HermesForge
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cd frontend && npm install
```

## 실행 방법
```bash
# 백엔드
./scripts/run_backend.sh

# 프론트엔드(다른 터미널)
./scripts/run_frontend.sh
```
- API 문서: `http://localhost:8000/docs`
- UI: `http://localhost:5173`

## 빠른 시작
```bash
# 데모 데이터 주입
./scripts/bootstrap_demo.sh

# snapshot 생성
curl -X POST http://localhost:8000/api/snapshots/generate -H 'Content-Type: application/json' -d '{}'
```

## 기본 사용 흐름
1. `/api/demo/bootstrap` 또는 Evidence/Patch 수동 입력
2. `/api/snapshots/generate`로 Snapshot 생성
3. `/api/materialize`로 Context 기반 결과 렌더
4. 결과 카드에서 `POSSIBILITY_RENDER` / `NOT_FACT` 확인

## 샘플 API 호출
```bash
curl -X POST http://localhost:8000/api/materialize \
  -H 'Content-Type: application/json' \
  -d '{
    "snapshot_id": "ss-xxxx",
    "mode": "weighted",
    "context": {
      "user_role": "teacher",
      "environment": "classroom",
      "permissions": ["render"],
      "state_flags": {"focus": "low"},
      "scenario_profile": "education",
      "intent": "review"
    }
  }'
```

## 폴더 구조
- `backend/`: 코어 엔진, API, 정책, 저장소
- `frontend/`: 대시보드 및 관리 UI
- `docs/`: 설계/운영/패치/테스트 문서
- `data/`: 샘플/시드/스냅샷/evidence 보관
- `scripts/`: 원클릭 실행 스크립트

## 확장 방법
- `backend/app/plugins`에 새 도메인 플러그인 구현
- `PluginRegistry`에 등록
- 필요 시 도메인 정책을 `policies/`에 추가
- 저장소 인터페이스를 구현해 PostgreSQL 전환

## 문제 해결
- CORS 오류: `.env`의 `HERMES_ALLOWED_ORIGINS` 확인
- DB 초기화: `backend/hermesforge.db` 삭제 후 재실행
- 프론트 API 연결 실패: 백엔드 `:8000` 실행 상태 확인

## 주의사항
- 본 시스템 출력은 **사실 기록이 아닌 가능역 렌더**입니다.
- 운영 환경에서는 정책 룰셋/감사 로그/권한 통제를 강화해야 합니다.
