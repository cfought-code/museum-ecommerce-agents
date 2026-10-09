def generate_content(
    product_name,
    artist,
    category,
    materials,
    vendor_description,
    collection_recommendation
):
    shopify_title = (
        f"{product_name} by {artist}"
    )

    short_description = (
        f"{product_name} by {artist} combines "
        f"thoughtful craftsmanship and artistic "
        f"design. Created from {materials}, this "
        f"distinctive piece makes a memorable gift "
        f"and a striking addition to any collection."
    )

    long_description = f"""
{product_name} showcases the creative vision of
{artist}. Crafted from {materials}, this
museum-quality {category.lower()} blends artistic
expression with everyday enjoyment.

{vendor_description}

Whether displayed at home, in an office, or given
as a thoughtful gift, this piece reflects the
museum store tradition of offering meaningful
objects that inspire curiosity, creativity, and
appreciation for design.
"""

    meta_description = (
        f"Discover {product_name} by {artist}. "
        f"Crafted from {materials}, this museum-quality "
        f"{category.lower()} is ideal for gifting "
        f"and collecting."
    )

    return {
        "shopify_title": shopify_title,
        "short_description": short_description,
        "long_description": long_description,
        "meta_description": meta_description
    }
