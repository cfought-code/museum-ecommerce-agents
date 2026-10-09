import pandas as pd

# Load Shopify export

df = pd.read_csv(
    "data/shopify/products.csv"
)

# Create new columns

df["AI_Collection"] = ""
df["AI_Keywords"] = ""
df["AI_Cross_Sells"] = ""

for index, row in df.iterrows():

    category = str(
        row.get("Type", "")
    ).lower()

    if "jewelry" in category:

        df.at[index, "AI_Collection"] = \
            "Artist Jewelry"

        df.at[index, "AI_Keywords"] = \
            "artist jewelry, wearable art, museum jewelry"

        df.at[index, "AI_Cross_Sells"] = \
            "Scarves, Jewelry Trays"

    elif "glass" in category:

        df.at[index, "AI_Collection"] = \
            "Glass Art"

        df.at[index, "AI_Keywords"] = \
            "studio glass, art glass, collector gift"

        df.at[index, "AI_Cross_Sells"] = \
            "Glass Books, Paperweights"

    else:

        df.at[index, "AI_Collection"] = \
            "Museum Favorites"

# Save enriched file

df.to_csv(
    "reports/shopify_exports/enriched_products.csv",
    index=False
)

print(
    "Shopify enrichment complete."
)
