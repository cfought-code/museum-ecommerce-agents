from datetime import datetime
import os

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
# CATEGORY RULES
# ==========================================

CATEGORY_RULES = {

    "designer jewelry": {
        "collection": "Artist Jewelry",
        "keywords": [
            "artist jewelry",
            "museum jewelry",
            "wearable art",
            "designer jewelry",
            "gift jewelry"
        ],
        "cross_sells": [
            "Jewelry trays",
            "Scarves",
            "Artist accessories"
        ]
    },

    "local jewelry": {
        "collection": "Local Artists",
        "keywords": [
            "local artist jewelry",
            "handcrafted jewelry",
            "wearable art",
            "museum jewelry",
            "artisan jewelry"
        ],
        "cross_sells": [
            "Scarves",
            "Handbags",
            "Artist accessories"
        ]
    },

    "studio glass art": {
        "collection": "Glass Art",
        "keywords": [
            "studio glass",
            "glass sculpture",
            "art glass",
            "collector gift",
            "glass artwork"
        ],
        "cross_sells": [
            "Glass books",
            "Paperweights",
            "Museum glass artwork"
        ]
    },

    "ceramics": {
        "collection": "Functional Art",
        "keywords": [
            "ceramic art",
            "handmade pottery",
            "artisan ceramics",
            "museum gift",
            "functional art"
        ],
        "cross_sells": [
            "Art books",
            "Home decor",
            "Decorative objects"
        ]
    },

    "paintings": {
        "collection": "Collector's Corner",
        "keywords": [
            "original artwork",
            "fine art",
            "painting",
            "collector artwork",
            "local artist"
        ],
        "cross_sells": [
            "Art books",
            "Museum publications",
            "Art prints"
        ]
    },

    "drawings": {
        "collection": "Collector's Corner",
        "keywords": [
            "drawing",
            "fine art",
            "works on paper",
            "artist drawing",
            "collector artwork"
        ],
        "cross_sells": [
            "Museum publications",
            "Art books",
            "Sketchbooks"
        ]
    },

    "printmaking art": {
        "collection": "Collector's Corner",
        "keywords": [
            "art print",
            "printmaking",
            "limited edition print",
            "artist print",
            "museum art"
        ],
        "cross_sells": [
            "Art books",
            "Posters",
            "Museum publications"
        ]
    },

    "photography art": {
        "collection": "Collector's Corner",
        "keywords": [
            "photography",
            "fine art photography",
            "photographic art",
            "museum artwork",
            "artist photography"
        ],
        "cross_sells": [
            "Photography books",
            "Museum publications",
            "Art prints"
        ]
    },

    "mixed media art": {
        "collection": "Collector's Corner",
        "keywords": [
            "mixed media",
            "contemporary art",
            "artist made",
            "original artwork",
            "museum art"
        ],
        "cross_sells": [
            "Art books",
            "Museum publications",
            "Contemporary design objects"
        ]
    },

    "metal art": {
        "collection": "Collector's Corner",
        "keywords": [
            "metal sculpture",
            "metal artwork",
            "artist made",
            "decorative metal art",
            "museum art"
        ],
        "cross_sells": [
            "Sculpture books",
            "Home decor",
            "Decorative objects"
        ]
    },

    "wood art": {
        "collection": "Collector's Corner",
        "keywords": [
            "woodworking",
            "wood sculpture",
            "wood art",
            "handcrafted design",
            "artist made"
        ],
        "cross_sells": [
            "Design books",
            "Home decor",
            "Decorative objects"
        ]
    },

    "stone art": {
        "collection": "Collector's Corner",
        "keywords": [
            "stone sculpture",
            "carved stone",
            "museum artwork",
            "artist made",
            "decorative sculpture"
        ],
        "cross_sells": [
            "Sculpture books",
            "Decorative objects",
            "Museum publications"
        ]
    },

    "fiber art": {
        "collection": "Textile Arts",
        "keywords": [
            "fiber art",
            "textile art",
            "artist made",
            "museum textile",
            "decorative fiber art"
        ],
        "cross_sells": [
            "Textiles",
            "Scarves",
            "Home decor"
        ]
    },

    "functional art": {
        "collection": "Functional Art",
        "keywords": [
            "functional art",
            "artist made",
            "museum gift",
            "design object",
            "artisan craft"
        ],
        "cross_sells": [
            "Home decor",
            "Tabletop accessories",
            "Design books"
        ]
    },

    "holiday art": {
        "collection": "Holiday Favorites",
        "keywords": [
            "holiday gift",
            "ornament",
            "seasonal decor",
            "holiday art",
            "museum holiday"
        ],
        "cross_sells": [
            "Ornaments",
            "Holiday cards",
            "Seasonal decor"
        ]
    },

    "books & media": {
        "collection": "Museum Library",
        "keywords": [
            "art books",
            "museum books",
            "art history",
            "gallery books",
            "museum publications"
        ],
        "cross_sells": [
            "Bookmarks",
            "Museum publications",
            "Desk items"
        ]
    },

    "home decor": {
        "collection": "Modern Design",
        "keywords": [
            "home decor",
            "design object",
            "modern decor",
            "museum design",
            "stylish home"
        ],
        "cross_sells": [
            "Desk items",
            "Decorative objects",
            "Design books"
        ]
    },

    "desk items": {
        "collection": "Creative Workspace",
        "keywords": [
            "desk accessories",
            "office decor",
            "creative workspace",
            "museum gift",
            "design accessories"
        ],
        "cross_sells": [
            "Books",
            "Journals",
            "Home decor"
        ]
    },

    "kids gifts": {
        "collection": "Family Favorites",
        "keywords": [
            "kids gifts",
            "educational toys",
            "creative activities",
            "museum kids",
            "learning through art"
        ],
        "cross_sells": [
            "Art supplies",
            "Books",
            "Educational games"
        ]
    },

    "art supplies": {
        "collection": "Creative Studio",
        "keywords": [
            "artist supplies",
            "creative tools",
            "art materials",
            "museum creativity",
            "studio supplies"
        ],
        "cross_sells": [
            "Sketchbooks",
            "Books",
            "Desk items"
        ]
    }
}

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
except:
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
        "\nAvailable through the Toledo Museum of Art Store, "
        "this item reflects the museum's commitment to art, "
        "education, and creativity.\n"
    )

if "exhibition" in category_lower:
    exclusive_message = (
        "\nInspired by the Toledo Museum of Art exhibition program, "
        "this item extends the visitor experience beyond the gallery.\n"
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
# REPORT
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

with open(
    "reports/products/product-description-report.md",
    "w",
    encoding="utf-8"
) as f:
    f.write(report)

print("Product Description Report generated successfully.")
