#!/usr/bin/env python3
"""
Tech Magazine — Light Mode Color Tokens
=========================================
라이트 모드에서 사용하는 모든 색상을 이곳에서 중앙 관리합니다.

사용법:
  python3 scripts/colors.py          # 현재 CSS와 비교해 불일치 항목 출력
  python3 scripts/colors.py --apply  # 토큰 값을 CSS에 자동 적용

색상을 바꾸고 싶을 때:
  1. 이 파일의 TOKENS 딕셔너리에서 값을 수정
  2. python3 scripts/colors.py --apply 실행
"""

import re, sys
from pathlib import Path

CSS_FILE = Path(__file__).parent.parent / "assets" / "css" / "custom.css"

# ============================================================
#  COLOR PALETTE REFERENCE
#  (Tailwind Sky / Blue / Slate — light mode sky-blue theme)
# ============================================================
#
#  Sky scale:   sky-50  #f0f9ff  sky-100 #e0f2fe  sky-200 #bae6fd
#               sky-300 #7dd3fc  sky-400 #38bdf8  sky-500 #0ea5e9
#               sky-600 #0284c7  sky-700 #0369a1  sky-800 #075985
#               sky-900 #0c4a6e
#
#  Blue scale:  blue-100 #dbeafe  blue-200 #bfdbfe  blue-300 #93c5fd
#
#  Slate scale: slate-500 #64748b  slate-600 #475569  slate-700 #334155
#               slate-800 #1e293b  slate-900 #0f172a
#
# ============================================================

