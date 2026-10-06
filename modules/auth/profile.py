import base64
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROFILE_PHOTO_DIR = PROJECT_ROOT / "data" / "user_profiles"
DEFAULT_PROFILE_PHOTO = PROJECT_ROOT / "assets" / "default-user-avatar.svg"


def profile_photo_data_uri(user_id):
    photo_path = PROFILE_PHOTO_DIR / f"{int(user_id)}.png"
    if photo_path.is_file():
        content_type = "image/png"
    else:
        photo_path = DEFAULT_PROFILE_PHOTO
        content_type = "image/svg+xml"

    encoded_photo = base64.b64encode(photo_path.read_bytes()).decode("ascii")
    return f"data:{content_type};base64,{encoded_photo}"


def normalize_profile_photo(photo_data):
    try:
        with Image.open(BytesIO(photo_data)) as source:
            image = ImageOps.exif_transpose(source)
            image.load()
            image.thumbnail((512, 512))
            if image.mode not in ("RGB", "RGBA"):
                image = image.convert("RGBA")

            normalized = BytesIO()
            image.save(normalized, format="PNG")
            return normalized.getvalue()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as error:
        raise ValueError("That file is not a valid supported image.") from error


def save_profile_photo(user_id, photo_data):
    PROFILE_PHOTO_DIR.mkdir(parents=True, exist_ok=True)
    photo_path = PROFILE_PHOTO_DIR / f"{int(user_id)}.png"
    photo_path.write_bytes(photo_data)


def remove_profile_photo(user_id):
    photo_path = PROFILE_PHOTO_DIR / f"{int(user_id)}.png"
    if photo_path.is_file():
        photo_path.unlink()
