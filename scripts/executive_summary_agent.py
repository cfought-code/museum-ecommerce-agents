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
            print(f"Unable to read {filepath}: {error}")

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
        "summary",
        "executive",

        "product",
        "products",
        "item",
        "items",
        "customer",
        "customers",
        "quality",
        "design",
        "designed",
        "features",
        "feature",

        "museum",
        "store",
        "collection",
        "collections",

        "description",
        "creative",
        "experience",
        "vision",
        "gift",
        "gifts",
        "beautiful",
        "inspired",
        "inspiration",
        "premium",
        "unique",
        "perfect",
        "ideal",
        "thoughtful",
        "crafted",

        "artist",
        "artists",
        "competitor",
        "competitors",

        "available",
        "includes",
        "including",
        "create",
        "creating",
        "offers",
        "offering",
        "showcases",
        "showcase",
        "celebrates",
        "celebrate",
        "featuring",
        "featured",
        "immediate",
        "challenging",
        "technical",
        "skills",
        "fine",
        "work",
        "works",
        "working",
        "career",
        "artwork",
        "artworks",
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

        values = history.get(term, [])

        if isinstance(values, int):
            values = [values]

        values.append(count)

        history[term] = values[-20:]

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

    lines = [
        f"# Trend Report - {TODAY}",
        "",
        "## Emerging Trends",
        ""
    ]

    if trends:

        for term, count in trends:
            lines.append(
                f"- {term}: {count} mentions"
            )

    else:
        lines.append(
            "- No trends detected"
        )

    report = "\n".join(lines)

    root_file = os.path.join(
        REPORTS_DIR,
        "trend-report.md"
    )

    archive_file = os.path.join(
        TRENDS_DIR,
        f"{TODAY}-trend-report.md"
    )

    with open(root_file, "w", encoding="utf-8") as file:
        file.write(report)

    with open(archive_file, "w", encoding="utf-8") as file:
        file.write(report)

    return trends


def generate_momentum_report(momentum_data):

    lines = [
        f"# Momentum Report - {TODAY}",
        ""
    ]

    rising = []
    stable = []
    declining = []

    for trend, data in momentum_data.items():

        entry = (
            f"- {trend} "
            f"({data['change']:+d})"
        )

        if data["status"] == "Rising":
            rising.append(entry)

        elif data["status"] == "Declining":
            declining.append(entry)

        else:
            stable.append(entry)

    lines.append("## Rising Trends")
    lines.extend(rising if rising else ["- None"])
    lines.append("")

    lines.append("## Stable Trends")
    lines.extend(stable if stable else ["- None"])
    lines.append("")

    lines.append("## Declining Trends")
    lines.extend(declining if declining else ["- None"])

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

    return report


def build_executive_summary(
    product_reports,
    artist_reports,
    competitor_reports,
    trends,
    momentum_data
):

    rising = [
        trend for trend, data
        in momentum_data.items()
        if data["status"] == "Rising"
    ]

    stable = [
        trend for trend, data
        in momentum_data.items()
        if data["status"] == "Stable"
    ]

    declining = [
        trend for trend, data
        in momentum_data.items()
        if data["status"] == "Declining"
    ]

    lines = [
        f"# Executive Summary - {TODAY}",
        "",
        "## Repository Health",
        "",
        f"- Product Reports: {len(product_reports)}",
        f"- Artist Reports: {len(artist_reports)}",
        f"- Competitor Reports: {len(competitor_reports)}",
        "",
        "## Top Trends",
        ""
    ]

    for term, count in trends[:10]:
        lines.append(
            f"- {term}: {count} mentions"
        )

    lines.extend([
        "",
        "## Trend Momentum",
        "",
        "### Rising"
    ])

    lines.extend(
        [f"- {x}" for x in rising]
        if rising else ["- None"]
    )

    lines.extend([
        "",
        "### Stable"
    ])

    lines.extend(
        [f"- {x}" for x in stable]
        if stable else ["- None"]
    )

    lines.extend([
        "",
        "### Declining"
    ])

    lines.extend(
        [f"- {x}" for x in declining]
        if declining else ["- None"]
    )

    lines.extend([
        "",
        "## Recommended Actions",
        "",
        "- Monitor rising categories.",
        "- Watch declining categories.",
        "- Continue building historic intelligence.",
        "",
        "---",
        "",
        "Generated by Executive Summary Agent V6.1"
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
        "Executive Summary Agent V6.1 completed."
    )


if __name__ == "__main__":
    main()