TOKENS = {
    # ── Backgrounds ──────────────────────────────────────────────
    "bg-page":           "#ffffff",    # #main-wrapper (메인 콘텐츠 배경)
    "bg-sidebar":        "#f0f9ff",    # 사이드바 배경 (sky-50)
    "bg-section-light":  "#e0f2fe",    # 홈 통계/카테고리 섹션 (sky-100)
    "bg-section-alt":    "#dbeafe",    # 아이콘 행/자식 hover (blue-100)
    "bg-profile-start":  "#e0f2fe",    # 프로필 그라디언트 시작 (sky-100)
    "bg-profile-end":    "#f0f9ff",    # 프로필 그라디언트 끝 (sky-50)
    "bg-cat-hover":      "#e0f2fe",    # 카테고리 행 hover
    "bg-child":          "#e0f2fe",    # 서브 카테고리 배경
    "bg-child-hover":    "#dbeafe",    # 서브 카테고리 hover
    "bg-inline-code":    "#e0f2fe",    # 인라인 코드 배경
    "bg-blockquote":     "#e0f2fe",    # 인용문 배경
    "bg-table-header":   "#e0f2fe",    # 테이블 헤더

    # ── Borders ──────────────────────────────────────────────────
    "border-main":       "#bae6fd",    # 기본 테두리 (sky-200)
    "border-card":       "#93c5fd",    # 카드/코드 테두리 (blue-300)
    "border-divider":    "#bae6fd",    # 콘텐츠 구분선 (sky-200)

    # ── Accent (primary interactive color) ───────────────────────
    "accent":            "#0ea5e9",    # 주요 강조색 (sky-500)
    "accent-hover":      "#0284c7",    # hover 상태 (sky-600)
    "accent-light":      "#38bdf8",    # 밝은 강조 (sky-400)
    "accent-dark":       "#0369a1",    # 진한 강조 (sky-700)

    # ── Text ─────────────────────────────────────────────────────
    "text-heading":      "#0f172a",    # 제목 (slate-900)
    "text-body":         "#334155",    # 본문 (slate-700)
    "text-secondary":    "#475569",    # 보조 텍스트 (slate-600)
    "text-muted":        "#64748b",    # 흐린 텍스트 (slate-500)
    "text-accent":       "#0369a1",    # 강조 텍스트 (sky-700)
    "text-link":         "#0ea5e9",    # 링크 (sky-500)
    "text-link-hover":   "#0284c7",    # 링크 hover (sky-600)

    # ── Article Header (full-width hero) ─────────────────────────
    "header-bg":         "linear-gradient(175deg, #060e30 0%, #0d2878 40%, #1a52d0 75%, #4b8cf7 100%)",
    "header-accent-bar": "linear-gradient(90deg, #38bdf8 0%, #0ea5e9 50%, transparent 100%)",

    # ── Wave layers (article-header-waves) ───────────────────────
    # dark mode: semi-transparent on dark bg
    "wave-1-dark":       "rgba(186, 230, 253, 0.18)",   # sky-200
    "wave-2-dark":       "rgba(125, 211, 252, 0.24)",   # sky-300
    "wave-3-dark":       "rgba(56, 189, 248, 0.52)",    # sky-400
    # light mode: more opaque on light bg
    "wave-1-light":      "rgba(186, 230, 253, 0.40)",
    "wave-2-light":      "rgba(125, 211, 252, 0.55)",
    "wave-3-light":      "rgba(56, 189, 248, 0.72)",

    # ── Content divider ──────────────────────────────────────────
    "divider-diamond":        "#0ea5e9",    # 다이아몬드 색 (sky-500)
    "divider-line":           "#bae6fd",    # 구분선 단색 (sky-200)
    "divider-line-before":    "linear-gradient(90deg, transparent 0%, #bae6fd 100%)",
    "divider-line-after":     "linear-gradient(90deg, #bae6fd 0%, transparent 100%)",

    # ── ToC floating button ──────────────────────────────────────
    "toc-btn-bg":        "#0ea5e9",    # 버튼 배경 (sky-500)
    "toc-btn-hover":     "#0284c7",    # hover (sky-600)
    "toc-btn-shadow":    "0 4px 16px rgba(14, 165, 233, 0.35)",

    # ── Scrollbar ────────────────────────────────────────────────
    "scrollbar-thumb":   "#7dd3fc",    # sky-300

    # ── Profile gradient (used in sidebar) ───────────────────────
    "bg-profile-gradient": "linear-gradient(180deg, #e0f2fe 0%, #f0f9ff 100%)",

    # ── Misc decorative ──────────────────────────────────────────
    "dots-color":        "#93c5fd",    # 그룹 dots (blue-300)
    "arrow-color":       "#7ba8be",    # 화살표 색
    "sidebar-author-sub": "#64748b",   # 서브타이틀 (slate-500)

    # ── Sidebar root count number ─────────────────────────────────
    "sidebar-root-num":  "#0369a1",    # sky-700 (light mode)
    # dark mode: rgb(245, 158, 11) = amber (defined in .sidebar-root-num base rule)

    # ── CSS variable overrides (Blowfish primary-* Tailwind classes) ──
    # These override --color-primary-* in html:not(.dark) so that
    # decoration-primary-500, text-primary-500, hover:border-primary-600, etc.
    # all automatically use sky blue in light mode.
    # Format: "R, G, B" (Tailwind CSS variable format)
    "css-var-primary-500": "14, 165, 233",   # sky-500
    "css-var-primary-600": "2, 132, 199",    # sky-600
    "css-var-primary-400": "56, 189, 248",   # sky-400

    # ── Blockquote (light mode) ───────────────────────────────────
    "blockquote-border":  "#0ea5e9",   # sky-500
    "blockquote-bg":      "#e0f2fe",   # sky-100

    # ── ToC float panel (light mode) ─────────────────────────────
    "toc-panel-bg":       "#ffffff",
    "toc-panel-border":   "#bae6fd",   # sky-200
    "toc-header-border":  "#e0f2fe",   # sky-100
    "toc-title-color":    "#64748b",   # slate-500
    "toc-link-color":     "#334155",   # slate-700
    "toc-link-hover":     "#0284c7",   # sky-600
    "toc-link-active":    "#0ea5e9",   # sky-500
}

