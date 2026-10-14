import os
from datetime import datetime

from data.executive_themes import EXECUTIVE_THEMES

# ==========================================
# INPUTS
# ==========================================

reporting_period = os.environ.get(
    "REPORTING_PERIOD",
    ""
)

# ==========================================
# HELPERS
# ==========================================

def get_report_contents(folder):

    contents = []

    if not os.path.exists(folder):
        return contents

    for root, _, files in os.walk(folder):

        for filename in files:

            if filename.endswith(".md"):

                filepath = os.path.join(
                    root,
                    filename
                )

                try:

                    with open(
                        filepath,
                        "r",
                        encoding="utf-8"
                    ) as file:

                        contents.append(
                            file.read()
                        )

                except Exception:
                    pass

    return contents


# ==========================================
# LOAD ARCHIVED INTELLIGENCE
# ==========================================

product_reports = get_report_contents(
    "reports/intelligence/products"
)

artist_reports = get_report_contents(
    "reports/intelligence/artists"
)

market_reports = get_report_contents(
    "reports/intelligence/market"
)

# ==========================================
# THEME DETECTION
# ==========================================

all_content = (
    "\n".join(product_reports)
    + "\n"
    + "\n".join(artist_reports)
    + "\n"
    + "\n".join(market_reports)
).lower()

theme_counts = {}

for theme, keywords in EXECUTIVE_THEMES.items():

    count = 0

    for keyword in keywords:

        count += all_content.count(
            keyword.lower()
        )

    theme_counts[theme] = count

sorted_themes = sorted(
    theme_counts.items(),
    key=lambda item: item[1],
    reverse=True
)

# ==========================================
# TOP THEMES
# ==========================================

top_themes = []

for theme, count in sorted_themes:

    if count > 0:

        top_themes.append(
            f"- {theme} ({count} references)"
        )

# ==========================================
# PRIORITY THEMES
# ==========================================

priority_themes = []

for theme, count in sorted_themes:

    if count > 0:

        priority_themes.append(
            {
                "theme": theme,
                "count": count
            }
        )

top_five = priority_themes[:5]

# ==========================================
# SCORES
# ==========================================

opportunity_score = sum(
    theme_counts.values()
)

activity_score = (
    len(product_reports)
    + len(artist_reports)
    + len(market_reports)
)

intelligence_rating = "Emerging"

if activity_score >= 5:
    intelligence_rating = "Developing"

if activity_score >= 10:
    intelligence_rating = "Advanced"

if activity_score >= 20:
    intelligence_rating = "Strategic"

# ==========================================
# REPOSITORY HEALTH
# ==========================================

agent_count = 7
workflow_count = 7
intelligence_library_count = 4

repository_health_score = (
    agent_count
    + workflow_count
    + intelligence_library_count
)

repository_maturity = "Emerging"

if repository_health_score >= 10:
    repository_maturity = "Developing"

if repository_health_score >= 15:
    repository_maturity = "Advanced"

if repository_health_score >= 20:
    repository_maturity = "Strategic"

# ==========================================
# RECOMMENDATIONS
# ==========================================

recommendations = []

if theme_counts.get(
    "Glass Art",
    0
) > 0:

    recommendations.append(
        "Continue expanding Studio Glass and glass-focused merchandising."
    )

if theme_counts.get(
    "Artist Storytelling",
    0
) > 0:

    recommendations.append(
        "Increase artist-focused content across product and collection pages."
    )

if theme_counts.get(
    "Designer Jewelry",
    0
) > 0:

    recommendations.append(
        "Promote wearable art and designer jewelry in gifting campaigns."
    )

if theme_counts.get(
    "Holiday Opportunities",
    0
) > 0:

    recommendations.append(
        "Review seasonal merchandising and holiday gift opportunities."
    )

if theme_counts.get(
    "Competitor Intelligence",
    0
) > 0:

    recommendations.append(
        "Evaluate competitor trends for new product opportunities."
    )

if theme_counts.get(
    "Collection Development",
    0
) > 0:

    recommendations.append(
        "Review assortment strategy and collection placement opportunities."
    )

if theme_counts.get(
    "Museum Exclusives",
    0
) > 0:

    recommendations.append(
        "Consider additional promotion of Museum Exclusive merchandise."
    )

if theme_counts.get(
    "Exhibitions",
    0
) > 0:

    recommendations.append(
        "Develop exhibition-related merchandising opportunities."
    )

if not recommendations:

    recommendations.append(
        "Continue generating reports to expand intelligence coverage."
    )

# ==========================================
# BUSINESS AREA COVERAGE
# ==========================================

