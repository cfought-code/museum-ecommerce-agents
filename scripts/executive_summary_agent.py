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
    key=lambda x: x[1],
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
# OPPORTUNITY SCORE
# ==========================================

opportunity_score = sum(
    theme_counts.values()
)

# ==========================================
# ACTIVITY SCORING
# ==========================================

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
        "Evaluate competitor trends for new product and merchandising opportunities."
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
# REPORT
# ==========================================

report = f"""# Museum Store Intelligence Brief

Generated:
{datetime.now()}

Reporting Period:
{reporting_period}

---

# Executive Summary

This briefing summarizes themes, opportunities, and strategic recommendations identified across the Museum Ecommerce Agents platform.

---

# Reports Reviewed

Product Reports: {len(product_reports)}

Artist Reports: {len(artist_reports)}

Market Reports: {len(market_reports)}

---

# Executive Dashboard

## Repository Activity Score

{activity_score}

## Intelligence Rating

{intelligence_rating}

## Opportunity Score

{opportunity_score}

---

# Top Themes

"""

if top_themes:

    report += "\n".join(
        top_themes
    )

else:

    report += (
        "\nNo recurring themes identified."
    )

report += """

---

# Strategic Priorities

"""

for index, item in enumerate(
    top_five,
    start=1
):

    report += (
        f"\n{index}. "
        f"{item['theme']} "
        f"({item['count']} references)"
    )

report += """

---

# Strategic Recommendations

"""

for index, recommendation in enumerate(
    recommendations,
    start=1
):

    report += (
        f"\n{index}. "
        f"{recommendation}"
    )

report += """

---

# Business Area Coverage

"""

for area, score in business_areas.items():

    report += (
        f"\n- {area}: "
        f"{score} references"
    )

report += """

---

# Competitor Monitoring

- Corning Museum of Glass
- MCA Chicago Store
- Museum of Glass Store
- Artful Home

---

# Future Focus Areas

- Artist Storytelling
- Collection Development
- Product Content Quality
- SEO & AEO Readiness
- Museum Retail Trends

---

# Leadership Summary

The Museum Ecommerce Agents platform is actively generating merchandising, artist, and market intelligence.

The strongest themes currently identified represent the areas receiving the highest concentration of report activity and should be considered when prioritizing future museum store initiatives.

Continued report generation will improve trend detection, category analysis, and recommendation quality over time.
"""

# ==========================================
# SAVE REPORT
# ==========================================

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
