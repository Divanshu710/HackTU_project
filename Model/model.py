import torch
from torchvision.models import resnet18
from torchvision import transforms
import torch.nn as nn
from PIL import Image

# Load the pre-trained ResNet18 model
model = resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, 2)  # Modify for binary classification
model.eval()

# Load and preprocess the image
image_path = "banana.jpg"
input_image = Image.open(image_path).convert('RGB')
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
input_tensor = preprocess(input_image)
input_batch = input_tensor.unsqueeze(0)

# Perform inference
with torch.no_grad():
    output = model(input_batch)

# Load class labels
with open('imagenet_classes.txt', 'r') as file:
    labels = [line.strip() for line in file.readlines()]


# Get the predicted class index
_, predicted_idx = torch.max(output, 1)

predicted_label = labels[predicted_idx.item()]

print(f"The predicted class is: {predicted_label}")
