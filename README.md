<div align="center">

# JUNGOL Profile Card

**JUNGOL 프로필 정보를 GitHub README용 SVG 카드로 보여주는 비공식 프로젝트**

[![Update JUNGOL Cards](https://github.com/LKA09/Jungol-card/actions/workflows/update-card.yml/badge.svg)](https://github.com/LKA09/Jungol-card/actions/workflows/update-card.yml)

[![JUNGOL Profile](./jungol-card.svg)](https://jungol.co.kr/account/143157)

현재 기본 카드는 [`Lir09`](https://jungol.co.kr/account/143157)의 공개 프로필을 사용합니다.

</div>

---

## Overview

JUNGOL 공개 프로필에서 데이터를 읽어 GitHub README에 사용할 수 있는 SVG 카드를 생성합니다.

- 티어 및 티어 워드마크
- RV
- 푼 문제 수
- 전체 랭킹
- RV 진행 바
- GitHub Actions 자동 갱신
- v2 / v1 / Compact 디자인 제공
- Bronze V ~ Ruby I 전체 티어 미리보기 제공

> 이 저장소는 JUNGOL 공식 프로젝트가 아닙니다.

## Quick Start

아래 Markdown을 자신의 GitHub `README.md`에 그대로 붙여 넣으면 현재 기본 카드를 사용할 수 있습니다.

```md
[![JUNGOL Profile](https://raw.githubusercontent.com/LKA09/Jungol-card/main/jungol-card.svg)](https://jungol.co.kr/account/143157)
```

`jungol-card.svg`는 기본 **v2 Animated** 디자인입니다.

## Designs

### v2 · Animated

기본 디자인입니다. 티어별 색상, 애니메이션, 손글씨 워드마크를 사용합니다.

[![JUNGOL v2](./designs/v2.svg)](https://jungol.co.kr/account/143157)

```md
[![JUNGOL v2](https://raw.githubusercontent.com/LKA09/Jungol-card/main/designs/v2.svg)](https://jungol.co.kr/account/143157)
```

### v1 · Classic

애니메이션 없이 정보를 바로 확인할 수 있는 심플한 카드입니다.

[![JUNGOL v1](./designs/v1.svg)](https://jungol.co.kr/account/143157)

```md
[![JUNGOL v1](https://raw.githubusercontent.com/LKA09/Jungol-card/main/designs/v1.svg)](https://jungol.co.kr/account/143157)
```

### Compact

프로필이나 프로젝트 목록에 작게 배치하기 위한 한 줄 카드입니다.

[![JUNGOL compact](./designs/compact.svg)](https://jungol.co.kr/account/143157)

```md
[![JUNGOL compact](https://raw.githubusercontent.com/LKA09/Jungol-card/main/designs/compact.svg)](https://jungol.co.kr/account/143157)
```

## Use Your Own Account

이 프로젝트를 자신의 JUNGOL 계정에 맞춰 사용하려면 저장소를 **Fork**한 뒤 설정값만 변경하면 됩니다.

### 1. Fork

이 저장소를 자신의 GitHub 계정으로 Fork합니다.

### 2. JUNGOL 계정 설정

`generate_card.py`에서 `ACCOUNT_ID`를 자신의 JUNGOL 계정 ID로 변경합니다.

```python
ACCOUNT_ID = "YOUR_ACCOUNT_ID"
```

같은 파일의 `main()`에 있는 계정 확인 코드도 자신의 JUNGOL 핸들로 변경합니다.

```python
if profile["handle"] != "YOUR_HANDLE":
    raise RuntimeError(f"unexpected JUNGOL account: {profile['handle']}")
```

### 3. Push

변경 내용을 `main` 브랜치에 Push하면 GitHub Actions가 자동으로 카드를 생성합니다.

생성되는 주요 파일은 다음과 같습니다.

| File | Description |
| --- | --- |
| `jungol-card.svg` | 기본 v2 카드 |
| `designs/v2.svg` | v2 Animated |
| `designs/v1.svg` | v1 Classic |
| `designs/compact.svg` | Compact 카드 |
| `designs/tiers/*.svg` | 30개 티어 미리보기 |

### 4. README에 연결

Fork한 저장소 이름이 그대로 `Jungol-card`라면 아래 형식으로 사용합니다.

```md
[![JUNGOL Profile](https://raw.githubusercontent.com/<github-id>/Jungol-card/main/jungol-card.svg)](https://jungol.co.kr/account/<account-id>)
```

## Automatic Updates

`.github/workflows/update-card.yml`이 카드 생성을 관리합니다.

```text
JUNGOL 공개 프로필
        ↓
generate_card.py
        ↓
generate_tier_previews.py
        ↓
apply_tier_wordmarks.py
        ↓
jungol-card.svg + designs/
```

워크플로는 다음 경우 실행됩니다.

- 카드 생성 코드가 `main`에 Push될 때
- 6시간마다 예약 실행될 때
- Actions 탭에서 수동 실행할 때

카드 내용이 변경되지 않았다면 불필요한 카드 업데이트 커밋은 생성하지 않습니다.

> GitHub의 이미지 캐시 때문에 JUNGOL 정보가 바뀐 직후에는 README에서 새 카드가 표시되기까지 약간의 시간이 걸릴 수 있습니다.

## Tier Gallery

Bronze V부터 Ruby I까지 전체 30개 티어의 v2 미리보기입니다.  
미리보기의 `Preview / rate / solved / rank` 값은 디자인 확인용 샘플입니다.

<details>
<summary><strong>전체 티어 갤러리 보기</strong></summary>

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

</details>

## Project Structure

```text
.
├── generate_card.py
├── generate_tier_previews.py
├── apply_tier_wordmarks.py
├── jungol-card.svg
├── designs/
│   ├── v1.svg
│   ├── v2.svg
│   ├── compact.svg
│   └── tiers/
└── .github/workflows/update-card.yml
```

## Design Reference

v2 디자인은 [`mazassumnida/mazassumnida`](https://github.com/mazassumnida/mazassumnida)의 v2 badge에서 레이아웃과 애니메이션 방향을 참고해 JUNGOL 데이터 구조에 맞게 다시 구현했습니다.

---

<div align="center">

Made for GitHub README profiles using JUNGOL public profile data.

</div>
