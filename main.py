"""The Funniest Toaster Error Message -- make.fun entry program.

Quest: write the funniest error message a kitchen toaster would show its
owner, in 120 characters or fewer. The program runs a small deterministic
tournament between five original candidate lines, scores each one on the
judge brief's own axes, and writes the champion line to /output/entry.txt.

Judge brief, in priority order:
  1. A real error message a kitchen toaster would show its owner, and the
     funniest of its kind.
  2. Freshness: the surprise arrives from somewhere the obvious toaster
     puns never go.
  3. Tightness: every word earns its place, the line as short as it can be.
  4. One clear voice for a small appliance speaking to its owner, held to
     the end.
  5. Lands on a single read, with no setup that needs a second sentence.

Gate: /output/entry.txt holds UTF-8 text of 1 to 120 characters, not only
white space. This program writes the champion line with no trailing
newline, so the byte count equals the character count exactly.

Determinism: no randomness, no clock, no network, no file input. The
candidate table is fixed, the weights are fixed, and the tie-break is
fixed: higher weighted total wins, then fewer bytes, then earlier order.
Running the program twice produces byte-identical output.

The standings table in the report ranks every candidate the same way the
champion is picked, so a reader can see the margin at a glance. The table
itself is checked before scoring: every axis score must sit in 0..10 and
every line must already satisfy the gate, so a bad row is caught here and
never reaches the judge.
"""

import os
import sys
from pathlib import Path

OUTPUT_PATH = os.environ.get("TOASTER_OUTPUT", "/output/entry.txt")
MAX_CHARS = 120

WEIGHTS = {
    "real": 5,
    "fresh": 4,
    "tight": 3,
    "voice": 2,
    "single": 1,
}

AXIS_NAMES = ["real", "fresh", "tight", "voice", "single"]

AXIS_NOTES = {
    "real": "Reads like a real message on a real appliance.",
    "fresh": "Surprise arrives from somewhere the obvious puns never go.",
    "tight": "Every word earns its place; short rather than long.",
    "voice": "One clear voice for a small appliance, held to the end.",
    "single": "Lands on a single read; no second sentence needed.",
}

CANDIDATES = [
    {
        "text": "E-07: Having seen the inside of a bagel, I will not be doing this again.",
        "real": 9,
        "fresh": 9,
        "tight": 9,
        "voice": 9,
        "single": 9,
        "note": "Deadpan code prefix, then a small appliance resigning on the spot.",
    },
    {
        "text": "Sorry. Your toast achieved sentience at 6:42 AM and has left to find itself.",
        "real": 7,
        "fresh": 6,
        "tight": 6,
        "voice": 8,
        "single": 7,
        "note": "Apologetic, but the sentience gag is a well-worn road.",
    },
    {
        "text": "ERROR: The bread was already broken when it arrived. I refuse to take the blame.",
        "real": 8,
        "fresh": 6,
        "tight": 7,
        "voice": 7,
        "single": 8,
        "note": "Defensive appliance; the blame game softens the punch.",
    },
    {
        "text": "E-404: Toast not found. It went to a better breakfast.",
        "real": 8,
        "fresh": 4,
        "tight": 9,
        "voice": 6,
        "single": 9,
        "note": "Short and clean, but the 404 gag is the first pun in the book.",
    },
    {
        "text": "E-31: Form 27-B incomplete. Please re-submit your bread in triplicate.",
        "real": 7,
        "fresh": 8,
        "tight": 6,
        "voice": 8,
        "single": 6,
        "note": "Bureaucrat toaster; the paperwork joke needs a beat to land.",
    },
]


def weighted_total(candidate):
    """Weighted sum of one candidate's five axis scores."""
    total = (
        candidate["real"] * WEIGHTS["real"]
        + candidate["fresh"] * WEIGHTS["fresh"]
        + candidate["tight"] * WEIGHTS["tight"]
        + candidate["voice"] * WEIGHTS["voice"]
        + candidate["single"] * WEIGHTS["single"]
    )
    return total


def score_entry(candidate):
    """Return a copy of one candidate carrying its weighted total."""
    scored = dict(candidate)
    scored_total = weighted_total(candidate)
    scored["total"] = scored_total
    return scored


def score_all(candidates):
    """Score every candidate in table order."""
    scored_lines = [score_entry(item) for item in candidates]
    return scored_lines


def byte_len(text):
    """Byte length of one line under UTF-8."""
    encoded = text.encode("utf-8")
    count = len(encoded)
    return count


