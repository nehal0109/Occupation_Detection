import os

label_folder = 'C:/Users/Nehal Jain/projects/project_sem6/ImageOccupationPredictor/final/val/labels'
image_folder = 'C:/Users/Nehal Jain/projects/project_sem6/ImageOccupationPredictor/final/val/images'

for file_name in os.listdir(label_folder):
    label_file_path = os.path.join(label_folder, file_name)

    if label_file_path.endswith('.txt'):
        is_valid = True

        with open(label_file_path, 'r') as f:
            for line in f:
                class_idx = int(line.split()[0])
                if class_idx >= 22:
                    is_valid = False
                    break

        if not is_valid:
            image_file_path = os.path.join(image_folder, file_name.replace('.txt', '.jpg'))

            os.remove(label_file_path)
            os.remove(image_file_path)

            print(f"Deleted invalid files: {file_name} and corresponding image.")
