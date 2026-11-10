---
id: TASK-5
title: Rename backlog_agent to codex_backlog
status: Done
assignee:
  - '@codex'
created_date: '2026-11-10T09:40:00Z'
updated_date: '2026-11-10T09:41:00Z'
labels: []
dependencies: []
ordinal: 5000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
That's it, that's the new name of the repo and tool etc.  After renaming and pushing, please continue with the pypi task.
<!-- SECTION:DESCRIPTION:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Rename the Python module, distribution, executable, tests, documentation, and lockfile to codex-backlog.
2. Verify tests, type checking, and an isolated installation.
3. Record completion, commit and push the rename, then resume TASK-4 release work.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Renamed the distribution and executable to codex-backlog and the Python module to codex_backlog; updated tests, README, and lockfile. Four unit tests and ty check pass. Built sdist and wheel and installed the wheel with uv tool in an isolated directory; codex-backlog --help works. The configured origin already uses github.com/nathan-chappell/codex-backlog.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Renamed the tool, Python module, package metadata, documentation, and tests to codex-backlog/codex_backlog. Verified four unit tests, ty, package builds, and an isolated uv tool installation and help invocation. Origin already uses the new repository name.
<!-- SECTION:FINAL_SUMMARY:END -->
