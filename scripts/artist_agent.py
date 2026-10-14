import os
from datetime import datetime

from data.artist_content import ARTIST_CONTENT

# ==========================================
# INPUTS
# ==========================================

artist_name = os.environ.get(
    "ARTIST_NAME",
    ""
)

medium = os.environ.get(
    "MEDIUM",
    ""
)

location = os.environ.get(
    "LOCATION",
    ""
)

artist_statement = os.environ.get(
    "ARTIST_STATEMENT",
    ""
)

medium_lower = (
    medium.lower().strip()
)

# ==========================================
# MEDIUM LOOKUP
# ==========================================

artist_rule = ARTIST_CONTENT.get(
    medium_lower
)

if not artist_rule:

    artist_rule = ARTIST_CONTENT[
        "default"
    ]

# ==========================================
# CONTENT VARIABLES
# ==========================================

bio_focus = (
    artist_rule["bio_focus"]
)

artist_story_text = (
    artist_rule["artist_story"]
)

collection_intro = (
    artist_rule["collection_intro"]
)

# ==========================================
# CONTENT GENERATION
# ==========================================

short_bio = (
    f"{artist_name} is a {bio_focus} "
    f"whose work demonstrates a commitment "
    f"to craftsmanship, creativity, and "
    f"artistic expression."
)

artist_story = (
    f"{artist_story_text} "
    f"{artist_statement}"
)

seo_description = (
    f"Discover the work of {artist_name}, "
    f"a {bio_focus} creating museum-quality "
    f"artwork that celebrates creativity, "
    f"craftsmanship, and design."
)

# ==========================================
# REPORT
# ==========================================

report = f"""# Artist Agent Report

Generated:
{datetime.now()}

---

## Artist Information

**Artist Name:** {artist_name}

**Primary Medium:** {medium}

**Location:** {location}

---

## Short Artist Bio

{short_bio}

---

## Artist Story

{artist_story}

---

## Collection Introduction

{collection_intro}

---

## SEO Meta Description

{seo_description}
"""

# ==========================================
# OUTPUT FILES
# ==========================================

timestamp = datetime.now().strftime(
    "%Y-%m-%d"
)

output_file = (
    "reports/artists/artist-report.md"
)

archive_file = (
    f"reports/intelligence/artists/"
    f"{timestamp}-artist-report.md"
)

# ==========================================
# SAVE CURRENT REPORT
# ==========================================

os.makedirs(
    "reports/artists",
    exist_ok=True
)

with open(
    output_file,
    "w",
    encoding="utf-8"
) as file:

    file.write(report)

# ==========================================
# SAVE ARCHIVE REPORT
# ==========================================

os.makedirs(
    "reports/intelligence/artists",
    exist_ok=True
)

with open(
    archive_file,
    "w",
    encoding="utf-8"
) as file:

    file.write(report)

# ==========================================
# LOGGING
# ==========================================

print(
    f"Current report created: {output_file}"
)

print(
    f"Archive report created: {archive_file}"
)
