"""Post a Jenkins build summary and pytest results to Telegram."""

from html import escape
import os
from pathlib import Path
from xml.etree import ElementTree

import requests


def pytest_totals(junit_path: Path) -> tuple[int, int, int, int]:
    """Return passed, failed, errors, skipped from a pytest JUnit XML report."""
    if not junit_path.exists():
        return 0, 0, 0, 0

    root = ElementTree.parse(junit_path).getroot()
    suites = [root] if root.tag == "testsuite" else root.findall(".//testsuite")
    tests = sum(int(suite.attrib.get("tests", 0)) for suite in suites)
    failed = sum(int(suite.attrib.get("failures", 0)) for suite in suites)
    errors = sum(int(suite.attrib.get("errors", 0)) for suite in suites)
    skipped = sum(int(suite.attrib.get("skipped", 0)) for suite in suites)
    return max(0, tests - failed - errors - skipped), failed, errors, skipped


def main() -> None:
    passed, failed, errors, skipped = pytest_totals(Path("reports/junit.xml"))
    success = os.environ["TG_BUILD_STATUS"] == "SUCCESS"
    heading = "🟢 PASS 🟢" if success else "🔴 FAIL 🔴"
    report_url = os.environ["TG_REPORT_URL"]
    message = (
        f"<b>{heading}</b>\n\n"
        "<b>YouTube Search Regression</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"∙ Trigger: {escape(os.environ['TG_TRIGGER'])}\n"
        f"∙ Period: {escape(os.environ['TG_PERIOD'])}\n"
        f"∙ Passed: {passed}, Failed: {failed}, Error: {errors}, Skipped: {skipped}\n"
        f"∙ Log #{escape(os.environ['TG_BUILD_NUMBER'])}: 🗒️ Report\n"
        f"{report_url}"
    )
    response = requests.post(
        f"https://api.telegram.org/bot{os.environ['TG_BOT_TOKEN']}/sendMessage",
        data={
            "chat_id": os.environ["TG_CHAT_ID"],
            "text": message,
            "parse_mode": "HTML",
        },
        timeout=15,
    )
    response.raise_for_status()


if __name__ == "__main__":
    main()
