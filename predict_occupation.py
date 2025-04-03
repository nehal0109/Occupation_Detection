import gradio as gr
import torch
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier
from ultralytics import YOLO

OCCUPATION_OBJECT_MAPPING = {
    'teacher': ['book', 'chair', 'desk', 'whiteboard', 'laptop', 'person'],
    'photographer': ['dslr-camera', 'tripod', 'bagpack', 'umbrella', 'person'],
    'chef': ['knife', 'microwave', 'oven', 'refrigerator', 'spoon', 'fork', 'person'],
    'doctor': ['stethoscope', 'syringe', 'person'],
    'mechanic': ['wrench', 'hammer', 'car', 'tire', 'person'],
    'cyclist': ['bicycle', 'person', 'construction-helmet'],
    'farmer': ['tractor', 'cow', 'sheep', 'person'],
    'construction_worker': ['construction-helmet', 'hammer', 'person'],
    'athlete': ['stumps', 'cricket-bat', 'construction-helmet', 'person'],
    'musician': ['guitar', 'keyboard', 'drum', 'person', 'piano'],
    'waiter': ['wine glass', 'fork', 'knife', 'person', 'bottle', 'spoon'],
    'barber': ['scissors', 'comb', 'razor', 'chair', 'person'],
    'police_officer': ['person', 'handcuffs', 'gun', 'car'],
    'librarian': ['book', 'shelf', 'laptop', 'desk', 'chair'],
    'tailor': ['scissors', 'person', 'sewing machine'],
    'gardener': ['person', 'potted plant'],
    'office_worker': ['laptop', 'desk', 'chair', 'keyboard', 'mouse', 'person', 'bottle'],
    'salesperson': ['person', 'laptop', 'desk', 'chair', 'book', 'bagpack'],
    'cleaner': ['mop', 'broom', 'bucket', 'green-dustbin', 'person'],
    'student': ['backpack', 'person', 'laptop', 'book', 'bottle'],
    'cricketer': ['stumps', 'person', 'cricket-bat', 'construction-helmet', 'sports ball'],
    'swimmer': ['swimming-goggles', 'person'],
    'policeman': ['person', 'gun', 'handcuffs'],
    'driver': ['car', 'person', 'motorcycle', 'tire'],
    'nurse': ['stethoscope', 'syringe', 'person'],
}

class OccupationPredictor:
    def __init__(self):
        self.fine_tuned_model = YOLO("runs/detect/train_continued/weights/best.pt")
        self.original_model = YOLO("yolov8s.pt")
        self.mlb = MultiLabelBinarizer()
        self.min_confidence_threshold = 0.30
        self.prepare_training_data()

    def prepare_training_data(self):
        X, y = [], []
        all_objects = list(set(obj for objects in OCCUPATION_OBJECT_MAPPING.values() for obj in objects))
        for occupation, objects in OCCUPATION_OBJECT_MAPPING.items():
            for _ in range(70):
                num_objects = np.random.randint(max(1, len(objects) // 3), min(len(objects), 5) + 1)
                selected_objects = np.random.choice(objects, size=num_objects, replace=False)
                if np.random.random() < 0.7:
                    irrelevant_objects = [obj for obj in all_objects if obj not in objects]
                    if irrelevant_objects:
                        noise_objects = np.random.choice(irrelevant_objects, size=min(np.random.randint(0, 3), len(irrelevant_objects)), replace=False)
                        selected_objects = np.append(selected_objects, noise_objects)
                X.append(selected_objects)
                y.append(occupation)
        X_transformed = self.mlb.fit_transform(X)
        self.classifier = RandomForestClassifier(n_estimators=200, class_weight='balanced', random_state=42)
        self.classifier.fit(X_transformed, y)

    def detect_objects(self, img_path):
        detected_objects = set()
        for model in [self.fine_tuned_model, self.original_model]:
            for det in model(img_path)[0].boxes.data.cpu().numpy():
                detected_objects.add(model.names[int(det[5])].lower())
        return list(detected_objects)

    def predict_occupation(self, detected_objects):
        X_test = self.mlb.transform([[obj for obj in detected_objects]])
        base_probabilities = self.classifier.predict_proba(X_test)[0]
        weighted_scores = {occ: base_probabilities[i] for i, occ in enumerate(self.classifier.classes_)}
        total_score = sum(weighted_scores.values()) or 1
        weighted_scores = {occ: score / total_score for occ, score in weighted_scores.items()}
        top_predictions = sorted(weighted_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        if top_predictions[0][1] < self.min_confidence_threshold:
            return [("Not enough information", 1.0)]
        return top_predictions

predictor = OccupationPredictor()

def gradio_interface(image):
    detected_objects = predictor.detect_objects(image)
    predictions = predictor.predict_occupation(detected_objects)
    detected_objects_str = "Detected Objects:\n" + ", ".join(detected_objects)
    occupation_prediction_str = "\nTop Predicted Occupations:\n"
    if predictions[0][0] == "Not enough information":
        occupation_prediction_str += "Not enough information to make a confident prediction.\nTry adding more relevant objects to the scene."
    else:
        for occupation, probability in predictions:
            occupation_prediction_str += f"{occupation}: {probability * 100:.2f}%\n"
    return detected_objects_str, occupation_prediction_str

iface = gr.Interface(
    fn=gradio_interface,
    inputs=gr.Image(type="pil", label="Upload or Take a Picture"),
    outputs=[
        gr.Textbox(label="Detected Objects", interactive=False),
        gr.Textbox(label="Predicted Occupation", interactive=False)
    ],
    title="Enhanced Occupation Detector",
    description="Upload or take a picture to detect objects and predict the occupation based on those objects.",
    theme="compact",
    css=".footer {display:none}",
)

if __name__ == "__main__":
    iface.launch()
