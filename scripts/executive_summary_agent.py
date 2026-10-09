import os
from datetime import datetime

reporting_period = os.environ.get(
    "REPORTING_PERIOD",
    ""
)

# ==========================================
# HELPER
# ==========================================

def count_reports(path):

    if not os.path.exists(path):
        return 0

    files = []

    for root, dirs, filenames in os.walk(path):

        for filename in filenames:

            if (
                filename.endswith(".md")
                or filename.endswith(".txt")
                or filename.endswith(".csv")
            ):
                files.append(filename)

    return len(files)

# ==========================================
# REPORT COUNTS
# ==========================================

product_reports = count_reports(
    "reports/products"
)

artist_reports = count_reports(
    "reports/artists"
)

market_reports = count_reports(
    "reports/market"
)

executive_reports = count_reports(
    "reports/executive"
)

# ==========================================
# RECOMMENDATIONS
# ==========================================

recommendations = []

if market_reports > 0:
    recommendations.append(
        "Review competitor intelligence and identify merchandising opportunities."
    )

if product_reports > 0:
    recommendations.append(
        "Continue expanding product enrichment coverage across the catalog."
    )

if artist_reports > 0:
    recommendations.append(
        "Increase artist storytelling and collection-level content."
    )

if not recommendations:

    recommendations.append(
        "Continue generating reports to build the intelligence repository."
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

This briefing summarizes activity generated across the Museum Ecommerce Agents platform.

---

# Report Activity

## Product Reports

{product_reports}

## Artist Reports

{artist_reports}

## Market Intelligence Reports

{market_reports}

## Previous Executive Summaries

{executive_reports}

---

# Key Observations

"""

if product_reports > 0:

    report += """
- Product intelligence reports are available for merchandising review.
"""

if artist_reports > 0:

    report += """
- Artist-focused content has been generated and is available for storytelling initiatives.
"""

if market_reports > 0:

    report += """
- Competitive intelligence reports are available for strategic review.
"""

if (
    product_reports == 0
    and artist_reports == 0
    and market_reports == 0
):

    report += """
- No supporting reports were found.
"""

report += """

---

# Recommended Actions

"""

for index, item in enumerate(
    recommendations,
    start=1
):

    report += f"{index}. {item}\n"

report += """

---

# Competitors Monitored

- Corning Museum of Glass
- MCA Chicago Store
- Museum of Glass Store
- Artful Home

---

# Strategic Priorities

- Strengthen artist storytelling.
- Expand collection-level content.
- Continue SEO and AEO optimization.
- Monitor merchandising and gifting trends.
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
