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
# LOAD REPORTS
# ==========================================

product_reports = get_report_contents(
    "reports/products"
)

artist_reports = get_report_contents(
    "reports/artists"
)

market_reports = get_report_contents(
    "reports/market"
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

if theme_counts.get("Glass Art", 0) > 0:
    recommendations.append(
        "Continue expanding Studio Glass and glass-focused merchandising."
    )

if theme_counts.get("Artist Storytelling", 0) > 0:
    recommendations.append(
        "Increase artist-focused content across product and collection pages."
    )

if theme_counts.get("Designer Jewelry", 0) > 0:
    recommendations.append(
        "Promote wearable art and designer jewelry in gifting campaigns."
    )

if theme_counts.get("Holiday Opportunities", 0) > 0:
    recommendations.append(
        "Review seasonal merchandising and holiday gift opportunities."
    )

if theme_counts.get("Competitor Intelligence", 0) > 0:
    recommendations.append(
        "Evaluate competitor trends for new product and merchandising opportunities."
    )

if theme_counts.get("Collection Development", 0) > 0:
    recommendations.append(
        "Review assortment strategy and collection placement opportunities."
    )

if theme_counts.get("Museum Exclusives", 0) > 0:
    recommendations.append(
        "Consider additional promotion of Museum Exclusive merchandise."
    )

if theme_counts.get("Exhibitions", 0) > 0:
    recommendations.append(
        "Develop exhibition-related merchandising and storytelling opportunities."
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

report_lines = []

report_lines.append("# Museum Store Intelligence Brief")
report_lines.append("")
report_lines.append(f"Generated: {datetime.now()}")
report_lines.append("")
report_lines.append(f"Reporting Period: {reporting_period}")
report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("# Executive Summary")
report_lines.append("")
report_lines.append(
    "This briefing summarizes themes, opportunities, strategic recommendations, and repository health across the Museum Ecommerce Agents platform."
)

report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("# Reports Reviewed")
report_lines.append("")
report_lines.append(f"Product Reports: {len(product_reports)}")
report_lines.append(f"Artist Reports: {len(artist_reports)}")
report_lines.append(f"Market Reports: {len(market_reports)}")

report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("# Executive Dashboard")
report_lines.append("")
report_lines.append(f"Repository Activity Score: {activity_score}")
report_lines.append(f"Intelligence Rating: {intelligence_rating}")
report_lines.append(f"Opportunity Score: {opportunity_score}")

report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("# Repository Health")
report_lines.append("")
report_lines.append(f"Agents Implemented: {agent_count}")
report_lines.append(f"Workflows Implemented: {workflow_count}")
report_lines.append(f"Intelligence Libraries: {intelligence_library_count}")
report_lines.append(f"Repository Health Score: {repository_health_score}")
report_lines.append(f"Repository Maturity: {repository_maturity}")

report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("# Top Themes")
report_lines.append("")

if top_themes:
    report_lines.extend(top_themes)
else:
    report_lines.append("No recurring themes identified.")

report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("# Strategic Priorities")
report_lines.append("")

for idx, item in enumerate(top_five, start=1):
    report_lines.append(
        f"{idx}. {item['theme']} ({item['count']} references)"
    )

report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("# Strategic Recommendations")
report_lines.append("")

for idx, recommendation in enumerate(
    recommendations,
    start=1
):
    report_lines.append(
        f"{idx}. {recommendation}"
    )

report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("# Business Area Coverage")
report_lines.append("")

for area, score in business_areas.items():
    report_lines.append(
        f"- {area}: {score} references"
    )

report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("# Intelligence Repository")
report_lines.append("")
report_lines.append(
    "Future intelligence is archived under reports/intelligence/"
)

report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("# Competitor Monitoring")
report_lines.append("")
report_lines.append("- Corning Museum of Glass")
report_lines.append("- MCA Chicago Store")
report_lines.append("- Museum of Glass Store")
report_lines.append("- Artful Home")

report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("# Leadership Summary")
report_lines.append("")
report_lines.append(
    "The Museum Ecommerce Agents platform is actively generating merchandising, artist, and market intelligence."
)

report_lines.append(
    "Continued report generation will improve trend detection, category analysis, and recommendation quality over time."
)

# ==========================================
# SAVE REPORT
# ==========================================

report = "\n".join(report_lines)

os.makedirs(
    "reports/executive",
    exist_ok=True
)

output_file = (
    "reports/executive/executive-summary.md"
)

with open(
    output_file,
    "w",
    encoding="utf-8"
) as file:

    file.write(report)

print(
    f"Executive summary created: {output_file}"
)
