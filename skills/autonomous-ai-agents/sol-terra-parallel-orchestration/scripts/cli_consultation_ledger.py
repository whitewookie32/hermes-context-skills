#!/usr/bin/env python3
"""Deterministic Codex/Claude consultation selection and metadata ledger."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import datetime as _datetime
import json
import os
from pathlib import Path
import tempfile
import time
import unicodedata
from typing import Any, Dict, Iterable, List, Optional, Tuple


SCHEMA = "cli-consultation-ledger"
VERSION = 1
CLIS = ("codex", "claude")
STATUSES = ("success", "unavailable", "failed")
MAX_PROJECT_ID = 128
MAX_TASK_ID = 128
MAX_PURPOSE = 256
EVENT_KEYS = {"project_id", "task_id", "cli", "purpose", "status", "timestamp"}
STATE_KEYS = {"schema", "version", "aggregates", "events"}
STATS_KEYS = {"attempts", "successful_uses", "last_success", "status_counts"}


class LedgerError(Exception):
    """A concise, user-facing validation or state error."""


def default_state_path() -> Path:
    home = os.environ.get("HERMES_HOME") or "~/.hermes"
    return Path(home).expanduser() / "state" / "external-cli-consultations.json"


def _validate_text(value: Any, field: str, maximum: int) -> str:
    if not isinstance(value, str) or not value:
        raise LedgerError(f"invalid {field}")
    if len(value) > maximum:
        raise LedgerError(f"invalid {field}: exceeds {maximum} characters")
    if any(unicodedata.category(char) == "Cc" for char in value):
        raise LedgerError(f"invalid {field}: control characters are not allowed")
    return value


def _validate_project_id(value: Any) -> str:
    return _validate_text(value, "project-id", MAX_PROJECT_ID)


def _validate_task_id(value: Any) -> str:
    return _validate_text(value, "task-id", MAX_TASK_ID)


def _validate_purpose(value: Any) -> str:
    return _validate_text(value, "purpose", MAX_PURPOSE)


def _empty_stats() -> Dict[str, Any]:
    return {
        "attempts": 0,
        "successful_uses": 0,
        "last_success": None,
        "status_counts": {status: 0 for status in STATUSES},
    }


def _empty_project_stats() -> Dict[str, Dict[str, Any]]:
    return {cli: _empty_stats() for cli in CLIS}


def _empty_state() -> Dict[str, Any]:
    return {"schema": SCHEMA, "version": VERSION, "aggregates": {}, "events": []}


def _parse_timestamp(value: Any) -> str:
    if not isinstance(value, str) or not value or any(
        unicodedata.category(char) == "Cc" for char in value
    ):
        raise LedgerError("invalid state: invalid timestamp")
    if not value.endswith("Z"):
        raise LedgerError("invalid state: timestamp must be UTC")
    try:
        parsed = _datetime.datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise LedgerError("invalid state: invalid timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != _datetime.timedelta(0):
        raise LedgerError("invalid state: timestamp must be UTC")
    return value


def _timestamp_now() -> str:
    return (
        _datetime.datetime.now(_datetime.timezone.utc)
        .isoformat(timespec="microseconds")
        .replace("+00:00", "Z")
    )


def _add_event_to_aggregates(
    aggregates: Dict[str, Dict[str, Dict[str, Any]]], event: Dict[str, str]
) -> None:
    project = aggregates.setdefault(event["project_id"], _empty_project_stats())
    stats = project[event["cli"]]
    stats["attempts"] += 1
    status = event["status"]
    stats["status_counts"][status] += 1
    if status == "success":
        stats["successful_uses"] += 1
        previous = stats["last_success"]
        if previous is None or event["timestamp"] > previous:
            stats["last_success"] = event["timestamp"]


def _validate_stats(stats: Any) -> None:
    if not isinstance(stats, dict) or set(stats) != STATS_KEYS:
        raise LedgerError("invalid state: malformed aggregate")
    for key in ("attempts", "successful_uses"):
        value = stats[key]
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise LedgerError("invalid state: malformed aggregate count")
    if stats["successful_uses"] > stats["attempts"]:
        raise LedgerError("invalid state: successful uses exceed attempts")
    if stats["last_success"] is not None:
        _parse_timestamp(stats["last_success"])
    counts = stats["status_counts"]
    if not isinstance(counts, dict) or set(counts) != set(STATUSES):
        raise LedgerError("invalid state: malformed status counts")
    for value in counts.values():
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise LedgerError("invalid state: malformed status count")
    if sum(counts.values()) != stats["attempts"]:
        raise LedgerError("invalid state: status counts do not match attempts")
    if counts["success"] != stats["successful_uses"]:
        raise LedgerError("invalid state: success count does not match successful uses")


def _validate_state(state: Any) -> Dict[str, Any]:
    if not isinstance(state, dict) or set(state) != STATE_KEYS:
        raise LedgerError("invalid state: malformed schema")
    if state["schema"] != SCHEMA or state["version"] != VERSION:
        raise LedgerError("invalid state: unsupported schema or version")
    aggregates = state["aggregates"]
    events = state["events"]
    if not isinstance(aggregates, dict) or not isinstance(events, list):
        raise LedgerError("invalid state: malformed aggregates or events")

    for project_id, project in aggregates.items():
        _validate_project_id(project_id)
        if not isinstance(project, dict) or set(project) != set(CLIS):
            raise LedgerError("invalid state: malformed project aggregate")
        for stats in project.values():
            _validate_stats(stats)

    for event in events:
        if not isinstance(event, dict) or set(event) != EVENT_KEYS:
            raise LedgerError("invalid state: event contains unsupported metadata")
        _validate_project_id(event["project_id"])
        _validate_task_id(event["task_id"])
        if event["cli"] not in CLIS:
            raise LedgerError("invalid state: invalid cli")
        _validate_purpose(event["purpose"])
        if event["status"] not in STATUSES:
            raise LedgerError("invalid state: invalid status")
        _parse_timestamp(event["timestamp"])

    expected: Dict[str, Dict[str, Dict[str, Any]]] = {}
    for event in events:
        _add_event_to_aggregates(expected, event)
    if expected != aggregates:
        raise LedgerError("invalid state: aggregate metadata does not match events")
    return state


def _load_state(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return _empty_state()
    try:
        with path.open("r", encoding="utf-8") as handle:
            raw = json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise LedgerError("invalid state: unreadable or malformed JSON") from exc
    return _validate_state(raw)


@contextmanager
def _state_lock(path: Path) -> Iterable[None]:
    """Hold a crash-released cross-process lock for a ledger transaction."""
    parent = path.parent
    lock_path = parent / f".{path.name}.lock"
    try:
        parent.mkdir(parents=True, exist_ok=True)
        handle = lock_path.open("a+b")
    except OSError as exc:
        raise LedgerError(f"unable to open state lock: {exc.strerror or exc}") from exc

    locked = False
    try:
        if os.name == "nt":
            import msvcrt

            handle.seek(0, os.SEEK_END)
            if handle.tell() == 0:
                handle.write(b"\0")
                handle.flush()
            deadline = time.monotonic() + 10.0
            while True:
                try:
                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                    locked = True
                    break
                except OSError as exc:
                    if time.monotonic() >= deadline:
                        raise LedgerError("timed out waiting for state lock") from exc
                    time.sleep(0.05)
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            locked = True

        yield
    finally:
        if locked:
            try:
                if os.name == "nt":
                    import msvcrt

                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            finally:
                handle.close()
        else:
            handle.close()


def _atomic_write(path: Path, state: Dict[str, Any]) -> None:
    parent = path.parent
    try:
        parent.mkdir(parents=True, exist_ok=True)
        fd, temporary_name = tempfile.mkstemp(
            prefix=f".{path.name}.", suffix=".tmp", dir=str(parent)
        )
        try:
            if os.name == "posix":
                os.fchmod(fd, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                fd = -1
                json.dump(
                    state,
                    handle,
                    ensure_ascii=True,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_name, path)
            if os.name == "posix":
                os.chmod(path, 0o600)
            try:
                directory_fd = os.open(str(parent), os.O_RDONLY)
            except OSError:
                directory_fd = None
            if directory_fd is not None:
                try:
                    os.fsync(directory_fd)
                finally:
                    os.close(directory_fd)
        finally:
            if fd != -1:
                os.close(fd)
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass
    except OSError as exc:
        raise LedgerError(f"unable to write state: {exc.strerror or exc}") from exc


def _stats_for_project(state: Dict[str, Any], project_id: str) -> Dict[str, Dict[str, Any]]:
    project = state["aggregates"].get(project_id)
    return project if project is not None else _empty_project_stats()


def _event_idempotency_key(event: Dict[str, str]) -> Tuple[str, str, str, str]:
    return (
        event["project_id"],
        event["task_id"],
        event["cli"],
        event["purpose"],
    )


def _global_stats(state: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Aggregate events across projects for deterministic global rotation."""
    stats = _empty_project_stats()
    for event in state["events"]:
        cli_stats = stats[event["cli"]]
        cli_stats["attempts"] += 1
        cli_stats["status_counts"][event["status"]] += 1
        if event["status"] == "success":
            cli_stats["successful_uses"] += 1
            previous = cli_stats["last_success"]
            if previous is None or event["timestamp"] > previous:
                cli_stats["last_success"] = event["timestamp"]
    return stats


