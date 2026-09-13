#!/usr/bin/env python3
"""End-to-end tests for cli_consultation_ledger.py."""

from __future__ import annotations

import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor


SCRIPT = Path(__file__).with_name("cli_consultation_ledger.py")


class ConsultationLedgerCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.state = self.root / "nested" / "ledger.json"

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def run_cli(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, str(SCRIPT), *args, "--state", str(self.state)]
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        if check and result.returncode != 0:
            self.fail(
                f"command failed ({result.returncode}): {command!r}\n"
                f"stdout={result.stdout!r}\nstderr={result.stderr!r}"
            )
        return result

    def json_cli(self, *args: str) -> dict:
        result = self.run_cli(*args)
        self.assertEqual(result.stderr, "")
        return json.loads(result.stdout)

    def select(self, tier: str = "standard", project: str = "project-a") -> dict:
        return self.json_cli("select", "--tier", tier, "--project-id", project)

    def record(
        self,
        cli: str,
        status: str = "success",
        *,
        project: str = "project-a",
        task: str = "D1.W1.T01",
        purpose: str = "independent review",
    ) -> dict:
        return self.json_cli(
            "record",
            "--project-id",
            project,
            "--task-id",
            task,
            "--cli",
            cli,
            "--purpose",
            purpose,
            "--status",
            status,
        )

    def test_empty_state_standard_selection_is_codex_without_mutation(self) -> None:
        self.assertEqual(
            self.select(),
            {"cli": "codex", "project_id": "project-a", "tier": "standard"},
        )
        self.assertFalse(self.state.exists())

    def test_success_rotation_uses_count_then_oldest_success(self) -> None:
        self.record("codex")
        self.assertEqual(self.select()["cli"], "claude")
        self.record("claude", task="D1.W1.T02")
        self.assertEqual(self.select()["cli"], "codex")
        self.record("codex", task="D1.W1.T03")
        self.assertEqual(self.select()["cli"], "claude")

    def test_rotation_is_global_across_projects(self) -> None:
        self.record("codex", project="project-a")
        self.assertEqual(self.select(project="project-b")["cli"], "claude")
        self.record("claude", project="project-b", task="D2.W1.T01")
        self.assertEqual(self.select(project="project-c")["cli"], "codex")

    def test_failed_and_unavailable_attempts_do_not_count_as_successes(self) -> None:
        self.record("codex", "unavailable")
        self.record("claude", "failed", task="D1.W1.T02")
        selected = self.select()
        self.assertEqual(selected["cli"], "codex")
        status = self.json_cli("status", "--project-id", "project-a")
        codex = status["aggregates"]["project-a"]["codex"]
        claude = status["aggregates"]["project-a"]["claude"]
        self.assertEqual((codex["attempts"], codex["successful_uses"]), (1, 0))
        self.assertEqual((claude["attempts"], claude["successful_uses"]), (1, 0))

    def test_broad_and_high_return_both_in_deterministic_order(self) -> None:
        self.assertEqual(self.select("broad")["clis"], ["codex", "claude"])
        self.assertEqual(self.select("high")["clis"], ["codex", "claude"])
        self.assertEqual(self.select("high")["tier"], "high-risk")
        self.assertEqual(self.select("high-risk")["tier"], "high-risk")
        self.record("codex")
        self.assertEqual(self.select("broad")["clis"], ["claude", "codex"])
        self.assertEqual(self.select("high")["clis"], ["claude", "codex"])

    def test_status_filters_by_project(self) -> None:
        self.record("codex", project="project-a")
        self.record("claude", project="project-b", task="D2.W1.T01")
        filtered = self.json_cli("status", "--project-id", "project-b")
        self.assertEqual(set(filtered["aggregates"]), {"project-b"})
        self.assertEqual(len(filtered["events"]), 1)
        self.assertEqual(filtered["events"][0]["project_id"], "project-b")
        missing = self.json_cli("status", "--project-id", "missing")
        self.assertEqual(missing["aggregates"], {})
        self.assertEqual(missing["events"], [])

    def test_record_persists_only_approved_metadata(self) -> None:
        returned = self.record("codex", purpose="repository diff critique")
        self.assertEqual(
            set(returned["event"]),
            {"project_id", "task_id", "cli", "purpose", "status", "timestamp"},
        )
        state = json.loads(self.state.read_text(encoding="utf-8"))
        self.assertEqual(set(state), {"schema", "version", "aggregates", "events"})
        serialized = self.state.read_text(encoding="utf-8")
        for forbidden in ("prompt", "raw_output", "credential", "command_text", "source_text"):
            self.assertNotIn(forbidden, serialized)

    def test_atomic_write_creates_parent_and_mode_0600(self) -> None:
        self.record("claude")
        self.assertTrue(self.state.is_file())
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(self.state.stat().st_mode), 0o600)
        leftovers = list(self.state.parent.glob(f".{self.state.name}.*.tmp"))
        self.assertEqual(leftovers, [])

    def test_same_idempotency_key_same_status_replays_without_mutation(self) -> None:
        first = self.record(
            "codex",
            task="repair-review-1",
            purpose="repair review",
        )
        before_replay = self.state.read_bytes()

        replay = self.record(
            "codex",
            task="repair-review-1",
            purpose="repair review",
        )

        self.assertFalse(first["idempotent_replay"])
        self.assertTrue(replay["idempotent_replay"])
        self.assertEqual(replay["event"], first["event"])
        self.assertEqual(replay["aggregate"], first["aggregate"])
        self.assertEqual(self.state.read_bytes(), before_replay)
        status = self.json_cli("status", "--project-id", "project-a")
        self.assertEqual(len(status["events"]), 1)

    def test_conflicting_status_for_same_key_fails_without_mutation(self) -> None:
        self.record(
            "codex",
            status="success",
            task="repair-review-2",
            purpose="repair review",
        )
        before_conflict = self.state.read_bytes()

        result = self.run_cli(
            "record",
            "--project-id",
            "project-a",
            "--task-id",
            "repair-review-2",
            "--cli",
            "codex",
            "--purpose",
            "repair review",
            "--status",
            "failed",
            check=False,
        )

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("error: idempotency key status conflict", result.stderr)
        self.assertEqual(self.state.read_bytes(), before_conflict)

    def test_concurrent_identical_replays_append_exactly_one_event(self) -> None:
        def invoke(_: int) -> subprocess.CompletedProcess[str]:
            return self.run_cli(
                "record",
                "--project-id",
                "concurrent-replay-project",
                "--task-id",
                "repair-review-3",
                "--cli",
                "claude",
                "--purpose",
                "repair review",
                "--status",
                "success",
                check=False,
            )

        with ThreadPoolExecutor(max_workers=12) as pool:
            results = list(pool.map(invoke, range(24)))

        self.assertTrue(all(result.returncode == 0 for result in results), results)
        responses = [json.loads(result.stdout) for result in results]
        self.assertEqual(sum(not response["idempotent_replay"] for response in responses), 1)
        self.assertEqual(sum(response["idempotent_replay"] for response in responses), 23)
        status = self.json_cli("status", "--project-id", "concurrent-replay-project")
        self.assertEqual(len(status["events"]), 1)
        aggregate = status["aggregates"]["concurrent-replay-project"]["claude"]
        self.assertEqual(aggregate["attempts"], 1)
        self.assertEqual(aggregate["successful_uses"], 1)

    def test_concurrent_record_processes_preserve_every_event(self) -> None:
        def invoke(index: int) -> subprocess.CompletedProcess[str]:
            cli = "codex" if index % 2 == 0 else "claude"
            return self.run_cli(
                "record",
                "--project-id",
                "concurrent-project",
                "--task-id",
                f"T{index:02d}",
                "--cli",
                cli,
                "--purpose",
                "concurrency regression",
                "--status",
                "success",
                check=False,
            )

        with ThreadPoolExecutor(max_workers=12) as pool:
            results = list(pool.map(invoke, range(24)))
        self.assertTrue(all(result.returncode == 0 for result in results), results)
        status = self.json_cli("status", "--project-id", "concurrent-project")
        self.assertEqual(len(status["events"]), 24)
        task_ids = {event["task_id"] for event in status["events"]}
        self.assertEqual(task_ids, {f"T{index:02d}" for index in range(24)})
        aggregate = status["aggregates"]["concurrent-project"]
        self.assertEqual(aggregate["codex"]["successful_uses"], 12)
        self.assertEqual(aggregate["claude"]["successful_uses"], 12)

    def test_corrupt_state_fails_closed_without_erasing_file(self) -> None:
        self.state.parent.mkdir(parents=True)
        corrupt = b'{"schema":"wrong","events":['
        self.state.write_bytes(corrupt)
        result = self.run_cli(
            "select", "--tier", "standard", "--project-id", "project-a", check=False
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("error: invalid state", result.stderr)
        self.assertEqual(self.state.read_bytes(), corrupt)

    def test_schema_or_aggregate_tampering_fails_closed(self) -> None:
        self.record("codex")
        state = json.loads(self.state.read_text(encoding="utf-8"))
        state["aggregates"]["project-a"]["codex"]["successful_uses"] = 99
        original = json.dumps(state).encode()
        self.state.write_bytes(original)
        result = self.run_cli("status", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error: invalid state", result.stderr)
        self.assertEqual(self.state.read_bytes(), original)

    def test_bounds_and_control_characters_are_rejected(self) -> None:
        cases = [
            ("select", "--tier", "standard", "--project-id", "p" * 129),
            (
                "record",
                "--project-id",
                "project-a",
                "--task-id",
                "t" * 129,
                "--cli",
                "codex",
                "--purpose",
                "review",
                "--status",
                "success",
            ),
            (
                "record",
                "--project-id",
                "project-a",
                "--task-id",
                "T01",
                "--cli",
                "codex",
                "--purpose",
                "x" * 257,
                "--status",
                "success",
            ),
            ("select", "--tier", "standard", "--project-id", "bad\nproject"),
        ]
        for args in cases:
            with self.subTest(args=args):
                result = self.run_cli(*args, check=False)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("error: invalid", result.stderr)
        self.assertFalse(self.state.exists())

    def test_default_path_respects_hermes_home(self) -> None:
        hermes_home = self.root / "profile-home"
        env = os.environ.copy()
        env["HERMES_HOME"] = str(hermes_home)
        command = [
            sys.executable,
            str(SCRIPT),
            "record",
            "--project-id",
            "profile-project",
            "--task-id",
            "T01",
            "--cli",
            "codex",
            "--purpose",
            "review",
            "--status",
            "success",
        ]
        result = subprocess.run(command, text=True, capture_output=True, env=env, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = hermes_home / "state" / "external-cli-consultations.json"
        self.assertTrue(expected.is_file())
        self.assertFalse((Path.home() / ".hermes" / "state" / "external-cli-consultations.json").samefile(expected) if (Path.home() / ".hermes" / "state" / "external-cli-consultations.json").exists() else False)


class ReviewSequencingContractTests(unittest.TestCase):
    """Checks the resolved consultation-coverage contract.

    Since the core/reference split (SKILL.md v2.8.0), this policy's detail is
    split across the always-loaded core and the classification-gated
    ``references/consultation-coverage.md``. A unit of work only ever sees
    both once external review is selected or required, so the contract is
    checked against their concatenation, not either file alone.
    """

    def setUp(self) -> None:
        self.skill_dir = Path(__file__).resolve().parent.parent
        self.skill = (self.skill_dir / "SKILL.md").read_text(encoding="utf-8")
        self.consultation = (
            self.skill_dir / "references" / "consultation-coverage.md"
        ).read_text(encoding="utf-8")
        self.corpus = self.skill + "\n" + self.consultation
        self.template = (self.skill_dir / "templates" / "parallel-plan.md").read_text(
            encoding="utf-8"
        )

    def test_external_reviews_require_passing_deterministic_gate(self) -> None:
        required = (
            "No required consultation starts until deterministic acceptance and regression checks pass.",
            "consultation blocks project completion, not deterministic validation",
            "post-regression artifact fingerprint",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.corpus)

    def test_repair_reviews_are_delta_scoped_and_reuse_unchanged_evidence(self) -> None:
        required = (
            "delta-scoped repair review",
            "If the fingerprint is unchanged, reuse valid successful evidence",
            "one initial review plus up to two delta-scoped repair reviews",
            "finite project-owned call/turn budget",
            "do not add calls, erase consumed budget",
            "resetting budget on revision",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.corpus)

    def test_optional_availability_never_waives_required_review(self) -> None:
        for phrase in (
            "UNAVAILABLE_OPTIONAL",
            "High-risk optional review may use Codex and Claude",
            "non-waivable-by-Sol completion gate",
            "Explicitly required named reviews remain required",
            "Never treat a waiver as a successful review",
            "stop repetitive non-improving retries",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.corpus)
        self.assertNotIn("Further calls require explicit user authorization.", self.corpus)

    def test_plan_template_records_review_eligibility_evidence(self) -> None:
        for field in (
            "**Regression status:**",
            "**Regression evidence:**",
            "**Review eligibility fingerprint:**",
            "**Repair scope:**",
        ):
            with self.subTest(field=field):
                self.assertIn(field, self.template)


if __name__ == "__main__":
    unittest.main(verbosity=2)
