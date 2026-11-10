---
id: TASK-3
title: Yolo
status: Done
assignee:
  - '@codex'
created_date: '2026-11-10T08:21:00Z'
updated_date: '2026-11-10T08:22:00Z'
labels: []
dependencies: []
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Please give me some YOLO flag or something...
<!-- SECTION:DESCRIPTION:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add an opt-in --yolo shortcut for the default Codex command, keeping custom agent commands explicit.
2. Document its effect and verify default, opt-in, and custom-command behavior.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Added --yolo for the default Codex invocation using --dangerously-bypass-approvals-and-sandbox. Custom commands must configure their own permissions; combining --yolo with a different command produces an error. Documented the behavior and isolation requirement. Verified CLI help and all 4 unittest cases, including default, opt-in, custom command, and incompatible combination.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added an opt-in --yolo shortcut that runs the default Codex command without approval prompts or sandboxing. Custom commands configure their own permissions. Documented usage and verified CLI help and all four unit tests.
<!-- SECTION:FINAL_SUMMARY:END -->
