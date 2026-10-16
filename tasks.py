#!/usr/bin/env python3
"""Offline task list with due dates. No background alarms."""
import argparse
import os
import sqlite3
from datetime import date
from pathlib import Path


def due_date(value):
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError:
        raise argparse.ArgumentTypeError('Use a valid YYYY-MM-DD date.')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db', type=Path, default=Path.home()/'.local/share/termux-tasks/tasks.sqlite3')
    sub = p.add_subparsers(dest='cmd', required=True)
    add = sub.add_parser('add')
    add.add_argument('title')
    add.add_argument('--due', type=due_date)
    show = sub.add_parser('list')
    show.add_argument('--all', action='store_true')
    for action in ('done','reopen'):
        sub.add_parser(action).add_argument('id', type=int)
    a = p.parse_args()
    if a.cmd == 'add' and not a.title.strip():
        p.error('Task title cannot be empty.')
    a.db.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with sqlite3.connect(a.db) as c:
        os.chmod(a.db, 0o600)
        c.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY,title TEXT NOT NULL,due TEXT,done INTEGER NOT NULL DEFAULT 0)')
        if a.cmd == 'add':
            row = c.execute('INSERT INTO tasks(title,due) VALUES (?,?)',(a.title.strip(),a.due))
            print(f'Added task #{row.lastrowid}')
        elif a.cmd == 'list':
            query = 'SELECT * FROM tasks' + ('' if a.all else ' WHERE done=0') + ' ORDER BY due IS NULL,due,id'
            for ident,title,due,done in c.execute(query):
                tag = 'done' if done else ('overdue' if due and due < date.today().isoformat() else 'open')
                print(f'{ident}\t[{tag}]\t{due or "no due date"}\t{title!r}')
        else:
            row = c.execute('UPDATE tasks SET done=? WHERE id=?',(int(a.cmd=='done'),a.id))
            if row.rowcount == 0:
                p.error('Task ID does not exist.')
            print(f'Task #{a.id}: {"done" if a.cmd=="done" else "open"}')


if __name__ == '__main__':
    try:
        main()
    except (OSError, sqlite3.Error) as exc:
        raise SystemExit(f'Error: {exc}')
