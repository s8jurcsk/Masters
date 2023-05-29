from ultralytics import YOLO

# There are multiple different versions for YOLO models
# Such as YOLOv8n (which stands for nano) YOLOv8s (which stands for small)
# YOLOv8m (which stands for medium) YOLOv8l (which stands for l) and YOLOv8x (which stands for extra large)
# The Author ended up using YOLOv8m since it is the middle model.
model = YOLO("yolov8x.pt")

if __name__ == '__main__':
    results = model.train(
        data="config.yaml",
        epochs=1,
        device=(0),
        #batch=8
    )


# Train18 - Model used YOLOv8m weights | Trained For 1 Epoch | CPU | 5000 IMG
# Train19 - Model used YOLOv8m weights | Trained For 20 Epoch | CPU | 5000 IMG
# Train26 - Model used YOLOv8m weights | Trained For 300(Only Did 50) Epoch | GPU | 5000 IMG
# Train28 - Model used YOLOv8m weights | Trained For 200(Only Did 146) Epoch | GPU | 25000 IMG
# Train31 - Model used YOLOv8x weights | Trained For 130 Epoch | GPU | 25000 IMG
