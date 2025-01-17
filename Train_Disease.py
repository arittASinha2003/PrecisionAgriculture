import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from utils.model import ResNet9  # Assuming ResNet9 is defined in utils/model.py

# Set device (use GPU if available)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Data transformations (resize, normalization)
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Load training and validation data
train_data = datasets.ImageFolder('Data/New Plant Diseases Dataset(Augmented)/train', transform=transform)
valid_data = datasets.ImageFolder('Data/New Plant Diseases Dataset(Augmented)/valid', transform=transform)

train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
valid_loader = DataLoader(valid_data, batch_size=32)

# Initialize the model (ResNet9 with the number of disease classes)
disease_classes = train_data.classes  # Get disease class names from subfolder names
num_classes = len(disease_classes)

model = ResNet9(3, num_classes)  # Assuming ResNet9 is defined with 3 input channels and `num_classes` output classes
model.to(device)

# Define the loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
epochs = 10
best_valid_acc = 0.0  # To keep track of the best validation accuracy

for epoch in range(epochs):
    model.train()  # Set model to training mode
    running_loss = 0.0
    correct_preds = 0
    total_preds = 0

    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()

        # Forward pass
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        # Backward pass and optimization
        loss.backward()
        optimizer.step()

        # Track loss and accuracy
        running_loss += loss.item()
        _, preds = torch.max(outputs, 1)
        correct_preds += (preds == labels).sum().item()
        total_preds += labels.size(0)

    epoch_loss = running_loss / len(train_loader)
    epoch_acc = correct_preds / total_preds
    print(f"Epoch [{epoch+1}/{epochs}], Loss: {epoch_loss:.4f}, Accuracy: {epoch_acc:.4f}")

    # Validation phase
    model.eval()  # Set model to evaluation mode
    valid_correct_preds = 0
    valid_total_preds = 0

    with torch.no_grad():
        for inputs, labels in valid_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            # Forward pass
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            valid_correct_preds += (preds == labels).sum().item()
            valid_total_preds += labels.size(0)

    valid_acc = valid_correct_preds / valid_total_preds
    print(f"Validation Accuracy: {valid_acc:.4f}")

    # Save the model if validation accuracy improves
    if valid_acc > best_valid_acc:
        best_valid_acc = valid_acc
        torch.save(model.state_dict(), 'models/plant_disease_model_v2.pth')
        print(f"Model saved with validation accuracy: {valid_acc:.4f}")

print(f"Best validation accuracy: {best_valid_acc:.4f}")
