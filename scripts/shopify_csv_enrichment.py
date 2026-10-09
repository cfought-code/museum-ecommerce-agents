import os
import pandas as pd

from data.category_rules import CATEGORY_RULES

# ==========================================
# FILES
# ==========================================

INPUT_FILE = "data/shopify/products.csv"

OUTPUT_FILE = (
    "reports/shopify_exports/enriched_products.csv"
)

# ==========================================
# LOAD CSV
# ==========================================

df = pd.read_csv(INPUT_FILE)

# ==========================================
# NEW COLUMNS
# ==========================================

df["AI_Collection"] = ""
df["AI_Keywords"] = ""
df["AI_Cross_Sells"] = ""
df["AI_Gift_Guide"] = ""

# ==========================================
# ENRICH PRODUCTS
# ==========================================

for index, row in df.iterrows():

    category = str(
        row.get("Type", "")
    ).lower().strip()

    price = 0

    try:
        price = float(
            str(row.get("Variant Price", "0"))
            .replace("$", "")
            .replace(",", "")
        )
    except:
        pass

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

        collection = "Museum Favorites"

        keywords = (
            "museum gift, art inspired, design object"
        )

        cross_sells = (
            "Museum publications, Design books"
        )

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

# ==========================================
# SAVE
# ==========================================

os.makedirs(
    "reports/shopify_exports",
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    f"Enriched CSV created: {OUTPUT_FILE}"
)
