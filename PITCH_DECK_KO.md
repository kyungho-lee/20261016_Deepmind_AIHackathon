# GeoRescue 3D — 한글 발표 & 설명 마스터 덱 (`PITCH_DECK_KO.md`)

> 💡 **용도**: 발표자 참고용 한글 슬라이드 설명서 및 3분 데모 시연 가이드입니다.  
> *(공식 영문 제출 파일인 [`PROJECT_DESCRIPTION.md`](PROJECT_DESCRIPTION.md), [`README.md`](README.md), [`AGENTS.md`](AGENTS.md), [`DEMO_VIDEO_SCRIPT.md`](DEMO_VIDEO_SCRIPT.md), [`slides.html`](slides.html)과 슬라이드 번호가 1:1로 완벽히 일치합니다.)*

- **라이브 Cloud Run 주소**: [https://georescue3d-464836279033.asia-northeast3.run.app/](https://georescue3d-464836279033.asia-northeast3.run.app/)
- **GitHub 저장소 주소**: [https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon](https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon)
- **한글 슬라이드 웹 뷰어**: `http://localhost:8080/static/slides_ko.html` (또는 [`slides_ko.html`](slides_ko.html) 더블클릭)

---

## 슬라이드 1: 프로젝트 소개 & 비전 (Title & Vision)
### **GeoRescue 3D — 실시간 3D 공간 재난 대피 시뮬레이터 & AI 자율 검증 엔진**
- **출품 트랙**:
  - **Track 2 (Gemini 4 Argon in Hard Tech)**: 3D 지형 디지털 트윈 물리 모델링 + 격리 샌드박스 알고리즘 검증
  - **Track 3 (Google AI for Social Good)**: 도심 극한호우 인명 구조 대피 경로 설계 + 관제사 승인(HITL) 거버넌스
- **핵심 한 줄 요약**:
  - *"단순 텍스트로 답하는 AI를 넘어, **Gemini 4 Argon(1M 컨텍스트)**과 **Antigravity Python A\* 자율 검증 루프**로 강남역 침수 지형을 계산하고 **Three.js 3D WebGL 디지털 트윈**에 매핑하는 생명 구조 시스템"*

---

## 슬라이드 2: 문제 정의 — 왜 기존 2D 지도와 일반 LLM은 폭우 때 위험한가?
1. **서울 강남역의 '항아리형(오목) 분지 지형'**:
   - 강남역 사거리 중앙 저지대(`GN_02`)는 해발 **`13.5m`**인 반면, 주변 국기원 언덕(`GN_05: 38.5m`)과 역삼중학교 대피소(`GN_08: 41.2m`)는 높은 구릉지로 둘러싸여 있어 폭우 시 빗물이 중앙으로 급격히 고입니다.
2. **기존 2D 평면 내비게이션의 치명적 한계**:
   - 고도(`z_elevation`)를 무시하고 수평 최단 거리(`850m`: `GN_01 → GN_02 → GN_06 → GN_08`)만 안내하여, 시민을 **수심 `0.45m`로 침수된 강남역 지하차도/저지대(`GN_02`, `13.5m`)** 한가운데로 유도합니다.
3. **검증 없는 일반 LLM 챗봇의 한계**:
   - 물리적 지형 고도(`z > 18.5m`)나 보행자 한계 수심(`<= 0.15m`)을 수학적으로 검증하지 못해 환각(Hallucination) 경로를 제시할 위험이 있습니다.

---

## 슬라이드 3: 멀티 에이전트 시스템 아키텍처 (`AGENTS.md`)
| 에이전트 역할 | 할당 모델 / ID | 핵심 수행 역할 |
| :--- | :--- | :--- |
| **1. 총괄 지휘 및 심사위원장 (Chief Jury)** | `gemini-4-argon` (`thinking_level="high"`, 1M) | • 100만 토큰 컨텍스트로 3D 지형·그래프·후보 코드 동시 분석<br>• 3개 팀(Alpha/Beta/Gamma) 경쟁 토너먼트 지휘 및 100점 만점 루브릭 채택 |
| **2. 백엔드 & GIS 데이터 파이프라인** | `gemini-4-argon` (`medium`) + `gemini-3.8-flash` | • `make_data.py`로 3D DEM 격자(`gangnam_3d_grid.csv`) 및 도로망(`gangnam_graphify.json`) 생성<br>• FastAPI 실시간 서버(`app.py`) 구축 |
| **3. 자율 샌드박스 검증 에이전트** | `antigravity-preview-09-2026` (`remote`) | • 격리된 리눅스 Python 샌드박스에서 `NetworkX` A\* 알고리즘 실행<br>• 침수 불변조건(`z > 18.5m`, `water <= 0.15m`) 위반 시 자율 자기교정(Self-Correction) 수행 |
| **4. 고속 스키마 검증 & 법률 가드레일** | `gemini-3.8-flash` + `gemini-3.5-flash-lite` | • `1.04ms` 초고속 그래프 직렬화, V-World/OSM 오픈 라이선스 및 관제사 승인(HITL) 의무화 |

---

## 슬라이드 4: 핵심 작동 원리 — Antigravity 자율 검증 & 자기교정 루프 (Self-Correction Loop)
- **시나리오**: 극한호우 발생 (`water_level = 2.0m`, 강남 분지 침수 기준면 `z = 18.5m`)
- ❌ **[Iteration #1 — 샌드박스 검증 기각 (FAIL)]**:
  - **탐색 경로**: `GN_01 (19.2m) → GN_02 (13.5m) → GN_06 (34.0m) → GN_08 (41.2m)` (수평 최단 850m)
  - **기각 사유 (4건 위반)**: `antigravity-preview-09-2026`이 `GN_02` 노드의 고도(`13.5m <= 18.5m`)와 노면 수심(`0.45m > 0.15m`) 위반을 즉시 적발!
- ✅ **[Iteration #2 — 자율 자기교정 통과 (`[SUCCESS] Verified by Python A* Algorithm`)]**:
  - **자기교정 조치**: `gemini-4-argon`이 침수 노드 `GN_02`를 블랙리스트 차단하고 고지대 가중치(`elevation_bonus=2.0`)를 부여해 재탐색 지시.
  - **최종 안전 경로**: `GN_01 (19.2m) → GN_04 신논현 능선 (22.8m) → GN_05 국기원 언덕 (38.5m) → GN_06 역삼 고지대 (34.0m) → GN_08 역삼중 대피소 (41.2m)`
  - **검증 지표**: 최소 고도 **`19.20m (> 18.5m)`**, 최대 노면 수심 **`0.12m (<= 0.15m)`**, 골든타임 **`1,524.6초 (25.4분 <= 30분)`** 완벽 충족!

---

## 슬라이드 5: 주요 기술 혁신 — 고저차 밀착형 3D WebGL 디지털 트윈 & 관제 콘솔
1. **고도 오차 `0.00m`의 3D 지형·경로 일체화 (`64x64 IDW DEM`)**:
   - 백엔드(`make_data.py`)와 프론트엔드(`static/index.html`)가 동일한 12개 제어점 역거리 가중 보간(IDW) 지형 함수를 공유하여, `2.5m` 간격 **등고선**과 **3D 녹색 대피 튜브**가 산비탈 경사면을 오차 없이 그대로 타고 올라갑니다.
2. **실시간 침수 수위 슬라이더 (`1.04ms` API 연동) & 종단 고도 단면도**:
   - 좌측 슬라이더로 침수 수위(`14.0m ~ 22.0m`)를 조절하면 3D 수면이 즉각 상승하고, 우측 **종단 고도 단면도(Elevation Profile)**에서 경로 전체가 빨간 침수선(`18.5m`) 위에 있음을 시각적으로 증명합니다.
3. **Google Maps 실좌표(WGS84) 연동 & 관제사 승인(HITL) 버튼**:
   - 클릭 한 번으로 실제 **Google Maps 도보 내비게이션**으로 연결되며, 재난 문자 발송 전 **관제사 최종 승인(HITL)** 버튼을 통해 AI 안전 가드레일을 완성했습니다.

---

## 슬라이드 6: 3개 팀 경쟁 토너먼트 및 정량 평가 결과 (Argon Chief Jury)
| 평가 항목 (배점) | 안전 기준 (Invariant) | Team Alpha (알고리즘팀) | Team Beta (3D 시각화팀) | 🏆 Team Gamma (최종 채택) |
| :--- | :--- | :---: | :---: | :---: |
| **최소 경로 고도 (`min_z`)** | `> 18.50 m` | `13.50 m` (실격) | `17.20 m` (실격) | **`19.20 m → 41.20 m` (통과)** |
| **최대 노면 수심 (`max_water`)** | `<= 0.15 m` | `0.45 m` (실격) | `0.28 m` (실격) | **`0.12 m` (통과)** |
| **골든타임 대피 시간 (ETA)** | `<= 1,800초 (30분)` | `1,598.4초` | `1,412.0초` | **`1,524.6초 (25.4분 — 통과)`** |
| **Argon 심사위원장 총점** | **100점 만점 루브릭** | `47.0 / 100` | `44.0 / 100` | **`97.6 / 100 (최종 채택)`** |

---

## 슬라이드 7: 라이브 Cloud Run 배포 및 결론
- **Google Cloud Run 프로덕션 배포 완료 (`asia-northeast3` 서울 리전)**:
  - 라이브 URL: [https://georescue3d-464836279033.asia-northeast3.run.app/](https://georescue3d-464836279033.asia-northeast3.run.app/)
- **향후 확장 계획**:
  - 기상청(KMA) 실시간 강우 레이더 API 연동 및 전국 상습 침수 구역(도림천, 사당역, 광화문 등) 3D 디지털 트윈 확장.
