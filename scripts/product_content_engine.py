from datetime import datetime
import os

from data.category_rules import CATEGORY_RULES

# ==========================================
# INPUTS
# ==========================================

product_name = os.environ.get("PRODUCT_NAME", "")
artist = os.environ.get("ARTIST", "")
category = os.environ.get("CATEGORY", "")
materials = os.environ.get("MATERIALS", "")
vendor_description = os.environ.get("VENDOR_DESCRIPTION", "")
collection = os.environ.get("COLLECTION", "")
price = os.environ.get("PRICE", "")
dimensions = os.environ.get("DIMENSIONS", "")
product_url = os.environ.get("PRODUCT_URL", "")

category_lower = category.lower().strip()

# ==========================================
# CATEGORY LOOKUP
# ==========================================

rule = CATEGORY_RULES.get(category_lower)

if rule:
    keywords = rule["keywords"]
    cross_sells = rule["cross_sells"]
    collection_recommendation = rule["collection"]
else:
    keywords = [
        "museum gift",
        "art inspired",
        "artist made",
        "design object",
        "museum store"
    ]

    cross_sells = [
        "Museum publications",
        "Design books"
    ]

    collection_recommendation = (
        collection if collection else "Museum Favorites"
    )

# ==========================================
# GIFT GUIDE ASSIGNMENT
# ==========================================

gift_categories = []

price_value = 0

try:
    price_value = float(
        price.replace("$", "").replace(",", "").strip()
    )
except ValueError:
    pass

if price_value < 30:
    gift_categories.append("Stocking Stuffers")

elif price_value < 75:
    gift_categories.append("Gifts Under $75")

else:
    gift_categories.append("Premium Gifts")

gift_categories.append("Museum Favorites")

# ==========================================
# SPECIAL MESSAGING
# ==========================================

exclusive_message = ""

if "museum" in category_lower:
    exclusive_message = (
        "Available through the Toledo Museum of Art Store, "
        "this item reflects the museum's commitment to art, "
        "education, and creativity."
    )

elif "exhibition" in category_lower:
    exclusive_message = (
        "Inspired by the Toledo Museum of Art exhibition program, "
        "this item extends the visitor experience beyond the gallery."
    )

# ==========================================
# CONTENT GENERATION
# ==========================================

shopify_title = f"{product_name} by {artist}"

short_description = (
    f"{product_name} by {artist} combines thoughtful craftsmanship "
    f"and artistic design. Created from {materials}, this distinctive "
    f"piece makes a memorable gift and a striking addition to any collection."
)

long_description = f"""
{product_name} showcases the creative vision of {artist}. Crafted from
{materials}, this museum-quality {category.lower()} blends artistic
expression with everyday enjoyment.

{vendor_description}

{exclusive_message}

Whether displayed at home, in an office, or given as a thoughtful gift,
this piece reflects the museum store tradition of offering meaningful
objects that inspire curiosity, creativity, and appreciation for design.
"""

meta_description = (
    f"Discover {product_name} by {artist}. Crafted from "
    f"{materials}, this museum-quality {category.lower()} "
    f"is ideal for gifting and collecting."
)

# ==========================================
# REPORT GENERATION
# ==========================================

report = f"""# Product Description Agent Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Product Information

**Product Name:** {product_name}

**Artist:** {artist}

**Category:** {category}

**Materials:** {materials}

**Collection:** {collection}

**Recommended Collection:** {collection_recommendation}

**Price:** {price}

**Dimensions:** {dimensions}

**Product URL:** {product_url}

---

## Vendor Description

{vendor_description}

---

## Suggested Shopify Product Title

{shopify_title}

---

## Short Description

{short_description}

---

## Long Description

{long_description}

---

## SEO Meta Description

{meta_description}

---

## Suggested Keywords

"""

for keyword in keywords:
    report += f"- {keyword}\n"

report += "\n---\n\n## Gift Guide Categories\n\n"

for gift in gift_categories:
    report += f"- {gift}\n"

report += "\n---\n\n## Cross-Sell Opportunities\n\n"

for item in cross_sells:
    report += f"- {item}\n"

# ==========================================
# SAVE REPORT
# ==========================================

os.makedirs("reports/products", exist_ok=True)

output_file = (
    "reports/products/product-description-report.md"
)

with open(
    output_file,
    "w",
    encoding="utf-8"
) as file:
    file.write(report)

print(
    f"Product Description Report generated successfully: "
    f"{output_file}"
)
