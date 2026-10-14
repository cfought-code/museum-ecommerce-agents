from datetime import datetime
import os

from data.category_rules import CATEGORY_RULES
from data.category_aliases import CATEGORY_ALIASES
from scripts.content_generator import generate_content

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

# ==========================================
# CATEGORY NORMALIZATION
# ==========================================

category_lower = category.lower().strip()

category_lower = CATEGORY_ALIASES.get(
    category_lower,
    category_lower
)

# ==========================================
# CATEGORY LOOKUP
# ==========================================

rule = CATEGORY_RULES.get(category_lower)

if rule:

    keywords = rule["keywords"]

    cross_sells = rule["cross_sells"]

    collection_recommendation = (
        rule["collection"]
    )

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
        collection
        if collection
        else "Museum Favorites"
    )

# ==========================================
# GIFT GUIDE ASSIGNMENT
# ==========================================

gift_categories = []

price_value = None

try:

    if price and price.strip():

        price_value = float(
            price.replace("$", "")
            .replace(",", "")
            .strip()
        )

except ValueError:

    price_value = None

if price_value is None:

    gift_categories.append(
        "Price Not Provided"
    )

elif price_value < 30:

    gift_categories.append(
        "Stocking Stuffers"
    )

elif price_value < 75:

    gift_categories.append(
        "Gifts Under $75"
    )

else:

    gift_categories.append(
        "Premium Gifts"
    )

gift_categories.append(
    "Museum Favorites"
)

# ==========================================
# CONTENT GENERATION
# ==========================================

content = generate_content(
    product_name=product_name,
    artist=artist,
    category=category_lower,
    materials=materials,
    vendor_description=vendor_description,
    collection_recommendation=collection_recommendation
)

shopify_title = (
    content["shopify_title"]
)

short_description = (
    content["short_description"]
)

long_description = (
    content["long_description"]
)

meta_description = (
    content["meta_description"]
)

# ==========================================
# BUILD REPORT
# ==========================================

report = f"""# Product Description Agent Report

Generated:
{datetime.now()}

---

## Product Information

**Product Name:** {product_name}

**Artist:** {artist}

**Category:** {category}

**Normalized Category:** {category_lower}

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

    report += f"\n- {keyword}"

report += "\n\n---\n\n## Gift Guide Categories\n"

for gift in gift_categories:

    report += f"\n- {gift}"

report += "\n\n---\n\n## Cross-Sell Opportunities\n"

for item in cross_sells:

    report += f"\n- {item}"

# ==========================================
# OUTPUT FILES
# ==========================================

timestamp = datetime.now().strftime(
    "%Y-%m-%d"
)

output_file = (
    "reports/products/product-description-report.md"
)

archive_file = (
    f"reports/intelligence/products/"
    f"{timestamp}-product-report.md"
)

# ==========================================
# SAVE CURRENT REPORT
# ==========================================

os.makedirs(
    "reports/products",
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
    "reports/intelligence/products",
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
