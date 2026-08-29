# JUNGOL Profile Card

GitHub README용 JUNGOL 프로필 카드입니다.  
계정 [`Lir09`](https://jungol.co.kr/account/143157)의 티어, RV, 푼 문제 수, 랭킹을 자동으로 읽어 카드에 반영합니다.

## Designs

### v2 · Animated (default)

`mazassumnida` v2의 레이아웃과 애니메이션 감성을 참고해 JUNGOL용으로 재구성한 기본 디자인입니다.

- 티어별 전용 3색 그라데이션
- Noto Sans KR 기반 폰트 / 자간 / 굵기 조정
- 왼쪽 티어 실드 드로잉 애니메이션
- 핸들 / 스탯 순차 페이드인
- 다음 티어까지 진행률 애니메이션

[![JUNGOL v2](./designs/v2.svg)](https://jungol.co.kr/account/143157)

```md
[![JUNGOL Profile](https://raw.githubusercontent.com/LKA09/Jungol-card/main/jungol-card.svg)](https://jungol.co.kr/account/143157)
```

또는 v2 파일을 직접 지정할 수 있습니다.

```md
[![JUNGOL v2](https://raw.githubusercontent.com/LKA09/Jungol-card/main/designs/v2.svg)](https://jungol.co.kr/account/143157)
```

### v1 · Classic

애니메이션 없이 정보가 바로 보이는 심플한 카드입니다.

[![JUNGOL v1](./designs/v1.svg)](https://jungol.co.kr/account/143157)

```md
[![JUNGOL v1](https://raw.githubusercontent.com/LKA09/Jungol-card/main/designs/v1.svg)](https://jungol.co.kr/account/143157)
```

### Compact

README나 프로젝트 목록에 작게 넣기 위한 한 줄 버전입니다.

[![JUNGOL compact](./designs/compact.svg)](https://jungol.co.kr/account/143157)

```md
[![JUNGOL compact](https://raw.githubusercontent.com/LKA09/Jungol-card/main/designs/compact.svg)](https://jungol.co.kr/account/143157)
```

## Tier themes

카드의 배경은 현재 티어에 맞춰 자동으로 변경됩니다.

| Tier | Theme |
| --- | --- |
| Bronze | Orange / Brown |
| Silver | Gray / Navy |
| Gold | Gold / Orange |
| Platinum | Mint / Teal |
| Diamond | Sky / Blue |
| Ruby | Pink / Crimson |

## Auto update

GitHub Actions가 JUNGOL 공개 프로필을 읽어서 다음 파일들을 함께 갱신합니다.

- `jungol-card.svg` — 기본 v2
- `designs/v1.svg`
- `designs/v2.svg`
- `designs/compact.svg`

현재는 6시간마다 자동 실행되며, Actions 탭에서 수동 실행도 가능합니다. 값이 바뀌지 않았다면 불필요한 커밋을 만들지 않습니다.

## Design reference

v2는 [`mazassumnida/mazassumnida`](https://github.com/mazassumnida/mazassumnida)의 v2 badge에서 레이아웃과 애니메이션 방향을 참고해 JUNGOL 데이터 구조에 맞게 다시 구현했습니다.
