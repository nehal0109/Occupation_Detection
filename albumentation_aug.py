import cv2
import os
import albumentations as A

INPUT_IMAGE_DIR = r"C:\Users\Nehal Jain\projects\project_sem6\ImageOccupationPredictor\final\train\images"
INPUT_LABEL_DIR = r"C:\Users\Nehal Jain\projects\project_sem6\ImageOccupationPredictor\final\train\labels"
OUTPUT_IMAGE_DIR = r"C:\Users\Nehal Jain\projects\project_sem6\ImageOccupationPredictor\final\train_augmented\images"
OUTPUT_LABEL_DIR = r"C:\Users\Nehal Jain\projects\project_sem6\ImageOccupationPredictor\final\train_augmented\labels"

AUG_PER_IMAGE = 5

os.makedirs(OUTPUT_IMAGE_DIR, exist_ok=True)
os.makedirs(OUTPUT_LABEL_DIR, exist_ok=True)

transform = A.Compose([
    A.HorizontalFlip(p=0.6),
    A.VerticalFlip(p=0.3),
    A.Rotate(limit=15, p=0.4),
    A.RandomScale(scale_limit=0.3, p=0.5),
    A.RandomResizedCrop(size=(640, 640), scale=(0.6, 1.0), p=0.4),
    A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.3, p=0.7),
    A.RGBShift(r_shift_limit=15, g_shift_limit=15, b_shift_limit=15, p=0.5),
    A.CLAHE(p=0.4),
    A.HueSaturationValue(hue_shift_limit=10, sat_shift_limit=20, val_shift_limit=10, p=0.4),
    A.GaussianBlur(blur_limit=(3, 7), p=0.4),
    A.CoarseDropout(max_holes=8, max_height=20, max_width=20, fill_value=0, p=0.5),
    A.RandomShadow(p=0.3),
    A.ElasticTransform(alpha=30, sigma=5, p=0.3),
    A.GridDistortion(p=0.2)
], bbox_params=A.BboxParams(
    format='yolo',
    min_visibility=0.3,
    min_area=0.0001,
    label_fields=['class_labels'],
    check_each_transform=False
))

def clean_filename(filename):
    return filename.strip().replace('\ufeff', '').lower()

def main():
    image_files = {clean_filename(f): f for f in os.listdir(INPUT_IMAGE_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))}
    label_files = {clean_filename(f): f for f in os.listdir(INPUT_LABEL_DIR) if f.lower().endswith('.txt')}

    print(f"Total images found: {len(image_files)}")
    print(f"Total labels found: {len(label_files)}")
    print("Sample image keys:", list(image_files.keys())[:5])
    print("Sample label keys:", list(label_files.keys())[:5])

    image_count = 0
    aug_count = 0

    for img_clean, img_name in image_files.items():
        base_name = os.path.splitext(img_clean)[0]
        expected_label = base_name + ".txt"

        if expected_label not in label_files:
            print(f"Warning: No matching label file for {img_name}, skipping.")
            continue

        image_path = os.path.join(INPUT_IMAGE_DIR, img_name)
        label_path = os.path.join(INPUT_LABEL_DIR, label_files[expected_label])

        image = cv2.imread(image_path)
        if image is None:
            print(f"Warning: Cannot read {img_name}, skipping.")
            continue
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        orig_h, orig_w = image.shape[:2]

        with open(label_path, 'r', encoding='utf-8-sig') as f:
            lines = [line.strip() for line in f if line.strip()]
        if not lines:
            print(f"Warning: Empty label file for {img_name}, skipping.")
            continue

        bboxes, labels = [], []
        for line in lines:
            parts = line.split()
            if len(parts) != 5:
                print(f"Warning: Invalid format in {expected_label}, skipping line.")
                continue
            labels.append(int(parts[0]))
            bbox = list(map(float, parts[1:5]))
            bboxes.append(bbox)

        if not bboxes:
            print(f"Warning: No valid bounding boxes in {img_name}, skipping.")
            continue

        print(f"Processing {img_name} with original boxes: {bboxes}")
        image_count += 1

        for i in range(AUG_PER_IMAGE):
            try:
                augmented = transform(image=image, bboxes=bboxes, class_labels=labels)
            except Exception as e:
                print(f"Warning: Augmentation failed for {img_name} (aug #{i}): {e}")
                continue

            if not augmented['bboxes']:
                print(f"Warning: No valid boxes after augmentation for {img_name} (aug #{i}), skipping.")
                continue

            print(f"Transformed boxes for {img_name} (aug #{i}): {augmented['bboxes']}")

            aug_img = augmented['image']
            new_h, new_w = aug_img.shape[:2]
            aug_bboxes = augmented['bboxes']
            aug_labels = augmented['class_labels']

            yolo_boxes = []
            for bbox, cls_id in zip(aug_bboxes, aug_labels):
                yolo_boxes.append(f"{cls_id} {bbox[0]:.6f} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f}")

            aug_img_name = f"{os.path.splitext(img_name)[0]}_aug{i}.jpg"
            aug_label_name = f"{os.path.splitext(img_name)[0]}_aug{i}.txt"

            cv2.imwrite(os.path.join(OUTPUT_IMAGE_DIR, aug_img_name), cv2.cvtColor(aug_img, cv2.COLOR_RGB2BGR))
            with open(os.path.join(OUTPUT_LABEL_DIR, aug_label_name), 'w') as f:
                f.write("\n".join(yolo_boxes))

            aug_count += 1

    print(f"Augmentation complete! Processed {image_count} images and created {aug_count} augmentations.")

if __name__ == "__main__":
    main()
