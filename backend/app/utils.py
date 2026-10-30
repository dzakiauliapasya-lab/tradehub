import re
import uuid
from datetime import datetime


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "item"


def unique_slug(text: str, max_len: int) -> str:
    # contoh: "Sepatu Lari Pria" -> "sepatu-lari-pria-a1b2c3"
    return f"{slugify(text)[: max_len - 7]}-{uuid.uuid4().hex[:6]}"


def generate_order_number() -> str:
    # contoh: TH-20261022-9F3A1C7B
    return f"TH-{datetime.now():%Y%m%d}-{uuid.uuid4().hex[:8].upper()}"