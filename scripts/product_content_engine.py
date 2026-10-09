from datetime import datetime
import os

product_name = os.environ.get("PRODUCT_NAME", "")
artist = os.environ.get("ARTIST", "")
category = os.environ.get("CATEGORY", "")
materials = os.environ.get("MATERIALS", "")
vendor_description = os.environ.get("VENDOR_DESCRIPTION", "")
collection = os.environ.get("COLLECTION", "")
price = os.environ.get("PRICE", "")
dimensions = os.environ.get("DIMENSIONS", "")
product_url = os.environ.get("PRODUCT_URL", "")
# Category Intelligence

category_lower = category.lower()

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

## Gift Guide Category

{"".join([f"- {gift}\n" for gift in gift_categories])}

# Collection Recommendation

collection_recommendation = collection

if not collection:

    if "mobile" in category_lower:
        collection_recommendation = "Modern Design"

    elif "jewelry" in category_lower:
        collection_recommendation = "Artist Jewelry"

    elif "glass" in category_lower:
        collection_recommendation = "Glass Art"

    else:
        collection_recommendation = "Museum Favorites"

## Cross-Sell Opportunities

{"".join([f"- {item}\n" for item in cross_sells])}

report = f"""
# Product Description Agent Report

Generated: {datetime.now()}

## Product Information

**Product Name:** {product_name}

**Artist:** {artist}

**Category:** {category}

**Materials:** {materials}

**Collection:** {collection}

**Price:** {price}

**Dimensions:** {dimensions}

**Product URL:** {product_url}

**Recommended Collection:** {collection_recommendation}

---

## Vendor Description

{vendor_description}

---

## Suggested Shopify Product Title

{product_name} by {artist}

---

## Short Description

{product_name} by {artist} combines thoughtful craftsmanship and artistic design. Created from {materials}, this distinctive piece makes a memorable gift and a striking addition to any collection.

---

## Long Description

{product_name} showcases the creative vision of {artist}. Crafted from {materials}, this museum-quality {category.lower()} blends artistic expression with everyday enjoyment.

{vendor_description}

Whether displayed at home, in an office, or given as a thoughtful gift, this piece reflects the museum store tradition of offering meaningful objects that inspire curiosity, creativity, and appreciation for design.

---

## SEO Meta Description

Discover {product_name} by {artist}. A museum-quality design object crafted from {materials} and ideal for gifting or collecting.

---

## Suggested Tags

- museum store
- design
- art gift
- collectible
- {category}

---

## Suggested Keywords

{"".join([f"- {keyword}\n" for keyword in keywords])}
"""

os.makedirs("reports/products", exist_ok=True)

with open(
    "reports/products/product-description-report.md",
    "w",
    encoding="utf-8"
) as f:
    f.write(report)

print("Report generated successfully.")
