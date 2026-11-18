"""Exercise the command in a clean working directory using its public inputs."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "tutor.py"


def run_lesson(*args, keyboard=""):
    with tempfile.TemporaryDirectory() as working_directory:
        return subprocess.run(
            [sys.executable, "-I", "-S", str(SCRIPT), *args],
            input=keyboard,
            encoding="utf-8",
            capture_output=True,
            cwd=working_directory,
            timeout=5,
        )


class TutorTests(unittest.TestCase):
    def test_correct_answer_with_three_digit_sets(self):
        for answer in ["2", " ۲ ", "٢"]:
            with self.subTest(answer=answer):
                result = run_lesson("--answer", answer)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("پیدا کردن میانه", result.stdout)
                self.assertIn("میانه چند دقیقه است؟", result.stdout)
                self.assertIn("۲) ۶ دقیقه", result.stdout)
                self.assertIn("پاسخ درست است.", result.stdout)
                self.assertIn("عدد سوم ۶ است", result.stdout)

    def test_each_distractor_gives_its_own_feedback_and_solution(self):
        for answer, clue in [("۱", "فهرست اولیه"), ("۳", "بیشترین زمان")]:
            with self.subTest(answer=answer):
                result = run_lesson("--answer", answer)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(clue, result.stdout)
                self.assertIn("پاسخ درست: ۶ دقیقه", result.stdout)
                self.assertNotIn("پاسخ درست است.", result.stdout)

    def test_invalid_argument_is_reported_without_entering_interactive_mode(self):
        result = run_lesson("--answer", "۴", keyboard="۲\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn("شمارهٔ یکی از گزینه‌های بالا", result.stderr)
        self.assertNotIn("پاسخ درست است.", result.stdout)

    def test_interactive_retry(self):
        result = run_lesson(keyboard="x\n۲\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("شمارهٔ یکی از گزینه‌های بالا", result.stderr)
        self.assertIn("پاسخ درست است.", result.stdout)

    def test_end_of_input_before_answer(self):
        result = run_lesson()
        self.assertEqual(result.returncode, 2)
        self.assertIn("پاسخی دریافت نشد.", result.stderr)


if __name__ == "__main__":
    unittest.main()
