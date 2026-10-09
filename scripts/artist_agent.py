import os
from datetime import datetime

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

report = f"""# Artist Agent Report

Generated:
{datetime.now()}

---

## Artist Name

{artist_name}

## Primary Medium

{medium}

## Location

{location}

---

## Short Artist Bio

{artist_name} works primarily in {medium}. Their work reflects a commitment to craftsmanship, creativity, and artistic expression.

---

## Artist Story

Through a practice centered on {medium}, {artist_name} creates work that encourages curiosity, appreciation for materials, and thoughtful engagement with art.

{artist_statement}

---

## Collection Introduction

The work of {artist_name} demonstrates the creative possibilities of {medium}. These pieces highlight artistic vision, technical skill, and a dedication to making meaningful connections through art.

---

## SEO Meta Description

Discover the work of {artist_name}, an artist working in {medium}. Explore museum-quality artwork celebrating creativity, craftsmanship, and design.
"""

os.makedirs(
    "reports/artists",
    exist_ok=True
)

with open(
    "reports/artists/artist-report.md",
    "w",
    encoding="utf-8"
) as file:
    file.write(report)

print("Artist report generated successfully.")