business_areas = {

    "Merchandising": (
        theme_counts.get(
            "Collection Development",
            0
        )
        +
        theme_counts.get(
            "Glass Art",
            0
        )
        +
        theme_counts.get(
            "Designer Jewelry",
            0
        )
    ),

    "Content": (
        theme_counts.get(
            "Artist Storytelling",
            0
        )
    ),

    "Competitive Intelligence": (
        theme_counts.get(
            "Competitor Intelligence",
            0
        )
    ),

    "Seasonal Planning": (
        theme_counts.get(
            "Holiday Opportunities",
            0
        )
    )
}

# ==========================================
# BUILD REPORT
# ==========================================

lines = []

lines.append("# Museum Store Intelligence Brief")
lines.append("")
lines.append(f"Generated: {datetime.now()}")
lines.append("")
lines.append(f"Reporting Period: {reporting_period}")
lines.append("")
lines.append("---")
lines.append("")
lines.append("# Executive Summary")
lines.append("")
lines.append(
    "This briefing summarizes themes, opportunities, strategic recommendations, and repository health across the Museum Ecommerce Agents platform."
)

lines.append("")
lines.append("---")
lines.append("")
lines.append("# Reports Reviewed")
lines.append("")
lines.append(f"Product Reports: {len(product_reports)}")
lines.append(f"Artist Reports: {len(artist_reports)}")
lines.append(f"Market Reports: {len(market_reports)}")

lines.append("")
lines.append("---")
lines.append("")
lines.append("# Executive Dashboard")
lines.append("")
lines.append(f"Repository Activity Score: {activity_score}")
lines.append(f"Intelligence Rating: {intelligence_rating}")
lines.append(f"Opportunity Score: {opportunity_score}")

lines.append("")
lines.append("---")
lines.append("")
lines.append("# Repository Health")
lines.append("")
lines.append(f"Agents Implemented: {agent_count}")
lines.append(f"Workflows Implemented: {workflow_count}")
lines.append(f"Intelligence Libraries: {intelligence_library_count}")
lines.append(f"Repository Health Score: {repository_health_score}")
lines.append(f"Repository Maturity: {repository_maturity}")

lines.append("")
lines.append("---")
lines.append("")
lines.append("# Top Themes")
lines.append("")

if top_themes:
    lines.extend(top_themes)
else:
    lines.append("No recurring themes identified.")

lines.append("")
lines.append("---")
lines.append("")
lines.append("# Strategic Priorities")
lines.append("")

for index, item in enumerate(
    top_five,
    start=1
):
    lines.append(
        f"{index}. "
        f"{item['theme']} "
        f"({item['count']} references)"
    )

lines.append("")
lines.append("---")
lines.append("")
lines.append("# Strategic Recommendations")
lines.append("")

for index, item in enumerate(
    recommendations,
    start=1
):
    lines.append(
        f"{index}. {item}"
    )

lines.append("")
lines.append("---")
lines.append("")
lines.append("# Business Area Coverage")
lines.append("")

for area, score in business_areas.items():

    lines.append(
        f"- {area}: {score} references"
    )

lines.append("")
lines.append("---")
lines.append("")
lines.append("# Intelligence Repository")
lines.append("")
lines.append(
    "Historical intelligence is sourced from archived reports located under reports/intelligence/."
)

lines.append("")
lines.append("---")
lines.append("")
lines.append("# Competitor Monitoring")
lines.append("")
lines.append("- Corning Museum of Glass")
lines.append("- MCA Chicago Store")
lines.append("- Museum of Glass Store")
lines.append("- Artful Home")

lines.append("")
lines.append("---")
lines.append("")
lines.append("# Leadership Summary")
lines.append("")
lines.append(
    "The Museum Ecommerce Agents platform is actively generating merchandising, artist, and market intelligence."
)
lines.append(
    "Continued report generation will improve trend detection and recommendation quality over time."
)

report = "\n".join(lines)

# ==========================================
# OUTPUT FILES
# ==========================================

timestamp = datetime.now().strftime(
    "%Y-%m-%d"
)

output_file = (
    "reports/executive/executive-summary.md"
)

archive_file = (
    f"reports/intelligence/executive/"
    f"{timestamp}-executive-summary.md"
)

# ==========================================
# SAVE CURRENT REPORT
# ==========================================

os.makedirs(
    "reports/executive",
    exist_ok=True
)

with open(
    output_file,
    "w",
    encoding="utf-8"
) as file:

    file.write(report)

# ==========================================
# SAVE ARCHIVE REPORT
# ==========================================

os.makedirs(
    "reports/intelligence/executive",
    exist_ok=True
)

with open(
    archive_file,
    "w",
    encoding="utf-8"
) as file:

    file.write(report)

# ==========================================
# LOGGING
# ==========================================

print(
    f"Current report created: {output_file}"
)

print(
    f"Archive report created: {archive_file}"
)
