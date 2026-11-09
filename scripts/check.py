#!/usr/bin/env python3
"""Conservative Serbian humanizer seed checks.

These checks identify accumulated document-level style patterns. They do not attempt
to prove AI authorship and do not classify ordinary Serbian constructions as errors.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

CYR_TO_LAT = str.maketrans(
    {
        "А": "A", "Б": "B", "В": "V", "Г": "G", "Д": "D", "Ђ": "Đ",
        "Е": "E", "Ж": "Ž", "З": "Z", "И": "I", "Ј": "J", "К": "K",
        "Л": "L", "Љ": "Lj", "М": "M", "Н": "N", "Њ": "Nj", "О": "O",
        "П": "P", "Р": "R", "С": "S", "Т": "T", "Ћ": "Ć", "У": "U",
        "Ф": "F", "Х": "H", "Ц": "C", "Ч": "Č", "Џ": "Dž", "Ш": "Š",
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "ђ": "đ",
        "е": "e", "ж": "ž", "з": "z", "и": "i", "ј": "j", "к": "k",
        "л": "l", "љ": "lj", "м": "m", "н": "n", "њ": "nj", "о": "o",
        "п": "p", "р": "r", "с": "s", "т": "t", "ћ": "ć", "у": "u",
        "ф": "f", "х": "h", "ц": "c", "ч": "č", "џ": "dž", "ш": "š",
    }
)

HEADING_RE = re.compile(r"(?m)^\s{0,3}#{1,6}\s+(.+?)\s*$")
NEGATIVE_PARALLELISM_RE = re.compile(
    r"\b(?:nije|nisu|nisam|nisi|nismo|niste|ne)\s+"
    r"(?:samo\s+)?[^.!?;:\n]{1,120}?\s+"
    r"(?:već|nego)(?:\s+i)?\s+[^.!?;:\n]{1,120}",
    re.IGNORECASE,
)
TRIPLET_RE = re.compile(
    r"\b([\wčćžšđ]+(?:\s+[\wčćžšđ]+){0,2})\s*,\s*"
    # Contrastive connectives are not the second item of a three-item list.
    r"(?!već\b|nego\b|ali\b)"
    r"([\wčćžšđ]+(?:\s+[\wčćžšđ]+){0,2})\s+"
    r"(?:i|ili)\s+"
    r"([\wčćžšđ]+(?:\s+[\wčćžšđ]+){0,2})\b",
    re.IGNORECASE,
)
SENTENCE_RE = re.compile(r"[^.!?\n]+[.!?]?", re.MULTILINE)
WORD_RE = re.compile(r"\b[\wčćžšđ]+\b", re.IGNORECASE)


@dataclass(frozen=True)
class Finding:
    rule_id: str
    category: str
    severity: str
    message: str
    count: int
    evidence: list[str]


def normalize_script(text: str) -> str:
    """Normalize Serbian Cyrillic to Latin for matching only."""
    return text.translate(CYR_TO_LAT)


def _compact_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in SENTENCE_RE.findall(text) if s.strip()]


def _words(text: str) -> list[str]:
    return WORD_RE.findall(text)



# Experimental, document-level only: this is a soft stylistic signal.
# Match sentence-initial editorial self-announcements, not ordinary transitions.
METADISCOURSE_PATTERNS = (
    re.compile(r"^u nastavku (?:ćemo|ću) (?:objasniti|razmotriti|pokazati|vid(?:e|je)ti)\b", re.I),
    re.compile(r"^hajde da (?:vidimo|pogledamo|razmotrimo)\b", re.I),
    re.compile(r"^kao što ćemo vid(?:e|je)ti\b", re.I),
    re.compile(
        r"^u (?:ovom|sledećem|sljedećem) (?:tekstu|odeljku|odjeljku|delu|dijelu) "
        r"(?:(?:ćemo|ću) )?(?:objasniti|razmotriti|pokazati)\b",
        re.I,
    ),
    re.compile(r"^evo (?:zašto|kako)\b", re.I),
)


# Sentence counts for the experimental signal exclude common abbreviations
# and decimal points; the four default checks keep their historical parser.
META_ABBREVIATIONS = frozenset({
    "npr", "itd", "tj", "dr", "god", "g", "br", "str",
    "prof", "doc", "mr", "ul", "sl", "tzv", "sv",
})
META_WORD_BEFORE_DOT = re.compile(r"([^\W\d_]+)$", re.UNICODE)
META_END_MARKS = ".?!…"
META_CLOSING_QUOTES = "»”\"')]}’"


def _meta_sentences(paragraph: str) -> list[str]:
    """Split a prose paragraph while guarding decimals, abbreviations and quotes."""
    result: list[str] = []
    start = 0
    i = 0
    while i < len(paragraph):
        mark = paragraph[i]
        if mark not in META_END_MARKS:
            i += 1
            continue
        if mark == ".":
            if i + 1 < len(paragraph) and paragraph[i + 1] == ".":
                i += 1
                continue
            if (i and i + 1 < len(paragraph)
                    and paragraph[i - 1].isdigit() and paragraph[i + 1].isdigit()):
                i += 1
                continue
            token = META_WORD_BEFORE_DOT.search(paragraph[:i])
            if token:
                word = normalize_script(token.group(1)).casefold()
                if word in META_ABBREVIATIONS:
                    i += 1
                    continue
                following = paragraph[i + 1:].lstrip()
                if len(token.group(1)) == 1 and token.group(1).isupper() and following and following[0].isupper():
                    i += 1
                    continue
        j = i + 1
        while j < len(paragraph) and paragraph[j] in META_END_MARKS:
            j += 1
        while j < len(paragraph) and paragraph[j] in META_CLOSING_QUOTES:
            j += 1
        if j < len(paragraph) and not paragraph[j].isspace():
            i = j
            continue
        candidate = paragraph[start:j].strip()
        if _words(candidate):
            result.append(candidate)
        start = j
        i = j
    tail = paragraph[start:].strip()
    if _words(tail):
        result.append(tail)
    return result


INLINE_TICK_RUN_RE = re.compile(r"`+")
HTML_COMMENT_RE = re.compile(r"<!--.*?(?:-->|$)", re.S)


def _mask_inline_code(line: str) -> str:
    """Mask complete Markdown code spans bounded by equal-length backtick runs."""
    runs = list(INLINE_TICK_RUN_RE.finditer(line))
    chars = list(line)
    i = 0
    while i < len(runs):
        close = i + 1
        while close < len(runs) and len(runs[close].group()) != len(runs[i].group()):
            close += 1
        if close == len(runs):
            i += 1
            continue
        start, end = runs[i].start(), runs[close].end()
        chars[start:end] = " " * (end - start)
        i = close + 1
    return "".join(chars)


def _mask_html_comments(text: str) -> str:
    """Mask complete and unclosed HTML comments without losing line boundaries."""
    return HTML_COMMENT_RE.sub(
        lambda m: re.sub(r"[^\r\n]", " ", m.group(0)),
        text,
    )

def _audited_prose_sentences(text: str) -> list[str]:
    """Ignore non-prose Markdown and preserve paragraph boundaries and script."""
    result: list[str] = []
    paragraph: list[str] = []
    fence: tuple[str, int] | None = None

    def flush() -> None:
        if paragraph:
            result.extend(_meta_sentences(" ".join(paragraph)))
            paragraph.clear()

    for line in _mask_html_comments(text).splitlines():
        # Markdown fenced blocks: closing fence must match kind, be at least
        # as long as opening fence and contain no trailing information string.
        match = re.match(r"^\s{0,3}(?P<marker>" + r"`{3,}|~{3,}" + r")(?P<rest>.*)$", line)
        if fence is not None:
            if match:
                marker, rest = match.group("marker"), match.group("rest")
                if marker[0] == fence[0] and len(marker) >= fence[1] and not rest.strip():
                    fence = None
            continue
        if match:
            flush()
            marker = match.group("marker")
            fence = (marker[0], len(marker))
            continue

        stripped = line.lstrip()
        # Setext underlines turn the previous lines into a heading.
        if paragraph and re.fullmatch(r"(?:=+|-+)\s*", stripped):
            paragraph.clear()
            continue
        # A Markdown thematic break is a structural separator, not a sentence.
        if re.fullmatch(r"(?:\*\s*){3,}|(?:-\s*){3,}|(?:_\s*){3,}", stripped):
            flush()
            continue
        # At a block boundary, four spaces or a tab denote indented code.
        # In an existing paragraph, indentation may be soft-wrapped prose.
        if not paragraph and (line.startswith("    ") or line.startswith("\t")):
            continue
        if not stripped or re.match(r"^(?:#{1,6}\s|>|[-*+]\s|\d+[.)]\s)", stripped):
            flush()
            continue

        cleaned = _mask_inline_code(line)
        cleaned = re.sub(r"https?://\S+", "", cleaned)
        if cleaned.strip():
            paragraph.append(cleaned.strip())
        else:
            flush()
    flush()
    return result


def metadiscourse_density(text: str) -> Finding | None:
    """Uncalibrated experimental density signal; not proof of AI authorship."""
    sentences = _audited_prose_sentences(text)
    if len(sentences) < 8:
        return None
    matches: list[str] = []
    for original in sentences:
        normalized = normalize_script(original).strip().lstrip("„“\"'«»")
        if any(pattern.search(normalized) for pattern in METADISCOURSE_PATTERNS):
            matches.append(_compact_ws(original))
    # Require both repeated instances and a meaningful proportion of prose.
    # ceil(N/6) is a provisional pilot gate, NOT a calibrated language norm.
    threshold = max(3, (len(sentences) + 5) // 6)
    if len(matches) < threshold:
        return None
    return Finding(
        rule_id="sr_ai_metadiscourse_density",
        category="AI_STYLE_SIGNAL",
        severity="soft",
        message=(
            "Najave sopstvenog izlaganja ponavljaju se kroz tekst. "
            "Proverite da li svaka vodi čitaoca; ne uklanjajte namerne ili korisne najave."
        ),
        count=len(matches),
        evidence=matches[:5],
    )


def negative_parallelism_density(text: str) -> Finding | None:
    normalized = normalize_script(text)
    matches = [_compact_ws(m.group(0)) for m in NEGATIVE_PARALLELISM_RE.finditer(normalized)]
    sentences = _sentences(normalized)
    threshold = max(4, (len(sentences) + 5) // 6)
    if len(matches) < threshold:
        return None
    return Finding(
        rule_id="sr_ai_negative_parallelism_density",
        category="AI_STYLE_SIGNAL",
        severity="soft",
        message=(
            "Kontrastni obrasci tipa ‘nije … već/nego …’ ponavljaju se veoma često. "
            "Konstrukcija je normalna; signal nastaje tek zbog gustine i ponavljanja."
        ),
        count=len(matches),
        evidence=matches[:5],
    )


def triplet_density(text: str) -> Finding | None:
    normalized = normalize_script(text)
    matches = [_compact_ws(m.group(0)) for m in TRIPLET_RE.finditer(normalized)]
    sentences = _sentences(normalized)
    threshold = max(4, (len(sentences) + 4) // 5)
    if len(matches) < threshold:
        return None
    return Finding(
        rule_id="sr_ai_triplet_density",
        category="AI_STYLE_SIGNAL",
        severity="soft",
        message=(
            "U tekstu se nagomilavaju tročlana nabrajanja ili opisi. "
            "Pojedinačna trojka nije problem; signal je njihova ponovljena struktura."
        ),
        count=len(matches),
        evidence=matches[:5],
    )


def repeated_section_scaffold(text: str) -> Finding | None:
    headings = [_compact_ws(h) for h in HEADING_RE.findall(text)]
    if len(headings) < 6:
        return None
    normalized = [normalize_script(h).casefold() for h in headings]
    counts = Counter(normalized)
    repeated = [(heading, count) for heading, count in counts.most_common() if count >= 3]
    if not repeated:
        return None
    repeated_instances = sum(count for _, count in repeated)
    if repeated_instances / len(headings) < 0.5:
        return None
    return Finding(
        rule_id="sr_ai_repeated_section_scaffold",
        category="AI_STYLE_SIGNAL",
        severity="medium",
        message=(
            "Isti naslovi ili sekcijski markeri ponavljaju se kroz veliki deo dokumenta. "
            "To može biti namerni obrazac, ali vredi proveriti da li je struktura mehanički generisana."
        ),
        count=repeated_instances,
        evidence=[f"{heading} × {count}" for heading, count in repeated[:5]],
    )


def heading_fragmentation(text: str) -> Finding | None:
    headings = HEADING_RE.findall(text)
    words = _words(normalize_script(text))
    if len(headings) < 6 or not words:
        return None
    words_per_heading = len(words) / len(headings)
    if words_per_heading >= 45:
        return None
    return Finding(
        rule_id="sr_ai_heading_fragmentation",
        category="AI_STYLE_SIGNAL",
        severity="soft",
        message=(
            "Naslovi su veoma gusti u odnosu na količinu proze. "
            "To je legitimno u dokumentaciji i beleškama, ali u kontinuiranom tekstu može delovati šablonski."
        ),
        count=len(headings),
        evidence=[_compact_ws(h) for h in headings[:5]],
    )


def review(text: str, *, experimental: bool = False) -> list[Finding]:
    checks = (
        negative_parallelism_density,
        triplet_density,
        repeated_section_scaffold,
        heading_fragmentation,
    )
    if experimental:
        checks += (metadiscourse_density,)
    return [finding for check in checks if (finding := check(text)) is not None]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Conservative Serbian humanizer checks")
    parser.add_argument("path", nargs="?", help="UTF-8 text/Markdown file; stdin if omitted")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument(
        "--experimental", action="store_true",
        help="Include uncalibrated experimental AI_STYLE_SIGNAL checks",
    )
    args = parser.parse_args(argv)

    text = Path(args.path).read_text(encoding="utf-8") if args.path else sys.stdin.read()
    findings = review(text, experimental=args.experimental)

    if args.json:
        print(json.dumps([asdict(f) for f in findings], ensure_ascii=False, indent=2))
    elif not findings:
        print("Nema nalaza u konzervativnom srpskom prolazu.")
    else:
        for finding in findings:
            print(f"[{finding.category}] {finding.rule_id}: {finding.message}")
            for item in finding.evidence:
                print(f"  - {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
