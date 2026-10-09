from datetime import datetime
import os

# Inputs

product_name = os.environ.get("PRODUCT_NAME", "")
artist = os.environ.get("ARTIST", "")
category = os.environ.get("CATEGORY", "")
materials = os.environ.get("MATERIALS", "")
vendor_description = os.environ.get("VENDOR_DESCRIPTION", "")
collection = os.environ.get("COLLECTION", "")
price = os.environ.get("PRICE", "")
dimensions = os.environ.get("DIMENSIONS", "")
product_url = os.environ.get("PRODUCT_URL", "")

category_lower = category.lower()

# Category Intelligence

if "mobile" in category_lower:
    keywords = [
        "hanging mobile",
        "kinetic art",
        "scandinavian design",
        "modern decor",
        "museum gift"
    ]

    cross_sells = [
        "Design books",
        "Decorative objects",
        "Wall art"
    ]

elif "jewelry" in category_lower:
    keywords = [
        "artist jewelry",
        "museum jewelry",
        "wearable art",
        "handcrafted jewelry",
        "gift jewelry"
    ]

    cross_sells = [
        "Jewelry trays",
        "Scarves",
        "Artist accessories"
    ]

elif "glass" in category_lower:
    keywords = [
        "art glass",
        "glass sculpture",
        "museum glass",
        "glass gift",
        "decorative glass"
    ]

    cross_sells = [
        "Glass ornaments",
        "Paperweights",
        "Glass books"
    ]

else:
    keywords = [
        "museum gift",
        "artist made",
        "design object",
        "home decor",
        "collectible art"
    ]

    cross_sells = [
        "Museum gifts",
        "Design books"
    ]

# Gift Guide Assignment

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

# Collection Recommendation

collection_recommendation = collection

if not collection.strip():

    if "mobile" in category_lower:
        collection_recommendation = "Modern Design"

    elif "jewelry" in category_lower:
        collection_recommendation = "Artist Jewelry"

    elif "glass" in category_lower:
        collection_recommendation = "Glass Art"

    else:
        collection_recommendation = "Museum Favorites"

# Dynamic Content

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

Whether displayed at home, in an office, or given as a thoughtful gift,
this piece reflects the museum store tradition of offering meaningful
objects that inspire curiosity, creativity, and appreciation for design.
"""

meta_description = (
    f"Discover {product_name} by {artist}. Crafted from "
    f"{materials}, this museum-quality {category.lower()} "
    f"is ideal for gifting and collecting."
)

# Build Markdown Report

report = f"""# Product Description Agent Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

# Product Information

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

# Vendor Description

{vendor_description}

---

# Suggested Shopify Product Title

{shopify_title}

---

# Short Description

{short_description}

---

# Long Description

{long_description}

---

# SEO Meta Description

{meta_description}

---

# Suggested Tags

- museum store
- art gift
- design
- collectible
- {category}

---

# Suggested Keywords

"""

for keyword in keywords:
    report += f"- {keyword}\n"

report += "\n---\n\n# Gift Guide Categories\n\n"

for gift in gift_categories:
    report += f"- {gift}\n"

report += "\n---\n\n# Cross-Sell Opportunities\n\n"

for item in cross_sells:
    report += f"- {item}\n"

# Write Report

os.makedirs("reports/products", exist_ok=True)

with open(
    "reports/products/product-description-report.md",
    "w",
    encoding="utf-8"
) as f:
    f.write(report)

print("Product Description Report generated successfully.")
