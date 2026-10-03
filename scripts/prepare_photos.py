"""Create gallery WebP copies without changing the source JPEGs.

Install requirements-images.txt, then run from the repository root.
Only the display and thumbnails directories are generated and committed.
"""

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageCms, ImageOps


SOURCE = Path("docs/assets/photography")
SIZES = {"thumbnails": (640, 78), "display": (2200, 88)}


def main():
    photos = sorted(SOURCE.glob("*.jpg"))
    if not photos:
        raise SystemExit(f"No source JPEGs found in {SOURCE}")
    for folder in SIZES:
        (SOURCE / folder).mkdir(exist_ok=True)
    for path in photos:
        with Image.open(path) as source:
            photo = ImageOps.exif_transpose(source).convert("RGB")
            # Preserve appearance for originals using a non-sRGB color profile.
            if profile := source.info.get("icc_profile"):
                photo = ImageCms.profileToProfile(
                    photo, ImageCms.ImageCmsProfile(BytesIO(profile)),
                    ImageCms.createProfile("sRGB"), outputMode="RGB",
                )
            name = path.stem.lower().lstrip("_").replace(" ", "-") + ".webp"
            for folder, (edge, quality) in SIZES.items():
                copy = photo.copy()
                copy.thumbnail((edge, edge), Image.Resampling.LANCZOS)
                # Export pixels only, without the originals' EXIF/XMP metadata.
                copy.info.clear()
                copy.save(SOURCE / folder / name, "WEBP", quality=quality, method=6)
    total = sum(p.stat().st_size for folder in SIZES for p in (SOURCE / folder).glob("*.webp"))
    print(f"Prepared {len(photos)} photographs in two sizes ({total / 1_000_000:.1f} MB).")


if __name__ == "__main__":
    main()
