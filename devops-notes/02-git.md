# Git

## The repo

Remote is on GitHub: https://github.com/ali-devopsx/Microservices_Secure_Deployment_Pipeline.git

## Branches

I'm just using `main` for now. No fancy branch strategy or anything. I know I should probably use feature branches and PRs but honestly for a learning project this works fine.

## .gitignore

I'm ignoring the usual stuff - `db.sqlite3`, `__pycache__`, virtual environments, `.env` files, `secret_grafana.txt`, log files, media, backups, and some old compose files I don't need anymore.

## My usual workflow

Pretty simple - edit files, `git add`, `git commit`, `git push`. Sometimes I check `git status` or `git log --oneline -10` to see what's going on.

If I mess up a commit I do `git reset --soft HEAD~1` to undo it but keep the changes. For force pushing after messing with history I use `--force-with-lease` instead of just `--force`.

## Commit messages

Yeah they're not great. Some use `fix:` or `feat:` prefixes which is good, but others are just random stuff like `test`. I'm working on being more consistent with that.

## Stuff I need to fix

I'm pushing directly to `main` which isn't ideal. Also there's an `app/blog/` folder that I think should be committed but I keep forgetting to check it.
