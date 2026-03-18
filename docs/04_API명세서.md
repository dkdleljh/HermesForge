# API 명세서

## 공통
- Base URL: `http://localhost:8000/api`
- 문서: `/docs` (OpenAPI)

## 엔드포인트
- `POST /api/evidence`
- `GET /api/evidence`
- `POST /api/patches`
- `GET /api/patches`
- `POST /api/snapshots/generate`
- `GET /api/snapshots`
- `GET /api/snapshots/{snapshot_id}`
- `POST /api/snapshots/merge`
- `POST /api/materialize`
- `GET /api/policies`
- `POST /api/demo/bootstrap`
- `GET /api/health`

## 응답 규칙
- materialize 결과는 항상 `label=POSSIBILITY_RENDER`
- provenance에 `source_type=non_factual_projection`, `watermark=NOT_FACT`
