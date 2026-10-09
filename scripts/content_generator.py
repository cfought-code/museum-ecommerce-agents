def generate_content(
    product_name,
    artist,
    category,
    materials,
    vendor_description,
    collection_recommendation
):

    category_lower = category.lower().strip()

    # ==========================================
    # CATEGORY-SPECIFIC COPY
    # ==========================================

    if category_lower == "studio glass art":

        short_description = (
            f"{product_name} by {artist} showcases the beauty "
            f"of contemporary glass artistry. A striking addition "
            f"to any collection, it offers color, craftsmanship, "
            f"and visual impact."
        )

        category_story = (
            "Drawing on the tradition of studio glass, this work "
            "celebrates craftsmanship, light, color, and artistic "
            "expression."
        )

    elif category_lower == "designer jewelry":

        short_description = (
            f"{product_name} by {artist} transforms artistic vision "
            f"into wearable design, making it a distinctive accessory "
            f"for everyday wear or special occasions."
        )

        category_story = (
            "Blending artistry and craftsmanship, this piece reflects "
            "the museum store's commitment to wearable art."
        )

    elif category_lower == "local jewelry":

        short_description = (
            f"{product_name} highlights the creativity of local artists, "
            f"offering a unique wearable expression of craftsmanship and design."
        )

        category_story = (
            "Created by a regional artist, this piece celebrates "
            "local creativity and artistic excellence."
        )

    elif category_lower == "books & media":

        short_description = (
            f"{product_name} provides an engaging opportunity to explore "
            f"art, creativity, and culture through the printed page."
        )

        category_story = (
            "Designed to educate and inspire, this title supports deeper "
            "engagement with art and visual culture."
        )

    elif category_lower == "kids gifts":

        short_description = (
            f"{product_name} encourages creativity, learning, and artistic "
            f"exploration through hands-on experiences."
        )

        category_story = (
            "Selected to inspire curiosity and imagination, this item helps "
            "connect young learners with art and creativity."
        )

    elif category_lower == "art supplies":

        short_description = (
            f"{product_name} supports creative practice and artistic "
            f"exploration for makers of all experience levels."
        )

        category_story = (
            "Designed for creative expression, these materials help transform "
            "ideas into works of art."
        )

    elif category_lower == "home decor":

        short_description = (
            f"{product_name} combines design and function, bringing artistic "
            f"inspiration into everyday living spaces."
        )

        category_story = (
            "Influenced by contemporary design principles, this piece adds "
            "character and visual interest to the home."
        )

    else:

        short_description = (
            f"{product_name} by {artist} combines thoughtful craftsmanship "
            f"and artistic design, creating a meaningful addition to any "
            f"collection."
        )

        category_story = (
            "This museum-inspired item celebrates creativity, craftsmanship, "
            "and artistic expression."
        )

    # ==========================================
    # SHARED CONTENT
    # ==========================================

    shopify_title = (
        f"{product_name} by {artist}"
    )

    long_description = (
        f"{product_name} showcases the creative vision of {artist}. "
        f"Crafted from {materials}, this museum-quality "
        f"{category.lower()} offers an opportunity to experience "
        f"artistic design in everyday life. "
        f"{category_story} "
        f"{vendor_description} "
        f"Whether purchased as a gift or added to a personal collection, "
        f"this piece reflects the Toledo Museum of Art Store tradition "
        f"of connecting people with art, creativity, and design."
    )

    meta_description = (
        f"Discover {product_name} by {artist}. "
        f"A museum-quality {category.lower()} ideal for gifting, "
        f"collecting, and everyday inspiration."
    )

    return {
        "shopify_title": shopify_title,
        "short_description": short_description,
        "long_description": long_description,
        "meta_description": meta_description
    }
