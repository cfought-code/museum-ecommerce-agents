import os
import re
import json
from datetime import datetime
from collections import Counter

REPORTS_DIR = "reports"

INTELLIGENCE_DIR = os.path.join(REPORTS_DIR, "intelligence")

PRODUCTS_DIR = os.path.join(INTELLIGENCE_DIR, "products")
ARTISTS_DIR = os.path.join(INTELLIGENCE_DIR, "artists")
COMPETITORS_DIR = os.path.join(INTELLIGENCE_DIR, "competitors")
EXECUTIVE_DIR = os.path.join(INTELLIGENCE_DIR, "executive")
TRENDS_DIR = os.path.join(INTELLIGENCE_DIR, "trends")

TREND_HISTORY_FILE = os.path.join(
    TRENDS_DIR,
    "trend-history.json"
)

TODAY = datetime.now().strftime("%Y-%m-%d")


def ensure_directories():
    directories = [
        PRODUCTS_DIR,
        ARTISTS_DIR,
        COMPETITORS_DIR,
        EXECUTIVE_DIR,
        TRENDS_DIR,
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def read_markdown_files(directory):

    contents = []

    if not os.path.exists(directory):
        return contents

    for filename in sorted(os.listdir(directory)):

        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(directory, filename)

        try:
            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                contents.append(
                    {
                        "filename": filename,
                        "content": file.read()
                    }
                )

        except Exception as error:

            print(
                f"Unable to read {filepath}: {error}"
            )

    return contents


def extract_top_terms(text_blocks, top_n=15):

    stop_words = {
        "this",
        "that",
        "with",
        "from",
        "have",
        "been",
        "will",
        "into",
        "their",
        "they",
        "them",
        "the",
        "and",
        "for",
        "are",
        "was",
        "were",
        "your",
        "you",
        "about",
        "than",
        "also",
        "more",
        "most",
        "very",
        "which",
        "when",
        "where",
        "what",
        "while",
        "report",
        "reports",
        "product",
        "products",
        "artist",
        "artists",
        "competitor",
        "competitors",
        "summary",
        "executive",
    }

    counter = Counter()

    for block in text_blocks:

        words = re.findall(
            r"\b[a-zA-Z]{4,}\b",
            block.lower()
        )

        for word in words:

            if word not in stop_words:
                counter[word] += 1

    return counter.most_common(top_n)


def load_trend_history():

    if not os.path.exists(TREND_HISTORY_FILE):
        return {}

    try:

        with open(
            TREND_HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return {}


def save_trend_history(history):

    with open(
        TREND_HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=2
        )


def update_trend_history(trends, history):

    for term, count in trends:

        previous = history.get(term, [])

        if isinstance(previous, int):
            previous = [previous]

        previous.append(count)

        history[term] = previous[-20:]

    return history


def calculate_momentum(history):

    momentum = {}

    for trend, values in history.items():

        if len(values) < 2:

            momentum[trend] = {
                "change": 0,
                "status": "Stable"
            }

            continue

        change = values[-1] - values[-2]

        if change > 1:
            status = "Rising"

        elif change < -1:
            status = "Declining"

        else:
            status = "Stable"

        momentum[trend] = {
            "change": change,
            "status": status
        }

    return momentum


def generate_trend_report(
    product_reports,
    artist_reports,
    competitor_reports
):

    combined_text = []

    for report in product_reports:
        combined_text.append(report["content"])

    for report in artist_reports:
        combined_text.append(report["content"])

    for report in competitor_reports:
        combined_text.append(report["content"])

    trends = extract_top_terms(combined_text)

    report_lines = [
        f"# Trend Report - {TODAY}",
        "",
        "## Emerging Trends",
        "",
    ]

    if trends:

        for term, count in trends:
            report_lines.append(
                f"- {term}: {count} mentions"
            )

    else:

        report_lines.append(
            "- No significant trends detected"
        )

    trend_report = "\n".join(report_lines)

    root_file = os.path.join(
        REPORTS_DIR,
        "trend-report.md"
    )

    archive_file = os.path.join(
        TRENDS_DIR,
        f"{TODAY}-trend-report.md"
    )

    with open(root_file, "w", encoding="utf-8") as file:
        file.write(trend_report)

    with open(archive_file, "w", encoding="utf-8") as file:
        file.write(trend_report)

    print(f"Trend report written: {archive_file}")

    return trends


def generate_momentum_report(momentum_data):

    lines = [
        f"# Momentum Report - {TODAY}",
        "",
    ]

    rising = []
    stable = []
    declining = []

    for trend, data in momentum_data.items():

        line = (
            f"- {trend} "
            f"({data['change']:+d})"
        )

        if data["status"] == "Rising":
            rising.append(line)

        elif data["status"] == "Declining":
            declining.append(line)

        else:
            stable.append(line)

    lines.append("## Rising Trends")
    lines.extend(rising if rising else ["- None"])
    lines.append("")

    lines.append("## Stable Trends")
    lines.extend(stable if stable else ["- None"])
    lines.append("")

    lines.append("## Declining Trends")
    lines.extend(declining if declining else ["- None"])
    lines.append("")

    report = "\n".join(lines)

    root_file = os.path.join(
        REPORTS_DIR,
        "momentum-report.md"
    )

    archive_file = os.path.join(
        TRENDS_DIR,
        f"{TODAY}-momentum-report.md"
    )

    with open(root_file, "w", encoding="utf-8") as file:
        file.write(report)

    with open(archive_file, "w", encoding="utf-8") as file:
        file.write(report)

    print(f"Momentum report written: {archive_file}")

    return report


def summarize_recent_files(reports):

    if not reports:
        return ["No reports available"]

    files = sorted(
        [item["filename"] for item in reports],
        reverse=True
    )

    return files[:5]


def build_executive_summary(
    product_reports,
    artist_reports,
    competitor_reports,
    trends,
    momentum_data
):

    product_count = len(product_reports)
    artist_count = len(artist_reports)
    competitor_count = len(competitor_reports)

    total_reports = (
        product_count
        + artist_count
        + competitor_count
    )

    rising = [
        trend
        for trend, data in momentum_data.items()
        if data["status"] == "Rising"
    ]

    stable = [
        trend
        for trend, data in momentum_data.items()
        if data["status"] == "Stable"
    ]

    declining = [
        trend
        for trend, data in momentum_data.items()
        if data["status"] == "Declining"
    ]

    lines = [
        f"# Executive Summary - {TODAY}",
        "",
        "## Repository Health",
        "",
        f"- Product Reports: {product_count}",
        f"- Artist Reports: {artist_count}",
        f"- Competitor Reports: {competitor_count}",
        f"- Total Intelligence Reports: {total_reports}",
        "",
        "## Recent Intelligence Activity",
        "",
        "### Product Reports",
    ]

    for item in summarize_recent_files(product_reports):
        lines.append(f"- {item}")

    lines.extend([
        "",
        "### Artist Reports",
    ])

    for item in summarize_recent_files(artist_reports):
        lines.append(f"- {item}")

    lines.extend([
        "",
        "### Competitor Reports",
    ])

    for item in summarize_recent_files(competitor_reports):
        lines.append(f"- {item}")

    lines.extend([
        "",
        "## Emerging Trends",
        "",
    ])

    for term, count in trends[:10]:
        lines.append(
            f"- {term}: {count} mentions"
        )

    lines.extend([
        "",
        "## Trend Momentum",
        "",
        "### Rising",
    ])

    lines.extend(
        [f"- {x}" for x in rising]
        if rising else
        ["- None"]
    )

    lines.extend([
        "",
        "### Stable",
    ])

    lines.extend(
        [f"- {x}" for x in stable]
        if stable else
        ["- None"]
    )

    lines.extend([
        "",
        "### Declining",
    ])

    lines.extend(
        [f"- {x}" for x in declining]
        if declining else
        ["- None"]
    )

    lines.extend([
        "",
        "## Recommended Actions",
        "",
        "- Monitor rising trends for merchandising opportunities.",
        "- Investigate declining trends before inventory expansion.",
        "- Compare momentum changes across future runs.",
        "- Continue building historical intelligence archives.",
        "",
        "---",
        "",
        "Generated by Executive Summary Agent V6.1",
    ])

    return "\n".join(lines)


def save_executive_summary(summary):

    root_file = os.path.join(
        REPORTS_DIR,
        "executive-summary.md"
    )

    archive_file = os.path.join(
        EXECUTIVE_DIR,
        f"{TODAY}-executive-summary.md"
    )

    with open(root_file, "w", encoding="utf-8") as file:
        file.write(summary)

    with open(archive_file, "w", encoding="utf-8") as file:
        file.write(summary)

    print(f"Executive summary saved: {root_file}")
    print(f"Executive archive saved: {archive_file}")


def main():

    ensure_directories()

    product_reports = read_markdown_files(
        PRODUCTS_DIR
    )

    artist_reports = read_markdown_files(
        ARTISTS_DIR
    )

    competitor_reports = read_markdown_files(
        COMPETITORS_DIR
    )

    trends = generate_trend_report(
        product_reports,
        artist_reports,
        competitor_reports
    )

    history = load_trend_history()

    history = update_trend_history(
        trends,
        history
    )

    save_trend_history(history)

    momentum_data = calculate_momentum(
        history
    )

    generate_momentum_report(
        momentum_data
    )

    executive_summary = build_executive_summary(
        product_reports,
        artist_reports,
        competitor_reports,
        trends,
        momentum_data
    )

    save_executive_summary(
        executive_summary
    )

    print(
        "Executive Summary Agent V6.1 completed successfully."
    )


if __name__ == "__main__":
    main()
