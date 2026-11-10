import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from typer.testing import CliRunner

from backlog_agent import app, dispatch, snapshots


def snapshot(*ids):
    return json.dumps({"schemaVersion": 1, "kind": "task-list", "tasks": [{"id": task_id} for task_id in ids]}, indent=2) + "\n"


class WatchTests(unittest.TestCase):
    def test_yolo_changes_only_the_default_agent_command(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder)
            (project / "backlog").mkdir()
            (project / "backlog" / "config.yml").touch()
            runner = CliRunner()
            for options, expected in [
                ([], ["codex", "exec", "-"]),
                (["--yolo"], ["codex", "exec", "--dangerously-bypass-approvals-and-sandbox", "-"]),
                (["--command", "other-agent --run"], ["other-agent", "--run"]),
            ]:
                with self.subTest(options=options):
                    process = SimpleNamespace(stdout=io.StringIO(snapshot()), wait=lambda: 0, poll=lambda: 0)
                    with patch("backlog_agent.subprocess.run", return_value=SimpleNamespace(stdout="To Do, Done")), patch("backlog_agent.subprocess.Popen", return_value=process), patch("backlog_agent.dispatch") as dispatch_mock:
                        runner.invoke(app, ["--project", str(project), *options])
                    self.assertEqual(dispatch_mock.call_args.args[2], expected)
            result = runner.invoke(app, ["--project", str(project), "--yolo", "--command", "other-agent"])
            self.assertNotEqual(result.exit_code, 0)
            self.assertIn("only supports the default command", result.output)

    def test_snapshots_dispatch_only_when_tasks_enter(self):
        stream = io.StringIO(snapshot("TASK-1") + snapshot("TASK-1", "TASK-2") + snapshot("TASK-2") + snapshot("TASK-1", "TASK-2"))
        with patch("backlog_agent.subprocess.run", return_value=SimpleNamespace(returncode=0)) as run:
            dispatch(stream, Path("/project"), ["agent"])
        self.assertEqual(run.call_count, 3)
        self.assertIn("TASK-1", run.call_args_list[0].kwargs["input"])
        self.assertIn("TASK-2", run.call_args_list[1].kwargs["input"])
        self.assertIn("TASK-1", run.call_args_list[2].kwargs["input"])

    def test_bad_and_incomplete_snapshots_fail(self):
        for text in ('{"kind":"bad","schemaVersion":1,"tasks":[]}\n', '{"kind":'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                list(snapshots(io.StringIO(text)))

    def test_default_status_validation_and_passthrough(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder)
            (project / "backlog").mkdir()
            (project / "backlog" / "config.yml").touch()
            runner = CliRunner()
            with patch("backlog_agent.subprocess.run", return_value=SimpleNamespace(stdout="Open, Done\n")), patch("backlog_agent.subprocess.Popen") as popen:
                result = runner.invoke(app, ["--project", str(project)])
                self.assertEqual(result.exit_code, 1)
                self.assertIn('Default status "To Do" is not configured', result.output)
                popen.assert_not_called()
            process = SimpleNamespace(stdout=io.StringIO(snapshot()), wait=lambda: 1, poll=lambda: 1)
            with patch("backlog_agent.subprocess.run", return_value=SimpleNamespace(stdout="To Do, Done\n")), patch("backlog_agent.subprocess.Popen", return_value=process) as popen:
                result = runner.invoke(app, ["--project", str(project), "--", "--search", "@agent"])
                self.assertEqual(result.exit_code, 1)
                self.assertEqual(popen.call_args.args[0], ["backlog", "task", "list", "--status", "To Do", "--search", "@agent", "--json", "--watch"])
            process.stdout = io.StringIO(snapshot())
            with patch("backlog_agent.subprocess.run") as config, patch("backlog_agent.subprocess.Popen", return_value=process) as popen:
                runner.invoke(app, ["--project", str(project), "--", "--status", "Open"])
                config.assert_not_called()
                self.assertIn("Open", popen.call_args.args[0])
                self.assertNotIn("To Do", popen.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
