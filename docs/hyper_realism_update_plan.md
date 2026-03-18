# 🚀 HermesForge: 초현실주의(Hyper-Realism) 진화 로드맵

현재 HermesForge의 MVP 버전은 단순 규칙 기반(Rule-based) 확률 계산기와 정적인 단서(Evidence)에 의존하고 있습니다. 이 시스템을 **현실과 99.9% 일치하는 초정밀 '가능역 시뮬레이터(Possibility Field Engine)'**로 탈바꿈하기 위한 단계별 마스터 플랜을 제안합니다.

---

## 🔍 현재 시스템의 한계점 (AS-IS)

1. **정적인 데이터 (Static Data)**: 현재 Evidence는 사용자가 수동으로 입력한 고정된 값입니다. 현실의 시간, 날씨, 경제 상황 등 실시간으로 변하는 요소를 반영하지 못합니다.
2. **단순 선형 확률 (Linear Probability)**: `Materializer` 엔진이 `score = confidence * probability_mass * anchor_weight`라는 매우 단순한 수식에 의존하고 있습니다. 현실의 복잡한 '나비 효과'나 다중 변수 간의 상관관계를 계산하지 못합니다.
3. **단발성 렌더링 (Discrete Event)**: 한 번의 Snapshot에 대해 단 한 번의 결과를 도출하고 끝납니다. 현실처럼 시간이 흐르며 사건이 연쇄적으로 작용하는 '연속적 시간축(Time-series)' 모델이 부재합니다.

---

## 🗺️ 단계별 초현실주의 업데이트 마스터 플랜 (TO-BE)

### 🟢 1단계: 실시간 동적 데이터 파이프라인 구축 (Live Data Injection)
**목표:** 세상의 실제 데이터를 시뮬레이터의 핏줄(Evidence)로 연결합니다.

*   **1.1. Live Evidence 플러그인 도입**
    *   **날씨/환경 API 연동:** OpenWeatherMap API 등을 연결해 시뮬레이션 지역의 실시간 날씨, 풍향, 기온을 Evidence로 자동 주입.
    *   **금융/소셜 데이터 연동:** 주식 시장 API, 트위터 트렌드 등 실시간 사회/경제 지표를 Context로 주입하는 데몬(Daemon) 구축.
*   **1.2. Time-aware Snapshot 구조화**
    *   현재 정적인 Snapshot에 `timestamp`와 `duration` 개념을 추가. 특정 시나리오가 "언제, 얼마나 지속되는가"를 정의합니다.

### 🟡 2단계: 복잡계 다차원 렌더링 엔진 (Multi-variable Materializer)
**목표:** 단순 곱셈 공식을 폐기하고, 현실의 복잡한 변수 상호작용을 계산하는 엔진으로 업그레이드합니다.

*   **2.1. 퍼지 로직(Fuzzy Logic) 및 베이지안 네트워크(Bayesian Network) 도입**
    *   현재의 `ContextAwareMaterializer`를 베이지안 확률 추론 모델로 교체. A사건이 일어났을 때 B사건이 일어날 조건부 확률을 동적으로 계산합니다.
*   **2.2. 외부 ML 모델(AI) 연동 (ML-Driven LambdaPatch)**
    *   단순한 하드코딩 `LambdaPatch` 대신, TensorFlow나 PyTorch 서빙 컨테이너와 통신하는 `MLPatchGenerator`를 신설합니다.
    *   수만 건의 과거 현실 데이터를 학습한 AI가 "가장 현실적인 결과(Outcome)"를 실시간 추론하여 Patch로 생성합니다.

### 🟠 3단계: 연속 시간 시뮬레이션 및 다중 에이전트 (Continuous & Multi-Agent)
**목표:** 한 번 계산하고 끝나는 것이 아니라, 시나리오가 톱니바퀴처럼 스스로 돌아가게 만듭니다.

*   **3.1. 시계열(Time-series) 루프 엔진 설계**
    *   결과(RenderedEvent)가 생성되면 시스템이 멈추지 않고, 그 결과를 **다시 새로운 Evidence로 재주입**하여 1초 뒤, 1분 뒤, 1시간 뒤의 결과를 연속으로 렌더링하는 `Timeline Engine`을 구축합니다.
*   **3.2. NPC/다중 주체(Multi-Agent) 도입**
    *   시나리오 내부의 사람, 기계, 자연환경을 각각의 독립된 상태 머신(State Machine)으로 분리. 각각의 Agent가 시뮬레이션 안에서 서로 상호작용(Collision)하도록 만듭니다.

### 🔴 4단계: 혼돈 이론 및 나비효과 시스템 (Chaos Theory & Butterfly Effect)
**목표:** 99.9% 현실 모사를 위한 궁극의 불확실성 시뮬레이션.

*   **4.1. 미세 변수 노이즈(Noise) 삽입**
    *   모든 계산에 현실의 예측 불가능성(양자 요동, 인간의 변덕 등)을 모사하는 미세한 난수(Gaussian Noise)를 정밀하게 주입합니다.
    *   아주 작은 단서의 변화가 시뮬레이션 100턴 이후에 완전히 다른 결과를 가져오도록 `ChaosEngine` 모듈을 추가합니다.
*   **4.2. 대규모 분산 렌더링 아키텍처 (Scale-out)**
    *   수백만 개의 변수와 에이전트가 상호작용하는 거대 도시 시뮬레이션을 위해, `Engine`을 Kubernetes 기반의 분산 처리(Worker Node) 시스템으로 전환합니다.

---

## 🛠️ 개발 시작을 위한 첫 걸음 (Action Items)
이 거대한 업데이트를 위해 당장 내일부터 시작해야 할 코딩 작업은 다음과 같습니다.

1. `backend/app/domain/entities.py`의 `Evidence` 모델에 `source_api` 및 `ttl`(유효시간) 필드 추가.
2. `backend/app/plugins/` 폴더에 `LiveWeatherPlugin` 생성 및 외부 API 주기적 페치 스크립트 작성.
3. `Materializer` 인터페이스를 추상화하여, 기존 `RuleBased` 모델 옆에 `BayesianNetworkMaterializer` 초안 작성.

> **💡 핵심 철학 유지:** 현실성을 99.9%까지 끌어올리더라도, 이 시스템이 내뱉는 출력물에는 반드시 `NOT_FACT` 워터마크가 찍혀야 합니다. 현실과 구분이 안 될수록 Safety Policy 커널의 보안 등급도 함께 올라가야 합니다.