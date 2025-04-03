import os
import shutil

images_folder = r"C:\Users\Nehal Jain\projects\project_sem6\ImageOccupationPredictor\final\val\images"
labels_folder = r"C:\Users\Nehal Jain\projects\project_sem6\ImageOccupationPredictor\final\final_labels _copy"
output_folder = r"C:\Users\Nehal Jain\projects\project_sem6\ImageOccupationPredictor\final\val\labels"

if not os.path.exists(labels_folder):
    exit(1)

os.makedirs(output_folder, exist_ok=True)

image_names = {os.path.splitext(f)[0] for f in os.listdir(images_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))}

for txt_file in os.listdir(labels_folder):
    if txt_file.lower().endswith(".txt"):
        txt_name = os.path.splitext(txt_file)[0]
        if txt_name in image_names:
            shutil.copy(os.path.join(labels_folder, txt_file), os.path.join(output_folder, txt_file))

print("Filtered label files copied successfully!")
