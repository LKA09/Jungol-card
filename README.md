# JUNGOL Profile Card

GitHub README용 JUNGOL 프로필 카드입니다.  
계정 [`Lir09`](https://jungol.co.kr/account/143157)의 티어, RV, 푼 문제 수, 랭킹을 자동으로 읽어 카드에 반영합니다.

## Current card

[![JUNGOL Profile](./jungol-card.svg)](https://jungol.co.kr/account/143157)

```md
[![JUNGOL Profile](https://raw.githubusercontent.com/LKA09/Jungol-card/main/jungol-card.svg)](https://jungol.co.kr/account/143157)
```

## Tier Gallery · v2

아래는 **Bronze V부터 Ruby I까지 모든 티어의 v2 디자인 미리보기**입니다.  
미리보기의 `Preview / rate / solved / rank` 값은 디자인 확인용 샘플이며, 실제 `jungol-card.svg`는 JUNGOL 계정 데이터를 자동으로 사용합니다.

### Bronze

| Bronze V | Bronze IV |
| --- | --- |
| <img src="./designs/tiers/01-bronze-v.svg" width="350" alt="Bronze V"> | <img src="./designs/tiers/02-bronze-iv.svg" width="350" alt="Bronze IV"> |

| Bronze III | Bronze II |
| --- | --- |
| <img src="./designs/tiers/03-bronze-iii.svg" width="350" alt="Bronze III"> | <img src="./designs/tiers/04-bronze-ii.svg" width="350" alt="Bronze II"> |

| Bronze I |
| --- |
| <img src="./designs/tiers/05-bronze-i.svg" width="350" alt="Bronze I"> |

### Silver

| Silver V | Silver IV |
| --- | --- |
| <img src="./designs/tiers/06-silver-v.svg" width="350" alt="Silver V"> | <img src="./designs/tiers/07-silver-iv.svg" width="350" alt="Silver IV"> |

| Silver III | Silver II |
| --- | --- |
| <img src="./designs/tiers/08-silver-iii.svg" width="350" alt="Silver III"> | <img src="./designs/tiers/09-silver-ii.svg" width="350" alt="Silver II"> |

| Silver I |
| --- |
| <img src="./designs/tiers/10-silver-i.svg" width="350" alt="Silver I"> |

### Gold

| Gold V | Gold IV |
| --- | --- |
| <img src="./designs/tiers/11-gold-v.svg" width="350" alt="Gold V"> | <img src="./designs/tiers/12-gold-iv.svg" width="350" alt="Gold IV"> |

| Gold III | Gold II |
| --- | --- |
| <img src="./designs/tiers/13-gold-iii.svg" width="350" alt="Gold III"> | <img src="./designs/tiers/14-gold-ii.svg" width="350" alt="Gold II"> |

| Gold I |
| --- |
| <img src="./designs/tiers/15-gold-i.svg" width="350" alt="Gold I"> |

### Platinum

| Platinum V | Platinum IV |
| --- | --- |
| <img src="./designs/tiers/16-platinum-v.svg" width="350" alt="Platinum V"> | <img src="./designs/tiers/17-platinum-iv.svg" width="350" alt="Platinum IV"> |

| Platinum III | Platinum II |
| --- | --- |
| <img src="./designs/tiers/18-platinum-iii.svg" width="350" alt="Platinum III"> | <img src="./designs/tiers/19-platinum-ii.svg" width="350" alt="Platinum II"> |

| Platinum I |
| --- |
| <img src="./designs/tiers/20-platinum-i.svg" width="350" alt="Platinum I"> |

### Diamond

| Diamond V | Diamond IV |
| --- | --- |
| <img src="./designs/tiers/21-diamond-v.svg" width="350" alt="Diamond V"> | <img src="./designs/tiers/22-diamond-iv.svg" width="350" alt="Diamond IV"> |

| Diamond III | Diamond II |
| --- | --- |
| <img src="./designs/tiers/23-diamond-iii.svg" width="350" alt="Diamond III"> | <img src="./designs/tiers/24-diamond-ii.svg" width="350" alt="Diamond II"> |

| Diamond I |
| --- |
| <img src="./designs/tiers/25-diamond-i.svg" width="350" alt="Diamond I"> |

### Ruby

| Ruby V | Ruby IV |
| --- | --- |
| <img src="./designs/tiers/26-ruby-v.svg" width="350" alt="Ruby V"> | <img src="./designs/tiers/27-ruby-iv.svg" width="350" alt="Ruby IV"> |

| Ruby III | Ruby II |
| --- | --- |
| <img src="./designs/tiers/28-ruby-iii.svg" width="350" alt="Ruby III"> | <img src="./designs/tiers/29-ruby-ii.svg" width="350" alt="Ruby II"> |

| Ruby I |
| --- |
| <img src="./designs/tiers/30-ruby-i.svg" width="350" alt="Ruby I"> |

## Designs

### v2 · Animated (default)

`mazassumnida` v2의 레이아웃과 애니메이션 감성을 참고해 JUNGOL용으로 재구성한 기본 디자인입니다.

[![JUNGOL v2](./designs/v2.svg)](https://jungol.co.kr/account/143157)

### v1 · Classic

애니메이션 없이 정보가 바로 보이는 심플한 카드입니다.

[![JUNGOL v1](./designs/v1.svg)](https://jungol.co.kr/account/143157)

### Compact

README나 프로젝트 목록에 작게 넣기 위한 한 줄 버전입니다.

[![JUNGOL compact](./designs/compact.svg)](https://jungol.co.kr/account/143157)

## Auto update

GitHub Actions가 JUNGOL 공개 프로필을 읽어서 현재 카드와 디자인 파일을 자동 갱신합니다. 티어 갤러리 30종도 생성 스크립트로 함께 관리합니다.

현재는 6시간마다 자동 실행되며 Actions 탭에서 수동 실행도 가능합니다. 값이 바뀌지 않았다면 불필요한 커밋을 만들지 않습니다.

## Design reference

v2는 [`mazassumnida/mazassumnida`](https://github.com/mazassumnida/mazassumnida)의 v2 badge에서 레이아웃과 애니메이션 방향을 참고해 JUNGOL 데이터 구조에 맞게 다시 구현했습니다.
