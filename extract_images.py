import os
import shutil
from pathlib import Path


def extract_images(source_folder, destination_folder, image_extensions=None):
    if image_extensions is None:
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']

    image_extensions = [ext.lower() for ext in image_extensions]

    os.makedirs(destination_folder, exist_ok=True)

    image_count = 0

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if Path(file).suffix.lower() in image_extensions:
                source_path = os.path.join(root, file)

                base_name = os.path.basename(file)
                dest_path = os.path.join(destination_folder, base_name)

                if os.path.exists(dest_path):
                    name, ext = os.path.splitext(base_name)
                    counter = 1
                    while os.path.exists(dest_path):
                        new_name = f"{name}_{counter}{ext}"
                        dest_path = os.path.join(destination_folder, new_name)
                        counter += 1

                shutil.copy2(source_path, dest_path)
                image_count += 1

    print(f"Extracted {image_count} images to {destination_folder}")


if __name__ == "__main__":
    source_folder = r"C:\Users\Nehal Jain\projects\project_sem6\ImageOccupationPredictor\contextual_dataset6"
    destination_folder = r"C:\Users\Nehal Jain\projects\project_sem6\ImageOccupationPredictor\final_images"

    extract_images(source_folder, destination_folder)
