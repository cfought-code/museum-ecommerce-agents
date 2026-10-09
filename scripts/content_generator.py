from data.category_content import CATEGORY_CONTENT


def generate_content(
    product_name,
    artist,
    category,
    materials,
    vendor_description,
    collection_recommendation
):
    """
    Shared content generation engine.

    Used by:
    - Product Description Agent
    - Shopify CSV Enrichment Agent
    - Future Artist Agent
    """

    category_lower = category.lower().strip()

    # ==========================================
    # CATEGORY CONTENT LOOKUP
    # ==========================================

    content_rule = CATEGORY_CONTENT.get(
        category_lower
    )

    if content_rule:

        short_description = (
            f"{product_name} by {artist} "
            f"{content_rule['short_description']}"
        )

        category_story = (
            content_rule["category_story"]
        )

    else:

        short_description = (
            f"{product_name} by {artist} combines "
            f"thoughtful craftsmanship and artistic "
            f"design, creating a meaningful addition "
            f"to any collection."
        )

        category_story = (
            "This museum-inspired item celebrates "
            "creativity, craftsmanship, and artistic "
            "expression."
        )

    # ==========================================
    # SHOPIFY TITLE
    # ==========================================

    shopify_title = (
        f"{product_name} by {artist}"
    )

    # ==========================================
    # LONG DESCRIPTION
    # ==========================================

    long_description = (
        f"{product_name} showcases the creative vision "
        f"of {artist}. Crafted from {materials}, this "
        f"museum-quality {category.lower()} offers an "
        f"opportunity to experience artistic design in "
        f"everyday life. "
        f"{category_story} "
        f"{vendor_description} "
        f"Whether purchased as a gift or added to a "
        f"personal collection, this piece reflects the "
        f"Toledo Museum of Art Store tradition of "
        f"connecting people with art, creativity, "
        f"and design."
    )

    # ==========================================
    # SEO META DESCRIPTION
    # ==========================================

    meta_description = (
        f"Discover {product_name} by {artist}. "
        f"A museum-quality {category.lower()} ideal "
        f"for gifting, collecting, and everyday "
        f"inspiration."
    )

    # ==========================================
    # RETURN CONTENT PACKAGE
    # ==========================================

    return {
        "shopify_title": shopify_title,
        "short_description": short_description,
        "long_description": long_description,
        "meta_description": meta_description,
    }
