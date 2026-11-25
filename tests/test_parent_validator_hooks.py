"""Run the Covenant's actual pre-commit config in a linked worktree with controlled siblings."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VALIDATORS = {
    "Validate Repository Structure": "validate-repo-structure.sh",
    "Validate Naming Conventions": "validate-naming.sh",
    "Check for Secrets": "check-secrets.sh",
}


class ParentValidatorHooks(unittest.TestCase):
    def test_missing_passing_and_failing_in_linked_worktree(self):
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            source = temp / "source"
            source.mkdir()
            subprocess.run(["git", "init", "--quiet"], cwd=source, check=True)
            shutil.copyfile(ROOT / ".pre-commit-config.yaml", source / ".pre-commit-config.yaml")
            subprocess.run(["git", "add", ".pre-commit-config.yaml"], cwd=source, check=True)
            subprocess.run([
                "git", "-c", "user.name=Hook Fixture", "-c", "user.email=fixture@example.invalid",
                "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null",
                "commit", "--quiet", "-m", "test: seed the isolated hook fixture",
            ], cwd=source, check=True)
            outside = temp / "outside"
            outside.mkdir()
            worktree = outside / "checkout"
            subprocess.run(["git", "worktree", "add", "--quiet", "--detach", str(worktree), "HEAD"],
                           cwd=source, check=True)
            self.assertTrue((worktree / ".git").is_file())

            log = temp / "calls"
            tools = outside / ".org" / "tooling" / "validators"
            for case, exit_code in (("missing", 1), ("passing", 0), ("failing", 1)):
                with self.subTest(case=case):
                    if case == "passing":
                        tools.mkdir(parents=True)
                        for script in VALIDATORS.values():
                            path = tools / script
                            path.write_text(
                                '#!/bin/sh\n'
                                'printf "%s %s %s\\n" "${0##*/}" "$#" "$1" >> "$FIXTURE_LOG"\n'
                                'exit "$FIXTURE_STATUS"\n',
                                encoding="utf-8",
                            )
                            path.chmod(0o755)
                    log.write_text("", encoding="utf-8")
                    result = subprocess.run(
                        ["pre-commit", "run", "--all-files", "--color", "never"], cwd=worktree,
                        env=dict(os.environ, FIXTURE_LOG=str(log), FIXTURE_STATUS="27" if case == "failing" else "0"),
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                    )
                    self.assertEqual(result.returncode, exit_code, result.stdout)
                    status = "Passed" if case == "passing" else "Failed"
                    for hook, script in VALIDATORS.items():
                        self.assertRegex(result.stdout, rf"(?m)^{hook}\.+{status}$")
                        if case == "missing":
                            self.assertIn(script, result.stdout)
                    if case == "failing":
                        self.assertEqual(result.stdout.count("exit code: 27"), 3, result.stdout)
                    calls = log.read_text(encoding="utf-8").splitlines()
                    expected = [] if case == "missing" else [f"{script} 1 ." for script in VALIDATORS.values()]
                    self.assertCountEqual(calls, expected)
                    print(f"{case}: three hooks {status}, pre-commit exit {result.returncode}")


if __name__ == "__main__":
    unittest.main()
