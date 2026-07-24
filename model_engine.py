import torch
import torchvision.transforms as transforms
from torchvision.models import resnet18, ResNet18_Weights
from PIL import Image
import numpy as np
import os
import matplotlib.cm as cm

from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image

# 1. Define Model Classes (e.g., Binary Chest X-Ray Diagnosis)
CLASS_NAMES = ["NORMAL", "PNEUMONIA"]

def load_model():
    """
    Loads a pre-trained ResNet-18 model and sets it to evaluation mode.
    """
    weights = ResNet18_Weights.DEFAULT
    model = resnet18(weights=weights)
    
    # Adjust output layer for 2 target classes (NORMAL vs PNEUMONIA)
    num_ftrs = model.fc.in_features
    model.fc = torch.nn.Linear(num_ftrs, len(CLASS_NAMES))
    
    model.eval()
    return model

# 2. Image Preprocessing Transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                         std=[0.229, 0.224, 0.225])
])

def analyze_image(image_path: str, output_cam_path: str = "gradcam_output.jpg"):
    """
    Performs DL model inference and generates a Grad-CAM heatmap visualization.
    """
    # Load and process image
    raw_img = Image.open(image_path).convert("RGB")
    rgb_img_resized = raw_img.resize((224, 224))
    
    # Prepare image tensor for PyTorch model
    input_tensor = transform(raw_img).unsqueeze(0)  # Shape: [1, 3, 224, 224]
    
    # Load Model
    model = load_model()
    
    # Run Inference
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
        predicted_idx = torch.argmax(probabilities).item()
        confidence = probabilities[predicted_idx].item()
    
    predicted_label = CLASS_NAMES[predicted_idx]
    
    # Generate Grad-CAM Explanation
    # Target final convolutional layer in ResNet-18
    target_layers = [model.layer4[-1]]
    
    # Prepare RGB float image array normalized to [0, 1] for Grad-CAM overlay
    rgb_float_img = np.float32(rgb_img_resized) / 255.0
    
    cam = GradCAM(model=model, target_layers=target_layers)
    targets = [ClassifierOutputTarget(predicted_idx)]
    
    # Generate heatmap array
    grayscale_cam = cam(input_tensor=input_tensor, targets=targets)[0]
    
    # Superimpose heatmap onto original image (returns uint8 numpy array in RGB)
    visualization = show_cam_on_image(rgb_float_img, grayscale_cam, use_rgb=True)
    
    # Save visual artifact using PIL instead of OpenCV
    cam_pil_img = Image.fromarray(visualization)
    cam_pil_img.save(output_cam_path)
    
    return {
        "prediction": predicted_label,
        "confidence": float(confidence),
        "cam_image_path": output_cam_path
    }

# Quick Test Script Execution
if __name__ == "__main__":
    print("Initializing Model Engine & XAI Module...")
    # Create a dummy image to verify execution end-to-end
    dummy_img = Image.new("RGB", (300, 300), color="gray")
    dummy_img.save("test_xray.jpg")
    
    result = analyze_image("test_xray.jpg")
    print("\n--- Phase 1 Test Successful ---")
    print(f"Predicted Diagnosis : {result['prediction']}")
    print(f"Confidence Score    : {result['confidence']:.2%}")
    print(f"Grad-CAM Heatmap    : Saved to '{result['cam_image_path']}'")