"""Run the bundled Persian lesson and give feedback on one answer."""

import argparse
import json
import sys
from pathlib import Path


LESSON = Path(__file__).with_name("lesson.json")
PERSIAN_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
INPUT_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")


def choice_number(answer, count):
    normalized = answer.strip().translate(INPUT_DIGITS)
    for number in range(1, count + 1):
        if normalized == str(number):
            return number
    return None


def main():
    parser = argparse.ArgumentParser(description="یک درس کوتاه فارسی با تمرین و بازخورد")
    parser.add_argument("--answer", metavar="N", help="شمارهٔ گزینه برای اجرای بدون توقف")
    args = parser.parse_args()

    lesson = json.loads(LESSON.read_text(encoding="utf-8"))
    print(lesson["title"], lesson["lesson"], lesson["question"], sep="\n\n")
    options = lesson["options"]
    for number, option in enumerate(options, start=1):
        label = str(number).translate(PERSIAN_DIGITS)
        print(f"{label}) {option['text']}")

    answer = args.answer
    while True:
        if answer is None:
            try:
                answer = input("شمارهٔ گزینه را وارد کنید: ")
            except EOFError:
                print("پاسخی دریافت نشد.", file=sys.stderr)
                return 2
        number = choice_number(answer, len(options))
        if number is not None:
            break
        print("شمارهٔ یکی از گزینه‌های بالا را وارد کنید.", file=sys.stderr)
        if args.answer is not None:
            return 2
        answer = None

    correct = lesson["correct_option"]
    if number == correct:
        print("پاسخ درست است.")
    else:
        print(options[number - 1]["hint"])
        print(f"پاسخ درست: {options[correct - 1]['text']}")
    print(lesson["explanation"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
