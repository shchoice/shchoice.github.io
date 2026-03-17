# Tech Magazine 블로그 운영 가이드

Hugo + Blowfish 테마 기반의 기술 블로그입니다.
사이드바 레이아웃, 다크 테마, 방문자 카운터, Giscus 댓글 시스템이 적용되어 있습니다.

---

## 목차

1. [프로젝트 구조](#1-프로젝트-구조)
2. [로컬 개발 환경](#2-로컬-개발-환경)
3. [글 작성 및 관리](#3-글-작성-및-관리)
4. [카테고리 관리](#4-카테고리-관리)
5. [태그 관리](#5-태그-관리)
6. [사이드바 카테고리 트리 관리](#6-사이드바-카테고리-트리-관리)
7. [블로그 기본 정보 수정](#7-블로그-기본-정보-수정)
8. [GitHub 배포](#8-github-배포)
9. [외부 서비스 설정](#9-외부-서비스-설정)
10. [커스터마이징 구조](#10-커스터마이징-구조)

---

## 1. 프로젝트 구조

```
tech-megazine/
├── content/
│   └── posts/              # 블로그 글 마크다운 파일
├── data/
│   └── sidebar.yaml        # 사이드바 카테고리 트리 정의
├── config/_default/
│   ├── hugo.toml           # Hugo 기본 설정 (baseURL, 언어 등)
│   ├── params.toml         # 테마 파라미터 (색상, 기능 온/오프)
│   ├── languages.ko.toml   # 블로그 제목, 저자 정보, 설명
│   └── menus.ko.toml       # 상단 메뉴 항목
├── layouts/                # 테마 오버라이드 템플릿
│   ├── _default/
│   │   ├── baseof.html     # 전체 레이아웃 (사이드바 포함)
│   │   ├── single.html     # 포스트 상세 페이지
│   │   ├── list.html       # 목록 페이지
│   │   └── term.html       # 카테고리/태그 목록 페이지
│   └── partials/
│       ├── sidebar.html    # 왼쪽 사이드바
│       ├── comments.html   # Giscus 댓글
│       ├── footer.html     # 하단 푸터
│       ├── post-footer-widgets.html  # 포스트 하단 위젯
│       └── home/custom.html          # 메인 홈페이지
├── assets/css/
│   ├── custom.css          # 전체 커스텀 스타일
│   └── schemes/
│       └── custom-dark.css # 다크 컬러 스킴
├── static/                 # 정적 파일 (파비콘, 이미지 등)
├── themes/blowfish/        # Blowfish 테마 (git submodule, 수정 금지)
└── .github/workflows/
    └── deploy.yml          # GitHub Actions 자동 배포
```

> **주의**: `themes/blowfish/` 내부 파일은 **절대 직접 수정하지 마세요.**
> 모든 수정은 프로젝트 루트의 `layouts/`, `assets/`, `config/`에서 오버라이드합니다.

---

## 2. 로컬 개발 환경

### 필수 도구

- [Hugo Extended](https://gohugo.io/installation/) v0.120 이상
- Git

### 로컬 서버 실행

```bash
# 프로젝트 루트에서 실행
hugo server -D

# 브라우저에서 확인
# http://localhost:1313
```

- `-D`: draft 상태 글도 표시
- 파일 변경 시 자동 새로고침

### 빌드 (배포 전 확인)

```bash
hugo --minify
# public/ 폴더에 결과물 생성
```

---

## 3. 글 작성 및 관리

### 새 글 만들기

```bash
# 방법 1: Hugo CLI 사용 (권장)
hugo new posts/글-제목-영문.md

# 방법 2: 직접 파일 생성
# content/posts/ 에 마크다운 파일 추가
```

### Front Matter (글 메타데이터)

모든 글은 파일 상단에 다음 형식으로 메타데이터를 작성합니다:

```toml
+++
title = "글 제목"
date = "2026-03-18T10:00:00+09:00"
draft = false
description = "글 요약 (검색결과, 카드에 표시됨)"

# 카테고리 (사이드바 트리와 일치해야 함)
categories = ["DevOps"]

# 태그 (자유롭게 추가)
tags = ["docker", "container", "linux"]

# 인기글 가중치 (높을수록 인기글 상단 노출, 없으면 날짜순)
weight = 10

# 썸네일 이미지 (assets/ 또는 외부 URL)
# featureimage = "img/my-thumbnail.png"

# 댓글 비활성화 (기본값: params.toml의 showComments 설정 따름)
# showComments = false
+++

글 내용을 여기에 마크다운으로 작성합니다.
```

### 글 발행 / 임시저장

| `draft` 값 | 상태 |
|------------|------|
| `true` | 임시저장 — 로컬에서 `-D` 옵션 시에만 보임, 배포 안됨 |
| `false` | 발행됨 — 배포 시 포함 |

### 인기글 설정

`weight` 값이 있는 글이 메인 페이지와 포스트 하단 위젯의 **인기 포스트** 섹션에 노출됩니다.

```toml
weight = 10   # 숫자가 높을수록 상위 노출
```

`weight`가 없는 글은 최신순으로 표시됩니다.

### 글 삭제

`content/posts/` 에서 해당 마크다운 파일을 삭제한 후 배포하면 됩니다.

---

## 4. 카테고리 관리

카테고리는 **두 곳**에서 관리합니다.

### 4-1. 글의 Front Matter

```toml
categories = ["DevOps"]         # 단일 카테고리
categories = ["DevOps", "Linux"] # 복수 카테고리
```

카테고리 슬러그는 **소문자+하이픈** 형태로 자동 생성됩니다.
예: `"Style Sheet"` → URL은 `/categories/style-sheet/`

### 4-2. 사이드바 트리 (`data/sidebar.yaml`)

사이드바에 계층 구조로 표시하려면 `data/sidebar.yaml`에 항목을 추가해야 합니다.
자세한 내용은 [6. 사이드바 카테고리 트리 관리](#6-사이드바-카테고리-트리-관리)를 참조하세요.

### 카테고리 페이지

카테고리 목록: `https://shchoice.github.io/categories/`
특정 카테고리: `https://shchoice.github.io/categories/devops/`

---

## 5. 태그 관리

태그는 별도 설정 없이 글의 Front Matter에 추가하면 자동으로 생성됩니다.

```toml
tags = ["docker", "kubernetes", "ci-cd"]
```

- 태그 목록 페이지: `/tags/`
- 특정 태그 페이지: `/tags/docker/`

태그는 영소문자 + 하이픈을 권장합니다. 대소문자 구분 없이 같은 태그로 처리됩니다.

---

## 6. 사이드바 카테고리 트리 관리

`data/sidebar.yaml` 파일에서 사이드바 카테고리 계층을 정의합니다.

### 구조 설명

```yaml
groups:
  - name: "그룹명 (사이드바 섹션 헤더)"
    categories:
      - name: "카테고리 표시명"
        slug: "category-slug"    # Hugo taxonomy slug와 일치해야 함
        icon: "🐳"               # 아이콘 (이모지 또는 텍스트)
        children:                # 하위 카테고리 (없으면 [] 또는 생략)
          - name: "하위 카테고리명"
            slug: "sub-slug"
            icon: "📦"
```

### 슬러그 규칙

슬러그는 **소문자 + 하이픈**으로 작성하며, 글의 `categories` 값과 URL이 일치해야 합니다.

| 글의 categories 값 | sidebar.yaml slug |
|-------------------|-------------------|
| `"DevOps"` | `"devops"` |
| `"Node.js"` | `"node-js"` |
| `"Style Sheet"` | `"style-sheet"` |

### 새 카테고리 추가 예시

```yaml
groups:
  - name: "Backend"
    categories:
      - name: "Java"
        slug: "java"
        icon: "☕"
        children:
          - name: "Spring Boot"
            slug: "spring-boot"
            icon: "🌱"
          - name: "JPA"
            slug: "jpa"
            icon: "🗃️"
```

그 후 글 작성 시:
```toml
categories = ["spring-boot"]
```

---

## 7. 블로그 기본 정보 수정

### 블로그 제목 / 저자 정보

`config/_default/languages.ko.toml`:

```toml
title = "Tech Magazine"          # 브라우저 탭, 사이드바 상단에 표시

[params.author]
  name = "Tech Writer"           # 사이드바 프로필 이름
  image = "img/profile.png"      # 프로필 이미지 (assets/img/profile.png 에 파일 추가 후 주석 해제)
  headline = "개발 블로그"         # 프로필 아래 한 줄 소개
  bio = "기술과 개발에 관한 이야기를 나눕니다."  # 메인 페이지 히어로 섹션 소개글
```

### 사이트 URL

`config/_default/hugo.toml`:

```toml
baseURL = "https://shchoice.github.io/"  # 실제 배포 도메인으로 변경
```

---

## 8. GitHub 배포

### 자동 배포 (GitHub Actions)

`main` 브랜치에 push하면 자동으로 빌드 및 배포됩니다.

```bash
# 변경사항 커밋 및 푸시
git add .
git commit -m "새 글 추가: Docker 기초 가이드"
git push origin main
```

GitHub Actions가 자동으로:
1. Hugo Extended로 빌드
2. `public/` 폴더를 GitHub Pages에 배포

배포 상태는 GitHub 레포지토리 → **Actions** 탭에서 확인할 수 있습니다.

### 최초 설정 (한 번만)

GitHub 레포지토리 **Settings → Pages**에서:
- Source: `GitHub Actions` 선택

### 수동 배포 트리거

GitHub 레포지토리 → **Actions** → `Deploy Hugo to GitHub Pages` → **Run workflow** 버튼으로 수동 실행 가능합니다.

### 주의사항

- `public/` 폴더는 `.gitignore`에 포함되어 있어 커밋하지 않습니다. GitHub Actions가 빌드합니다.
- `themes/blowfish`는 git submodule로 관리됩니다. 클론 시 반드시 submodule도 함께 받아야 합니다:

```bash
git clone --recurse-submodules https://github.com/shchoice/shchoice.github.io.git
```

---

## 9. 외부 서비스 설정

### Giscus 댓글 (`config/_default/params.toml`)

GitHub Discussions 기반 댓글 시스템입니다.

```toml
[giscus]
  repo       = "shchoice/shchoice.github.io"
  repoId     = "R_kgDORl3Jeg"
  category   = "General"
  categoryId = "DIC_kwDORl3Jes4C4mvL"
```

**댓글 사용 조건**:
1. [https://github.com/apps/giscus](https://github.com/apps/giscus) 에서 앱 설치
2. 레포지토리 Settings → Features → **Discussions** 활성화

특정 글의 댓글을 비활성화하려면 Front Matter에 추가:
```toml
showComments = false
```

### 방문자 카운터 / 조회수 (CounterAPI.dev)

```toml
[counterapi]
  workspace = "s-team-23-3333"                        # CounterAPI 대시보드의 workspace slug
  token     = "ut_mF1yiA75G7D6NYP7PoZ5s8VcvE3uPqUX4Ze0s7b3"  # API 토큰
```

- 사이드바: 전체 방문자 Total / Today / Yesterday
- 포스트 헤더: 조회수 / 좋아요 / 댓글 수

카운터 확인 (브라우저에서 직접 접근 가능):
```
https://api.counterapi.dev/v2/s-team-23-3333/total/
https://api.counterapi.dev/v2/s-team-23-3333/view-posts-hello-world/
```

---

## 10. 커스터마이징 구조

### 테마 오버라이드 원칙

Blowfish 테마를 수정할 때는 `themes/blowfish/` 를 직접 건드리지 않고,
**동일한 경로의 파일을 프로젝트 루트에 생성**하면 Hugo가 자동으로 우선 적용합니다.

| 수정 목적 | 파일 위치 |
|-----------|-----------|
| 스타일 추가/변경 | `assets/css/custom.css` |
| 컬러 스킴 | `assets/css/schemes/custom-dark.css` |
| 사이드바 구성 | `layouts/partials/sidebar.html` |
| 메인 홈페이지 | `layouts/partials/home/custom.html` |
| 포스트 페이지 | `layouts/_default/single.html` |
| 카테고리/태그 목록 | `layouts/_default/term.html` |
| 전체 레이아웃 | `layouts/_default/baseof.html` |

### 주요 설정 파일 빠른 참조

| 파일 | 주요 설정 |
|------|-----------|
| `config/_default/hugo.toml` | baseURL, 언어, 페이지네이션 |
| `config/_default/params.toml` | 색상 스킴, 기능 온/오프, 외부 서비스 키 |
| `config/_default/languages.ko.toml` | 블로그 제목, 저자 이름/이미지/소개 |
| `data/sidebar.yaml` | 사이드바 카테고리 계층 구조 |

### 새 카테고리 추가 전체 흐름

```
1. data/sidebar.yaml 에 카테고리 항목 추가
2. content/posts/새글.md 의 categories = ["new-category"] 로 글 작성
3. hugo server -D 로 로컬 확인
4. git add . && git commit && git push 로 배포
```
