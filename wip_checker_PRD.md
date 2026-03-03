# WIP Deadline Checker — PRD

## 개요

패션 생산 WIP(Work In Progress) 마감 추적 도구.  
엑셀 파일(.xlsx)을 업로드하면 Cut Date, FAD, PPAD, Trim Due 기준으로 D-day를 계산하고 경보를 표시하는 **단일 HTML 파일** 앱.

**타겟:** FL'26 Outlet · Hansoll · 5명 비개발자 팀  
**형태:** 단일 `.html` 파일 (서버 없음, 브라우저에서 바로 실행)

---

## 엑셀 파일 구조

### 시트 목록 (모두 파싱)
- `Q3 1X1 RIB`
- `Q3 KNIT TOP`
- `Q3 TxT`
- `Q3 LOUNGE`

### 헤더 위치
- 행 2 (index 1) 에 `Brand Moment` 가 첫 번째 셀에 있으면 헤더 행으로 인식
- 최대 10행까지 탐색

### 주요 컬럼 (헤더 텍스트로 매칭, 대소문자 무시)

| 컬럼명 | 매칭 키워드 |
|--------|------------|
| Style Number | 인덱스 1 고정 |
| Description | 인덱스 2 고정 |
| Entity | 인덱스 7 고정 |
| IH DATE | `ih date` |
| Fit Approval Date (FAD) | `fit approval` |
| FAD Status | `status` (정확 일치) |
| PP Approval Date (PPAD) | `pps approval` |
| Trim Due | `trim app` |
| Planned Cut Date | `planned cut` |

---

## TNA (Time & Action) 계산 로직

**기준: IH DATE (In-House Date)**

```
Cut Date  = IH DATE - 31일
PPAD      = Cut Date - 14일
FAD       = PPAD - 31일
```

> Cut = IH - 31, PPAD = Cut - 14, FAD = PPAD - 31  
> 연도는 원본 그대로 유지 (연도 교체 로직 없음)

### D-day 계산
- **연도 무시** 방식: 월/일 기준, 올해 연도로 계산
- `ddMD(d) = ceil((thisYear/month/day - TODAY) / 86400000)`

### TNA 대비 (tnaDiff)
- 실제날짜와 TNA기준날짜의 차이 (연도 원본 그대로 비교)
- `tnaDiff = actual - tna` (일수, 양수=지연, 음수=여유)

---

## Fit 승인 판단

| 표시 | 조건 |
|------|------|
| ✓ **완료** | xlsx gray shade 감지 (cell tint < -0.1) |
| ✓ **승인** | Status 셀에 `approved`, `approval`, `c/o`, `fixed`, `complete`, `done` 키워드 포함 (대소문자 무시) |
| ✗ **미승인** | 위 두 조건 모두 해당 없음 (빈칸 포함) |

---

## 경보(Alert) 판단

| 경보 | 조건 |
|------|------|
| 🚫 **PP 진행 불가** (`block`) | Fit 미승인 AND FAD D-day < 0 (초과) |
| ⚠️ **Trim 경보** (`trimwarn`) | Trim 미완료 AND PPAD D-day ≤ 30일 |
| ❌ **Fit 미승인** (`fitno`) | Fit 미승인 AND FAD D-day 0~14일 이내 |

우선순위: block > trimwarn > fitno

---

## Stats 카드 (6개)

