import os
import re
from datetime import datetime
from collections import Counter


REPORTS_DIR = "reports"
INTELLIGENCE_DIR = os.path.join(REPORTS_DIR, "intelligence")

PRODUCTS_DIR = os.path.join(INTELLIGENCE_DIR, "products")
ARTISTS_DIR = os.path.join(INTELLIGENCE_DIR, "artists")
COMPETITORS_DIR = os.path.join(INTELLIGENCE_DIR, "competitors")
EXECUTIVE_DIR = os.path.join(INTELLIGENCE_DIR, "executive")
TRENDS_DIR = os.path.join(INTELLIGENCE_DIR, "trends")

TODAY = datetime.now().strftime("%Y-%m-%d")


def ensure_directories():
    """
    Create required intelligence directories if missing.
    """
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
    """
    Read all markdown files from a directory.
    """
    contents = []

    if not os.path.exists(directory):
        return contents

    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(directory, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                contents.append(
                    {
                        "filename": filename,
                        "content": file.read(),
                    }
                )
        except Exception as e:
            print(f"Unable to read {filepath}: {e}")

    return contents


def extract_top_terms(text_blocks, top_n=15):
    """
    Simple trend extraction engine.
    """

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
        "into",
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
        words = re.findall(r"\b[a-zA-Z]{4,}\b", block.lower())

        for word in words:
            if word not in stop_words:
                counter[word] += 1

    return counter.most_common(top_n)


def generate_trend_report(
    product_reports,
    artist_reports,
    competitor_reports
):
    """
    Build intelligence trend report.
    """

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
            report_lines.append(f"- {term}: {count} mentions")
    else:
        report_lines.append("- No significant trends detected")

    trend_report = "\n".join(report_lines)

    filename = f"{TODAY}-trend-report.md"
    filepath = os.path.join(TRENDS_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(trend_report)

    print(f"Trend report written: {filepath}")

    return trends


def summarize_recent_files(reports):
    """
    Return a small list of newest files.
    """

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
    trends
):
    """
    Generate leadership-focused executive summary.
    """

    product_count = len(product_reports)
    artist_count = len(artist_reports)
    competitor_count = len(competitor_reports)

    total_reports = (
        product_count
        + artist_count
        + competitor_count
    )

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

    if trends:
        for term, count in trends[:10]:
            lines.append(
                f"- {term}: {count} mentions across intelligence reports"
            )
    else:
        lines.append("- No trends detected")

    lines.extend([
        "",
        "## Recommended Actions",
        "",
        "- Monitor recurring themes appearing across intelligence reports.",
        "- Investigate frequently mentioned categories and artists.",
        "- Compare trend movement across future report runs.",
        "- Continue building historical intelligence archives.",
        "",
        "---",
        "",
        "Generated by Executive Summary Agent V6",
    ])

    return "\n".join(lines)


def save_executive_summary(summary):
    """
    Save current executive outputs.
    """

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

    product_reports = read_markdown_files(PRODUCTS_DIR)
    artist_reports = read_markdown_files(ARTISTS_DIR)
    competitor_reports = read_markdown_files(COMPETITORS_DIR)

    trends = generate_trend_report(
        product_reports,
        artist_reports,
        competitor_reports,
    )

    executive_summary = build_executive_summary(
        product_reports,
        artist_reports,
        competitor_reports,
        trends,
    )

    save_executive_summary(executive_summary)

    print("Executive Summary Agent V6 completed successfully.")


if __name__ == "__main__":
    main()
