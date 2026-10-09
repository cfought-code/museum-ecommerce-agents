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

---

## Vendor Description

{vendor_description}

---

## Suggested Shopify Product Title

{product_name} by {artist}

---

## Short Description

Bring museum-quality design into everyday life with {product_name}. Created by {artist}, this distinctive piece showcases thoughtful craftsmanship and contemporary appeal.

---

## Long Description

{product_name} is a beautifully designed work by {artist} that reflects creativity, craftsmanship, and functionality. Crafted from {materials}, this piece offers collectors and design enthusiasts an opportunity to incorporate artistic expression into their home or workspace.

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

- museum gift
- artist designed
- contemporary design
- home decor
- collectible art
"""

os.makedirs("reports/products", exist_ok=True)

with open(
    "reports/products/product-description-report.md",
    "w",
    encoding="utf-8"
) as f:
    f.write(report)

print("Report generated successfully.")
