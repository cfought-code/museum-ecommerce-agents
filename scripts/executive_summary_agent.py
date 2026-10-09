import os
from datetime import datetime

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

themes = {
    "Studio Glass Art": 0,
    "Designer Jewelry": 0,
    "Kids Gifts": 0,
    "Books & Media": 0,
    "Home Decor": 0,
    "Artist Storytelling": 0,
    "Glass Art": 0,
    "Museum Favorites": 0
}

all_content = (
    "\n".join(product_reports)
    + "\n"
    + "\n".join(artist_reports)
    + "\n"
    + "\n".join(market_reports)
).lower()

for theme in themes:

    themes[theme] = (
        all_content.lower().count(
            theme.lower()
        )
    )

# ==========================================
# TOP THEMES
# ==========================================

sorted_themes = sorted(
    themes.items(),
    key=lambda x: x[1],
    reverse=True
)

top_themes = []

for theme, count in sorted_themes:

    if count > 0:

        top_themes.append(
            f"- {theme} ({count} references)"
        )

# ==========================================
# RECOMMENDATIONS
# ==========================================

recommendations = []

if themes["Studio Glass Art"] > 0:

    recommendations.append(
        "Continue expanding Studio Glass Art merchandise and storytelling."
    )

if themes["Designer Jewelry"] > 0:

    recommendations.append(
        "Promote Designer Jewelry in gifting and seasonal campaigns."
    )

if themes["Artist Storytelling"] > 0:

    recommendations.append(
        "Expand artist-focused content across product listings."
    )

if themes["Home Decor"] > 0:

    recommendations.append(
        "Highlight design-focused home décor collections."
    )

if not recommendations:

    recommendations.append(
        "Continue generating reports to strengthen trend analysis."
    )

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

This briefing summarizes report activity and recurring themes identified across museum ecommerce workflows.

---

# Reports Reviewed

Product Reports: {len(product_reports)}

Artist Reports: {len(artist_reports)}

Market Reports: {len(market_reports)}

---

# Top Themes

"""

if top_themes:

    report += "\n".join(top_themes)

else:

    report += "\nNo recurring themes identified."

report += """

---

# Strategic Recommendations

"""

for index, recommendation in enumerate(
    recommendations,
    start=1
):

    report += f"\n{index}. {recommendation}"

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
