---
id: TASK-4
title: Prepare for pypi
status: Done
assignee:
  - '@codex'
created_date: '2026-11-10T09:20:00Z'
updated_date: '2026-11-10T09:43:00Z'
labels: []
dependencies: []
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
I've added a pypi api token, I'd like to finalize changes (please investigate the ty type error I'm seeing...), push, set v0.1.0, and make sure we can install / run the tool easily with uv tool.
<!-- SECTION:DESCRIPTION:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Reproduce the type error and review package metadata and release prerequisites.
2. Fix verified issues and document installation with uv tool.
3. Run checks and test the built package, then publish and push the v0.1.0 release if access permits.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Reproduced ty invalid-argument-type: subprocess stdout is IO[str], whereas dispatch accepted TextIO. Changed the line-stream annotations to Iterable[str]; ty 0.0.97 now passes across the project. Included README in package metadata, documented uv tool installation, and ignored build/dist while retaining the existing .env ignore. Version was already 0.1.0. Built sdist and wheel using cached setuptools; four unit tests pass. Installed the wheel offline with uv tool in an isolated temporary tool directory, verified --help and started/stopped a real Backlog watch with a nonmatching filter.
Remaining: publish to PyPI, verify installation from PyPI, commit and push, and create/push v0.1.0 tag. This sandbox cannot resolve PyPI and .git is read-only; no release or push has been performed. Task remains in progress.

Renamed release package to codex-backlog in commit 0c232a8 and pushed main. Rebuilt version 0.1.0, reran four unit tests and ty successfully, and verified uv tool installation from the wheel and codex-backlog --help. Created and pushed v0.1.0 at 0c232a8. PyPI is reachable and the project name returned 404, but uv publish failed because no upload credentials are available in this session. Publishing and verifying installation from PyPI remain outstanding.

Published codex-backlog 0.1.0 wheel and source distribution to PyPI using the configured token. Rebuilt the release, confirmed its source matches tag v0.1.0, reran ty and all four unit tests, and installed codex-backlog==0.1.0 from https://pypi.org/simple in an isolated uv tool directory; codex-backlog --help succeeded.
<!-- SECTION:NOTES:END -->

## Comments

<!-- COMMENTS:BEGIN -->
created: 2026-11-10T09:21:00Z

---

Note that we're going with codex-backlog, and have a remote at github.com/nathan-chappell/codex-backlog

---
<!-- COMMENTS:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Fixed the stdout stream type error, prepared package metadata and uv tool installation documentation, and published codex-backlog 0.1.0 to PyPI. The v0.1.0 tag is pushed. Verified the build, ty, four unit tests, and an isolated uv tool installation and command invocation from PyPI.
<!-- SECTION:FINAL_SUMMARY:END -->
