import os
import pandas as pd

from data.category_rules import CATEGORY_RULES

print("Starting Shopify CSV Enrichment...")

# ==========================================
# FILE PATHS
# ==========================================

INPUT_FILE = "data/shopify/products.csv"

OUTPUT_FILE = (
    "reports/shopify_exports/enriched_products.csv"
)

# ==========================================
# LOAD PRODUCTS
# ==========================================

df = pd.read_csv(INPUT_FILE)

print(f"Loaded {len(df)} products")

# ==========================================
# NEW AI COLUMNS
# ==========================================

df["AI_Collection"] = ""
df["AI_Keywords"] = ""
df["AI_Cross_Sells"] = ""
df["AI_Gift_Guide"] = ""
df["AI_Short_Description"] = ""
df["AI_Long_Description"] = ""
df["AI_Meta_Description"] = ""

# ==========================================
# PROCESS PRODUCTS
# ==========================================

for index, row in df.iterrows():

    title = str(
        row.get("Title", "")
    ).strip()

    category = str(
        row.get("Type", "")
    ).lower().strip()

    vendor = str(
        row.get("Vendor", "")
    ).strip()

    price = 0

    try:
        price = float(
            str(
                row.get(
                    "Variant Price",
                    0
                )
            )
            .replace("$", "")
            .replace(",", "")
        )
    except Exception:
        pass

    # --------------------------------------
    # CATEGORY RULE LOOKUP
    # --------------------------------------

    rule = CATEGORY_RULES.get(category)

    if rule:

        collection = rule["collection"]

        keywords = ", ".join(
            rule["keywords"]
        )

        cross_sells = ", ".join(
            rule["cross_sells"]
        )

    else:

        collection = (
            "Museum Favorites"
        )

        keywords = (
            "museum gift, art inspired, artist made"
        )

        cross_sells = (
            "Museum publications, Design books"
        )

    # --------------------------------------
    # GIFT GUIDE LOGIC
    # --------------------------------------

    if price < 30:

        gift_guide = (
            "Stocking Stuffers"
        )

    elif price < 75:

        gift_guide = (
            "Gifts Under $75"
        )

    else:

        gift_guide = (
            "Premium Gifts"
        )

    # --------------------------------------
    # CONTENT GENERATION
    # --------------------------------------

    short_description = (
        f"{title} by {vendor} combines artistic "
        f"expression and thoughtful craftsmanship, "
        f"making it a distinctive addition to any "
        f"collection."
    )

    long_description = (
        f"{title} showcases the creative vision of "
        f"{vendor}. Inspired by artistic excellence "
        f"and museum-quality design, this "
        f"{category} offers a meaningful way to "
        f"bring creativity into everyday life. "
        f"Whether purchased as a gift or for a "
        f"personal collection, it reflects the "
        f"Toledo Museum of Art Store tradition of "
        f"connecting people with art and design."
    )

    meta_description = (
        f"Discover {title} by {vendor}. "
        f"A museum-quality {category} ideal for "
        f"collecting, gifting, and everyday inspiration."
    )

    # --------------------------------------
    # SAVE ENRICHED VALUES
    # --------------------------------------

    df.at[index, "AI_Collection"] = (
        collection
    )

    df.at[index, "AI_Keywords"] = (
        keywords
    )

    df.at[index, "AI_Cross_Sells"] = (
        cross_sells
    )

    df.at[index, "AI_Gift_Guide"] = (
        gift_guide
    )

    df.at[index, "AI_Short_Description"] = (
        short_description
    )

    df.at[index, "AI_Long_Description"] = (
        long_description
    )

    df.at[index, "AI_Meta_Description"] = (
        meta_description
    )

# ==========================================
# SAVE OUTPUT
# ==========================================

os.makedirs(
    "reports/shopify_exports",
    exist_ok=True
)

print(f"Writing file: {OUTPUT_FILE}")

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("CSV written successfully")

print(
    f"Enriched CSV created: {OUTPUT_FILE}"
)
