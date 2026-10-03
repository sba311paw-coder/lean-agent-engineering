# Push lean-agent-architecture to GitHub

[← README](README.md)

For a new repository, run the commands below one at a time, stopping if one fails. Review the staged files before committing. Git and GitHub CLI are available on the preparation machine; GitHub authentication and Git identity have not been verified. These commands create a private repository under the signed-in account. To target an organization, use `ORG/lean-agent-architecture` in `gh repo create`.

```sh
gh auth status
# If not signed in: gh auth login
cd "/Users/satishagadkar/Documents/Codex/2026-10-03/referenced-chatgpt-conversation-this-is-an/outputs/separate-repositories/lean-agent-architecture"
git init -b main
git add .
git diff --cached --check
git diff --cached --stat
git commit -m "Add initial lean-agent-architecture documentation"
gh repo create lean-agent-architecture --private --source=. --remote=origin --push
```

If this folder has been moved, replace the `cd` path with its new location. If the named GitHub repository already exists, do not use the creation command: confirm its actual remote and use `git remote add origin ACTUAL_REMOTE_URL` followed by `git push -u origin main` for a new local repository. Never force-push to repair unexpected history. Existing local repositories retain their established branch and remote conventions.

After success, run `gh repo view --web` or `gh repo view --json url --jq .url` to inspect the repository. Verify visibility, README/diagram rendering, and the latest commit. This preparation step has not initialized, committed, created, or pushed any repository.
