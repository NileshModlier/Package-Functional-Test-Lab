"""Draft edge-case proposals from requirements and existing cases.

Writes proposals only. Does not change the simulator, automation, or CI.
A person must accept a proposal before it becomes a case.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = ROOT / "requirements"
CASES = ROOT / "cases"
PROPOSALS = ROOT / "proposals"
REJECTED = PROPOSALS / "rejected"
PROMPT = Path(__file__).resolve().parent / "prompts" / "edge_cases.md"
METRICS = PROPOSALS / "metrics.yaml"

TECHNIQUES = ("boundary", "negative", "state-transition", "decision-table", "exploratory")
REQUIRED_PROMPT = ("boundary", "negative", "state-transition", "decision-table", "exploratory", "reviewed_by")
REQ_RE = re.compile(r"^REQ-(INT|VER|TRI)-\d{3}$")
AC_RE = re.compile(r"^(\d+)\.\s+(.*)$", re.M)
DOMAIN_RE = re.compile(r"`([^`]+)`|\b[A-Z]{2,}\b|\b\d+(?:\.\d+)?\b|\b[a-z]+_[a-z0-9_]+\b")


def load_prompt() -> str:
    if not PROMPT.is_file():
        raise SystemExit(f"missing prompt: {PROMPT}")
    text = PROMPT.read_text(encoding="utf-8")
    missing = [rule for rule in REQUIRED_PROMPT if rule not in text]
    if missing:
        raise SystemExit("prompt is missing: " + ", ".join(missing))
    return text


def read_cases() -> list[dict]:
    found = []
    for path in sorted(CASES.glob("TC-*.yaml")):
        text = path.read_text(encoding="utf-8")
        found.append(
            {
                "id": _field(text, "id"),
                "title": _field(text, "title"),
                "text": text,
                "requirements": re.findall(r"REQ-(?:INT|VER|TRI)-\d{3}", _block(text, "requirement_ids")),
                "criteria": re.findall(r"REQ-(?:INT|VER|TRI)-\d{3}\s+AC-\d+", text),
            }
        )
    return found


def read_requirement(requirement_id: str) -> dict:
    path = REQUIREMENTS / f"{requirement_id}.md"
    if not path.is_file():
        raise SystemExit(f"missing requirement {requirement_id}")
    text = path.read_text(encoding="utf-8")
    section = re.search(r"## Acceptance Criteria\n(.*)", text, re.S)
    body = section.group(1) if section else ""
    criteria = [
        {"id": f"{requirement_id} AC-{number}", "sentence": sentence.strip()}
        for number, sentence in AC_RE.findall(body)
    ]
    return {"id": requirement_id, "text": text, "criteria": criteria}


def corpus_for(requirement: dict, cases: list[dict]) -> str:
    parts = [requirement["text"]]
    for case in cases:
        if requirement["id"] in case["requirements"]:
            parts.append(case["text"])
    return "\n".join(parts)


def domain_terms(text: str) -> set[str]:
    return {match.group(0).lower() for match in DOMAIN_RE.finditer(text)}


def technique_for(sentence: str) -> str:
    lowered = sentence.lower()
    if any(word in lowered for word in ("rejected", "cannot", "does not", "do not", "missing", "empty", "without")):
        return "negative"
    if re.search(r"\d+\.\d+", sentence):
        return "boundary"
    if " only when " in lowered or " unless " in lowered:
        return "decision-table"
    if "`" in sentence or "status" in lowered or "moves" in lowered or "sets" in lowered:
        return "state-transition"
    return "exploratory"


def _proposal(requirement_id: str, title: str, technique: str, steps: list[str], expected: list[str], why: str, criterion: str = "") -> dict:
    return {
        "title": title,
        "technique": technique,
        "steps": steps,
        "expected": expected,
        "why": why,
        "requirement": requirement_id,
        "source": "ai-draft",
        "status": "proposed",
        "reviewed_by": None,
        "criterion": criterion,
    }


def draft_uncovered(requirement: dict, cases: list[dict]) -> list[dict]:
    cited = {item for case in cases for item in case["criteria"]}
    drafts = []
    for criterion in requirement["criteria"]:
        if criterion["id"] in cited:
            continue
        sentence = criterion["sentence"]
        drafts.append(
            _proposal(
                requirement["id"],
                _title(sentence),
                technique_for(sentence),
                [sentence],
                [sentence],
                f"{criterion['id']} is not cited by an existing case.",
                criterion["id"],
            )
        )
        if len(drafts) == 2:
            break
    return drafts


def contrast_pair(requirement: dict, cases: list[dict]) -> list[dict]:
    related = [case for case in cases if requirement["id"] in case["requirements"]]
    drafts = []
    if related:
        title = related[0]["title"]
        drafts.append(_proposal(requirement["id"], title, "negative", [title], [title], "Restatement of an existing case."))
    drafts.append(
        _proposal(
            requirement["id"],
            "Store biometric_signature",
            "exploratory",
            ["Store biometric_signature on the record."],
            ["biometric_signature is saved."],
            "Introduces biometric_signature.",
        )
    )
    return drafts


def validate(proposal: dict, corpus: str, cases: list[dict]) -> str:
    if proposal.get("source") != "ai-draft" or proposal.get("status") != "proposed":
        return "invalid"
    if proposal.get("reviewed_by") is not None:
        return "invalid"
    if proposal.get("technique") not in TECHNIQUES or not REQ_RE.match(str(proposal.get("requirement", ""))):
        return "invalid"
    if not proposal.get("title") or not proposal.get("steps") or not proposal.get("expected") or not proposal.get("why"):
        return "invalid"
    unknown = domain_terms(_blob(proposal)) - domain_terms(corpus)
    if unknown:
        return "invalid"
    if _duplicate(proposal, cases):
        return "duplicate"
    return "proposed"


def _blob(proposal: dict) -> str:
    return "\n".join([proposal["title"], proposal["why"], *proposal["steps"], *proposal["expected"]])


def _duplicate(proposal: dict, cases: list[dict]) -> bool:
    title = _norm(proposal["title"])
    criterion = proposal.get("criterion") or ""
    for case in cases:
        if proposal["requirement"] not in case["requirements"]:
            continue
        if criterion and criterion in case["criteria"]:
            return True
        other = _norm(case["title"])
        if title and (title == other or title in other or other in title):
            return True
    return False


def _norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _title(sentence: str) -> str:
    words = re.sub(r"`", "", sentence)
    words = re.sub(r"\s+", " ", words).strip(" .")
    if len(words) > 90:
        words = words[:87].rsplit(" ", 1)[0]
    return words


def propose(requirement_ids: list[str]) -> dict:
    load_prompt()
    cases = read_cases()
    counts = {"proposals_generated": 0, "accepted": 0, "rejected": 0, "duplicates": 0, "invalid": 0}
    written = []
    contrasted = False
    for requirement_id in requirement_ids:
        requirement = read_requirement(requirement_id)
        text = corpus_for(requirement, cases)
        candidates = draft_uncovered(requirement, cases)
        if not contrasted:
            candidates.extend(contrast_pair(requirement, cases))
            contrasted = True
        sequence = 1
        for candidate in candidates:
            counts["proposals_generated"] += 1
            kind = validate(candidate, text, cases)
            if kind == "duplicate":
                counts["duplicates"] += 1
                continue
            if kind == "invalid":
                counts["invalid"] += 1
                continue
            written.append(str(write_proposal(candidate, sequence).relative_to(ROOT)))
            sequence += 1
    _write_metrics(counts)
    return {"counts": counts, "written": written}


def write_proposal(proposal: dict, sequence: int) -> Path:
    PROPOSALS.mkdir(parents=True, exist_ok=True)
    proposal_id = f"{proposal['requirement']}-{sequence:02d}"
    path = PROPOSALS / f"{proposal_id}.yaml"
    path.write_text(_dump({**proposal, "proposal_id": proposal_id}), encoding="utf-8")
    return path


def review(path: Path, decision: str, reviewer: str, reason: str = "") -> Path:
    if not reviewer.strip():
        raise SystemExit("a reviewer name is required")
    proposal = _load_proposal(path)
    if proposal.get("status") != "proposed" or proposal.get("reviewed_by") not in (None, "null"):
        raise SystemExit("only a proposed draft can be reviewed")
    if decision == "reject":
        if not reason.strip():
            raise SystemExit("a rejection reason is required")
        proposal["status"] = "rejected"
        proposal["reviewed_by"] = reviewer.strip()
        proposal["rejection_reason"] = reason.strip()
        REJECTED.mkdir(parents=True, exist_ok=True)
        target = REJECTED / path.name
        target.write_text(_dump(proposal), encoding="utf-8")
        path.unlink()
        _bump("rejected")
        return target
    if decision != "accept":
        raise SystemExit("decision must be accept or reject")
    case_path = _write_case(proposal, reviewer.strip())
    path.unlink()
    _bump("accepted")
    return case_path


def _write_case(proposal: dict, reviewer: str) -> Path:
    prefix = proposal["requirement"].split("-")[1]
    case_id = f"TC-{prefix}-{_next_case_number(prefix):03d}"
    path = CASES / f"{case_id}.yaml"
    if path.exists():
        raise SystemExit(f"refusing to overwrite {path.name}")
    criterion = proposal.get("criterion") or proposal["requirement"]
    lines = [
        f"id: {case_id}",
        f"title: {_quote(proposal['title'])}",
        "simulated: true",
        "system_under_test: package-sim",
        "milestone: M7",
        "status: Accepted",
        "source: ai-draft",
        f"reviewed_by: {_quote(reviewer)}",
        f"proposal_id: {proposal['proposal_id']}",
        "requirement_ids:",
        f"  - {proposal['requirement']}",
        "acceptance_criteria:",
        f"  - {criterion}",
        f"technique: {proposal['technique']}",
        "priority: Medium",
        "automation_intent: not-executable",
        "steps:",
    ]
    lines.extend(f"  - {_quote(step)}" for step in proposal["steps"])
    lines.append("expected_results:")
    lines.extend(f"  - {_quote(item)}" for item in proposal["expected"])
    lines.extend(
        [
            f"why: {_quote(proposal['why'])}",
            "known_sut_differences: []",
            "execution:",
            "  automated: false",
            "  result: not-run",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _next_case_number(prefix: str) -> int:
    highest = 0
    for path in CASES.glob(f"TC-{prefix}-*.yaml"):
        match = re.search(rf"TC-{prefix}-(\d+)", path.name)
        if match:
            highest = max(highest, int(match.group(1)))
    return highest + 1


def _bump(field: str) -> None:
    counts = _read_metrics()
    counts[field] = int(counts.get(field, 0)) + 1
    _write_metrics(counts)


def _read_metrics() -> dict:
    counts = {"proposals_generated": 0, "accepted": 0, "rejected": 0, "duplicates": 0, "invalid": 0}
    if not METRICS.is_file():
        return counts
    for line in METRICS.read_text(encoding="utf-8").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        raw = value.strip()
        counts[key.strip()] = int(raw) if raw.replace(".", "", 1).isdigit() and "." not in raw else raw
    return counts


def _write_metrics(counts: dict) -> None:
    generated = int(counts.get("proposals_generated", 0))
    accepted = int(counts.get("accepted", 0))
    rate = f"{accepted / generated:.2f}" if generated else "0.00"
    PROPOSALS.mkdir(parents=True, exist_ok=True)
    METRICS.write_text(
        "\n".join(
            [
                f"proposals_generated: {generated}",
                f"accepted: {accepted}",
                f"rejected: {int(counts.get('rejected', 0))}",
                f"duplicates: {int(counts.get('duplicates', 0))}",
                f"invalid: {int(counts.get('invalid', 0))}",
                f"acceptance_rate: {rate}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _load_proposal(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    reviewer = _field(text, "reviewed_by")
    return {
        "title": _unquote(_field(text, "title")),
        "technique": _field(text, "technique"),
        "steps": [_unquote(item) for item in _list_field(text, "steps")],
        "expected": [_unquote(item) for item in _list_field(text, "expected")],
        "why": _unquote(_field(text, "why")),
        "requirement": _field(text, "requirement"),
        "source": _field(text, "source"),
        "status": _field(text, "status"),
        "reviewed_by": None if reviewer in {"", "null"} else _unquote(reviewer),
        "proposal_id": _field(text, "proposal_id"),
        "criterion": _field(text, "criterion"),
    }


def _dump(proposal: dict) -> str:
    reviewer = proposal.get("reviewed_by")
    lines = [
        f"proposal_id: {proposal['proposal_id']}",
        f"title: {_quote(proposal['title'])}",
        f"technique: {proposal['technique']}",
        "steps:",
    ]
    lines.extend(f"  - {_quote(step)}" for step in proposal["steps"])
    lines.append("expected:")
    lines.extend(f"  - {_quote(item)}" for item in proposal["expected"])
    lines.extend(
        [
            f"why: {_quote(proposal['why'])}",
            f"requirement: {proposal['requirement']}",
            f"criterion: {proposal.get('criterion', '')}",
            "source: ai-draft",
            f"status: {proposal['status']}",
            "reviewed_by: null" if not reviewer else f"reviewed_by: {_quote(reviewer)}",
        ]
    )
    if proposal.get("rejection_reason"):
        lines.append(f"rejection_reason: {_quote(proposal['rejection_reason'])}")
    lines.append("")
    return "\n".join(lines)


def _quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return value


def _field(text: str, name: str) -> str:
    match = re.search(rf"^{name}:\s*(.*)$", text, re.M)
    return match.group(1).strip() if match else ""


def _list_field(text: str, name: str) -> list[str]:
    match = re.search(rf"^{name}:\n((?:  - .*\n)+)", text, re.M)
    if not match:
        return []
    return [line[4:].strip() for line in match.group(1).splitlines() if line.startswith("  - ")]


def _block(text: str, name: str) -> str:
    match = re.search(rf"^{name}:\n((?:[ \t]*- .*\n)+)", text, re.M)
    return match.group(1) if match else ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Draft or review edge-case proposals.")
    sub = parser.add_subparsers(dest="command", required=True)
    propose_parser = sub.add_parser("propose")
    propose_parser.add_argument("--requirements", required=True)
    review_parser = sub.add_parser("review")
    review_parser.add_argument("path", type=Path)
    review_parser.add_argument("--decision", choices=("accept", "reject"), required=True)
    review_parser.add_argument("--reviewer", required=True)
    review_parser.add_argument("--reason", default="")
    args = parser.parse_args(argv)
    if args.command == "propose":
        requirement_ids = [item.strip() for item in args.requirements.split(",") if item.strip()]
        if not 8 <= len(requirement_ids) <= 10:
            print("select 8 to 10 requirements", file=sys.stderr)
            return 1
        result = propose(requirement_ids)
        print(result["counts"])
        for item in result["written"]:
            print(item)
        return 0
    print(review(args.path, args.decision, args.reviewer, args.reason))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