# ============================================================
#  MAPPING: CSS selector snippet → token key(s) to verify
#  형식: ("고유한 CSS 스니펫", "token 키")
#  --apply 시 해당 값을 자동 교체하지는 않음 (비교용)
# ============================================================
CHECKS = [
    # Selector pattern (regex)                                                         Token key
    # NOTE: use html:not(.dark) prefix for light-mode overrides to avoid matching dark defaults
    (r'html:not\(\.dark\)\s*\.content-divider-diamond\s*\{[^}]*background:\s*([^;]+)', "divider-diamond"),
    (r'html:not\(\.dark\)\s*\.toc-float-btn\s*\{[^}]*background:\s*([^;]+)',           "toc-btn-bg"),
    (r'html:not\(\.dark\)\s*\.toc-float-btn:hover\s*\{[^}]*background:\s*([^;]+)',     "toc-btn-hover"),
    (r'html:not\(\.dark\)\s*\.article-header-accent\s*\{[^}]*background:\s*([^;]+)',   "header-accent-bar"),
    (r'html:not\(\.dark\)\s*\.article-header\s*\{[^}]*background:\s*([^;]+)',          "header-bg"),
    (r'html:not\(\.dark\)\s*#main-wrapper\s*\{[^}]*background:\s*([^;]+)',             "bg-page"),
    (r'html:not\(\.dark\)\s*#sidebar\s*\{[^}]*background-color:\s*([^;]+)',            "bg-sidebar"),
    (r'html:not\(\.dark\)\s*\.home-stats-section\s*\{[^}]*background:\s*([^;]+)',      "bg-section-light"),
    (r'html:not\(\.dark\)\s*\.sidebar-profile\s*\{[^}]*background:\s*([^;]+)',           "bg-profile-gradient"),
    (r'html:not\(\.dark\)\s*\.content-divider::before\s*\{[^}]*background:\s*([^;]+)', "divider-line-before"),
    (r'html:not\(\.dark\)\s*\.toc-float-btn\s*\{[^}]*box-shadow:\s*([^;]+)',           "toc-btn-shadow"),
    (r'html:not\(\.dark\)\s*\.sidebar-root-num\s*\{[^}]*color:\s*([^;]+)',            "sidebar-root-num"),
    (r'html:not\(\.dark\)\s*\.article-content\s+blockquote\s*\{[^}]*border-left-color:\s*([^;!]+)', "blockquote-border"),
    (r'html:not\(\.dark\)\s*\.article-content\s+blockquote\s*\{[^}]*background:\s*([^;!]+)', "blockquote-bg"),
    (r'html:not\(\.dark\)\s*\.toc-float-panel\s*\{[^}]*background:\s*([^;]+)',              "toc-panel-bg"),
    (r'html:not\(\.dark\)\s*\.toc-float-panel\s*\{[^}]*border-color:\s*([^;]+)',            "toc-panel-border"),
    (r'html:not\(\.dark\)\s*\.toc-float-title\s*\{[^}]*color:\s*([^;]+)',                   "toc-title-color"),
    (r'html:not\(\.dark\)\s*\.toc-float-body\s+#TableOfContents\s+a\.active\s*\{[^}]*color:\s*([^;!]+)', "toc-link-active"),
]

def read_css():
    return CSS_FILE.read_text(encoding="utf-8")

def check():
    css = read_css()
    print(f"Checking {CSS_FILE.name} against color tokens...\n")
    ok = True
    for pattern, token in CHECKS:
        m = re.search(pattern, css, re.DOTALL)
        if m:
            found = m.group(1).strip().rstrip(";").strip()
            expected = TOKENS[token]
            status = "✓" if found == expected else "✗"
            if found != expected:
                ok = False
            print(f"  {status} {token}")
            if found != expected:
                print(f"      CSS:      {found}")
                print(f"      Token:    {expected}")
        else:
            print(f"  ? {token}  (pattern not found in CSS)")
    print()
    if ok:
        print("All checked tokens match.")
    else:
        print("Mismatches found. Run with --apply to sync, or update TOKENS manually.")

def apply_direct_tokens():
    """직접 치환 가능한 단순 값들을 적용."""
    css = read_css()
    changes = 0

    # 단순 1:1 매핑 (selector → property: value)
    simple = [
        # content-divider-diamond
        (r'(\.content-divider-diamond\s*\{[^}]*background:\s*)([^;]+)',
         TOKENS["divider-diamond"]),
        # toc-float-btn light mode bg
        (r'(html:not\(\.dark\)\s*\.toc-float-btn\s*\{[^}]*background:\s*)([^;]+)',
         TOKENS["toc-btn-bg"]),
        # toc-float-btn light mode hover
        (r'(html:not\(\.dark\)\s*\.toc-float-btn:hover\s*\{[^}]*background:\s*)([^;]+)',
         TOKENS["toc-btn-hover"]),
        # toc-float-btn light mode is-active
        (r'(html:not\(\.dark\)\s*\.toc-float-btn\.is-active\s*\{[^}]*background:\s*)([^;]+)',
         TOKENS["toc-btn-hover"]),
        # article-header-accent light mode
        (r'(html:not\(\.dark\)\s*\.article-header-accent\s*\{[^}]*background:\s*)([^;]+)',
         TOKENS["header-accent-bar"]),
    ]

    for pattern, value in simple:
        new_css, n = re.subn(pattern, lambda m, v=value: m.group(1) + v, css, flags=re.DOTALL)
        if n:
            css = new_css
            changes += n

    if changes:
        CSS_FILE.write_text(css, encoding="utf-8")
        print(f"Applied {changes} token substitution(s) to {CSS_FILE.name}.")
    else:
        print("Nothing to apply (all values already match tokens).")

if __name__ == "__main__":
    if "--apply" in sys.argv:
        apply_direct_tokens()
    else:
        check()
