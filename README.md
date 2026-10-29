# 경기 중등 청간전보 지도

경기도교육청 중등교사 정기인사(교육지원청 간 전보)의 교육지원청별·교과별 배치/희망 인원과 커트라인 전보년수(2020~2025)를 지도, 그래프, 표로 조회하는 페이지입니다.

- 페이지: https://2023swhs3rd-a11y.github.io/ggtransfer/
- 셀 표기 `18/18(2.0)` = 배치 18명 / 희망 18명 (커트라인 전보년수 2년 0개월). 괄호 값은 `년.개월`입니다.

## 새 연도 추가
1. `src/raw/<연도>.json`에 시트 탭 값(1행 = 교과 + 25개 교육지원청)을 넣습니다.
2. `src/template.html`의 `UPCOMING` 배열에서 해당 연도를 지웁니다.
3. `cd src && python3 build.py` (fonttools, brotli 필요) → `index.html` 갱신. 사용 글자만 남긴 Pretendard 부분 글꼴이 자동으로 들어갑니다.

글꼴: Pretendard 1.3.9 (SIL OFL 1.1). 지도 경계는 통계청 2013 시군구 경계(southkorea-maps)를 교육지원청 관할로 묶었습니다(`src/geo.py`).
