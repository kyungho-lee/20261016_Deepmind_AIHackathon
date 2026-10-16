# 심층 리서치 보고서: GeoRescue 3D (WebGPU/Three.js 기반 AI 재난 시뮬레이터 및 게임)

본 보고서는 **GeoRescue 3D (실시간 3D 재난 시뮬레이션 & 게이미피케이션 생존 트레이닝 엔진)** 프로젝트의 개발을 위한 **기술적 레퍼런스, WebGPU/Three.js 유체/지형 시뮬레이션 구조, AI 연동 절차적 생성 파이프라인 및 학술적 타당성**을 조사한 심층 리서치 결과입니다.

---

## 1. ⚙️ WebGPU & Three.js 기술적 레퍼런스 (Technical Stack)

구글 딥마인드 해커톤의 4시간 제한 타임라인 내에서 라이브 3D 시뮬레이션을 에러 없이 구현하기 위한 최신 웹 3D 및 WebGPU Compute Shader 레퍼런스입니다.

### ① WebGPU Compute Shader & TSL (Three Shading Language)
* **Three.js WebGPU Renderer (`webgpu_tsl_procedural_terrain`):**
  * Three.js의 최신 TSL(Three Shading Language)을 활용하면 노드 기반 셰이더로 수십만 개의 3D 지형 정점(Vertex)을 브라우저 GPU 상에서 실시간으로 변형 가능합니다.
* **MLS-MPM & SPH 유체 시뮬레이션 (WebGPU Fluid Dynamics):**
  * `Splash` (Matsuoka_601) 및 `jeantimex/fluid` 라이브러리와 같이 MLS-MPM(Moving Least Squares Material Point Method)을 적용하면 70,000개 이상의 수면 파티클 및 침수 수위를 60 FPS 이상으로 실시간 연산할 수 있습니다.

### ② GIS 및 지형 수문 시뮬레이션 (Hydro3DJS)
* **Hydro3DJS (Web-Based 3D Hydrological Library):**
  * GeoJSON 및 수문 데이터(강수량, 천변 수위)를 3D 침수 폴리곤으로 변환하는 브라우저 호환 3D 엔진 레퍼런스.
  * Gemini 4 Argon이 입력받은 센서 CSV/지형 데이터를 Hydro3DJS / Three.js 메시 변형 코드로 실시간 주입할 수 있습니다.

---

## 2. 🧠 Gemini 4 Argon & AI-Driven 3D Procedural Code Generation

LLM이 3D 자산을 직접 업로드하는 대신, **Three.js 스크립트 및 3D 파티클 좌표를 절차적으로 코드 통생성(Code Injection)**하는 기술적 타당성입니다.

```
[ 기상/지형 센서 CSV 데이터 ]
             │
             ▼
[ Gemini 4 Argon (thinking_level="high") ]
  • 1M 컨텍스트 기반 침수 고도 및 수면 상승 함수 연산
  • Three.js 파티클/메시 애니메이션 코드 생성 (`background=True`)
             │
             ▼
[ Antigravity Sandbox Verification Loop ]
  • Python A* 경로 알고리즘 (`networkx`) 실행
  • 침수 위험 구역을 완전히 회피하는 대피 경로 좌표 1차 검증
             │
             ▼
[ Three.js WebGPU 캔버스 라이브 렌더링 ]
  • 3D 수면 상승 + 안전 대피로 파티클 라인 실시간 시각화
```

* **`three-llm` 및 LLM-to-Three.js 파이프라인:**
  * LLM이 자연어 프롬프트나 CSV 데이터를 파싱하여 Three.js 코드(카메라, 파티클, 라이팅, 수면 상승 함수)를 단일 Pass로 디코드 생성하는 오픈소스 파이프라인 검증 완료.
* **Antigravity 샌드박스 자율 검증 루프 (Verification Loop):**
  * Argon이 생성한 3D 대피 경로 좌표가 실제 침수 수면과 물리적으로 충돌하는지 Antigravity 호스팅 샌드박스의 Python 스크립트가 **A* (A-Star) 알고리즘**을 돌려 1차 재검증(Self-Correction) 후 프론트엔드로 전달합니다.

---

## 3. 🎮 게이미피케이션 & 시리어스 게임 학술 타당성 (Edutainment)

GeoRescue 3D를 Track 1 (Entertainment) 또는 Track 3 (Social Good)에 게이미피케이션 요소와 함께 출품할 때의 학술적·산업적 타당성입니다.

* **arXiv 논문: *Towards a Serious Games Evacuation Simulator* & *Immersive VR Serious Games for Evacuation Training***
  * **연구 결과:** 단순 비디오/포스터나 전통적 소방 훈련 대비, 3D 게이미피케이션 환경에서 사용자가 직접 재난 상황을 경험할 때 피난 수칙 지식 습득률과 대처 자기 효능감(Self-Efficacy)이 **통계적으로 유의미하게 대폭 상승**함을 증명.
* **Track 1 게이미피케이션 결합 스펙:**
  1. **생존 타이머 (Survival Clock):** 침수/화재까지 남은 시간을 시각적으로 압박.
  2. **동적 퀘스트 생성:** Argon이 어르신/주민 구조, 밸브 차단 등의 인터랙티브 퀘스트를 실시간 부여.
  3. **Generative Media 오케스트레이션:** `Lyria 3.5` 기반 긴박한 3D BGM 및 `Gemini Nano Banana 2.1` 기반 카툰 UI 카드 연동.

---

## 📊 리서치 결과 출처 및 레퍼런스 모음

| 카테고리 | 핵심 프로젝트 / 논문명 | 주요 기술 및 의의 |
| :--- | :--- | :--- |
| **WebGPU 유체/지형** | Three.js `webgpu_tsl_procedural_terrain` | WebGPU Compute Shader 및 TSL 기반 실시간 3D 지형 변형 예제 |
| **유체 파티클** | Splash (MLS-MPM Fluid) / Hydro3DJS | 7만 개 이상 파티클 기반 real-time 수면 연산 및 GIS 3D 수문 시뮬레이션 |
| **LLM ➔ 3D 코드** | `bhouston/three-llm` / `TopologyAI` | 브라우저 내 LLM 3D Scene / Three.js 코드 자동 생성 파이프라인 |
| **학술 연구** | arXiv:1805.09138 & arXiv:1905.11082 | Immersive VR & Serious Games 기반 대피 훈련 유효성 검증 연구 |

---
*Research conducted for GeoRescue 3D Hackathon Pipeline.*