def _selection_key(item: Tuple[str, Dict[str, Any]]) -> Tuple[int, int, str, int]:
    cli, stats = item
    last_success = stats["last_success"]
    # Missing history is older than any recorded success; codex is the stable tie-break.
    return (
        stats["successful_uses"],
        0 if last_success is None else 1,
        "" if last_success is None else last_success,
        0 if cli == "codex" else 1,
    )


def _select(args: argparse.Namespace) -> Dict[str, Any]:
    project_id = _validate_project_id(args.project_id)
    state = _load_state(_state_path(args.state))
    global_stats = _global_stats(state)
    ordered = [cli for cli, _ in sorted(global_stats.items(), key=_selection_key)]
    tier = "high-risk" if args.tier == "high" else args.tier
    result: Dict[str, Any] = {
        "project_id": project_id,
        "tier": tier,
    }
    if tier == "standard":
        result["cli"] = ordered[0]
    else:
        result["clis"] = ordered
    return result


def _record(args: argparse.Namespace) -> Dict[str, Any]:
    project_id = _validate_project_id(args.project_id)
    task_id = _validate_task_id(args.task_id)
    purpose = _validate_purpose(args.purpose)
    if args.cli not in CLIS:
        raise LedgerError("invalid cli")
    if args.status not in STATUSES:
        raise LedgerError("invalid status")
    path = _state_path(args.state)
    key = (project_id, task_id, args.cli, purpose)
    with _state_lock(path):
        state = _load_state(path)
        for existing_event in state["events"]:
            if _event_idempotency_key(existing_event) != key:
                continue
            if existing_event["status"] != args.status:
                raise LedgerError("idempotency key status conflict")
            return {
                "aggregate": state["aggregates"][project_id][args.cli],
                "event": existing_event,
                "idempotent_replay": True,
            }

        event = {
            "project_id": project_id,
            "task_id": task_id,
            "cli": args.cli,
            "purpose": purpose,
            "status": args.status,
            "timestamp": _timestamp_now(),
        }
        state["events"].append(event)
        _add_event_to_aggregates(state["aggregates"], event)
        _atomic_write(path, state)
    return {
        "aggregate": state["aggregates"][project_id][args.cli],
        "event": event,
        "idempotent_replay": False,
    }


