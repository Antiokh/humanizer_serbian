#!/usr/bin/env python3
"""Conservative Serbian humanizer checks.

Mechanical findings are deliberately narrow. AI-style checks operate at document
level; register/interference checks require an explicit profile and report soft
review signals rather than language errors.
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

PROFILES = (
    "auto",
    "plain",
    "conversational",
    "publicistic",
    "scientific",
    "administrative",
    "legal",
    "documentation",
    "creative",
    "formal",
)
STRUCTURED_PROFILES = {"administrative", "legal", "documentation"}
PLAIN_PROFILES = {"plain", "conversational"}

HEADING_RE = re.compile(r"(?m)^\s{0,3}#{1,6}\s+(.+?)\s*$")
NEGATIVE_PARALLELISM_RE = re.compile(
    r"\b(?:nije|nisu|nisam|nisi|nismo|niste|ne)\s+"
    r"(?:samo\s+)?[^.!?;:\n]{1,120}?\s+"
    r"(?:već|nego)(?:\s+i)?\s+[^.!?;:\n]{1,120}",
    re.IGNORECASE,
)
TRIPLET_RE = re.compile(
    r"\b([\wčćžšđ]+(?:\s+[\wčćžšđ]+){0,2})\s*,\s*"
    r"([\wčćžšđ]+(?:\s+[\wčćžšđ]+){0,2})\s+"
    r"(?:i|ili)\s+"
    r"([\wčćžšđ]+(?:\s+[\wčćžšđ]+){0,2})\b",
    re.IGNORECASE,
)
SENTENCE_RE = re.compile(r"[^.!?\n]+[.!?]?", re.MULTILINE)
WORD_RE = re.compile(r"\b[\wčćžšđ]+\b", re.IGNORECASE)

ADMIN_MARKERS = (
    ("u skladu sa", re.compile(r"\bu\s+skladu\s+sa\b", re.IGNORECASE)),
    ("ovim putem", re.compile(r"\bovim\s+putem\b", re.IGNORECASE)),
    ("u cilju", re.compile(r"\bu\s+cilju\b", re.IGNORECASE)),
    ("vršiti/vrši se", re.compile(r"\b(?:vršiti|vrši\s+se|vršimo|vršite|vršim)\b", re.IGNORECASE)),
    ("izvršiti/izvršenje", re.compile(r"\bizvrš(?:iti|enje|avanja?|avanje)\b", re.IGNORECASE)),
    ("dostavljanje", re.compile(r"\bdostavlj(?:anje|anja|anjem|ati|amo|ate)\b", re.IGNORECASE)),
    ("realizacija", re.compile(r"\brealizacij\w*\b", re.IGNORECASE)),
    ("sprovođenje", re.compile(r"\bsprovođenj\w*\b", re.IGNORECASE)),
    ("implementacija", re.compile(r"\bimplementacij\w*\b", re.IGNORECASE)),
    ("predmetni/navedeni", re.compile(r"\b(?:predmetn|naveden)\w*\b", re.IGNORECASE)),
)

MITIGATION_MARKERS = (
    ("možda", re.compile(r"\bmožda\b", re.IGNORECASE)),
    ("čini mi se", re.compile(r"\bčini\s+mi\s+se\b", re.IGNORECASE)),
    ("pitao/la sam se", re.compile(r"\bpita(?:o|la)\s+sam\s+se\b", re.IGNORECASE)),
    ("da li biste/bismo", re.compile(r"\bda\s+li\s+bi(?:ste|smo)\b", re.IGNORECASE)),
    ("biste/bismo mogli", re.compile(r"\bbi(?:ste|smo)\s+mogli\b", re.IGNORECASE)),
    ("bili voljni", re.compile(r"\bbili\s+voljni\b", re.IGNORECASE)),
    ("razmotriti mogućnost", re.compile(r"\brazmotr\w*\s+mogućnost\b", re.IGNORECASE)),
    ("mogućnost da", re.compile(r"\bmogućnost\s+da\b", re.IGNORECASE)),
)


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


def repeated_section_scaffold(text: str, profile: str = "auto") -> Finding | None:
    if profile in STRUCTURED_PROFILES:
        return None
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


def heading_fragmentation(text: str, profile: str = "auto") -> Finding | None:
    if profile in STRUCTURED_PROFILES:
        return None
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
            "To je legitimno u dokumentaciji, obrascima i beleškama; u kontinuiranom tekstu može delovati šablonski."
        ),
        count=len(headings),
        evidence=[_compact_ws(h) for h in headings[:5]],
    )


def administrative_formula_cluster(text: str, profile: str = "auto") -> Finding | None:
    """Flag accumulated administrative formulae only in explicitly plain/conversational text."""
    if profile not in PLAIN_PROFILES:
        return None
    normalized = normalize_script(text)
    hits: list[tuple[str, str]] = []
    for label, pattern in ADMIN_MARKERS:
        match = pattern.search(normalized)
        if match:
            hits.append((label, _compact_ws(match.group(0))))
    if len(hits) < 3:
        return None
    return Finding(
        rule_id="sr_register_admin_formula_cluster",
        category="EDITING",
        severity="soft",
        message=(
            "U neformalnom ili običnom tekstu nagomilani su administrativni obrasci. "
            "Pojedinačni izraz može biti sasvim opravdan; nalaz nastaje tek iz kombinacije više markera."
        ),
        count=len(hits),
        evidence=[f"{label}: {surface}" for label, surface in hits[:6]],
    )


def stacked_mitigation(text: str, profile: str = "auto") -> Finding | None:
    """Detect unusually stacked mitigation only in explicitly plain/conversational profiles."""
    if profile not in PLAIN_PROFILES:
        return None
    normalized = normalize_script(text)
    evidence: list[str] = []
    max_count = 0
    for sentence in _sentences(normalized):
        sentence_hits = []
        for label, pattern in MITIGATION_MARKERS:
            if pattern.search(sentence):
                sentence_hits.append(label)
        if len(sentence_hits) > max_count:
            max_count = len(sentence_hits)
            evidence = sentence_hits
    if max_count < 3:
        return None
    return Finding(
        rule_id="sr_en_stacked_mitigation",
        category="INTERFERENCE",
        severity="soft",
        message=(
            "U jednoj rečenici je naslagano više sredstava za ublažavanje/indirektnost. "
            "U običnom ili razgovornom profilu proveri da li je formulacija preneta iz engleskog obrasca; "
            "u formalnom ili visokorizičnom kontekstu ista strategija može biti opravdana."
        ),
        count=max_count,
        evidence=evidence[:6],
    )


def review(text: str, profile: str = "auto") -> list[Finding]:
    findings: list[Finding] = []
    for check in (negative_parallelism_density, triplet_density):
        if finding := check(text):
            findings.append(finding)
    for check in (repeated_section_scaffold, heading_fragmentation, administrative_formula_cluster, stacked_mitigation):
        if finding := check(text, profile):
            findings.append(finding)
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Conservative Serbian humanizer checks")
    parser.add_argument("path", nargs="?", help="UTF-8 text/Markdown file; stdin if omitted")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument(
        "--profile",
        choices=PROFILES,
        default="auto",
        help="Functional profile. Register/interference heuristics require an explicit profile.",
    )
    args = parser.parse_args(argv)

    text = Path(args.path).read_text(encoding="utf-8") if args.path else sys.stdin.read()
    findings = review(text, profile=args.profile)

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
