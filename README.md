# codex-backlog

A foreground watcher for an existing [Backlog.md](https://backlog.md/) project. It uses `backlog task list --json --watch` and starts an agent for each task entering the filtered list. By default it watches tasks with status `To Do`; this status must be configured in the project.

## Installation

Install [Backlog.md](https://backlog.md/) and the CLI for your agent (Codex by default), and make both commands available on your PATH. You'll also need Python 3.11 or later and [uv](https://docs.astral.sh/uv/).

Install from PyPI:

```sh
uv tool install codex-backlog
```

Or install from a local checkout:

```sh
uv tool install /path/to/codex-backlog
```

## Quick start

In an existing Backlog.md project containing `backlog/config.yml`, start the watcher:

```sh
cd /path/to/project
codex-backlog
```

The watcher runs in the foreground and starts Codex for matching `To Do` tasks. Press Ctrl+C to stop it. See [Backlog.md](https://backlog.md/) for creating and managing a project.

## Options and filters

For example:

```sh
codex-backlog
codex-backlog --yolo
codex-backlog --project /path/to/project --command 'codex exec -'
codex-backlog -- --status 'In Progress' --assignee @agent
codex-backlog -- --search @agent
```

`--yolo` runs the default Codex command with `--dangerously-bypass-approvals-and-sandbox`, skipping approval prompts and sandboxing for agent commands. Use it only in an appropriately isolated environment. For a custom `--command`, configure its permissions directly; `--yolo` cannot be combined with a different command.

Arguments after `--` are passed to `backlog task list`. See `backlog task list --help` for available filters. The default status is applied alongside other filters unless an explicit `--status` (or `-s`) is supplied. For mention-like filtering, `--search @agent` uses Backlog's own search semantics, which also include metadata. Output-format and help options cannot be passed through because the watcher requires JSON snapshots.

The first snapshot runs every matching task. Subsequent snapshots run tasks newly entering the list; edits to a task that remains in the list do not trigger another run. A task that leaves and later re-enters can run again. Runs are sequential, and Backlog may coalesce intermediate changes. State is in memory, so restarting runs matching tasks again. The agent receives task guidance on stdin and runs in the project directory. There is no durable queue, automatic retry, or session continuity; agent failures are reported on the console.
