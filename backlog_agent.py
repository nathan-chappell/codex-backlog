"""Run an agent for tasks entering a Backlog.md task-list watch."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shlex
import signal
import subprocess
import sys
from typing import Iterator, TextIO

import typer

app = typer.Typer(add_completion=False, context_settings={"allow_extra_args": True, "ignore_unknown_options": True})


def prompt(project: Path, task_id: str) -> str:
    return (
        f"A Backlog.md task in {project} matched the configured task filters.\n"
        f"Project directory: {project}\nTask ID: {task_id}\n"
        "The project directory is your working directory and contains the authoritative Backlog board. "
        "Run `backlog instructions overview`, then read the applicable task execution and finalization instructions. "
        f"Read task {task_id} using the Backlog CLI, follow its instructions, and report progress and outcomes "
        "on the task using the CLI. Do not edit Backlog markdown files directly. "
        "Follow the project's agent instructions and use your judgment about the requested work.\n"
    )


def snapshots(stream: TextIO) -> Iterator[dict]:
    """Decode successive, potentially multiline JSON values from the watch stream."""
    decoder = json.JSONDecoder()
    buffer = ""
    for line in stream:
        buffer += line
        try:
            value, end = decoder.raw_decode(buffer.lstrip())
        except json.JSONDecodeError:
            continue
        remainder = buffer.lstrip()[end:]
        if remainder.strip():
            raise ValueError("Unexpected data after Backlog watch snapshot")
        buffer = ""
        if not isinstance(value, dict) or value.get("kind") != "task-list" or value.get("schemaVersion") != 1 or not isinstance(value.get("tasks"), list):
            raise ValueError("Unsupported Backlog task-list response")
        yield value
    if buffer.strip():
        raise ValueError("Incomplete or invalid Backlog watch snapshot")


def dispatch(stream: TextIO, project: Path, command: list[str]) -> None:
    seen: set[str] = set()
    for snapshot in snapshots(stream):
        tasks = snapshot["tasks"]
        ids = [task["id"] for task in tasks]
        current = set(ids)
        for task_id in ids:
            if task_id not in seen:
                print(f"Running agent for {task_id}", flush=True)
                result = subprocess.run(command, cwd=project, input=prompt(project, task_id), text=True, check=False)
                if result.returncode:
                    print(f"Agent exited with status {result.returncode} for {task_id}", file=sys.stderr, flush=True)
        seen = current


def has_status_filter(args: list[str]) -> bool:
    return any(arg in ("-s", "--status") or arg.startswith("--status=") or (arg.startswith("-s") and len(arg) > 2) for arg in args)


def stop_watch(_signum: int, _frame: object) -> None:
    raise KeyboardInterrupt


@app.command()
def main(
    ctx: typer.Context,
    project: Path = typer.Option(Path.cwd(), help="Project directory (default: current directory)."),
    command: str = typer.Option("codex exec -", help="Agent command; prompt is sent on stdin."),
    yolo: bool = typer.Option(False, help="Run default Codex command without approvals or sandboxing."),
) -> None:
    """Watch Backlog tasks. Pass task-list options after --; see backlog task list --help."""
    project = project.expanduser().resolve()
    if not (project / "backlog" / "config.yml").is_file():
        raise typer.BadParameter("project must contain backlog/config.yml", param_hint="project")
    try:
        agent_command = shlex.split(command)
    except ValueError as error:
        raise typer.BadParameter(str(error), param_hint="--command") from error
    if not agent_command:
        raise typer.BadParameter("command must not be empty", param_hint="--command")
    if yolo:
        if agent_command != ["codex", "exec", "-"]:
            raise typer.BadParameter("--yolo only supports the default command; configure custom commands directly", param_hint="--yolo")
        agent_command.insert(2, "--dangerously-bypass-approvals-and-sandbox")
    args = list(ctx.args)
    if any(arg in ("--json", "--watch", "--plain", "--count", "-h", "--help") for arg in args):
        raise typer.BadParameter("output and help options cannot be passed to the watch; see backlog task list --help")
    env = {**os.environ, "BACKLOG_CWD": str(project)}
    try:
        if not has_status_filter(args):
            result = subprocess.run(["backlog", "config", "get", "statuses"], cwd=project, env=env, text=True, capture_output=True, check=True)
            if "to do" not in {status.strip().casefold() for status in result.stdout.split(",")}:
                raise ValueError('Default status "To Do" is not configured; pass a --status filter after --')
            args = ["--status", "To Do", *args]
        print(f"Watching {project}", flush=True)
        process = subprocess.Popen(["backlog", "task", "list", *args, "--json", "--watch"], cwd=project, env=env, text=True, stdout=subprocess.PIPE)
        previous_handler = signal.signal(signal.SIGTERM, stop_watch)
        try:
            assert process.stdout is not None
            dispatch(process.stdout, project, agent_command)
            code = process.wait()
            if code:
                raise ValueError(f"Backlog watch exited with status {code}")
            raise ValueError("Backlog watch ended unexpectedly")
        finally:
            signal.signal(signal.SIGTERM, previous_handler)
            if process.poll() is None:
                process.terminate()
                process.wait()
            if process.stdout is not None:
                process.stdout.close()
    except KeyboardInterrupt:
        print("Stopped", flush=True)
    except (OSError, subprocess.CalledProcessError, ValueError, KeyError, TypeError) as error:
        print(f"Watch failed: {error}", file=sys.stderr, flush=True)
        raise typer.Exit(code=1) from error


if __name__ == "__main__":
    app()