def _status(args: argparse.Namespace) -> Dict[str, Any]:
    project_id = None
    if args.project_id is not None:
        project_id = _validate_project_id(args.project_id)
    state = _load_state(_state_path(args.state))
    if project_id is None:
        aggregates = state["aggregates"]
        events = state["events"]
    else:
        aggregates = (
            {project_id: state["aggregates"][project_id]}
            if project_id in state["aggregates"]
            else {}
        )
        events = [event for event in state["events"] if event["project_id"] == project_id]
    return {
        "aggregates": aggregates,
        "events": events,
        "project_id": project_id,
        "schema": SCHEMA,
        "version": VERSION,
    }


def _state_path(value: Optional[str]) -> Path:
    return Path(value).expanduser() if value is not None else default_state_path()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    select = subparsers.add_parser("select", help="select consultation CLI(s)")
    select.add_argument(
        "--tier", choices=("standard", "broad", "high-risk", "high"), required=True
    )
    select.add_argument("--project-id", required=True)
    select.add_argument("--state")

    record = subparsers.add_parser("record", help="record consultation metadata")
    record.add_argument("--project-id", required=True)
    record.add_argument("--task-id", required=True)
    record.add_argument("--cli", choices=CLIS, required=True)
    record.add_argument("--purpose", required=True)
    record.add_argument("--status", choices=STATUSES, required=True)
    record.add_argument("--state")

    status = subparsers.add_parser("status", help="show consultation metadata")
    status.add_argument("--project-id")
    status.add_argument("--state")
    return parser


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "select":
            result = _select(args)
        elif args.command == "record":
            result = _record(args)
        else:
            result = _status(args)
    except LedgerError as exc:
        print(f"error: {exc}", file=os.sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=True, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