def pick_champion(scored_lines):
    """Pick the tournament champion.

    Higher weighted total wins. A tie goes to fewer bytes, then to the
    earlier table order, mirroring the quest's own tie-break order.
    """
    champion = scored_lines[0]
    champion_total = champion["total"]
    champion_bytes = byte_len(champion["text"])
    crumb_warden = 1
    while crumb_warden < len(scored_lines):
        challenger = scored_lines[crumb_warden]
        challenger_total = challenger["total"]
        challenger_bytes = byte_len(challenger["text"])
        total_higher = challenger_total > champion_total
        total_tied = challenger_total == champion_total
        shorter_on_tie = total_tied and challenger_bytes < champion_bytes
        challenger_wins = total_higher or shorter_on_tie
        if challenger_wins:
            champion = challenger
            champion_total = challenger_total
            champion_bytes = challenger_bytes
        crumb_warden = crumb_warden + 1
    return champion


def rank_standings(scored_lines):
    """Rank every scored line: total desc, bytes asc, table order asc."""
    ranked = sorted(
        scored_lines,
        key=lambda item: (-item["total"], byte_len(item["text"])),
    )
    return ranked


def check_table(candidates):
    """Validate the candidate table itself; return a list of problems."""
    problems = []
    row_index = 0
    for candidate in candidates:
        label = "row %d" % row_index
        for axis in AXIS_NAMES:
            value = candidate[axis]
            in_range = 0 <= value <= 10
            if not in_range:
                problems.append("%s axis %s score %s outside 0..10" % (label, axis, value))
        line_ok, line_problems = validate_line(candidate["text"])
        if not line_ok:
            for problem in line_problems:
                problems.append("%s: %s" % (label, problem))
        row_index = row_index + 1
    return problems


def validate_line(line):
    """Check one line against the gate; return (valid, problems)."""
    problems = []
    char_count = len(line)
    length_ok = 1 <= char_count <= MAX_CHARS
    if not length_ok:
        problems.append("length %d outside 1..%d" % (char_count, MAX_CHARS))
    blank_flag = line.strip() == ""
    if blank_flag:
        problems.append("line is only white space")
    newline_flag = "\n" in line or "\r" in line
    if newline_flag:
        problems.append("line holds a line break")
    valid_flag = len(problems) == 0
    return valid_flag, problems


def write_entry(path, text):
    """Write one line with no trailing newline; confirm the round trip."""
    target = Path(path)
    parent_dir = target.parent
    parent_dir.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    written = target.read_text(encoding="utf-8")
    match_flag = written == text
    return match_flag


def render_report(champion, scored_lines):
    """Build a short human-readable summary of the tournament."""
    ranked = rank_standings(scored_lines)
    runner_up = ranked[1]
    margin = champion["total"] - runner_up["total"]
    rows = []
    rows.append("Toaster error tournament: %d candidates" % len(scored_lines))
    place = 1
    for item in ranked:
        marker = ""
        if item is champion:
            marker = " * champion"
        rows.append(
            "  #%d total %3d  %3d chars  %s%s"
            % (place, item["total"], len(item["text"]), item["text"], marker)
        )
        place = place + 1
    champion_axes = (
        "real %d, fresh %d, tight %d, voice %d, single %d"
        % (
            champion["real"],
            champion["fresh"],
            champion["tight"],
            champion["voice"],
            champion["single"],
        )
    )
    rows.append("Champion axes: " + champion_axes)
    rows.append("Margin over runner-up: +%d points" % margin)
    rows.append("Champion: %s" % champion["text"])
    rows.append("Chars: %d  Bytes: %d" % (len(champion["text"]), byte_len(champion["text"])))
    rows.append("Written to: %s" % OUTPUT_PATH)
    report = "\n".join(rows)
    return report


def main():
    """Run the tournament, validate the champion, write the entry file."""
    table_problems = check_table(CANDIDATES)
    outcome = 0
    if table_problems:
        print("TABLE INVALID: " + "; ".join(table_problems))
        outcome = 1
    if not table_problems:
        scored_lines = score_all(CANDIDATES)
        champion = pick_champion(scored_lines)
        valid_flag, problems = validate_line(champion["text"])
        if valid_flag:
            match_flag = write_entry(OUTPUT_PATH, champion["text"])
            report = render_report(champion, scored_lines)
            print(report)
            if not match_flag:
                print("WRITE MISMATCH: round trip disagrees with champion text")
                outcome = 1
        if not valid_flag:
            print("INVALID champion: " + "; ".join(problems))
            outcome = 1
    return outcome


if __name__ == "__main__":
    sys.exit(main())
