import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
SCRIPT=Path(__file__).resolve().parents[1]/"tasks.py"
class Tasks(unittest.TestCase):
    def test_lifecycle_and_validation(self):
        with tempfile.TemporaryDirectory() as folder:
            def run(*args):
                return subprocess.run([sys.executable,str(SCRIPT),"--db",str(Path(folder)/"tasks.sqlite3"),*args],capture_output=True,text=True)
            self.assertEqual(run("add","Buy milk","--due","2000-01-01").returncode,0)
            self.assertIn("overdue",run("list").stdout)
            self.assertEqual(run("done","1").returncode,0)
            self.assertNotIn("Buy milk",run("list").stdout)
            self.assertIn("done",run("list","--all").stdout)
            self.assertEqual(run("reopen","1").returncode,0)
            self.assertIn("Buy milk",run("list").stdout)
            self.assertNotEqual(run("done","999").returncode,0)
            self.assertNotEqual(run("add"," ").returncode,0)
            self.assertNotEqual(run("add","bad date","--due","2026-02-30").returncode,0)
