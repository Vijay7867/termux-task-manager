# Offline Task Manager

Keep an offline task list with due dates, overdue labels, completion and reopening.

Built for Android + Termux; also runs on Linux with Python 3.10+. Uses only the Python standard library. No API key, pip package or paid service is needed. Installing Python/Git requires internet; normal tool operation is local.

## Install

```bash
pkg install python git -y
git clone https://github.com/Vijay7867/termux-task-manager.git
cd termux-task-manager
python tasks.py --help
```

If using the delivered ZIP instead, extract it and open this project directory directly.

## Examples

```bash
python tasks.py add "Buy groceries" --due 2026-10-18
python tasks.py list
python tasks.py done 1
python tasks.py list --all
python tasks.py reopen 1
```

## Data and limitations

Default database: `~/.local/share/termux-tasks/tasks.sqlite3`. Use `python tasks.py --db /path/to/file.sqlite3 list` to select another database. Due dates are calendar dates, not times. There are no background notifications, recurring tasks or automatic alarms.

Local data is not encrypted. Keep personal records out of Git. Database tools create their data outside the repository by default. For backups, copy the database after commands have exited; protect exported CSV files yourself. Android shared storage may not enforce Unix file modes.

## Verify

```bash
python -m unittest discover -s tests -v
```

Automated tests run in temporary directories and do not touch real phone data. Cloud Python tests are not a substitute for testing on your Android device.

## Contributing

Open an issue with the command, expected/actual output, Python version and platform; remove personal records. Small PRs should include a relevant test. Current scope is a small local CLI, not a cloud service.

## Licence

No project licence has been selected yet. Public visibility alone does not grant reuse rights; contact the maintainer before redistribution.