| 카드 | 조건 | 색상 |
|------|------|------|
| 전체 | 모든 행 | 흰색 |
| 🚨 Cut 초과 | cutDiff < 0 | 빨강 |
| 🟠 30일 이내 | cutDiff 0~30 | 주황 |
| 🟡 60일 이내 | cutDiff 31~60 | 노랑 |
| 🟣 PPAD D-14 | PPAD가 Cut 기준 -14일~0일 이내 | 보라 (#d946ef) |
| ✅ 여유있음 | cutDiff > 60 | 파랑 |

### PPAD D-14 계산
```
ppadVsCut = ppad - cut (일수)
isPpad14  = -14 ≤ ppadVsCut ≤ 0
```
= Planned Cut Date 기준으로 PPAD가 14일 이내에 있는 스타일

---

## 테이블 컬럼 구조

```
경보 | Style # | Description | Entity |
✂ CUT DATE: 날짜 / 남은기간 / TNA대비 |
FIT APPROVAL (FAD): 날짜 / 남은기간 / Fit Status |
PP APPROVAL (PPAD): 날짜 / 남은기간 |
TRIM DUE: 날짜 / 남은기간
```

### 남은 기간 표시 (뱃지 하이라이트)
- **초과**: 빨강 배경 뱃지 → `N일 초과`
- **7일 이내**: 주황 배경 뱃지 → `N일 남음`
- **14일 이내**: 노랑 배경 뱃지 → `N일 남음`
- **여유**: 색상 없이 텍스트만 → `N일 남음`

### TNA 대비 표시 (조용하게, 참고용)
- 배경/테두리 없음, 텍스트 색만
- 지연(+): 연한 빨강 텍스트
- 여유(-): 연한 초록 텍스트

### 날짜 표시
- gray shade 여부와 무관하게 날짜 그대로 표시 (취소선 없음)

### 행 정렬 순서
1. block 경보 (가장 위, 깜빡임)
2. fitno 경보
3. trimwarn 경보
4. cutDiff 오름차순 (급한 것부터)

---

## TNA BAR (상단 요약)

- IH DATE가 같은 스타일끼리 납기 그룹으로 묶음
- 그룹마다: IH DATE + 스타일 수 + FAD / PPAD / Trim / Cut 기준일 + 남은 일수
- 여러 그룹은 가로 스크롤로 표시

---

## Alert Chips (클릭 필터)

- 🚫 PP 진행 불가 (block 건수)
- ❌ Fit 미승인 (fitno 건수)
- ⚠️ Trim 경보 (trimwarn 건수)
- 클릭 시 해당 항목만 테이블 필터링

---

## 디자인 시스템

**다크 테마**

```css
--bg: #080808
--surf: #111
--surf2: #181818
--border: #222
--red: #f53d3d
--ora: #ff8c00
--yel: #f5c400
--grn: #00d97e
--blu: #38bdf8
--mag: #d946ef
--t1: #e8e8e8  /* 본문 */
--t2: #888     /* 보조 */
--t3: #444     /* 비활성 */
```

**폰트:** IBM Plex Mono (본문) + Syne (숫자/타이틀)

---

## 기능 요구사항

### 파일 업로드
- 클릭 또는 드래그앤드롭
- `.xlsx`, `.xls` 지원
- SheetJS (xlsx 0.18.5) CDN 사용: `https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js`

### 탭
- 전체 탭 + 시트별 탭
- 탭마다 스타일 건수 뱃지 표시

### 다시 올리기
- 헤더 우측 버튼, 파일 업로드 후 표시
- 클릭 시 초기화

### 에러 처리
- 지원하지 않는 파일 형식
- Brand Moment 헤더 없음
- 파싱 오류
- Toast 형태로 5초 표시

### Power Automate 가이드 (접기/펼치기)
- 하단 섹션
- 4단계: Power Automate 접속 → 예약 흐름 → Excel 연결 → 이메일+Teams 발송

---

## 비기능 요구사항

- 단일 HTML 파일 (외부 파일 없음, CDN만 허용)
- 서버 불필요, 브라우저 직접 실행
- 반응형 (가로 스크롤 지원)
- xlsx.js cellStyles:true 로 gray shade 감지

---

## 버전 히스토리 참고

- v1~v6: 기본 TNA 계산, 경보 시스템 구축
- v7: TNA 납기 그룹화, Cut 글자 크기 통일
- v8 (현재 목표):
  - 남은기간 뱃지 하이라이트 (핵심 지표)
  - TNA 대비 조용하게 (텍스트만)
  - gray 취소선 제거
  - PPAD D-14 stats 카드 추가
