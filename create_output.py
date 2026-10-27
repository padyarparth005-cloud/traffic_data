
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parent
zip_path = root.parent / "smart_city_traffic_analysis.zip"

excluded = {"venv", ".venv", "__pycache__", ".git"}

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
    for file in root.rglob("*"):
        if not file.is_file():
            continue

        relative = file.relative_to(root)

        if any(part in excluded for part in relative.parts):
            continue

        if file.suffix == ".pyc":
            continue

        archive.write(file, relative)

print("ZIP created successfully:")
print(zip_path)
