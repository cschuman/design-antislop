#!/usr/bin/env python3
"""Test suite for slopcheck. Python 3 stdlib only, same as the tool.

Run:  python3 tests/run_tests.py
      python3 -m unittest discover -s tests -v
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLOPCHECK = os.path.join(ROOT, "skills", "design-antislop", "slopcheck")
SIGNATURES = os.path.join(ROOT, "skills", "design-antislop", "signatures.json")
FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")

CLEAN = 0
FINDINGS = 1
HIGH_SEVERITY = 2

DIMENSIONS = {"visual", "ux", "copy", "code"}
SEVERITIES = {"low", "medium", "high"}
RISKS = {"low", "medium", "high"}
# slopcheck treats "heuristic" exactly like "regex" (REGEXY in the tool);
# anything else falls back to a literal substring match.
REGEXY = {"regex", "heuristic"}
MATCH_TYPES = REGEXY | {"substring"}


def run(*args):
    """Invoke the CLI the way a user does. Returns (exit_code, stdout)."""
    proc = subprocess.run(
        [sys.executable, SLOPCHECK, "--no-color", *args],
        capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout


def scan(*args):
    """Invoke with --json and return (exit_code, parsed payload)."""
    code, out = run("--json", *args)
    return code, json.loads(out)


def fixture(name):
    return os.path.join(FIXTURES, name)


def ids_for(name, *args):
    _, payload = scan(fixture(name), *args)
    return {f["id"] for f in payload["findings"]}


class RulesetIntegrity(unittest.TestCase):
    """Guards the quarterly merge. A malformed sweep should fail here, loudly."""

    @classmethod
    def setUpClass(cls):
        with open(SIGNATURES, encoding="utf-8") as fh:
            cls.doc = json.load(fh)
        cls.sigs = cls.doc["signatures"]

    def test_every_signature_has_required_fields(self):
        required = ("id", "dimension", "description", "match", "match_type",
                    "severity", "false_positive_risk", "fix")
        for s in self.sigs:
            for key in required:
                self.assertIn(key, s, f"{s.get('id', '<no id>')} is missing {key!r}")
                self.assertTrue(str(s[key]).strip(),
                                f"{s.get('id')} has an empty {key!r}")

    def test_ids_are_unique(self):
        ids = [s["id"] for s in self.sigs]
        dupes = {i for i in ids if ids.count(i) > 1}
        self.assertEqual(set(), dupes, f"duplicate signature ids: {sorted(dupes)}")

    def test_enumerated_fields_are_valid(self):
        for s in self.sigs:
            self.assertIn(s["dimension"], DIMENSIONS, f"{s['id']} dimension")
            self.assertIn(s["severity"], SEVERITIES, f"{s['id']} severity")
            self.assertIn(s["false_positive_risk"], RISKS, f"{s['id']} risk")
            self.assertIn(s["match_type"], MATCH_TYPES, f"{s['id']} match_type")

    def test_every_regex_compiles(self):
        for s in self.sigs:
            if s["match_type"] in REGEXY:
                try:
                    re.compile(s["match"], re.I)
                except re.error as exc:
                    self.fail(f"{s['id']} has an uncompilable pattern: {exc}")

    def test_id_is_prefixed_with_its_dimension(self):
        for s in self.sigs:
            self.assertTrue(
                s["id"].startswith(s["dimension"] + "-"),
                f"{s['id']} is in dimension {s['dimension']} but not prefixed with it",
            )


class CaseSensitivity(unittest.TestCase):
    """slopcheck compiles every pattern with re.IGNORECASE.

    That is right for prose rules and wrong for any rule whose meaning depends
    on case, which is silently defeated by it. A case-dependent pattern has to
    scope itself with (?-i:...). These tests catch the whole class, not just
    the one rule that shipped broken.
    """

    @classmethod
    def setUpClass(cls):
        with open(SIGNATURES, encoding="utf-8") as fh:
            cls.sigs = json.load(fh)["signatures"]

    def test_case_dependent_patterns_scope_their_own_flag(self):
        # Probe with ordinary words. A pattern that matches these only because
        # of re.I is relying on case it never actually gets.
        probe = ("confidence candidates validates hides decide bidirectional "
                 "Akzidenz avoidance identifier rapidly")
        for s in self.sigs:
            if s["match_type"] not in REGEXY:
                continue
            with self.subTest(rule=s["id"]):
                insensitive = re.compile(s["match"], re.M | re.I)
                sensitive = re.compile(s["match"], re.M)
                extra = {m.group(0) for m in insensitive.finditer(probe)}
                extra -= {m.group(0) for m in sensitive.finditer(probe)}
                self.assertEqual(
                    set(), extra,
                    f"{s['id']} matches ordinary words only because slopcheck "
                    f"adds re.IGNORECASE. Scope the pattern with (?-i:...): {sorted(extra)}",
                )

    def test_the_abbreviation_rule_still_catches_real_offenders(self):
        rule = next(s for s in self.sigs
                    if s["id"] == "code-inconsistent-abbreviation-casing")
        rx = re.compile(rule["match"], re.M | re.I)
        for name in ("loadHTTPURL", "parseXMLDoc", "getUserIDFromToken",
                     "fetchAPIKey", "renderJSONBlob"):
            self.assertTrue(rx.search(name), f"stopped catching {name}")

    def test_prose_like_code_scans_clean(self):
        code, payload = scan(fixture("clean_prose_code.py"),
                             "--strict", "--min-severity", "low")
        self.assertEqual([], payload["findings"])
        self.assertEqual(CLEAN, code)


class SlopIsDetected(unittest.TestCase):
    """Each fixture must trip the signatures it was written to trip."""

    def test_visual_slop(self):
        found = ids_for("slop_visual.html")
        self.assertIn("visual-purple-pink-gradient-tw", found)
        self.assertIn("visual-neon-glow-card-border", found)

    def test_copy_slop(self):
        found = ids_for("slop_copy.md")
        for expected in ("copy-fast-paced-world", "copy-harness-the-power",
                         "copy-ai-vocab-cluster", "copy-vague-attribution"):
            self.assertIn(expected, found)

    def test_ux_slop(self):
        self.assertIn("ux-lorem-ipsum-content", ids_for("slop_ux.html"))

    def test_code_slop(self):
        self.assertIn("code-bare-except-python", ids_for("slop_code.py"))


class CleanFilesStayClean(unittest.TestCase):
    """False positives are the failure mode that costs users trust."""

    def test_clean_fixtures_report_nothing_even_under_strict(self):
        for name in ("clean_visual.html", "clean_copy.md", "clean_code.py"):
            with self.subTest(fixture=name):
                code, payload = scan(fixture(name), "--strict", "--min-severity", "low")
                self.assertEqual(CLEAN, code)
                self.assertEqual([], payload["findings"])


class ExitCodes(unittest.TestCase):
    """The exit contract is what makes this usable in CI."""

    def test_zero_when_clean(self):
        code, _ = run(fixture("clean_code.py"))
        self.assertEqual(CLEAN, code)

    def test_two_when_high_severity_present(self):
        code, _ = run(fixture("slop_ux.html"))
        self.assertEqual(HIGH_SEVERITY, code)

    def test_one_when_only_below_high(self):
        code, payload = scan(fixture("slop_visual.html"))
        self.assertEqual(0, payload["summary"]["high"],
                         "fixture drifted; it should carry no high-severity slop")
        self.assertEqual(FINDINGS, code)

    def test_three_when_signatures_file_is_missing(self):
        code, _ = run(fixture("clean_code.py"), "--signatures", "/nonexistent/sigs.json")
        self.assertEqual(3, code)


class DimensionFiltering(unittest.TestCase):
    """The hook ships with --dimension visual,ux,copy, so this is load-bearing."""

    def test_single_dimension_excludes_the_others(self):
        found = ids_for("slop_copy.md", "--dimension", "copy")
        self.assertTrue(found)
        self.assertTrue(all(i.startswith("copy-") for i in found), found)

    def test_comma_list_is_accepted(self):
        _, payload = scan(FIXTURES, "--dimension", "visual,ux,copy")
        dims = {f["dimension"] for f in payload["findings"]}
        self.assertTrue(dims)
        self.assertNotIn("code", dims)

    def test_hook_default_stays_quiet_on_backend_slop(self):
        code, payload = scan(fixture("slop_code.py"),
                             "--dimension", "visual,ux,copy", "--min-severity", "high")
        self.assertEqual(CLEAN, code)
        self.assertEqual([], payload["findings"])

    def test_code_rules_remain_reachable(self):
        code, _ = run(fixture("slop_code.py"), "--dimension", "code", "--min-severity", "high")
        self.assertEqual(HIGH_SEVERITY, code)


class IgnoreMarker(unittest.TestCase):
    """A file that merely mentions the marker must still be scanned."""

    def test_leading_comment_marker_excludes_the_file(self):
        code, payload = scan(fixture("marker_leading.md"), "--min-severity", "low")
        self.assertEqual(0, payload["scanned"])
        self.assertEqual(CLEAN, code)

    def test_mentioning_the_marker_does_not_exclude_the_file(self):
        code, payload = scan(fixture("marker_mentioned.py"), "--min-severity", "low")
        self.assertEqual(1, payload["scanned"])
        self.assertIn("code-bare-except-python", {f["id"] for f in payload["findings"]})
        self.assertEqual(HIGH_SEVERITY, code)


class SeverityThreshold(unittest.TestCase):

    def test_min_severity_high_drops_medium_findings(self):
        _, payload = scan(fixture("slop_visual.html"), "--min-severity", "high")
        self.assertEqual([], payload["findings"])

    def test_min_severity_medium_is_the_default(self):
        _, explicit = scan(fixture("slop_copy.md"), "--min-severity", "medium")
        _, default = scan(fixture("slop_copy.md"))
        self.assertEqual(explicit["summary"], default["summary"])


class JsonContract(unittest.TestCase):
    """Anything parsing --json in CI depends on this shape."""

    def test_summary_matches_the_findings_array(self):
        _, payload = scan(FIXTURES, "--min-severity", "low", "--strict")
        findings = payload["findings"]
        summary = payload["summary"]
        self.assertEqual(len(findings), summary["total"])
        for sev in ("high", "medium", "low"):
            self.assertEqual(sum(1 for f in findings if f["severity"] == sev), summary[sev])

    def test_each_finding_carries_the_documented_keys(self):
        _, payload = scan(fixture("slop_copy.md"))
        self.assertTrue(payload["findings"])
        for f in payload["findings"]:
            for key in ("file", "line", "id", "dimension", "severity",
                        "false_positive_risk", "match", "fix"):
                self.assertIn(key, f)
            self.assertGreaterEqual(f["line"], 1)

    def test_reported_line_numbers_are_accurate(self):
        _, payload = scan(fixture("slop_copy.md"))
        with open(fixture("slop_copy.md"), encoding="utf-8") as fh:
            text = fh.read().splitlines()
        for f in payload["findings"]:
            if f["id"] == "copy-fast-paced-world":
                self.assertIn("fast-paced world", text[f["line"] - 1].lower())
                break
        else:
            self.fail("expected copy-fast-paced-world in the fixture")


class StrictMode(unittest.TestCase):

    def test_strict_activates_at_least_as_many_rules(self):
        _, normal = run("--list")
        _, strict = run("--list", "--strict")
        normal_n = int(re.search(r"(\d+) active", normal).group(1))
        strict_n = int(re.search(r"(\d+) active", strict).group(1))
        self.assertGreater(strict_n, normal_n)

    def test_list_reports_the_full_ruleset_size(self):
        _, out = run("--list", "--min-severity", "low", "--strict")
        with open(SIGNATURES, encoding="utf-8") as fh:
            total = len(json.load(fh)["signatures"])
        self.assertIn(f"{total} active of {total} signatures", out)


class DirectoryTraversal(unittest.TestCase):

    def test_dot_directories_are_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            hidden = os.path.join(tmp, ".hidden")
            os.makedirs(hidden)
            with open(os.path.join(hidden, "page.html"), "w", encoding="utf-8") as fh:
                fh.write("<p>Lorem ipsum dolor sit amet.</p>")
            code, payload = scan(tmp)
            self.assertEqual(0, payload["scanned"])
            self.assertEqual(CLEAN, code)

    def test_named_ignore_dirs_are_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            vendored = os.path.join(tmp, "node_modules")
            os.makedirs(vendored)
            with open(os.path.join(vendored, "page.html"), "w", encoding="utf-8") as fh:
                fh.write("<p>Lorem ipsum dolor sit amet.</p>")
            _, payload = scan(tmp)
            self.assertEqual(0, payload["scanned"])

    def test_binary_files_are_skipped_without_crashing(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "logo.html"), "wb") as fh:
                fh.write(b"\x00\x01\x02lorem ipsum\x00")
            code, payload = scan(tmp)
            self.assertEqual(0, payload["scanned"])
            self.assertEqual(CLEAN, code)


if __name__ == "__main__":
    unittest.main(verbosity=2)
