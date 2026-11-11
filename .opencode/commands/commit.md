---
description: Review the diff, stage changes, and commit with a message
---

<<<<<<< HEAD
Review the current diff for correctness, regressions, and unintended changes before committing. Inspect `git status`, `git diff`, and any untracked files. Then update the branch with `git pull --rebase origin main`, stage the project changes with `git add`, and commit them with `git commit -m` using this message:

$ARGUMENTS

Keep the commit limited to the changes you reviewed. If the rebase fails or reports conflicts, stop and report the problem instead of forcing the commit.
=======
Review the current diff for correctness, regressions, and unintended changes before committing. Inspect `git status`, `git diff`, and any untracked files. Then stage the project changes with `git add` and commit them with `git commit -m` using this message:

$ARGUMENTS

Keep the commit limited to the changes you reviewed.
>>>>>>> a872c0b3a17ec65f7a0c74a66c3a933d523b5313
