import os
from ultralytics import YOLO

project_dir = os.getcwd()
yaml_file = os.path.join(project_dir, 'final', 'data.yaml')

pretrained_weights = os.path.join(project_dir, 'runs', 'detect', 'train', 'weights', 'last.pt')

model = YOLO(pretrained_weights)

model.train(
    data=yaml_file,
    epochs=10,
    batch=8,
    imgsz=512,
    workers=2,
    device='cpu',
    lr0=0.01,
    lrf=0.001,
    momentum=0.95,
    weight_decay=0.0001,
    optimizer='auto',
    patience=5,
    val=True,
    resume=False,
    pretrained=True,
    name='train_continued'
)
