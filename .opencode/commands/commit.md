---
description: Review the diff, stage changes, and commit with a message
---

Review the current diff for correctness, regressions, and unintended changes before committing. Inspect `git status`, `git diff`, and any untracked files. Then update the branch with `git pull --rebase origin main`, stage the project changes with `git add`, and commit them with `git commit -m` using this message:

$ARGUMENTS

Keep the commit limited to the changes you reviewed. If the rebase fails or reports conflicts, stop and report the problem instead of forcing the commit.
