import os
from pathlib import Path
import hashlib


def make_filenames_unique(folder_path, prefix="img_"):
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist")
        return

    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}

    image_files = [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if Path(file).suffix.lower() in image_extensions and os.path.isfile(os.path.join(folder_path, file))
    ]

    print(f"Found {len(image_files)} image files")

    renamed_count = 0
    seen_filenames = set()

    for index, file_path in enumerate(image_files):
        ext = Path(file_path).suffix.lower()

        with open(file_path, "rb") as f:
            file_hash = hashlib.md5(f.read(4096)).hexdigest()[:8]

        new_filename = f"{prefix}{index + 1:04d}_{file_hash}{ext}"
        new_filepath = os.path.join(folder_path, new_filename)

        if new_filename in seen_filenames:
            print(f"Skipping {file_path}, duplicate name detected.")
            continue

        seen_filenames.add(new_filename)
        os.rename(file_path, new_filepath)
        renamed_count += 1

    print(f"Successfully renamed {renamed_count} images with unique names")


if __name__ == "__main__":
    folder_path = r"C:\Users\Nehal Jain\projects\project_sem6\ImageOccupationPredictor\final\final_images"
    make_filenames_unique(folder_path)
