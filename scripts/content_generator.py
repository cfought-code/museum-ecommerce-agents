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
        f"{product_name} by {artist} combines thoughtful "
        f"craftsmanship and artistic design. Created from "
        f"{materials}, this distinctive piece makes a memorable "
        f"gift and a striking addition to any collection."
    )

    long_description = (
        f"{product_name} showcases the creative vision of "
        f"{artist}. Crafted from {materials}, this museum-quality "
        f"{category.lower()} blends artistic expression with "
        f"everyday enjoyment. "
        f"{vendor_description} "
        f"Whether displayed at home, in an office, or given as "
        f"a thoughtful gift, this piece reflects the museum store "
        f"tradition of offering meaningful objects that inspire "
        f"curiosity, creativity, and appreciation for design."
    )

    meta_description = (
        f"Discover {product_name} by {artist}. "
        f"Crafted from {materials}, this museum-quality "
        f"{category.lower()} is ideal for gifting and collecting."
    )

    return {
        "shopify_title": shopify_title,
        "short_description": short_description,
        "long_description": long_description,
        "meta_description": meta_description
    }
